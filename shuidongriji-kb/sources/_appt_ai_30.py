# -*- coding: utf-8 -*-
"""《水东日记》卷 30 —— APPT 职官任职 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "30-001~005 祭社稷、文天祥像、诛蚊赋、均徭朱熹书、写像",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
DATA = [
    # ---- 30-002 张遂郎中 ----
    {"appointment_id": "APPT-15001", "item_id": "30-002",
     "person": {"text": "张遂", "person_ent_ids": []},
     "office": {"text": "郎中", "official_ent_ids": []},
     "institution": {"text": "未明", "ent_ids": []},
     "when": "未明", "status": "现任",
     "evidence": "张遂郎中持文山像求题",
     "confidence": 0.8},
]
