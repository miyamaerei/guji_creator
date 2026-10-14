#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build REG 制度层（本书骨架）—— 读 _regs_ai_<NN>.py → _layers/regs/regs.json

用法: python build_regs.py [--volumes NN]   （缺省全量 01-06；全局层，跨卷聚合）

ID 纪律（schemas §0.3）：`<REG-><卷段位><序号>`，按卷分配，跨卷不撞。
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
        part = load_ai("regs", vol)
        if part:
            part = assign_ids(part, "REG-", vol)
            check_item_ids(part, reg)
            recs.extend(part)
            print(f"  REG 卷{vol:02d}: 源 {len(part)} 条")
    if not recs:
        print("  [跳过] 无 _regs_ai_*.py 源数据")
        return
    save_json(layer_file("regs"), {"records": recs})
    print(f"  REG 全局层: {len(recs)} 条")


if __name__ == "__main__":
    main()
