# -*- coding: utf-8 -*-
"""《水东日记》卷 26 —— REL 人物关系 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "26-001 | 七言集句诗序", "26-002 | 于谦旧居", "26-003 | 刑律五品奏请",
    "26-004 | 张泰宁夏石彪", "26-005 | 国朝文物杜佑碑",
]

# 字段键（打包器校验用）：rel_id, item_id, person_a, person_b, relation_type, direction, evidence, confidence
DATA = [
    # ---- 26-002 于谦与叶盛邻 ----
    {"rel_id": "REL-13001", "item_id": "26-002",
     "person_a": {"text": "于谦", "person_a_ent_ids": []},
     "person_b": {"text": "叶盛", "person_b_ent_ids": []},
     "relation_type": "同僚", "direction": "双向",
     "evidence": "于节庵公旧居小苏州巷与余南北隣……后为余妻金氏作墓表",
     "confidence": 0.85},
    # ---- 26-004 石彪衔张泰 ----
    {"rel_id": "REL-13002", "item_id": "26-004",
     "person_a": {"text": "石彪", "person_a_ent_ids": []},
     "person_b": {"text": "张泰", "person_b_ent_ids": []},
     "relation_type": "恩怨", "direction": "单向",
     "evidence": "石彪尝索古瓶于泰泰不与彪衔之",
     "confidence": 0.82},
]
