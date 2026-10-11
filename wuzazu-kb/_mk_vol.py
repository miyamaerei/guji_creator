# -*- coding: utf-8 -*-
"""统一卷源落盘器：校验 → 原子写入 → 自动摊平 → 可选打包。

AI 产出的统一卷源先过一遍**机器校验**再落盘，把格式错误挡在打包器之前，
避免"跑完 14 个阶段才发现条号臆造/枚举写错"。

用法：
    # 校验并落盘（默认不跑打包）
    python _mk_vol.py 01 _src/_vol_01.py

    # 落盘 + 立刻打包验证
    python _mk_vol.py 01 _src/_vol_01.py --build

    # 从 stdin 读（AI 直接管道输出）
    cat raw.py | python _mk_vol.py 01 -

校验项（对应 _vol_prompt.py 的自检清单）：
    1. 合法 Python + 顶层 SRC/RECORDS/DATA 字典
    2. 外层 key 是有效条号且存在于 _item_registry.json
    3. 无业务 ID / original / norm / volume / *_ent_ids 等禁写键
    4. 枚举值合法（复用 _kg_enums，未知值照旧进 pending 不阻断）
    5. 未考处字段不落空串
    6. 摊平后各层记录数与统一卷源一致
"""

from __future__ import annotations

import io
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

import _kg_enums as E  # noqa: E402
from _kg_pack_base import UNKNOWN, load_registry, read_text, write_text  # noqa: E402
import _vol_schema as V  # noqa: E402
from _vol_prompt import FIELD_ENUM, MUST  # noqa: E402

# 禁写键：这些一律由打包器负责，AI 写了就是越权
FORBIDDEN_EXACT = {"original", "norm", "volume", "ent_id", "event_id", "rel_id",
                   "nam_id", "cit_id", "obj_id", "cus_id", "opn_id", "ming_id",
                   "appointment_id", "trl_id"}
FORBIDDEN_PREFIX = ("ENT-", "WZZ-E-", "REL-", "NAM-", "CIT-", "OBJ-",
                    "CUS-", "OPN-", "MING-", "APPT-", "TRL-")
FORBIDDEN_SUFFIX = ("_ent_ids",)


def _scan_keys(obj, path: str = "") -> list[tuple[str, object]]:
    """深度遍历，收集所有键。"""
    found: list[tuple[str, object]] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            found.append((f"{path}.{k}", v))
            found.extend(_scan_keys(v, f"{path}.{k}"))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            found.extend(_scan_keys(v, f"{path}[{i}]"))
    return found


def _forbidden(key_path: str, value) -> str | None:
    key = key_path.rsplit(".", 1)[-1].split("[")[0]
    if key in FORBIDDEN_EXACT:
        return f"禁写键 {key}（由打包器负责）"
    if key.endswith(FORBIDDEN_SUFFIX):
        return f"禁写键 {key}（跨层回填由打包器负责，只写词形）"
    if isinstance(value, str):
        for pfx in FORBIDDEN_PREFIX:
            if value.startswith(pfx) and len(value) > len(pfx):
                return f"疑似手写业务 ID：{value}"
    return None


