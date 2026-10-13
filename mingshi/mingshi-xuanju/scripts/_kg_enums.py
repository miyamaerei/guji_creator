# -*- coding: utf-8 -*-
"""《明史·选举志》xjz 型枚举单点文件（与 references/schemas.md §3-§12 同源）。

继承工厂 enum-library 的树状基准值；本书新增的选举专属值（如 EXAM_TIERS 武科 tier）
已回溯进 schemas.md/SKILL.md，这里与文档保持一致。
封闭枚举一律 frozenset；越界值不中断，由 extract.py 收集进 pending 表统一决议。
"""

# —— L2 制度层 REG 选举 token ——
# 注：源文《选举志》卷45「选举之法，大略有四：曰学校，曰科目，曰荐举，曰铨选」，
# 学校为四法之一；贡举为岁贡/选贡/恩贡/纳贡机制（学校之亚），并存为独立 token。
SELECTION_TYPES = frozenset({"学校", "科目", "贡举", "荐举", "铨选"})
SCHOOL_TYPES = frozenset({"国学", "府州县学", "社学", "武学", "宗学", "其他"})
EXAM_TIERS = frozenset({
    "童试", "科考", "乡试", "会试", "殿试",
    "武乡试", "武会试", "武殿试", "未明",
})
REG_CATEGORIES_XJZ = frozenset({
    "学校制", "科举制", "荐举制", "铨选制",
    "保举", "考察考满", "武科", "其他",
})
REG_STATUS = frozenset({
    "初置", "定制", "遵行", "弊坏", "改革", "复设", "废罢", "未明",
})

# —— L4 四维 ——
EVO_STAGES = frozenset({
    "初置", "定制定型", "增改", "裁革", "复设", "变法", "弊坏", "复原", "未明",
})
QUAN_FORMS = frozenset({
    "解额", "会额", "监生额", "教官额", "生员额", "未明",
})

# —— 各层枚举 ——
TME_CATEGORIES = frozenset({
    "初置", "改置", "增员", "复设", "废置", "改称", "裁并", "移驻",
    "职掌变更", "升秩降秩", "未明", "定额变更", "法弊",
    "定制定型", "增改",
})
OPN_TYPES = frozenset({"奏议", "疏", "建言", "论", "驳议", "引书"})
OPN_CLAIM_MARKERS = frozenset({
    "请", "宜", "乞", "恐", "弊", "坏", "苦", "忧", "患", "不可",
    "非", "当", "议", "驳", "论", "言其", "疏论", "极言", "便",
})
NAM_TYPES = frozenset({"一甲题名", "考官题名", "进士题名", "监生名录"})
FRD_TYPES = frozenset({"冒籍", "倩代", "怀挟", "关节", "通榜", "其他"})
OBJ_CLASSES = frozenset({"文制", "场屋", "武科器械", "其他"})
EVT_TYPES_XJZ = frozenset({"科场案", "制度争议", "变革事件", "其他"})

# —— 实体 / 规则 / 机构 类型（本书定制）——
ENT_TYPES = frozenset({"机构", "学校", "职官", "人物", "地名", "书籍", "概念", "考场"})
RULE_TYPES = frozenset({"著为令", "不许", "禁", "凡", "例", "定制"})
STRUCT_TYPES = frozenset({"国学", "府州县学", "宗学", "社学", "武学", "机构", "考场", "其他"})

# —— 跨库联动（指向《明史》他志）——
CROSS_KB = frozenset({
    "mingshi-zhiguanzhi",   # 职官志（ORG/OFF）
    "mingshi-shihuozhi",    # 食货志（QUAN 科费/廪给）
    "mingshi-bingzhi",      # 兵志（武科/军职）
})
