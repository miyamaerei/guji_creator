# -*- coding: utf-8 -*-
"""一次性修复历史遗留 ERR：EVO脏ID / ENT非法type / GEO重复 / 河间府悬空 / 真定府缺失。"""
import json, os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYERS = os.path.join(ROOT, "_layers")

def load(name):
    p = os.path.join(LAYERS, name, "all.json")
    return json.load(open(p, encoding="utf-8"))["records"]

def save(name, recs):
    json.dump({"records": recs, "count": len(recs)},
              open(os.path.join(LAYERS, name, "all.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

ents = load("ent"); geos = load("geo"); evos = load("evo")

# 1. EVO-002/EVO-003 脏 item_id：看一下内容
print("=== 脏 evo 记录 ===")
for e in evos:
    if e.get("evo_id") in ("EVO-002","EVO-003"):
        print(e.get("evo_id"), "item_id=", e.get("item_id"), "|", str(e.get("summary",""))[:120])

# 2. ENT-002 / ENT-007
print("\n=== 脏 ent 记录 ===")
for e in ents:
    if e.get("ent_id") in ("ENT-002","ENT-007"):
        print(e.get("ent_id"), "type=", e.get("type"), "| name=", e.get("name"), "| item_id=", e.get("item_id"))

# 3. GEO-22001-c* 重复：看重复的都是谁
print("\n=== GEO-22001-c* 重复样本 ===")
from collections import Counter
cnt = Counter(g["geo_id"] for g in geos)
dups = [gid for gid,c in cnt.items() if c>1 and gid.startswith("GEO-22001")]
print("重复 geo_id 数:", len(dups), "总重复条数:", sum(cnt[g] for g in dups))
# 看一条样本
for g in geos:
    if g["geo_id"] == "GEO-22001-c01":
        print("样本:", g.get("name"), "parent=", g.get("parent"), "type=", g.get("type"))

# 4. 河间府：看 GEO-02002 当前 children，以及 c11-c16 实际 geo_id
print("\n=== 河间府 GEO-02002 ===")
for g in geos:
    if g["geo_id"] == "GEO-02002":
        print("children:", g.get("children"))
        print("name:", g.get("name"))
print("--- 吴桥/东光/故城/南皮/盐山/庆云 实际节点 ---")
for g in geos:
    if g.get("name") in ("吴桥县","东光县","故城县","南皮县","盐山县","庆云县"):
        print(g["geo_id"], g["name"], "parent=", g.get("parent"))

# 5. GEO-03001 系列
print("\n=== GEO-03001 系列 ===")
for g in geos:
    if g["geo_id"].startswith("GEO-03001"):
        print(g["geo_id"], g.get("name"), "parent=", g.get("parent"), "type=", g.get("type"))
