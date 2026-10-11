# -*- coding: utf-8 -*-
"""《水东日记》卷 37 —— APPT 职官任职 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "37-001~006 瀛国公诗、刘江杀倭、王恽纪梦、志石昭穆、试马、药方",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
DATA = [
    # ---- 37-002 刘江中军左都督总兵镇辽东 ----
    {"appointment_id": "APPT-18501", "item_id": "37-002",
     "person": {"text": "刘江（刘荣）", "person_ent_ids": []},
     "office": {"text": "中军左都督总兵官", "official_ent_ids": []},
     "institution": {"text": "辽东", "ent_ids": []},
     "when": "永乐间", "status": "现任",
     "evidence": "国朝名将刘江以中军左都督总兵镇辽东杀倭寇",
     "confidence": 0.85},
]
