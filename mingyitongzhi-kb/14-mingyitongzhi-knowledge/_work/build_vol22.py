# -*- coding: utf-8 -*-
"""Build vol22 济南府 structured JSON files."""
import json, os

OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol22"
os.makedirs(OUT, exist_ok=True)

ITEM = "22-001"
VOL = "卷22"
REGION = "山东"

# ---- county order (原文出现顺序) ----
counties = [
    # (geo_suffix, name, parent_geo, location_text, households_count, households_note)
    ("c01", "历城县", "GEO-22001", "附郭", 98, "编户九十八里"),
    ("c02", "章丘县", "GEO-22001", "在府城东一百一十里", 103, "编户一百三里"),
    ("c03", "邹平县", "GEO-22001", "在府城东北一百八十里", 57, "编户五十七里"),
    ("c04", "淄川县", "GEO-22001", "在府城东二百三十里", 60, "编户六十里"),
    ("c05", "长山县", "GEO-22001", "在府城东北二百里", 63, "编户六十三里"),
    ("c06", "新城县", "GEO-22001", "在府城东北三百二十里", 45, "编户四十五里"),
    ("c07", "齐河县", "GEO-22001", "在府城西五十里", 27, "编户二十七里"),
    ("c08", "齐东县", "GEO-22001", "在府城东北一百八十里", 55, "编户五十五里"),
    ("c09", "济阳县", "GEO-22001", "在府城北九十里", 58, "编户五十八里"),
    ("c10", "禹城县", "GEO-22001", "在府城西北一百里", 56, "编户五十六里"),
    ("c11", "临邑县", "GEO-22001", "在府城北一百五十里", 32, "编户三十二里"),
    ("c12", "长清县", "GEO-22001", "在府城西南七十里", 44, "编户四十四里"),
    ("c13", "肥城县", "GEO-22001", "在府城西南一百六十里", 30, "编户三十里"),
    ("c14", "青城县", "GEO-22001", "在府城东北二百二十里", 33, "编户三十三里"),
    ("c15", "陵县", "GEO-22001", "在府城西北二百四十里", 32, "编户三十二里"),
    ("c16", "新泰县", "GEO-22001-s01", "在州城东南一百八十里", 21, "编户二十一里"),
    ("c17", "莱芜县", "GEO-22001-s01", "在州城东一百二十里", 42, "编户四十二里"),
    ("c18", "德平县", "GEO-22001-s02", "在州城东一百六十里", 41, "编户四十一里"),
    ("c19", "平原县", "GEO-22001-s02", "在州城东南一百二十里", 46, "编户四十六里"),
    ("c20", "阳信县", "GEO-22001-s03", "在州城北四十里", 70, "编户七十里"),
    ("c21", "海丰县", "GEO-22001-s03", "在州城东北六十里", 43, "编户四十三里"),
    ("c22", "乐陵县", "GEO-22001-s03", "在府城西北九十里", 56, "编户五十六里"),
    ("c23", "商河县", "GEO-22001-s03", "在州城南一百二十里", 68, "编户六十八里"),
    ("c24", "利津县", "GEO-22001-s04", "在州城东六十里", 40, "编户四十里"),
    ("c25", "沾化县", "GEO-22001-s04", "在州城西北六十里", 24, "编户二十四里"),
    ("c26", "蒲台县", "GEO-22001-s04", "在州城南三十里", 59, "编户五十九里"),
]

subprefectures = [
    ("s01", "泰安州", "GEO-22001", "在府城南一百八十里", 97, "编户九十七里", ["c16","c17"]),
    ("s02", "德州", "GEO-22001", "在府城西北二百八十里", 34, "编户三十四里", ["c18","c19"]),
    ("s03", "武定州", "GEO-22001", "在府城东北七十里", 98, "编户九十八里", ["c20","c21","c22","c23"]),
    ("s04", "滨州", "GEO-22001", "在府城东北三百五十里", 78, "编户七十八里", ["c24","c25","c26"]),
]

weisuo = [
    ("w01", "济南卫", "GEO-22001", "卫", "在府城内西南隅洪武十九年建"),
    ("w02", "德州卫", "GEO-22001", "卫", "在府治西洪武九年以千户所改建"),
    ("w03", "德州左卫", "GEO-22001", "卫", "在州治西北永乐五年建"),
    ("w04", "武定州守御千户所", "GEO-22001", "千户所", "在州治南洪武元年建为乐安千户所宣德元年改为武定"),
    ("w05", "肥城守御千户所", "GEO-22001", "千户所", "在县治西洪武二十一年建"),
]

def geo_id(suffix):
    return "GEO-22001-" + suffix

# Build county geo map
county_geo = {}
for suf, name, parent, loc, hc, hn in counties:
    cid = geo_id(suf)
    county_geo[name] = cid

# ---- GEO nodes ----
geos = []

# prefecture children: direct counties c01-c15, subprefectures s01-s04, weisuo w01-w05
direct_counties = [geo_id(s[0]) for s in counties if s[2] == "GEO-22001"]
sp_children = [geo_id(s[0]) for s in subprefectures]
ws_children = [geo_id(w[0]) for w in weisuo]

