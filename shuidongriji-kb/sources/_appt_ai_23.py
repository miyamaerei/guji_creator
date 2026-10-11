# -*- coding: utf-8 -*-
"""《水东日记》卷 23 —— APPT 职官任职 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "23-001 | 文彦博 翼城庙记", "23-002 | 许可用 中丞", "23-003 | 欧阳文忠公论鱼袋",
    "23-004 | 内府对类书", "23-005 | 王交山论寇准李纲", "23-006 | 古今文章精义",
    "23-007 | 孟氏祖庭碑磨字", "23-008 | 宦防录薏苡方",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
DATA = [
    # ---- 23-001 文彦博平章军国重事 ----
    {"appointment_id": "APPT-11501", "item_id": "23-001",
     "person": {"text": "文彦博", "person_ent_ids": []},
     "office": {"text": "太师平章军国重事", "official_ent_ids": []},
     "institution": {"text": "未明", "ent_ids": []},
     "when": "北宋", "status": "现任",
     "evidence": "太师平章军国重事潞国文忠烈公",
     "confidence": 0.85},
    # ---- 23-002 许可用中丞 ----
    {"appointment_id": "APPT-11502", "item_id": "23-002",
     "person": {"text": "许可用", "person_ent_ids": []},
     "office": {"text": "中丞（御史中丞）", "official_ent_ids": []},
     "institution": {"text": "未明", "ent_ids": []},
     "when": "元延祐初", "status": "现任",
     "evidence": "相台许可用中丞元延祐初科进士文章亦表著一时",
     "confidence": 0.82},
]
