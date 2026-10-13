# -*- coding: utf-8 -*-
"""【卷04】APPT 任职层源数据 —— 南京官/王府/地方任职记录"""

APPTS = [
    # ============ 条6 南京兵部参赞机务（黄福）============
    {"slot": 1, "item_id": "04-006",
     "person": {"text": "黄福", "person_ent_ids": []},
     "office": {"text": "尚书参赞机务", "official_ent_ids": []},
     "institution": {"text": "南京兵部", "ent_ids": []},
     "when": "宣德八年", "status": "现任",
     "evidence": "按参赞机务，自宣德八年黄福始", "confidence": 0.92},

    # ============ 条30 王府沿革中的任职（勋臣武相）============
    {"slot": 2, "item_id": "04-030",
     "person": {"text": "王存中", "person_ent_ids": []},
     "office": {"text": "试佥事", "official_ent_ids": []},
     "institution": {"text": "按察分司", "ent_ids": []},
     "when": "洪武十五年", "status": "现任",
     "evidence": "以儒士王存中等五百三十一人为试佥事，人按二县", "confidence": 0.9},

    # ============ 条36 按察司沿革中的任职 ============
    {"slot": 3, "item_id": "04-036",
     "person": {"text": "王存中", "person_ent_ids": []},
     "office": {"text": "试佥事", "official_ent_ids": []},
     "institution": {"text": "天下府州县按察分司", "ent_ids": []},
     "when": "洪武十五年", "status": "现任",
     "evidence": "以儒士王存中等五百三十一人为试佥事，人按二县", "confidence": 0.9},

    # ============ 条43 行太仆寺（边防马政任职，无具体人名则略）============
    {"slot": 4, "item_id": "04-044",
     "person": {"text": "未明", "person_ent_ids": []},
     "office": {"text": "少卿", "official_ent_ids": []},
     "institution": {"text": "行太仆寺", "ent_ids": []},
     "when": "洪武三十年", "status": "现任",
     "evidence": "山西、北平、陕西，每寺设少卿一人，丞三人；甘肃、辽东，每寺设少卿、丞各一人",
     "confidence": 0.75},
]

# 说明：卷04 为地方行政编制条，人名任职记录极少（原文多为职官编制与职掌陈述，
#      非人物行迹）。按"宁缺毋滥"纪律，仅为有明确人名者建 APPT。