geos.append({
    "geo_id": "GEO-22001",
    "item_id": ITEM,
    "name": "济南府",
    "type": "prefecture",
    "region": REGION,
    "parent": "GEO-000",
    "children": direct_counties + sp_children + ws_children,
    "volume_range": VOL,
    "attributes": {
        "borders": [
            {"direction": "东", "to_place": "青州府临淄县界", "distance_li": 250},
            {"direction": "西", "to_place": "东昌府茌平县界", "distance_li": 140},
            {"direction": "南", "to_place": "兖州府宁阳县界", "distance_li": 300},
            {"direction": "北", "to_place": "直隶河间府景州吴桥县界", "distance_li": 317},
        ],
        "to_capital": [
            {"capital": "京师", "distance_li": 900},
            {"capital": "南京", "distance_li": 1850},
        ],
        "households": {"count": None, "unit": "里", "note": "领州四县二十六；各属州县编户见下"},
        "grain_tax": {"amount": 851600, "unit": "石", "note": "粮八十五万一千六百石零"},
        "jun_name": "济南【汉名】",
        "topography": "南有泰山之固【田肯说汉高祖】；凭负山海【杜氏通典】；北枕鬲津西临漳水【德州志】；介山东两路之间最为冲要【金史蒙古纲传】；地险于海【郡国志】；有崇山巨浸【元程文遂闲堂记】",
        "customs": "俗多织作【汉书地理志】；士务功名【同上】；习尚淳厚民皆务本【棣州志】；敦厚阔大多大节【元程文遂闲堂记】",
        "garrisons": [
            {"name": "都转运盐使司", "type": "司", "location_text": "在府治东洪武元年建"},
            {"name": "济南卫", "type": "卫", "location_text": "在府城内西南隅洪武十九年建"},
            {"name": "直隶德州卫", "type": "卫", "location_text": "在府治西洪武九年以千户所改建"},
            {"name": "直隶德州左卫", "type": "卫", "location_text": "在州治西北永乐五年建"},
            {"name": "直隶武定州守御千户所", "type": "千户所", "location_text": "在州治南洪武元年建"},
            {"name": "肥城守御千户所", "type": "千户所", "location_text": "在县治西洪武二十一年建"},
        ],
        "fiefs": [
            {"name": "德王府", "type": "王府", "note": "府城内成化三年建"},
            {"name": "临朐王府", "type": "王府", "note": "同城"},
            {"name": "宁海王府", "type": "王府", "note": "同城"},
            {"name": "临清王府", "type": "王府", "note": "同城"},
        ],
    },
    "cit_ids": ["CIT-001","CIT-002","CIT-003","CIT-004","CIT-005","CIT-006","CIT-007","CIT-008"],
})

# subprefecture nodes
for suf, name, parent, loc, hc, hn, child_counties in subprefectures:
    cid = geo_id(suf)
    kids = [geo_id(cc) for cc in child_counties]
    geos.append({
        "geo_id": cid,
        "item_id": ITEM,
        "name": name,
        "type": "subprefecture",
        "region": REGION,
        "parent": parent,
        "children": kids,
        "volume_range": VOL,
        "attributes": {
            "location_text": loc,
            "households": {"count": hc, "unit": "里", "note": hn},
        },
    })

# county nodes
for suf, name, parent, loc, hc, hn in counties:
    cid = geo_id(suf)
    geos.append({
        "geo_id": cid,
        "item_id": ITEM,
        "name": name,
        "type": "county",
        "region": REGION,
        "parent": parent,
        "children": [],
        "volume_range": VOL,
        "attributes": {
            "location_text": loc,
            "households": {"count": hc, "unit": "里", "note": hn},
        },
    })

# weisuo nodes
for suf, name, parent, wtype, loc in weisuo:
    cid = geo_id(suf)
    geos.append({
        "geo_id": cid,
        "item_id": ITEM,
        "name": name,
        "type": "weisuo",
        "region": REGION,
        "parent": parent,
        "children": [],
        "volume_range": VOL,
        "attributes": {"location_text": loc, "garrison_type": wtype},
    })

