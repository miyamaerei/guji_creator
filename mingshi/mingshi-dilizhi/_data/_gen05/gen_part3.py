# -*- coding: utf-8 -*-
"""卷05 分片3生成器：05-182 ~ 05-269（浙江布政司全境）。校验后输出 data_part3.py。"""

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


# ---------- 浙江布政司总述 ----------
item(
    "05-182",
    geo={
        "name": N("05-182", "浙江"),
        "level": "布政使司",
        "node_type": "政区",
        "parent": {"text": "", "rel": ""},
        "bearing_distance": [
            {
                "bearing": "",
                "to_anchor": "南京",
                "distance": 900,
                "unit": "里",
                "raw": N("05-182", "距南京九百里"),
            },
            {
                "bearing": "",
                "to_anchor": "京师",
                "distance": 3200,
                "unit": "里",
                "raw": N("05-182", "京师三千二百里"),
            },
        ],
        "quantity": [
            {
                "kind": "编户",
                "reign": "洪武",
                "year": 26,
                "era_raw": "洪武二十六年",
                "num": 2138225,
                "unit": "户",
                "raw": "洪武二十六年编户二百一十三万八千二百二十五",
            },
            {
                "kind": "口数",
                "reign": "洪武",
                "year": 26,
                "era_raw": "洪武二十六年",
                "num": 10487567,
                "unit": "口",
                "raw": "口一千四十八万七千五百六十七",
            },
            {
                "kind": "编户",
                "reign": "弘治",
                "year": 4,
                "era_raw": "弘治四年",
                "num": 1503124,
                "unit": "户",
                "raw": "弘治四年，户一百五十万三千一百二十四",
            },
            {
                "kind": "口数",
                "reign": "弘治",
                "year": 4,
                "era_raw": "弘治四年",
                "num": 5305843,
                "unit": "口",
                "raw": "口五百三十万五千八百四十三",
            },
            {
                "kind": "编户",
                "reign": "万历",
                "year": 6,
                "era_raw": "万历六年",
                "num": 1542408,
                "unit": "户",
                "raw": "万历六年，户一百五十四万二千四百八",
            },
            {
                "kind": "口数",
                "reign": "万历",
                "year": 6,
                "era_raw": "万历六年",
                "num": 5153005,
                "unit": "口",
                "raw": "口五百一十五万三千五",
            },
        ],
        "note": "领府十一，属州一，县七十五",
    },
    ents=[
        {"text": N("05-182", "浙江"), "type": "place", "count": 1, "provenance": "条目名"},
        {
            "text": N("05-182", "江浙等处行中书省"),
            "type": "institution",
            "count": 1,
            "provenance": "元置江浙等处行中书省",
        },
        {
            "text": N("05-182", "杭州路"),
            "type": "place",
            "count": 1,
            "provenance": "治杭州路",
        },
        {
            "text": N("05-182", "浙东道宣慰使司"),
            "type": "institution",
            "count": 1,
            "provenance": "又分置浙东道宣慰使司",
        },
        {
            "text": N("05-182", "庆元路"),
            "type": "place",
            "count": 1,
            "provenance": "治庆元路",
        },
        {
            "text": N("05-182", "中书分省"),
            "type": "institution",
            "count": 1,
            "provenance": "太祖戊戌年十二月置中书分省",
        },
        {
            "text": N("05-182", "宁越府"),
            "type": "place",
            "count": 1,
            "provenance": "治宁越府",
        },
        {
            "text": N("05-182", "严州府"),
            "type": "place",
            "count": 1,
            "provenance": "癸卯年二月移治严州府",
        },
        {
            "text": N("05-182", "浙江等处行中书省"),
            "type": "institution",
            "count": 1,
            "provenance": "置浙江等处行中书省",
        },
        {
            "text": N("05-182", "杭州府"),
            "type": "place",
            "count": 1,
            "provenance": "治杭州府",
        },
        {
            "text": N("05-182", "杭州都卫"),
            "type": "institution",
            "count": 1,
            "provenance": "洪武三年十二月置杭州都卫",
        },
        {
            "text": N("05-182", "浙江都指挥使司"),
            "type": "institution",
            "count": 1,
            "provenance": "八年十月改都卫为浙江都指挥使司",
        },
        {
            "text": N("05-182", "承宣布政使司"),
            "type": "system",
            "count": 1,
            "provenance": "九年六月改行中书省为承宣布政使司",
        },
        {
            "text": N("05-182", "太祖"),
            "type": "person",
            "count": 1,
            "provenance": "太祖戊戌年十二月置中书分省",
        },
        {
            "text": N("05-182", "洪武"),
            "type": "era",
            "count": 1,
            "provenance": "洪武二十六年编户",
        },
    ],
    tme=[
        {
            "reign": "元",
            "year": 18,
            "era_raw": N("05-182", "太祖戊戌年十二月"),
            "category": "初置",
            "event": N("05-182", "置中书分省"),
            "place": "浙江",
        },
        {
            "reign": "元",
            "year": 23,
            "era_raw": N("05-182", "癸卯年二月"),
            "category": "移治",
            "event": N("05-182", "移治严州府"),
            "place": "浙江",
        },
        {
            "reign": "元",
            "year": 26,
            "era_raw": N("05-182", "丙午年十二月"),
            "category": "改置",
            "event": N("05-182", "罢分省，置浙江等处行中书省"),
            "place": "浙江",
        },
        {
            "reign": "洪武",
            "year": 3,
            "era_raw": N("05-182", "洪武三年十二月"),
            "category": "增置",
            "event": N("05-182", "置杭州都卫"),
            "place": "浙江",
        },
        {
            "reign": "洪武",
            "year": 8,
            "era_raw": N("05-182", "八年十月"),
            "category": "改置",
            "event": N("05-182", "改都卫为浙江都指挥使司"),
            "place": "浙江",
        },
        {
            "reign": "洪武",
            "year": 9,
            "era_raw": N("05-182", "九年六月"),
            "category": "改置",
            "event": N("05-182", "改行中书省为承宣布政使司"),
            "place": "浙江",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-182", "元置江浙等处行中书省"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-182", "元置江浙等处行中书省"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-182", "太祖戊戌年十二月"),
            "reign": "元",
            "year": 18,
            "change_type": "改置",
            "change": N("05-182", "置中书分省"),
            "owner": "未明",
        },
        {
            "phase": 3,
            "era_raw": N("05-182", "丙午年十二月"),
            "reign": "元",
            "year": 26,
            "change_type": "改置",
            "change": N("05-182", "罢分省，置浙江等处行中书省"),
            "owner": "未明",
        },
        {
            "phase": 4,
            "era_raw": N("05-182", "洪武三年十二月"),
            "reign": "洪武",
            "year": 3,
            "change_type": "增设",
            "change": N("05-182", "置杭州都卫"),
            "owner": "未明",
        },
        {
            "phase": 5,
            "era_raw": N("05-182", "八年十月"),
            "reign": "洪武",
            "year": 8,
            "change_type": "改置",
            "change": N("05-182", "改都卫为浙江都指挥使司"),
            "owner": "未明",
        },
        {
            "phase": 6,
            "era_raw": N("05-182", "九年六月"),
            "reign": "洪武",
            "year": 9,
            "change_type": "改置",
            "change": N("05-182", "改行中书省为承宣布政使司"),
            "owner": "未明",
        },
    ],
)

