# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - 枚举单点（_kg_enums.py）

全部启用层枚举的唯一权威来源（pitfalls.md #4：枚举收进单点文件，registerVersion 模式）。
基准：继承工厂 enum-library.md 规范值快照（本实例 schemas.md 锁定的版本）。
治理（#15/#27）：执行期未匹配值走「收集-报告-暂存」——入 pending 表不中断 -> 收尾决议
（新增/归并/改名）-> registerVersion+1 -> 回溯存量 -> 更新基准库与本快照。
验证脚本比对「文档口径 = 代码口径」（值种数 vs schema 定义数，比值 >1.5 判漂移告警）。

与基准库 v4 的差异注记（2026-10-11 客座赘语增量）：
  * ENTITY_TYPES 基准库 §1.1 已扩至 20 值（新增 star 星象 / event 事件名）。
    本实例 schemas.md §3 锁定的快照为 18 值；star/event 若在执行期出现，
    须先走 pending 决议（有原文证据 + 使用说明）再启用，禁止静默扩容。
  * EVENT_TYPES 基准库 §1.3.1 已扩至 27 顶层（新增 异闻/宗教/制度/沿革）。
    本实例 schemas.md §6 锁定顶层 23 值（笔记/轶事体只继承顶层）；同样走决议。
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# 版本治理
# ---------------------------------------------------------------------------
REGISTER_VERSION = 1  # 新增/归并/改名枚举后 +1，并回溯全部存量（dry-run 再 commit）

# ---------------------------------------------------------------------------
# 1. 实体类型 ENTITY_TYPES（schemas.md §3 快照，18 值；别名并入）
# ---------------------------------------------------------------------------
ENTITY_TYPES = {
    "person",
    "official",
    "institution",
    "place",
    "era",
    "work",
    "object",
    "animal",
    "plant",
    "food",
    "doc",
    "system",
    "behavior",
    "punishment",
    "time",
    "quantity",
    "posthumous",
    "unknown",
}
ENTITY_TYPES_ALIASES = {  # 各书历史值 → 规范值（回填通道，不新增规范值）
    "office": "official",
    "org": "institution",
    "book": "work",
    "artifact": "object",
}
ENTITY_TYPES_DOC = {
    "person": "人物",
    "official": "职官（别名 office）",
    "institution": "机构（别名 org）",
    "place": "地名",
    "era": "年号朝代",
    "work": "文献书名（别名 book）",
    "object": "名物（别名 artifact 器物）",
    "animal": "动物",
    "plant": "植物",
    "food": "饮食",
    "doc": "文书",
    "system": "制度",
    "behavior": "行为",
    "punishment": "刑罚",
    "time": "时间",
    "quantity": "数量",
    "posthumous": "谥号",
    "unknown": "类型待定（兜底）",
}

# ---------------------------------------------------------------------------
# 2. 任职状态 APPT_STATUS（schemas.md §4 快照，12 值）
# ---------------------------------------------------------------------------
APPT_STATUS = {
    "现任",
    "致仕",
    "升迁",
    "贬谪",
    "罢黜",
    "兼领",
    "暂代",
    "追赠",
    "未明",
    "起复",
    "世袭",
    "举荐",
}
APPT_STATUS_ALIASES = {}

# ---------------------------------------------------------------------------
# 3. 关系类型 REL_TYPES（schemas.md §5 快照，13 值）
# ---------------------------------------------------------------------------
REL_TYPES = {
    "同僚",
    "师生",
    "姻亲",
    "同乡",
    "同科",
    "举荐",
    "弹劾",
    "恩怨",
    "上下级",
    "父子亲属",
    "敌对",
    "同窗",
    "其他",
}
REL_TYPES_ALIASES = {"主从": "上下级"}

# 关系方向（非封闭枚举，但收在此处统一口径）
REL_DIRECTIONS = {"单向", "双向", "未明"}
REL_DIRECTIONS_ALIASES = {}

# ---------------------------------------------------------------------------
# 4. 事件类型 EVENT_TYPES（schemas.md §6 快照，顶层 23 值；不引入子类型）
# ---------------------------------------------------------------------------
EVENT_TYPES = {
    "朝政",
    "政变",
    "军事",
    "军政",
    "边事",
    "人事任免",
    "弹劾",
    "礼仪",
    "科举",
    "文事",
    "建言",
    "灾异",
    "轶事",
    "祭祀",
    "经济",
    "司法",
    "神异传说",
    "疾疫",
    "御灾赈济",
    "缉捕防盗",
    "巡查监察",
    "家事",
    "其他",
}
EVENT_TYPES_ALIASES = {
    "政事": "朝政",
    "军务": "军事",
    "科第": "科举",
    "刑罚": "司法",
    "祭祀仪礼": "祭祀",
}

# ---------------------------------------------------------------------------
# 5. 作者论说立场 OPN_STANCES（schemas.md §7 快照，5 值）
# ---------------------------------------------------------------------------
OPN_STANCES = {"肯定", "否定", "怀疑", "讽刺", "中立"}
OPN_STANCES_ALIASES = {}

# ---------------------------------------------------------------------------
# 6. 翻译风格 TRL_STYLES（schemas.md §8 快照，3 值）
# ---------------------------------------------------------------------------
TRL_STYLES = {"直译", "意译", "注释性翻译"}
TRL_STYLES_ALIASES = {}

# ---------------------------------------------------------------------------
# 统一注册表（打包器/验证脚本按层取枚举）
#   每项: {values: 封闭集, aliases: 别名映射, doc: 口径说明}
# ---------------------------------------------------------------------------
ENUM_REGISTRY = {
    "ent_type": {
        "values": ENTITY_TYPES,
        "aliases": ENTITY_TYPES_ALIASES,
        "doc": "L1 实体类型（18 值快照）",
    },
    "appt_status": {
        "values": APPT_STATUS,
        "aliases": APPT_STATUS_ALIASES,
        "doc": "APPT 任职状态（12 值快照）",
    },
    "rel_type": {
        "values": REL_TYPES,
        "aliases": REL_TYPES_ALIASES,
        "doc": "REL 关系类型（13 值快照）",
    },
    "rel_direction": {
        "values": REL_DIRECTIONS,
        "aliases": REL_DIRECTIONS_ALIASES,
        "doc": "REL 关系方向（3 值）",
    },
    "event_type": {
        "values": EVENT_TYPES,
        "aliases": EVENT_TYPES_ALIASES,
        "doc": "L5 事件类型（顶层 23 值快照）",
    },
    "opn_stance": {
        "values": OPN_STANCES,
        "aliases": OPN_STANCES_ALIASES,
        "doc": "OPN 论说立场（5 值快照）",
    },
    "trl_style": {
        "values": TRL_STYLES,
        "aliases": TRL_STYLES_ALIASES,
        "doc": "TRL 翻译风格（3 值快照）",
    },
}

# 源数据记录字段 → 枚举键的路由（打包器据此对记录字段做封闭集硬校验）
# 即各层源数据里哪些字段必须命中封闭枚举。
ENUM_FIELD_MAP = {
    "ent": [("type", "ent_type")],
    "appt": [("status", "appt_status")],
    "rel": [("relation_type", "rel_type"), ("direction", "rel_direction")],
    "event": [("type", "event_type")],
    "opn": [("stance", "opn_stance")],
    "trl": [("style", "trl_style")],
}
