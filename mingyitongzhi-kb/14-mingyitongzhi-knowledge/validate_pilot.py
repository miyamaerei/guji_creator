# -*- coding: utf-8 -*-
"""主程序验证：北直隶+南直隶试点数据是否符合 schemas.md。"""
import json, os
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")

registry = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
errors = []
gaps = []

def load(name):
    p = os.path.join(LAYERS, name, "all.json")
    if not os.path.exists(p): return []
    return json.load(open(p, encoding="utf-8"))["records"]

ents = load("ent"); geos = load("geo"); evos = load("evo")
mtns = load("mtn"); pers = load("per"); sites = load("site"); cits = load("cit")

# 枚举
ENT_TYPES = {"geo","person","mtn","site","prod","book","era","dynasty","待定"}
GEO_TYPES = {"metro","prefecture","department","subprefecture","county","tusi","weisuo","foreign","other"}

print(f"=== registry: {len(registry)} 条 ===")
# 1. registry 完整性
for iid, r in registry.items():
    if not r.get("title"): errors.append(f"[registry] {iid} 缺 title")
    if not r.get("region"): errors.append(f"[registry] {iid} 缺 region")
    if "volume" not in r: errors.append(f"[registry] {iid} 缺 volume")

# 2. 各层 item_id 合法性
for layer_name, recs, idkey in [("ent",ents,"ent_id"),("geo",geos,"geo_id"),
                                  ("evo",evos,"evo_id"),("mtn",mtns,"mtn_id"),
                                  ("per",pers,"per_id"),("site",sites,"site_id"),
                                  ("cit",cits,"cit_id")]:
    for r in recs:
        iid = r.get("item_id")
        if iid not in registry:
            errors.append(f"[{layer_name}] {r.get(idkey,'?')} item_id={iid} 不在 registry")

# 3. 枚举校验
for r in ents:
    if r.get("type") not in ENT_TYPES:
        errors.append(f"[ent] {r.get('ent_id')} type={r.get('type')!r} 不在枚举")
for r in geos:
    if r.get("type") not in GEO_TYPES:
        errors.append(f"[geo] {r.get('geo_id')} type={r.get('type')!r} 不在枚举")

# 3.5 GEO 树完整性校验
geo_ids = {g["geo_id"] for g in geos}
# a. geo_id 唯一性
dup_ids = [gid for gid in geo_ids if sum(1 for g in geos if g["geo_id"]==gid) > 1]
if dup_ids:
    errors.append(f"[geo] geo_id 重复: {set(dup_ids)}")
# b. children/parent 悬空引用
for g in geos:
    for ch in g.get("children",[]):
        if ch not in geo_ids:
            errors.append(f"[geo] {g['geo_id']}({g['name']}) children 悬空: {ch} 不在 geos 表")
    parent = g.get("parent")
    if parent and parent != "GEO-000" and parent not in geo_ids:
        errors.append(f"[geo] {g['geo_id']}({g['name']}) parent 悬空: {parent} 不在 geos 表")
# c. 国内 prefecture/department 必须有子节点（树深度至少到县/州/土司）
for g in geos:
    if g["type"] in ("prefecture","department") and g.get("region") not in ("外夷",):
        children = g.get("children",[])
        if not children:
            gaps.append(f"[geo] {g['geo_id']}({g['name']}) 国内府/州无子节点（应至少到县/属州/土司）")

# 4. 覆盖：每条 registry 在各层出现情况
covered = defaultdict(set)
for layer_name, recs in [("ent",ents),("geo",geos),("evo",evos),("mtn",mtns),
                          ("per",pers),("site",sites),("cit",cits)]:
    for r in recs:
        covered[r["item_id"]].add(layer_name)

zero_layer = [iid for iid in registry if not covered[iid]]
if zero_layer:
    gaps.append(f"{len(zero_layer)} 条 0 层记录: {zero_layer}")

# 5. 报告
print(f"\n=== 各层条数 ===")
for n, rs in [("ent",ents),("geo",geos),("evo",evos),("mtn",mtns),("per",pers),("site",sites),("cit",cits)]:
    print(f"  {n}: {len(rs)}")

print(f"\n=== ERR: {len(errors)} ===")
for e in errors[:20]: print(f"  ✗ {e}")
if len(errors)>20: print(f"  ... 还有 {len(errors)-20} 条")

print(f"\n=== GAP: {len(gaps)} ===")
for g in gaps: print(f"  ! {g}")

print(f"\n=== 每条目层覆盖 ===")
for iid in sorted(registry.keys()):
    layers_here = sorted(covered[iid])
    print(f"  {iid} {registry[iid]['title']:12s}  [{len(layers_here)}层] {','.join(layers_here)}")