# ---------- 杭州府 ----------
item(
    "05-183",
    geo={
        "name": N("05-183", "杭州府"),
        "level": "府",
        "node_type": "政区",
        "parent": {"text": "浙江", "rel": "领"},
        "note": "元杭州路，属江浙行省。太祖丙午年十一月为府。领县九",
    },
    ents=[
        {"text": N("05-183", "杭州府"), "type": "place", "count": 1, "provenance": "条目名"},
        {
            "text": N("05-183", "杭州路"),
            "type": "place",
            "count": 1,
            "provenance": "元杭州路",
        },
        {
            "text": N("05-183", "江浙行省"),
            "type": "institution",
            "count": 1,
            "provenance": "属江浙行省",
        },
        {
            "text": N("05-183", "太祖"),
            "type": "person",
            "count": 1,
            "provenance": "太祖丙午年十一月为府",
        },
    ],
    tme=[
        {
            "reign": "元",
            "year": 26,
            "era_raw": N("05-183", "太祖丙午年十一月"),
            "category": "升秩",
            "event": N("05-183", "为府"),
            "place": "杭州府",
        },
    ],
    evo=[
        {
            "phase": 1,
            "era_raw": N("05-183", "元杭州路，属江浙行省"),
            "reign": "元",
            "year": 0,
            "change_type": "初置",
            "change": N("05-183", "元杭州路，属江浙行省"),
            "owner": "未明",
        },
        {
            "phase": 2,
            "era_raw": N("05-183", "太祖丙午年十一月"),
            "reign": "元",
            "year": 26,
            "change_type": "改置",
            "change": N("05-183", "为府"),
            "owner": "未明",
        },
    ],
)

