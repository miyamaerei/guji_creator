# -*- coding: utf-8 -*-
"""【卷01 续】条21–53 APPT 任职层源数据"""

APPTS = [
    # 条24 总督仓场（李昶）
    {"slot": 1, "item_id": "01-024",
     "person": {"text": "李昶", "person_ent_ids": []},
     "office": {"text": "户部尚书", "official_ent_ids": []},
     "institution": {"text": "总督仓场", "ent_ids": []},
     "when": "宣德五年", "status": "现任",
     "evidence": "宣德五年，始命李昶为户部尚书，专督其事，遂为定制", "confidence": 0.95},
    {"slot": 2, "item_id": "01-024",
     "person": {"text": "张养蒙", "person_ent_ids": []},
     "office": {"text": "右侍郎", "official_ent_ids": []},
     "institution": {"text": "总督仓场", "ent_ids": []},
     "when": "万历二十五年", "status": "现任",
     "evidence": "二十五年，以右侍郎张养蒙督辽饷", "confidence": 0.9},

    # 条40 协理京营戎政（于谦/刘天和/仇鸾/刘之纶）
    {"slot": 3, "item_id": "01-040",
     "person": {"text": "于谦", "person_ent_ids": []},
     "office": {"text": "兵部尚书", "official_ent_ids": []},
     "institution": {"text": "提督团营", "ent_ids": []},
     "when": "景泰元年", "status": "兼领",
     "evidence": "景泰元年始设提督团营，命兵部尚书于谦兼领之，后罢", "confidence": 0.95},
    {"slot": 4, "item_id": "01-040",
     "person": {"text": "刘天和", "person_ent_ids": []},
     "office": {"text": "尚书", "official_ent_ids": []},
     "institution": {"text": "协理京营戎政", "ent_ids": []},
     "when": "嘉靖二十年", "status": "现任",
     "evidence": "嘉靖二十年，始命尚书刘天和辍部务，另给关防，专理戎政", "confidence": 0.92},
    {"slot": 5, "item_id": "01-040",
     "person": {"text": "仇鸾", "person_ent_ids": []},
     "office": {"text": "总督京营戎政", "official_ent_ids": []},
     "institution": {"text": "京营", "ent_ids": []},
     "when": "嘉靖二十九年", "status": "现任",
     "evidence": "二十九年，以“总督京营戎政”之印畀仇鸾", "confidence": 0.9},
    {"slot": 6, "item_id": "01-040",
     "person": {"text": "刘之纶", "person_ent_ids": []},
     "office": {"text": "兵部侍郎", "official_ent_ids": []},
     "institution": {"text": "协理京营戎政", "ent_ids": []},
     "when": "崇祯二年", "status": "现任",
     "evidence": "崇祯二年复增一人，以庶吉士刘之纶为兵部侍郎充之", "confidence": 0.9},
]
