# -*- coding: utf-8 -*-
"""《水东日记》卷 26 —— APPT 职官任职 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "26-001 | 七言集句诗序", "26-002 | 于谦旧居", "26-003 | 刑律五品奏请",
    "26-004 | 张泰宁夏石彪", "26-005 | 国朝文物杜佑碑",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
DATA = [
    # ---- 26-002 于谦大理少卿 ----
    {"appointment_id": "APPT-13001", "item_id": "26-002",
     "person": {"text": "于谦", "person_ent_ids": []},
     "office": {"text": "大理寺少卿", "official_ent_ids": []},
     "institution": {"text": "大理寺", "ent_ids": []},
     "when": "未明", "status": "升迁",
     "evidence": "其自河南以大理少卿葬父回始相识",
     "confidence": 0.82},
    # ---- 26-004 张泰都督宁夏 ----
    {"appointment_id": "APPT-13002", "item_id": "26-004",
     "person": {"text": "张泰", "person_ent_ids": []},
     "office": {"text": "镇守宁夏都督", "official_ent_ids": []},
     "institution": {"text": "宁夏", "ent_ids": []},
     "when": "未明", "status": "现任",
     "evidence": "张泰都督宁夏石彪尝索古瓶于泰",
     "confidence": 0.82},
]
