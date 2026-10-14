# -*- coding: utf-8 -*-
"""P2.5 收尾：重算 GEO children，重建 geo_tree.md 与 geo_station.json。"""
import json, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
LAY = os.path.join(ROOT, "_layers")
geo = json.load(open(os.path.join(LAY, "geo.json"), encoding="utf-8"))

by_id = {g["geo_id"]: g for g in geo}
kids = defaultdict(list)
for g in geo:
    if g.get("parent_id") and g["parent_id"] in by_id:
        kids[g["parent_id"]].append(g["geo_id"])
for g in geo:
    g["children"] = [by_id[c]["name"] for c in kids.get(g["geo_id"], [])]

json.dump(geo, open(os.path.join(LAY, "geo.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# 可读树
lines = ["# 明会典·地理管辖树", "", f"共 {len(geo)} 个地理节点（含 驿/递运所/仓）。", ""]
out = []


def dump(gid, depth):
    if depth > 6:
        return
    g = by_id[gid]
    extra = ""
    if g.get("post_stations"):
        extra += f"　驿:{'、'.join(g['post_stations'][:4])}"
    if g.get("granaries"):
        extra += f"　仓:{'、'.join(g['granaries'][:3])}"
    if g.get("garrisons"):
        extra += f"　卫:{'、'.join(g['garrisons'][:3])}"
    out.append("  " * depth + f"- {g['name']}（{g['type']}）〔卷{g.get('volume','')}〕{extra}")
    for c in kids.get(gid, []):
        dump(c, depth + 1)


for g in geo:
    if g["type"] in ("直隶", "布政司", "都司", "都督府", "留守司", "亲军", "南京"):
        out.append(f"## {g['name']}（{g['type']}）")
        for c in kids.get(g["geo_id"], []):
            dump(c, 0)
        out.append("")
open(os.path.join(LAY, "geo_tree.md"), "w", encoding="utf-8").write("\n".join(lines + out))

# 驻防链接
links = []
for g in geo:
    if g.get("garrisons"):
        for w in g["garrisons"]:
            links.append({"place_id": g["geo_id"], "place": g["name"], "place_type": g["type"],
                          "garrison": w, "match": "name"})
json.dump(links, open(os.path.join(LAY, "geo_station.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

from collections import Counter
lv = Counter(g["type"] for g in geo)
print("GEO 节点:", len(geo), dict(lv))
print("有驿站", sum(1 for g in geo if g.get("post_stations")),
      "有仓场", sum(1 for g in geo if g.get("granaries")),
      "有驻防", sum(1 for g in geo if g.get("garrisons")))
print("geo_tree.md / geo_station.json 已重建")
