# -*- coding: utf-8 -*-
"""《宛署杂记》知识工程 枚举单点（C5）

规则：
- 所有枚举值只从这里读，禁止内嵌在打包器/源数据里（C5）。
- 封闭集 + 归类型必带兜底值（other / unknown / 其他）。
- 打包器对未注册值记 ERR，不静默放行。
- 改值 = registerVersion+1 并回溯存量；入库须双写 enum-library.md + enum-changelog.md。
"""
VERSION = "1.0"

# ============ ENTITY_TYPES 实体类型（继承基准库 §1.1 快照 20 值） ============
ENTITY_TYPES = [
    "person", "official", "institution", "place", "era", "work", "object",
    "animal", "plant", "food", "doc", "system", "behavior", "punishment",
    "time", "quantity", "posthumous", "star", "event", "unknown",
]
# 本书实际启用子集（未启用的保留在封闭全集中）
ENTITY_ACTIVE = [
    "person", "official", "institution", "place", "era", "work", "object",
    "doc", "system", "behavior", "punishment", "quantity", "unknown",
]

# ============ APPT_STATUS 任职状态（继承基准库 §1.10 快照 12 值） ============
APPT_STATUS = [
    "现任", "致仕", "升迁", "贬谪", "罢黜", "兼领", "暂代",
    "追赠", "未明", "起复", "世袭", "举荐",
]

# ============ EVENT_TYPES 事件类型（继承基准库 §1.3 顶层 27 值，中文） ============
EVENT_TYPES = [
    "朝政", "政变", "军事", "军政", "边事", "人事任免", "弹劾", "礼仪",
    "科举", "文事", "建言", "灾异", "轶事", "祭祀", "经济", "司法",
    "神异传说", "疾疫", "御灾赈济", "缉捕防盗", "巡查监察", "家事",
    "异闻", "宗教", "制度", "沿革", "其他",
]

# ============ LIT_TYPES 文献类型（继承基准库 §1.11 四部树快照，本书启用子集） ============
LIT_TYPES = [
    # 史部
    "诏令奏议", "碑记", "方志", "传记", "杂史",
    # 集部
    "诗", "文", "记", "序跋", "题跋", "赋", "词",
    # 子部/经部
    "经书", "笔记", "杂学",
    # 兜底
    "其他",
]

# ============ REG_TYPES 制度类型（基准库 §1.12 中文值 + 本书归纳增量，封闭+兜底） ============
REG_TYPES = [
    "朝仪", "官制", "铨选考课", "赋役", "礼仪", "祭祀", "科举", "司法",
    "财政", "军政", "民政救济", "宫禁内府", "其他",
]

# ============ NAM_TYPES 名录类型（继承基准库 §1.5 快照，本书启用子集） ============
NAM_TYPES = [
    "官员题名", "题名记", "人物", "文人", "僧侣", "皇族", "其他",
]

# ============ OPN_STANCES 作者论说立场（继承基准库 §1.8 快照 5 值） ============
OPN_STANCES = [
    "肯定", "否定", "怀疑", "讽刺", "中立",
]

# ============ CUS_TYPES 方言风俗类型（继承基准库 §1.7 快照 12 值） ============
CUS_TYPES = [
    "方言词", "民俗", "禁忌", "谚语", "节令", "物产习俗", "婚丧",
    "信仰祭祀", "称谓", "风尚", "技艺", "其他",
]

# ============ GEO_TYPES 地理古迹类型（继承基准库 §1.17 快照，本书启用子集） ============
GEO_TYPES = [
    "山水", "寺观祠庙", "桥渡", "都邑宫阙", "陵墓", "水利沟渠",
    "园第坊巷", "政区", "其他",
]

# ============ 枚举组登记表（打包器/校验器用） ============
ENUM_GROUPS = {
    "ENTITY": ENTITY_TYPES,
    "APPT": APPT_STATUS,
    "EVENT": EVENT_TYPES,
    "LIT": LIT_TYPES,
    "REG": REG_TYPES,
    "NAM": NAM_TYPES,
    "OPN": OPN_STANCES,
    "CUS": CUS_TYPES,
    "GEO": GEO_TYPES,
}

# 兼容别名：打包器按 <GROUP>_TYPES 取枚举集（C5 单点）
APPT_TYPES = APPT_STATUS
OPN_TYPES = OPN_STANCES
