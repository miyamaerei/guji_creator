# -*- coding: utf-8 -*-
"""抽样选几条典型数据做验证"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

# 加载几个关键层
org_profiles = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))
geo = json.load(open(os.path.join(ROOT, "_layers", "geo.json"), encoding="utf-8"))
offices = json.load(open(os.path.join(ROOT, "_layers", "offices.json"), encoding="utf-8"))

print("=" * 70)
print("抽样验证用的典型数据")
print("=" * 70)

# 1. 有品级的部门
print("\n【1. 有品级的部门】")
with_rank = [o for o in org_profiles if o.get("rank")]
rank_dist = Counter(o["rank"] for o in with_rank)
for rank, cnt in rank_dist.most_common(5):
    sample = [o for o in with_rank if o["rank"] == rank][:3]
    print(f"\n  {rank} ({cnt}条):")
    for s in sample:
        print(f"    - {s['org_name']} (item: {s['item_id']})")

# 2. 地理层级
print("\n\n【2. 地理层级抽样】")
geo_levels = Counter(g["level"] for g in geo)
for level in ["省", "府", "州", "县"]:
    samples = [g for g in geo if g["level"] == level][:5]
    print(f"\n  {level}级 ({geo_levels.get(level, 0)}条):")
    for s in samples:
        print(f"    - {s['name']}")

# 3. 官职抽样
print("\n\n【3. 官职抽样】")
print(f"  官职总数: {len(offices)}条")
sample_offices = offices[:10]
for o in sample_offices:
    print(f"    - {o['office_name']} (item: {o['item_id']})")
