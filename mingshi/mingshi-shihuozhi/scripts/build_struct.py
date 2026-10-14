#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build L4 食货四维层 —— 读 _struct_ai_<NN>.py → _layers/structs/structs.json

源数据外形（各卷一个文件）：
    AI_RECORDS = {"QUAN": [...], "INST": [...], "EVO": [...], "FISC": [...]}
    （LED/TRANS/HK/LAND 可选；空键省略。C16 树由 build_ledger.py 单独产出。）

ID 纪律（schemas §0.3）：子类前缀 + 卷段位 + 序号（如 QUAN-01001）。
QUAN 的 dimension 由 unit 自动推导（unit_dimension，若源未填）。
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    REGISTRY_FILE,
    load_json,
    layer_dir,
    save_json,
    unit_dimension,
)
from _ai_source import assign_ids, check_item_ids, load_ai, volumes_arg  # noqa: E402
from _kg_enums import STRUCT_PREFIX  # noqa: E402


def main() -> None:
    vols = volumes_arg(sys.argv[1:])
    reg = load_json(REGISTRY_FILE, {})
    merged: dict = {}
    for vol in vols:
        data = load_ai("struct", vol)
        if not data:
            print(f"  [跳过] 卷{vol:02d} 无 _struct_ai_{vol:02d}.py 源数据")
            continue
        if not isinstance(data, dict):
            raise RuntimeError(
                f"_struct_ai_{vol:02d}.py: AI_RECORDS 必须是 {'子类': 记录列表} 的 dict"
            )
        for sub, recs in data.items():
            if sub not in STRUCT_PREFIX:
                raise RuntimeError(f"_struct_ai_{vol:02d}.py: 非法子类 {sub!r}")
            if not isinstance(recs, list):
                raise RuntimeError(f"structs.{sub}: AI_RECORDS[{sub!r}] 必须是 list")
            recs = [dict(r) for r in recs]
            if sub == "QUAN":
                for r in recs:
                    if r.get("unit") and not r.get("dimension"):
                        r["dimension"] = unit_dimension(r["unit"])
            recs = assign_ids(recs, STRUCT_PREFIX[sub], vol)
            check_item_ids(recs, reg)
            merged.setdefault(sub, []).extend(recs)
            print(f"  L4 卷{vol:02d} {sub}: 源 {len(recs)} 条")

    if not merged:
        print("  [跳过] 无 _struct_ai_*.py 源数据")
        return

    save_json(layer_dir("structs") / "structs.json", merged)
    total = sum(len(v) for v in merged.values())
    print(
        f"  L4 全局层: {total} 条（子类: {', '.join(f'{k}={len(v)}' for k, v in merged.items())}）"
    )


if __name__ == "__main__":
    main()
