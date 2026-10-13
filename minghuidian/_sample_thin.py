# -*- coding: utf-8 -*-
"""抽样看稀疏卷的条目"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 稀疏卷样本
thin_vols = [62, 22, 67, 132, 47]

for vol in thin_vols:
    print(f"\n{'='*60}")
    print(f"卷 {vol} 抽样")
    print(f"{'='*60}")
    items = [(iid, item) for iid, item in reg.items() if int(iid.split("-")[0]) == vol]
    print(f"总条目: {len(items)}")
    for iid, item in items[:3]:
        print(f"\n  {iid}:")
        print(f"    title: {item['title'][:40]}")
        print(f"    original: {item['original'][:60]}...")
