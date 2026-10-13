# -*- coding: utf-8 -*-
"""抽样看G7/G8诸文职/武职内容"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# G7: 卷164-178, G8: 卷179-180
print("=" * 70)
print("【G7 诸文职】抽样（卷164-178）")
print("=" * 70)

g7_items = [(iid, item) for iid, item in reg.items() if 164 <= int(iid.split("-")[0]) <= 178]
print(f"G7总条目: {len(g7_items)}")
print()

# 抽样15条
for iid, item in g7_items[:15]:
    print(f"  {iid}: {item['title'][:50]}")
    print(f"       {item['original'][:50]}...")
    print()

print("=" * 70)
print("【G8 诸武职】抽样（卷179-180）")
print("=" * 70)

g8_items = [(iid, item) for iid, item in reg.items() if 179 <= int(iid.split("-")[0]) <= 180]
print(f"G8总条目: {len(g8_items)}")
print()

for iid, item in g8_items[:10]:
    print(f"  {iid}: {item['title'][:50]}")
    print(f"       {item['original'][:50]}...")
    print()
