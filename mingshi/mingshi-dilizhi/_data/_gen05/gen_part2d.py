# -*- coding: utf-8 -*-
"""卷05 分片2d生成器：以 data_part2 为底，仅抽取 05-091~104（data_part2 独占、未被
data_part2c 覆盖）按穷尽标准回填 ents / gar（AI 逐条审订，剔除扫描器噪声）。
输出 data_part2d.py（gen_main 合并时 ONLY 覆盖 05-091~104，不动 05-105~181）。"""

import copy
import io
import json
import os
import pprint
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from data_part2 import PART as BASE

reg = json.load(io.open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))


def N(iid, s):
    norm = reg[iid]["norm"]
    if s not in norm:
        raise SystemExit("[%s] 未命中 norm: %r" % (iid, s))
    return s


# 只取 data_part2 独占的 05-091~104（深拷，避免覆盖 05-105~181）
RANGE = ["05-%03d" % n for n in range(91, 105)]
D = {}
for iid in RANGE:
    if iid in BASE:
        D[iid] = copy.deepcopy(BASE[iid])


ADDED = {"ents": 0, "gar": 0}


def add_ent(iid, text, type_, prov):
    D[iid]["ents"].append({
        "text": N(iid, text),
        "type": type_,
        "count": 1,
        "provenance": prov,
    })
    ADDED["ents"] += 1


def add_gar(iid, name, type_, note=""):
    D[iid].setdefault("gar", []).append({
        "name": N(iid, name),
        "type": type_,
        "note": note or N(iid, name),
    })
    ADDED["gar"] += 1


# ---------- 05-091 安化 ----------
add_ent("05-091", "浮泥山", "place", "东有浮泥山")
add_ent("05-091", "大峰山", "place", "有大峰山")
add_ent("05-091", "辰山", "place", "西北有辰山")
add_ent("05-091", "善溪", "water", "又南有善溪，自武陵县流注于澬江")
add_ent("05-091", "武陵县", "place", "自武陵县流注于澬江")

# ---------- 05-092 茶陵州 ----------
add_ent("05-092", "酃县", "place", "自酃县流入")
add_ent("05-092", "江西永新县", "place", "源出江西永新县之景阳山")
add_ent("05-092", "景阳山", "place", "源出江西永新县之景阳山")
add_ent("05-092", "攸县", "place", "北入攸县之攸水")
add_ent("05-092", "茶水", "water", "又东南有茶水")
add_ent("05-092", "攸水", "water", "北入攸县之攸水")

# ---------- 05-094 武陵 ----------
add_ent("05-094", "荣王府", "institution", "弘治四年八月建荣王府")
add_ent("05-094", "善德山", "place", "东南有善德山")
add_ent("05-094", "郎口", "water", "又有朗水流入焉，谓之郎口")
add_ent("05-094", "朗水", "water", "又有朗水流入焉")
add_ent("05-094", "九溪卫", "institution", "自九溪卫流入")

# ---------- 05-095 桃源 ----------
add_ent("05-095", "壶头山", "place", "西有壶头山")
add_ent("05-095", "朗溪", "water", "东有朗溪")
add_ent("05-095", "泥溪", "water", "西南有泥溪")
add_ent("05-095", "高都巡检司", "institution", "又西南有高都巡检司")
add_gar("05-095", "高都巡检司", "巡检司", "又西南有高都巡检司")
add_ent("05-095", "白马巡检司", "institution", "又南有白马巡检司")
add_gar("05-095", "白马巡检司", "巡检司", "又南有白马巡检司")
add_ent("05-095", "苏溪", "place", "本名苏溪")
add_ent("05-095", "春村", "place", "治县东后春村")

# ---------- 05-096 龙阳 ----------
add_ent("05-096", "军山", "place", "东有军山")
add_ent("05-096", "鼎口", "water", "谓之鼎口")
add_ent("05-096", "鼎水", "water", "东北有鼎水流入焉")
add_ent("05-096", "赤沙湖", "water", "又东南有赤沙湖")
add_ent("05-096", "蠡湖", "water", "一名蠡湖")
add_ent("05-096", "鼎港口巡检司", "institution", "有鼎港口巡检司")
add_gar("05-096", "鼎港口巡检司", "巡检司", "有鼎港口巡检司")

# ---------- 05-097 沅江 ----------
add_ent("05-097", "龙阳州", "place", "元属龙阳州")
add_ent("05-097", "龙阳县", "place", "十年五月省入龙阳县")

# ---------- 05-099 衡阳 ----------
add_ent("05-099", "雍王府", "institution", "雍王府自四川保宁府迁此")
add_ent("05-099", "四川保宁府", "place", "雍王府自四川保宁府迁此")
add_ent("05-099", "桂王府", "institution", "万历二十九年十月建桂王府")
add_ent("05-099", "回雁峰", "place", "南有回雁峰")
add_ent("05-099", "岣嵝峰", "place", "北有岣嵝峰")
add_ent("05-099", "蒸口", "water", "谓之蒸口")
add_ent("05-099", "耒口", "water", "谓之耒口")
add_ent("05-099", "酃湖", "water", "又东有酃湖")
add_ent("05-099", "新城县", "place", "又东有新城县")
add_ent("05-099", "新城市", "place", "省为新城市")
add_ent("05-099", "江东巡检司", "institution", "江东巡检司治此")
add_gar("05-099", "江东巡检司", "巡检司", "江东巡检司治此")
add_ent("05-099", "松柏市巡检司", "institution", "西南有松柏市巡检司")
add_gar("05-099", "松柏市巡检司", "巡检司", "西南有松柏市巡检司")

# ---------- 05-100 衡山 ----------
add_ent("05-100", "攸县", "place", "自攸县合攸水流入境")
add_ent("05-100", "茶陵口", "water", "曰茶陵口")
add_ent("05-100", "祝融", "place", "峰之最大者曰祝融")
add_ent("05-100", "紫盖", "place", "峰之最大者曰祝融、紫盖")

# ---------- 05-101 耒阳 ----------
add_ent("05-101", "罗渡巡检司", "institution", "又西南有罗渡巡检司")
add_gar("05-101", "罗渡巡检司", "巡检司", "又西南有罗渡巡检司")

# ---------- 05-103 安仁 ----------
add_ent("05-103", "小江", "water", "南有小江水")
add_ent("05-103", "郴州", "place", "自郴州流入")
add_ent("05-103", "衡山县", "place", "西北流至衡山县")
add_ent("05-103", "潭湖", "water", "北有潭湖二巡检司")
add_gar("05-103", "潭湖", "巡检司", "北有潭湖二巡检司")


if __name__ == "__main__":
    with io.open(os.path.join(HERE, "data_part2d.py"), "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write('"""卷05 分片2d：05-091~104 穷尽回填（gen_part2d.py 生成）。"""\n\n')
        f.write("PART = ")
        f.write(pprint.pformat(D, width=100, indent=4))
        f.write("\n")
    print("PART2d done, items=%d ents=%d gar=%d" % (len(D), ADDED["ents"], ADDED["gar"]))
