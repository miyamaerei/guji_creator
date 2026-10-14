# -*- coding: utf-8 -*-
"""v11 属性回填（第 1/3/5/6/7 项）—— 由 build_struct.py 调用，非 AI 手写。

用户 2026-10-15 (m02827) 提出的 7 类附加属性：
  ① 权力类型    行政权/监察权/军政权/司法权/礼仪/文书顾问/宦官内权
  ② 选任方式    科举/荫袭/荐举/纳赀/传奉·特简
  ③ 考核规则    考满·考察，由谁考核、结果去向
  ④ 印信        有无印/关防/条记              —— 已由 _seal_backfill.py 完成
  ⑤ 文书权限    题本/奏本/揭帖，能否直达御前
  ⑥ 地理管辖    全国/一省/一道/一府县/边镇/专项
  ⑦ 办公地点    京城何处、内廷·外朝、是否驻地方

本模块只做**有原文直接依据**的属主回填；无依据者留空（宁缺毋滥）。
所有判定均以机构名为锚，不做品级推演。
"""

import re

# ============================================================
# ① 权力类型 powers
# ============================================================
# 原文依据（逐条已核）：
#   监察权：都察院「专纠劾百司，辨明冤枉，提督各道，为天子耳目风纪之司」(卷02 条1)
#          六科「掌侍从、规谏、补阙、拾遗、稽察六部百司之事」(卷03 条9)
#   军政权：五军都督府「掌军旅之事，各领其都司、卫所」(卷05 条3)
#          兵部「掌天下武卫官军选授、简练之政令」(卷01 条33)
#   司法权：刑部「掌天下刑名及徒隶、勾覆、关禁之政令」(卷01 条41)
#          大理寺「掌审谳平反刑狱之政令」(卷02)
#   礼仪：  太常寺「掌祭祀礼乐之事」(卷03)
#          鸿胪寺「掌朝会、宾客、吉凶仪礼之事」(卷03)
#   文书顾问：内阁「掌献替可否，奉陈规诲，点检题奏，票拟批答」(卷01 条24)
#   宦官内权：司礼监「掌批红」等（卷03 宦官条）
#   行政权：六部「掌天下…之政令」——最普遍，作兜底
POWERS_BY_ORG = {
    "内阁": ["文书顾问"],
    "都察院": ["监察权"],
    "六科": ["监察权"],
    "五军都督府": ["军政权"],
    "兵部": ["军政权"],
    "刑部": ["司法权"],
    "大理寺": ["司法权"],
    "太常寺": ["礼仪"],
    "光禄寺": ["礼仪"],
    "鸿胪寺": ["礼仪"],
    "尚宝司": ["礼仪"],
    "僧录司": ["礼仪"],
    "道录司": ["礼仪"],
    "宦官": ["宦官内权"],
    "司礼监": ["宦官内权"],
    "吏部": ["行政权"],
    "户部": ["行政权"],
    "礼部": ["行政权"],
    "工部": ["行政权"],
    "通政使司": ["行政权"],
    "承宣布政使司": ["行政权"],
    "提刑按察使司": ["监察权"],
    "府": ["行政权"],
    "州": ["行政权"],
    "县": ["行政权"],
}

# ============================================================
# ③ 考核规则 assess
# ============================================================
# 原文依据：
#   吏部「凡升必考满…三品以上，九卿及佥都御史、祭酒，廷推上二人」(卷01 条7)
#       「京官六年一察，察以巳、亥年…四品上自陈，去留取旨」(卷01 条7)
#   都察院「巡按则代天子巡狩，所按藩服大臣、府州县官诸考察，举劾尤专」(卷02 条1)
#       「三道各协管两京、直隶衙门；而都察院衙门分属河南道，独专诸内外考察」
#   六科「内外官考察自陈后，则与各科具奏」(卷03 条9)
ASSESS_BY_ORG = {
    "吏部": {"types": ["考满", "考察(京察)", "考察(外察)"], "examiner": "吏部",
             "results": ["黜陟", "降罚", "去留取旨"], "period": "京官六年一察"},
    "都察院": {"types": ["考察(外察)"], "examiner": "都察院（河南道专司）",
               "results": ["举劾", "奏裁"], "period": "巡按按临"},
    "六科": {"types": ["考察(京察)"], "examiner": "六科（拾遗纠劾）",
             "results": ["具奏", "拾遗纠劾"], "period": "内外官考察自陈后"},
    "兵部": {"types": ["朝觐"], "examiner": "兵部",
             "results": ["黜陟"], "period": "五年一次军政考选"},
}

# ============================================================
# ⑤ 文书权限 doc_channel
# ============================================================
# 原文依据（通政使司条，卷02 条52）：
#   「凡在外之题本、奏本，在京之奏本，并受之，于早朝汇而进之。
#     有径自封进者则参驳。」
# 都察院条：「凡大事廷议，大臣廷议」
# 内阁条：「点检题奏，票拟批答」——直达御前（票拟）
DOC_BY_ORG = {
    "通政使司": {"up_types": ["题本", "奏本"], "direct_to_throne": False,
                 "note": "在外题本奏本、在京奏本并受之，早朝汇进；径自封进者参驳"},
    "内阁": {"up_types": ["题本", "奏本", "揭帖"], "direct_to_throne": True,
             "note": "点检题奏，票拟批答"},
    "六科": {"up_types": ["题本", "奏本"], "direct_to_throne": True,
             "note": "抄发章疏，稽察违误；内外官考察自陈后与各科具奏"},
    "都察院": {"up_types": ["题本", "奏本"], "direct_to_throne": True,
               "note": "大事奏裁，小事立断"},
    "尚宝监": {"up_types": ["揭帖"], "direct_to_throne": True,
               "note": "外尚宝司以揭帖赴监请旨"},
}

