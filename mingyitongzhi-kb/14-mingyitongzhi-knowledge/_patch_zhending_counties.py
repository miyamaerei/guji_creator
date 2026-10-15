# -*- coding: utf-8 -*-
"""补真定府 GEO 县节点：从原文抽县名，建 county/subprefecture 节点，修正 children。"""
import json, os, re
ROOT = os.path.dirname(os.path.abspath(__file__))

# 真定府下辖（从 L163 人工清点）
# 直辖县 10
direct_counties = ["真定县","井陉县","获鹿县","元氏县","灵寿县","藁城县","栾城县","无极县","平山县","阜平县"]
# 属州 5 + 各自领县
substates = {
    "定州": ["新乐县","曲阳县","行唐县"],
    "冀州": ["南宫县","新河县","枣强县","武邑县"],
    "晋州": ["安平县","饶阳县","武强县"],
    "赵州": ["柏乡县","隆平县","高邑县","临城县","赞皇县","宁晋县"],
    "深州": ["衡水县"],
}

# 加载现有 geo 层
p = os.path.join(ROOT,"_layers","geo","all.json")
data = json.load(open(p,encoding="utf-8"))
recs = data["records"]

# 找到真定府节点
zd = next(r for r in recs if r["geo_id"]=="GEO-001" and r["name"]=="真定府")

# 建子节点
new_nodes = []
children_ids = []
# 直辖县
for idx, cname in enumerate(direct_counties, 1):
    gid = f"GEO-03001-c{idx:02d}"
    new_nodes.append({
        "geo_id": gid, "name": cname, "type": "county",
        "parent": "GEO-001", "region": "北直隶", "item_id": "03-001",
        "children": [], "attributes": {}
    })
    children_ids.append(gid)

# 属州
for sidx, (sname, counties) in enumerate(substates.items(), 1):
    s_gid = f"GEO-03001-s{sidx:02d}"
    s_children = []
    new_nodes.append({
        "geo_id": s_gid, "name": sname, "type": "subprefecture",
        "parent": "GEO-001", "region": "北直隶", "item_id": "03-001",
        "children": s_children, "attributes": {}
    })
    children_ids.append(s_gid)
    # 属州领县
    for cidx, cname in enumerate(counties, 1):
        c_gid = f"{s_gid}-c{cidx:02d}"
        new_nodes.append({
            "geo_id": c_gid, "name": cname, "type": "county",
            "parent": s_gid, "region": "北直隶", "item_id": "03-001",
            "children": [], "attributes": {}
        })
        s_children.append(c_gid)

# 修正定府 children
zd["children"] = children_ids

# 追加新节点（去掉旧的悬空 GEO-002/003）
recs = [r for r in recs if not (r["geo_id"] in ("GEO-002","GEO-003") and r.get("region")=="北直隶")]
recs.extend(new_nodes)

json.dump({"records":recs,"count":len(recs)}, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"补 {len(new_nodes)} 节点: {len(direct_counties)}直辖县 + {len(substates)}属州 + {sum(len(v) for v in substates.values())}州领县")
print(f"真定府 children: {len(children_ids)}")