# ---------- 杭州府属县 ----------
item(
    "05-184",
    geo={
        "name": N("05-184", "钱塘"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "杭州府", "rel": "领"},
        "note": "倚。洪武三年四月建吴王府。十一年正月改封周王，迁河南开封府。南有凤凰山，有秦望山。西南有灵隐山。南有钱塘江，亦曰浙江，有三源：曰新安江，出南直歙县；曰信安江，出开化县；曰东阳江，出东阳县。汇而东为钱塘江，至会稽县三江海口入海。西有西湖，源出武林泉。又北有运河，至秀水县北，而接南直运河。又有安溪，即苕溪也，自余杭县流入，下流至乌程县东北，注于太湖",
    },
    ents=[
        {"text": N("05-184", "钱塘"), "type": "place", "count": 1, "provenance": "条目名"},
        {
            "text": N("05-184", "吴王府"),
            "type": "institution",
            "count": 1,
            "provenance": "洪武三年四月建吴王府",
        },
        {
            "text": N("05-184", "周王"),
            "type": "person",
            "count": 1,
            "provenance": "十一年正月改封周王",
        },
        {
            "text": N("05-184", "河南开封府"),
            "type": "place",
            "count": 1,
            "provenance": "迁河南开封府",
        },
        {"text": N("05-184", "凤凰山"), "type": "place", "count": 1, "provenance": "南有凤凰山"},
        {"text": N("05-184", "秦望山"), "type": "place", "count": 1, "provenance": "有秦望山"},
        {"text": N("05-184", "灵隐山"), "type": "place", "count": 1, "provenance": "西南有灵隐山"},
        {
            "text": N("05-184", "钱塘江"),
            "type": "water",
            "count": 2,
            "provenance": "南有钱塘江，亦曰浙江",
        },
        {
            "text": N("05-184", "浙江"),
            "type": "water",
            "count": 1,
            "provenance": "亦曰浙江",
        },
        {
            "text": N("05-184", "新安江"),
            "type": "water",
            "count": 1,
            "provenance": "曰新安江，出南直歙县",
        },
        {
            "text": N("05-184", "南直歙县"),
            "type": "place",
            "count": 1,
            "provenance": "出南直歙县",
        },
        {
            "text": N("05-184", "信安江"),
            "type": "water",
            "count": 1,
            "provenance": "曰信安江，出开化县",
        },
        {"text": N("05-184", "开化县"), "type": "place", "count": 1, "provenance": "出开化县"},
        {
            "text": N("05-184", "东阳江"),
            "type": "water",
            "count": 1,
            "provenance": "曰东阳江，出东阳县",
        },
        {"text": N("05-184", "东阳县"), "type": "place", "count": 1, "provenance": "出东阳县"},
        {
            "text": N("05-184", "会稽县"),
            "type": "place",
            "count": 1,
            "provenance": "至会稽县三江海口入海",
        },
        {
            "text": N("05-184", "西湖"),
            "type": "water",
            "count": 1,
            "provenance": "西有西湖，源出武林泉",
        },
        {
            "text": N("05-184", "运河"),
            "type": "water",
            "count": 1,
            "provenance": "又北有运河，至秀水县北，而接南直运河",
        },
        {"text": N("05-184", "秀水县"), "type": "place", "count": 1, "provenance": "至秀水县北"},
        {
            "text": N("05-184", "安溪"),
            "type": "water",
            "count": 1,
            "provenance": "又有安溪，即苕溪也",
        },
        {
            "text": N("05-184", "苕溪"),
            "type": "water",
            "count": 1,
            "provenance": "即苕溪也，自余杭县流入",
        },
        {"text": N("05-184", "余杭县"), "type": "place", "count": 1, "provenance": "自余杭县流入"},
        {
            "text": N("05-184", "乌程县"),
            "type": "place",
            "count": 1,
            "provenance": "下流至乌程县东北",
        },
        {"text": N("05-184", "太湖"), "type": "water", "count": 1, "provenance": "注于太湖"},
        {"text": N("05-184", "洪武"), "type": "era", "count": 1, "provenance": "洪武三年四月建吴王府"},
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 3,
            "era_raw": N("05-184", "洪武三年四月"),
            "category": "增置",
            "event": N("05-184", "建吴王府"),
            "place": "钱塘",
        },
        {
            "reign": "洪武",
            "year": 11,
            "era_raw": N("05-184", "十一年正月"),
            "category": "改置",
            "event": N("05-184", "改封周王，迁河南开封府"),
            "place": "钱塘",
        },
    ],
    hyd=[
        {
            "name": N("05-184", "钱塘江"),
            "alt": "浙江",
            "type": "江",
            "flow": "南有钱塘江，亦曰浙江，有三源：曰新安江，出南直歙县；曰信安江，出开化县；曰东阳江，出东阳县。汇而东为钱塘江，至会稽县三江海口入海",
            "anchor": {"anchor": "钱塘县南", "context": N("05-184", "南有钱塘江")},
        },
        {
            "name": N("05-184", "西湖"),
            "alt": "",
            "type": "湖",
            "flow": N("05-184", "西有西湖，源出武林泉"),
            "anchor": {"anchor": "钱塘县西", "context": N("05-184", "西有西湖")},
        },
        {
            "name": N("05-184", "运河"),
            "alt": "",
            "type": "河",
            "flow": N("05-184", "又北有运河，至秀水县北，而接南直运河"),
            "anchor": {"anchor": "钱塘县北", "context": N("05-184", "又北有运河")},
        },
        {
            "name": N("05-184", "安溪"),
            "alt": "苕溪",
            "type": "溪",
            "flow": N("05-184", "又有安溪，即苕溪也，自余杭县流入，下流至乌程县东北，注于太湖"),
            "anchor": {"anchor": "钱塘县", "context": N("05-184", "又有安溪")},
        },
    ],
)

