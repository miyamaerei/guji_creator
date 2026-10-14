#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build L1 Entity Layer —— 读 _ents_ai_<NN>.py → _layers/ents/<NN>_ents.json

用法: python build_ent.py [--volumes NN]   （缺省全量 01-06）
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (
    REGISTRY_FILE,
    load_json,
    layer_file,
    save_json,
    normalize_entity_type,
)  # noqa: E402
from _ai_source import assign_ids, check_item_ids, load_ai, volumes_arg  # noqa: E402


def main() -> None:
    vols = volumes_arg(sys.argv[1:])
    reg = load_json(REGISTRY_FILE, {})
    for vol in vols:
        recs = load_ai("ents", vol)
        if not recs:
            print(f"  [跳过] 卷{vol:02d} 无 _ents_ai_{vol:02d}.py 源数据")
            continue
        recs = assign_ids(recs, "ENT-", vol)
        check_item_ids(recs, reg)
        for r in recs:
            if "type" in r:
                r["type"] = normalize_entity_type(r["type"])
        save_json(layer_file("ents", vol), {"volume": f"{vol:02d}", "records": recs})
        print(f"  L1 卷{vol:02d}: {len(recs)} 条")


if __name__ == "__main__":
    main()
