# -*- coding: utf-8 -*-
"""《福惠全书》枚举单点（V1.0）——8 层方案（ent/rule/struct/reg/opn/proc/doc/rel + 跨层索引）。
继承基准库快照 + 本书归纳（DOC_TYPES 8 / REL_TYPES 角色版）。执行期未匹配值走 V3 收集。"""

# ============ ENTITY_TYPES 实体类型（继承基准库 §1.1 20 值） ============
ENTITY_TYPES = [
    "person", "official", "institution", "place", "era", "work", "object",
    "animal", "plant", "food", "doc", "system", "behavior", "punishment",
    "time", "quantity", "posthumous", "star", "event", "unknown",
]

# ============ RULE_TYPES 规则类型（继承基准库 §1.2 7 值） ============
RULE_TYPES = [
    "禁止型", "义务型", "允许型", "程序型", "时限型", "处罚型", "优先级型",
]
RULE_MODALS = [
    "必须", "禁止", "应该", "可以", "不必", "不得", "宜",
]

# ============ EVENT_TYPES 事件类型（继承基准库 §1.3 27 顶层，备用） ============
EVENT_TYPES = [
    "朝政", "政变", "军事", "军政", "边事", "人事任免", "弹劾", "礼仪", "科举",
    "文事", "建言", "灾异", "轶事", "祭祀", "经济", "司法", "神异传说", "疾疫",
    "御灾赈济", "缉捕防盗", "巡查监察", "家事", "异闻", "宗教", "制度", "沿革", "其他",
]

# ============ REG_TYPES 制度类型（政书英文键分支 v6，10 值） ============
REG_TYPES = [
    "official_system", "selection_assessment", "fiscal", "justice_prison",
    "baojia_xiangyue", "education_sacrifice", "military", "post_transport",
    "governance", "other",
]

# ============ OPN_STANCES 作者论说立场（继承基准库 5 值） ============
OPN_STANCES = [
    "肯定", "否定", "怀疑", "讽刺", "中立",
]

# ============ STRUCT 结构化四维（继承 lgs/xzl 归纳快照，本书不新增值） ============
STRUCT_DIMS = ["ACT", "FRD", "LGR", "TME"]
ACT_TYPES = ["official", "xiangyue_role", "justice_role", "clerk_role", "other"]
FRD_TYPES = ["abuse", "guard", "evil_custom", "other"]
LGR_TYPES = ["ledger", "geye", "template_form", "board", "voucher", "other"]
TME_TYPES = ["deadline", "meeting", "assessment", "season", "age_limit", "other"]

# ============ DOC_TYPES 文书类型（本书归纳 8 类，封闭+兜底） ============
DOC_TYPES = [
    "状词", "票单", "册簿", "牌批", "谕告", "结状", "启禀", "其他",
]

# ============ REL_TYPES 关系类型（C3 12 值 + 本书角色类，封闭+兜底） ============
REL_TYPES = [
    "同僚", "师生", "姻亲", "同乡", "同科", "举荐", "弹劾", "恩怨",
    "上下级", "父子亲属", "敌对", "保甲隶属", "吏役职责", "诉讼三方", "幕宾聘用", "其他",
]

# ============ 枚举组登记表（打包器/校验器用） ============
ENUM_GROUPS = {
    "ENTITY": ENTITY_TYPES,
    "RULE": RULE_TYPES,
    "EVENT": EVENT_TYPES,
    "REG": REG_TYPES,
    "OPN": OPN_STANCES,
    "ACT": ACT_TYPES,
    "FRD": FRD_TYPES,
    "LGR": LGR_TYPES,
    "TME": TME_TYPES,
    "DOC": DOC_TYPES,
    "REL": REL_TYPES,
}

# 兼容别名（历史文件用旧键）
RULE_TYPES_ALIAS = RULE_TYPES
OPN_TYPES = OPN_STANCES
RELATION_TYPES = REL_TYPES

VERSION = "1.0"
