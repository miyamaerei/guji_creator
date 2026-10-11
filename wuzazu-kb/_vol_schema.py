# -*- coding: utf-8 -*-
"""《五杂俎》知识工程 | 统一卷源（unified volume source）—— 按卷扇出的低成本装填格式

为什么有这层
------------
旧做法是"按层扇出"：11 层 × N 卷 = 11N 次AI 调用，同一份原文被反复读取 11 次。
实测卷01+02（`_src/_index_01_02.md`，85823 字符）仅这一份原文就被 22 个 agent 各读一遍，
叠加34K 字符的 skill 包与 P0→P3 的串行回读，全书 token 量放大到千万级。

新做法是"按卷扇出"：**一个卷一次 AI 调用，一次产全部 11 层**，原文只读 1 遍。
层与层的引用关系（who→ent_ids 等）不再需要 AI 记住前面层的产物，
由打包器在`_kg_layers.resolve_refs` 里统一回填——这本来就是它的工作。

本模块只做两件事，且**不改动任何打包器/验证器**：

1. `_vol_contract(volume) -> dict[item_id, dict[layer, list[record]]]`
   读 `_src/_vol_<NN>.py` 里的 `SRC` 字典，得到"条目 → 各层记录"的统一视图。
2. `split(volume)` 把统一卷源**摊平**成打包器要的 11 个 `_src/_<layer>_ai_<NN>.py`
   （每个仍是老格式 `RECORDS = [...]`），因此下游 `build_*.py` / `validate_*.py` /
   `_kg_entity.py` 全部零改动、行为不变。

反向操作 `merge(volume)`：把 11 个分层文件折回一个 `_vol_<NN>.py`，
用于迁移存量数据（`_src/_ent_ai_01.py` 等已装填的层）与跨层一致性巡检。

统一卷源形状（唯一手写/AI 产出区）
--------------------------------
```python
SRC = {
  "01-001": {                      # 条号，与 _item_registry.json 的 key 严格一致
    "ent":   [("老子", "person", "老子（指老聃）")],        # 紧凑元组：text, type, normalized?
    "event": [{"type": "文事", "who": "老子", "action": "…", "what": "…",
               "when": "未明", "where": "未明"}],
    "rel":   [("甲", "乙", "同僚", "双向", "证据原文")],
    "trl":   "译文正文",            # 字符串 = 一条；也可写 list[dict] 走完整契约
    # 无材料的层整个键省略，不要写空 list
  },
}
```

紧凑元组 = 省 token 的关键：11 层里最密的 ent/rel/cit 三层用元组代替 dict，
每条省下 `"item_id": …,` 与重复键名约 30~40% 输出字符。

不写：业务 ID（ENT-/WZZ-E-… 由打包器分配）、original/norm（指纹库注入）、
volume（由文件名推导）、ent_ids（回填）。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

from _kg_pack_base import (  # noqa: E402
    ALL_VOLUMES,
    SRC_DIR,
    VOLUME_NAME,
    ensure_dirs,
    read_text,
    registry_items,
    write_text,
)

# 与 _kg_pack_base.LAYERS 的层名保持一致（打包器口径的唯一真源）
LAYERS: tuple[str, ...] = (
    "ent", "event", "rel", "nam", "cit",
    "obj", "cus", "opn", "ming", "appt", "trl",
)

# 分层文件名（拆分的输出目标）
def layer_source_path(layer: str, volume: str) -> Path:
    return SRC_DIR / f"_{layer}_ai_{volume}.py"


def volume_source_path(volume: str) -> Path:
    return SRC_DIR / f"_vol_{volume}.py"


# --------------------------------------------------------------------------
# 1. 紧凑元组 → 完整记录（摊平前的展开）
# --------------------------------------------------------------------------

# 各层的紧凑元组字段顺序，None 表示该位置可省略。
# 顺序必须与 _kg_layers.ENGINE 的字段语义一一对应。
TUPLE_FIELDS: dict[str, tuple[tuple[str, ...], str | None]] = {
    # ent: (text, type) 或 (text, type, normalized)
    "ent": (("text", "type", "normalized"), "normalized"),
    # rel: (person_a, person_b, relation_type, direction, evidence)
    "rel": (("person_a", "person_b", "relation_type", "direction", "evidence"), None),
    # cit: (cited_work, citation_type, context)
    "cit": (("cited_work", "citation_type", "context"), None),
}


def _expand_tuple(layer: str, item: Any) -> dict:
    """紧凑元组 → 完整 dict。非元组原样返回。"""
    fields = TUPLE_FIELDS.get(layer)
    if not fields or not isinstance(item, (list, tuple)):
        return dict(item) if isinstance(item, dict) else {"_raw": item}
    names = fields[0]
    out: dict[str, Any] = {}
    for i, key in enumerate(names):
        if i >= len(item):
            break
        value = item[i]
        if value in (None, "") and key != fields[1]:
            # 必填位缺省 → 留给打包器补"未明"，不写脏值
            continue
        out[key] = value
    return out


def _normalize_layer_value(layer: str, value: Any) -> list[dict]:
    """一层的值统一成 list[dict]（兼容 str / dict / 元组 / list）。"""
    if value in (None, "", [], {}):
        return []
    if isinstance(value, str):                       # trl 简写：整段译文
        return [{"translation": value}]
    if isinstance(value, dict):                      # 单条
        return [_expand_tuple(layer, value)]
    if isinstance(value, (list, tuple)):
        # trl 的 list[str] = 多条纯译文
        if layer == "trl" and all(isinstance(x, str) for x in value):
            return [{"translation": x} for x in value]
        return [_expand_tuple(layer, x) for x in value]
    return []


# trl 的字符串简写（"译文正文"）落地时补的默认字段。
# style / confidence 是必填（前者枚举 trl_style），但不逐条手写：
# 译文层按 style 基准统一归一，由打包器 `_apply_fallbacks` 兜 note，
# 这里只补 style 与 confidence 的缺省值。
TRL_DEFAULTS: dict[str, Any] = {"style": "注释性翻译", "confidence": "high"}


# --------------------------------------------------------------------------
# 2. 读统一卷源
# --------------------------------------------------------------------------

VOL_KEYS = ("SRC", "RECORDS", "DATA")


def load_volume(volume: str) -> dict[str, dict[str, list[dict]]]:
    """读 `_src/_vol_<NN>.py`，返回 {item_id: {layer: [record, ...]}}。"""
    p = volume_source_path(volume)
    if not p.exists():
        return {}
    ns: dict = {"__file__": str(p), "__name__": f"_vol_{volume}"}
    exec(compile(read_text(p), str(p), "exec"), ns)  # noqa: S102 - 本地可信源数据
    raw = None
    for key in VOL_KEYS:
        if isinstance(ns.get(key), dict):
            raw = ns[key]
            break
    if raw is None:
        raise TypeError(f"{p} 缺少顶层字典：需要 {' / '.join(VOL_KEYS)}")
    out: dict[str, dict[str, list[dict]]] = {}
    for item_id, layers in raw.items():
        item_id = str(item_id).strip()
        if not isinstance(layers, dict):
            continue
        bucket: dict[str, list[dict]] = {}
        for layer, value in layers.items():
            if layer not in LAYERS:
                continue
            rows = _normalize_layer_value(layer, value)
            for row in rows:
                row["item_id"] = item_id      # 条号以统一卷源的 key 为准
                if layer == "trl":
                    for k, dv in TRL_DEFAULTS.items():
                        row.setdefault(k, dv)
            if rows:
                bucket[layer] = rows
        if bucket:
            out[item_id] = bucket
    return out


def have_volume(volume: str) -> bool:
    return volume_source_path(volume).exists()


# --------------------------------------------------------------------------
# 3.摊平：统一卷源 → 11 个分层文件（打包器的老格式，零改动兼容）
# --------------------------------------------------------------------------

def _render_records(records: list[dict]) -> str:
    """渲染成打包器可读的 Python 字面量（RECORDS = [...]）。"""
    import json
    body = json.dumps(records, ensure_ascii=False, indent=4)
    return "RECORDS = " + body + "\n"


def split(volume: str, *, write: bool = True) -> dict[str, int]:
    """把 `_vol_<NN>.py` 摊平成 11 个 `_<layer>_ai_<NN>.py`。

    返回 {layer: 记录数}。某层没有材料就不产出文件（打包器据此跳过该层该卷）。
    """
    data = load_volume(volume)
    counts: dict[str, int] = {}
    if write:
        ensure_dirs()
    for layer in LAYERS:
        rows: list[dict] = []
        for item_id in sorted(data, key=_item_sort_key):
            rows.extend(data[item_id].get(layer, []))
        if not rows:
            # 空层：清掉旧文件，避免 stale 数据混入打包
            p = layer_source_path(layer, volume)
            if write and p.exists():
                p.unlink()
            counts[layer] = 0
            continue
        header = (
            f'"""（自动摊平，勿手改）由 _vol_{volume}.py 拆出。\n'
            f'层：{layer}　卷：{volume} {VOLUME_NAME.get(volume, "")}　'
            f'记录数：{len(rows)}\n'
            f'要改内容请改 _vol_{volume}.py 后重新 python _vol_sync.py split。\n'
            f'"""\n\n'
        )
        if write:
            write_text(layer_source_path(layer, volume),
                       header + _render_records(rows))
        counts[layer] = len(rows)
    return counts


