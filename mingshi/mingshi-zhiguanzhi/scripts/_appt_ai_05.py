# -*- coding: utf-8 -*-
"""卷五 APPT 任职层源数据 —— 《明史·职官志》卷五十二。

卷五为勋爵/军事/卫所/土官制度条，人名任职记载集中于：
  条2 驸马都尉典兵出镇者（梅殷/李坚/李让/沐昕/宋琥/赵辉/李贞/王宁/崔元）
  条5 朱文正为大都督
  条6 仇鸾佩总督京营戎政印
  条9 冯国用为帐前总制亲军都指挥使
按「宁缺毋滥」只记原文明确的人名+职衔。
"""
VERSION = "1.0"

APPTS = [
    # ============ 条2 驸马都尉典兵出镇 ============
    {"slot": 1, "item_id": "05-002",
     "person": {"text": "梅殷", "person_ent_ids": []},
     "office": {"text": "镇守淮安总兵官", "official_ent_ids": []},
     "institution": {"text": "镇守淮安", "ent_ids": []},
     "when": "建文时", "status": "现任",
     "evidence": "建文时，梅殷为镇守淮安总兵官", "confidence": 0.95},

    {"slot": 2, "item_id": "05-002",
     "person": {"text": "李坚", "person_ent_ids": []},
     "office": {"text": "左副将军", "official_ent_ids": []},
     "institution": {"text": "征讨军", "ent_ids": []},
     "when": "建文时", "status": "现任",
     "evidence": "李坚为左副将军", "confidence": 0.95},

    {"slot": 3, "item_id": "05-002",
     "person": {"text": "李让", "person_ent_ids": []},
     "office": {"text": "掌北京行部事", "official_ent_ids": []},
     "institution": {"text": "北京行部", "ent_ids": []},
     "when": "成祖时", "status": "现任",
     "evidence": "成祖时，李让掌北京行部事", "confidence": 0.95},

    {"slot": 4, "item_id": "05-002",
     "person": {"text": "沐昕", "person_ent_ids": []},
     "office": {"text": "守备南京", "official_ent_ids": []},
     "institution": {"text": "南京守备", "ent_ids": []},
     "when": "仁宗时", "status": "现任",
     "evidence": "仁宗时沐昕，宣宗时宋琥，并守备南京", "confidence": 0.95},

    {"slot": 5, "item_id": "05-002",
     "person": {"text": "宋琥", "person_ent_ids": []},
     "office": {"text": "守备南京", "official_ent_ids": []},
     "institution": {"text": "南京守备", "ent_ids": []},
     "when": "宣宗时", "status": "现任",
     "evidence": "宣宗时宋琥守备南京", "confidence": 0.95},

    {"slot": 6, "item_id": "05-002",
     "person": {"text": "赵辉", "person_ent_ids": []},
     "office": {"text": "掌南京左府事", "official_ent_ids": []},
     "institution": {"text": "南京左军都督府", "ent_ids": []},
     "when": "英宗时", "status": "现任",
     "evidence": "英宗时，赵辉掌南京左府事", "confidence": 0.95},

    {"slot": 7, "item_id": "05-002",
     "person": {"text": "李贞", "person_ent_ids": []},
     "office": {"text": "恩亲侯", "official_ent_ids": []},
     "institution": {"text": "勋爵", "ent_ids": []},
     "when": "明初", "status": "现任",
     "evidence": "若恩亲侯李贞，以恩泽封侯，非制也", "confidence": 0.9},

    {"slot": 8, "item_id": "05-002",
     "person": {"text": "王宁", "person_ent_ids": []},
     "office": {"text": "永春侯", "official_ent_ids": []},
     "institution": {"text": "勋爵", "ent_ids": []},
     "when": "明初", "status": "追赠",
     "evidence": "永春侯王宁，以恩泽封侯，非制也", "confidence": 0.85},

    {"slot": 9, "item_id": "05-002",
     "person": {"text": "崔元", "person_ent_ids": []},
     "office": {"text": "京山侯", "official_ent_ids": []},
     "institution": {"text": "勋爵", "ent_ids": []},
     "when": "明中", "status": "现任",
     "evidence": "京山侯崔元，以恩泽封侯，非制也", "confidence": 0.85},

    # ============ 条5 大都督 ============
    {"slot": 10, "item_id": "05-005",
     "person": {"text": "朱文正", "person_ent_ids": []},
     "office": {"text": "大都督", "official_ent_ids": []},
     "institution": {"text": "大都督府", "ent_ids": []},
     "when": "太祖下集庆后", "status": "现任",
     "evidence": "以朱文正为大都督，节制中外诸军事", "confidence": 0.95},

    # ============ 条6 京营总督 ============
    {"slot": 11, "item_id": "05-006",
     "person": {"text": "仇鸾", "person_ent_ids": []},
     "office": {"text": "总督京营戎政", "official_ent_ids": []},
     "institution": {"text": "京营", "ent_ids": []},
     "when": "嘉靖二十九年", "status": "现任",
     "evidence": "改提督曰总督，铸「总督京营戎政」印，俾仇鸾佩之", "confidence": 0.95},

    # ============ 条9 亲军都指挥使 ============
    {"slot": 12, "item_id": "05-009",
     "person": {"text": "冯国用", "person_ent_ids": []},
     "office": {"text": "都指挥使", "official_ent_ids": []},
     "institution": {"text": "帐前总制亲军都指挥使司", "ent_ids": []},
     "when": "明初", "status": "现任",
     "evidence": "明初，置帐前总制亲军都指挥使司，以冯国用为都指挥使", "confidence": 0.95},
]
