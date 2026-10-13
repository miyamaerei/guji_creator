# -*- coding: utf-8 -*-
"""《先进遗风》L5 事件层源数据样例（_event_ai_01.py）

说明：
  * 顶层键固定为 events（列表），五元组式记录
  * 单条字段：
      item_id  必填，指纹库条号
      type     事件类型，封闭集顶层 23 值（_kg_enums.EVENT_TYPES）
      who      主体（规范化主名）
      action   行为/事件核心（原文概括）
      time     时间（原文无则「未明」）
      place    地点（原文无则「未明」）
      confidence 0-1（<0.8 入待核）
"""

events = [
    {
        "item_id": "01-008",
        "type": "轶事",
        "who": "杨溥",
        "action": "执政时询问其子沿途守令贤否，子言江陵令不贤",
        "time": "未明",
        "place": "京邸",
        "confidence": 0.85,
    },
    {
        "item_id": "01-039",
        "type": "司法",
        "who": "刑部",
        "action": "设提牢厅典守狱囚，月更一主政总其事",
        "time": "未明",
        "place": "未明",
        "confidence": 0.8,
    },
]