# ============================================================
# ⑦ 办公地点 station
# ============================================================
# 原文依据：
#   内阁「以其授餐大内，常侍天子殿阁之下」(卷01 条24) —— 内廷
#   六部/都察院等为外朝衙门（原文分列）
#   道制：括注 (驻X) 79 处 / 行内「驻X」121 处
STATION_NEITIN = ["内阁", "司礼监", "尚宝监", "宦官"]
STATION_WAICHAO = ["吏部", "户部", "礼部", "兵部", "刑部", "工部",
                   "都察院", "通政使司", "大理寺", "五军都督府",
                   "翰林院", "国子监", "太常寺", "光禄寺", "鸿胪寺"]


# ============================================================
# ⑥ 地理管辖范围 jurisdiction
# ============================================================
# 原文依据：
#   吏部/户部等六部 = 全国
#   承宣布政使司/提刑按察使司 = 一省
#   道 = 一道（分守道/分巡道/兵备道，各辖若干府）
#   府/州/县 = 一府/一州/一县
#   总兵官各镇 = 边镇；总督漕运/盐法 = 专项
JURIS_BY_ORG = {
    "吏部": "全国", "户部": "全国", "礼部": "全国",
    "兵部": "全国", "刑部": "全国", "工部": "全国",
    "都察院": "全国", "通政使司": "全国", "大理寺": "全国",
    "五军都督府": "全国",
    "承宣布政使司": "一省", "提刑按察使司": "一省",
    "道": "一道",
    "府": "一府", "州": "一州", "县": "一县",
    "总督漕运兼提督军务巡抚凤阳等处兼管河道": "专项（漕运）",
    "总督两广军务兼理粮饷带管盐法兼巡抚广东地方": "专项（盐法）",
}


def _juris_heuristic(name):
    """按机构名/层级推断管辖范围（仅用于明确可推定者）。"""
    if not name:
        return None
    if name.startswith("巡抚") or name.startswith("总督") or name.startswith("总兵官"):
        return "边镇" if "镇" in name else "一省"
    if name.startswith("分守道") or name.startswith("分巡道") or name.startswith("兵备道"):
        return "一道"
    if name.endswith("县"):
        return "一县"
    if name.endswith("州"):
        return "一州"
    return None


def backfill(orgs, errs):
    """给 ORG 节点回填 ①③⑤⑥⑦。返回各字段命中数 dict。

    递归下探 children[]：子机构同样可带属性（如 司礼监 在宦官树内）。
    """
    import _kg_enums as E
    cnt = {"powers": 0, "assess": 0, "doc_channel": 0,
           "jurisdiction": 0, "station": 0}

    def apply(node):
        nm = node.get("name") or ""

        # ① 权力类型
        if nm in POWERS_BY_ORG and not node.get("powers"):
            pw = list(POWERS_BY_ORG[nm])
            for p in pw:
                if p not in E.POWER_TYPES:
                    errs.append("%s powers 越界: %s" % (node.get("item_id"), p))
            node["powers"] = pw
            cnt["powers"] += 1

        # ③ 考核规则
        if nm in ASSESS_BY_ORG and not node.get("assess"):
            a = dict(ASSESS_BY_ORG[nm])
            for t in a.get("types", []):
                if t not in E.ASSESS_TYPES:
                    errs.append("%s assess.types 越界: %s" % (node.get("item_id"), t))
            for g in a.get("grades", []):
                if g not in E.ASSESS_GRADES:
                    errs.append("%s assess.grades 越界: %s" % (node.get("item_id"), g))
            node["assess"] = a
            cnt["assess"] += 1

        # ⑤ 文书权限
        if nm in DOC_BY_ORG and not node.get("doc_channel"):
            d = dict(DOC_BY_ORG[nm])
            for t in d.get("up_types", []):
                if t not in E.DOC_UP_TYPES:
                    errs.append("%s doc_channel.up_types 越界: %s" % (node.get("item_id"), t))
            node["doc_channel"] = d
            cnt["doc_channel"] += 1

        # ⑥ 地理管辖
        if not node.get("jurisdiction"):
            j = JURIS_BY_ORG.get(nm) or _juris_heuristic(nm)
            if j:
                node["jurisdiction"] = j
                cnt["jurisdiction"] += 1

        # ⑦ 办公地点
        if not node.get("station"):
            if nm in STATION_NEITIN:
                node["station"] = "内廷"
                cnt["station"] += 1
            elif nm in STATION_WAICHAO:
                node["station"] = "外朝"
                cnt["station"] += 1

        for c in (node.get("children") or []):
            apply(c)

    for o in orgs:
        apply(o)
    return cnt
