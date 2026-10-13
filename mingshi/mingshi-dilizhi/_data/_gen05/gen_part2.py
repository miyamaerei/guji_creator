# -*- coding: utf-8 -*-
"""卷05 分片2生成器：05-091 ~ 05-181。从 registry norm 校验逐字命中后输出 data_part2.py。"""

import io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
reg = json.load(io.open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))


def N(iid, s):
    norm = reg[iid]["norm"]
    if s not in norm:
        raise SystemExit("[%s] 未命中 norm: %r" % (iid, s))
    return s


# 条目数据。参考 norm 原文逐条编写，文本字段全部来自 norm。
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


# ---------- 长沙府尾 ----------
item(
    "05-091",
    geo={
        "name": N("05-091", "安化"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "长沙府", "rel": "领"},
        "note": "府西。东有浮泥山，有大峰山。西北有辰山，西有澬江。又南有善溪，自武陵县流注于澬江",
    },
    ents=[
        {
            "text": N("05-091", "安化"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-091", "浮泥山"),
            "type": "place",
            "count": 1,
            "provenance": "东有浮泥山",
        },
        {
            "text": N("05-091", "大峰山"),
            "type": "place",
            "count": 1,
            "provenance": "有大峰山",
        },
        {
            "text": N("05-091", "辰山"),
            "type": "place",
            "count": 1,
            "provenance": "西北有辰山",
        },
        {
            "text": N("05-091", "澬江"),
            "type": "water",
            "count": 3,
            "provenance": "西有澬江",
        },
        {
            "text": N("05-091", "善溪"),
            "type": "water",
            "count": 1,
            "provenance": "又南有善溪，自武陵县流注于澬江",
        },
    ],
    hyd=[
        {
            "name": N("05-091", "澬江"),
            "type": "江",
            "flow": N("05-091", "西有澬江"),
            "anchor": {"anchor": "安化县西", "context": N("05-091", "西有澬江")},
        },
        {
            "name": N("05-091", "善溪"),
            "type": "溪",
            "flow": N("05-091", "又南有善溪，自武陵县流注于澬江"),
            "anchor": {"anchor": "安化县南", "context": N("05-091", "又南有善溪")},
        },
    ],
)

item(
    "05-092",
    geo={
        "name": N("05-092", "茶陵州"),
        "level": "属州",
        "node_type": "政区",
        "parent": {"text": "长沙府", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "北",
                "to_anchor": "长沙府",
                "distance": 450,
                "unit": "里",
                "raw": N("05-092", "北距府四百五十里"),
            }
        ],
        "note": "元直隶湖南道。太祖甲辰年降为县。成化十八年十月复为州。西有云阳山。东有视渡口巡检司",
    },
    ents=[
        {
            "text": N("05-092", "茶陵州"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-092", "湖南道"),
            "type": "institution",
            "count": 1,
            "provenance": "元直隶湖南道",
        },
        {
            "text": N("05-092", "云阳山"),
            "type": "place",
            "count": 1,
            "provenance": "西有云阳山",
        },
        {
            "text": N("05-092", "洣水"),
            "type": "water",
            "count": 2,
            "provenance": "西北有洣水，自酃县流入",
        },
        {
            "text": N("05-092", "茶水"),
            "type": "water",
            "count": 1,
            "provenance": "又东南有茶水，源出江西永新县之景阳山",
        },
        {
            "text": N("05-092", "视渡口巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "东有视渡口巡检司",
        },
    ],
    tme=[
        {
            "reign": "元",
            "year": 24,
            "era_raw": N("05-092", "太祖甲辰年"),
            "category": "降秩",
            "event": N("05-092", "降为县"),
            "place": "茶陵州",
        },
        {
            "reign": "成化",
            "year": 18,
            "era_raw": N("05-092", "成化十八年十月"),
            "category": "升秩",
            "event": N("05-092", "复为州"),
            "place": "茶陵州",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-092", "元直隶湖南道"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-092", "元直隶湖南道"),
            "owner": "湖南道",
        },
        {
            "phase": 2,
            "era_raw": N("05-092", "太祖甲辰年"),
            "reign": "元",
            "year": 24,
            "change_type": "降县",
            "change": N("05-092", "降为县"),
            "owner": "长沙府",
        },
        {
            "phase": 3,
            "era_raw": N("05-092", "成化十八年十月"),
            "reign": "成化",
            "year": 18,
            "change_type": "升州",
            "change": N("05-092", "复为州"),
            "owner": "长沙府",
        },
    ],
    hyd=[
        {
            "name": N("05-092", "洣水"),
            "type": "江",
            "flow": N("05-092", "西北有洣水，自酃县流入"),
            "anchor": {"anchor": "茶陵州西北", "context": N("05-092", "西北有洣水")},
        },
        {
            "name": N("05-092", "茶水"),
            "type": "溪",
            "flow": N(
                "05-092",
                "又东南有茶水，源出江西永新县之景阳山，西流来合焉，北入攸县之攸水",
            ),
            "anchor": {"anchor": "茶陵州东南", "context": N("05-092", "又东南有茶水")},
        },
    ],
    gar=[
        {
            "name": N("05-092", "视渡口巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "茶陵州东",
            "dusi": "未明",
            "note": "东有视渡口巡检司",
        },
    ],
)

item(
    "05-093",
    geo={
        "name": N("05-093", "常德府"),
        "level": "府",
        "node_type": "政区",
        "parent": {"text": "湖广", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "东北",
                "to_anchor": "布政司",
                "distance": 1050,
                "unit": "里",
                "raw": N("05-093", "东北距布政司一千零五十里"),
            }
        ],
        "note": "元常德路，属湖广行省。太祖甲辰年为府。领县四",
    },
    ents=[
        {
            "text": N("05-093", "常德府"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-093", "常德路"),
            "type": "place",
            "count": 1,
            "provenance": "元常德路",
        },
        {
            "text": N("05-093", "湖广行省"),
            "type": "institution",
            "count": 1,
            "provenance": "属湖广行省",
        },
    ],
    tme=[
        {
            "reign": "元",
            "year": 24,
            "era_raw": N("05-093", "太祖甲辰年"),
            "category": "初置",
            "event": N("05-093", "为府"),
            "place": "常德府",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-093", "元常德路，属湖广行省"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-093", "元常德路，属湖广行省"),
            "owner": "湖广行省",
        },
        {
            "phase": 2,
            "era_raw": N("05-093", "太祖甲辰年"),
            "reign": "元",
            "year": 24,
            "change_type": "改置",
            "change": N("05-093", "为府"),
            "owner": "湖广行省",
        },
    ],
)

item(
    "05-094",
    geo={
        "name": N("05-094", "武陵"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "常德府", "rel": "领"},
        "note": "倚。弘治四年八月建荣王府。东南有善德山。南有沅水，又有朗水流入焉，谓之郎口。又东北有渐水，即鼎水也，自九溪卫流入",
    },
    ents=[
        {
            "text": N("05-094", "武陵"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-094", "善德山"),
            "type": "place",
            "count": 1,
            "provenance": "东南有善德山",
        },
        {
            "text": N("05-094", "沅水"),
            "type": "water",
            "count": 2,
            "provenance": "南有沅水",
        },
        {
            "text": N("05-094", "朗水"),
            "type": "water",
            "count": 1,
            "provenance": "又有朗水流入焉",
        },
        {
            "text": N("05-094", "渐水"),
            "type": "water",
            "count": 1,
            "provenance": "又东北有渐水",
        },
        {
            "text": N("05-094", "荣王府"),
            "type": "institution",
            "count": 1,
            "provenance": "弘治四年八月建荣王府",
        },
    ],
    tme=[
        {
            "reign": "弘治",
            "year": 4,
            "era_raw": N("05-094", "弘治四年八月"),
            "category": "增置",
            "event": N("05-094", "建荣王府"),
            "place": "武陵",
        },
    ],
    hyd=[
        {
            "name": N("05-094", "沅水"),
            "type": "江",
            "flow": N("05-094", "南有沅水"),
            "anchor": {"anchor": "武陵县南", "context": N("05-094", "南有沅水")},
        },
        {
            "name": N("05-094", "朗水"),
            "type": "江",
            "flow": N("05-094", "又有朗水流入焉，谓之郎口"),
            "anchor": {"anchor": "武陵县南", "context": N("05-094", "又有朗水流入焉")},
        },
        {
            "name": N("05-094", "渐水"),
            "type": "河",
            "flow": N("05-094", "又东北有渐水，即鼎水也，自九溪卫流入"),
            "anchor": {"anchor": "武陵县东北", "context": N("05-094", "又东北有渐水")},
        },
    ],
)

item(
    "05-095",
    geo={
        "name": N("05-095", "桃源"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "常德府", "rel": "领"},
        "note": "府西。元桃源州。洪武二年降为县。西有壶头山。南有沅水，东有朗溪，西南有泥溪。西南有高都巡检司。又南有白马巡检司",
    },
    ents=[
        {
            "text": N("05-095", "桃源"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-095", "壶头山"),
            "type": "place",
            "count": 1,
            "provenance": "西有壶头山，接武陵、沅陵界",
        },
        {
            "text": N("05-095", "沅水"),
            "type": "water",
            "count": 2,
            "provenance": "南有沅水",
        },
        {
            "text": N("05-095", "朗溪"),
            "type": "water",
            "count": 1,
            "provenance": "东有朗溪",
        },
        {
            "text": N("05-095", "泥溪"),
            "type": "water",
            "count": 1,
            "provenance": "西南有泥溪",
        },
        {
            "text": N("05-095", "高都巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "又西南有高都巡检司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 2,
            "era_raw": N("05-095", "洪武二年"),
            "category": "降秩",
            "event": N("05-095", "降为县"),
            "place": "桃源",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-095", "元桃源州"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-095", "元桃源州"),
            "owner": "常德府",
        },
        {
            "phase": 2,
            "era_raw": N("05-095", "洪武二年"),
            "reign": "洪武",
            "year": 2,
            "change_type": "降县",
            "change": N("05-095", "降为县"),
            "owner": "常德府",
        },
    ],
    hyd=[
        {
            "name": N("05-095", "沅水"),
            "type": "江",
            "flow": N("05-095", "南有沅水"),
            "anchor": {"anchor": "桃源县南", "context": N("05-095", "南有沅水")},
        },
        {
            "name": N("05-095", "朗溪"),
            "type": "溪",
            "flow": N("05-095", "东有朗溪"),
            "anchor": {"anchor": "桃源县东", "context": N("05-095", "东有朗溪")},
        },
        {
            "name": N("05-095", "泥溪"),
            "type": "溪",
            "flow": N("05-095", "西南有泥溪，俱流入焉"),
            "anchor": {"anchor": "桃源县西南", "context": N("05-095", "西南有泥溪")},
        },
    ],
    gar=[
        {
            "name": N("05-095", "高都巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "桃源县西南",
            "dusi": "未明",
            "note": "又西南有高都巡检司",
        },
        {
            "name": N("05-095", "白马巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "桃源县南",
            "dusi": "未明",
            "note": "又南有白马巡检司，本名苏溪，治县东后春村，寻徙，更名，后废",
        },
    ],
)

item(
    "05-096",
    geo={
        "name": N("05-096", "龙阳"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "常德府", "rel": "领"},
        "note": "府东少南。元龙阳州。洪武三年三月降为县。旧治在东，今治景泰元年十二月所徙。东有军山。北有沅水。又东南有赤沙湖。西北有小江口巡检司",
    },
    ents=[
        {
            "text": N("05-096", "龙阳"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-096", "军山"),
            "type": "place",
            "count": 1,
            "provenance": "东有军山",
        },
        {
            "text": N("05-096", "沅水"),
            "type": "water",
            "count": 2,
            "provenance": "北有沅水",
        },
        {
            "text": N("05-096", "鼎水"),
            "type": "water",
            "count": 1,
            "provenance": "东北有鼎水流入焉",
        },
        {
            "text": N("05-096", "赤沙湖"),
            "type": "water",
            "count": 1,
            "provenance": "又东南有赤沙湖",
        },
        {
            "text": N("05-096", "小江口巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "又西北有小江口巡检司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 3,
            "era_raw": N("05-096", "洪武三年三月"),
            "category": "降秩",
            "event": N("05-096", "降为县"),
            "place": "龙阳",
        },
        {
            "reign": "景泰",
            "year": 1,
            "era_raw": N("05-096", "景泰元年十二月"),
            "category": "徙治",
            "event": N("05-096", "今治景泰元年十二月所徙"),
            "place": "龙阳",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-096", "元龙阳州"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-096", "元龙阳州"),
            "owner": "常德府",
        },
        {
            "phase": 2,
            "era_raw": N("05-096", "洪武三年三月"),
            "reign": "洪武",
            "year": 3,
            "change_type": "降县",
            "change": N("05-096", "降为县"),
            "owner": "常德府",
        },
        {
            "phase": 3,
            "era_raw": N("05-096", "景泰元年十二月"),
            "reign": "景泰",
            "year": 1,
            "change_type": "徙治",
            "change": N("05-096", "旧治在东，今治景泰元年十二月所徙"),
            "owner": "常德府",
        },
    ],
    hyd=[
        {
            "name": N("05-096", "沅水"),
            "type": "江",
            "flow": N("05-096", "北有沅水"),
            "anchor": {"anchor": "龙阳县北", "context": N("05-096", "北有沅水")},
        },
        {
            "name": N("05-096", "鼎水"),
            "type": "河",
            "flow": N("05-096", "东北有鼎水流入焉，谓之鼎口"),
            "anchor": {
                "anchor": "龙阳县东北",
                "context": N("05-096", "东北有鼎水流入焉"),
            },
        },
        {
            "name": N("05-096", "赤沙湖"),
            "alt": "蠡湖",
            "type": "湖",
            "flow": N("05-096", "又东南有赤沙湖，一名蠡湖"),
            "anchor": {
                "anchor": "龙阳县东南",
                "context": N("05-096", "又东南有赤沙湖"),
            },
        },
    ],
    gar=[
        {
            "name": N("05-096", "鼎港口巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "龙阳鼎口",
            "dusi": "未明",
            "note": "有鼎港口巡检司",
        },
        {
            "name": N("05-096", "小江口巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "龙阳县西北",
            "dusi": "未明",
            "note": "又西北有小江口巡检司",
        },
    ],
)

item(
    "05-097",
    geo={
        "name": N("05-097", "沅江"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "常德府", "rel": "领"},
        "note": "府东南。元属龙阳州。洪武三年州废来属。十年五月省入龙阳县。十三年五月复置。西南有沅水。又有澬水、澧水，并流入县境，至县东北入洞庭湖",
    },
    ents=[
        {
            "text": N("05-097", "沅江"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-097", "沅水"),
            "type": "water",
            "count": 2,
            "provenance": "西南有沅水",
        },
        {
            "text": N("05-097", "澬水"),
            "type": "water",
            "count": 1,
            "provenance": "又有澬水、澧水",
        },
        {
            "text": N("05-097", "澧水"),
            "type": "water",
            "count": 1,
            "provenance": "又有澬水、澧水",
        },
        {
            "text": N("05-097", "洞庭湖"),
            "type": "water",
            "count": 1,
            "provenance": "至县东北入洞庭湖",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 3,
            "era_raw": N("05-097", "洪武三年"),
            "category": "改隶",
            "event": N("05-097", "州废，来属"),
            "place": "沅江",
        },
        {
            "reign": "洪武",
            "year": 10,
            "era_raw": N("05-097", "十年五月"),
            "category": "省入",
            "event": N("05-097", "省入龙阳县"),
            "place": "沅江",
        },
        {
            "reign": "洪武",
            "year": 13,
            "era_raw": N("05-097", "十三年五月"),
            "category": "复设",
            "event": N("05-097", "复置"),
            "place": "沅江",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-097", "元属龙阳州"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-097", "元属龙阳州"),
            "owner": "龙阳州",
        },
        {
            "phase": 2,
            "era_raw": N("05-097", "洪武三年"),
            "reign": "洪武",
            "year": 3,
            "change_type": "改隶",
            "change": N("05-097", "州废，来属"),
            "owner": "常德府",
        },
        {
            "phase": 3,
            "era_raw": N("05-097", "十年五月"),
            "reign": "洪武",
            "year": 10,
            "change_type": "省入",
            "change": N("05-097", "省入龙阳县"),
            "owner": "龙阳县",
        },
        {
            "phase": 4,
            "era_raw": N("05-097", "十三年五月"),
            "reign": "洪武",
            "year": 13,
            "change_type": "复置",
            "change": N("05-097", "复置"),
            "owner": "常德府",
        },
    ],
    hyd=[
        {
            "name": N("05-097", "沅水"),
            "type": "江",
            "flow": N("05-097", "西南有沅水"),
            "anchor": {"anchor": "沅江县西南", "context": N("05-097", "西南有沅水")},
        },
        {
            "name": N("05-097", "澬水"),
            "type": "江",
            "flow": N("05-097", "又有澬水、澧水，并流入县境，至县东北入洞庭湖"),
            "anchor": {"anchor": "沅江县", "context": N("05-097", "又有澬水、澧水")},
        },
        {
            "name": N("05-097", "澧水"),
            "type": "江",
            "flow": N("05-097", "又有澬水、澧水，并流入县境，至县东北入洞庭湖"),
            "anchor": {"anchor": "沅江县", "context": N("05-097", "又有澬水、澧水")},
        },
        {
            "name": N("05-097", "洞庭湖"),
            "type": "湖",
            "flow": N("05-097", "至县东北入洞庭湖"),
            "anchor": {
                "anchor": "沅江县东北",
                "context": N("05-097", "至县东北入洞庭湖"),
            },
        },
    ],
)

# ---------- 衡州府 ----------
item(
    "05-098",
    geo={
        "name": N("05-098", "衡州府"),
        "level": "府",
        "node_type": "政区",
        "parent": {"text": "湖广", "rel": "领"},
        "bearing_distance": [
            {
                "bearing": "东北",
                "to_anchor": "布政司",
                "distance": 1300,
                "unit": "里",
                "raw": N("05-098", "东北距布政司一千三百里"),
            }
        ],
        "note": "元衡州路，属湖南道宣慰司。太祖甲辰年为府。领州一，县九",
    },
    ents=[
        {
            "text": N("05-098", "衡州府"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-098", "衡州路"),
            "type": "place",
            "count": 1,
            "provenance": "元衡州路",
        },
        {
            "text": N("05-098", "湖南道宣慰司"),
            "type": "institution",
            "count": 1,
            "provenance": "属湖南道宣慰司",
        },
    ],
    tme=[
        {
            "reign": "元",
            "year": 24,
            "era_raw": N("05-098", "太祖甲辰年"),
            "category": "初置",
            "event": N("05-098", "为府"),
            "place": "衡州府",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-098", "元衡州路，属湖南道宣慰司"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-098", "元衡州路，属湖南道宣慰司"),
            "owner": "湖南道宣慰司",
        },
        {
            "phase": 2,
            "era_raw": N("05-098", "太祖甲辰年"),
            "reign": "元",
            "year": 24,
            "change_type": "改置",
            "change": N("05-098", "为府"),
            "owner": "湖南道宣慰司",
        },
    ],
)

item(
    "05-099",
    geo={
        "name": N("05-099", "衡阳"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "衡州府", "rel": "领"},
        "note": "倚。南有回雁峰，北有岣嵝峰。东有湘水，又有蒸水自西南流入焉，谓之蒸口。又东北有耒水。又东有酃湖。又东有新城县，元末置。洪武十年五月省为新城市。西南有松柏市巡检司",
    },
    ents=[
        {
            "text": N("05-099", "衡阳"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-099", "回雁峰"),
            "type": "place",
            "count": 1,
            "provenance": "南有回雁峰",
        },
        {
            "text": N("05-099", "岣嵝峰"),
            "type": "place",
            "count": 1,
            "provenance": "北有岣嵝峰",
        },
        {
            "text": N("05-099", "湘水"),
            "type": "water",
            "count": 2,
            "provenance": "东有湘水",
        },
        {
            "text": N("05-099", "耒水"),
            "type": "water",
            "count": 1,
            "provenance": "又东北有耒水，注湘",
        },
        {
            "text": N("05-099", "桂王府"),
            "type": "institution",
            "count": 1,
            "provenance": "万历二十九年十月建桂王府",
        },
    ],
    tme=[
        {
            "reign": "弘治",
            "year": 12,
            "era_raw": N("05-099", "弘治十二年"),
            "category": "徙治",
            "event": N("05-099", "雍王府自四川保宁府迁此"),
            "place": "衡阳",
        },
        {
            "reign": "万历",
            "year": 29,
            "era_raw": N("05-099", "万历二十九年十月"),
            "category": "增置",
            "event": N("05-099", "建桂王府"),
            "place": "衡阳",
        },
        {
            "reign": "洪武",
            "year": 10,
            "era_raw": N("05-099", "洪武十年五月"),
            "category": "省入",
            "event": N("05-099", "省为新城市"),
            "place": "衡阳",
        },
    ],
    hyd=[
        {
            "name": N("05-099", "湘水"),
            "type": "江",
            "flow": N("05-099", "东有湘水"),
            "anchor": {"anchor": "衡阳县东", "context": N("05-099", "东有湘水")},
        },
        {
            "name": N("05-099", "蒸水"),
            "type": "江",
            "flow": N("05-099", "又有蒸水自西南流入焉，谓之蒸口"),
            "anchor": {
                "anchor": "衡阳县西南",
                "context": N("05-099", "又有蒸水自西南流入焉"),
            },
        },
        {
            "name": N("05-099", "耒水"),
            "type": "江",
            "flow": N("05-099", "又东北有耒水，注湘，谓之耒口"),
            "anchor": {"anchor": "衡阳县东北", "context": N("05-099", "又东北有耒水")},
        },
        {
            "name": N("05-099", "酃湖"),
            "type": "湖",
            "flow": N("05-099", "又东有酃湖"),
            "anchor": {"anchor": "衡阳县东", "context": N("05-099", "又东有酃湖")},
        },
    ],
    gar=[
        {
            "name": N("05-099", "江东巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "衡阳县东新城市",
            "dusi": "未明",
            "note": "洪武十年五月省为新城市，江东巡检司治此",
        },
        {
            "name": N("05-099", "松柏市巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "衡阳县西南",
            "dusi": "未明",
            "note": "西南有松柏市巡检司",
        },
    ],
)

item(
    "05-100",
    geo={
        "name": N("05-100", "衡山"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "衡州府", "rel": "领"},
        "note": "府东北。元属天临路。洪武间改属。西有衡山。东有湘江。东南有茶陵江。东有草市、东南有雷家埠二巡检司",
    },
    ents=[
        {
            "text": N("05-100", "衡山"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-100", "衡山"),
            "type": "place",
            "count": 1,
            "provenance": "西有衡山",
        },
        {
            "text": N("05-100", "湘江"),
            "type": "water",
            "count": 1,
            "provenance": "东有湘江",
        },
        {
            "text": N("05-100", "茶陵江"),
            "type": "water",
            "count": 1,
            "provenance": "东南有茶陵江",
        },
        {
            "text": N("05-100", "洣水"),
            "type": "water",
            "count": 1,
            "provenance": "东南有茶陵江，即洣水也",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-100", "元属天临路"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-100", "元属天临路"),
            "owner": "天临路",
        },
        {
            "phase": 2,
            "era_raw": N("05-100", "洪武间"),
            "reign": "洪武",
            "year": 0,
            "change_type": "改隶",
            "change": N("05-100", "改属"),
            "owner": "衡州府",
        },
    ],
    hyd=[
        {
            "name": N("05-100", "湘江"),
            "type": "江",
            "flow": N("05-100", "东有湘江"),
            "anchor": {"anchor": "衡山县东", "context": N("05-100", "东有湘江")},
        },
        {
            "name": N("05-100", "茶陵江"),
            "alt": "洣水",
            "type": "江",
            "flow": N(
                "05-100", "东南有茶陵江，即洣水也，自攸县合攸水流入境，注于湘，曰茶陵口"
            ),
            "anchor": {"anchor": "衡山县东南", "context": N("05-100", "东南有茶陵江")},
        },
    ],
    gar=[
        {
            "name": N("05-100", "草市"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "衡山县东",
            "dusi": "未明",
            "note": "东有草市、东南有雷家埠二巡检司",
        },
        {
            "name": N("05-100", "雷家埠"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "衡山县东南",
            "dusi": "未明",
            "note": "东有草市、东南有雷家埠二巡检司",
        },
    ],
)

item(
    "05-101",
    geo={
        "name": N("05-101", "耒阳"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "衡州府", "rel": "领"},
        "note": "府东南。元耒阳州，直隶湖南道。洪武三年三月降为县。耒水在北。东有侯计山，肥水出焉。又西南有罗渡巡检司",
    },
    ents=[
        {
            "text": N("05-101", "耒阳"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-101", "耒水"),
            "type": "water",
            "count": 3,
            "provenance": "耒水在北",
        },
        {
            "text": N("05-101", "侯计山"),
            "type": "place",
            "count": 1,
            "provenance": "东有侯计山",
        },
        {
            "text": N("05-101", "肥水"),
            "type": "water",
            "count": 1,
            "provenance": "肥水出焉",
        },
        {
            "text": N("05-101", "罗渡巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "又西南有罗渡巡检司",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 3,
            "era_raw": N("05-101", "洪武三年三月"),
            "category": "降秩",
            "event": N("05-101", "降为县"),
            "place": "耒阳",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-101", "元耒阳州，直隶湖南道"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-101", "元耒阳州，直隶湖南道"),
            "owner": "湖南道",
        },
        {
            "phase": 2,
            "era_raw": N("05-101", "洪武三年三月"),
            "reign": "洪武",
            "year": 3,
            "change_type": "降县",
            "change": N("05-101", "降为县"),
            "owner": "衡州府",
        },
    ],
    hyd=[
        {
            "name": N("05-101", "耒水"),
            "type": "江",
            "flow": N("05-101", "耒水在北"),
            "anchor": {"anchor": "耒阳县北", "context": N("05-101", "耒水在北")},
        },
        {
            "name": N("05-101", "肥水"),
            "type": "溪",
            "flow": N("05-101", "东有侯计山，肥水出焉，西南入耒水"),
            "anchor": {"anchor": "耒阳县东", "context": N("05-101", "肥水出焉")},
        },
    ],
    gar=[
        {
            "name": N("05-101", "罗渡巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "耒阳县西南",
            "dusi": "未明",
            "note": "又西南有罗渡巡检司",
        },
    ],
)

item(
    "05-102",
    geo={
        "name": N("05-102", "常宁"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "衡州府", "rel": "领"},
        "note": "府南。元常宁州，直隶湖南道。洪武三年三月降为县。西北有湘水，东有舂陵水合焉",
    },
    ents=[
        {
            "text": N("05-102", "常宁"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-102", "湘水"),
            "type": "water",
            "count": 1,
            "provenance": "西北有湘水",
        },
        {
            "text": N("05-102", "舂陵水"),
            "type": "water",
            "count": 1,
            "provenance": "东有舂陵水合焉",
        },
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 3,
            "era_raw": N("05-102", "洪武三年三月"),
            "category": "降秩",
            "event": N("05-102", "降为县"),
            "place": "常宁",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-102", "元常宁州，直隶湖南道"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-102", "元常宁州，直隶湖南道"),
            "owner": "湖南道",
        },
        {
            "phase": 2,
            "era_raw": N("05-102", "洪武三年三月"),
            "reign": "洪武",
            "year": 3,
            "change_type": "降县",
            "change": N("05-102", "降为县"),
            "owner": "衡州府",
        },
    ],
    hyd=[
        {
            "name": N("05-102", "湘水"),
            "type": "江",
            "flow": N("05-102", "西北有湘水"),
            "anchor": {"anchor": "常宁县西北", "context": N("05-102", "西北有湘水")},
        },
        {
            "name": N("05-102", "舂陵水"),
            "type": "江",
            "flow": N("05-102", "东有舂陵水合焉"),
            "anchor": {"anchor": "常宁县东", "context": N("05-102", "东有舂陵水合焉")},
        },
    ],
)

item(
    "05-103",
    geo={
        "name": N("05-103", "安仁"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "衡州府", "rel": "领"},
        "note": "府东少北。西有杨梅峰。南有小江水。南有安平、北有潭湖二巡检司",
    },
    ents=[
        {
            "text": N("05-103", "安仁"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-103", "杨梅峰"),
            "type": "place",
            "count": 1,
            "provenance": "西有杨梅峰",
        },
        {
            "text": N("05-103", "小江水"),
            "type": "water",
            "count": 1,
            "provenance": "南有小江水",
        },
        {
            "text": N("05-103", "洣水"),
            "type": "water",
            "count": 1,
            "provenance": "西北流至衡山县，合于洣水",
        },
    ],
    hyd=[
        {
            "name": N("05-103", "小江水"),
            "type": "江",
            "flow": N("05-103", "南有小江水，自郴州流入，西北流至衡山县，合于洣水"),
            "anchor": {"anchor": "安仁县南", "context": N("05-103", "南有小江水")},
        },
    ],
    gar=[
        {
            "name": N("05-103", "安平"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "安仁县南",
            "dusi": "未明",
            "note": "南有安平、北有潭湖二巡检司",
        },
        {
            "name": N("05-103", "潭湖"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "安仁县北",
            "dusi": "未明",
            "note": "南有安平、北有潭湖二巡检司",
        },
    ],
)

item(
    "05-104",
    geo={
        "name": N("05-104", "灵阝"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "衡州府", "rel": "领"},
        "note": "府东。洣水在县东，源出洣泉，西有云秋水流合焉",
    },
    ents=[
        {
            "text": N("05-104", "灵阝"),
            "type": "place",
            "count": 1,
            "provenance": "条目名",
        },
        {
            "text": N("05-104", "洣水"),
            "type": "water",
            "count": 1,
            "provenance": "洣水在县东",
        },
        {
            "text": N("05-104", "洣泉"),
            "type": "water",
            "count": 1,
            "provenance": "源出洣泉",
        },
        {
            "text": N("05-104", "云秋水"),
            "type": "water",
            "count": 1,
            "provenance": "西有云秋水流合焉",
        },
    ],
    hyd=[
        {
            "name": N("05-104", "洣水"),
            "type": "江",
            "flow": N("05-104", "洣水在县东，源出洣泉"),
            "anchor": {"anchor": "灵阝县东", "context": N("05-104", "洣水在县东")},
        },
        {
            "name": N("05-104", "云秋水"),
            "type": "溪",
            "flow": N("05-104", "西有云秋水流合焉"),
            "anchor": {
                "anchor": "灵阝县西",
                "context": N("05-104", "西有云秋水流合焉"),
            },
        },
    ],
)

print("PART2 done, items=%d" % len(D))