def _item_sort_key(item_id: str) -> tuple:
    try:
        vol, seq = item_id.split("-")
        return (vol, int(seq))
    except ValueError:
        return ("99", 999)


# 判重时忽略的运行时字段（由打包器注入，不参与语义判重）
_VOLATILE_ROW_KEYS = frozenset({"original", "norm", "volume", "start", "end"})


def row_key(row: dict) -> str:
    """记录的内容指纹：按 (item_id, 语义字段) 生成，用于合并时判重。

    忽略 original/norm/volume/start/end —— 这些由指纹库注入或按位置推算，
    不是装填的语义内容。
    """
    return "|".join(
        f"{k}={row[k]!r}"
        for k in sorted(row)
        if k not in _VOLATILE_ROW_KEYS
    )


# --------------------------------------------------------------------------
# 4. 折叠：11 个分层文件 → 统一卷源（迁移存量 / 巡检）
# --------------------------------------------------------------------------

SKIP_KEYS = {"item_id", "id", "ent_id", "event_id", "rel_id", "nam_id",
             "cit_id", "obj_id", "cus_id", "opn_id", "ming_id",
             "appointment_id", "trl_id", "volume", "original", "norm",
             "start", "end"}


def _load_layer_file(layer: str, volume: str) -> list[dict]:
    p = layer_source_path(layer, volume)
    if not p.exists():
        return []
    ns: dict = {"__file__": str(p), "__name__": f"_{layer}_ai_{volume}"}
    exec(compile(read_text(p), str(p), "exec"), ns)  # noqa: S102
    for key in ("RECORDS", f"{layer.upper()}_RECORDS"):
        val = ns.get(key)
        if isinstance(val, list):
            return [dict(r) for r in val if isinstance(r, dict)]
    return []


