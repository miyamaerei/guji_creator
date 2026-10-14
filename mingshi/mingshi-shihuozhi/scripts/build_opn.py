#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build C9 论说层 —— 读 _opn_ai_<NN>.py → _layers/opns/opns.json

用法: python build_opn.py [--volumes NN]   （缺省全量 01-06；全局层）

ID 纪律：`<OPN-><卷段位><序号>`，按卷分配，跨卷不撞。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import REGISTRY_FILE, load_json, layer_file, save_json  # noqa: E402
from _ai_source import assign_ids, check_item_ids, load_ai, volumes_arg  # noqa: E402


def main() -> None:
    vols = volumes_arg(sys.argv[1:])
    reg = load_json(REGISTRY_FILE, {})
    recs = []
    for vol in vols:
        part = load_ai("opn", vol)
        if part:
            part = assign_ids(part, "OPN-", vol)
            check_item_ids(part, reg)
            recs.extend(part)
            print(f"  C9 卷{vol:02d}: 源 {len(part)} 条")
    if not recs:
        print("  [跳过] 无 _opn_ai_*.py 源数据")
        return
    save_json(layer_file("opns"), {"records": recs})
    print(f"  C9 全局层: {len(recs)} 条")


if __name__ == "__main__":
    main()
