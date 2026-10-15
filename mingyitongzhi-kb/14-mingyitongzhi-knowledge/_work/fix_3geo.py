# -*- coding: utf-8 -*-
"""修剩余 3 个 geo ERR：
1. GEO-03001 真定府 15 节点重复 → 去重
2. GEO-04003 大名府 缺 GEO-04003-s01 开州节点（长垣县 parent 悬空）
3. GEO-05002 永宁县父节点缺失
"""
import json, os
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "_layers/geo/all.json")
data = json.load(open(P, encoding="utf-8"))
recs = data["records"]

# 1. 真定府去重：按 geo_id 保第一次
seen = OrderedDict()
for r in recs:
    seen.setdefault(r["geo_id"], r)
recs = list(seen.values())
print(f"1. 去重后 {len(recs)} 条（原 {len(data['records'])}）")

by_id = {r["geo_id"]: r for r in recs}

# 2. 大名府补开州 GEO-04003-s01
if "GEO-04003-s01" not in by_id:
    # 找长垣县
    changyuan = by_id.get("GEO-04003-c10")
    # 从大名府 children 里移除 c10，改为 s01
    dafu = by_id["GEO-04003"]
    if "GEO-04003-c10" in dafu["children"]:
        dafu["children"].remove("GEO-04003-c10")
    if "GEO-04003-s01" not in dafu["children"]:
        dafu["children"].append("GEO-04003-s01")
    # 建开州节点
    kz = {
        "geo_id": "GEO-04003-s01", "name": "开州", "type": "subprefecture",
        "parent": "GEO-04003", "region": "北直隶", "item_id": "04-003",
        "children": ["GEO-04003-c10"], "attributes": {},
    }
    recs.append(kz); by_id["GEO-04003-s01"] = kz
    print("2. +开州 GEO-04003-s01, 长垣县挂其下")

# 3. 补 GEO-05002 永宁县父节点
if "GEO-05002" not in by_id:
    yn = {
        "geo_id": "GEO-05002", "name": "永宁县", "type": "county",
        "parent": "GEO-000", "region": "北直隶", "item_id": "05-002",
        "children": ["GEO-05002-c01"], "attributes": {},
    }
    recs.append(yn); by_id["GEO-05002"] = yn
    # 让 GEO-05002-c01 挂在 GEO-05002 下（已是）
    print("3. +永宁县父节点 GEO-05002")

json.dump({"records": recs, "count": len(recs)}, open(P, "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print(f"done. total {len(recs)}")
