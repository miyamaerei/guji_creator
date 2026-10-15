# -*- coding: utf-8 -*-
"""《吕公实政录》枚举单点（C5）。版本：1.0（2026-10-12 实例化）。
继承基准库快照（00-book-knowledge-factory/references/enum-library.md v4）+ 本书归纳增量；
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

# ---- 规则类型（继承基准库 7 值封闭全集）----
RULE_TYPES = ["prohibit", "obligation", "allow", "procedure", "deadline", "penalty", "priority"]
RULE_TYPES_ZH = {"prohibit": "禁止型", "obligation": "义务型", "allow": "允许型",
                 "procedure": "程序型", "deadline": "时限型", "penalty": "处罚型", "priority": "优先级型"}

# ---- 结构化四维类型（本书归纳，封闭 + 兜底 other）----
ACT_TYPES = ["official", "xiangyue_role", "justice_role", "clerk_role", "other"]
ACT_TYPES_ZH = {"official": "官职", "xiangyue_role": "乡约角色", "justice_role": "司法刑狱角色",
                "clerk_role": "文书角色", "other": "其他"}

FRD_TYPES = ["abuse", "guard", "evil_custom", "other"]
FRD_TYPES_ZH = {"abuse": "积弊", "guard": "防弊措施", "evil_custom": "恶风禁忌", "other": "其他"}

LGR_TYPES = ["ledger", "geye", "template_form", "board", "voucher", "other"]
LGR_TYPES_ZH = {"ledger": "簿册", "geye": "格叶", "template_form": "状式",
                "board": "榜牌", "voucher": "单据", "other": "其他"}

TME_TYPES = ["deadline", "meeting", "assessment", "season", "age_limit", "other"]
TME_TYPES_ZH = {"deadline": "期限", "meeting": "会期", "assessment": "考绩期",
                "season": "节令农时", "age_limit": "年龄时限", "other": "其他"}

# ---- 结构化维度枚举（C4 登记）----
STRUCT_DIMS = ["ACT", "FRD", "LGR", "TME"]

# ---- 古今翻译层 TRL（工厂层库 C5：封闭 + 兜底）----
TRL_STYLES = ["直译", "意译", "注释性翻译"]