# ---- EVO chain (济南府) ----
evos = [
    {"evo_id":"EVO-001","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"周","era":None,"institution_name":"青州之域","action":"因之","detail":"禹贡青州之域，天文危分野"},
    {"evo_id":"EVO-002","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"春秋战国","era":None,"institution_name":"齐地","action":"因之","detail":"春秋战国并为齐地"},
    {"evo_id":"EVO-003","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"秦","era":None,"institution_name":"齐郡地","action":"置郡","detail":"秦属齐郡"},
    {"evo_id":"EVO-004","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"汉","era":"文帝","institution_name":"济南国","action":"置","detail":"汉初属齐国，文帝分置济南国"},
    {"evo_id":"EVO-005","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"汉","era":"景帝","institution_name":"济南郡","action":"改","detail":"景帝改为济南郡，东汉仍为国，俱治东平陵"},
    {"evo_id":"EVO-006","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"晋","era":None,"institution_name":"历城","action":"迁","detail":"晋移治历城"},
    {"evo_id":"EVO-007","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"南北朝","era":"刘宋","institution_name":"侨立冀州","action":"置","detail":"刘宋割青州西部于此侨立冀州"},
    {"evo_id":"EVO-008","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"南北朝","era":"后魏","institution_name":"齐州兼济南郡","action":"改","detail":"后魏改为齐州，兼置济南郡"},
    {"evo_id":"EVO-009","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"隋","era":None,"institution_name":"齐郡","action":"改","detail":"隋初置郡存州，后改为齐郡"},
    {"evo_id":"EVO-010","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"唐","era":"天宝","institution_name":"临淄郡/济南郡","action":"改","detail":"唐复为齐州，天宝初改为临淄郡，寻改为济南郡，乾元初复为齐州"},
    {"evo_id":"EVO-011","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"宋","era":None,"institution_name":"济南府","action":"升","detail":"宋升为兴德军，又升为济南府"},
    {"evo_id":"EVO-012","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"金","era":None,"institution_name":"济南府","action":"因之","detail":"金因之"},
    {"evo_id":"EVO-013","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"元","era":None,"institution_name":"济南路","action":"改","detail":"元改为济南路"},
    {"evo_id":"EVO-014","item_id":ITEM,"geo_id":"GEO-22001","dynasty":"明","era":None,"institution_name":"济南府","action":"因之","detail":"本朝复改为济南府，领州四县二十六"},
]

# ---- CIT ----
cits = [
    {"cit_id":"CIT-001","item_id":ITEM,"cited_work":"田肯","cited_work_ent_id":None,"context":"立论","original":"【田肯说汉高祖】"},
    {"cit_id":"CIT-002","item_id":ITEM,"cited_work":"杜氏通典","cited_work_ent_id":None,"context":"立论","original":"【杜氏通典】"},
    {"cit_id":"CIT-003","item_id":ITEM,"cited_work":"德州志","cited_work_ent_id":None,"context":"立论","original":"【德州志】"},
    {"cit_id":"CIT-004","item_id":ITEM,"cited_work":"金史","cited_work_ent_id":None,"context":"立论","original":"【金史蒙古纲传】"},
    {"cit_id":"CIT-005","item_id":ITEM,"cited_work":"郡国志","cited_work_ent_id":None,"context":"考源","original":"【郡国志】"},
    {"cit_id":"CIT-006","item_id":ITEM,"cited_work":"程文遂闲堂记","cited_work_ent_id":None,"context":"立论","original":"【元程文遂闲堂记】"},
    {"cit_id":"CIT-007","item_id":ITEM,"cited_work":"汉书地理志","cited_work_ent_id":None,"context":"证俗","original":"【汉书地理志】"},
    {"cit_id":"CIT-008","item_id":ITEM,"cited_work":"棣州志","cited_work_ent_id":None,"context":"证俗","original":"【棣州志】"},
]

# ---- ENTS (key entities) ----
ents = [
    {"ent_id":"ENT-001","name":"济南府","type":"geo","norm":"济南府","first_source":ITEM},
    {"ent_id":"ENT-002","name":"泰安州","type":"geo","norm":"泰安州","first_source":ITEM},
    {"ent_id":"ENT-003","name":"德州","type":"geo","norm":"德州","first_source":ITEM},
    {"ent_id":"ENT-004","name":"武定州","type":"geo","norm":"武定州","first_source":ITEM},
    {"ent_id":"ENT-005","name":"滨州","type":"geo","norm":"滨州","first_source":ITEM},
    {"ent_id":"ENT-006","name":"泰山","type":"mtn","norm":"泰山","first_source":ITEM},
    {"ent_id":"ENT-007","name":"大明湖","type":"mtn","norm":"大明湖","first_source":ITEM},
    {"ent_id":"ENT-008","name":"趵突泉","type":"mtn","norm":"趵突泉","first_source":ITEM},
    {"ent_id":"ENT-009","name":"通典","type":"book","norm":"通典","first_source":ITEM},
    {"ent_id":"ENT-010","name":"杜甫","type":"person","norm":"杜甫","first_source":ITEM},
    {"ent_id":"ENT-011","name":"曾巩","type":"person","norm":"曾巩","first_source":ITEM},
    {"ent_id":"ENT-012","name":"李白","type":"person","norm":"李白","first_source":ITEM},
    {"ent_id":"ENT-013","name":"辛弃疾","type":"person","norm":"辛弃疾","first_source":ITEM},
    {"ent_id":"ENT-014","name":"张养浩","type":"person","norm":"张养浩","first_source":ITEM},
    {"ent_id":"ENT-015","name":"铁铉","type":"person","norm":"铁铉","first_source":ITEM},
]

import pickle
with open(os.path.join(OUT, "_skeleton.pkl"), "wb") as f:
    pickle.dump({"geos":geos,"evos":evos,"cits":cits,"ents":ents,
                 "counties":counties,"subprefectures":subprefectures,"weisuo":weisuo}, f)
print("skeleton written, geos=", len(geos))
