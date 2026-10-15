# -*- coding: utf-8 -*-
"""GAP1: 为普安州(88-009)添加4个卫所子节点。"""
import json, os

ROOT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge"
SRC = os.path.join(ROOT, "_data", "guizhou_vol88.json")

with open(SRC, encoding="utf-8") as f:
    data = json.load(f)

weisuus = [
    ("GEO-88009w01", "晋安卫", "在州治南，洪武二十二年建，隶贵州都司"),
    ("GEO-88009w02", "乐民守御千户所", "在州城西南九十里"),
    ("GEO-88009w03", "平夷守御千户所", "在州城西一百里"),
    ("GEO-88009w04", "安笼守御千户所", "在州城东南三百二十里；各所俱隶普安卫"),
]

for item in data:
    if item.get("item_id") != "88-009":
        continue
    geos = item["layers"]["geos"]
    parent = geos[0]
    existing = {g["geo_id"] for g in geos}
    new_children = []
    for gid, name, loc in weisuus:
        if gid in existing:
            continue
        node = {
            "geo_id": gid,
            "item_id": "88-009",
            "name": name,
            "type": "weisuo",
            "region": "贵州",
            "parent": "GEO-88009",
            "children": [],
            "volume_range": "卷88",
            "attributes": {"location_text": loc},
            "cit_ids": [],
        }
        geos.append(node)
        new_children.append(gid)
    for cid in new_children:
        if cid not in parent.setdefault("children", []):
            parent["children"].append(cid)
    print("88-009 children:", parent["children"])
    print("geos count:", len(geos))

with open(SRC, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("written:", SRC)

# 同时写出独立分片 _data/vol88/88-009_普安州.json，供 build_merge.py 扫描
os.makedirs(os.path.join(ROOT, "_data", "vol88"), exist_ok=True)
for item in data:
    if item.get("item_id") == "88-009":
        slice_path = os.path.join(ROOT, "_data", "vol88", "88-009_普安州.json")
        with open(slice_path, "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)
        print("written slice:", slice_path)
        break