def validate(volume: str, text: str) -> tuple[list[str], list[str], dict | None]:
    """返回 (errors, warnings, parsed_dict)。"""
    errors: list[str] = []
    warnings: list[str] = []

    # 1. 语法
    try:
        compile(text, f"_vol_{volume}.py", "exec")
    except SyntaxError as e:
        return [f"语法错误：第 {e.lineno} 行 {e.msg}"], [], None

    ns: dict = {"__file__": f"_vol_{volume}.py", "__name__": f"_vol_{volume}"}
    try:
        exec(compile(text, f"_vol_{volume}.py", "exec"), ns)  # noqa: S102
    except Exception as e:                                    # noqa: BLE001
        return [f"执行失败：{type(e).__name__}: {e}"], [], None

    data = None
    for key in V.VOL_KEYS:
        if isinstance(ns.get(key), dict):
            data = ns[key]
            break
    if data is None:
        return [f"缺少顶层字典：需要 {' / '.join(V.VOL_KEYS)}"], [], None
    if not data:
        return ["SRC 为空"], [], data

    # 2. 条号有效性
    registry = load_registry()
    vol_items = {i for i, _ in V.registry_items(volume)}
    for item_id in data:
        if not re.fullmatch(r"\d{2}-\d{3}", str(item_id)):
            errors.append(f"条号格式非法：{item_id}（应为 NN-NNN）")
        elif str(item_id) not in registry:
            hint = "（本卷无此条）" if str(item_id) in {
                i for i in registry if i[:2] == volume[:2]} else ""
            errors.append(f"条号不在指纹库：{item_id}{hint}")

    # 3. 禁写键 + 枚举 + 空串
    n_records = 0
    for key_path, value in _scan_keys(data):
        bad = _forbidden(key_path, value)
        if bad:
            errors.append(f"{key_path}：{bad}")

    for item_id, layers in data.items():
        if not isinstance(layers, dict):
            errors.append(f"{item_id}：层容器必须是 dict")
            continue
        for layer, payload in layers.items():
            if layer not in V.LAYERS:
                errors.append(f"{item_id}.{layer}：未知层名"
                              f"（合法：{'/'.join(V.LAYERS)}）")
                continue
            rows = V._normalize_layer_value(layer, payload)
            if layer == "trl":
                for row in rows:
                    for dk, dv in V.TRL_DEFAULTS.items():
                        row.setdefault(dk, dv)
            n_records += len(rows)
            for i, row in enumerate(rows):
                where = f"{item_id}.{layer}[{i}]"
                # 必填缺失
                for mf in MUST.get(layer, ()):
                    if mf in row:
                        continue
                    # trl 可用简写字符串已被展开为 translation
                    if row.get(mf) in ("", None):
                        warnings.append(f"{where}：必填 {mf} 为空")
                # 枚举校验：跨字段串值（如把 citation_type 的值写进 context）
                # 是装填最常见错法，且 validate_layers 会判 error —— 这里直接挡在落盘前
                for field, enum_name in FIELD_ENUM.get(layer, {}).items():
                    if field not in row:
                        continue
                    val = row[field]
                    if isinstance(val, (dict, list)):
                        continue
                    if str(val) == UNKNOWN:
                        continue
                    _, bad_enum = E.validate(enum_name, val, where=where)
                    if bad_enum:
                        legal = " / ".join(E.canonical_values(enum_name))
                        # 值合法但放错字段是装填最常见错法，给出定位提示
                        hint = ""
                        for ln, m in FIELD_ENUM.items():
                            if ln == layer:
                                continue
                            for lf, le in m.items():
                                if lf == field and le in E.enum_names() \
                                        and val in E.canonical_values(le):
                                    hint = (f"　提示：「{val}」是 {ln}.{field} "
                                            f"的合法值，不是 {layer}.{field}")
                                    break
                            if hint:
                                break
                        errors.append(f"{where}.{field}：枚举外值「{bad_enum}」"
                                      f"（合法值：{legal}）{hint}")
                # 未考处显式未明
                for field in ("when", "where"):
                    if field in row and row[field] == "":
                        warnings.append(f"{where}.{field}：未考处应写 "
                                        f"\"{UNKNOWN}\" 而非空串")

    if n_records == 0:
        warnings.append("没有任何记录")
    return errors, warnings, data


def main() -> None:
    argv = sys.argv[1:]
    do_build = "--build" in argv
    argv = [a for a in argv if not a.startswith("--")]
    if len(argv) < 2:
        print(__doc__)
        raise SystemExit(2)

    volume = argv[0].zfill(2)
    src = argv[1]
    text = sys.stdin.read() if src == "-" else read_text(src)

    print("=" * 68)
    print(f"统一卷源落盘校验　卷{volume}　来源：{src}")
    print("=" * 68)

    errors, warnings, data = validate(volume, text)

    for w in warnings[:20]:
        print(f"  [警告] {w}")
    if len(warnings) > 20:
        print(f"  …另有 {len(warnings) - 20} 条警告")
    for e in errors[:20]:
        print(f"  [错误] {e}")
    if len(errors) > 20:
        print(f"  …另有 {len(errors) - 20} 条错误")

    if errors:
        print(f"\n[中止] {len(errors)} 个错误，未落盘。修正后重试。")
        raise SystemExit(1)

    target = V.volume_source_path(volume)
    write_text(target, text)
    n_items = len(data or {})
    print(f"\n[落盘] {target}（{n_items} 条目 / "
          f"{sum(len(v) for b in (data or {}).values() if isinstance(b, dict) for v in b.values()):,} 层记录）")

    # py_compile 复核
    proc = subprocess.run([sys.executable, "-m", "py_compile", str(target)],
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace")
    print(f"[语法] py_compile {'通过' if proc.returncode == 0 else '失败：' + proc.stderr[:200]}")

    # 摊平
    counts = V.split(volume)
    total = sum(counts.values())
    print(f"[摊平] {total} 条 → " +
          " ".join(f"{k}={v}" for k, v in counts.items() if v))

    if do_build:
        print("\n[打包] 跑 build_all --volumes " + volume)
        proc = subprocess.run(
            [sys.executable, str(ROOT / "build_all.py"), "--volumes", volume],
            cwd=str(ROOT), capture_output=True, text=True,
            encoding="utf-8", errors="replace")
        tail = (proc.stdout or "").strip().splitlines()[-12:]
        for line in tail:
            print("    " + line)
        print(f"[打包] exit={proc.returncode}")
        raise SystemExit(proc.returncode)

    print("\n[下一步] python build_all.py --volumes " + volume)


if __name__ == "__main__":
    main()