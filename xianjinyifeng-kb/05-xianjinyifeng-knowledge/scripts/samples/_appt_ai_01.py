# -*- coding: utf-8 -*-
"""《先进遗风》APPT 职官任职层源数据样例（_appt_ai_01.py）

说明：
  * 顶层键固定为 appointments（列表）
  * 单条字段：
      item_id  必填，指纹库条号
      person   任职人（用规范化主名）
      office   官职/封爵名（原文有据）
      start    起始时间（原文无则写「未明」）
      end      结束时间（原文无则写「未明」）
      status   任职状态，封闭集 12 值（_kg_enums.APPT_STATUS）
      evidence 原文证据词（可留空，交给 V2 人工）
  * 只建模「原文明确提到」的任职；不写 original/业务 ID。
"""

appointments = [
    {
        "item_id": "01-001",
        "person": "宋濂",
        "office": "学士",
        "start": "未明",
        "end": "未明",
        "status": "现任",
        "evidence": "学士宋文宪公濓",
    },
    {
        "item_id": "01-039",
        "person": "王守仁",
        "office": "新建伯",
        "start": "未明",
        "end": "未明",
        "status": "追赠",
        "evidence": "新建伯文成王先生守仁",
    },
]
