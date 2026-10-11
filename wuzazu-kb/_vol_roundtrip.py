# -*- coding: utf-8 -*-
"""统一卷源 ↔ 分层文件 往返一致性断言（迁移安全网）。

对每个已装填卷做：
    备份原分层文件 → merge → split → 逐层逐条比对 → 断言零丢失、零漂移。

用法：
    python _vol_roundtrip.py            # 校验（不写盘）
    python _vol_roundtrip.py --apply    # 真正执行 merge + split 并复验
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

import _vol_schema as V  # noqa: E402


def snapshot(volume: str, source: V.Path | None = None) -> dict[str, list[dict]]:
    """读某卷的全部分层记录（source 指定目录则从那里读，用于读备份）。"""
    snap: dict[str, list[dict]] = {}
    for layer in V.LAYERS:
        p = (source or V.SRC_DIR) / f"_{layer}_ai_{volume}.py"
        if not p.exists():
            continue
        ns: dict = {"__file__": str(p), "__name__": f"_{layer}_ai_{volume}"}
        exec(compile(p.read_text(encoding="utf-8"), str(p), "exec"), ns)  # noqa: S102
        for key in ("RECORDS", f"{layer.upper()}_RECORDS"):
            val = ns.get(key)
            if isinstance(val, list):
                snap[layer] = [dict(r) for r in val if isinstance(r, dict)]
                break
    return snap


def _canon(rows: list[dict]) -> list[str]:
    """记录的无序规范化表示（用于比对，不依赖文件内顺序）。

    打包器 `pack_volume` 在分配 ID 前会 `prepared.sort(key=layer_sort_key)`，
    排序键是 (卷, 条号, 该层语义键) —— ID 分配完全由数据内容决定，与源文件
    里的记录先后无关。因此往返校验必须按**内容集合**比对，不能按位置。
    """
    return sorted(
        repr(sorted((k, repr(v)) for k, v in r.items()))
        for r in rows
    )


def compare(before: dict[str, list[dict]], after: dict[str, list[dict]]) -> list[str]:
    """逐层按内容集合比对，返回差异描述列表（空 = 完全一致，忽略记录顺序）。"""
    problems: list[str] = []
    for layer in sorted(set(before) | set(after)):
        b = before.get(layer, [])
        a = after.get(layer, [])
        if len(b) != len(a):
            problems.append(f"{layer}: 记录数 {len(b)} → {len(a)}")
            continue
        cb, ca = _canon(b), _canon(a)
        if cb == ca:
            continue
        missing = [x for x in cb if x not in ca]
        added = [x for x in ca if x not in cb]
        for x in missing[:3]:
            problems.append(f"{layer}: 丢失 {x[:160]}")
        for x in added[:3]:
            problems.append(f"{layer}: 新增 {x[:160]}")
        if not missing and not added:
            problems.append(f"{layer}: 集合相同但逐条签名不符")
    return problems


def main() -> None:
    apply = "--apply" in sys.argv
    volumes = [v for v in V.ALL_VOLUMES
               if any((V.SRC_DIR / f"_{l}_ai_{v}.py").exists() for l in V.LAYERS)]

    if not volumes:
        print("没有可校验的分层数据（_src/ 下无 _<layer>_ai_NN.py）")
        return

    backup_dir = V.SRC_DIR / "_legacy"
    backup_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 68)
    print(f"统一卷源往返校验　卷：{volumes}　模式：{'写入' if apply else '只读'}")
    print("=" * 68)

    ok = True
    for vol in volumes:
        before = snapshot(vol)
        n_before = sum(len(v) for v in before.values())

        if apply:
            for layer in before:
                p = V.layer_source_path(layer, vol)
                if p.exists():
                    (backup_dir / p.name).write_text(
                        p.read_text(encoding="utf-8"), encoding="utf-8")
            V.merge(vol, drop_existing=False)   # 已手动备份，不再重复备份
            V.split(vol)
            after = snapshot(vol)
        else:
            unified = V.load_volume(vol) if V.have_volume(vol) else {}
            after = {}
            for layer in V.LAYERS:
                rows: list[dict] = []
                for item_id in sorted(unified, key=V._item_sort_key):
                    rows.extend(unified[item_id].get(layer, []))
                if rows:
                    after[layer] = rows

        n_after = sum(len(v) for v in after.values())
        problems = compare(before, after)
        status = "PASS" if (not problems and n_before == n_after) else "FAIL"
        if status == "FAIL":
            ok = False
        print(f"\n[{status}] 卷{vol} {V.VOLUME_NAME.get(vol, '')}："
              f"{len(before)} 层 / {n_before} 条 → {len(after)} 层 / {n_after} 条")
        for p in problems[:8]:
            print(f"        - {p}")

    print()
    print("总体：" + ("全部通过，零丢失" if ok else "存在差异，见上"))
    if not apply:
        print("（只读模式；加 --apply 执行 merge+split 并复验）")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()