def merge(volume: str, *, write: bool = True, drop_existing: bool = True) -> dict[str, Any]:
    """把 11 个分层文件折回统一卷源。

    drop_existing=True 时先备份原分层文件到 `_src/_legacy/`，避免不可逆覆盖。
    返回统计 dict。
    """
    merged: dict[str, dict[str, list[dict]]] = {}
    stats: dict[str, int] = {}
    for layer in LAYERS:
        rows = _load_layer_file(layer, volume)
        stats[layer] = len(rows)
        if not rows:
            continue
        for row in rows:
            item_id = str(row.get("item_id") or "").strip()
            if not item_id:
                continue
            clean = {k: v for k, v in row.items() if k not in SKIP_KEYS}
            merged.setdefault(item_id, {}).setdefault(layer, []).append(clean)
    if write and merged:
        ensure_dirs()
        if drop_existing:
            _backup_layer_files(volume, [l for l in LAYERS if stats.get(l)])
        write_text(volume_source_path(volume), render_volume_source(volume, merged))
    return {"volume": volume, "items": len(merged), "per_layer": stats}


def _backup_layer_files(volume: str, layers: list[str]) -> list[str]:
    """把将被覆盖的分层文件备份到 _src/_legacy/（可回滚）。"""
    bak_dir = SRC_DIR / "_legacy"
    bak_dir.mkdir(parents=True, exist_ok=True)
    saved: list[str] = []
    for layer in layers:
        p = layer_source_path(layer, volume)
        if p.exists():
            target = bak_dir / p.name
            target.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
            saved.append(str(target.relative_to(ROOT)))
    return saved


def render_volume_source(volume: str, data: dict[str, dict[str, list[dict]]]) -> str:
    """渲染统一卷源文件（可读优先：按条号分组，层内紧凑元组）。"""
    name = VOLUME_NAME.get(volume, "")
    lines = [
        f'"""《五杂俎》卷{volume}（{name}）统一卷源 —— 11 层一次装填',
        "",
        "形状：SRC[条号][层名] =记录列表；无材料的层整个键省略。",
        "紧凑元组顺序见 _vol_schema.py 的 TUPLE_FIELDS（或 _vol_prompt.py 打印的契约）。",
        "不写：业务 ID / original / norm / volume / ent_ids（打包器负责）。",
        '"""',
        "",
        "SRC = {",
    ]
    for item_id in sorted(data, key=_item_sort_key):
        bucket = data[item_id]
        lines.append(f'"{item_id}": {{')
        for layer in LAYERS:
            rows = bucket.get(layer)
            if not rows:
                continue
            lines.append(f'    "{layer}": {rows!r},')
        lines.append("},")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# 5. 巡检：统一卷源 vs 分层文件一致性