item(
    "05-185",
    geo={
        "name": N("05-185", "仁和"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "杭州府", "rel": "领"},
        "note": "倚。东北有皋亭山，有临平山，下有临平湖，后塞。北有北新关，成化中设户部分司于此。又有塘栖镇",
    },
    ents=[
        {"text": N("05-185", "仁和"), "type": "place", "count": 1, "provenance": "条目名"},
        {"text": N("05-185", "皋亭山"), "type": "place", "count": 1, "provenance": "东北有皋亭山"},
        {"text": N("05-185", "临平山"), "type": "place", "count": 1, "provenance": "有临平山"},
        {"text": N("05-185", "临平湖"), "type": "water", "count": 1, "provenance": "下有临平湖，后塞"},
        {
            "text": N("05-185", "北新关"),
            "type": "institution",
            "count": 1,
            "provenance": "北有北新关",
        },
        {
            "text": N("05-185", "户部分司"),
            "type": "institution",
            "count": 1,
            "provenance": "成化中设户部分司于此",
        },
        {"text": N("05-185", "塘栖镇"), "type": "place", "count": 1, "provenance": "又有塘栖镇"},
        {"text": N("05-185", "成化"), "type": "era", "count": 1, "provenance": "成化中设户部分司"},
    ],
    tme=[
        {
            "reign": "成化",
            "year": 0,
            "era_raw": N("05-185", "成化中"),
            "category": "增置",
            "event": N("05-185", "设户部分司于此"),
            "place": "仁和",
        },
    ],
    hyd=[
        {
            "name": N("05-185", "临平湖"),
            "alt": "",
            "type": "湖",
            "flow": N("05-185", "有临平山，下有临平湖，后塞"),
            "anchor": {"anchor": "仁和县东北", "context": N("05-185", "下有临平湖")},
        },
    ],
)

