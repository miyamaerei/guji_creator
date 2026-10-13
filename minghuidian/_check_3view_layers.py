# -*- coding: utf-8 -*-
"""检查三个视角层的质量"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

# 检查geo_profiles
geo_profiles = json.load(open(os.path.join(ROOT, "_layers", "geo_profiles.json"), encoding="utf-8"))
print("=" * 70)
print(f"【GEO_PROFILE 地理主档层】{len(geo_profiles)}条")
print("=" * 70)
print(f"\n字段: {list(geo_profiles[0].keys())}")
print(f"\n抽样:")
for g in geo_profiles[:10]:
    print(f"  - {g.get('geo_name', '?'):15s} level={g.get('level', '?'):6s} parent={g.get('parent_geo', '?')}")

# 检查person_profiles
person_profiles = json.load(open(os.path.join(ROOT, "_layers", "person_profiles.json"), encoding="utf-8"))
print(f"\n{'=' * 70}")
print(f"【PERSON_PROFILE 人物主档层】{len(person_profiles)}条")
print("=" * 70)
print(f"\n字段: {list(person_profiles[0].keys())}")
print(f"\n抽样:")
for p in person_profiles[:10]:
    print(f"  - {p.get('office_name', '?'):20s} item={p.get('item_id', '?')}")

# 检查process_profiles
process_profiles = json.load(open(os.path.join(ROOT, "_layers", "process_profiles.json"), encoding="utf-8"))
print(f"\n{'=' * 70}")
print(f"【PROCESS_PROFILE 流程主档层】{len(process_profiles)}条")
print("=" * 70)
print(f"\n字段: {list(process_profiles[0].keys())}")
print(f"\n抽样:")
for p in process_profiles[:10]:
    print(f"  - {p.get('process_name', '?'):30s} length={p.get('length', '?')}")
