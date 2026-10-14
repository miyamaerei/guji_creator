#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build L3 过程层 + C1 任职层 + C14 时间沿革层
  _proc_ai_<NN>.py  → _layers/procs/<NN>_procs.json   （per-volume）
  _appt_ai_<NN>.py  → _layers/appts/appts.json        （global）
  _tme_ai_<NN>.py   → _layers/tmes/tmes.json          （global）

用法: python build_proc_appt_tme.py [--volumes NN]   （缺省全量 01-06）

ID 纪律：PROC/APPT/TME 均按卷分配 `<前缀><卷段位><序号>`，跨卷不撞。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import REGISTRY_FILE, load_json, layer_file, save_json  # noqa: E402
from _ai_source import assign_ids, check_item_ids, load_ai, volumes_arg  # noqa: E402


def _merge(src: str, id_prefix: str, vols, reg) -> list:
    recs = []
    for vol in vols:
        part = load_ai(src, vol)
        if part:
            part = assign_ids(part, id_prefix, vol)
            check_item_ids(part, reg)
            recs.extend(part)
            print(f"  {src} 卷{vol:02d}: 源 {len(part)} 条")
    return recs


def main() -> None:
    vols = volumes_arg(sys.argv[1:])
    reg = load_json(REGISTRY_FILE, {})

    # L3 过程层（per-volume）
    for vol in vols:
        recs = load_ai("proc", vol)
        if not recs:
            print(f"  [跳过] 卷{vol:02d} 无 _proc_ai_{vol:02d}.py 源数据")
            continue
        recs = assign_ids(recs, "PROC-", vol)
        check_item_ids(recs, reg)
        save_json(layer_file("procs", vol), {"volume": f"{vol:02d}", "records": recs})
        print(f"  L3 卷{vol:02d}: {len(recs)} 条")

    # C1 任职层（global）
    appts = _merge("appt", "APPT-", vols, reg)
    if appts:
        save_json(layer_file("appts"), {"records": appts})
        print(f"  C1 全局层: {len(appts)} 条")
    else:
        print("  [跳过] 无 _appt_ai_*.py 源数据（宁缺毋滥，视卷别而定）")

    # C14 时间沿革层（global）
    tmes = _merge("tme", "TME-", vols, reg)
    if tmes:
        save_json(layer_file("tmes"), {"records": tmes})
        print(f"  C14 全局层: {len(tmes)} 条")
    else:
        print("  [跳过] 无 _tme_ai_*.py 源数据")


if __name__ == "__main__":
    main()
