# -*- coding: utf-8 -*-
"""Generate vol124 (景东府), vol125 (广南府), vol126 (广西府) JSON files."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "_data")

def dump(obj, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

# ============================================================
# vol124 — 景东府
# ============================================================
V124 = "124"
I124 = "124-001"

ents_124 = [
    {"ent_id": "ENT-001", "name": "景东府", "type": "geo", "norm": "景东府", "first_source": I124},
    {"ent_id": "ENT-W01", "name": "景东卫", "type": "geo", "norm": "景东卫", "first_source": I124},
    {"ent_id": "ENT-K量董山", "name": "量董山", "type": "mtn", "norm": "量董山", "first_source": I124},
    {"ent_id": "ENT-K邦泰山", "name": "邦泰山", "type": "mtn", "norm": "邦泰山", "first_source": I124},
    {"ent_id": "ENT-K鹤笼山", "name": "鹤笼山", "type": "mtn", "norm": "鹤笼山", "first_source": I124},
    {"ent_id": "ENT-K防乐山", "name": "防乐山", "type": "mtn", "norm": "防乐山", "first_source": I124},
    {"ent_id": "ENT-K澜沧江", "name": "澜沧江", "type": "mtn", "norm": "澜沧江", "first_source": I124},
    {"ent_id": "ENT-K大河", "name": "大河", "type": "mtn", "norm": "大河", "first_source": I124},
    {"ent_id": "ENT-K龙潭", "name": "龙潭", "type": "mtn", "norm": "龙潭", "first_source": I124},
    {"ent_id": "ENT-K笕泉", "name": "笕泉", "type": "mtn", "norm": "笕泉", "first_source": I124},
]

geos_124 = [
    {
        "geo_id": "GEO-124001",
        "item_id": I124,
        "name": "景东府",
        "type": "prefecture",
        "region": "云南",
        "parent": "GEO-000",
        "children": ["GEO-124001-w01"],
        "volume_range": "卷124",
        "attributes": {
            "borders": [
                {"direction": "东", "to_place": "楚雄府楚雄县界", "distance_li": 320},
                {"direction": "西", "to_place": "大侯州界", "distance_li": 360},
                {"direction": "南", "to_place": "威逺州界", "distance_li": 400},
                {"direction": "北", "to_place": "楚雄府定邉县界", "distance_li": 200},
            ],
            "to_capital": [
                {"capital": "南京", "distance_li": 8180},
                {"capital": "京师", "distance_li": 11600},
            ],
            "households": {"count": 8, "unit": "里", "note": "亲领编户八里"},
            "grain_tax": {"amount": None, "unit": "石", "note": ""},
            "jun_name": "开南【元名】",
            "topography": "荒僻之地【元史开南州徼外荒僻之地庄蹻王滇池汉武开西南夷诸葛孔明定益州皆未尝涉其境】；控扼之所【郡志东有邦泰山之秀南有孟沼山之防景董山峙其西防乐山耸其北地接极邉是亦控扼之所】；水城绕郡【云南志】",
            "customs": "民多百夷田皆种秫【郡志】；不通汉书惟用缅字【同上】",
            "garrisons": [
                {"name": "景东卫", "type": "卫", "location_text": "在府北卫城中洪武二十三年建"}
            ],
        },
        "cit_ids": ["CIT-001", "CIT-002", "CIT-003"],
    },
    {
        "geo_id": "GEO-124001-w01",
        "item_id": I124,
        "name": "景东卫",
        "type": "weisuo",
        "region": "云南",
        "parent": "GEO-124001",
        "children": [],
        "volume_range": "卷124",
        "attributes": {
            "location_text": "在府北卫城中",
            "garrison_type": "卫",
        },
    },
]

evos_124 = [
    {"evo_id": "EVO-001", "item_id": I124, "geo_id": "GEO-124001", "dynasty": "唐", "era": None, "institution_name": "银生府", "action": "因之", "detail": "唐时南诏蒙氏为银生府之地，旧为濮落杂蛮所居，后金齿白蛮侵夺其地"},
    {"evo_id": "EVO-002", "item_id": I124, "geo_id": "GEO-124001", "dynasty": "宋", "era": None, "institution_name": "大理段氏地", "action": "因之", "detail": "宋时大理段氏莫能复"},
    {"evo_id": "EVO-003", "item_id": I124, "geo_id": "GEO-124001", "dynasty": "元", "era": "中统/至元", "institution_name": "开南州", "action": "置", "detail": "元中统初讨平之，以其所部隶威楚万户；至元中置开南州，隶威楚路"},
    {"evo_id": "EVO-004", "item_id": I124, "geo_id": "GEO-124001", "dynasty": "明", "era": "洪武", "institution_name": "景东府", "action": "改", "detail": "本朝洪武中改为景东府，亲领编户八里"},
]

mtns_124 = [
    {"mtn_id": "MTN-001", "item_id": I124, "geo_id": "GEO-124001", "name": "量董山", "type": "山", "location_text": "在府治西", "description": "昔为酋寨，今立卫地其上", "lore": ""},
    {"mtn_id": "MTN-002", "item_id": I124, "geo_id": "GEO-124001", "name": "邦泰山", "type": "山", "location_text": "在府治东", "description": "高耸延长，土官世居其麓", "lore": ""},
    {"mtn_id": "MTN-003", "item_id": I124, "geo_id": "GEO-124001", "name": "鹤笼山", "type": "山", "location_text": "在府北三十里", "description": "一峰突兀，其顶盘圆", "lore": ""},
    {"mtn_id": "MTN-004", "item_id": I124, "geo_id": "GEO-124001", "name": "防乐山", "type": "山", "location_text": "在府北九十里", "description": "一名无量山，高不可跻，连亘三百余里，中有石洞深不可测，一峰特出状若崆峒，蒙氏封为南岳；其南有泉为通华河，其北有泉为清水河，俱东入于大河", "lore": ""},
    {"mtn_id": "MTN-005", "item_id": I124, "geo_id": "GEO-124001", "name": "澜沧江", "type": "江", "location_text": "俗名浪沧", "description": "源出金齿，流经府西南二百余里，南注车里", "lore": ""},
    {"mtn_id": "MTN-006", "item_id": I124, "geo_id": "GEO-124001", "name": "大河", "type": "江", "location_text": "源定邉县阿茊村", "description": "合三岔河，经府治东南，入马龙江", "lore": ""},
    {"mtn_id": "MTN-007", "item_id": I124, "geo_id": "GEO-124001", "name": "龙潭", "type": "潭", "location_text": "在府北九十里", "description": "岁旱祷雨有应", "lore": ""},
    {"mtn_id": "MTN-008", "item_id": I124, "geo_id": "GEO-124001-w01", "name": "笕泉", "type": "泉", "location_text": "源出防乐山", "description": "以竹笕引入卫城，凿池潴之，上覆以亭", "lore": ""},
]

cits_124 = [
    {"cit_id": "CIT-001", "item_id": I124, "cited_work": "元史", "cited_work_ent_id": None, "context": "形胜", "original": "【元史开南州徼外荒僻之地庄蹻王滇池汉武开西南夷诸葛孔明定益州皆未尝涉其境】"},
    {"cit_id": "CIT-002", "item_id": I124, "cited_work": "郡志", "cited_work_ent_id": None, "context": "形胜", "original": "【郡志东有邦泰山之秀南有孟沼山之防景董山峙其西防乐山耸其北地接极邉是亦控扼之所】"},
    {"cit_id": "CIT-003", "item_id": I124, "cited_work": "云南志", "cited_work_ent_id": None, "context": "形胜", "original": "【云南志水城绕郡】"},
]

main_124 = {
    "item_id": I124,
    "volume": V124,
    "source": "景东府",
    "region": "云南",
    "layers": {
        "ents": ents_124,
        "geos": geos_124,
        "evos": evos_124,
        "mtns": mtns_124,
        "pers": [],
        "sites": [],
        "prods": [],
        "cits": cits_124,
    },
    "layer_count": 7,
    "validation": {"errs": [], "gap": 0, "notes": "亲领；卫所w01；sites拆至sites1/2"},
    "title": "景东府",
}

sites1_124 = {
    "item_id": I124, "volume": V124, "source": "景东府", "region": "云南",
    "layers": {
        "ents": [], "geos": [], "evos": [], "mtns": [], "pers": [],
        "sites": [
            {"site_id": "SITE-001", "item_id": I124, "geo_id": "GEO-124001", "name": "开化寺", "type": "寺观", "location_text": "在府治南", "history_lore": "", "original": "开化寺【在府治南】"},
            {"site_id": "SITE-002", "item_id": I124, "geo_id": "GEO-124001", "name": "龙泉寺", "type": "寺观", "location_text": "在府治东", "history_lore": "", "original": "龙泉寺【在府治东】"},
            {"site_id": "SITE-003", "item_id": I124, "geo_id": "GEO-124001", "name": "真武观", "type": "寺观", "location_text": "在府治西", "history_lore": "", "original": "真武观【在府治西】"},
        ],
        "prods": [], "cits": [],
    },
    "layer_count": 7, "title": "景东府",
}

sites2_124 = {
    "item_id": I124, "volume": V124, "source": "景东府", "region": "云南",
    "layers": {
        "ents": [], "geos": [], "evos": [], "mtns": [], "pers": [],
        "sites": [
            {"site_id": "SITE-001", "item_id": I124, "geo_id": "GEO-124001", "name": "母关", "type": "关梁", "location_text": "在府南一百里", "history_lore": "", "original": "母关【在府南一百里】"},
            {"site_id": "SITE-002", "item_id": I124, "geo_id": "GEO-124001", "name": "安定关", "type": "关梁", "location_text": "在府北一百五十里", "history_lore": "", "original": "安定关【在府北一百五十里】"},
            {"site_id": "SITE-003", "item_id": I124, "geo_id": "GEO-124001", "name": "景阑关", "type": "关梁", "location_text": "在府东南一百二十里", "history_lore": "", "original": "景阑关【在府东南一百二十里】"},
            {"site_id": "SITE-004", "item_id": I124, "geo_id": "GEO-124001", "name": "通华桥", "type": "关梁", "location_text": "在府治北跨通华河", "history_lore": "", "original": "通华桥【在府治北跨通华河】"},
            {"site_id": "SITE-005", "item_id": I124, "geo_id": "GEO-124001-w01", "name": "景东卫学", "type": "学校", "location_text": "在卫城泰安门外", "history_lore": "正统七年建", "original": "景东卫学【在卫城泰安门外正统七年建】"},
        ],
        "prods": [], "cits": [],
    },
    "layer_count": 7, "title": "景东府",
}

w01_124 = {
    "item_id": I124, "volume": V124, "source": "景东卫", "region": "云南",
    "layers": {
        "ents": [{"ent_id": "ENT-W01", "name": "景东卫", "type": "geo", "norm": "景东卫", "first_source": I124}],
        "geos": [], "evos": [], "mtns": [], "pers": [], "sites": [], "prods": [], "cits": [],
    },
    "layer_count": 7, "title": "景东府",
}

# ============================================================
# vol125 — 广南府
# ============================================================
V125 = "125"
I125 = "125-001"

ents_125 = [
    {"ent_id": "ENT-001", "name": "广南府", "type": "geo", "norm": "广南府", "first_source": I125},
    {"ent_id": "ENT-S01", "name": "富州", "type": "geo", "norm": "富州", "first_source": I125},
    {"ent_id": "ENT-K牌头山", "name": "牌头山", "type": "mtn", "norm": "牌头山", "first_source": I125},
    {"ent_id": "ENT-K莲花山", "name": "莲花山", "type": "mtn", "norm": "莲花山", "first_source": I125},
    {"ent_id": "ENT-K祛丕山", "name": "祛丕山", "type": "mtn", "norm": "祛丕山", "first_source": I125},
    {"ent_id": "ENT-K玉泉山", "name": "玉泉山", "type": "mtn", "norm": "玉泉山", "first_source": I125},
    {"ent_id": "ENT-K者鹞山", "name": "者鹞山", "type": "mtn", "norm": "者鹞山", "first_source": I125},
    {"ent_id": "ENT-K西宁山", "name": "西宁山", "type": "mtn", "norm": "西宁山", "first_source": I125},
    {"ent_id": "ENT-K西洋江", "name": "西洋江", "type": "mtn", "norm": "西洋江", "first_source": I125},
    {"ent_id": "ENT-K南水溪", "name": "南水溪", "type": "mtn", "norm": "南水溪", "first_source": I125},
    {"ent_id": "ENT-K南汪溪", "name": "南汪溪", "type": "mtn", "norm": "南汪溪", "first_source": I125},
]

geos_125 = [
    {
        "geo_id": "GEO-125001",
        "item_id": I125,
        "name": "广南府",
        "type": "prefecture",
        "region": "云南",
        "parent": "GEO-000",
        "children": ["GEO-125001-s01"],
        "volume_range": "卷125",
        "attributes": {
            "borders": [
                {"direction": "东", "to_place": "广西泗城州界", "distance_li": 120},
                {"direction": "西", "to_place": "广西府维摩州界", "distance_li": 150},
                {"direction": "南", "to_place": "古器野界", "distance_li": 60},
                {"direction": "北", "to_place": "泗城州界", "distance_li": 240},
            ],
            "to_capital": [
                {"capital": "南京", "distance_li": 7990},
                {"capital": "京师", "distance_li": 11430},
            ],
            "households": {"count": 6, "unit": "里", "note": "亲领编户六里；领州一"},
            "grain_tax": {"amount": 1000, "unit": "石", "note": "粮一千石零"},
            "jun_name": "广南【元名】",
            "topography": "山崖高峻【郡志山崖险峻道途崎岖一夫当隘百夫莫入其地险固若金城汤池】",
            "customs": "习俗俭约【郡志其地多侬人沙人习俗俭约男女皆事犁锄服短衣长袴构楼而居好食百虫大防病不服药惟务祭鬼而已】；嚚讼好斗【安宁州旧志州有盐井之利嚚讼好斗蛮俗之常】",
            "garrisons": [],
        },
        "cit_ids": ["CIT-001", "CIT-002"],
    },
    {
        "geo_id": "GEO-125001-s01",
        "item_id": I125,
        "name": "富州",
        "type": "department",
        "region": "云南",
        "parent": "GEO-125001",
        "children": [],
        "volume_range": "卷125",
        "attributes": {
            "location_text": "在府城东二百里",
            "households": {"count": 4, "unit": "里", "note": "编户四里"},
        },
    },
]

evos_125 = [
    {"evo_id": "EVO-001", "item_id": I125, "geo_id": "GEO-125001", "dynasty": "宋", "era": None, "institution_name": "特磨道", "action": "因之", "detail": "宋时名特磨道，侬智高之裔居之"},
    {"evo_id": "EVO-002", "item_id": I125, "geo_id": "GEO-125001", "dynasty": "元", "era": "至元", "institution_name": "广南西道宣抚司", "action": "置", "detail": "元至元间立广南西道宣抚司，领路城等五州；后来安路夺其路城、上林、罗佐三州，惟领安宁及富二州"},
    {"evo_id": "EVO-003", "item_id": I125, "geo_id": "GEO-125001", "dynasty": "明", "era": "洪武", "institution_name": "广南府", "action": "改", "detail": "本朝洪武中置广南府，亲领编户六里，领州一"},
]

mtns_125 = [
    {"mtn_id": "MTN-001", "item_id": I125, "geo_id": "GEO-125001", "name": "牌头山", "type": "山", "location_text": "在府城西北五里", "description": "峰峦起伏，其右小山连峙如盾，土民筑寨其上", "lore": ""},
    {"mtn_id": "MTN-002", "item_id": I125, "geo_id": "GEO-125001", "name": "莲花山", "type": "山", "location_text": "在府城东北二十里", "description": "五峰连耸，诸小峰参差傍峙，形如莲花", "lore": ""},
    {"mtn_id": "MTN-003", "item_id": I125, "geo_id": "GEO-125001-s01", "name": "祛丕山", "type": "山", "location_text": "在冨州治西", "description": "形如石狮，昔土人结屋以避兵，名狮头寨", "lore": ""},
    {"mtn_id": "MTN-004", "item_id": I125, "geo_id": "GEO-125001-s01", "name": "玉泉山", "type": "山", "location_text": "在冨州西北七十里", "description": "山顶有泉飞流如素练，下有石池清碧，回旋溢流于西洋江", "lore": ""},
    {"mtn_id": "MTN-005", "item_id": I125, "geo_id": "GEO-125001-s01", "name": "者鹞山", "type": "山", "location_text": "在冨州东南九十里", "description": "高可一百仞，怪石槎枒", "lore": ""},
    {"mtn_id": "MTN-006", "item_id": I125, "geo_id": "GEO-125001-s01", "name": "西宁山", "type": "山", "location_text": "在冨州东北一百一十里", "description": "下有岩洞深邃，土人隐遁其中", "lore": ""},
    {"mtn_id": "MTN-007", "item_id": I125, "geo_id": "GEO-125001", "name": "西洋江", "type": "江", "location_text": "在府城南八十里", "description": "源出本府板郎山、速部山、木玉山三流相合，东南入于田州府右江", "lore": ""},
    {"mtn_id": "MTN-008", "item_id": I125, "geo_id": "GEO-125001-s01", "name": "南水溪", "type": "溪", "location_text": "在冨州东三十里", "description": "源出花梁山，其水尚温", "lore": ""},
    {"mtn_id": "MTN-009", "item_id": I125, "geo_id": "GEO-125001-s01", "name": "南汪溪", "type": "溪", "location_text": "在富州治西", "description": "源出麻卯山暨僻令山，流至州南合南水溪，东行至石洞伏流十五里复出，入于右江", "lore": ""},
]

cits_125 = [
    {"cit_id": "CIT-001", "item_id": I125, "cited_work": "郡志", "cited_work_ent_id": None, "context": "形胜/风俗", "original": "【郡志山崖险峻道途崎岖一夫当隘百夫莫入其地险固若金城汤池】"},
    {"cit_id": "CIT-002", "item_id": I125, "cited_work": "安宁州旧志", "cited_work_ent_id": None, "context": "风俗", "original": "【安宁州旧志州有盐井之利嚚讼好斗蛮俗之常】"},
]

main_125 = {
    "item_id": I125, "volume": V125, "source": "广南府", "region": "云南",
    "layers": {
        "ents": ents_125, "geos": geos_125, "evos": evos_125,
        "mtns": mtns_125, "pers": [], "sites": [], "prods": [], "cits": cits_125,
    },
    "layer_count": 7,
    "validation": {"errs": [], "gap": 0, "notes": "领州一富州s01占位"},
    "title": "广南府",
}

s01_125 = {
    "item_id": I125, "volume": V125, "source": "富州", "region": "云南",
    "layers": {
        "ents": [{"ent_id": "ENT-S01", "name": "富州", "type": "geo", "norm": "富州", "first_source": I125}],
        "geos": [], "evos": [], "mtns": [], "pers": [], "sites": [], "prods": [], "cits": [],
    },
    "layer_count": 7, "title": "广南府",
}

# ============================================================
# vol126 — 广西府
# ============================================================
V126 = "126"
I126 = "126-001"

mtn_names_126 = [
    "发果山", "阿卢山", "吉输山", "恩容山", "鍞北门山", "英武山",
    "罗德山", "高来山", "卜龙山", "阿欲部山", "盘江山", "曲部山",
    "万年龙山", "小维摩山", "阿母山", "宝宁山", "接角山", "大维摩山",
    "龙定山", "巴盘江", "巴甸江", "矣邦池", "八甸溪", "山湖",
]

ents_126 = [
    {"ent_id": "ENT-001", "name": "广西府", "type": "geo", "norm": "广西府", "first_source": I126},
    {"ent_id": "ENT-S01", "name": "师宗州", "type": "geo", "norm": "师宗州", "first_source": I126},
    {"ent_id": "ENT-S02", "name": "弥勒州", "type": "geo", "norm": "弥勒州", "first_source": I126},
    {"ent_id": "ENT-S03", "name": "维摩州", "type": "geo", "norm": "维摩州", "first_source": I126},
]
for nm in mtn_names_126:
    ents_126.append({"ent_id": f"ENT-K{nm}", "name": nm, "type": "mtn", "norm": nm, "first_source": I126})

geos_126 = [
    {
        "geo_id": "GEO-126001",
        "item_id": I126,
        "name": "广西府",
        "type": "prefecture",
        "region": "云南",
        "parent": "GEO-000",
        "children": ["GEO-126001-s01", "GEO-126001-s02", "GEO-126001-s03"],
        "volume_range": "卷126",
        "attributes": {
            "borders": [
                {"direction": "东", "to_place": "广南府界", "distance_li": 450},
                {"direction": "南", "to_place": "临安府阿弥州界", "distance_li": 160},
                {"direction": "西", "to_place": "临安府宁州界", "distance_li": 180},
                {"direction": "北", "to_place": "曲靖府罗雄州界", "distance_li": 50},
            ],
            "to_capital": [
                {"capital": "南京", "distance_li": 7520},
                {"capital": "京师", "distance_li": 10965},
            ],
            "households": {"count": None, "unit": "里", "note": "领州三：师宗州编户一十六里、弥勒州编户一十六里、维摩州编户五里"},
            "grain_tax": {"amount": 2170, "unit": "石", "note": "粮二千一百七十石零"},
            "jun_name": "",
            "topography": "山谷幽阻【云南志】；东瞰广西南距交趾【旧志】",
            "customs": "质野富强【云南志生蛮四种曰黑爨曰僰曰土獠曰白子其俗质野民强家富】",
            "garrisons": [],
        },
        "cit_ids": ["CIT-001", "CIT-002"],
    },
    {
        "geo_id": "GEO-126001-s01",
        "item_id": I126, "name": "师宗州", "type": "department", "region": "云南",
        "parent": "GEO-126001", "children": [], "volume_range": "卷126",
        "attributes": {"location_text": "在府城北八十里", "households": {"count": 16, "unit": "里", "note": "编户一十六里"}},
    },
    {
        "geo_id": "GEO-126001-s02",
        "item_id": I126, "name": "弥勒州", "type": "department", "region": "云南",
        "parent": "GEO-126001", "children": [], "volume_range": "卷126",
        "attributes": {"location_text": "在府城西九十里", "households": {"count": 16, "unit": "里", "note": "编户一十六里"}},
    },
    {
        "geo_id": "GEO-126001-s03",
        "item_id": I126, "name": "维摩州", "type": "department", "region": "云南",
        "parent": "GEO-126001", "children": [], "volume_range": "卷126",
        "attributes": {"location_text": "在府城东南三百六十里", "households": {"count": 5, "unit": "里", "note": "编户五里"}},
    },
]

evos_126 = [
    {"evo_id": "EVO-001", "item_id": I126, "geo_id": "GEO-126001", "dynasty": "汉", "era": None, "institution_name": "益州牂牁郡地", "action": "因之", "detail": "禹贡梁州之界，古滇国东南境，汉为益州牂牁郡地"},
    {"evo_id": "EVO-002", "item_id": I126, "geo_id": "GEO-126001", "dynasty": "蜀汉", "era": None, "institution_name": "兴古郡", "action": "因之", "detail": "蜀汉属兴古郡"},
    {"evo_id": "EVO-003", "item_id": I126, "geo_id": "GEO-126001", "dynasty": "晋", "era": None, "institution_name": "宁州", "action": "因之", "detail": "晋郡属宁州"},
    {"evo_id": "EVO-004", "item_id": I126, "geo_id": "GEO-126001", "dynasty": "隋", "era": None, "institution_name": "牂州", "action": "因之", "detail": "隋属牂州"},
    {"evo_id": "EVO-005", "item_id": I126, "geo_id": "GEO-126001", "dynasty": "唐", "era": "大和", "institution_name": "羁縻州/南诏地", "action": "因之", "detail": "唐时东爨乌蛮等部所居，为羁縻州，隶黔州都督府；大和间南诏蒙氏并其地"},
    {"evo_id": "EVO-006", "item_id": I126, "geo_id": "GEO-126001", "dynasty": "宋", "era": None, "institution_name": "师宗弥勒二部", "action": "因之", "detail": "宋时析为师宗弥勒二部，大理段氏莫能制"},
    {"evo_id": "EVO-007", "item_id": I126, "geo_id": "GEO-126001", "dynasty": "元", "era": "宪宗/至元", "institution_name": "广西路", "action": "置", "detail": "元宪宗时内附，隶落蒙万户府；至元中置广西路，属临安广西元江等处宣慰司"},
    {"evo_id": "EVO-008", "item_id": I126, "geo_id": "GEO-126001", "dynasty": "明", "era": None, "institution_name": "广西府", "action": "改", "detail": "本朝改为广西府，领州三"},
]

mtns_126 = [
    {"mtn_id": "MTN-001", "item_id": I126, "geo_id": "GEO-126001", "name": "发果山", "type": "山", "location_text": "在府治北", "description": "培塿相接，环于府治", "lore": ""},
    {"mtn_id": "MTN-002", "item_id": I126, "geo_id": "GEO-126001", "name": "阿卢山", "type": "山", "location_text": "在府城西三里", "description": "延亘四十余里，南接弥勒州，北跨师宗州，旧有阿卢部", "lore": ""},
    {"mtn_id": "MTN-003", "item_id": I126, "geo_id": "GEO-126001", "name": "吉输山", "type": "山", "location_text": "在府城东南五里", "description": "", "lore": ""},
    {"mtn_id": "MTN-004", "item_id": I126, "geo_id": "GEO-126001-s01", "name": "恩容山", "type": "山", "location_text": "在师宗州之五里", "description": "三峰峭拔", "lore": ""},
    {"mtn_id": "MTN-005", "item_id": I126, "geo_id": "GEO-126001-s01", "name": "鍞北门山", "type": "山", "location_text": "在师宗州北一十二里", "description": "二峰高耸，经行其间如门", "lore": ""},
    {"mtn_id": "MTN-006", "item_id": I126, "geo_id": "GEO-126001-s01", "name": "英武山", "type": "山", "location_text": "在师宗州东八十里", "description": "峰峦峭拔，高可千仞", "lore": ""},
    {"mtn_id": "MTN-007", "item_id": I126, "geo_id": "GEO-126001-s01", "name": "罗德山", "type": "山", "location_text": "在师宗州东一百二十里", "description": "一峰尖秀", "lore": ""},
    {"mtn_id": "MTN-008", "item_id": I126, "geo_id": "GEO-126001-s01", "name": "高来山", "type": "山", "location_text": "在师宗州东三百里", "description": "高三百尺，其西南三十里有马者笼山，高如之", "lore": ""},
    {"mtn_id": "MTN-009", "item_id": I126, "geo_id": "GEO-126001-s02", "name": "卜龙山", "type": "山", "location_text": "在弥勒州南五里", "description": "峰峦重叠，环于州治", "lore": ""},
    {"mtn_id": "MTN-010", "item_id": I126, "geo_id": "GEO-126001-s02", "name": "阿欲部山", "type": "山", "location_text": "在弥勒州西一十里", "description": "冈峦森列，下有温泉，盘亘七十余里，东接北倾山", "lore": ""},
    {"mtn_id": "MTN-011", "item_id": I126, "geo_id": "GEO-126001-s02", "name": "盘江山", "type": "山", "location_text": "在弥勒州东南一百二里", "description": "东西两山相峙，盘江流其中，东抵师宗州南界阿迷州；其东有石窍深广丈余，浊水涌出，入盘江", "lore": ""},
    {"mtn_id": "MTN-012", "item_id": I126, "geo_id": "GEO-126001-s03", "name": "曲部山", "type": "山", "location_text": "在维摩州治西", "description": "中峰高耸，下有泉为溪，流经州南数里入石窍", "lore": ""},
    {"mtn_id": "MTN-013", "item_id": I126, "geo_id": "GEO-126001-s03", "name": "万年龙山", "type": "山", "location_text": "在维摩州东北一百里", "description": "下有泉成溪，流入广南府界", "lore": ""},
    {"mtn_id": "MTN-014", "item_id": I126, "geo_id": "GEO-126001-s03", "name": "小维摩山", "type": "山", "location_text": "在维摩州东北八十里", "description": "高可千仞", "lore": ""},
    {"mtn_id": "MTN-015", "item_id": I126, "geo_id": "GEO-126001-s03", "name": "阿母山", "type": "山", "location_text": "在维摩州东南九十里", "description": "高余千仞", "lore": ""},
    {"mtn_id": "MTN-016", "item_id": I126, "geo_id": "GEO-126001-s03", "name": "宝宁山", "type": "山", "location_text": "在维摩州东北一百里", "description": "下有泉为宝宁溪", "lore": ""},
    {"mtn_id": "MTN-017", "item_id": I126, "geo_id": "GEO-126001-s03", "name": "接角山", "type": "山", "location_text": "在维摩州东南一百五十里", "description": "下有溪，亦名接角", "lore": ""},
    {"mtn_id": "MTN-018", "item_id": I126, "geo_id": "GEO-126001-s03", "name": "大维摩山", "type": "山", "location_text": "在维摩州东南二百里", "description": "高出众山，土官世居其上", "lore": ""},
    {"mtn_id": "MTN-019", "item_id": I126, "geo_id": "GEO-126001-s03", "name": "龙定山", "type": "山", "location_text": "在维摩州东南二百一十里", "description": "五峰屹然高耸", "lore": ""},
    {"mtn_id": "MTN-020", "item_id": I126, "geo_id": "GEO-126001", "name": "巴盘江", "type": "江", "location_text": "一名潘江", "description": "自澂江府入境，东南流经师宗州及府之西境，西南至弥勒州东，注普安州界", "lore": ""},
    {"mtn_id": "MTN-021", "item_id": I126, "geo_id": "GEO-126001-s02", "name": "巴甸江", "type": "江", "location_text": "源出弥勒州治西北", "description": "南流数里而东，入盘江", "lore": ""},
    {"mtn_id": "MTN-022", "item_id": I126, "geo_id": "GEO-126001", "name": "矣邦池", "type": "池", "location_text": "在府治南", "description": "周三十余里，半跨弥勒州界；水源有二，一出阿卢山麓石窍，一出弥勒州吉双乡，南流入盘江，中有小山，建广福寺", "lore": ""},
    {"mtn_id": "MTN-023", "item_id": I126, "geo_id": "GEO-126001-s02", "name": "八甸溪", "type": "溪", "location_text": "在弥勒州治北", "description": "其源有三，一出阿欲山，一出旧村，一出北倾山，至州治东合流，南入盘江", "lore": ""},
    {"mtn_id": "MTN-024", "item_id": I126, "geo_id": "GEO-126001-s02", "name": "山湖", "type": "湖", "location_text": "在弥勒州境内", "description": "产大鱼", "lore": ""},
]

prods_126 = [
    {"prod_id": "PROD-001", "item_id": I126, "name": "毡", "category": "土产", "note": ""},
    {"prod_id": "PROD-002", "item_id": I126, "name": "茶", "category": "土产", "note": ""},
    {"prod_id": "PROD-003", "item_id": I126, "name": "鸡腿竹", "category": "土产", "note": "每节上大下小如鸡腿状"},
    {"prod_id": "PROD-004", "item_id": I126, "name": "蜡", "category": "土产", "note": ""},
    {"prod_id": "PROD-005", "item_id": I126, "name": "白面猿", "category": "土产", "note": ""},
    {"prod_id": "PROD-006", "item_id": I126, "name": "麻布", "category": "土产", "note": ""},
]

cits_126 = [
    {"cit_id": "CIT-001", "item_id": I126, "cited_work": "云南志", "cited_work_ent_id": None, "context": "形胜/风俗", "original": "【云南志山谷幽阻】"},
    {"cit_id": "CIT-002", "item_id": I126, "cited_work": "旧志", "cited_work_ent_id": None, "context": "形胜", "original": "【旧志东瞰广西南距交趾】"},
]

main_126 = {
    "item_id": I126, "volume": V126, "source": "广西府", "region": "云南",
    "layers": {
        "ents": ents_126, "geos": geos_126, "evos": evos_126,
        "mtns": mtns_126, "pers": [], "sites": [],
        "prods": prods_126, "cits": cits_126,
    },
    "layer_count": 7,
    "validation": {"errs": [], "gap": 0, "notes": "领州三s01/s02/s03占位；sites拆至sites1/2；prods土产六条"},
    "title": "广西府",
}

sites1_126 = {
    "item_id": I126, "volume": V126, "source": "广西府", "region": "云南",
    "layers": {
        "ents": [], "geos": [], "evos": [], "mtns": [], "pers": [],
        "sites": [
            {"site_id": "SITE-001", "item_id": I126, "geo_id": "GEO-126001-s02", "name": "广福寺", "type": "寺观", "location_text": "在弥勒州东九十里", "history_lore": "", "original": "广福寺【在弥勒州东九十里】"},
            {"site_id": "SITE-002", "item_id": I126, "geo_id": "GEO-126001-s01", "name": "观音庵", "type": "寺观", "location_text": "在师宗州治东", "history_lore": "", "original": "观音庵【在师宗州治东】"},
        ],
        "prods": [], "cits": [],
    },
    "layer_count": 7, "title": "广西府",
}

sites2_126 = {
    "item_id": I126, "volume": V126, "source": "广西府", "region": "云南",
    "layers": {
        "ents": [], "geos": [], "evos": [], "mtns": [], "pers": [],
        "sites": [
            {"site_id": "SITE-001", "item_id": I126, "geo_id": "GEO-126001-s02", "name": "玉津桥", "type": "关梁", "location_text": "在弥勒州治南跨八甸溪", "history_lore": "", "original": "玉津桥【在弥勒州治南跨八甸溪】"},
            {"site_id": "SITE-002", "item_id": I126, "geo_id": "GEO-126001", "name": "广西府学", "type": "学校", "location_text": "在府治东", "history_lore": "本朝建", "original": "广西府学【在府治本朝建】"},
        ],
        "prods": [], "cits": [],
    },
    "layer_count": 7, "title": "广西府",
}

# ============================================================
# Write all files
# ============================================================
os.makedirs(os.path.join(DATA, "vol124"), exist_ok=True)
os.makedirs(os.path.join(DATA, "vol125"), exist_ok=True)
os.makedirs(os.path.join(DATA, "vol126"), exist_ok=True)

dump(main_124, os.path.join(DATA, "vol124", "124-001_景东府.json"))
dump(sites1_124, os.path.join(DATA, "vol124", "124-001_sites1_寺观.json"))
dump(sites2_124, os.path.join(DATA, "vol124", "124-001_sites2_关梁学校.json"))
dump(w01_124, os.path.join(DATA, "vol124", "124-001_w01_景东卫.json"))

dump(main_125, os.path.join(DATA, "vol125", "125-001_广南府.json"))
dump(s01_125, os.path.join(DATA, "vol125", "125-001_s01_富州.json"))

dump(main_126, os.path.join(DATA, "vol126", "126-001_广西府.json"))
dump({"item_id": I126, "volume": V126, "source": "师宗州", "region": "云南",
      "layers": {"ents": [{"ent_id": "ENT-S01", "name": "师宗州", "type": "geo", "norm": "师宗州", "first_source": I126}],
                 "geos": [], "evos": [], "mtns": [], "pers": [], "sites": [], "prods": [], "cits": []},
      "layer_count": 7, "title": "广西府"},
     os.path.join(DATA, "vol126", "126-001_s01_师宗州.json"))
dump({"item_id": I126, "volume": V126, "source": "弥勒州", "region": "云南",
      "layers": {"ents": [{"ent_id": "ENT-S02", "name": "弥勒州", "type": "geo", "norm": "弥勒州", "first_source": I126}],
                 "geos": [], "evos": [], "mtns": [], "pers": [], "sites": [], "prods": [], "cits": []},
      "layer_count": 7, "title": "广西府"},
     os.path.join(DATA, "vol126", "126-001_s02_弥勒州.json"))
dump({"item_id": I126, "volume": V126, "source": "维摩州", "region": "云南",
      "layers": {"ents": [{"ent_id": "ENT-S03", "name": "维摩州", "type": "geo", "norm": "维摩州", "first_source": I126}],
                 "geos": [], "evos": [], "mtns": [], "pers": [], "sites": [], "prods": [], "cits": []},
      "layer_count": 7, "title": "广西府"},
     os.path.join(DATA, "vol126", "126-001_s03_维摩州.json"))
dump(sites1_126, os.path.join(DATA, "vol126", "126-001_sites1_寺观.json"))
dump(sites2_126, os.path.join(DATA, "vol126", "126-001_sites2_关梁学校.json"))

print("Done.")
print(f"vol124 files: 4 (main + sites1 + sites2 + w01)")
print(f"vol125 files: 2 (main + s01)")
print(f"vol126 files: 6 (main + s01 + s02 + s03 + sites1 + sites2)")
print(f"vol124 GEO nodes: {len(geos_124)}, mtns: {len(mtns_124)}")
print(f"vol125 GEO nodes: {len(geos_125)}, mtns: {len(mtns_125)}")
print(f"vol126 GEO nodes: {len(geos_126)}, mtns: {len(mtns_126)}")
