# -*- coding: utf-8 -*-
"""卷05 分片1b生成器：以 data_part1 为底（05-001~090），按穷尽标准自动回填 ents / gar。
分类器：后缀定 type；巡检司/所/卫 同时入 gar；关/镇/堡/寨/隘/市 入 ent（gar 细化留 AI 精修）。
N() 硬校验；噪声（河岸描述/日期/截断）规则过滤，其余交人工修枝。输出 data_part1b.py。"""

import copy
import io
import json
import os
import pprint
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
from data_part1 import PART as BASE
import _gapscan as gs

reg = gs.reg


def N(iid, s):
    norm = reg[iid]["norm"]
    if s not in norm:
        raise SystemExit("[%s] 未命中 norm: %r" % (iid, s))
    return s


D = {iid: copy.deepcopy(rec) for iid, rec in BASE.items()}
ADDED = {"ents": 0, "gar": 0}

PLACE_SUF = "山岭峰崖岩矶洞石林洲岛原坂坪坡冈田村墟庄岭"
WATER_SUF = "江河湖溪水池塘潭浦荡湾泾浜津口港泽海川"
POLITY_SUF = "县州府郡路军省道城管城乡坞"


DROP_EXPLICIT = {"豫四州", "襄阳等三路", "河南江", "北岸对乌林", "迳山南襄河口",
                  "而东从山", "城内黄龙山", "通洞庭湖"}


def is_noise(cand):
    # 日期 / 河岸描述（方位+滨临隔通距 起首）/ 明显截断
    if any(ch in cand for ch in "年月日"):
        return True
    if "还湖" in cand or "还广" in cand or "还湖广" in cand:
        return True
    if re.match(r"^[东南西北中上下]*(滨|临|隔|距|通)", cand) and re.search(r"(江|大|湖|河|洞庭)$", cand):
        return True  # 河岸描述：临大江/北滨江/通大江/通洞庭湖…
    if cand in DROP_EXPLICIT:
        return True
    return False


def strip_prefix(cand):
    # 城X/县X/州X + 方位 → 去前2字（城内黄龙山→黄龙山）
    if len(cand) >= 3 and cand[0] in "城州县府司所卫路郡道省关镇堡寨" and cand[1] in "东南西北中上下":
        cand = cand[2:]
    return cand


def classify(cand):
    if cand.endswith("巡检司"):
        return "institution"
    if cand.endswith(("守御千户所", "千户所", "百户所")):
        return "institution"
    if cand.endswith("卫"):
        return "institution"
    if cand.endswith(("蛮夷官司",)):
        return "institution"
    if cand.endswith(tuple(POLITY_SUF)):
        return "place"
    if cand.endswith(tuple(PLACE_SUF)):
        return "place"
    if cand.endswith(tuple(WATER_SUF)):
        return "water"
    if cand.endswith(("宣慰司", "宣抚司", "安抚司", "长官司", "招讨司", "都司", "都卫", "军民宣慰使司")):
        return "institution"
    if cand.endswith(("镇", "关", "堡", "寨", "隘", "市", "驿", "台", "楼", "阁", "亭", "寺", "观", "庙", "院", "园", "庄")):
        return "institution"
    return "place"


def add_ent(iid, text, type_):
    D[iid].setdefault("ents", []).append({
        "text": N(iid, text), "type": type_, "count": 1,
        "provenance": "卷05穷尽回填",
    })
    ADDED["ents"] += 1


def add_gar(iid, name, type_):
    D[iid].setdefault("gar", []).append({
        "name": N(iid, name), "type": type_,
        "note": N(iid, name),
    })
    ADDED["gar"] += 1


for iid in sorted(D):
    rec = D[iid]
    norm = reg[iid]["norm"]
    cov = gs.covered_hard(rec)
    for c, n, pos in gs.candidates(norm):
        if c in cov or any(c in x or x in c for x in cov if len(x) >= 2):
            continue
        if is_noise(c):
            continue
        c = strip_prefix(c)
        if len(c) < 2:
            continue
        # 再查覆盖（strip 后可能已覆盖）
        if c in cov or any(c in x or x in c for x in cov if len(x) >= 2):
            continue
        kind = classify(c)
        add_ent(iid, c, kind)
        if kind == "巡检司":
            add_gar(iid, c, "巡检司")
        elif kind == "所":
            add_gar(iid, c, "千户所")
        elif kind == "卫":
            add_gar(iid, c, "卫")

# ---------- 人工补录：扫描器漏抽/被截断的真实实体 ----------
add_ent("05-001", "襄阳", "place")
add_ent("05-003", "黄龙山", "place")
add_ent("05-003", "大江", "water")

# ---------- 王府（藩府机构，扫描器抽成"XX年建X王府"短语，实为王府名）----------
add_ent("05-027", "郢王府", "institution")
add_ent("05-027", "梁王府", "institution")
add_ent("05-035", "景王府", "institution")
add_ent("05-051", "惠王府", "institution")
add_ent("05-081", "襄王府", "institution")


if __name__ == "__main__":
    with io.open(os.path.join(HERE, "data_part1b.py"), "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write('"""卷05 分片1b：05-001~090 穷尽回填（gen_part1b.py 自动生成+人工修枝）。"""\n\n')
        f.write("PART = ")
        f.write(pprint.pformat(D, width=100, indent=4))
        f.write("\n")
    print("PART1b done, items=%d ents=%d gar=%d" % (len(D), ADDED["ents"], ADDED["gar"]))
