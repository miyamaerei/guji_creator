"""把 shuntian_counties_draft.json 转成标准县文件，输出到 _data/vol01/"""
import json, os, re

WORK = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_work"
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol01"

# 县清单: (code, name, parent_geo_id, parent_label)
# parent: GEO-01002 = 顺天府, s01=通州, s02=昌平州, s03=涿州, s04=霸州, s05=蓟州
COUNTIES = [
    ("c01", "大兴县", "GEO-01002", "顺天府"),
    ("c02", "宛平县", "GEO-01002", "顺天府"),
    ("c03", "良乡县", "GEO-01002", "顺天府"),
    ("c04", "固安县", "GEO-01002", "顺天府"),
    ("c05", "永清县", "GEO-01002", "顺天府"),
    ("c06", "东安县", "GEO-01002", "顺天府"),
    ("c07", "香河县", "GEO-01002", "顺天府"),
    ("c08", "三河县", "GEO-01002-s01", "通州"),
    ("c09", "武清县", "GEO-01002-s01", "通州"),
    ("c10", "漷县",   "GEO-01002-s01", "通州"),
    ("c11", "宝坻县", "GEO-01002-s01", "通州"),
    ("c12", "顺义县", "GEO-01002-s02", "昌平州"),
    ("c13", "密云县", "GEO-01002-s02", "昌平州"),
    ("c14", "怀柔县", "GEO-01002-s02", "昌平州"),
    ("c15", "房山县", "GEO-01002-s03", "涿州"),
    ("c16", "文安县", "GEO-01002-s04", "霸州"),
    ("c17", "大城县", "GEO-01002-s04", "霸州"),
    ("c18", "保定县", "GEO-01002-s04", "霸州"),
    ("c19", "玉田县", "GEO-01002-s05", "蓟州"),
    ("c20", "丰润县", "GEO-01002-s05", "蓟州"),
    ("c21", "遵化县", "GEO-01002-s05", "蓟州"),
    ("c22", "平谷县", "GEO-01002-s05", "蓟州"),
]

draft = json.load(open(os.path.join(WORK, "shuntian_counties_draft.json"), encoding="utf-8"))

os.makedirs(OUT, exist_ok=True)
summary = []
for code, cname, parent, parent_label in COUNTIES:
    d = draft.get(cname, {"evo":"","mtns":[],"sites":[],"pers":[]})
    geo_id = f"GEO-01002-{code}"
    county_node = {
        "geo_id": geo_id,
        "item_id": "01-002",
        "name": cname,
        "type": "county",
        "region": "北直隶",
        "parent": parent,
        "children": [],
        "volume_range": "卷1",
        "attributes": {
            "evo_summary": d.get("evo", "")[:200],
        },
        "original": d.get("evo", "")[:300],
    }
    # evos: 把 evo 文本拆成沿革链（简化：一条记录）
    evos = []
    if d.get("evo"):
        evos.append({
            "evo_id": f"EVO-01002-{code}",
            "item_id": "01-002",
            "geo_id": geo_id,
            "dynasty": "未明",
            "era": None,
            "institution_name": cname,
            "action": "因之",
            "detail": d["evo"],
            "original": d["evo"],
        })
    # mtns
    mtns = []
    for i, m in enumerate(d.get("mtns", []), 1):
        mtns.append({
            "mtn_id": f"MTN-01002-{code}-{i:02d}",
            "item_id": "01-002",
            "geo_id": geo_id,
            "name": m["name"],
            "type": m["type"],
            "location_text": m["location_text"],
            "description": m["description"],
            "lore": "",
            "original": m["original"],
        })
    # sites
    sites = []
    for i, s in enumerate(d.get("sites", []), 1):
        sites.append({
            "site_id": f"SITE-01002-{code}-{i:02d}",
            "item_id": "01-002",
            "geo_id": geo_id,
            "name": s["name"],
            "type": s["type"],
            "location_text": s["location_text"],
            "history_lore": s["history_lore"],
            "original": s["original"],
        })
    # pers
    pers = []
    for i, p in enumerate(d.get("pers", []), 1):
        pers.append({
            "per_id": f"PER-01002-{code}-{i:02d}",
            "item_id": "01-002",
            "geo_id": geo_id,
            "name": p["name"],
            "type": p["type"],
            "dynasty": "未明",
            "native_place": "",
            "office": "",
            "summary": p["summary"],
            "original": p["original"],
        })
    # ents: 该县本身 + 县名
    ents = [
        {"ent_id": f"ENT-01002-{code}", "name": cname, "type": "geo", "norm": cname, "first_source": "01-002"},
    ]
    cits = []
    obj = {
        "item_id": "01-002",
        "volume": "01",
        "source": cname,
        "region": "北直隶",
        "original": d.get("evo", "")[:300],
        "layers": {
            "ents": ents,
            "geos": [county_node],
            "evos": evos,
            "mtns": mtns,
            "pers": pers,
            "sites": sites,
            "prods": [],
            "cits": cits,
        },
        "layer_count": 7,
        "validation": {
            "errs": [],
            "gap": 0,
            "notes": f"parent={parent_label}; auto-extracted, pending manual review"
        }
    }
    fname = f"01-002_{code}_{cname}.json"
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    summary.append(f"{fname}: evo={len(evos)} mtn={len(mtns)} site={len(sites)} per={len(pers)}")

print("\n".join(summary))
print(f"\n共 {len(summary)} 个县文件已生成到 {OUT}")
