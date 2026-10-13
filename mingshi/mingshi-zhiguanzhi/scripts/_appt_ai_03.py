# -*- coding: utf-8 -*-
"""
【卷03】APPT 职官任职层源数据
只建有直接证据的任职（具体人名 + 官职）。无具体人名的笼统描述不建。
"""

APPTS = [
    # ============ 条17 尚宝司沿革中的任职 ============
    {"slot": 1, "item_id": "03-017",
     "person": {"text": "耿瑄", "person_ent_ids": []},
     "office": {"text": "散骑舍人", "official_ent_ids": []},
     "institution": {"text": "尚宝司", "ent_ids": []},
     "when": "太祖初", "status": "兼领",
     "evidence": "以侍从儒臣、勋卫领之（如耿瑄以散骑舍人…领之）", "confidence": 0.85},
    {"slot": 2, "item_id": "03-017",
     "person": {"text": "黄观", "person_ent_ids": []},
     "office": {"text": "侍中", "official_ent_ids": []},
     "institution": {"text": "尚宝司", "ent_ids": []},
     "when": "太祖初", "status": "兼领",
     "evidence": "黄观以侍中…领之", "confidence": 0.85},
    {"slot": 3, "item_id": "03-017",
     "person": {"text": "杨荣", "person_ent_ids": []},
     "office": {"text": "尚宝司卿", "official_ent_ids": []},
     "institution": {"text": "尚宝司", "ent_ids": []},
     "when": "太祖初", "status": "兼领",
     "evidence": "杨荣以…领之", "confidence": 0.85},

    # ============ 条19 六科沿革中的任职 ============
    {"slot": 4, "item_id": "03-019",
     "person": {"text": "魏敏", "person_ent_ids": []},
     "office": {"text": "给事中", "official_ent_ids": []},
     "institution": {"text": "六科", "ent_ids": []},
     "when": "洪武二十二年", "status": "现任",
     "evidence": "初，魏敏、卓敬等凡八十一人为给事中", "confidence": 0.88},
    {"slot": 5, "item_id": "03-019",
     "person": {"text": "卓敬", "person_ent_ids": []},
     "office": {"text": "给事中", "official_ent_ids": []},
     "institution": {"text": "六科", "ent_ids": []},
     "when": "洪武二十二年", "status": "现任",
     "evidence": "魏敏、卓敬等凡八十一人为给事中", "confidence": 0.88},

    # ============ 条22 中书科沿革中的任职 ============
    {"slot": 6, "item_id": "03-022",
     "person": {"text": "唐铎", "person_ent_ids": []},
     "office": {"text": "谏议大夫", "official_ent_ids": []},
     "institution": {"text": "谏院", "ent_ids": []},
     "when": "洪武十五年", "status": "现任",
     "evidence": "十五年，又置谏议大夫（以兵部尚书唐铎为之）", "confidence": 0.88},

    # ============ 条27 钦天监沿革中的任职 ============
    {"slot": 7, "item_id": "03-027",
     "person": {"text": "刘基", "person_ent_ids": []},
     "office": {"text": "太史令", "official_ent_ids": []},
     "institution": {"text": "太史监", "ent_ids": []},
     "when": "吴元年", "status": "现任",
     "evidence": "以刘基为太史令", "confidence": 0.95},
    {"slot": 8, "item_id": "03-027",
     "person": {"text": "张佑", "person_ent_ids": []},
     "office": {"text": "太史", "official_ent_ids": []},
     "institution": {"text": "司天监", "ent_ids": []},
     "when": "洪武元年", "status": "现任",
     "evidence": "洪武元年，征元太史张佑、张沂等十四人", "confidence": 0.88},
    {"slot": 9, "item_id": "03-027",
     "person": {"text": "张沂", "person_ent_ids": []},
     "office": {"text": "太史", "official_ent_ids": []},
     "institution": {"text": "司天监", "ent_ids": []},
     "when": "洪武元年", "status": "现任",
     "evidence": "征元太史张佑、张沂等十四人", "confidence": 0.88},

    # ============ 条43 道录司沿革中的任职 ============
    {"slot": 10, "item_id": "03-043",
     "person": {"text": "张正常", "person_ent_ids": []},
     "office": {"text": "正一真人", "official_ent_ids": []},
     "institution": {"text": "龙虎山", "ent_ids": []},
     "when": "洪武元年", "status": "世袭",
     "evidence": "洪武元年，张正常入朝，去其天师之号，封为真人，世袭",
     "confidence": 0.92},
    {"slot": 11, "item_id": "03-043",
     "person": {"text": "张正常", "person_ent_ids": []},
     "office": {"text": "天师", "official_ent_ids": []},
     "institution": {"text": "龙虎山", "ent_ids": []},
     "when": "洪武元年前", "status": "罢黜",
     "evidence": "张正常入朝，去其天师之号，封为真人", "confidence": 0.88},
]
