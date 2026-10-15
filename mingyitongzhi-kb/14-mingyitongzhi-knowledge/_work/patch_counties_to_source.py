import json, os, glob

# 从 git 恢复的县名数据
nanz = {
  "GEO-06002": {"file": "_data/vol06/06-002_应天府.json", "direct": ["上元县","江宁县","句容县","溧阳县","溧水县","江浦县","六合县","高淳县"], "subs": []},
  "GEO-07003": {"file": "_data/vol07/07-003_凤阳府.json", "direct": ["凤阳县","临淮县","怀远县","定远县","五河县","虹县"], "subs": [("寿州",["霍丘县","蒙城县"]),("泗州",["盱眙县","天长县"]),("宿州",["灵璧县"]),("颍州",["颍上县","太和县"]),("亳州",[])]},
  "GEO-08004": {"file": "_data/vol08/08-004_苏州府.json", "direct": ["吴县","长洲县","昆山县","常熟县","吴江县","嘉定县"], "subs": [("太仓州",["崇明县"])]},
  "GEO-09005": {"file": "_data/vol09/09-005_松江府.json", "direct": ["华亭县","上海县","青浦县"], "subs": []},
  "GEO-10006": {"file": "_data/vol10/10-006_常州府.json", "direct": ["武进县","无锡县","江阴县","宜兴县","靖江县"], "subs": []},
  "GEO-11007": {"file": "_data/vol11/11-007_镇江府.json", "direct": ["丹徒县","丹阳县","金坛县"], "subs": []},
  "GEO-13008": {"file": "_data/vol13/13-008_淮安府.json", "direct": ["山阳县","盐城县","清河县","安东县","桃源县","沭阳县"], "subs": [("海州",["赣榆县"]),("邳州",["宿迁县","睢宁县"])]},
  "GEO-14009": {"file": "_data/vol14/14-009_庐州府.json", "direct": ["合肥县","舒城县","庐江县"], "subs": [("无为州",["巢县"]),("六安州",["英山县","霍山县"])]},
  "GEO-14010": {"file": "_data/vol14/14-010_安庆府.json", "direct": ["怀宁县","桐城县","潜山县","太湖县","宿松县","望江县"], "subs": []},
  "GEO-15011": {"file": "_data/vol15/15-011_太平府.json", "direct": ["当涂县","芜湖县","繁昌县"], "subs": []},
  "GEO-15012": {"file": "_data/vol15/15-012_宁国府.json", "direct": ["宣城县","宁国县","泾县","太平县","旌德县","南陵县"], "subs": []},
  "GEO-16013": {"file": "_data/vol16/16-013_池州府.json", "direct": ["贵池县","青阳县","铜陵县","石埭县","建德县","东流县"], "subs": []},
  "GEO-16014": {"file": "_data/vol16/16-014_徽州府.json", "direct": ["歙县","休宁县","婺源县","祁门县","黟县","绩溪县"], "subs": []},
  "GEO-17015": {"file": "_data/vol17/17-015_广徳州.json", "direct": ["建平县"], "subs": []},
}

shan = {
  "GEO-19001": {"file": "_data/vol19/19-001_太原府.json", "direct": ["阳曲县","太原县","榆次县","太谷县","祁县","徐沟县","清源县","交城县","文水县","寿阳县","临县","盂县","静乐县","河曲县"], "subs": [("平定州",["乐平县"]),("忻州",["定襄县"]),("代州",["五台县","繁峙县","崞县"]),("岢岚州",["岚县","兴县"]),("保德州",[]),("永宁州",["宁乡县"])]},
  "GEO-20001": {"file": "_data/vol20/20-001_平阳府.json", "direct": ["临汾县","襄陵县","洪洞县","浮山县","赵城县","太平县","岳阳县","曲沃县","翼城县","汾西县","蒲县"], "subs": [("蒲州",["临晋县","荣河县","猗氏县","万泉县","河津县"]),("解州",["安邑县","夏县","闻喜县","平陆县","芮城县"]),("绛州",["稷山县","绛县","垣曲县"]),("霍州",["灵石县"]),("吉州",["乡宁县"]),("隰州",["大宁县","石楼县","永和县"])]},
  "GEO-21001": {"file": "_data/vol21/21-001_大同府.json", "direct": ["大同县","怀仁县"], "subs": [("浑源州",[]),("应州",["山阴县"]),("朔州",["马邑县"]),("蔚州",["广灵县","广昌县","灵丘县"])]},
  "GEO-21101": {"file": "_data/vol21/21-002_潞安府.json", "direct": ["长治县","长子县","屯留县","襄垣县","潞城县","壶关县","平顺县","黎城县"], "subs": []},
  "GEO-21201": {"file": "_data/vol21/21-003_21-003.json", "direct": ["汾阳县","孝义县","平遥县","介休县"], "subs": []},
  "GEO-21301": {"file": "_data/vol21/21-004_21-004.json", "direct": ["榆社县","和顺县"], "subs": []},
  "GEO-21401": {"file": "_data/vol21/21-005_21-005.json", "direct": ["沁源县","武乡县"], "subs": []},
  "GEO-21501": {"file": "_data/vol21/21-006_21-006.json", "direct": ["高平县","阳城县","陵川县","沁水县"], "subs": []},
}

def build_tree(pref_gid, item_id, region, direct, subs):
    """返回 (新增geo节点列表, 府children列表)"""
    new_geos = []
    children = []
    # 直辖县
    for i, cname in enumerate(direct, 1):
        cid = f"{pref_gid}-c{i:02d}"
        new_geos.append({"geo_id": cid, "name": cname, "type": "county", "parent": pref_gid, "region": region, "item_id": item_id, "children": []})
        children.append(cid)
    # 属州
    for j, (sname, scounties) in enumerate(subs, 1):
        sid = f"{pref_gid}-s{j:02d}"
        s_children = []
        for k, scname in enumerate(scounties, 1):
            scid = f"{sid}-c{k:02d}"
            new_geos.append({"geo_id": scid, "name": scname, "type": "county", "parent": sid, "region": region, "item_id": item_id, "children": []})
            s_children.append(scid)
        new_geos.append({"geo_id": sid, "name": sname, "type": "department", "parent": pref_gid, "region": region, "item_id": item_id, "children": s_children})
        children.append(sid)
    return new_geos, children

total_added = 0
for pref_gid, info in {**nanz, **shan}.items():
    fpath = info["file"]
    if not os.path.exists(fpath):
        print(f"SKIP (no file): {fpath}")
        continue
    d = json.load(open(fpath, encoding="utf-8"))
    region = d.get("region", "")
    item_id = d["item_id"]
    # 找府节点
    pref_node = None
    for g in d["layers"]["geos"]:
        if g["geo_id"] == pref_gid:
            pref_node = g
            break
    if not pref_node:
        print(f"SKIP (no pref node {pref_gid}): {fpath}")
        continue
    # 构建新节点
    new_geos, children = build_tree(pref_gid, item_id, region, info["direct"], info["subs"])
    # 更新府节点 children
    pref_node["children"] = children
    # 追加新 geo 节点
    existing_ids = {g["geo_id"] for g in d["layers"]["geos"]}
    added = 0
    for ng in new_geos:
        if ng["geo_id"] not in existing_ids:
            d["layers"]["geos"].append(ng)
            added += 1
    total_added += added
    # 写回
    with open(fpath, "w", encoding="utf-8") as fp:
        json.dump(d, fp, ensure_ascii=False, indent=2)
    print(f"{os.path.basename(fpath):30s} +{added:3d} nodes, children={len(children)}")

print(f"\n共新增 {total_added} 个 GEO 县/州节点")
