# -*- coding: utf-8 -*-
"""《平平言》枚举单点（C5）。版本：1.0（2026-10-13 实例化）。
继承基准库快照（00-book-knowledge-factory/references/enum-library.md）+ lgs/xzl 归纳快照；
改值须 version+1 并双写 enum-changelog.md（缺一即野分支）。打包器只从本文件读，禁止内嵌字面量。"""

VERSION = "1.0"

# ---- 实体类型（继承基准库 20 值封闭全集；ENTITY_ACTIVE 为本书实际启用子集）----
ENTITY_TYPES = [
    "person", "official", "institution", "place", "era", "work",
    "object", "animal", "plant", "food", "doc", "system",
    "behavior", "punishment", "time", "quantity", "posthumous",
    "star", "event", "unknown",
]
ENTITY_ACTIVE = [
    "person", "official", "institution", "place", "era", "work",
    "doc", "system", "behavior", "punishment", "time", "quantity", "unknown",
]
ENTITY_ALIASES = {"office": "official", "org": "institution", "book": "work"}

# ---- 规则类型（继承基准库 7 值，中文键——与 lgs/xzl/fqh 一致）----
RULE_TYPES = ["禁止型", "义务型", "允许型", "程序型", "时限型", "处罚型", "优先级型"]
RULE_MODALS = ["必须", "禁止", "应该", "可以", "不必", "不得", "宜"]
RULE_TYPES_ALIAS = RULE_TYPES  # 兼容别名（历史文件用旧键）

# ---- 事件类型（继承基准库 §1.3 27 顶层，备用——本实例未启用 L5）----
EVENT_TYPES = [
    "朝政", "政变", "军事", "军政", "边事", "人事任免", "弹劾", "礼仪", "科举",
    "文事", "建言", "灾异", "轶事", "祭祀", "经济", "司法", "神异传说", "疾疫",
    "御灾赈济", "缉捕防盗", "巡查监察", "家事", "异闻", "宗教", "制度", "沿革", "其他",
]

# ---- 制度类型（政书英文键分支 v6，10 值）----
REG_TYPES = [
    "official_system", "selection_assessment", "fiscal", "justice_prison",
    "baojia_xiangyue", "education_sacrifice", "military", "post_transport",
    "governance", "other",
]

# ---- 论说立场（继承基准库 §1.8 5 值）----
OPN_STANCES = ["肯定", "否定", "怀疑", "讽刺", "中立"]
OPN_TYPES = OPN_STANCES  # 兼容别名（历史文件用旧键）

# ---- 结构化四维（继承 lgs/xzl 归纳快照，封闭 + 兜底 other）----
STRUCT_DIMS = ["ACT", "FRD", "LGR", "TME"]
ACT_TYPES = ["official", "justice_role", "clerk_role", "xiangyue_role", "other"]
FRD_TYPES = ["abuse", "guard", "evil_custom", "other"]
LGR_TYPES = ["ledger", "geye", "template_form", "board", "voucher", "other"]
TME_TYPES = ["deadline", "meeting", "assessment", "season", "age_limit", "other"]

# ---- 古今翻译层 TRL（工厂层库 C5：封闭 + 兜底）----
TRL_STYLES = ["直译", "意译", "注释性翻译"]

# ---- 枚举组登记表（打包器/校验器用）----
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
    "TRL": TRL_STYLES,
}
