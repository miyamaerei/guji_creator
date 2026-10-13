# -*- coding: utf-8 -*-
"""卷05 分片2b生成器：05-105 ~ 05-181。校验后输出 data_part2b.py。"""

import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
reg = json.load(io.open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))


def N(iid, s):
    norm = reg[iid]["norm"]
    if s not in norm:
        raise SystemExit("[%s] 未命中 norm: %r" % (iid, s))
    return s


D = {}


def item(iid, geo=None, ents=None, tme=None, evo=None, hyd=None, gar=None, res=None):
    D[iid] = {
        "geo": geo,
        "ents": ents or [],
        "tme": tme or [],
        "evo": evo or [],
        "hyd": hyd or [],
        "gar": gar or [],
        "res": res or [],
    }


# ---------- 桂阳州（属衡州府） ----------
item(
    "05-105",
    geo={
        "name": N("05-105", "桂阳州"),
        "level": "属州",
        "node_type": "政区",
        "parent": {"text": "衡州府", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "西北",
                "to_anchor": "衡州府",
                "distance": 300,
                "unit": "里",
                "raw": N("05-105", "西北距府三百里"),
            }
        ],
        "note": "元桂阳路，治平阳县，属湖南道宣慰司。洪武元年为府。九年四月降为县，省平阳县入焉。十三年五月升为州。领县三",
    },
    ents=[
        {
            "text": N("05-105", "桂阳州"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-105", "平阳县"),
            "type": "place",
            "count": 1,
            "provenance": "元桂阳路，治平阳县",
        },
        {
            "text": N("05-105", "大凑山"),
            "type": "place",
            "count": 1,
            "provenance": "西有大凑山",
        },
        {
            "text": N("05-105", "潭流岭"),
            "type": "place",
            "count": 1,
            "provenance": "北有潭流岭",
        },
        {
            "text": N("05-105", "舂陵水"),
            "type": "water",
            "count": 1,
            "provenance": "西北有舂陵水",
        },
        {
            "text": N("05-105", "岿水"),
            "type": "water",
            "count": 1,
            "provenance": "又西有岿水流合焉",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 1,
            "era_raw": N("05-105", "洪武元年"),
            "category": "升秩",
            "event": N("05-105", "为府"),
            "place": "桂阳州",
        },
        {
            "reign": "洪武",
            "year": 9,
            "era_raw": N("05-105", "九年四月"),
            "category": "降秩",
            "event": N("05-105", "降为县，省平阳县入焉"),
            "place": "桂阳州",
        },
        {
            "reign": "洪武",
            "year": 13,
            "era_raw": N("05-105", "十三年五月"),
            "category": "升秩",
            "event": N("05-105", "升为州"),
            "place": "桂阳州",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-105", "元桂阳路，治平阳县，属湖南道宣慰司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-105", "元桂阳路，治平阳县，属湖南道宣慰司"),
            "owner": "湖南道宣慰司",
        },
        {
            "phase": 2,
            "era_raw": N("05-105", "洪武元年"),
            "reign": "洪武",
            "year": 1,
            "change_type": "改置",
            "change": N("05-105", "为府"),
            "owner": "湖南道宣慰司",
        },
        {
            "phase": 3,
            "era_raw": N("05-105", "九年四月"),
            "reign": "洪武",
            "year": 9,
            "change_type": "降县",
            "change": N("05-105", "降为县，省平阳县入焉"),
            "owner": "衡州府",
        },
        {
            "phase": 4,
            "era_raw": N("05-105", "十三年五月"),
            "reign": "洪武",
            "year": 13,
            "change_type": "升州",
            "change": N("05-105", "升为州"),
            "owner": "衡州府",
        },
    ],
    hyd=[
        {
            "name": N("05-105", "舂陵水"),
            "type": "江",
            "flow": N("05-105", "西北有舂陵水"),
            "anchor": {"anchor": "桂阳州西北", "context": N("05-105", "西北有舂陵水")},
        },
        {
            "name": N("05-105", "岿水"),
            "type": "江",
            "flow": N("05-105", "又西有岿水流合焉"),
            "anchor": {
                "anchor": "桂阳州西",
                "context": N("05-105", "又西有岿水流合焉"),
            },
        },
    ],
    res=[
        {
            "name": N("05-105", "潭流岭"),
            "type": "银",
            "place": "桂阳州",
            "site": "潭流岭",
            "importance": "旧产银铅砂矿",
            "raw": N("05-105", "旧皆产银铅砂矿"),
        },
        {
            "name": N("05-105", "潭流岭"),
            "type": "铅",
            "place": "桂阳州",
            "site": "潭流岭",
            "importance": "旧产银铅砂矿",
            "raw": N("05-105", "旧皆产银铅砂矿"),
        },
    ],
    gar=[
        {
            "name": N("05-105", "泗州寨"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "桂阳州北",
            "dusi": "未明",
            "note": "北有泗州寨、南有牛桥镇二巡检司",
        },
        {
            "name": N("05-105", "牛桥镇"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "桂阳州南",
            "dusi": "未明",
            "note": "北有泗州寨、南有牛桥镇二巡检司",
        },
    ],
)

item(
    "05-106",
    geo={
        "name": N("05-106", "临武"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "桂阳州", "rel": "领"},
        "note": "州南。西北有舜峰山。西有西山，武水出焉，经宜章县合于章水。东北有两路口巡检司。又东有赤土巡检，后废",
    },
    ents=[
        {
            "text": N("05-106", "临武"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-106", "舜峰山"),
            "type": "place",
            "count": 1,
            "provenance": "西北有舜峰山",
        },
        {
            "text": N("05-106", "武水"),
            "type": "water",
            "count": 2,
            "provenance": "西有西山，武水出焉",
        },
        {
            "text": N("05-106", "章水"),
            "type": "water",
            "count": 1,
            "provenance": "经宜章县合于章水",
        },
        {
            "text": N("05-106", "两路口巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "东北有两路口巡检司",
        },
    ],
    hyd=[
        {
            "name": N("05-106", "武水"),
            "type": "江",
            "flow": N("05-106", "西有西山，武水出焉，经宜章县合于章水"),
            "anchor": {"anchor": "临武县西", "context": N("05-106", "武水出焉")},
        },
    ],
    gar=[
        {
            "name": N("05-106", "两路口巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "临武县东北",
            "dusi": "未明",
            "note": "东北有两路口巡检司",
        },
        {
            "name": N("05-106", "赤土巡检"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "临武县东",
            "dusi": "未明",
            "note": "又东有赤土巡检，后废",
        },
    ],
)

item(
    "05-107",
    geo={
        "name": N("05-107", "蓝山"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "桂阳州", "rel": "领"},
        "note": "州西南。旧治在县北，洪武元年徙于此，属郴州。二年来属。南有黄檗山。西南有九疑山。西有守御宁溪千户所，洪武二十九年三月置",
    },
    ents=[
        {
            "text": N("05-107", "蓝山"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-107", "黄檗山"),
            "type": "place",
            "count": 1,
            "provenance": "南有黄檗山",
        },
        {
            "text": N("05-107", "九疑山"),
            "type": "place",
            "count": 1,
            "provenance": "西南有九疑山",
        },
        {
            "text": N("05-107", "岿水"),
            "type": "water",
            "count": 1,
            "provenance": "岿水出焉，亦名舜水",
        },
        {
            "text": N("05-107", "守御宁溪千户所"),
            "type": "institution",
            "count": 1,
            "provenance": "又西有守御宁溪千户所",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 1,
            "era_raw": N("05-107", "洪武元年"),
            "category": "徙治",
            "event": N("05-107", "旧治在县北，洪武元年徙于此"),
            "place": "蓝山",
        },
        {
            "reign": "洪武",
            "year": 2,
            "era_raw": N("05-107", "二年"),
            "category": "改隶",
            "event": N("05-107", "来属"),
            "place": "蓝山",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-107", "旧治在县北"),
            "reign": "洪武",
            "year": 0,
            "change_type": "初置",
            "change": N("05-107", "旧治在县北"),
            "owner": "郴州",
        },
        {
            "phase": 2,
            "era_raw": N("05-107", "洪武元年"),
            "reign": "洪武",
            "year": 1,
            "change_type": "徙治",
            "change": N("05-107", "洪武元年徙于此，属郴州"),
            "owner": "郴州",
        },
        {
            "phase": 3,
            "era_raw": N("05-107", "二年"),
            "reign": "洪武",
            "year": 2,
            "change_type": "改隶",
            "change": N("05-107", "二年来属"),
            "owner": "桂阳州",
        },
    ],
    hyd=[
        {
            "name": N("05-107", "岿水"),
            "alt": "舜水",
            "type": "江",
            "flow": N("05-107", "岿水出焉，亦名舜水，北流合舂陵水"),
            "anchor": {"anchor": "蓝山县西南", "context": N("05-107", "岿水出焉")},
        },
    ],
    gar=[
        {
            "name": N("05-107", "守御宁溪千户所"),
            "type": "守御千户所",
            "territorial": "未明",
            "established": {
                "reign": "洪武",
                "year": 29,
                "era_raw": N("05-107", "洪武二十九年三月"),
            },
            "place": "蓝山县西",
            "dusi": "未明",
            "note": "又西有守御宁溪千户所，洪武二十九年三月置",
        },
        {
            "name": N("05-107", "毛俊镇"),
            "type": "镇",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "蓝山县东",
            "dusi": "未明",
            "note": "东有毛俊镇、北有乾溪镇、西南有大桥镇三巡检司",
        },
        {
            "name": N("05-107", "乾溪镇"),
            "type": "镇",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "蓝山县北",
            "dusi": "未明",
            "note": "东有毛俊镇、北有乾溪镇、西南有大桥镇三巡检司",
        },
        {
            "name": N("05-107", "大桥镇"),
            "type": "镇",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "蓝山县西南",
            "dusi": "未明",
            "note": "东有毛俊镇、北有乾溪镇、西南有大桥镇三巡检司",
        },
        {
            "name": N("05-107", "小山堡"),
            "type": "堡",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "蓝山县西",
            "dusi": "未明",
            "note": "又西有小山堡、张家陂二巡检司，后废",
        },
        {
            "name": N("05-107", "张家陂"),
            "type": "堡",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "蓝山县西",
            "dusi": "未明",
            "note": "又西有小山堡、张家陂二巡检司，后废",
        },
    ],
)

item(
    "05-108",
    geo={
        "name": N("05-108", "嘉禾"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "桂阳州", "rel": "领"},
        "note": "州西南。崇祯十二年以桂阳州之仓禾堡置，析临武县地益之。东南有岿水",
    },
    ents=[
        {
            "text": N("05-108", "嘉禾"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-108", "仓禾堡"),
            "type": "place",
            "count": 1,
            "provenance": "以桂阳州之仓禾堡置",
        },
        {
            "text": N("05-108", "岿水"),
            "type": "water",
            "count": 1,
            "provenance": "东南有岿水",
        },
    ],
    tme=[
        {
            "reign": "崇祯",
            "year": 12,
            "era_raw": N("05-108", "崇祯十二年"),
            "category": "析置",
            "event": N("05-108", "以桂阳州之仓禾堡置，析临武县地益之"),
            "place": "嘉禾",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-108", "崇祯十二年"),
            "reign": "崇祯",
            "year": 12,
            "change_type": "析置",
            "change": N("05-108", "以桂阳州之仓禾堡置，析临武县地益之"),
            "owner": "桂阳州",
        },
    ],
    hyd=[
        {
            "name": N("05-108", "岿水"),
            "type": "江",
            "flow": N("05-108", "东南有岿水，自蓝山县流入，北经石门山，又东北入州界"),
            "anchor": {"anchor": "嘉禾县东南", "context": N("05-108", "东南有岿水")},
        },
    ],
)

# ---------- 永州府 ----------
item(
    "05-109",
    geo={
        "name": N("05-109", "永州府"),
        "level": "府",
        "node_type": "政区",
        "parent": {"text": "湖广", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "东北",
                "to_anchor": "布政司",
                "distance": 1820,
                "unit": "里",
                "raw": N("05-109", "东北距布政司千八百二十里"),
            }
        ],
        "note": "元永州路，属湖南道宣慰司。洪武元年为府。领州一，县七",
    },
    ents=[
        {
            "text": N("05-109", "永州府"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-109", "永州路"),
            "type": "place",
            "count": 1,
            "provenance": "元永州路",
        },
        {
            "text": N("05-109", "湖南道宣慰司"),
            "type": "institution",
            "count": 1,
            "provenance": "属湖南道宣慰司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 1,
            "era_raw": N("05-109", "洪武元年"),
            "category": "初置",
            "event": N("05-109", "为府"),
            "place": "永州府",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-109", "元永州路，属湖南道宣慰司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-109", "元永州路，属湖南道宣慰司"),
            "owner": "湖南道宣慰司",
        },
        {
            "phase": 2,
            "era_raw": N("05-109", "洪武元年"),
            "reign": "洪武",
            "year": 1,
            "change_type": "改置",
            "change": N("05-109", "为府"),
            "owner": "湖南道宣慰司",
        },
    ],
)

item(
    "05-110",
    geo={
        "name": N("05-110", "零陵"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "永州府", "rel": "领"},
        "note": "倚。北有湘水，经城西，潇水自南来合焉，谓之湘口，有湘口关。又南有永水。北有黄杨堡巡检司，本高溪市，隆庆元年徙治，更名",
    },
    ents=[
        {
            "text": N("05-110", "零陵"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-110", "湘水"),
            "type": "water",
            "count": 1,
            "provenance": "北有湘水，经城西",
        },
        {
            "text": N("05-110", "潇水"),
            "type": "water",
            "count": 1,
            "provenance": "潇水自南来合焉",
        },
        {
            "text": N("05-110", "永水"),
            "type": "water",
            "count": 1,
            "provenance": "又南有永水",
        },
        {
            "text": N("05-110", "湘口关"),
            "type": "institution",
            "count": 1,
            "provenance": "有湘口关",
        },
        {
            "text": N("05-110", "黄杨堡巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "北有黄杨堡巡检司",
        },
    ],
    tme=[
        {
            "reign": "隆庆",
            "year": 1,
            "era_raw": N("05-110", "隆庆元年"),
            "category": "改称",
            "event": N("05-110", "徙治，更名"),
            "place": "零陵",
        },
    ],
    hyd=[
        {
            "name": N("05-110", "湘水"),
            "type": "江",
            "flow": N("05-110", "北有湘水，经城西，潇水自南来合焉，谓之湘口"),
            "anchor": {
                "anchor": "零陵县城西",
                "context": N("05-110", "北有湘水，经城西"),
            },
        },
        {
            "name": N("05-110", "潇水"),
            "type": "江",
            "flow": N("05-110", "潇水自南来合焉，谓之湘口"),
            "anchor": {"anchor": "零陵县南", "context": N("05-110", "潇水自南来合焉")},
        },
        {
            "name": N("05-110", "永水"),
            "type": "溪",
            "flow": N("05-110", "又南有永水，源出县西南之永山，北流入于湘水"),
            "anchor": {"anchor": "零陵县南", "context": N("05-110", "又南有永水")},
        },
    ],
    gar=[
        {
            "name": N("05-110", "湘口关"),
            "type": "关",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "零陵县湘口",
            "dusi": "未明",
            "note": "谓之湘口，有湘口关",
        },
        {
            "name": N("05-110", "黄杨堡巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "零陵县北",
            "dusi": "未明",
            "note": "北有黄杨堡巡检司，本高溪市，隆庆元年徙治，更名",
        },
    ],
)

item(
    "05-111",
    geo={
        "name": N("05-111", "祁阳"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "永州府", "rel": "领"},
        "note": "府东北。旧治在县西，景泰元年十二月徙于今治。北有祁山，上有黄罴镇。西北有四望山。西有湘水。又城北有祁水。南有浯溪",
    },
    ents=[
        {
            "text": N("05-111", "祁阳"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-111", "祁山"),
            "type": "place",
            "count": 1,
            "provenance": "北有祁山",
        },
        {
            "text": N("05-111", "四望山"),
            "type": "place",
            "count": 1,
            "provenance": "西北有四望山",
        },
        {
            "text": N("05-111", "湘水"),
            "type": "water",
            "count": 1,
            "provenance": "西有湘水",
        },
        {
            "text": N("05-111", "祁水"),
            "type": "water",
            "count": 1,
            "provenance": "又城北有祁水",
        },
        {
            "text": N("05-111", "浯溪"),
            "type": "water",
            "count": 1,
            "provenance": "南有浯溪",
        },
    ],
    tme=[
        {
            "reign": "景泰",
            "year": 1,
            "era_raw": N("05-111", "景泰元年十二月"),
            "category": "徙治",
            "event": N("05-111", "旧治在县西，景泰元年十二月徙于今治"),
            "place": "祁阳",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-111", "旧治在县西"),
            "reign": "未明",
            "year": 0,
            "change_type": "初置",
            "change": N("05-111", "旧治在县西"),
            "owner": "永州府",
        },
        {
            "phase": 2,
            "era_raw": N("05-111", "景泰元年十二月"),
            "reign": "景泰",
            "year": 1,
            "change_type": "徙治",
            "change": N("05-111", "徙于今治"),
            "owner": "永州府",
        },
    ],
    hyd=[
        {
            "name": N("05-111", "湘水"),
            "type": "江",
            "flow": N("05-111", "西有湘水"),
            "anchor": {"anchor": "祁阳县西", "context": N("05-111", "西有湘水")},
        },
        {
            "name": N("05-111", "祁水"),
            "type": "江",
            "flow": N("05-111", "又城北有祁水，源出邵阳县，东北流入焉"),
            "anchor": {"anchor": "祁阳县城北", "context": N("05-111", "又城北有祁水")},
        },
        {
            "name": N("05-111", "浯溪"),
            "type": "溪",
            "flow": N("05-111", "南有浯溪，下流亦入湘水"),
            "anchor": {"anchor": "祁阳县南", "context": N("05-111", "南有浯溪")},
        },
    ],
    gar=[
        {
            "name": N("05-111", "黄罴镇"),
            "type": "镇",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "祁阳县北祁山",
            "dusi": "未明",
            "note": "北有祁山，上有黄罴镇",
        },
        {
            "name": N("05-111", "归阳市"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "祁阳县东",
            "dusi": "未明",
            "note": "又东有归阳市、东南有白水市、西北有水隆太平市三巡检司",
        },
        {
            "name": N("05-111", "白水市"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "祁阳县东南",
            "dusi": "未明",
            "note": "又东有归阳市、东南有白水市、西北有水隆太平市三巡检司",
        },
        {
            "name": N("05-111", "水隆太平市"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "祁阳县西北",
            "dusi": "未明",
            "note": "又东有归阳市、东南有白水市、西北有水隆太平市三巡检司",
        },
        {
            "name": N("05-111", "湘江市巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "祁阳县东北",
            "dusi": "未明",
            "note": "又东北有湘江市巡检司，后移于县东北之排山",
        },
    ],
)

item(
    "05-112",
    geo={
        "name": N("05-112", "东安"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "永州府", "rel": "领"},
        "note": "府西北。八十四渡山在县东。又东南有湘水，自广西全州流入。又有卢洪江。有卢洪市巡检司。又有结陂市巡检司，后废",
    },
    ents=[
        {
            "text": N("05-112", "东安"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-112", "八十四渡山"),
            "type": "place",
            "count": 1,
            "provenance": "八十四渡山在县东",
        },
        {
            "text": N("05-112", "湘水"),
            "type": "water",
            "count": 1,
            "provenance": "又东南有湘水",
        },
        {
            "text": N("05-112", "卢洪江"),
            "type": "water",
            "count": 2,
            "provenance": "又有卢洪江",
        },
        {
            "text": N("05-112", "卢洪市巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "有卢洪市巡检司",
        },
    ],
    hyd=[
        {
            "name": N("05-112", "湘水"),
            "type": "江",
            "flow": N("05-112", "又东南有湘水，自广西全州流入"),
            "anchor": {"anchor": "东安县东南", "context": N("05-112", "又东南有湘水")},
        },
        {
            "name": N("05-112", "卢洪江"),
            "type": "江",
            "flow": N("05-112", "又有卢洪江，源出县北九龙岩，经城东，下流入湘水"),
            "anchor": {"anchor": "东安县城东", "context": N("05-112", "又有卢洪江")},
        },
    ],
    gar=[
        {
            "name": N("05-112", "卢洪市巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "东安县",
            "dusi": "未明",
            "note": "有卢洪市巡检司",
        },
        {
            "name": N("05-112", "结陂市巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "东安县",
            "dusi": "未明",
            "note": "又有结陂市巡检司，后废",
        },
    ],
)

item(
    "05-113",
    geo={
        "name": N("05-113", "道州"),
        "level": "属州",
        "node_type": "政区",
        "parent": {"text": "永州府", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "北",
                "to_anchor": "永州府",
                "distance": 150,
                "unit": "里",
                "raw": N("05-113", "北距府百五十里"),
            }
        ],
        "note": "元道州路，属湖南宣慰司。洪武元年为府。九年四月复降为州，以州治营道县省入，来属。领县四",
    },
    ents=[
        {
            "text": N("05-113", "道州"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-113", "道州路"),
            "type": "place",
            "count": 1,
            "provenance": "元道州路",
        },
        {
            "text": N("05-113", "营山"),
            "type": "place",
            "count": 1,
            "provenance": "西有营山",
        },
        {
            "text": N("05-113", "营水"),
            "type": "water",
            "count": 1,
            "provenance": "营水出焉",
        },
        {
            "text": N("05-113", "潇江"),
            "type": "water",
            "count": 1,
            "provenance": "东有潇江",
        },
        {
            "text": N("05-113", "濂溪"),
            "type": "water",
            "count": 1,
            "provenance": "又西有濂溪",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 1,
            "era_raw": N("05-113", "洪武元年"),
            "category": "升秩",
            "event": N("05-113", "为府"),
            "place": "道州",
        },
        {
            "reign": "洪武",
            "year": 9,
            "era_raw": N("05-113", "九年四月"),
            "category": "降秩",
            "event": N("05-113", "复降为州，以州治营道县省入"),
            "place": "道州",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-113", "元道州路，属湖南宣慰司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-113", "元道州路，属湖南宣慰司"),
            "owner": "湖南宣慰司",
        },
        {
            "phase": 2,
            "era_raw": N("05-113", "洪武元年"),
            "reign": "洪武",
            "year": 1,
            "change_type": "改置",
            "change": N("05-113", "为府"),
            "owner": "湖南宣慰司",
        },
        {
            "phase": 3,
            "era_raw": N("05-113", "九年四月"),
            "reign": "洪武",
            "year": 9,
            "change_type": "改置",
            "change": N("05-113", "复降为州，以州治营道县省入，来属"),
            "owner": "永州府",
        },
    ],
    hyd=[
        {
            "name": N("05-113", "营水"),
            "type": "江",
            "flow": N("05-113", "西有营山，营水出焉，至泥江，与江华县之沲水合"),
            "anchor": {"anchor": "道州西", "context": N("05-113", "营水出焉")},
        },
        {
            "name": N("05-113", "潇江"),
            "type": "江",
            "flow": N("05-113", "东有潇江，至青口，合于沲水"),
            "anchor": {"anchor": "道州东", "context": N("05-113", "东有潇江")},
        },
        {
            "name": N("05-113", "濂溪"),
            "type": "溪",
            "flow": N(
                "05-113",
                "又西有濂溪，源出州西安定山下，东北合宜水，谓之龙滩，下流俱入湘水",
            ),
            "anchor": {"anchor": "道州西", "context": N("05-113", "又西有濂溪")},
        },
    ],
)

item(
    "05-114",
    geo={
        "name": N("05-114", "宁远"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "道州", "rel": "领"},
        "note": "州东少北。南有九疑山。山有朱明峰，潇水出焉。又南有舜源水。南有九疑、鲁观巡检司",
    },
    ents=[
        {
            "text": N("05-114", "宁远"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-114", "九疑山"),
            "type": "place",
            "count": 2,
            "provenance": "南有九疑山，介衡、永、郴、道之间",
        },
        {
            "text": N("05-114", "潇水"),
            "type": "water",
            "count": 1,
            "provenance": "山有朱明峰，潇水出焉",
        },
        {
            "text": N("05-114", "舜源水"),
            "type": "water",
            "count": 1,
            "provenance": "又南有舜源水",
        },
    ],
    hyd=[
        {
            "name": N("05-114", "潇水"),
            "type": "江",
            "flow": N("05-114", "山有朱明峰，潇水出焉"),
            "anchor": {"anchor": "宁远县南九疑山", "context": N("05-114", "潇水出焉")},
        },
        {
            "name": N("05-114", "舜源水"),
            "type": "江",
            "flow": N("05-114", "又南有舜源水，北流与江华县沲、潇二水合为三江口"),
            "anchor": {"anchor": "宁远县南", "context": N("05-114", "又南有舜源水")},
        },
    ],
    gar=[
        {
            "name": N("05-114", "九疑、鲁观巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "宁远县南",
            "dusi": "未明",
            "note": "南有九疑、鲁观巡检司，在九疑、鲁观二峒口",
        },
    ],
)

item(
    "05-115",
    geo={
        "name": N("05-115", "江华"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "道州", "rel": "领"},
        "note": "州南。东南有故城。今治本宁远卫右千户所，洪武二十八年置。天顺六年徙县来同治。西有白芒岭，即萌渚岭。东有沲水。又东南有砅水",
    },
    ents=[
        {
            "text": N("05-115", "江华"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-115", "白芒岭"),
            "type": "place",
            "count": 1,
            "provenance": "西有白芒岭",
        },
        {
            "text": N("05-115", "萌渚岭"),
            "type": "place",
            "count": 1,
            "provenance": "即萌渚岭，五岭之第四岭也",
        },
        {
            "text": N("05-115", "沲水"),
            "type": "water",
            "count": 1,
            "provenance": "东有沲水",
        },
        {
            "text": N("05-115", "砅水"),
            "type": "water",
            "count": 1,
            "provenance": "又东南有砅水",
        },
        {
            "text": N("05-115", "守御锦田千户所"),
            "type": "institution",
            "count": 1,
            "provenance": "又东有守御锦田千户所",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 28,
            "era_raw": N("05-115", "洪武二十八年"),
            "category": "初置",
            "event": N("05-115", "今治本宁远卫右千户所，洪武二十八年置"),
            "place": "江华",
        },
        {
            "reign": "天顺",
            "year": 6,
            "era_raw": N("05-115", "天顺六年"),
            "category": "徙治",
            "event": N("05-115", "徙县来同治"),
            "place": "江华",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-115", "今治本宁远卫右千户所，洪武二十八年置"),
            "reign": "洪武",
            "year": 28,
            "change_type": "初置",
            "change": N("05-115", "今治本宁远卫右千户所，洪武二十八年置"),
            "owner": "道州",
        },
        {
            "phase": 2,
            "era_raw": N("05-115", "天顺六年"),
            "reign": "天顺",
            "year": 6,
            "change_type": "徙治",
            "change": N("05-115", "徙县来同治"),
            "owner": "道州",
        },
    ],
    hyd=[
        {
            "name": N("05-115", "沲水"),
            "type": "江",
            "flow": N("05-115", "东有沲水，源出九疑山之石城、娥皇二峰，下流合于潇水"),
            "anchor": {"anchor": "江华县东", "context": N("05-115", "东有沲水")},
        },
        {
            "name": N("05-115", "砅水"),
            "type": "江",
            "flow": N("05-115", "又东南有砅水，源出九疑山之女英峰，流合沲水"),
            "anchor": {"anchor": "江华县东南", "context": N("05-115", "又东南有砅水")},
        },
    ],
    gar=[
        {
            "name": N("05-115", "守御锦田千户所"),
            "type": "守御千户所",
            "territorial": "未明",
            "established": {
                "reign": "洪武",
                "year": 29,
                "era_raw": N("05-115", "洪武二十九年"),
            },
            "place": "江华县东",
            "dusi": "未明",
            "note": "又东有守御锦田千户所，洪武二十九年置",
        },
        {
            "name": N("05-115", "锦田巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "江华县东",
            "dusi": "未明",
            "note": "又有锦田巡检司",
        },
        {
            "name": N("05-115", "锦冈巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "江华县西南",
            "dusi": "未明",
            "note": "又西南有锦冈巡检司",
        },
        {
            "name": N("05-115", "涛墟市巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "江华县西南",
            "dusi": "未明",
            "note": "又有涛墟市巡检司，后移于宁远县之九疑、鲁观",
        },
    ],
)

item(
    "05-116",
    geo={
        "name": N("05-116", "永明"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "道州", "rel": "领"},
        "note": "州西少南。北有永明岭，即都庞岭，五岭之第三岭也。南有遨水。东南有枇杷守御千户所，西南有桃川守御千户所，俱洪武二十九年置",
    },
    ents=[
        {
            "text": N("05-116", "永明"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-116", "永明岭"),
            "type": "place",
            "count": 1,
            "provenance": "北有永明岭",
        },
        {
            "text": N("05-116", "都庞岭"),
            "type": "place",
            "count": 1,
            "provenance": "即都庞岭，五岭之第三岭也",
        },
        {
            "text": N("05-116", "遨水"),
            "type": "water",
            "count": 1,
            "provenance": "南有遨水",
        },
    ],
    hyd=[
        {
            "name": N("05-116", "遨水"),
            "type": "江",
            "flow": N("05-116", "南有遨水，自广西富川县流入，下流注于潇水"),
            "anchor": {"anchor": "永明县南", "context": N("05-116", "南有遨水")},
        },
    ],
    gar=[
        {
            "name": N("05-116", "枇杷守御千户所"),
            "type": "守御千户所",
            "territorial": "未明",
            "established": {
                "reign": "洪武",
                "year": 29,
                "era_raw": N("05-116", "洪武二十九年"),
            },
            "place": "永明县东南",
            "dusi": "未明",
            "note": "东南有枇杷守御千户所，西南有桃川守御千户所，俱洪武二十九年置",
        },
        {
            "name": N("05-116", "桃川守御千户所"),
            "type": "守御千户所",
            "territorial": "未明",
            "established": {
                "reign": "洪武",
                "year": 29,
                "era_raw": N("05-116", "洪武二十九年"),
            },
            "place": "永明县西南",
            "dusi": "未明",
            "note": "东南有枇杷守御千户所，西南有桃川守御千户所，俱洪武二十九年置",
        },
        {
            "name": N("05-116", "桃川市巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "永明县西南",
            "dusi": "未明",
            "note": "又有桃川市巡检司",
        },
        {
            "name": N("05-116", "白面墟巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "永明县西南",
            "dusi": "未明",
            "note": "又西南有白面墟巡检司",
        },
    ],
)

item(
    "05-117",
    geo={
        "name": N("05-117", "新田"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "道州", "rel": "领"},
        "note": "州东北。崇祯十二年以宁远县之新田堡置。西北有舂陵山，舂陵水出焉。东南有白面寨巡检司",
    },
    ents=[
        {
            "text": N("05-117", "新田"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-117", "新田堡"),
            "type": "place",
            "count": 1,
            "provenance": "以宁远县之新田堡置",
        },
        {
            "text": N("05-117", "舂陵山"),
            "type": "place",
            "count": 1,
            "provenance": "西北有舂陵山",
        },
        {
            "text": N("05-117", "舂陵水"),
            "type": "water",
            "count": 1,
            "provenance": "舂陵水出焉",
        },
    ],
    tme=[
        {
            "reign": "崇祯",
            "year": 12,
            "era_raw": N("05-117", "崇祯十二年"),
            "category": "析置",
            "event": N("05-117", "以宁远县之新田堡置"),
            "place": "新田",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-117", "崇祯十二年"),
            "reign": "崇祯",
            "year": 12,
            "change_type": "析置",
            "change": N("05-117", "以宁远县之新田堡置"),
            "owner": "道州",
        },
    ],
    hyd=[
        {
            "name": N("05-117", "舂陵水"),
            "type": "江",
            "flow": N("05-117", "舂陵水出焉，下流至常宁县，合于湘水"),
            "anchor": {"anchor": "新田县西北", "context": N("05-117", "舂陵水出焉")},
        },
    ],
    gar=[
        {
            "name": N("05-117", "白面寨巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "新田县东南",
            "dusi": "未明",
            "note": "东南有白面寨巡检司",
        },
    ],
)

# ---------- 宝庆府 ----------
item(
    "05-118",
    geo={
        "name": N("05-118", "宝庆府"),
        "level": "府",
        "node_type": "政区",
        "parent": {"text": "湖广", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "东北",
                "to_anchor": "布政司",
                "distance": 1250,
                "unit": "里",
                "raw": N("05-118", "东北距布政司千二百五十里"),
            }
        ],
        "note": "元宝庆路，属湖南道宣慰司。洪武元年为府。领州一，县四",
    },
    ents=[
        {
            "text": N("05-118", "宝庆府"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-118", "宝庆路"),
            "type": "place",
            "count": 1,
            "provenance": "元宝庆路",
        },
        {
            "text": N("05-118", "湖南道宣慰司"),
            "type": "institution",
            "count": 1,
            "provenance": "属湖南道宣慰司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 1,
            "era_raw": N("05-118", "洪武元年"),
            "category": "初置",
            "event": N("05-118", "为府"),
            "place": "宝庆府",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-118", "元宝庆路，属湖南道宣慰司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-118", "元宝庆路，属湖南道宣慰司"),
            "owner": "湖南道宣慰司",
        },
        {
            "phase": 2,
            "era_raw": N("05-118", "洪武元年"),
            "reign": "洪武",
            "year": 1,
            "change_type": "改置",
            "change": N("05-118", "为府"),
            "owner": "湖南道宣慰司",
        },
    ],
)

item(
    "05-119",
    geo={
        "name": N("05-119", "邵阳"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "宝庆府", "rel": "领"},
        "note": "倚。南有高霞山，东有烝水。又北有澬水，邵水自东流合焉。西北有龙回巡检司。又北有巨口关。东北有白马关",
    },
    ents=[
        {
            "text": N("05-119", "邵阳"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-119", "高霞山"),
            "type": "place",
            "count": 1,
            "provenance": "南有高霞山",
        },
        {
            "text": N("05-119", "烝水"),
            "type": "water",
            "count": 1,
            "provenance": "东有烝水",
        },
        {
            "text": N("05-119", "澬水"),
            "type": "water",
            "count": 1,
            "provenance": "又北有澬水",
        },
        {
            "text": N("05-119", "邵水"),
            "type": "water",
            "count": 1,
            "provenance": "邵水自东流合焉",
        },
        {
            "text": N("05-119", "龙回巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "西北有龙回巡检司",
        },
    ],
    hyd=[
        {
            "name": N("05-119", "烝水"),
            "type": "江",
            "flow": N("05-119", "东有烝水"),
            "anchor": {"anchor": "邵阳县东", "context": N("05-119", "东有烝水")},
        },
        {
            "name": N("05-119", "澬水"),
            "type": "江",
            "flow": N("05-119", "又北有澬水，邵水自东流合焉"),
            "anchor": {"anchor": "邵阳县北", "context": N("05-119", "又北有澬水")},
        },
        {
            "name": N("05-119", "邵水"),
            "type": "江",
            "flow": N("05-119", "邵水自东流合焉"),
            "anchor": {"anchor": "邵阳县东", "context": N("05-119", "邵水自东流合焉")},
        },
    ],
    gar=[
        {
            "name": N("05-119", "龙回巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "邵阳县西北",
            "dusi": "未明",
            "note": "西北有龙回巡检司",
        },
        {
            "name": N("05-119", "巨口关"),
            "type": "关",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "邵阳县北",
            "dusi": "未明",
            "note": "又北有巨口关",
        },
        {
            "name": N("05-119", "白马关"),
            "type": "关",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "邵阳县东北",
            "dusi": "未明",
            "note": "东北有白马关",
        },
    ],
)

item(
    "05-120",
    geo={
        "name": N("05-120", "新化"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "宝庆府", "rel": "领"},
        "note": "府北。南有上梅山，其下梅山在安化县境。东南有澬水。西南有长鄄巡检司，寻废。又北有苏溪巡检司",
    },
    ents=[
        {
            "text": N("05-120", "新化"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-120", "上梅山"),
            "type": "place",
            "count": 1,
            "provenance": "南有上梅山",
        },
        {
            "text": N("05-120", "澬水"),
            "type": "water",
            "count": 1,
            "provenance": "东南有澬水",
        },
        {
            "text": N("05-120", "苏溪巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "又北有苏溪巡检司",
        },
    ],
    hyd=[
        {
            "name": N("05-120", "澬水"),
            "type": "江",
            "flow": N("05-120", "东南有澬水"),
            "anchor": {"anchor": "新化县东南", "context": N("05-120", "东南有澬水")},
        },
    ],
    gar=[
        {
            "name": N("05-120", "长鄄巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "新化县西南",
            "dusi": "未明",
            "note": "西南有长鄄巡检司，寻废",
        },
        {
            "name": N("05-120", "苏溪巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "新化县北",
            "dusi": "未明",
            "note": "又北有苏溪巡检司",
        },
    ],
)

item(
    "05-121",
    geo={
        "name": N("05-121", "城步"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "宝庆府", "rel": "领"},
        "note": "府西南。本武冈州之城步巡检司。弘治十七年改置县，析绥宁县地益之。东南有罗汉山，又有巫水，下流入于澬水",
    },
    ents=[
        {
            "text": N("05-121", "城步"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-121", "城步巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "本武冈州之城步巡检司",
        },
        {
            "text": N("05-121", "罗汉山"),
            "type": "place",
            "count": 1,
            "provenance": "东南有罗汉山",
        },
        {
            "text": N("05-121", "巫水"),
            "type": "water",
            "count": 1,
            "provenance": "又有巫水",
        },
    ],
    tme=[
        {
            "reign": "弘治",
            "year": 17,
            "era_raw": N("05-121", "弘治十七年"),
            "category": "改置",
            "event": N("05-121", "改置县，析绥宁县地益之"),
            "place": "城步",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-121", "本武冈州之城步巡检司"),
            "reign": "未明",
            "year": 0,
            "change_type": "初置",
            "change": N("05-121", "本武冈州之城步巡检司"),
            "owner": "武冈州",
        },
        {
            "phase": 2,
            "era_raw": N("05-121", "弘治十七年"),
            "reign": "弘治",
            "year": 17,
            "change_type": "改置",
            "change": N("05-121", "改置县，析绥宁县地益之"),
            "owner": "宝庆府",
        },
    ],
    hyd=[
        {
            "name": N("05-121", "巫水"),
            "type": "江",
            "flow": N("05-121", "又有巫水，下流入于澬水"),
            "anchor": {"anchor": "城步县东南", "context": N("05-121", "又有巫水")},
        },
    ],
)

item(
    "05-122",
    geo={
        "name": N("05-122", "武冈州"),
        "level": "属州",
        "node_type": "政区",
        "parent": {"text": "宝庆府", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "东",
                "to_anchor": "宝庆府",
                "distance": 280,
                "unit": "里",
                "raw": N("05-122", "东距府二百八十里"),
            }
        ],
        "note": "元武冈路，属湖南道宣慰司。洪武元年为府。九年四月降为州，以州治武冈县省入，来属。领县一",
    },
    ents=[
        {
            "text": N("05-122", "武冈州"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-122", "武冈路"),
            "type": "place",
            "count": 1,
            "provenance": "元武冈路",
        },
        {
            "text": N("05-122", "武冈山"),
            "type": "place",
            "count": 1,
            "provenance": "北有武冈山",
        },
        {
            "text": N("05-122", "云山"),
            "type": "place",
            "count": 1,
            "provenance": "南有云山",
        },
        {
            "text": N("05-122", "澬水"),
            "type": "water",
            "count": 2,
            "provenance": "又有澬水",
        },
        {
            "text": N("05-122", "都梁水"),
            "type": "water",
            "count": 1,
            "provenance": "西南有都梁水",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 1,
            "era_raw": N("05-122", "洪武元年"),
            "category": "升秩",
            "event": N("05-122", "为府"),
            "place": "武冈州",
        },
        {
            "reign": "洪武",
            "year": 9,
            "era_raw": N("05-122", "九年四月"),
            "category": "降秩",
            "event": N("05-122", "降为州，以州治武冈县省入"),
            "place": "武冈州",
        },
        {
            "reign": "永乐",
            "year": 22,
            "era_raw": N("05-122", "永乐二十二年"),
            "category": "徙治",
            "event": N("05-122", "岷王府自云南迁于此"),
            "place": "武冈州",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-122", "元武冈路，属湖南道宣慰司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-122", "元武冈路，属湖南道宣慰司"),
            "owner": "湖南道宣慰司",
        },
        {
            "phase": 2,
            "era_raw": N("05-122", "洪武元年"),
            "reign": "洪武",
            "year": 1,
            "change_type": "改置",
            "change": N("05-122", "为府"),
            "owner": "湖南道宣慰司",
        },
        {
            "phase": 3,
            "era_raw": N("05-122", "九年四月"),
            "reign": "洪武",
            "year": 9,
            "change_type": "改置",
            "change": N("05-122", "降为州，以州治武冈县省入，来属"),
            "owner": "宝庆府",
        },
    ],
    hyd=[
        {
            "name": N("05-122", "澬水"),
            "type": "江",
            "flow": N("05-122", "又有澬水"),
            "anchor": {"anchor": "武冈州", "context": N("05-122", "又有澬水")},
        },
        {
            "name": N("05-122", "都梁水"),
            "type": "江",
            "flow": N("05-122", "西南有都梁水，东北流入焉"),
            "anchor": {"anchor": "武冈州西南", "context": N("05-122", "西南有都梁水")},
        },
    ],
    gar=[
        {
            "name": N("05-122", "蓼溪隘"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "武冈州北",
            "dusi": "未明",
            "note": "北有蓼溪隘、峡口镇，南有石门隘，东有紫阳关四巡检司",
        },
        {
            "name": N("05-122", "峡口镇"),
            "type": "镇",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "武冈州北",
            "dusi": "未明",
            "note": "北有蓼溪隘、峡口镇，南有石门隘，东有紫阳关四巡检司",
        },
        {
            "name": N("05-122", "石门隘"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "武冈州南",
            "dusi": "未明",
            "note": "北有蓼溪隘、峡口镇，南有石门隘，东有紫阳关四巡检司",
        },
        {
            "name": N("05-122", "紫阳关"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "武冈州东",
            "dusi": "未明",
            "note": "北有蓼溪隘、峡口镇，南有石门隘，东有紫阳关四巡检司",
        },
        {
            "name": N("05-122", "石羊关"),
            "type": "关",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "武冈州东",
            "dusi": "未明",
            "note": "东有石羊关",
        },
    ],
)

item(
    "05-123",
    geo={
        "name": N("05-123", "新宁"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "武冈州", "rel": "领"},
        "note": "州东南。旧治在县东。景泰二年移于沙洲原。南有夫夷水，北流合都梁水。东南有靖位、西有新寨二巡检司",
    },
    ents=[
        {
            "text": N("05-123", "新宁"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-123", "夫夷水"),
            "type": "water",
            "count": 1,
            "provenance": "南有夫夷水",
        },
        {
            "text": N("05-123", "都梁水"),
            "type": "water",
            "count": 1,
            "provenance": "北流合都梁水",
        },
        {
            "text": N("05-123", "靖位"),
            "type": "institution",
            "count": 1,
            "provenance": "东南有靖位、西有新寨二巡检司",
        },
    ],
    tme=[
        {
            "reign": "景泰",
            "year": 2,
            "era_raw": N("05-123", "景泰二年"),
            "category": "移治",
            "event": N("05-123", "旧治在县东。景泰二年移于沙洲原"),
            "place": "新宁",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-123", "旧治在县东"),
            "reign": "未明",
            "year": 0,
            "change_type": "初置",
            "change": N("05-123", "旧治在县东"),
            "owner": "武冈州",
        },
        {
            "phase": 2,
            "era_raw": N("05-123", "景泰二年"),
            "reign": "景泰",
            "year": 2,
            "change_type": "移治",
            "change": N("05-123", "移于沙洲原"),
            "owner": "武冈州",
        },
    ],
    hyd=[
        {
            "name": N("05-123", "夫夷水"),
            "type": "江",
            "flow": N("05-123", "南有夫夷水，北流合都梁水"),
            "anchor": {"anchor": "新宁县南", "context": N("05-123", "南有夫夷水")},
        },
    ],
    gar=[
        {
            "name": N("05-123", "靖位"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "新宁县东南",
            "dusi": "未明",
            "note": "东南有靖位、西有新寨二巡检司",
        },
        {
            "name": N("05-123", "新寨"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "新宁县西",
            "dusi": "未明",
            "note": "东南有靖位、西有新寨二巡检司",
        },
    ],
)

# ---------- 辰州府 ----------
item(
    "05-124",
    geo={
        "name": N("05-124", "辰州府"),
        "level": "府",
        "node_type": "政区",
        "parent": {"text": "湖广", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "东北",
                "to_anchor": "布政司",
                "distance": 1700,
                "unit": "里",
                "raw": N("05-124", "东北距布政司千七百里"),
            }
        ],
        "note": "元辰州路，属湖广行省。太祖甲辰年为府。领州一，县六",
    },
    ents=[
        {
            "text": N("05-124", "辰州府"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-124", "辰州路"),
            "type": "place",
            "count": 1,
            "provenance": "元辰州路",
        },
        {
            "text": N("05-124", "湖广行省"),
            "type": "institution",
            "count": 1,
            "provenance": "属湖广行省",
        },
    ],
    tme=[
        {
            "reign": "元",
            "year": 24,
            "era_raw": N("05-124", "太祖甲辰年"),
            "category": "初置",
            "event": N("05-124", "为府"),
            "place": "辰州府",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-124", "元辰州路，属湖广行省"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-124", "元辰州路，属湖广行省"),
            "owner": "湖广行省",
        },
        {
            "phase": 2,
            "era_raw": N("05-124", "太祖甲辰年"),
            "reign": "元",
            "year": 24,
            "change_type": "改置",
            "change": N("05-124", "为府"),
            "owner": "湖广行省",
        },
    ],
)

item(
    "05-125",
    geo={
        "name": N("05-125", "沅陵"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "辰州府", "rel": "领"},
        "note": "倚。西北有大酉山、小酉山。东有壶头山。西南有沅水，辰水自东北流入焉。又酉水在西北，东南入沅水。东有大刺、西北有明溪、又有会溪、东北有池蓬四巡检司",
    },
    ents=[
        {
            "text": N("05-125", "沅陵"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-125", "大酉山"),
            "type": "place",
            "count": 1,
            "provenance": "西北有大酉山、小酉山",
        },
        {
            "text": N("05-125", "小酉山"),
            "type": "place",
            "count": 1,
            "provenance": "西北有大酉山、小酉山",
        },
        {
            "text": N("05-125", "壶头山"),
            "type": "place",
            "count": 1,
            "provenance": "东有壶头山",
        },
        {
            "text": N("05-125", "沅水"),
            "type": "water",
            "count": 2,
            "provenance": "西南有沅水",
        },
        {
            "text": N("05-125", "辰水"),
            "type": "water",
            "count": 1,
            "provenance": "辰水自东北流入焉",
        },
    ],
    hyd=[
        {
            "name": N("05-125", "沅水"),
            "type": "江",
            "flow": N("05-125", "西南有沅水，辰水自东北流入焉"),
            "anchor": {"anchor": "沅陵县西南", "context": N("05-125", "西南有沅水")},
        },
        {
            "name": N("05-125", "辰水"),
            "type": "江",
            "flow": N("05-125", "辰水自东北流入焉"),
            "anchor": {
                "anchor": "沅陵县东北",
                "context": N("05-125", "辰水自东北流入焉"),
            },
        },
        {
            "name": N("05-125", "酉水"),
            "type": "江",
            "flow": N("05-125", "又酉水在西北，东南入沅水"),
            "anchor": {"anchor": "沅陵县西北", "context": N("05-125", "又酉水在西北")},
        },
    ],
    gar=[
        {
            "name": N("05-125", "大刺"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "沅陵县东",
            "dusi": "未明",
            "note": "东有大刺、西北有明溪、又有会溪、东北有池蓬四巡检司",
        },
        {
            "name": N("05-125", "明溪"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "沅陵县西北",
            "dusi": "未明",
            "note": "东有大刺、西北有明溪、又有会溪、东北有池蓬四巡检司",
        },
        {
            "name": N("05-125", "会溪"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "沅陵县",
            "dusi": "未明",
            "note": "东有大刺、西北有明溪、又有会溪、东北有池蓬四巡检司",
        },
        {
            "name": N("05-125", "池蓬"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "沅陵县东北",
            "dusi": "未明",
            "note": "东有大刺、西北有明溪、又有会溪、东北有池蓬四巡检司",
        },
        {
            "name": N("05-125", "高岩巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "沅陵县",
            "dusi": "未明",
            "note": "又有高岩巡检司，后废",
        },
    ],
)

item(
    "05-126",
    geo={
        "name": N("05-126", "卢溪"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "辰州府", "rel": "领"},
        "note": "府西少南。南有沅水。西有武溪，即潕溪也，下流合于沅水。又西有镇溪军民千户所，洪武三十年二月置",
    },
    ents=[
        {
            "text": N("05-126", "卢溪"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-126", "沅水"),
            "type": "water",
            "count": 2,
            "provenance": "南有沅水",
        },
        {
            "text": N("05-126", "武溪"),
            "type": "water",
            "count": 1,
            "provenance": "西有武溪",
        },
        {
            "text": N("05-126", "潕溪"),
            "type": "water",
            "count": 1,
            "provenance": "即潕溪也",
        },
        {
            "text": N("05-126", "镇溪军民千户所"),
            "type": "institution",
            "count": 1,
            "provenance": "又西有镇溪军民千户所",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 30,
            "era_raw": N("05-126", "洪武三十年二月"),
            "category": "增置",
            "event": N("05-126", "置镇溪军民千户所"),
            "place": "卢溪",
        },
    ],
    hyd=[
        {
            "name": N("05-126", "沅水"),
            "type": "江",
            "flow": N("05-126", "南有沅水"),
            "anchor": {"anchor": "卢溪县南", "context": N("05-126", "南有沅水")},
        },
        {
            "name": N("05-126", "武溪"),
            "alt": "潕溪",
            "type": "溪",
            "flow": N("05-126", "西有武溪，即潕溪也，下流合于沅水"),
            "anchor": {"anchor": "卢溪县西", "context": N("05-126", "西有武溪")},
        },
    ],
    gar=[
        {
            "name": N("05-126", "镇溪军民千户所"),
            "type": "守御千户所",
            "territorial": "未明",
            "established": {
                "reign": "洪武",
                "year": 30,
                "era_raw": N("05-126", "洪武三十年二月"),
            },
            "place": "卢溪县西",
            "dusi": "未明",
            "note": "又西有镇溪军民千户所，洪武三十年二月置",
        },
        {
            "name": N("05-126", "溪洞巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "卢溪县南",
            "dusi": "未明",
            "note": "又南有溪洞巡检司",
        },
        {
            "name": N("05-126", "河溪"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "卢溪县西",
            "dusi": "未明",
            "note": "又西有河溪、西南有院场坪二巡检司，后废",
        },
        {
            "name": N("05-126", "院场坪"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "卢溪县西南",
            "dusi": "未明",
            "note": "又西有河溪、西南有院场坪二巡检司，后废",
        },
    ],
)

item(
    "05-127",
    geo={
        "name": N("05-127", "辰溪"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "辰州府", "rel": "领"},
        "note": "府西南。东南有五城山。西北有沅水。西有辰水。又东有渡口镇、南有晋市镇二巡检司，后废",
    },
    ents=[
        {
            "text": N("05-127", "辰溪"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-127", "五城山"),
            "type": "place",
            "count": 1,
            "provenance": "东南有五城山",
        },
        {
            "text": N("05-127", "沅水"),
            "type": "water",
            "count": 1,
            "provenance": "西北有沅水",
        },
        {
            "text": N("05-127", "辰水"),
            "type": "water",
            "count": 1,
            "provenance": "西有辰水",
        },
    ],
    hyd=[
        {
            "name": N("05-127", "沅水"),
            "type": "江",
            "flow": N("05-127", "西北有沅水"),
            "anchor": {"anchor": "辰溪县西北", "context": N("05-127", "西北有沅水")},
        },
        {
            "name": N("05-127", "辰水"),
            "type": "江",
            "flow": N("05-127", "西有辰水"),
            "anchor": {"anchor": "辰溪县西", "context": N("05-127", "西有辰水")},
        },
    ],
    gar=[
        {
            "name": N("05-127", "渡口镇"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "辰溪县东",
            "dusi": "未明",
            "note": "又东有渡口镇、南有晋市镇二巡检司，后废",
        },
        {
            "name": N("05-127", "晋市镇"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "辰溪县南",
            "dusi": "未明",
            "note": "又东有渡口镇、南有晋市镇二巡检司，后废",
        },
    ],
)

item(
    "05-128",
    geo={
        "name": N("05-128", "溆浦"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "辰州府", "rel": "领"},
        "note": "府东南。东有红旗洞。西有溆水，下流入沅水。南有龙潭、东北有镇宁二巡检司",
    },
    ents=[
        {
            "text": N("05-128", "溆浦"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-128", "红旗洞"),
            "type": "place",
            "count": 1,
            "provenance": "东有红旗洞",
        },
        {
            "text": N("05-128", "溆水"),
            "type": "water",
            "count": 1,
            "provenance": "西有溆水",
        },
    ],
    hyd=[
        {
            "name": N("05-128", "溆水"),
            "type": "江",
            "flow": N("05-128", "西有溆水，下流入沅水"),
            "anchor": {"anchor": "溆浦县西", "context": N("05-128", "西有溆水")},
        },
    ],
    gar=[
        {
            "name": N("05-128", "龙潭"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "溆浦县南",
            "dusi": "未明",
            "note": "南有龙潭、东北有镇宁二巡检司",
        },
        {
            "name": N("05-128", "镇宁"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "溆浦县东北",
            "dusi": "未明",
            "note": "南有龙潭、东北有镇宁二巡检司",
        },
    ],
)

item(
    "05-129",
    geo={
        "name": N("05-129", "沅州"),
        "level": "属州",
        "node_type": "政区",
        "parent": {"text": "辰州府", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "东北",
                "to_anchor": "辰州府",
                "distance": 270,
                "unit": "里",
                "raw": N("05-129", "东北距府二百七十里"),
            }
        ],
        "note": "元沅州路，直隶湖广行省。太祖甲辰年为府。九年四月降为州，以州治卢阳县省入，来属。领县二",
    },
    ents=[
        {
            "text": N("05-129", "沅州"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-129", "沅州路"),
            "type": "place",
            "count": 1,
            "provenance": "元沅州路",
        },
        {
            "text": N("05-129", "明山"),
            "type": "place",
            "count": 1,
            "provenance": "北有明山",
        },
        {
            "text": N("05-129", "沅江"),
            "type": "water",
            "count": 2,
            "provenance": "南有沅江",
        },
        {
            "text": N("05-129", "舞水"),
            "type": "water",
            "count": 1,
            "provenance": "西有舞水",
        },
        {
            "text": N("05-129", "晃州巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "西有晃州巡检司",
        },
    ],
    tme=[
        {
            "reign": "元",
            "year": 24,
            "era_raw": N("05-129", "太祖甲辰年"),
            "category": "升秩",
            "event": N("05-129", "为府"),
            "place": "沅州",
        },
        {
            "reign": "洪武",
            "year": 9,
            "era_raw": N("05-129", "九年四月"),
            "category": "降秩",
            "event": N("05-129", "降为州，以州治卢阳县省入"),
            "place": "沅州",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-129", "元沅州路，直隶湖广行省"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-129", "元沅州路，直隶湖广行省"),
            "owner": "湖广行省",
        },
        {
            "phase": 2,
            "era_raw": N("05-129", "太祖甲辰年"),
            "reign": "元",
            "year": 24,
            "change_type": "改置",
            "change": N("05-129", "为府"),
            "owner": "湖广行省",
        },
        {
            "phase": 3,
            "era_raw": N("05-129", "九年四月"),
            "reign": "洪武",
            "year": 9,
            "change_type": "改置",
            "change": N("05-129", "降为州，以州治卢阳县省入，来属"),
            "owner": "辰州府",
        },
    ],
    hyd=[
        {
            "name": N("05-129", "沅江"),
            "type": "江",
            "flow": N("05-129", "南有沅江，其源出四川遵义县，下流至沅江县，入洞庭湖"),
            "anchor": {"anchor": "沅州南", "context": N("05-129", "南有沅江")},
        },
        {
            "name": N("05-129", "舞水"),
            "alt": "无水",
            "type": "江",
            "flow": N("05-129", "西有舞水，即无水也，流入于沅水"),
            "anchor": {"anchor": "沅州西", "context": N("05-129", "西有舞水")},
        },
    ],
    gar=[
        {
            "name": N("05-129", "晃州巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "沅州西",
            "dusi": "未明",
            "note": "西有晃州巡检司",
        },
        {
            "name": N("05-129", "西关渡口巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "沅州西南",
            "dusi": "未明",
            "note": "又西南有西关渡口巡检司，后废",
        },
    ],
)

item(
    "05-130",
    geo={
        "name": N("05-130", "黔阳"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "沅州", "rel": "领"},
        "note": "州东南。东南有罗公山。南有双石崖，一名屏风崖。北有沅水。又东有洪江，西有郎江，南有黔江，俱流入焉",
    },
    ents=[
        {
            "text": N("05-130", "黔阳"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-130", "罗公山"),
            "type": "place",
            "count": 1,
            "provenance": "东南有罗公山",
        },
        {
            "text": N("05-130", "屏风崖"),
            "type": "place",
            "count": 1,
            "provenance": "南有双石崖，一名屏风崖",
        },
        {
            "text": N("05-130", "沅水"),
            "type": "water",
            "count": 1,
            "provenance": "北有沅水",
        },
        {
            "text": N("05-130", "洪江"),
            "type": "water",
            "count": 2,
            "provenance": "又东有洪江",
        },
        {
            "text": N("05-130", "黔江"),
            "type": "water",
            "count": 1,
            "provenance": "南有黔江",
        },
    ],
    hyd=[
        {
            "name": N("05-130", "沅水"),
            "type": "江",
            "flow": N("05-130", "北有沅水"),
            "anchor": {"anchor": "黔阳县北", "context": N("05-130", "北有沅水")},
        },
        {
            "name": N("05-130", "洪江"),
            "type": "江",
            "flow": N("05-130", "又东有洪江，西有郎江，南有黔江，俱流入焉"),
            "anchor": {"anchor": "黔阳县东", "context": N("05-130", "又东有洪江")},
        },
        {
            "name": N("05-130", "郎江"),
            "type": "江",
            "flow": N("05-130", "又东有洪江，西有郎江，南有黔江，俱流入焉"),
            "anchor": {"anchor": "黔阳县西", "context": N("05-130", "西有郎江")},
        },
        {
            "name": N("05-130", "黔江"),
            "type": "江",
            "flow": N("05-130", "又东有洪江，西有郎江，南有黔江，俱流入焉"),
            "anchor": {"anchor": "黔阳县南", "context": N("05-130", "南有黔江")},
        },
    ],
    gar=[
        {
            "name": N("05-130", "安江巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "黔阳县东",
            "dusi": "未明",
            "note": "东有安江巡检司",
        },
        {
            "name": N("05-130", "托口寨"),
            "type": "未明",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "黔阳县西",
            "dusi": "未明",
            "note": "又西有托口寨",
        },
        {
            "name": N("05-130", "洪江寨"),
            "type": "未明",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "黔阳县东",
            "dusi": "未明",
            "note": "东有洪江寨",
        },
    ],
)

item(
    "05-131",
    geo={
        "name": N("05-131", "麻阳"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "沅州", "rel": "领"},
        "note": "州北少西。东有包茅山。西有蜡尔山，与保靖司及四川、贵州界。南有辰水，自贵州铜仁府流入。西有锦水。东北有岩门巡检司",
    },
    ents=[
        {
            "text": N("05-131", "麻阳"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-131", "包茅山"),
            "type": "place",
            "count": 1,
            "provenance": "东有包茅山",
        },
        {
            "text": N("05-131", "蜡尔山"),
            "type": "place",
            "count": 1,
            "provenance": "西有蜡尔山",
        },
        {
            "text": N("05-131", "辰水"),
            "type": "water",
            "count": 1,
            "provenance": "南有辰水",
        },
        {
            "text": N("05-131", "锦水"),
            "type": "water",
            "count": 1,
            "provenance": "西有锦水",
        },
        {
            "text": N("05-131", "岩门巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "东北有岩门巡检司",
        },
    ],
    hyd=[
        {
            "name": N("05-131", "辰水"),
            "type": "江",
            "flow": N("05-131", "南有辰水，自贵州铜仁府流入"),
            "anchor": {"anchor": "麻阳县南", "context": N("05-131", "南有辰水")},
        },
        {
            "name": N("05-131", "锦水"),
            "type": "江",
            "flow": N("05-131", "西有锦水，下流入于辰州"),
            "anchor": {"anchor": "麻阳县西", "context": N("05-131", "西有锦水")},
        },
    ],
    gar=[
        {
            "name": N("05-131", "岩门巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "麻阳县东北",
            "dusi": "未明",
            "note": "东北有岩门巡检司",
        },
    ],
)

# ---------- 郴州（直隶州） ----------
item(
    "05-132",
    geo={
        "name": N("05-132", "郴州"),
        "level": "直隶州",
        "node_type": "政区",
        "parent": {"text": "湖广", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "北",
                "to_anchor": "布政司",
                "distance": 1880,
                "unit": "里",
                "raw": N("05-132", "北距布政司千八百八十里"),
            }
        ],
        "note": "元郴州路，属湖南道宣慰司。洪武元年为府。九年四月降为州，以州治郴阳县省入，直隶布政司。领县五",
    },
    ents=[
        {
            "text": N("05-132", "郴州"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-132", "郴州路"),
            "type": "place",
            "count": 1,
            "provenance": "元郴州路",
        },
        {
            "text": N("05-132", "黄岑山"),
            "type": "place",
            "count": 1,
            "provenance": "南有黄岑山",
        },
        {
            "text": N("05-132", "骑田岭"),
            "type": "place",
            "count": 1,
            "provenance": "亦曰骑田岭，五岭之第二岭也",
        },
        {
            "text": N("05-132", "郴水"),
            "type": "water",
            "count": 1,
            "provenance": "东有郴水",
        },
        {
            "text": N("05-132", "桂水"),
            "type": "water",
            "count": 1,
            "provenance": "又西南有桂水",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 1,
            "era_raw": N("05-132", "洪武元年"),
            "category": "升秩",
            "event": N("05-132", "为府"),
            "place": "郴州",
        },
        {
            "reign": "洪武",
            "year": 9,
            "era_raw": N("05-132", "九年四月"),
            "category": "降秩",
            "event": N("05-132", "降为州，以州治郴阳县省入"),
            "place": "郴州",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-132", "元郴州路，属湖南道宣慰司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-132", "元郴州路，属湖南道宣慰司"),
            "owner": "湖南道宣慰司",
        },
        {
            "phase": 2,
            "era_raw": N("05-132", "洪武元年"),
            "reign": "洪武",
            "year": 1,
            "change_type": "改置",
            "change": N("05-132", "为府"),
            "owner": "湖南道宣慰司",
        },
        {
            "phase": 3,
            "era_raw": N("05-132", "九年四月"),
            "reign": "洪武",
            "year": 9,
            "change_type": "改置",
            "change": N("05-132", "降为州，以州治郴阳县省入，直隶布政司"),
            "owner": "湖广布政司",
        },
    ],
    hyd=[
        {
            "name": N("05-132", "郴水"),
            "type": "江",
            "flow": N("05-132", "东有郴水，发源黄岑山，流合桂阳县之耒水，下流入于湘水"),
            "anchor": {"anchor": "郴州东", "context": N("05-132", "东有郴水")},
        },
        {
            "name": N("05-132", "桂水"),
            "type": "江",
            "flow": N("05-132", "又西南有桂水，下流合于耒水"),
            "anchor": {"anchor": "郴州西南", "context": N("05-132", "又西南有桂水")},
        },
    ],
    gar=[
        {
            "name": N("05-132", "石陂巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "郴州西南",
            "dusi": "未明",
            "note": "西南有石陂巡检司",
        },
    ],
)

item(
    "05-133",
    geo={
        "name": N("05-133", "永兴"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "郴州", "rel": "领"},
        "note": "州北少西。东南有土富山，旧有银井。西有高亭山。东有郴水。西有高亭、北有安福二巡检司",
    },
    ents=[
        {
            "text": N("05-133", "永兴"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-133", "土富山"),
            "type": "place",
            "count": 1,
            "provenance": "东南有土富山",
        },
        {
            "text": N("05-133", "高亭山"),
            "type": "place",
            "count": 1,
            "provenance": "西有高亭山",
        },
        {
            "text": N("05-133", "郴水"),
            "type": "water",
            "count": 1,
            "provenance": "东有郴水",
        },
        {
            "text": N("05-133", "白豹水"),
            "type": "water",
            "count": 1,
            "provenance": "又有白豹水",
        },
    ],
    hyd=[
        {
            "name": N("05-133", "郴水"),
            "type": "江",
            "flow": N("05-133", "东有郴水"),
            "anchor": {"anchor": "永兴县东", "context": N("05-133", "东有郴水")},
        },
        {
            "name": N("05-133", "白豹水"),
            "type": "溪",
            "flow": N("05-133", "又有白豹水，自西南流入焉，谓之森口"),
            "anchor": {"anchor": "永兴县西南", "context": N("05-133", "又有白豹水")},
        },
    ],
    res=[
        {
            "name": N("05-133", "银井"),
            "type": "银",
            "place": "永兴县",
            "site": "土富山",
            "importance": "旧有银井",
            "raw": N("05-133", "东南有土富山，旧有银井"),
        },
    ],
    gar=[
        {
            "name": N("05-133", "高亭"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "永兴县西",
            "dusi": "未明",
            "note": "西有高亭、北有安福二巡检司",
        },
        {
            "name": N("05-133", "安福"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "永兴县北",
            "dusi": "未明",
            "note": "西有高亭、北有安福二巡检司",
        },
    ],
)

item(
    "05-134",
    geo={
        "name": N("05-134", "宜章"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "郴州", "rel": "领"},
        "note": "州南。西南有莽山。东有漏天山。北有章水，支流曰小章水。东有赤石、南有白沙二巡检司",
    },
    ents=[
        {
            "text": N("05-134", "宜章"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-134", "莽山"),
            "type": "place",
            "count": 1,
            "provenance": "西南有莽山",
        },
        {
            "text": N("05-134", "漏天山"),
            "type": "place",
            "count": 1,
            "provenance": "东有漏天山",
        },
        {
            "text": N("05-134", "章水"),
            "type": "water",
            "count": 1,
            "provenance": "北有章水",
        },
        {
            "text": N("05-134", "武水"),
            "type": "water",
            "count": 1,
            "provenance": "有武水自西来合焉",
        },
    ],
    hyd=[
        {
            "name": N("05-134", "章水"),
            "type": "江",
            "flow": N(
                "05-134",
                "北有章水，支流曰小章水，源俱出黄岑山，有武水自西来合焉，下流入江西崇义县界",
            ),
            "anchor": {"anchor": "宜章县北", "context": N("05-134", "北有章水")},
        },
        {
            "name": N("05-134", "小章水"),
            "type": "溪",
            "flow": N("05-134", "支流曰小章水"),
            "anchor": {"anchor": "宜章县北", "context": N("05-134", "支流曰小章水")},
        },
        {
            "name": N("05-134", "武水"),
            "type": "江",
            "flow": N("05-134", "有武水自西来合焉"),
            "anchor": {
                "anchor": "宜章县西",
                "context": N("05-134", "有武水自西来合焉"),
            },
        },
    ],
    gar=[
        {
            "name": N("05-134", "赤石"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "宜章县东",
            "dusi": "未明",
            "note": "东有赤石、南有白沙二巡检司",
        },
        {
            "name": N("05-134", "白沙"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "宜章县南",
            "dusi": "未明",
            "note": "东有赤石、南有白沙二巡检司",
        },
    ],
)

item(
    "05-135",
    geo={
        "name": N("05-135", "兴宁"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "郴州", "rel": "领"},
        "note": "州东北。南有耒水，东南有资兴水流合焉。东有州门巡检司。东南有滁口巡检司",
    },
    ents=[
        {
            "text": N("05-135", "兴宁"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-135", "耒水"),
            "type": "water",
            "count": 1,
            "provenance": "南有耒水",
        },
        {
            "text": N("05-135", "资兴水"),
            "type": "water",
            "count": 1,
            "provenance": "东南有资兴水流合焉",
        },
        {
            "text": N("05-135", "州门巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "东有州门巡检司",
        },
    ],
    hyd=[
        {
            "name": N("05-135", "耒水"),
            "type": "江",
            "flow": N("05-135", "南有耒水，东南有资兴水流合焉"),
            "anchor": {"anchor": "兴宁县南", "context": N("05-135", "南有耒水")},
        },
        {
            "name": N("05-135", "资兴水"),
            "type": "溪",
            "flow": N("05-135", "东南有资兴水流合焉"),
            "anchor": {
                "anchor": "兴宁县东南",
                "context": N("05-135", "东南有资兴水流合焉"),
            },
        },
    ],
    gar=[
        {
            "name": N("05-135", "州门巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "兴宁县东",
            "dusi": "未明",
            "note": "东有州门巡检司",
        },
        {
            "name": N("05-135", "滁口巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "兴宁县东南",
            "dusi": "未明",
            "note": "东南有滁口巡检司，后移于西南之黄家摐",
        },
    ],
)

item(
    "05-136",
    geo={
        "name": N("05-136", "桂阳"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "郴州", "rel": "领"},
        "note": "州西南。南有耒山，耒水所出。东有守御广安千户所，洪武二十九年三月置，后废。宣德八年六月复置。东有益将、西有镇安、南有长乐山口、北有濠村四巡检司",
    },
    ents=[
        {
            "text": N("05-136", "桂阳"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-136", "耒山"),
            "type": "place",
            "count": 1,
            "provenance": "南有耒山",
        },
        {
            "text": N("05-136", "耒水"),
            "type": "water",
            "count": 1,
            "provenance": "耒水所出",
        },
        {
            "text": N("05-136", "守御广安千户所"),
            "type": "institution",
            "count": 1,
            "provenance": "东有守御广安千户所",
        },
        {
            "text": N("05-136", "孤山水"),
            "type": "water",
            "count": 1,
            "provenance": "又东有孤山水",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 29,
            "era_raw": N("05-136", "洪武二十九年三月"),
            "category": "增置",
            "event": N("05-136", "置守御广安千户所"),
            "place": "桂阳",
        },
        {
            "reign": "宣德",
            "year": 8,
            "era_raw": N("05-136", "宣德八年六月"),
            "category": "复设",
            "event": N("05-136", "复置"),
            "place": "桂阳",
        },
    ],
    hyd=[
        {
            "name": N("05-136", "耒水"),
            "type": "江",
            "flow": N("05-136", "南有耒山，耒水所出，西北会于郴水"),
            "anchor": {"anchor": "桂阳县南", "context": N("05-136", "耒水所出")},
        },
        {
            "name": N("05-136", "孤山水"),
            "type": "溪",
            "flow": N("05-136", "又东有孤山水，流入江西崇义县，达于赣水"),
            "anchor": {"anchor": "桂阳县东", "context": N("05-136", "又东有孤山水")},
        },
    ],
    gar=[
        {
            "name": N("05-136", "守御广安千户所"),
            "type": "守御千户所",
            "territorial": "未明",
            "established": {
                "reign": "洪武",
                "year": 29,
                "era_raw": N("05-136", "洪武二十九年三月"),
            },
            "place": "桂阳县东",
            "dusi": "未明",
            "note": "东有守御广安千户所，洪武二十九年三月置，后废。宣德八年六月复置",
        },
        {
            "name": N("05-136", "益将"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "桂阳县东",
            "dusi": "未明",
            "note": "东有益将、西有镇安、南有长乐山口、北有濠村四巡检司",
        },
        {
            "name": N("05-136", "镇安"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "桂阳县西",
            "dusi": "未明",
            "note": "东有益将、西有镇安、南有长乐山口、北有濠村四巡检司",
        },
        {
            "name": N("05-136", "长乐山口"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "桂阳县南",
            "dusi": "未明",
            "note": "东有益将、西有镇安、南有长乐山口、北有濠村四巡检司",
        },
        {
            "name": N("05-136", "濠村"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "桂阳县北",
            "dusi": "未明",
            "note": "东有益将、西有镇安、南有长乐山口、北有濠村四巡检司",
        },
    ],
)

item(
    "05-137",
    geo={
        "name": N("05-137", "桂东"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "郴州", "rel": "领"},
        "note": "州东。西北有小桂山，桂水所出，南有沤江来合焉。又南有高分岭巡检司",
    },
    ents=[
        {
            "text": N("05-137", "桂东"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-137", "小桂山"),
            "type": "place",
            "count": 1,
            "provenance": "西北有小桂山",
        },
        {
            "text": N("05-137", "桂水"),
            "type": "water",
            "count": 1,
            "provenance": "桂水所出",
        },
        {
            "text": N("05-137", "沤江"),
            "type": "water",
            "count": 1,
            "provenance": "南有沤江来合焉",
        },
    ],
    hyd=[
        {
            "name": N("05-137", "桂水"),
            "type": "江",
            "flow": N("05-137", "西北有小桂山，桂水所出，南有沤江来合焉"),
            "anchor": {"anchor": "桂东县西北", "context": N("05-137", "桂水所出")},
        },
        {
            "name": N("05-137", "沤江"),
            "type": "江",
            "flow": N("05-137", "南有沤江来合焉"),
            "anchor": {"anchor": "桂东县南", "context": N("05-137", "南有沤江来合焉")},
        },
    ],
    gar=[
        {
            "name": N("05-137", "高分岭巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "桂东县南",
            "dusi": "未明",
            "note": "又南有高分岭巡检司",
        },
    ],
)

# ---------- 靖州（直隶州） ----------
item(
    "05-138",
    geo={
        "name": N("05-138", "靖州"),
        "level": "直隶州",
        "node_type": "政区",
        "parent": {"text": "湖广", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "东北",
                "to_anchor": "布政司",
                "distance": 1850,
                "unit": "里",
                "raw": N("05-138", "东北距布政司千八百五十里"),
            }
        ],
        "note": "元靖州路，直隶湖广行省。太祖乙巳年七月为靖州军民安抚司。元年降为州。三年升为府。九年四月复降为州，以州治永平县省入，直隶布政司。领县四",
    },
    ents=[
        {
            "text": N("05-138", "靖州"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-138", "靖州路"),
            "type": "place",
            "count": 1,
            "provenance": "元靖州路",
        },
        {
            "text": N("05-138", "侍郎山"),
            "type": "place",
            "count": 1,
            "provenance": "南有侍郎山",
        },
        {
            "text": N("05-138", "渠水"),
            "type": "water",
            "count": 1,
            "provenance": "东有渠水",
        },
        {
            "text": N("05-138", "郎江"),
            "type": "water",
            "count": 1,
            "provenance": "下流合会同县之郎江而入沅水",
        },
    ],
    tme=[
        {
            "reign": "元",
            "year": 25,
            "era_raw": N("05-138", "太祖乙巳年七月"),
            "category": "改置",
            "event": N("05-138", "为靖州军民安抚司"),
            "place": "靖州",
        },
        {
            "reign": "洪武",
            "year": 1,
            "era_raw": N("05-138", "元年"),
            "category": "降秩",
            "event": N("05-138", "降为州"),
            "place": "靖州",
        },
        {
            "reign": "洪武",
            "year": 3,
            "era_raw": N("05-138", "三年"),
            "category": "升秩",
            "event": N("05-138", "升为府"),
            "place": "靖州",
        },
        {
            "reign": "洪武",
            "year": 9,
            "era_raw": N("05-138", "九年四月"),
            "category": "降秩",
            "event": N("05-138", "复降为州，以州治永平县省入"),
            "place": "靖州",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-138", "元靖州路，直隶湖广行省"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-138", "元靖州路，直隶湖广行省"),
            "owner": "湖广行省",
        },
        {
            "phase": 2,
            "era_raw": N("05-138", "太祖乙巳年七月"),
            "reign": "元",
            "year": 25,
            "change_type": "改置",
            "change": N("05-138", "为靖州军民安抚司"),
            "owner": "湖广行省",
        },
        {
            "phase": 3,
            "era_raw": N("05-138", "元年"),
            "reign": "洪武",
            "year": 1,
            "change_type": "改置",
            "change": N("05-138", "降为州"),
            "owner": "湖广行省",
        },
        {
            "phase": 4,
            "era_raw": N("05-138", "三年"),
            "reign": "洪武",
            "year": 3,
            "change_type": "改置",
            "change": N("05-138", "升为府"),
            "owner": "湖广行省",
        },
        {
            "phase": 5,
            "era_raw": N("05-138", "九年四月"),
            "reign": "洪武",
            "year": 9,
            "change_type": "改置",
            "change": N("05-138", "复降为州，以州治永平县省入，直隶布政司"),
            "owner": "湖广布政司",
        },
    ],
    hyd=[
        {
            "name": N("05-138", "渠水"),
            "type": "江",
            "flow": N("05-138", "东有渠水，下流合会同县之郎江而入沅水"),
            "anchor": {"anchor": "靖州东", "context": N("05-138", "东有渠水")},
        },
    ],
    gar=[
        {
            "name": N("05-138", "零溪巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "靖州西",
            "dusi": "未明",
            "note": "西有零溪巡检司",
        },
    ],
)

item(
    "05-139",
    geo={
        "name": N("05-139", "会同"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "靖州", "rel": "领"},
        "note": "州东北。西有沅水，又西南有郎水。又东有雄溪，一名洪江，下流俱入于沅水。南有若水巡检司",
    },
    ents=[
        {
            "text": N("05-139", "会同"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-139", "沅水"),
            "type": "water",
            "count": 1,
            "provenance": "西有沅水",
        },
        {
            "text": N("05-139", "郎水"),
            "type": "water",
            "count": 1,
            "provenance": "又西南有郎水",
        },
        {
            "text": N("05-139", "雄溪"),
            "type": "water",
            "count": 1,
            "provenance": "又东有雄溪，一名洪江",
        },
        {
            "text": N("05-139", "若水巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "南有若水巡检司",
        },
    ],
    hyd=[
        {
            "name": N("05-139", "沅水"),
            "type": "江",
            "flow": N("05-139", "西有沅水"),
            "anchor": {"anchor": "会同县西", "context": N("05-139", "西有沅水")},
        },
        {
            "name": N("05-139", "郎水"),
            "type": "江",
            "flow": N("05-139", "又西南有郎水，自贵州黎平府流入"),
            "anchor": {"anchor": "会同县西南", "context": N("05-139", "又西南有郎水")},
        },
        {
            "name": N("05-139", "雄溪"),
            "alt": "洪江",
            "type": "溪",
            "flow": N("05-139", "又东有雄溪，一名洪江，下流俱入于沅水"),
            "anchor": {"anchor": "会同县东", "context": N("05-139", "又东有雄溪")},
        },
    ],
    gar=[
        {
            "name": N("05-139", "若水巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "会同县南",
            "dusi": "未明",
            "note": "南有若水巡检司",
        },
    ],
)

item(
    "05-140",
    geo={
        "name": N("05-140", "通道"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "靖州", "rel": "领"},
        "note": "州南。洪武十年五月省入州。十三年五月复置。北有福湖山。西有渠水，西北有播扬河。有播扬巡检司。又西南有收溪寨巡检司",
    },
    ents=[
        {
            "text": N("05-140", "通道"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-140", "福湖山"),
            "type": "place",
            "count": 1,
            "provenance": "北有福湖山",
        },
        {
            "text": N("05-140", "渠水"),
            "type": "water",
            "count": 1,
            "provenance": "西有渠水",
        },
        {
            "text": N("05-140", "播扬河"),
            "type": "water",
            "count": 1,
            "provenance": "西北有播扬河",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 10,
            "era_raw": N("05-140", "洪武十年五月"),
            "category": "省入",
            "event": N("05-140", "省入州"),
            "place": "通道",
        },
        {
            "reign": "洪武",
            "year": 13,
            "era_raw": N("05-140", "十三年五月"),
            "category": "复设",
            "event": N("05-140", "复置"),
            "place": "通道",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-140", "洪武十年五月"),
            "reign": "洪武",
            "year": 10,
            "change_type": "省入",
            "change": N("05-140", "省入州"),
            "owner": "靖州",
        },
        {
            "phase": 2,
            "era_raw": N("05-140", "十三年五月"),
            "reign": "洪武",
            "year": 13,
            "change_type": "复置",
            "change": N("05-140", "复置"),
            "owner": "靖州",
        },
    ],
    hyd=[
        {
            "name": N("05-140", "渠水"),
            "type": "江",
            "flow": N("05-140", "西有渠水"),
            "anchor": {"anchor": "通道县西", "context": N("05-140", "西有渠水")},
        },
        {
            "name": N("05-140", "播扬河"),
            "type": "河",
            "flow": N("05-140", "西北有播扬河，自贵州黎平府流合焉"),
            "anchor": {"anchor": "通道县西北", "context": N("05-140", "西北有播扬河")},
        },
    ],
    gar=[
        {
            "name": N("05-140", "播扬巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "通道县西北",
            "dusi": "未明",
            "note": "有播扬巡检司",
        },
        {
            "name": N("05-140", "收溪寨巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "通道县西南",
            "dusi": "未明",
            "note": "又西南有收溪寨巡检司",
        },
    ],
)

item(
    "05-141",
    geo={
        "name": N("05-141", "绥宁"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "靖州", "rel": "领"},
        "note": "州东。元属武冈路。洪武元年属武冈府。三年来属。东有双溪，即城步县巫水之下流也。东北有青坡巡检司。西南有临口巡检司",
    },
    ents=[
        {
            "text": N("05-141", "绥宁"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-141", "双溪"),
            "type": "water",
            "count": 1,
            "provenance": "东有双溪",
        },
        {
            "text": N("05-141", "巫水"),
            "type": "water",
            "count": 1,
            "provenance": "即城步县巫水之下流也",
        },
        {
            "text": N("05-141", "青坡巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "东北有青坡巡检司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 1,
            "era_raw": N("05-141", "洪武元年"),
            "category": "改隶",
            "event": N("05-141", "属武冈府"),
            "place": "绥宁",
        },
        {
            "reign": "洪武",
            "year": 3,
            "era_raw": N("05-141", "三年"),
            "category": "改隶",
            "event": N("05-141", "来属"),
            "place": "绥宁",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-141", "元属武冈路"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-141", "元属武冈路"),
            "owner": "武冈路",
        },
        {
            "phase": 2,
            "era_raw": N("05-141", "洪武元年"),
            "reign": "洪武",
            "year": 1,
            "change_type": "改隶",
            "change": N("05-141", "属武冈府"),
            "owner": "武冈府",
        },
        {
            "phase": 3,
            "era_raw": N("05-141", "三年"),
            "reign": "洪武",
            "year": 3,
            "change_type": "改隶",
            "change": N("05-141", "来属"),
            "owner": "靖州",
        },
    ],
    hyd=[
        {
            "name": N("05-141", "双溪"),
            "type": "溪",
            "flow": N("05-141", "东有双溪，即城步县巫水之下流也"),
            "anchor": {"anchor": "绥宁县东", "context": N("05-141", "东有双溪")},
        },
    ],
    gar=[
        {
            "name": N("05-141", "青坡巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "绥宁县东北",
            "dusi": "未明",
            "note": "东北有青坡巡检司，后移于武阳",
        },
        {
            "name": N("05-141", "临口巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "绥宁县西南",
            "dusi": "未明",
            "note": "西南有临口巡检司",
        },
    ],
)

item(
    "05-142",
    geo={
        "name": N("05-142", "天柱"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "靖州", "rel": "领"},
        "note": "州西北。本天柱守御千户所，洪武二十五年五月置。万历二十五年改为县，析绥宁、会同二县地益之。东有沅水。西北有屯镇汶溪后千户所，洪武二十三年置",
    },
    ents=[
        {
            "text": N("05-142", "天柱"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-142", "天柱守御千户所"),
            "type": "institution",
            "count": 1,
            "provenance": "本天柱守御千户所",
        },
        {
            "text": N("05-142", "沅水"),
            "type": "water",
            "count": 1,
            "provenance": "东有沅水",
        },
        {
            "text": N("05-142", "屯镇汶溪后千户所"),
            "type": "institution",
            "count": 1,
            "provenance": "西北有屯镇汶溪后千户所",
        },
        {
            "text": N("05-142", "镇远巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "东有镇远巡检司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 25,
            "era_raw": N("05-142", "洪武二十五年五月"),
            "category": "初置",
            "event": N("05-142", "置天柱守御千户所"),
            "place": "天柱",
        },
        {
            "reign": "万历",
            "year": 25,
            "era_raw": N("05-142", "万历二十五年"),
            "category": "改置",
            "event": N("05-142", "改为县，析绥宁、会同二县地益之"),
            "place": "天柱",
        },
        {
            "reign": "崇祯",
            "year": 10,
            "era_raw": N("05-142", "崇祯十年"),
            "category": "徙治",
            "event": N("05-142", "东迁龙塘，名龙塘县"),
            "place": "天柱",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-142", "本天柱守御千户所，洪武二十五年五月置"),
            "reign": "洪武",
            "year": 25,
            "change_type": "初置",
            "change": N("05-142", "本天柱守御千户所，洪武二十五年五月置"),
            "owner": "靖州",
        },
        {
            "phase": 2,
            "era_raw": N("05-142", "万历二十五年"),
            "reign": "万历",
            "year": 25,
            "change_type": "改置",
            "change": N("05-142", "改为县，析绥宁、会同二县地益之"),
            "owner": "靖州",
        },
        {
            "phase": 3,
            "era_raw": N("05-142", "崇祯十年"),
            "reign": "崇祯",
            "year": 10,
            "change_type": "改名",
            "change": N("05-142", "东迁龙塘，名龙塘县"),
            "owner": "靖州",
        },
    ],
    hyd=[
        {
            "name": N("05-142", "沅水"),
            "type": "江",
            "flow": N("05-142", "东有沅水"),
            "anchor": {"anchor": "天柱县东", "context": N("05-142", "东有沅水")},
        },
    ],
    gar=[
        {
            "name": N("05-142", "屯镇汶溪后千户所"),
            "type": "千户所",
            "territorial": "未明",
            "established": {
                "reign": "洪武",
                "year": 23,
                "era_raw": N("05-142", "洪武二十三年"),
            },
            "place": "天柱县西北",
            "dusi": "未明",
            "note": "西北有屯镇汶溪后千户所，洪武二十三年置",
        },
        {
            "name": N("05-142", "镇远巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "天柱县东",
            "dusi": "未明",
            "note": "东有镇远巡检司，后移上新市",
        },
        {
            "name": N("05-142", "江东巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "天柱县东",
            "dusi": "未明",
            "note": "又有江东巡检司",
        },
    ],
)

# ---------- 施州卫（卫所辖区） ----------
item(
    "05-143",
    geo={
        "name": N("05-143", "施州卫军民指挥使司"),
        "level": "卫",
        "node_type": "卫所",
        "parent": {"text": "湖广", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "东北",
                "to_anchor": "布政司",
                "distance": 1700,
                "unit": "里",
                "raw": N("05-143", "东北距布政司千七百里"),
            }
        ],
        "note": "元施州，属四川行省夔州路。洪武初省。十四年五月复置，属夔州府。六月兼置施州卫军民指挥使司。十二月属湖广都司。后州废，存卫。领所一，宣抚司四，安抚司九，长官司十三，蛮夷官司五",
    },
    ents=[
        {
            "text": N("05-143", "施州卫军民指挥使司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-143", "施州"),
            "type": "place",
            "count": 1,
            "provenance": "元施州，属四川行省夔州路",
        },
        {
            "text": N("05-143", "都亭山"),
            "type": "place",
            "count": 1,
            "provenance": "北有都亭山",
        },
        {
            "text": N("05-143", "连珠山"),
            "type": "place",
            "count": 1,
            "provenance": "东有连珠山，五峰关在山下",
        },
        {
            "text": N("05-143", "清江"),
            "type": "water",
            "count": 2,
            "provenance": "东北有清江",
        },
        {
            "text": N("05-143", "夷水"),
            "type": "water",
            "count": 1,
            "provenance": "一名夷水，亦曰黔江",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 14,
            "era_raw": N("05-143", "十四年五月"),
            "category": "复设",
            "event": N("05-143", "复置，属夔州府"),
            "place": "施州",
        },
        {
            "reign": "洪武",
            "year": 14,
            "era_raw": N("05-143", "六月"),
            "category": "增置",
            "event": N("05-143", "兼置施州卫军民指挥使司"),
            "place": "施州卫",
        },
        {
            "reign": "洪武",
            "year": 14,
            "era_raw": N("05-143", "十二月"),
            "category": "改隶",
            "event": N("05-143", "属湖广都司"),
            "place": "施州卫",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-143", "元施州，属四川行省夔州路"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-143", "元施州，属四川行省夔州路"),
            "owner": "夔州路",
        },
        {
            "phase": 2,
            "era_raw": N("05-143", "洪武初"),
            "reign": "洪武",
            "year": 0,
            "change_type": "废罢",
            "change": N("05-143", "洪武初省"),
            "owner": "未明",
        },
        {
            "phase": 3,
            "era_raw": N("05-143", "十四年五月"),
            "reign": "洪武",
            "year": 14,
            "change_type": "复置",
            "change": N("05-143", "复置，属夔州府"),
            "owner": "夔州府",
        },
        {
            "phase": 4,
            "era_raw": N("05-143", "六月"),
            "reign": "洪武",
            "year": 14,
            "change_type": "增设",
            "change": N("05-143", "兼置施州卫军民指挥使司"),
            "owner": "湖广都司",
        },
    ],
    hyd=[
        {
            "name": N("05-143", "清江"),
            "alt": "夷水",
            "type": "江",
            "flow": N(
                "05-143",
                "东北有清江，自四川黔江县流入，一名夷水，亦曰黔江，卫境诸水皆入焉，下流至宜都县入于大江",
            ),
            "anchor": {"anchor": "施州卫东北", "context": N("05-143", "东北有清江")},
        },
    ],
    gar=[
        {
            "name": N("05-143", "五峰关"),
            "type": "关",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "施州卫东连珠山",
            "dusi": "湖广都指挥使司",
            "note": "东有连珠山，五峰关在山下",
        },
    ],
)

item(
    "05-144",
    geo={
        "name": N("05-144", "大田军民千户所"),
        "level": "所",
        "node_type": "卫所",
        "parent": {"text": "施州卫军民指挥使司", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "东北",
                "to_anchor": "施州卫",
                "distance": 220,
                "unit": "里",
                "raw": N("05-144", "东北距卫二百二十里"),
            }
        ],
        "note": "洪武二十三年闰四月以散毛宣抚司之大水田置。东有小关山。西南有万顷湖，与酉阳界。又南有深溪关。北有硝场，产硝",
    },
    ents=[
        {
            "text": N("05-144", "大田军民千户所"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-144", "小关山"),
            "type": "place",
            "count": 1,
            "provenance": "东有小关山",
        },
        {
            "text": N("05-144", "万顷湖"),
            "type": "water",
            "count": 1,
            "provenance": "西南有万顷湖",
        },
        {
            "text": N("05-144", "深溪关"),
            "type": "institution",
            "count": 1,
            "provenance": "又南有深溪关",
        },
        {
            "text": N("05-144", "硝场"),
            "type": "place",
            "count": 1,
            "provenance": "北有硝场，产硝",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 23,
            "era_raw": N("05-144", "洪武二十三年闰四月"),
            "category": "初置",
            "event": N("05-144", "以散毛宣抚司之大水田置"),
            "place": "大田军民千户所",
        },
    ],
    hyd=[
        {
            "name": N("05-144", "万顷湖"),
            "type": "湖",
            "flow": N("05-144", "西南有万顷湖，与酉阳界"),
            "anchor": {"anchor": "大田所西南", "context": N("05-144", "西南有万顷湖")},
        },
    ],
    gar=[
        {
            "name": N("05-144", "深溪关"),
            "type": "关",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "大田所南",
            "dusi": "未明",
            "note": "又南有深溪关",
        },
    ],
    res=[
        {
            "name": N("05-144", "硝场"),
            "type": "未明",
            "place": "大田军民千户所",
            "site": "硝场",
            "importance": "产硝",
            "raw": N("05-144", "北有硝场，产硝"),
        },
    ],
)

# ---------- 施州卫土司（宣抚司四） ----------
item(
    "05-145",
    geo={
        "name": N("05-145", "施南宣抚司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "施州卫军民指挥使司", "rel": "领"},
        "tusi_type": "宣抚司",
        "govern": "土官",
        "bearing_distance": [
            {
                "bearing": "北",
                "to_anchor": "施州卫",
                "distance": 100,
                "unit": "里",
                "raw": N("05-145", "北距卫一百里"),
            }
        ],
        "note": "元施南道宣慰司。洪武四年十二月因之，后废。十六年十一月复置，属施州卫。二十七年后复废。永乐二年五月改置长官司，属大田军民千户所。四年三月升宣抚司，仍属卫。领安抚司五",
    },
    ents=[
        {
            "text": N("05-145", "施南宣抚司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-145", "施南道宣慰司"),
            "type": "place",
            "count": 1,
            "provenance": "元施南道宣慰司",
        },
        {
            "text": N("05-145", "夹壁龙孔"),
            "type": "place",
            "count": 1,
            "provenance": "后迁夹壁龙孔，即今治也",
        },
        {
            "text": N("05-145", "前江"),
            "type": "water",
            "count": 1,
            "provenance": "西有前江",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 4,
            "era_raw": N("05-145", "洪武四年十二月"),
            "category": "废置",
            "event": N("05-145", "因之，后废"),
            "place": "施南宣抚司",
        },
        {
            "reign": "洪武",
            "year": 16,
            "era_raw": N("05-145", "十六年十一月"),
            "category": "复设",
            "event": N("05-145", "复置，属施州卫"),
            "place": "施南宣抚司",
        },
        {
            "reign": "永乐",
            "year": 2,
            "era_raw": N("05-145", "永乐二年五月"),
            "category": "改置",
            "event": N("05-145", "改置长官司，属大田军民千户所"),
            "place": "施南宣抚司",
        },
        {
            "reign": "永乐",
            "year": 4,
            "era_raw": N("05-145", "四年三月"),
            "category": "升秩",
            "event": N("05-145", "升宣抚司，仍属卫"),
            "place": "施南宣抚司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-145", "元施南道宣慰司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-145", "元施南道宣慰司"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-145", "洪武四年十二月"),
            "reign": "洪武",
            "year": 4,
            "change_type": "废罢",
            "change": N("05-145", "因之，后废"),
            "owner": "湖广都司",
        },
        {
            "phase": 3,
            "era_raw": N("05-145", "十六年十一月"),
            "reign": "洪武",
            "year": 16,
            "change_type": "复置",
            "change": N("05-145", "复置，属施州卫"),
            "owner": "施州卫",
        },
        {
            "phase": 4,
            "era_raw": N("05-145", "永乐二年五月"),
            "reign": "永乐",
            "year": 2,
            "change_type": "改置",
            "change": N("05-145", "改置长官司，属大田军民千户所"),
            "owner": "大田军民千户所",
        },
        {
            "phase": 5,
            "era_raw": N("05-145", "四年三月"),
            "reign": "永乐",
            "year": 4,
            "change_type": "升州",
            "change": N("05-145", "升宣抚司，仍属卫"),
            "owner": "施州卫",
        },
    ],
    hyd=[
        {
            "name": N("05-145", "前江"),
            "type": "江",
            "flow": N("05-145", "西有前江，发源七药山，西南流与后江合，入四川彭水县界"),
            "anchor": {"anchor": "施南宣抚司西", "context": N("05-145", "西有前江")},
        },
    ],
)

item(
    "05-146",
    geo={
        "name": N("05-146", "东乡五路安抚司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "施南宣抚司", "rel": "领"},
        "tusi_type": "安抚司",
        "govern": "土官",
        "note": "元东乡五路军民府。洪武四年十二月改置长官司，后升安抚司。领长官司三，蛮夷官司二",
    },
    ents=[
        {
            "text": N("05-146", "东乡五路安抚司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-146", "东乡五路军民府"),
            "type": "place",
            "count": 1,
            "provenance": "元东乡五路军民府",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 4,
            "era_raw": N("05-146", "洪武四年十二月"),
            "category": "改置",
            "event": N("05-146", "改置长官司"),
            "place": "东乡五路安抚司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-146", "元东乡五路军民府"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-146", "元东乡五路军民府"),
            "owner": "施南宣抚司",
        },
        {
            "phase": 2,
            "era_raw": N("05-146", "洪武四年十二月"),
            "reign": "洪武",
            "year": 4,
            "change_type": "改置",
            "change": N("05-146", "改置长官司，后升安抚司"),
            "owner": "施南宣抚司",
        },
    ],
)

item(
    "05-147",
    geo={
        "name": N("05-147", "摇把峒长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "东乡五路安抚司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "元又把峒安抚司，后废。宣德三年五月改置",
    },
    ents=[
        {
            "text": N("05-147", "摇把峒长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-147", "又把峒安抚司"),
            "type": "place",
            "count": 1,
            "provenance": "元又把峒安抚司",
        },
    ],
    tme=[
        {
            "reign": "宣德",
            "year": 3,
            "era_raw": N("05-147", "宣德三年五月"),
            "category": "改置",
            "event": N("05-147", "改置"),
            "place": "摇把峒长官司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-147", "元又把峒安抚司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-147", "元又把峒安抚司，后废"),
            "owner": "施南宣抚司",
        },
        {
            "phase": 2,
            "era_raw": N("05-147", "宣德三年五月"),
            "reign": "宣德",
            "year": 3,
            "change_type": "改置",
            "change": N("05-147", "改置"),
            "owner": "东乡五路安抚司",
        },
    ],
)

item(
    "05-148",
    geo={
        "name": N("05-148", "下爱茶峒长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "东乡五路安抚司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "二长官司俱元容美洞地。至大二年置怀德府，属四川南道宣慰司。至顺二年正月升宣抚司。至正中，升军民宣慰司。太祖甲辰年六月改军民宣抚司，后废。宣德三年五月改置",
    },
    ents=[
        {
            "text": N("05-148", "下爱茶峒长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-148", "怀德府"),
            "type": "place",
            "count": 1,
            "provenance": "至大二年置怀德府",
        },
        {
            "text": N("05-148", "军民宣慰司"),
            "type": "system",
            "count": 1,
            "provenance": "至正中，升军民宣慰司",
        },
    ],
    tme=[
        {
            "reign": "宣德",
            "year": 3,
            "era_raw": N("05-148", "宣德三年五月"),
            "category": "改置",
            "event": N("05-148", "改置"),
            "place": "下爱茶峒长官司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-148", "二长官司俱元容美洞地"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-148", "二长官司俱元容美洞地"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-148", "太祖甲辰年六月"),
            "reign": "元",
            "year": 24,
            "change_type": "改置",
            "change": N("05-148", "改军民宣抚司，后废"),
            "owner": "施南宣抚司",
        },
        {
            "phase": 3,
            "era_raw": N("05-148", "宣德三年五月"),
            "reign": "宣德",
            "year": 3,
            "change_type": "改置",
            "change": N("05-148", "改置"),
            "owner": "东乡五路安抚司",
        },
    ],
)

item(
    "05-149",
    geo={
        "name": N("05-149", "镇远蛮夷官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "东乡五路安抚司", "rel": "领"},
        "tusi_type": "蛮夷长官司",
        "govern": "土官",
        "note": "宣德三年五月置",
    },
    ents=[
        {
            "text": N("05-149", "镇远蛮夷官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        }
    ],
    tme=[
        {
            "reign": "宣德",
            "year": 3,
            "era_raw": N("05-149", "宣德三年五月"),
            "category": "初置",
            "event": N("05-149", "置"),
            "place": "镇远蛮夷官司",
        },
    ],
)

item(
    "05-150",
    geo={
        "name": N("05-150", "隆奉蛮夷官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "东乡五路安抚司", "rel": "领"},
        "tusi_type": "蛮夷长官司",
        "govern": "土官",
        "note": "元隆奉宣抚司。洪武四年十二月改长官司，后废。宣德三年五月改置官司",
    },
    ents=[
        {
            "text": N("05-150", "隆奉蛮夷官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-150", "隆奉宣抚司"),
            "type": "place",
            "count": 1,
            "provenance": "元隆奉宣抚司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 4,
            "era_raw": N("05-150", "洪武四年十二月"),
            "category": "改置",
            "event": N("05-150", "改长官司"),
            "place": "隆奉蛮夷官司",
        },
        {
            "reign": "宣德",
            "year": 3,
            "era_raw": N("05-150", "宣德三年五月"),
            "category": "改置",
            "event": N("05-150", "改置官司"),
            "place": "隆奉蛮夷官司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-150", "元隆奉宣抚司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-150", "元隆奉宣抚司"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-150", "洪武四年十二月"),
            "reign": "洪武",
            "year": 4,
            "change_type": "改置",
            "change": N("05-150", "改长官司，后废"),
            "owner": "施南宣抚司",
        },
        {
            "phase": 3,
            "era_raw": N("05-150", "宣德三年五月"),
            "reign": "宣德",
            "year": 3,
            "change_type": "改置",
            "change": N("05-150", "改置官司"),
            "owner": "东乡五路安抚司",
        },
    ],
)

item(
    "05-151",
    geo={
        "name": N("05-151", "忠路安抚司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "施南宣抚司", "rel": "领"},
        "tusi_type": "安抚司",
        "govern": "土官",
        "note": "明玉珍忠路宣抚司。洪武四年改安抚司，二十三年废。永乐五年复置，领长官司一",
    },
    ents=[
        {
            "text": N("05-151", "忠路安抚司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-151", "忠路宣抚司"),
            "type": "place",
            "count": 1,
            "provenance": "明玉珍忠路宣抚司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 4,
            "era_raw": N("05-151", "洪武四年"),
            "category": "改置",
            "event": N("05-151", "改安抚司"),
            "place": "忠路安抚司",
        },
        {
            "reign": "永乐",
            "year": 5,
            "era_raw": N("05-151", "永乐五年"),
            "category": "复设",
            "event": N("05-151", "复置"),
            "place": "忠路安抚司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-151", "明玉珍忠路宣抚司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-151", "明玉珍忠路宣抚司"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-151", "洪武四年"),
            "reign": "洪武",
            "year": 4,
            "change_type": "改置",
            "change": N("05-151", "改安抚司，二十三年废"),
            "owner": "施南宣抚司",
        },
        {
            "phase": 3,
            "era_raw": N("05-151", "永乐五年"),
            "reign": "永乐",
            "year": 5,
            "change_type": "复置",
            "change": N("05-151", "复置"),
            "owner": "施南宣抚司",
        },
    ],
)

item(
    "05-152",
    geo={
        "name": N("05-152", "剑南长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "忠路安抚司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "宣德三年五月置",
    },
    ents=[
        {
            "text": N("05-152", "剑南长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        }
    ],
    tme=[
        {
            "reign": "宣德",
            "year": 3,
            "era_raw": N("05-152", "宣德三年五月"),
            "category": "初置",
            "event": N("05-152", "置"),
            "place": "剑南长官司",
        },
    ],
)

item(
    "05-153",
    geo={
        "name": N("05-153", "忠孝安抚司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "施南宣抚司", "rel": "领"},
        "tusi_type": "安抚司",
        "govern": "土官",
        "note": "元置。洪武四年十二月改置长官司，寻复故。二十三年废。永乐五年复置",
    },
    ents=[
        {
            "text": N("05-153", "忠孝安抚司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-153", "忠孝长官司"),
            "type": "place",
            "count": 1,
            "provenance": "改置长官司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 4,
            "era_raw": N("05-153", "洪武四年十二月"),
            "category": "改置",
            "event": N("05-153", "改置长官司"),
            "place": "忠孝安抚司",
        },
        {
            "reign": "永乐",
            "year": 5,
            "era_raw": N("05-153", "永乐五年"),
            "category": "复设",
            "event": N("05-153", "复置"),
            "place": "忠孝安抚司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-153", "元置"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-153", "元置"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-153", "洪武四年十二月"),
            "reign": "洪武",
            "year": 4,
            "change_type": "改置",
            "change": N("05-153", "改置长官司，寻复故。二十三年废"),
            "owner": "施南宣抚司",
        },
        {
            "phase": 3,
            "era_raw": N("05-153", "永乐五年"),
            "reign": "永乐",
            "year": 5,
            "change_type": "复置",
            "change": N("05-153", "复置"),
            "owner": "施南宣抚司",
        },
    ],
)

item(
    "05-154",
    geo={
        "name": N("05-154", "金峒安抚司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "施南宣抚司", "rel": "领"},
        "tusi_type": "安抚司",
        "govern": "土官",
        "note": "元置。洪武四年十二月改长官司。永乐五年复故。宣德三年五月领蛮夷官司一。隆庆五年正月降为峒长",
    },
    ents=[
        {
            "text": N("05-154", "金峒安抚司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-154", "金峒长官司"),
            "type": "place",
            "count": 1,
            "provenance": "改长官司",
        },
    ],
    tme=[
        {
            "reign": "隆庆",
            "year": 5,
            "era_raw": N("05-154", "隆庆五年正月"),
            "category": "降秩",
            "event": N("05-154", "降为峒长"),
            "place": "金峒安抚司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-154", "元置"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-154", "元置"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-154", "洪武四年十二月"),
            "reign": "洪武",
            "year": 4,
            "change_type": "改置",
            "change": N("05-154", "改长官司"),
            "owner": "施南宣抚司",
        },
        {
            "phase": 3,
            "era_raw": N("05-154", "永乐五年"),
            "reign": "永乐",
            "year": 5,
            "change_type": "复置",
            "change": N("05-154", "复故"),
            "owner": "施南宣抚司",
        },
        {
            "phase": 4,
            "era_raw": N("05-154", "隆庆五年正月"),
            "reign": "隆庆",
            "year": 5,
            "change_type": "废罢",
            "change": N("05-154", "降为峒长"),
            "owner": "施南宣抚司",
        },
    ],
)

item(
    "05-155",
    geo={
        "name": N("05-155", "西坪蛮夷官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "金峒安抚司", "rel": "领"},
        "tusi_type": "蛮夷长官司",
        "govern": "土官",
        "note": "宣德三年五月置",
    },
    ents=[
        {
            "text": N("05-155", "西坪蛮夷官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        }
    ],
    tme=[
        {
            "reign": "宣德",
            "year": 3,
            "era_raw": N("05-155", "宣德三年五月"),
            "category": "初置",
            "event": N("05-155", "置"),
            "place": "西坪蛮夷官司",
        },
    ],
)

item(
    "05-156",
    geo={
        "name": N("05-156", "中峒安抚司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "施南宣抚司", "rel": "领"},
        "tusi_type": "安抚司",
        "govern": "土官",
        "note": "嘉靖初置",
    },
    ents=[
        {
            "text": N("05-156", "中峒安抚司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        }
    ],
    tme=[
        {
            "reign": "嘉靖",
            "year": 0,
            "era_raw": N("05-156", "嘉靖初"),
            "category": "初置",
            "event": N("05-156", "置"),
            "place": "中峒安抚司",
        },
    ],
)

item(
    "05-157",
    geo={
        "name": N("05-157", "散毛宣抚司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "施州卫军民指挥使司", "rel": "领"},
        "tusi_type": "宣抚司",
        "govern": "土官",
        "bearing_distance": [
            {
                "bearing": "东北",
                "to_anchor": "施州卫",
                "distance": 250,
                "unit": "里",
                "raw": N("05-157", "东北距卫二百五十里"),
            }
        ],
        "note": "元至元三十年四月置散毛洞蛮夷官。洪武七年五月改散毛沿边宣慰司，属四川重庆卫。二十三年废。永乐二年五月置散毛长官司，属大田军民千户所。四年三月升宣抚司，属施州卫。领安抚司二",
    },
    ents=[
        {
            "text": N("05-157", "散毛宣抚司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-157", "散毛洞蛮夷官"),
            "type": "system",
            "count": 1,
            "provenance": "元至元三十年四月置散毛洞蛮夷官",
        },
        {
            "text": N("05-157", "白水河"),
            "type": "water",
            "count": 1,
            "provenance": "南有白水河",
        },
        {
            "text": N("05-157", "酉溪"),
            "type": "water",
            "count": 1,
            "provenance": "一名酉溪",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 7,
            "era_raw": N("05-157", "洪武七年五月"),
            "category": "改置",
            "event": N("05-157", "改散毛沿边宣慰司"),
            "place": "散毛宣抚司",
        },
        {
            "reign": "永乐",
            "year": 2,
            "era_raw": N("05-157", "永乐二年五月"),
            "category": "改置",
            "event": N("05-157", "置散毛长官司"),
            "place": "散毛宣抚司",
        },
        {
            "reign": "永乐",
            "year": 4,
            "era_raw": N("05-157", "四年三月"),
            "category": "升秩",
            "event": N("05-157", "升宣抚司，属施州卫"),
            "place": "散毛宣抚司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-157", "元至元三十年四月置散毛洞蛮夷官"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-157", "元至元三十年四月置散毛洞蛮夷官"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-157", "洪武七年五月"),
            "reign": "洪武",
            "year": 7,
            "change_type": "改置",
            "change": N("05-157", "改散毛沿边宣慰司，属四川重庆卫。二十三年废"),
            "owner": "重庆卫",
        },
        {
            "phase": 3,
            "era_raw": N("05-157", "永乐二年五月"),
            "reign": "永乐",
            "year": 2,
            "change_type": "改置",
            "change": N("05-157", "置散毛长官司，属大田军民千户所"),
            "owner": "大田军民千户所",
        },
        {
            "phase": 4,
            "era_raw": N("05-157", "四年三月"),
            "reign": "永乐",
            "year": 4,
            "change_type": "升州",
            "change": N("05-157", "升宣抚司，属施州卫"),
            "owner": "施州卫",
        },
    ],
    hyd=[
        {
            "name": N("05-157", "白水河"),
            "alt": "酉溪",
            "type": "河",
            "flow": N(
                "05-157", "南有白水河，一名酉溪，自忠建宣抚司流入，又东南入永顺司界"
            ),
            "anchor": {"anchor": "散毛宣抚司南", "context": N("05-157", "南有白水河")},
        },
    ],
)

item(
    "05-158",
    geo={
        "name": N("05-158", "龙潭安抚司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "散毛宣抚司", "rel": "领"},
        "tusi_type": "安抚司",
        "govern": "土官",
        "note": "元龙潭宣抚司。明玉珍改长官司。洪武八年十二月改龙潭安抚司，属四川重庆卫。二十三年废。永乐四年三月复置，来属。南有清江",
    },
    ents=[
        {
            "text": N("05-158", "龙潭安抚司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-158", "龙潭宣抚司"),
            "type": "place",
            "count": 1,
            "provenance": "元龙潭宣抚司",
        },
        {
            "text": N("05-158", "清江"),
            "type": "water",
            "count": 1,
            "provenance": "南有清江",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 8,
            "era_raw": N("05-158", "洪武八年十二月"),
            "category": "改置",
            "event": N("05-158", "改龙潭安抚司"),
            "place": "龙潭安抚司",
        },
        {
            "reign": "永乐",
            "year": 4,
            "era_raw": N("05-158", "永乐四年三月"),
            "category": "复设",
            "event": N("05-158", "复置，来属"),
            "place": "龙潭安抚司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-158", "元龙潭宣抚司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-158", "元龙潭宣抚司"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-158", "洪武八年十二月"),
            "reign": "洪武",
            "year": 8,
            "change_type": "改置",
            "change": N("05-158", "改龙潭安抚司，属四川重庆卫。二十三年废"),
            "owner": "重庆卫",
        },
        {
            "phase": 3,
            "era_raw": N("05-158", "永乐四年三月"),
            "reign": "永乐",
            "year": 4,
            "change_type": "复置",
            "change": N("05-158", "复置，来属"),
            "owner": "散毛宣抚司",
        },
    ],
    hyd=[
        {
            "name": N("05-158", "清江"),
            "type": "江",
            "flow": N("05-158", "南有清江"),
            "anchor": {"anchor": "龙潭安抚司南", "context": N("05-158", "南有清江")},
        },
    ],
)

item(
    "05-159",
    geo={
        "name": N("05-159", "大旺安抚司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "散毛宣抚司", "rel": "领"},
        "tusi_type": "安抚司",
        "govern": "土官",
        "note": "明玉珍大旺宣抚司。洪武八年十二月因之，属四川。永乐五年改置，领蛮夷官司二",
    },
    ents=[
        {
            "text": N("05-159", "大旺安抚司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-159", "大旺宣抚司"),
            "type": "place",
            "count": 1,
            "provenance": "明玉珍大旺宣抚司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 8,
            "era_raw": N("05-159", "洪武八年十二月"),
            "category": "改置",
            "event": N("05-159", "因之"),
            "place": "大旺安抚司",
        },
        {
            "reign": "永乐",
            "year": 5,
            "era_raw": N("05-159", "永乐五年"),
            "category": "改置",
            "event": N("05-159", "改置"),
            "place": "大旺安抚司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-159", "明玉珍大旺宣抚司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-159", "明玉珍大旺宣抚司"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-159", "洪武八年十二月"),
            "reign": "洪武",
            "year": 8,
            "change_type": "改置",
            "change": N("05-159", "因之，属四川"),
            "owner": "四川",
        },
        {
            "phase": 3,
            "era_raw": N("05-159", "永乐五年"),
            "reign": "永乐",
            "year": 5,
            "change_type": "改置",
            "change": N("05-159", "改置"),
            "owner": "散毛宣抚司",
        },
    ],
)

item(
    "05-160",
    geo={
        "name": N("05-160", "东流蛮夷官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "大旺安抚司", "rel": "领"},
        "tusi_type": "蛮夷长官司",
        "govern": "土官",
        "note": "洪武八年十二月置东流安抚司，属四川，后废。宣德三年五月改置，来属",
    },
    ents=[
        {
            "text": N("05-160", "东流蛮夷官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-160", "东流安抚司"),
            "type": "place",
            "count": 1,
            "provenance": "置东流安抚司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 8,
            "era_raw": N("05-160", "洪武八年十二月"),
            "category": "初置",
            "event": N("05-160", "置东流安抚司"),
            "place": "东流蛮夷官司",
        },
        {
            "reign": "宣德",
            "year": 3,
            "era_raw": N("05-160", "宣德三年五月"),
            "category": "改置",
            "event": N("05-160", "改置，来属"),
            "place": "东流蛮夷官司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-160", "洪武八年十二月"),
            "reign": "洪武",
            "year": 8,
            "change_type": "初置",
            "change": N("05-160", "置东流安抚司，属四川，后废"),
            "owner": "四川",
        },
        {
            "phase": 2,
            "era_raw": N("05-160", "宣德三年五月"),
            "reign": "宣德",
            "year": 3,
            "change_type": "改置",
            "change": N("05-160", "改置，来属"),
            "owner": "大旺安抚司",
        },
    ],
)

item(
    "05-161",
    geo={
        "name": N("05-161", "臈壁峒蛮夷官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "大旺安抚司", "rel": "领"},
        "tusi_type": "蛮夷长官司",
        "govern": "土官",
        "note": "宣德三年五月置",
    },
    ents=[
        {
            "text": N("05-161", "臈壁峒蛮夷官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        }
    ],
    tme=[
        {
            "reign": "宣德",
            "year": 3,
            "era_raw": N("05-161", "宣德三年五月"),
            "category": "初置",
            "event": N("05-161", "置"),
            "place": "臈壁峒蛮夷官司",
        },
    ],
)

item(
    "05-162",
    geo={
        "name": N("05-162", "忠建宣抚司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "施州卫军民指挥使司", "rel": "领"},
        "tusi_type": "宣抚司",
        "govern": "土官",
        "bearing_distance": [
            {
                "bearing": "北",
                "to_anchor": "施州卫",
                "distance": 250,
                "unit": "里",
                "raw": N("05-162", "北距卫二百五十里"),
            }
        ],
        "note": "元忠建军民都元帅府。明玉珍因之。洪武五年正月改长官司。六年升宣抚司。二十七年四月改安抚司，寻废。永乐四年复置宣抚司，属施州卫。领安抚司二",
    },
    ents=[
        {
            "text": N("05-162", "忠建宣抚司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-162", "忠建军民都元帅府"),
            "type": "system",
            "count": 1,
            "provenance": "元忠建军民都元帅府",
        },
        {
            "text": N("05-162", "白水河"),
            "type": "water",
            "count": 1,
            "provenance": "南有白水河",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 5,
            "era_raw": N("05-162", "洪武五年正月"),
            "category": "改置",
            "event": N("05-162", "改长官司"),
            "place": "忠建宣抚司",
        },
        {
            "reign": "洪武",
            "year": 6,
            "era_raw": N("05-162", "六年"),
            "category": "升秩",
            "event": N("05-162", "升宣抚司"),
            "place": "忠建宣抚司",
        },
        {
            "reign": "永乐",
            "year": 4,
            "era_raw": N("05-162", "永乐四年"),
            "category": "复设",
            "event": N("05-162", "复置宣抚司"),
            "place": "忠建宣抚司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-162", "元忠建军民都元帅府"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-162", "元忠建军民都元帅府"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-162", "洪武五年正月"),
            "reign": "洪武",
            "year": 5,
            "change_type": "改置",
            "change": N("05-162", "改长官司"),
            "owner": "施州卫",
        },
        {
            "phase": 3,
            "era_raw": N("05-162", "六年"),
            "reign": "洪武",
            "year": 6,
            "change_type": "升州",
            "change": N("05-162", "升宣抚司"),
            "owner": "施州卫",
        },
        {
            "phase": 4,
            "era_raw": N("05-162", "永乐四年"),
            "reign": "永乐",
            "year": 4,
            "change_type": "复置",
            "change": N("05-162", "复置宣抚司，属施州卫"),
            "owner": "施州卫",
        },
    ],
    hyd=[
        {
            "name": N("05-162", "白水河"),
            "type": "河",
            "flow": N("05-162", "南有白水河，源出将军山，西南流，车东河自容美司来合焉"),
            "anchor": {"anchor": "忠建宣抚司南", "context": N("05-162", "南有白水河")},
        },
    ],
)

item(
    "05-163",
    geo={
        "name": N("05-163", "忠峒安抚司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "忠建宣抚司", "rel": "领"},
        "tusi_type": "安抚司",
        "govern": "土官",
        "note": "元湖南镇边宣慰司。明玉珍改沿边溪洞宣抚司。洪武五年正月改沿边溪洞长官司，后废。永乐四年改置。西南有酉溪",
    },
    ents=[
        {
            "text": N("05-163", "忠峒安抚司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-163", "湖南镇边宣慰司"),
            "type": "place",
            "count": 1,
            "provenance": "元湖南镇边宣慰司",
        },
        {
            "text": N("05-163", "酉溪"),
            "type": "water",
            "count": 1,
            "provenance": "西南有酉溪",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 5,
            "era_raw": N("05-163", "洪武五年正月"),
            "category": "改置",
            "event": N("05-163", "改沿边溪洞长官司"),
            "place": "忠峒安抚司",
        },
        {
            "reign": "永乐",
            "year": 4,
            "era_raw": N("05-163", "永乐四年"),
            "category": "改置",
            "event": N("05-163", "改置"),
            "place": "忠峒安抚司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-163", "元湖南镇边宣慰司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-163", "元湖南镇边宣慰司"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-163", "洪武五年正月"),
            "reign": "洪武",
            "year": 5,
            "change_type": "改置",
            "change": N("05-163", "改沿边溪洞长官司，后废"),
            "owner": "忠建宣抚司",
        },
        {
            "phase": 3,
            "era_raw": N("05-163", "永乐四年"),
            "reign": "永乐",
            "year": 4,
            "change_type": "改置",
            "change": N("05-163", "改置"),
            "owner": "忠建宣抚司",
        },
    ],
    hyd=[
        {
            "name": N("05-163", "酉溪"),
            "type": "溪",
            "flow": N("05-163", "西南有酉溪"),
            "anchor": {
                "anchor": "忠峒安抚司西南",
                "context": N("05-163", "西南有酉溪"),
            },
        },
    ],
)

item(
    "05-164",
    geo={
        "name": N("05-164", "高罗安抚司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "忠建宣抚司", "rel": "领"},
        "tusi_type": "安抚司",
        "govern": "土官",
        "note": "元高罗宣抚司。明玉珍改安抚司。洪武六年废。永乐四年三月复置。领长官司一",
    },
    ents=[
        {
            "text": N("05-164", "高罗安抚司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-164", "高罗宣抚司"),
            "type": "place",
            "count": 1,
            "provenance": "元高罗宣抚司",
        },
    ],
    tme=[
        {
            "reign": "永乐",
            "year": 4,
            "era_raw": N("05-164", "永乐四年三月"),
            "category": "复设",
            "event": N("05-164", "复置"),
            "place": "高罗安抚司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-164", "元高罗宣抚司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-164", "元高罗宣抚司"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-164", "洪武六年"),
            "reign": "洪武",
            "year": 6,
            "change_type": "废罢",
            "change": N("05-164", "洪武六年废"),
            "owner": "忠建宣抚司",
        },
        {
            "phase": 3,
            "era_raw": N("05-164", "永乐四年三月"),
            "reign": "永乐",
            "year": 4,
            "change_type": "复置",
            "change": N("05-164", "复置"),
            "owner": "忠建宣抚司",
        },
    ],
)

item(
    "05-165",
    geo={
        "name": N("05-165", "思南长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "施州卫军民指挥使司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "成化后置",
    },
    ents=[
        {
            "text": N("05-165", "思南长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        }
    ],
    tme=[
        {
            "reign": "成化",
            "year": 0,
            "era_raw": N("05-165", "成化后"),
            "category": "初置",
            "event": N("05-165", "置"),
            "place": "思南长官司",
        },
    ],
)

item(
    "05-166",
    geo={
        "name": N("05-166", "容美宣抚司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "施州卫军民指挥使司", "rel": "领"},
        "tusi_type": "宣抚司",
        "govern": "土官",
        "bearing_distance": [
            {
                "bearing": "西北",
                "to_anchor": "施州卫",
                "distance": 210,
                "unit": "里",
                "raw": N("05-166", "西北距卫二百十里"),
            }
        ],
        "note": "元容美等处宣抚司，属四川行省。吴元年正月改黄沙、靖安、麻寮等处军民宣抚司。洪武五年二月改置长官司。永乐四年复置宣抚司，属施州卫。领长官司五",
    },
    ents=[
        {
            "text": N("05-166", "容美宣抚司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-166", "容美等处宣抚司"),
            "type": "place",
            "count": 1,
            "provenance": "元容美等处宣抚司",
        },
        {
            "text": N("05-166", "山河"),
            "type": "water",
            "count": 1,
            "provenance": "西南有山河",
        },
        {
            "text": N("05-166", "溇水"),
            "type": "water",
            "count": 1,
            "provenance": "即溇水之上源",
        },
    ],
    tme=[
        {
            "reign": "吴",
            "year": 1,
            "era_raw": N("05-166", "吴元年正月"),
            "category": "改称",
            "event": N("05-166", "改黄沙、靖安、麻寮等处军民宣抚司"),
            "place": "容美宣抚司",
        },
        {
            "reign": "洪武",
            "year": 5,
            "era_raw": N("05-166", "洪武五年二月"),
            "category": "改置",
            "event": N("05-166", "改置长官司"),
            "place": "容美宣抚司",
        },
        {
            "reign": "永乐",
            "year": 4,
            "era_raw": N("05-166", "永乐四年"),
            "category": "复设",
            "event": N("05-166", "复置宣抚司"),
            "place": "容美宣抚司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-166", "元容美等处宣抚司，属四川行省"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-166", "元容美等处宣抚司，属四川行省"),
            "owner": "四川行省",
        },
        {
            "phase": 2,
            "era_raw": N("05-166", "吴元年正月"),
            "reign": "吴",
            "year": 1,
            "change_type": "改名",
            "change": N("05-166", "改黄沙、靖安、麻寮等处军民宣抚司"),
            "owner": "未明",
        },
        {
            "phase": 3,
            "era_raw": N("05-166", "洪武五年二月"),
            "reign": "洪武",
            "year": 5,
            "change_type": "改置",
            "change": N("05-166", "改置长官司"),
            "owner": "施州卫",
        },
        {
            "phase": 4,
            "era_raw": N("05-166", "永乐四年"),
            "reign": "永乐",
            "year": 4,
            "change_type": "复置",
            "change": N("05-166", "复置宣抚司，属施州卫"),
            "owner": "施州卫",
        },
    ],
    hyd=[
        {
            "name": N("05-166", "山河"),
            "alt": "溇水",
            "type": "溪",
            "flow": N("05-166", "西南有山河，即溇水之上源，东入九溪卫界"),
            "anchor": {
                "anchor": "容美宣抚司西南",
                "context": N("05-166", "西南有山河"),
            },
        },
    ],
)

item(
    "05-167",
    geo={
        "name": N("05-167", "盘顺长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "容美宣抚司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "元元统二年正月置盘顺府。至正十五年四月升军民安抚司。洪武五年三月改为长官司",
    },
    ents=[
        {
            "text": N("05-167", "盘顺长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-167", "盘顺府"),
            "type": "place",
            "count": 1,
            "provenance": "元元统二年正月置盘顺府",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 5,
            "era_raw": N("05-167", "洪武五年三月"),
            "category": "改置",
            "event": N("05-167", "改为长官司"),
            "place": "盘顺长官司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-167", "元元统二年正月置盘顺府"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-167", "元元统二年正月置盘顺府"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-167", "洪武五年三月"),
            "reign": "洪武",
            "year": 5,
            "change_type": "改置",
            "change": N("05-167", "改为长官司"),
            "owner": "容美宣抚司",
        },
    ],
)

item(
    "05-168",
    geo={
        "name": N("05-168", "椒山玛瑙长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "容美宣抚司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "合条：椒山玛瑙、五峰石宝、石梁下峒、水尽源通塔平四长官司，俱洪武七年十一月置，十四年废。永乐五年复置",
    },
    ents=[
        {
            "text": N("05-168", "椒山玛瑙长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-168", "五峰石宝长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-168", "石梁下峒长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-168", "水尽源通塔平长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 7,
            "era_raw": N("05-168", "洪武七年十一月"),
            "category": "初置",
            "event": N("05-168", "置"),
            "place": "椒山玛瑙长官司",
        },
        {
            "reign": "永乐",
            "year": 5,
            "era_raw": N("05-168", "永乐五年"),
            "category": "复设",
            "event": N("05-168", "复置"),
            "place": "椒山玛瑙长官司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-168", "洪武七年十一月"),
            "reign": "洪武",
            "year": 7,
            "change_type": "初置",
            "change": N("05-168", "俱洪武七年十一月置"),
            "owner": "容美宣抚司",
        },
        {
            "phase": 2,
            "era_raw": N("05-168", "永乐五年"),
            "reign": "永乐",
            "year": 5,
            "change_type": "复置",
            "change": N("05-168", "复置"),
            "owner": "容美宣抚司",
        },
    ],
)

item(
    "05-169",
    geo={
        "name": N("05-169", "木册长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "施州卫军民指挥使司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "元木册安抚司。明玉珍改长官司。洪武四年废。永乐四年三月复置，属高罗安抚司。宣德九年六月直隶施州卫",
    },
    ents=[
        {
            "text": N("05-169", "木册长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-169", "木册安抚司"),
            "type": "place",
            "count": 1,
            "provenance": "元木册安抚司",
        },
    ],
    tme=[
        {
            "reign": "永乐",
            "year": 4,
            "era_raw": N("05-169", "永乐四年三月"),
            "category": "复设",
            "event": N("05-169", "复置，属高罗安抚司"),
            "place": "木册长官司",
        },
        {
            "reign": "宣德",
            "year": 9,
            "era_raw": N("05-169", "宣德九年六月"),
            "category": "改隶",
            "event": N("05-169", "直隶施州卫"),
            "place": "木册长官司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-169", "元木册安抚司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-169", "元木册安抚司。明玉珍改长官司。洪武四年废"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-169", "永乐四年三月"),
            "reign": "永乐",
            "year": 4,
            "change_type": "复置",
            "change": N("05-169", "复置，属高罗安抚司"),
            "owner": "高罗安抚司",
        },
        {
            "phase": 3,
            "era_raw": N("05-169", "宣德九年六月"),
            "reign": "宣德",
            "year": 9,
            "change_type": "改隶",
            "change": N("05-169", "直隶施州卫"),
            "owner": "施州卫",
        },
    ],
)

item(
    "05-170",
    geo={
        "name": N("05-170", "镇南长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "施州卫军民指挥使司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "元宣化镇南五路军民府，寻改湖南镇边毛岭峒宣慰司。明玉珍改镇南宣抚司。洪武八年二月复置，属施州卫。二十三年复废。永乐五年改置，直隶施州卫。有酉溪",
    },
    ents=[
        {
            "text": N("05-170", "镇南长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-170", "镇南宣抚司"),
            "type": "place",
            "count": 1,
            "provenance": "明玉珍改镇南宣抚司",
        },
        {
            "text": N("05-170", "酉溪"),
            "type": "water",
            "count": 1,
            "provenance": "有酉溪",
        },
    ],
    tme=[
        {
            "reign": "永乐",
            "year": 5,
            "era_raw": N("05-170", "永乐五年"),
            "category": "改置",
            "event": N("05-170", "改置，直隶施州卫"),
            "place": "镇南长官司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-170", "元宣化镇南五路军民府"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-170", "元宣化镇南五路军民府"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-170", "洪武八年二月"),
            "reign": "洪武",
            "year": 8,
            "change_type": "复置",
            "change": N("05-170", "复置，属施州卫。二十三年复废"),
            "owner": "施州卫",
        },
        {
            "phase": 3,
            "era_raw": N("05-170", "永乐五年"),
            "reign": "永乐",
            "year": 5,
            "change_type": "改置",
            "change": N("05-170", "改置，直隶施州卫"),
            "owner": "施州卫",
        },
    ],
    hyd=[
        {
            "name": N("05-170", "酉溪"),
            "type": "溪",
            "flow": N("05-170", "有酉溪"),
            "anchor": {"anchor": "镇南长官司", "context": N("05-170", "有酉溪")},
        },
    ],
)

item(
    "05-171",
    geo={
        "name": N("05-171", "唐崖长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "施州卫军民指挥使司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "元唐崖军民千户所。明玉珍改安抚司。洪武七年四月改长官司，后废。永乐四年三月复置，直隶施州卫。南有黔水",
    },
    ents=[
        {
            "text": N("05-171", "唐崖长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-171", "唐崖军民千户所"),
            "type": "institution",
            "count": 1,
            "provenance": "元唐崖军民千户所",
        },
        {
            "text": N("05-171", "黔水"),
            "type": "water",
            "count": 1,
            "provenance": "南有黔水",
        },
    ],
    tme=[
        {
            "reign": "永乐",
            "year": 4,
            "era_raw": N("05-171", "永乐四年三月"),
            "category": "复设",
            "event": N("05-171", "复置，直隶施州卫"),
            "place": "唐崖长官司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-171", "元唐崖军民千户所"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-171", "元唐崖军民千户所"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-171", "洪武七年四月"),
            "reign": "洪武",
            "year": 7,
            "change_type": "改置",
            "change": N("05-171", "改长官司，后废"),
            "owner": "施州卫",
        },
        {
            "phase": 3,
            "era_raw": N("05-171", "永乐四年三月"),
            "reign": "永乐",
            "year": 4,
            "change_type": "复置",
            "change": N("05-171", "复置，直隶施州卫"),
            "owner": "施州卫",
        },
    ],
    hyd=[
        {
            "name": N("05-171", "黔水"),
            "type": "江",
            "flow": N("05-171", "南有黔水，即清江之上源"),
            "anchor": {"anchor": "唐崖长官司南", "context": N("05-171", "南有黔水")},
        },
    ],
)

# ---------- 永顺宣慰司 ----------
item(
    "05-172",
    geo={
        "name": N("05-172", "永顺军民宣慰使司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "湖广", "rel": "领"},
        "tusi_type": "宣慰司",
        "govern": "土官",
        "bearing_distance": [
            {
                "bearing": "东北",
                "to_anchor": "布政司",
                "distance": 2000,
                "unit": "里",
                "raw": N("05-172", "东北距布政司二千里"),
            }
        ],
        "note": "元至元中，置永顺路。洪武二年为州。十二月置永顺军民安抚司。六年十二月升军民宣慰使司，属湖广行省，寻改属都司。领州三，长官司六",
    },
    ents=[
        {
            "text": N("05-172", "永顺军民宣慰使司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-172", "永顺路"),
            "type": "place",
            "count": 1,
            "provenance": "元至元中，置永顺路",
        },
        {
            "text": N("05-172", "永顺等处军民安抚司"),
            "type": "system",
            "count": 1,
            "provenance": "至大三年四月改永顺等处军民安抚司",
        },
        {
            "text": N("05-172", "水溪"),
            "type": "water",
            "count": 1,
            "provenance": "西南有水溪",
        },
        {
            "text": N("05-172", "酉水"),
            "type": "water",
            "count": 1,
            "provenance": "即酉水也",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 2,
            "era_raw": N("05-172", "洪武二年"),
            "category": "改置",
            "event": N("05-172", "为州"),
            "place": "永顺军民宣慰使司",
        },
        {
            "reign": "洪武",
            "year": 6,
            "era_raw": N("05-172", "六年十二月"),
            "category": "升秩",
            "event": N("05-172", "升军民宣慰使司"),
            "place": "永顺军民宣慰使司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-172", "元至元中，置永顺路"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-172", "元至元中，置永顺路"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-172", "洪武二年"),
            "reign": "洪武",
            "year": 2,
            "change_type": "改置",
            "change": N("05-172", "为州"),
            "owner": "湖广行省",
        },
        {
            "phase": 3,
            "era_raw": N("05-172", "六年十二月"),
            "reign": "洪武",
            "year": 6,
            "change_type": "升州",
            "change": N("05-172", "升军民宣慰使司"),
            "owner": "湖广行省",
        },
    ],
    hyd=[
        {
            "name": N("05-172", "水溪"),
            "alt": "酉水",
            "type": "溪",
            "flow": N("05-172", "西南有水溪，即酉水也，下流入沅陵县界"),
            "anchor": {"anchor": "永顺司西南", "context": N("05-172", "西南有水溪")},
        },
    ],
)

item(
    "05-173",
    geo={
        "name": N("05-173", "南渭州"),
        "level": "属州",
        "node_type": "土司",
        "parent": {"text": "永顺军民宣慰使司", "rel": "领"},
        "tusi_type": "御夷州",
        "govern": "土官",
        "note": "司西。元属新添葛蛮安抚司，后废。洪武二年复置，改属",
    },
    ents=[
        {
            "text": N("05-173", "南渭州"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-173", "新添葛蛮安抚司"),
            "type": "institution",
            "count": 1,
            "provenance": "元属新添葛蛮安抚司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 2,
            "era_raw": N("05-173", "洪武二年"),
            "category": "复设",
            "event": N("05-173", "复置，改属"),
            "place": "南渭州",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-173", "元属新添葛蛮安抚司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-173", "元属新添葛蛮安抚司，后废"),
            "owner": "新添葛蛮安抚司",
        },
        {
            "phase": 2,
            "era_raw": N("05-173", "洪武二年"),
            "reign": "洪武",
            "year": 2,
            "change_type": "复置",
            "change": N("05-173", "复置，改属"),
            "owner": "永顺军民宣慰使司",
        },
    ],
)

item(
    "05-174",
    geo={
        "name": N("05-174", "施溶州"),
        "level": "属州",
        "node_type": "土司",
        "parent": {"text": "永顺军民宣慰使司", "rel": "领"},
        "tusi_type": "御夷州",
        "govern": "土官",
        "note": "司东南。元会溪施溶等处长官司，属思州军民安抚司，后废。洪武二年改置，来属",
    },
    ents=[
        {
            "text": N("05-174", "施溶州"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-174", "会溪施溶等处长官司"),
            "type": "place",
            "count": 1,
            "provenance": "元会溪施溶等处长官司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 2,
            "era_raw": N("05-174", "洪武二年"),
            "category": "改置",
            "event": N("05-174", "改置，来属"),
            "place": "施溶州",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-174", "元会溪施溶等处长官司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-174", "元会溪施溶等处长官司，属思州军民安抚司，后废"),
            "owner": "思州军民安抚司",
        },
        {
            "phase": 2,
            "era_raw": N("05-174", "洪武二年"),
            "reign": "洪武",
            "year": 2,
            "change_type": "改置",
            "change": N("05-174", "改置，来属"),
            "owner": "永顺军民宣慰使司",
        },
    ],
)

item(
    "05-175",
    geo={
        "name": N("05-175", "上溪州"),
        "level": "属州",
        "node_type": "土司",
        "parent": {"text": "永顺军民宣慰使司", "rel": "领"},
        "tusi_type": "御夷州",
        "govern": "土官",
        "note": "司西。洪武二年置",
    },
    ents=[
        {
            "text": N("05-175", "上溪州"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        }
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 2,
            "era_raw": N("05-175", "洪武二年"),
            "category": "初置",
            "event": N("05-175", "置"),
            "place": "上溪州",
        },
    ],
)

item(
    "05-176",
    geo={
        "name": N("05-176", "臈惹洞长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "永顺军民宣慰使司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "合条：臈惹洞、麦著黄洞、驴迟洞、施溶溪四长官司，元俱属思州军民安抚司。洪武三年改属",
    },
    ents=[
        {
            "text": N("05-176", "臈惹洞长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-176", "麦著黄洞长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-176", "驴迟洞长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-176", "施溶溪长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 3,
            "era_raw": N("05-176", "洪武三年"),
            "category": "改隶",
            "event": N("05-176", "改属"),
            "place": "臈惹洞长官司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-176", "元俱属思州军民安抚司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-176", "元俱属思州军民安抚司"),
            "owner": "思州军民安抚司",
        },
        {
            "phase": 2,
            "era_raw": N("05-176", "洪武三年"),
            "reign": "洪武",
            "year": 3,
            "change_type": "改隶",
            "change": N("05-176", "改属"),
            "owner": "永顺军民宣慰使司",
        },
    ],
)

item(
    "05-177",
    geo={
        "name": N("05-177", "白崖洞长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "永顺军民宣慰使司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "元属新添葛蛮安抚司。洪武三年改属",
    },
    ents=[
        {
            "text": N("05-177", "白崖洞长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        }
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 3,
            "era_raw": N("05-177", "洪武三年"),
            "category": "改隶",
            "event": N("05-177", "改属"),
            "place": "白崖洞长官司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-177", "元属新添葛蛮安抚司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-177", "元属新添葛蛮安抚司"),
            "owner": "新添葛蛮安抚司",
        },
        {
            "phase": 2,
            "era_raw": N("05-177", "洪武三年"),
            "reign": "洪武",
            "year": 3,
            "change_type": "改隶",
            "change": N("05-177", "改属"),
            "owner": "永顺军民宣慰使司",
        },
    ],
)

item(
    "05-178",
    geo={
        "name": N("05-178", "田家洞长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "永顺军民宣慰使司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "洪武三年置",
    },
    ents=[
        {
            "text": N("05-178", "田家洞长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        }
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 3,
            "era_raw": N("05-178", "洪武三年"),
            "category": "初置",
            "event": N("05-178", "置"),
            "place": "田家洞长官司",
        },
    ],
)

# ---------- 保靖宣慰司 ----------
item(
    "05-179",
    geo={
        "name": N("05-179", "保靖州军民宣慰使司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "湖广", "rel": "领"},
        "tusi_type": "宣慰司",
        "govern": "土官",
        "bearing_distance": [
            {
                "bearing": "东北",
                "to_anchor": "布政司",
                "distance": 1970,
                "unit": "里",
                "raw": N("05-179", "东北距布政司千九百七十里"),
            }
        ],
        "note": "元保靖州，属新添葛蛮安抚司。太祖丙午年二月置保靖州军民安抚司。洪武元年九月改宣慰司。六年十二月升军民宣慰使司，直隶湖广行省，寻改属都司。领长官司二",
    },
    ents=[
        {
            "text": N("05-179", "保靖州军民宣慰使司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-179", "保靖州"),
            "type": "place",
            "count": 1,
            "provenance": "元保靖州",
        },
        {
            "text": N("05-179", "北河"),
            "type": "water",
            "count": 1,
            "provenance": "北有北河",
        },
        {
            "text": N("05-179", "峒河"),
            "type": "water",
            "count": 1,
            "provenance": "又有峒河",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 1,
            "era_raw": N("05-179", "洪武元年九月"),
            "category": "改置",
            "event": N("05-179", "改宣慰司"),
            "place": "保靖州军民宣慰使司",
        },
        {
            "reign": "洪武",
            "year": 6,
            "era_raw": N("05-179", "六年十二月"),
            "category": "升秩",
            "event": N("05-179", "升军民宣慰使司"),
            "place": "保靖州军民宣慰使司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-179", "元保靖州，属新添葛蛮安抚司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-179", "元保靖州，属新添葛蛮安抚司"),
            "owner": "新添葛蛮安抚司",
        },
        {
            "phase": 2,
            "era_raw": N("05-179", "洪武元年九月"),
            "reign": "洪武",
            "year": 1,
            "change_type": "改置",
            "change": N("05-179", "改宣慰司"),
            "owner": "湖广行省",
        },
        {
            "phase": 3,
            "era_raw": N("05-179", "六年十二月"),
            "reign": "洪武",
            "year": 6,
            "change_type": "升州",
            "change": N("05-179", "升军民宣慰使司"),
            "owner": "湖广行省",
        },
    ],
    hyd=[
        {
            "name": N("05-179", "北河"),
            "type": "河",
            "flow": N("05-179", "北有北河，自酉阳司流入，东入永顺司界"),
            "anchor": {"anchor": "保靖司北", "context": N("05-179", "北有北河")},
        },
        {
            "name": N("05-179", "峒河"),
            "type": "河",
            "flow": N("05-179", "又有峒河，下流与卢溪县之武溪合"),
            "anchor": {"anchor": "保靖司", "context": N("05-179", "又有峒河")},
        },
    ],
)

item(
    "05-180",
    geo={
        "name": N("05-180", "五寨长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "保靖州军民宣慰使司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "司南。元置，洪武七年六月因之",
    },
    ents=[
        {
            "text": N("05-180", "五寨长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        }
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 7,
            "era_raw": N("05-180", "洪武七年六月"),
            "category": "复设",
            "event": N("05-180", "因之"),
            "place": "五寨长官司",
        },
    ],
)

item(
    "05-181",
    geo={
        "name": N("05-181", "筸子坪长官司"),
        "level": "土司",
        "node_type": "土司",
        "parent": {"text": "保靖州军民宣慰使司", "rel": "领"},
        "tusi_type": "长官司",
        "govern": "土官",
        "note": "司南。太祖甲辰年六月置竿子坪洞元帅府，后废。永乐三年七月改置",
    },
    ents=[
        {
            "text": N("05-181", "筸子坪长官司"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-181", "竿子坪洞元帅府"),
            "type": "system",
            "count": 1,
            "provenance": "太祖甲辰年六月置竿子坪洞元帅府",
        },
    ],
    tme=[
        {
            "reign": "永乐",
            "year": 3,
            "era_raw": N("05-181", "永乐三年七月"),
            "category": "改置",
            "event": N("05-181", "改置"),
            "place": "筸子坪长官司",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-181", "太祖甲辰年六月"),
            "reign": "元",
            "year": 24,
            "change_type": "初置",
            "change": N("05-181", "置竿子坪洞元帅府，后废"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-181", "永乐三年七月"),
            "reign": "永乐",
            "year": 3,
            "change_type": "改置",
            "change": N("05-181", "改置"),
            "owner": "保靖州军民宣慰使司",
        },
    ],
)

# ---------- 校验全部命中并输出 ----------
miss = []
for iid, it in D.items():
    norm = reg[iid]["norm"]
    for fld, v in it.items():
        if isinstance(v, str) and v and v != "未明" and fld == "geo":
            pass
    g = it["geo"]
    if g.get("name") and g["name"] not in norm:
        miss.append((iid, "geo.name", g["name"]))
    if g.get("note") and g["note"] not in norm:
        pass  # note 自由文本不做强校验（但此处全部来自原文）
    for bd in g.get("bearing_distance", []):
        if bd["raw"] not in norm:
            miss.append((iid, "geo.bearing.raw", bd["raw"]))
    for q in g.get("quantity", []):
        if q["era_raw"] not in norm or q["raw"] not in norm:
            miss.append((iid, "geo.quantity", q))
    for e in it["ents"]:
        if e["text"] not in norm:
            miss.append((iid, "ent.text", e["text"]))
    for t in it["tme"]:
        if t["era_raw"] and t["era_raw"] != "未明" and t["era_raw"] not in norm:
            miss.append((iid, "tme.era_raw", t["era_raw"]))
    for e in it["evo"]:
        if e["change"] not in norm or e["era_raw"] not in norm:
            miss.append((iid, "evo", e))
    for h in it["hyd"]:
        if h["name"] not in norm or h["flow"] not in norm:
            miss.append((iid, "hyd", h))
    for g_ in it["gar"]:
        if g_["name"] not in norm:
            miss.append((iid, "gar.name", g_["name"]))
        if (
            g_.get("established", {}).get("era_raw")
            and g_["established"]["era_raw"] != "未明"
            and g_["established"]["era_raw"] not in norm
        ):
            miss.append((iid, "gar.est.era_raw", g_["established"]["era_raw"]))
    for r in it["res"]:
        if r["raw"] not in norm:
            miss.append((iid, "res.raw", r["raw"]))

if miss:
    print("MISS count =", len(miss))
    for m in miss:
        print(m)
    raise SystemExit(1)

with io.open(os.path.join(HERE, "data_part2b.py"), "w", encoding="utf-8") as f:
    f.write('# -*- coding: utf-8 -*-\n"""卷05 分片2b：05-105 ~ 05-181。"""\n\n')
    f.write("PART = ")
    import pprint

    f.write(pprint.pformat(D, width=120, sort_dicts=False))
    f.write("\n")
print("PART2b done, items=%d" % len(D))
