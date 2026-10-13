# -*- coding: utf-8 -*-
"""抽样看G6工部内容"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

print("=" * 70)
print("【G6 工部】抽样（卷146-163）")
print("=" * 70)

g6_items = [(iid, item) for iid, item in reg.items() if 146 <= int(iid.split("-")[0]) <= 163]
print(f"G6总条目: {len(g6_items)}")
print()

# 按卷分组看
from collections import defaultdict
by_vol = defaultdict(list)
for iid, item in g6_items:
    vol = int(iid.split("-")[0])
    by_vol[vol].append((iid, item))

for vol in sorted(by_vol.keys()):
    items = by_vol[vol]
    print(f"卷{vol}: {len(items)}条")
    print(f"  首条: {items[0][1]['title'][:50]}")
    print(f"  次条: {items[1][1]['title'][:50] if len(items)>1 else ''}")
    print()
