# -*- coding: utf-8 -*-
"""《治谱》枚举单点（V1.0）——6 层方案（ent/rule/struct/reg/opn/trl + 跨层索引）。
继承基准库快照 + pingpingyan 归纳快照。执行期未匹配值走 V3 收集-报告-暂存。"""

# ============ ENTITY_TYPES 实体类型（继承基准库 §1.1 20 值） ============
ENTITY_TYPES = [
    "person", "official", "institution", "place", "era", "work", "object",
    "animal", "plant", "food", "doc", "system", "behavior", "punishment",
    "time", "quantity", "posthumous", "star", "event", "unknown",
]
# 本书启用子集：person/official/institution/place/era/work/doc/system/behavior/punishment/time/quantity/unknown

# ============ RULE_TYPES 规则类型（继承基准库 §1.2 7 值，中文键） ============
RULE_TYPES = ["禁止型", "义务型", "允许型", "程序型", "时限型", "处罚型", "优先级型"]
RULE_MODALS = ["必须", "禁止", "应该", "可以", "不必", "不得", "宜"]

# ============ REG_TYPES 制度类型（政书英文键分支 v6，10 值） ============
REG_TYPES = [
    "official_system", "selection_assessment", "fiscal", "justice_prison",
    "baojia_xiangyue", "education_sacrifice", "military", "post_transport",
    "governance", "other",
]

# ============ OPN_STANCES 作者论说立场（继承基准库 §1.8 5 值） ============
OPN_STANCES = ["肯定", "否定", "怀疑", "讽刺", "中立"]

# ============ TRL 翻译风格（沿用 pingpingyan build_trl 口径） ============
TRL_STYLES = ["注释性翻译", "直译", "意译"]

# ============ STRUCT 结构化四维（继承 lgs/xzl/ppy 快照，本书不新增值） ============
STRUCT_DIMS = ["ACT", "FRD", "LGR", "TME"]
ACT_TYPES = ["official", "justice_role", "clerk_role", "xiangyue_role", "other"]
FRD_TYPES = ["abuse", "guard", "evil_custom", "other"]
LGR_TYPES = ["ledger", "geye", "template_form", "board", "voucher", "other"]
TME_TYPES = ["deadline", "meeting", "assessment", "season", "age_limit", "other"]

# ============ 枚举组登记表（打包器/校验器用） ============
ENUM_GROUPS = {
    "ENTITY": ENTITY_TYPES,
    "RULE": RULE_TYPES,
    "REG": REG_TYPES,
    "OPN": OPN_STANCES,
    "ACT": ACT_TYPES,
    "FRD": FRD_TYPES,
    "LGR": LGR_TYPES,
    "TME": TME_TYPES,
    "TRL": TRL_STYLES,
}

VERSION = "1.0"
