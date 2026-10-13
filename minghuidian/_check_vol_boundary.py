# -*- coding: utf-8 -*-
"""检查卷边界"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

for vol in [143, 144, 145, 146, 150, 155, 160]:
    items = [(iid, item) for iid, item in reg.items() if int(iid.split("-")[0]) == vol]
    if items:
        print(f"卷{vol}: {len(items)}条")
        print(f"  首条: {items[0][1]['title'][:60]}")
        print()
