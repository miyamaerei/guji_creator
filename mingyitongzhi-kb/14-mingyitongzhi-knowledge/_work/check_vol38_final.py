# -*- coding: utf-8 -*-
import json, os
BASE = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol38"
d = json.load(open(os.path.join(BASE, "38-001_杭州府.json"), encoding="utf-8"))

print("=== 主文件7层统计 ===")
for k, v in d["layers"].items():
    print(f"  {k}: {len(v)}")

g = d["layers"]["geos"][0]
all_ids = [x["geo_id"] for x in d["layers"]["geos"]]
print(f"\n=== GEO树 ===")
print(f"府: {g['name']} ({g['geo_id']}), parent={g['parent']}")
print(f"children数: {len(g['children'])}, geos列表数: {len(all_ids)}")
missing = [c for c in g["children"] if c not in all_ids]
print(f"children悬空: {missing if missing else '无'}")
bad = [f"{x['geo_id']}->'{x['parent']}'" for x in d["layers"]["geos"]
       if x["parent"] not in ["GEO-000"] + all_ids]
print(f"parent非法: {bad if bad else '无'}")

print(f"\n=== 拆分文件条数 ===")
for fn in ["38-001_pers1_名宦.json","38-001_pers2_人物.json","38-001_pers3_列女仙释.json",
           "38-001_sites1_寺观祠庙陵墓.json","38-001_sites2_宫室关梁公署学校.json"]:
    dd = json.load(open(os.path.join(BASE, fn), encoding="utf-8"))
    n = len(dd["layers"].get("pers", [])) or len(dd["layers"].get("sites", []))
    print(f"  {fn}: {n}条")
