# -*- coding: utf-8 -*-
"""生成GEO_PROFILE地理主档层"""
import json, os
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
geo = json.load(open(os.path.join(ROOT, "_layers", "geo.json"), encoding="utf-8"))

# 按地理名聚合，生成主档
geo_map = defaultdict(list)
for g in geo:
    geo_map[g["name"]].append(g)

geo_profiles = []
seq = 0

for name, entries in geo_map.items():
    seq += 1
    # 取第一个的级别
    level = entries[0].get("level", "unknown")

    # 找上级（根据级别推断）
    parent = None
    if level == "府":
        parent = "省"  # 简化
    elif level == "州":
        parent = "府"
    elif level == "县":
        parent = "府"
    elif level == "卫":
        parent = "都司"

    geo_profiles.append({
        "geo_id": f"GEOP-{seq:04d}",
        "geo_name": name,
        "level": level,
        "parent_geo": parent,
        "record_count": len(entries),
    })

print(f"【GEO_PROFILE 地理主档层】{len(geo_profiles)} 条")
print(f"\n级别分布:")
level_dist = Counter(g["level"] for g in geo_profiles)
for l, c in level_dist.most_common():
    print(f"  {l}: {c}条")

outpath = os.path.join(ROOT, "_layers", "geo_profiles.json")
with open(outpath, "w", encoding="utf-8") as f:
    json.dump(geo_profiles, f, ensure_ascii=False, indent=1)
print(f"\n已保存: {outpath}")
