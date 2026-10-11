# -*- coding: utf-8 -*-
"""《水东日记》卷 27 —— APPT 职官任职 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "27-001 | 姚文公燧撰宋太常少卿陈希亮神道碑",
    "27-002 | 李杜诗虽齐名而器识夐不同",
    "27-003 | 今驸马都尉周景父前监察御史秦颙",
    "27-004 | 高昌王世勋碑",
    "27-005 | 冯昱御史濮州人",
    "27-006 | 景泰三年四月十日独石都督孙安奏墩军",
    "27-007 | 山西参议孙敬前兵科给事中",
    "27-008 | 国朝定制母止封两人",
    "27-009 | 故事朝官结衔皆有一定之序",
    "27-010 | 人性好恶偏忌",
    "27-011 | 今怀来城东南旧石桥遗址",
    "27-012 | 宣府儒学圣人土像",
    "27-013 | 国初孔庙城隍皆木主",
    "27-014 | 于节庵养子于康颇好聚图画",
    "27-015 | 史记所载如纣囚西伯于羑里",
]

DATA = [
    # ---- 27-001 陈希亮太常少卿 ----
    {"appointment_id": "APPT-13501", "item_id": "27-001",
     "person": {"text": "陈希亮（公弼）", "person_ent_ids": []},
     "office": {"text": "太常少卿", "official_ent_ids": []},
     "institution": {"text": "太常寺", "ent_ids": []},
     "when": "宋治平前", "status": "追赠",
     "evidence": "宋太常少卿陈希亮……七世祖宋太常卿公以治平二年卒",
     "confidence": 0.88},
    # ---- 27-001 陈元凯建康路总管 ----
    {"appointment_id": "APPT-13502", "item_id": "27-001",
     "person": {"text": "陈元凯", "person_ent_ids": []},
     "office": {"text": "嘉议大夫、建康路总管兼管内劝农事", "official_ent_ids": []},
     "institution": {"text": "建康路", "ent_ids": []},
     "when": "元大德", "status": "现任",
     "evidence": "嘉议大夫建康路总管兼管内劝农事则元凯也",
     "confidence": 0.85},
    # ---- 27-004 宁宣府前卫指挥使 ----
    {"appointment_id": "APPT-13503", "item_id": "27-004",
     "person": {"text": "宁", "person_ent_ids": []},
     "office": {"text": "宣府前卫指挥使", "official_ent_ids": []},
     "institution": {"text": "宣府前卫", "ent_ids": []},
     "when": "明正统前后", "status": "现任",
     "evidence": "指挥佥事宁家……宁云",
     "confidence": 0.82},
    # ---- 27-006 孙安独石都督 ----
    {"appointment_id": "APPT-13504", "item_id": "27-006",
     "person": {"text": "孙安", "person_ent_ids": []},
     "office": {"text": "都督", "official_ent_ids": []},
     "institution": {"text": "独石", "ent_ids": []},
     "when": "景泰三年", "status": "现任",
     "evidence": "景泰三年四月十日独石都督孙安奏",
     "confidence": 0.88},
    # ---- 27-007 孙敬山西参议 ----
    {"appointment_id": "APPT-13505", "item_id": "27-007",
     "person": {"text": "孙敬", "person_ent_ids": []},
     "office": {"text": "山西参议", "official_ent_ids": []},
     "institution": {"text": "山西布政司", "ent_ids": []},
     "when": "天顺中", "status": "现任",
     "evidence": "山西参议孙敬前兵科给事中",
     "confidence": 0.85},
]
# 缺口登记：其余条目为诗评/轶事/考据，无明确任职动词。
