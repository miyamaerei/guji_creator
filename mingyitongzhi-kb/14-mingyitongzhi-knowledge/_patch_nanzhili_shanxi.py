# -*- coding: utf-8 -*-
"""补南直隶 + 山西 GEO 县节点。
- 南直隶 15 节点 parent 改 GEO-000；14 府补 county/subprefecture 子节点。
- 山西：太原府 GEO-001->GEO-19001、平阳府 GEO-001->GEO-20001（消除与真定府撞号）；
  8 个府/州补 county/subprefecture 子节点。
县名/州名来自 _work/nanzhili_extract.json 与 _work/shanxi_extract.json（自原文抽）。
id 规则（同贵州/真定样板）：直辖县 {府gid}-cNN；属州 {府gid}-sNN；州领县 {州gid}-cNN。
"""
import json, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(ROOT, "_layers", "geo", "all.json")

# 备份
shutil.copy(P, P + ".bak_patch")

data = json.load(open(P, encoding="utf-8"))
recs = data["records"]

nanz = json.load(open(os.path.join(ROOT, "_work", "nanzhili_extract.json"), encoding="utf-8"))
shan = json.load(open(os.path.join(ROOT, "_work", "shanxi_extract.json"), encoding="utf-8"))

# 现有 geo_id 集合（用于去重/幂等）
existing_ids = {r["geo_id"] for r in recs}


def find_pref(geo_id=None, name=None, region=None):
    for r in recs:
        if geo_id is not None and r["geo_id"] != geo_id:
            continue
        if name is not None and r["name"] != name:
            continue
        if region is not None and r.get("region") != region:
            continue
        return r
    raise KeyError(f"pref not found: gid={geo_id} name={name} region={region}")


new_nodes = []
created_ids = set()


def add_node(gid, name, ntype, parent, region, item_id, children=None):
    node = {
        "geo_id": gid, "name": name, "type": ntype,
        "parent": parent, "region": region, "item_id": item_id,
        "children": children if children is not None else [], "attributes": {},
    }
    new_nodes.append(node)
    created_ids.add(gid)


def build_unit(pref, region, extract):
    """对一个府/州，按抽取结果建直辖县+属州+州领县，返回该府 children 列表。"""
    pgid = pref["geo_id"]
    iid = pref["item_id"]
    children_ids = []

    # 直辖县
    for idx, cname in enumerate(extract["direct_counties"], 1):
        cgid = f"{pgid}-c{idx:02d}"
        add_node(cgid, cname, "county", pgid, region, iid)
        children_ids.append(cgid)

    # 属州
    for sidx, sp in enumerate(extract["subprefectures"], 1):
        sgid = f"{pgid}-s{sidx:02d}"
        s_children = []
        add_node(sgid, sp["name"], "subprefecture", pgid, region, iid, children=s_children)
        children_ids.append(sgid)
        for cidx, cname in enumerate(sp["counties"], 1):
            cgid = f"{sgid}-c{cidx:02d}"
            add_node(cgid, cname, "county", sgid, region, iid)
            s_children.append(cgid)

    return children_ids


# ---------- 南直隶 ----------
# 1) 京城 metro：仅 parent 改 GEO-000
jc = find_pref(geo_id="GEO-06001", region="南直隶")
jc["parent"] = "GEO-000"

for gid, ext in nanz.items():
    pref = find_pref(geo_id=gid, region="南直隶")
    pref["parent"] = "GEO-000"
    pref["children"] = build_unit(pref, "南直隶", ext)

# ---------- 山西 ----------
# 名 -> 当前 geo_id（太原/平阳需先改号）
shan_plan = [
    ("太原府", "GEO-19001"),
    ("平阳府", "GEO-20001"),
    ("大同府", "GEO-21001"),
    ("潞安府", "GEO-21101"),
    ("汾州",   "GEO-21201"),
    ("辽州",   "GEO-21301"),
    ("沁州",   "GEO-21401"),
    ("泽州",   "GEO-21501"),
]
for nm, new_gid in shan_plan:
    pref = find_pref(name=nm, region="山西")
    old_gid = pref["geo_id"]
    if old_gid != new_gid:
        assert old_gid == "GEO-001", f"意外旧号 {old_gid} for {nm}"
        pref["geo_id"] = new_gid  # 改号（太原/平阳）
    pref["parent"] = "GEO-000"
    pref["children"] = build_unit(pref, "山西", shan[nm])

# ---------- 落库 ----------
# 幂等：先删掉本次将要重建的子节点（按生成的 geo_id）
recs = [r for r in recs if r["geo_id"] not in created_ids]
recs.extend(new_nodes)

json.dump({"records": recs, "count": len(recs)}, open(P, "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

print(f"新增子节点 {len(new_nodes)} 个；总记录 {len(recs)}")
# 概览
for gid, ext in nanz.items():
    p = find_pref(geo_id=gid, region="南直隶")
    print(f"  南直隶 {gid} {ext['name']}: children={len(p['children'])}")
for nm, _ in shan_plan:
    p = find_pref(name=nm, region="山西")
    print(f"  山西   {p['geo_id']} {nm}: children={len(p['children'])}")
