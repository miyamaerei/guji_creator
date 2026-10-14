# -*- coding: utf-8 -*-
"""字段填写密度体检：各层字段填充率 + 树二级展开密度。"""
import json, os, re
from collections import Counter, defaultdict

L = lambda n: json.load(open(f"_layers/{n}.json", encoding="utf-8"))


def filled(v):
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() != ""
    if isinstance(v, (list, dict)):
        return len(v) > 0
    return True


def density(records, name):
    if not records:
        return
    keys = []
    seen = set()
    for r in records:
        if isinstance(r, dict):
            for k in r:
                if k not in seen:
                    seen.add(k); keys.append(k)
    n = len(records)
    print(f"\n### {name}  n={n}  fields={len(keys)}")
    rows = []
    for k in keys:
        c = sum(1 for r in records if isinstance(r, dict) and filled(r.get(k)))
        rows.append((k, c, c / n))
    for k, c, p in sorted(rows, key=lambda x: -x[2]):
        bar = "█" * int(round(p * 20))
        print(f"  {k:22s} {p*100:5.1f}%  {c:>6}/{n:<6} {bar}")


print("=" * 78)
print("一、结构层字段填写密度")
print("=" * 78)

for nm in ["rank", "njc", "xref", "geo", "org_profiles", "office_profiles",
           "geo_profiles", "person_profiles", "process_profiles",
           "ents", "rules", "tim", "nams", "dress", "rituals", "laws",
           "cits", "foreign", "materials", "inspect", "org_events"]:
    try:
        density(L(nm), nm)
    except Exception as e:
        print(nm, "ERR", e)

# ---------------- 树二级展开密度 ----------------
print("\n" + "=" * 78)
print("二、树二级展开密度（GEO 地理树）")
print("=" * 78)

geo = L("geo")
by_id = {g["geo_id"]: g for g in geo}
kids = defaultdict(list)
for g in geo:
    if g.get("parent_id"):
        kids[g["parent_id"]].append(g)

# 各 level 的“有子率”
lv = defaultdict(lambda: [0, 0])  # level -> [有子数, 总数]
for g in geo:
    lv[g["level"]][1] += 1
    if kids.get(g["geo_id"]):
        lv[g["level"]][0] += 1
print("\n-- 各层级「有下级」比例 --")
for l, (a, b) in sorted(lv.items(), key=lambda x: -x[1][1]):
    print(f"  {l:8s} 有子 {a:>5}/{b:<5} = {a/b*100:5.1f}%")

# 省→府 展开率
print("\n-- 省→府 展开 --")
for g in geo:
    if g["level"] == "省":
        fz = [k for k in kids.get(g["geo_id"], []) if k["type"] == "府"]
        zz = [k for k in kids.get(g["geo_id"], []) if k["type"] == "州"]
        print(f"  {g['name']:8s} 府{len(fz):>3}  直隶州{len(zz):>3}")

# 府→县 展开率（二级展开关键）
print("\n-- 府→(州/县) 展开（重点：二级） --")
tot_fu = tot_with = 0
zero_fu = []
for g in geo:
    if g["type"] != "府":
        continue
    tot_fu += 1
    cs = kids.get(g["geo_id"], [])
    xs = [k for k in cs if k["type"] in ("县", "州")]
    if xs:
        tot_with += 1
    else:
        zero_fu.append(g["name"])
print(f"  府总数 {tot_fu}，其中有下级(州/县) {tot_with} = {tot_with/tot_fu*100:.1f}%")
print(f"  空府（无州/县）{len(zero_fu)}: {zero_fu[:40]}")

# 州→县 展开
tot_zhou = tot_zhou_with = 0
for g in geo:
    if g["type"] == "州":
        tot_zhou += 1
        if kids.get(g["geo_id"]):
            tot_zhou_with += 1
print(f"\n  州总数 {tot_zhou}，其中有下级(县) {tot_zhou_with} = {tot_zhou_with/tot_zhou*100:.1f}%")

# 都司→卫 展开
print("\n-- 都司/都督府/留守司→卫所 展开 --")
for g in geo:
    if g["type"] in ("都司", "都督府", "留守司", "亲军", "南京"):
        cs = kids.get(g["geo_id"], [])
        ws = [k for k in cs if k["type"] in ("卫", "所", "护卫")]
        print(f"  {g['name']:14s}({g['type']})  卫所 {len(ws):>3}")

# ---------------- 关联字段（预留但未打通） ----------------
print("\n" + "=" * 78)
print("三、关联字段（garrisons/post_stations/granaries/administered_by）")
print("=" * 78)
for f in ["administered_by", "garrisons", "post_stations", "granaries", "children"]:
    c = sum(1 for g in geo if filled(g.get(f)))
    print(f"  {f:18s} {c:>5}/{len(geo)} = {c/len(geo)*100:5.1f}%")
