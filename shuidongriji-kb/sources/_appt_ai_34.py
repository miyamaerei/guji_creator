# -*- coding: utf-8 -*-
"""《水东日记》卷 34 —— APPT 职官任职（S4 片填写）

题名表 122 人官职已由 NAM-17001 entries.office 整体承载；本层只抽叙事中有明确任职句者。
"""

DATA = [
    {"appointment_id": "APPT-17001", "item_id": "34-006",
     "person": {"text": "叶盛", "person_ent_ids": ["ENT-036"]},
     "office": {"text": "协赞边外军务", "official_ent_ids": []},
     "institution": {"text": "宣府", "ent_ids": []},
     "when": "景泰三年夏至", "status": "现任",
     "evidence": "予自景泰三年夏至宣府，十一日奉敕协赞徼外军务；天顺八年秋以巡抚重临上谷", "confidence": 0.9},
    {"appointment_id": "APPT-17002", "item_id": "34-002",
     "person": {"text": "陈芜（王瑾）", "person_ent_ids": []},
     "office": {"text": "御用监太监", "official_ent_ids": []},
     "institution": {"text": "内府", "ent_ids": []},
     "when": "永乐丁亥入内府，宣庙御极陞太监", "status": "现任",
     "evidence": "御用监太监陈芜，交阯人，永乐丁亥入内府；既御极，陞太监，赐姓名曰王瑾，字润德", "confidence": 0.9},
    {"appointment_id": "APPT-17003", "item_id": "34-006",
     "person": {"text": "李秉", "person_ent_ids": []},
     "office": {"text": "总督边储赞理军务兼理巡抚，进提督军务", "official_ent_ids": []},
     "institution": {"text": "宣府", "ent_ids": []},
     "when": "景泰间", "status": "升迁",
     "evidence": "曹州李公秉总督边储，赞理军务兼理巡抚，进提督军务", "confidence": 0.85},
]
