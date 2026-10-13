# -*- coding: utf-8 -*-
"""批量修复：去重 + 补geo级别 + 建父子关系"""
import json, os, re
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

# ===== 1. 去重 =====
print("=" * 60)
print("【1. 去重】")
print("=" * 60)

for layer_name in ["nams", "ents", "materials", "org_events"]:
    p = os.path.join(ROOT, "_layers", layer_name + ".json")
    data = json.load(open(p, encoding="utf-8"))

    before = len(data)
    seen = set()
    unique = []

    for r in data:
        iid = r.get("item_id", "")
        # 找名称字段
        name = r.get("text", "") or r.get("name", "") or r.get("material", "") or r.get("org_name", "") or ""
        key = (iid, name)

        if key not in seen:
            seen.add(key)
            unique.append(r)

    after = len(unique)
    removed = before - after
    print(f"  {layer_name}: {before} → {after} (去重{removed}条)")

    with open(p, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=1)

# ===== 2. 补geo的unknown级别 =====
print(f"\n{'='*60}")
print("【2. 补geo级别】")
print("=" * 60)

geo = json.load(open(os.path.join(ROOT, "_layers", "geo.json"), encoding="utf-8"))

GEO_SUFFIXES = {
    "布政司": "省",
    "府": "府",
    "州": "州",
    "县": "县",
    "卫": "卫",
    "千户所": "所",
}

fixed = 0
for g in geo:
    if g.get("level") == "unknown" or not g.get("level"):
        name = g.get("name", "")
        for suffix, level in GEO_SUFFIXES.items():
            if name.endswith(suffix):
                g["level"] = level
                fixed += 1
                break

print(f"  修正了{fixed}条unknown级别")

# 分布
level_dist = Counter(g["level"] for g in geo)
print(f"  修正后分布:")
for l, c in level_dist.most_common():
    print(f"    {l}: {c}条")

with open(os.path.join(ROOT, "_layers", "geo.json"), "w", encoding="utf-8") as f:
    json.dump(geo, f, ensure_ascii=False, indent=1)

# ===== 3. 建父子节点关系 =====
print(f"\n{'='*60}")
print("【3. 建父子节点关系】")
print("=" * 60)

ents = json.load(open(os.path.join(ROOT, "_layers", "ents.json"), encoding="utf-8"))

# 建立实体名 → ent_id 映射
ent_name_map = {}
for e in ents:
    name = e.get("text", "")
    if name:
        ent_name_map[name] = e.get("ent_id", "")

# 给每个实体加parent_id
# 规则：如果文本中提到了上级衙门，就建立父子关系
# 比如 "吏部文选司" 的parent是 "吏部"
# 简化：按名称包含关系建父子
fixed_parent = 0
for e in ents:
    name = e.get("text", "")
    if not name:
        continue

    # 找上级（名称是当前名称的前缀，且更短）
    for other_name, other_id in ent_name_map.items():
        if other_name != name and name.startswith(other_name) and len(other_name) < len(name):
            # 其他是当前的上级
            e["parent_id"] = other_id
            e["node_type"] = "child"
            fixed_parent += 1
            break

print(f"  建立了{fixed_parent}条父子关系")

# 统计节点类型
node_types = Counter(e.get("node_type", "root") for e in ents)
print(f"  节点类型分布:")
for t, c in node_types.most_common():
    print(f"    {t}: {c}条")

with open(os.path.join(ROOT, "_layers", "ents.json"), "w", encoding="utf-8") as f:
    json.dump(ents, f, ensure_ascii=False, indent=1)

print(f"\n{'='*60}")
print("修复完成!")
print("=" * 60)