# --------------------------------------------------------------------------

def audit(volume: str) -> dict[str, Any]:
    """比对统一卷源与已摊平的分层文件，找出差异（漂移 / 丢失）。"""
    unified = load_volume(volume)
    diffs: list[dict] = []
    for layer in LAYERS:
        u_rows: list[dict] = []
        for item_id in sorted(unified, key=_item_sort_key):
            u_rows.extend(unified[item_id].get(layer, []))
        f_rows = _load_layer_file(layer, volume)
        if len(u_rows) != len(f_rows):
            diffs.append({"layer": layer, "unified": len(u_rows),
                          "file": len(f_rows), "kind": "count"})
        else:
            for a, b in zip(u_rows, f_rows):
                if a.get("item_id") != b.get("item_id"):
                    diffs.append({"layer": layer, "unified": a.get("item_id"),
                                  "file": b.get("item_id"), "kind": "order"})
                    break
    covered = len(unified)
    total = len(registry_items(volume))
    return {"volume": volume, "name": VOLUME_NAME.get(volume, ""),
            "items_in_source": covered, "items_in_registry": total,
            "coverage": f"{covered}/{total}",
            "missing_items": [i for i, _ in registry_items(volume)
                              if i not in unified],
            "diffs": diffs, "consistent": not diffs}


# --------------------------------------------------------------------------
# 6. CLI
# --------------------------------------------------------------------------

def _parse_volumes(raw: str | None) -> list[str]:
    if not raw:
        return [v for v in ALL_VOLUMES if have_volume(v)]
    vols = [v.strip().zfill(2) for v in raw.replace(",", " ").split() if v.strip()]
    return [v for v in vols if v in VOLUME_NAME]


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    known = {"split", "merge", "audit", "status"}
    cmd = argv[0] if argv and argv[0] in known else "status"
    rest = argv[1:] if cmd in known else argv

    # 兼容 `--volumes 01 02`、`--volumes=01,02`、`01 02` 三种写法
    vols_arg: str | None = None
    for i, token in enumerate(rest):
        if token == "--volumes":
            picked = []
            for nxt in rest[i + 1:]:
                if nxt.startswith("-"):
                    break
                picked.append(nxt)
            vols_arg = " ".join(picked)
            break
        if token.startswith("--volumes="):
            vols_arg = token.split("=", 1)[1]
            break
    if vols_arg is None:
        picked = [t for t in rest if not t.startswith("-") and t[:2].isdigit()]
        vols_arg = " ".join(picked) if picked else None
    vols = _parse_volumes(vols_arg)

    if cmd == "split":
        for v in vols:
            counts = split(v)
            total = sum(counts.values())
            print(f"[split] 卷{v} {VOLUME_NAME.get(v, '')}：{total} 条→ "
                  + " ".join(f"{k}={n}" for k, n in counts.items() if n))
        return

    if cmd == "merge":
        for v in vols:
            r = merge(v)
            print(f"[merge] 卷{v} {VOLUME_NAME.get(v, '')}：{r['items']} 条 → "
                  f"_vol_{v}.py（明细 {r['per_layer']}）")
        return

    if cmd == "audit":
        for v in vols:
            r = audit(v)
            flag = "OK" if r["consistent"] else "DIFF"
            print(f"[audit] 卷{v} {r['name']}：{flag}覆盖 {r['coverage']} "
                  f"差异 {len(r['diffs'])}")
            for d in r["diffs"][:6]:
                print(f"         - {d}")
            if r["missing_items"]:
                print(f"         ! 缺 {len(r['missing_items'])} 条："
                      f"{r['missing_items'][:8]}")
        return

    # status
    print("=" * 68)
    print("《五杂俎》统一卷源状态（按卷扇出）")
    print("=" * 68)
    print(f"{'卷':<4}{'名称':<10}{'状态':<8}{'条目':<8}说明")
    for v in ALL_VOLUMES:
        p = volume_source_path(v)
        n = len(load_volume(v)) if p.exists() else 0
        total = len(registry_items(v))
        state = "已装填" if p.exists() else ("未装填" if total else "—")
        note = "" if p.exists() else f"待装填 {total} 条"
        print(f"{v:<4}{VOLUME_NAME.get(v, ''):<10}{state:<8}{n:<8}{note}")
    print()
    print("命令：")
    print("  python _vol_schema.py split   --volumes 01 02   # 摊平成 11 个分层文件")
    print("  python _vol_schema.py merge   --volumes 01 02   # 折叠回统一卷源")
    print("  python _vol_schema.py audit   --volumes 01 02   # 一致性巡检")
    print("  python _vol_schema.py status                    # 进度总览")


if __name__ == "__main__":
    main()