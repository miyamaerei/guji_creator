# -*- coding: utf-8 -*-
"""《政学录》枚举单点。版本：1.1（2026-10-12 增量：+REG_TYPES 制度类型、+EVENT_TYPES 事件类型 27 顶层）。
继承基准库快照（enum-library.md v5）+ 《吕公实政录》归纳快照 + 本书归纳；改值须 version+1 并双写 enum-changelog.md。"""

VERSION = "1.1"

ENTITY_TYPES = [
    "person", "official", "institution", "place", "era", "work",
    "object", "animal", "plant", "food", "doc", "system",
    "behavior", "punishment", "time", "quantity", "posthumous",
    "star", "event", "unknown",          # 基准库 20 值封闭全集
]
ENTITY_ACTIVE = ["person", "official", "institution", "place", "era", "work",
                 "doc", "system", "behavior", "punishment", "time", "quantity", "unknown"]
ENTITY_ALIASES = {"office": "official", "org": "institution", "book": "work"}

RULE_TYPES = ["prohibit", "obligation", "allow", "procedure", "deadline", "penalty", "priority"]
RULE_TYPES_ZH = {"prohibit": "禁止型", "obligation": "义务型", "allow": "允许型",
                 "procedure": "程序型", "deadline": "时限型", "penalty": "处罚型", "priority": "优先级型"}

STRUCT_DIMS = ["ACT", "FRD", "LGR", "TME"]

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

# 制度层类型（本书归纳，封闭+兜底；v1.1 新增）
REG_TYPES = ["official_system", "selection_assessment", "fiscal", "justice_prison",
             "baojia_xiangyue", "education_sacrifice", "military", "post_transport",
             "governance", "other"]
REG_TYPES_ZH = {"official_system": "官制", "selection_assessment": "铨选考课", "fiscal": "钱粮赋役",
                "justice_prison": "刑名狱政", "baojia_xiangyue": "保甲乡约", "education_sacrifice": "文教祀典",
                "military": "军政边防", "post_transport": "驿递河工", "governance": "吏治政术", "other": "其他"}

# 事件层类型：继承基准库 enum-library.md §1.3 顶层 27 值（封闭+兜底；v1.1 新增）
EVENT_TYPES = ["politics", "coup", "military", "military_admin", "border", "personnel",
               "impeachment", "ritual", "examination", "culture", "remonstrance", "calamity",
               "anecdote", "sacrifice", "economy", "justice", "supernatural", "epidemic",
               "disaster_relief", "police", "inspection", "family", "odd_tales", "religion",
               "institution_change", "evolution", "other"]
EVENT_TYPES_ZH = {"politics": "朝政", "coup": "政变", "military": "军事", "military_admin": "军政",
                  "border": "边事", "personnel": "人事任免", "impeachment": "弹劾", "ritual": "礼仪",
                  "examination": "科举", "culture": "文事", "remonstrance": "建言", "calamity": "灾异",
                  "anecdote": "轶事", "sacrifice": "祭祀", "economy": "经济", "justice": "司法",
                  "supernatural": "神异传说", "epidemic": "疾疫", "disaster_relief": "御灾赈济",
                  "police": "缉捕防盗", "inspection": "巡查监察", "family": "家事", "odd_tales": "异闻",
                  "religion": "宗教", "institution_change": "制度", "evolution": "沿革", "other": "其他"}
