# -*- coding: utf-8 -*-
"""一次性修历史遗留 ERR。"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYERS = os.path.join(ROOT, "_layers")
REG = os.path.join(ROOT, "_item_registry.json")

def load(name):
    return json.load(open(os.path.join(LAYERS, name, "all.json"), encoding="utf-8"))["records"]
def save(name, recs):
    json.dump({"records": recs, "count": len(recs)},
              open(os.path.join(LAYERS, name, "all.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

reg = json.load(open(REG, encoding="utf-8"))
ents = load("ent"); geos = load("geo"); evos = load("evo")

# 1. 修脏 evo item_id
fixed_evo = 0
for e in evos:
    if e.get("item_id") == "EVO-002":
        e["item_id"] = "31-001"; fixed_evo += 1
    if e.get("item_id") == "EVO-003":
        e["item_id"] = "31-002"; fixed_evo += 1
print(f"[1] 修脏 evo item_id: {fixed_evo}")

# 2. 修非法 ent type
fixed_ent = 0
for e in ents:
    if e.get("type") == "river":
        e["type"] = "mtn"; fixed_ent += 1
    if e.get("type") == "geofeat":
        e["type"] = "mtn"; fixed_ent += 1
print(f"[2] 修非法 ent type: {fixed_ent}")

# 3. 河间府：补 GEO-02002-s01(景州) / s02(沧州) department 节点
geo_ids = {g["geo_id"] for g in geos}
added_geo = 0
if "GEO-02002-s01" not in geo_ids:
    geos.append({"geo_id":"GEO-02002-s01","name":"景州","type":"department","parent":"GEO-02002",
                 "children":["GEO-02002-s01-c11","GEO-02002-s01-c12","GEO-02002-s01-c13"],
                 "item_id":"02-002","region":"北直隶"})
    added_geo += 1
if "GEO-02002-s02" not in geo_ids:
    geos.append({"geo_id":"GEO-02002-s02","name":"沧州","type":"department","parent":"GEO-02002",
                 "children":["GEO-02002-s02-c14","GEO-02002-s02-c15","GEO-02002-s02-c16"],
                 "item_id":"02-002","region":"北直隶"})
    added_geo += 1
# 修河间府 children：c11-c16 改成 s01/s02
for g in geos:
    if g["geo_id"] == "GEO-02002":
        old = g.get("children",[])
        new = [c for c in old if not (c.startswith("GEO-02002-c1") and c[-2:] in ("11","12","13","14","15","16"))]
        if "GEO-02002-s01" not in new: new.append("GEO-02002-s01")
        if "GEO-02002-s02" not in new: new.append("GEO-02002-s02")
        g["children"] = new
        print(f"[3] 河间府 children: {len(old)} -> {len(new)}")
print(f"[3] 补河间府属州节点: {added_geo}")

# 4. 真定府：补 GEO-03001(prefecture) + s01~s05(department)
if "GEO-03001" not in geo_ids:
    # 从 c01 拿 item_id
    item_id_03 = next((c["item_id"] for c in geos if c["geo_id"]=="GEO-03001-c01"), "03-001")
    geos.append({"geo_id":"GEO-03001","name":"真定府","type":"prefecture","parent":"GEO-000",
                 "children":([f"GEO-03001-c{i:02d}" for i in range(1,11)] +
                             [f"GEO-03001-s0{i}" for i in range(1,6)]),
                 "item_id":item_id_03,"region":"北直隶"})
    added_geo += 1
# 补 s01~s05 属州（从 c11-c27 的 parent 反推）
sub_map = {"GEO-03001-s01":"定州","GEO-03001-s02":"冀州","GEO-03001-s03":"晋州",
           "GEO-03001-s04":"赵州","GEO-03001-s05":"深州"}
# 收集每个 s 的 children
sub_children = {sid:[] for sid in sub_map}
for g in geos:
    p = g.get("parent","")
    if p in sub_children:
        sub_children[p].append(g["geo_id"])
for sid, sname in sub_map.items():
    if sid not in geo_ids:
        geos.append({"geo_id":sid,"name":sname,"type":"department","parent":"GEO-03001",
                     "children":sub_children[sid],"item_id":"03-001","region":"北直隶"})
        added_geo += 1
print(f"[4] 补真定府+属州节点: {added_geo}")

# 5. 修 registry 03-001 title（衡水县 -> 真定府）
if "03-001" in reg and reg["03-001"].get("title") == "衡水县":
    reg["03-001"]["title"] = "真定府"
    print("[5] registry 03-001 title: 衡水县 -> 真定府")

# 写回
save("evo", evos); save("ent", ents); save("geo", geos)
json.dump(reg, open(REG,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("done.")