item(
    "05-186",
    geo={
        "name": N("05-186", "海宁"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "杭州府", "rel": "领"},
        "note": "府东少北。元海宁州。洪武二年降为县。南滨海，有捍海塘。西南有赭山，与萧山县龛山相对，浙江经其中，东接大海，谓之海门。东南有石墩镇巡检司，本置县东北硖石镇，后迁于此，更名。西南有赭山镇巡检司，本置县西陈桥北，寻迁赭山，更名，又迁文堂山上，仍故名。又西北有长安镇",
    },
    ents=[
        {"text": N("05-186", "海宁"), "type": "place", "count": 1, "provenance": "条目名"},
        {"text": N("05-186", "海宁州"), "type": "place", "count": 1, "provenance": "元海宁州"},
        {"text": N("05-186", "捍海塘"), "type": "place", "count": 1, "provenance": "南滨海，有捍海塘"},
        {"text": N("05-186", "赭山"), "type": "place", "count": 1, "provenance": "西南有赭山"},
        {"text": N("05-186", "萧山县"), "type": "place", "count": 1, "provenance": "与萧山县龛山相对"},
        {"text": N("05-186", "龛山"), "type": "place", "count": 1, "provenance": "与萧山县龛山相对"},
        {"text": N("05-186", "浙江"), "type": "water", "count": 1, "provenance": "浙江经其中"},
        {"text": N("05-186", "大海"), "type": "water", "count": 1, "provenance": "东接大海"},
        {"text": N("05-186", "海门"), "type": "place", "count": 1, "provenance": "谓之海门"},
        {
            "text": N("05-186", "石墩镇巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "东南有石墩镇巡检司",
        },
        {"text": N("05-186", "硖石镇"), "type": "place", "count": 1, "provenance": "本置县东北硖石镇"},
        {
            "text": N("05-186", "赭山镇巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "西南有赭山镇巡检司",
        },
        {"text": N("05-186", "陈桥"), "type": "place", "count": 1, "provenance": "本置县西陈桥北"},
        {"text": N("05-186", "文堂山"), "type": "place", "count": 1, "provenance": "又迁文堂山上"},
        {"text": N("05-186", "长安镇"), "type": "place", "count": 1, "provenance": "又西北有长安镇"},
        {"text": N("05-186", "洪武"), "type": "era", "count": 1, "provenance": "洪武二年降为县"},
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 2,
            "era_raw": N("05-186", "洪武二年"),
            "category": "降秩",
            "event": N("05-186", "降为县"),
            "place": "海宁",
        },
    ],
    hyd=[
        {
            "name": N("05-186", "浙江"),
            "alt": "",
            "type": "河",
            "flow": N("05-186", "浙江经其中，东接大海，谓之海门"),
            "anchor": {"anchor": "海宁县西南", "context": N("05-186", "浙江经其中")},
        },
    ],
    gar=[
        {
            "name": N("05-186", "石墩镇巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "海宁县东南",
            "dusi": "未明",
            "note": "东南有石墩镇巡检司，本置县东北硖石镇，后迁于此，更名",
        },
        {
            "name": N("05-186", "赭山镇巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "海宁县西南",
            "dusi": "未明",
            "note": "西南有赭山镇巡检司，本置县西陈桥北，寻迁赭山，更名，又迁文堂山上，仍故名",
        },
    ],
)

item(
    "05-187",
    geo={
        "name": N("05-187", "富阳"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "杭州府", "rel": "领"},
        "note": "府西。东有观山。西南有湖洑山。东南临富春江，即钱塘江也。西南有东梓巡检司，后废",
    },
    ents=[
        {"text": N("05-187", "富阳"), "type": "place", "count": 1, "provenance": "条目名"},
        {"text": N("05-187", "观山"), "type": "place", "count": 1, "provenance": "东有观山"},
        {"text": N("05-187", "湖洑山"), "type": "place", "count": 1, "provenance": "西南有湖洑山"},
        {"text": N("05-187", "富春江"), "type": "water", "count": 1, "provenance": "东南临富春江"},
        {"text": N("05-187", "钱塘江"), "type": "water", "count": 1, "provenance": "即钱塘江也"},
        {
            "text": N("05-187", "东梓巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "西南有东梓巡检司，后废",
        },
    ],
    hyd=[
        {
            "name": N("05-187", "富春江"),
            "alt": "钱塘江",
            "type": "江",
            "flow": N("05-187", "东南临富春江，即钱塘江也"),
            "anchor": {"anchor": "富阳县东南", "context": N("05-187", "东南临富春江")},
        },
    ],
    gar=[
        {
            "name": N("05-187", "东梓巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "富阳县西南",
            "dusi": "未明",
            "note": "西南有东梓巡检司，后废",
        },
    ],
)

item(
    "05-188",
    geo={
        "name": N("05-188", "余杭"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "杭州府", "rel": "领"},
        "note": "府西北。西南有大涤山。西北有径山。南有苕溪，源出于潜县天目山。东北有石濑巡检司，后废",
    },
    ents=[
        {"text": N("05-188", "余杭"), "type": "place", "count": 1, "provenance": "条目名"},
        {"text": N("05-188", "大涤山"), "type": "place", "count": 1, "provenance": "西南有大涤山"},
        {"text": N("05-188", "径山"), "type": "place", "count": 1, "provenance": "西北有径山"},
        {"text": N("05-188", "苕溪"), "type": "water", "count": 1, "provenance": "南有苕溪"},
        {"text": N("05-188", "于潜县"), "type": "place", "count": 1, "provenance": "源出于潜县天目山"},
        {"text": N("05-188", "天目山"), "type": "place", "count": 1, "provenance": "源出于潜县天目山"},
        {
            "text": N("05-188", "石濑巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "东北有石濑巡检司，后废",
        },
    ],
    hyd=[
        {
            "name": N("05-188", "苕溪"),
            "alt": "",
            "type": "溪",
            "flow": N("05-188", "南有苕溪，源出于潜县天目山"),
            "anchor": {"anchor": "余杭县南", "context": N("05-188", "南有苕溪")},
        },
    ],
    gar=[
        {
            "name": N("05-188", "石濑巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "余杭县东北",
            "dusi": "未明",
            "note": "东北有石濑巡检司，后废",
        },
    ],
)

item(
    "05-189",
    geo={
        "name": N("05-189", "临安"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "杭州府", "rel": "领"},
        "note": "府西。旧治在县西西墅镇。洪武初徙于今所，本吴越衣锦军也。西有天目山，亦曰东天目，其在于潜境者为西天目。西北有南溪，即东苕溪也，源出天目山，经县南，亦曰新溪",
    },
    ents=[
        {"text": N("05-189", "临安"), "type": "place", "count": 1, "provenance": "条目名"},
        {"text": N("05-189", "西墅镇"), "type": "place", "count": 1, "provenance": "旧治在县西西墅镇"},
        {"text": N("05-189", "吴越"), "type": "system", "count": 1, "provenance": "本吴越衣锦军也"},
        {"text": N("05-189", "衣锦军"), "type": "institution", "count": 1, "provenance": "本吴越衣锦军也"},
        {"text": N("05-189", "天目山"), "type": "place", "count": 1, "provenance": "西有天目山"},
        {"text": N("05-189", "东天目"), "type": "place", "count": 1, "provenance": "亦曰东天目"},
        {"text": N("05-189", "于潜"), "type": "place", "count": 1, "provenance": "其在于潜境者为西天目"},
        {"text": N("05-189", "西天目"), "type": "place", "count": 1, "provenance": "其在于潜境者为西天目"},
        {"text": N("05-189", "南溪"), "type": "water", "count": 1, "provenance": "西北有南溪"},
        {"text": N("05-189", "东苕溪"), "type": "water", "count": 1, "provenance": "即东苕溪也"},
        {"text": N("05-189", "新溪"), "type": "water", "count": 1, "provenance": "亦曰新溪"},
        {"text": N("05-189", "洪武"), "type": "era", "count": 1, "provenance": "洪武初徙于今所"},
    ],
    tme=[
        {
            "reign": "洪武",
            "year": 0,
            "era_raw": N("05-189", "洪武初"),
            "category": "移治",
            "event": N("05-189", "徙于今所"),
            "place": "临安",
        },
    ],
    hyd=[
        {
            "name": N("05-189", "南溪"),
            "alt": "东苕溪",
            "type": "溪",
            "flow": N("05-189", "西北有南溪，即东苕溪也，源出天目山，经县南，亦曰新溪"),
            "anchor": {"anchor": "临安县西北", "context": N("05-189", "西北有南溪")},
        },
    ],
)

item(
    "05-190",
    geo={
        "name": N("05-190", "于潜"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "杭州府", "rel": "领"},
        "note": "府西。北有天目山，浮溪出焉。县南为紫溪，下流至桐卢县入浙江",
    },
    ents=[
        {"text": N("05-190", "于潜"), "type": "place", "count": 1, "provenance": "条目名"},
        {"text": N("05-190", "天目山"), "type": "place", "count": 1, "provenance": "北有天目山"},
        {"text": N("05-190", "浮溪"), "type": "water", "count": 1, "provenance": "北有天目山，浮溪出焉"},
        {"text": N("05-190", "紫溪"), "type": "water", "count": 1, "provenance": "县南为紫溪"},
        {"text": N("05-190", "桐卢县"), "type": "place", "count": 1, "provenance": "下流至桐卢县入浙江"},
        {"text": N("05-190", "浙江"), "type": "water", "count": 1, "provenance": "入浙江"},
    ],
    hyd=[
        {
            "name": N("05-190", "浮溪"),
            "alt": "",
            "type": "溪",
            "flow": N("05-190", "北有天目山，浮溪出焉"),
            "anchor": {"anchor": "于潜县北", "context": N("05-190", "浮溪出焉")},
        },
        {
            "name": N("05-190", "紫溪"),
            "alt": "",
            "type": "溪",
            "flow": N("05-190", "县南为紫溪，下流至桐卢县入浙江"),
            "anchor": {"anchor": "于潜县南", "context": N("05-190", "县南为紫溪")},
        },
    ],
)

item(
    "05-191",
    geo={
        "name": N("05-191", "新城"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "杭州府", "rel": "领"},
        "note": "府西南。西有葛溪，又东北有松溪合焉，至岘口入于浙江",
    },
    ents=[
        {"text": N("05-191", "新城"), "type": "place", "count": 1, "provenance": "条目名"},
        {"text": N("05-191", "葛溪"), "type": "water", "count": 1, "provenance": "西有葛溪"},
        {"text": N("05-191", "松溪"), "type": "water", "count": 1, "provenance": "又东北有松溪合焉"},
        {"text": N("05-191", "岘口"), "type": "place", "count": 1, "provenance": "至岘口入于浙江"},
        {"text": N("05-191", "浙江"), "type": "water", "count": 1, "provenance": "至岘口入于浙江"},
    ],
    hyd=[
        {
            "name": N("05-191", "葛溪"),
            "alt": "",
            "type": "溪",
            "flow": N("05-191", "西有葛溪，又东北有松溪合焉，至岘口入于浙江"),
            "anchor": {"anchor": "新城县西", "context": N("05-191", "西有葛溪")},
        },
    ],
)

item(
    "05-192",
    geo={
        "name": N("05-192", "昌化"),
        "level": "县",
        "node_type": "政区",
        "parent": {"text": "杭州府", "rel": "领"},
        "note": "府西。东南有柳相山。南有铜坑山。西北有千顷山。西有昱岭，上有关。又西北有黄花岭，上亦有关。东南有柳溪，东流合于于潜之紫溪。又有双溪，自县治南流入柳溪。西有手甗岭巡检司，迁县西南株柳村，又迁县西湛村，又迁杨家塘，仍故名",
    },
    ents=[
        {"text": N("05-192", "昌化"), "type": "place", "count": 1, "provenance": "条目名"},
        {"text": N("05-192", "柳相山"), "type": "place", "count": 1, "provenance": "东南有柳相山"},
        {"text": N("05-192", "铜坑山"), "type": "place", "count": 1, "provenance": "南有铜坑山"},
        {"text": N("05-192", "千顷山"), "type": "place", "count": 1, "provenance": "西北有千顷山"},
        {"text": N("05-192", "昱岭"), "type": "place", "count": 1, "provenance": "西有昱岭"},
        {"text": N("05-192", "黄花岭"), "type": "place", "count": 1, "provenance": "又西北有黄花岭"},
        {"text": N("05-192", "柳溪"), "type": "water", "count": 1, "provenance": "东南有柳溪"},
        {"text": N("05-192", "于潜"), "type": "place", "count": 1, "provenance": "合于于潜之紫溪"},
        {"text": N("05-192", "紫溪"), "type": "water", "count": 1, "provenance": "合于于潜之紫溪"},
        {"text": N("05-192", "双溪"), "type": "water", "count": 1, "provenance": "又有双溪，自县治南流入柳溪"},
        {
            "text": N("05-192", "手甗岭巡检司"),
            "type": "institution",
            "count": 1,
            "provenance": "西有手甗岭巡检司",
        },
        {"text": N("05-192", "株柳村"), "type": "place", "count": 1, "provenance": "迁县西南株柳村"},
        {"text": N("05-192", "湛村"), "type": "place", "count": 1, "provenance": "又迁县西湛村"},
        {"text": N("05-192", "杨家塘"), "type": "place", "count": 1, "provenance": "又迁杨家塘"},
    ],
    hyd=[
        {
            "name": N("05-192", "柳溪"),
            "alt": "",
            "type": "溪",
            "flow": N("05-192", "东南有柳溪，东流合于于潜之紫溪"),
            "anchor": {"anchor": "昌化县东南", "context": N("05-192", "东南有柳溪")},
        },
        {
            "name": N("05-192", "双溪"),
            "alt": "",
            "type": "溪",
            "flow": N("05-192", "又有双溪，自县治南流入柳溪"),
            "anchor": {"anchor": "昌化县", "context": N("05-192", "又有双溪")},
        },
    ],
    gar=[
        {
            "name": N("05-192", "手甗岭巡检司"),
            "type": "巡检司",
            "territorial": "未明",
            "established": {"reign": "未明", "year": 0, "era_raw": "未明"},
            "place": "昌化县西",
            "dusi": "未明",
            "note": "西有手甗岭巡检司，迁县西南株柳村，又迁县西湛村，又迁杨家塘，仍故名",
        },
    ],
)
