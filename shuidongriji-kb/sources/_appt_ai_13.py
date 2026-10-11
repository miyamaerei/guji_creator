# -*- coding: utf-8 -*-
"""《水东日记》卷 13 —— APPT 职官任职 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "13-001 | 邹奕字道苏州人有文行元季尝守贑国初谪关西与一时知名士若江右",
    "13-002 | 谢员友规者鄞人洪武初以户役起充浙江宪司吏非其志也告指疾求退得",
    "13-003 | 洪武己巳之秋予兵籍都城艮维之姚坊门乃九月八日与其侪输作于公",
    "13-004 | 袭阳武侯家因凿池得唐故幽州衙前【缺】　使乐安郡府君孙公墓志铭",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
DATA = [
    # ---- 13-001 邹奕元季守赣 ----
    {"appointment_id": "APPT-6501", "item_id": "13-001",
     "person": {"text": "邹奕", "person_ent_ids": []},
     "office": {"text": "守赣（赣州知府）", "official_ent_ids": []},
     "institution": {"text": "赣州", "ent_ids": []},
     "when": "元季", "status": "现任",
     "evidence": "元季尝守贑国初谪关西",
     "confidence": 0.8},
    # ---- 13-002 谢员屡调任 ----
    {"appointment_id": "APPT-6502", "item_id": "13-002",
     "person": {"text": "谢员", "person_ent_ids": []},
     "office": {"text": "浙江宪司吏", "official_ent_ids": []},
     "institution": {"text": "浙江按察司", "ent_ids": []},
     "when": "洪武初", "status": "现任",
     "evidence": "洪武初以户役起充浙江宪司吏",
     "confidence": 0.85},
    {"appointment_id": "APPT-6503", "item_id": "13-002",
     "person": {"text": "谢员", "person_ent_ids": []},
     "office": {"text": "临洮府（吏）", "official_ent_ids": []},
     "institution": {"text": "临洮府", "ent_ids": []},
     "when": "洪武初", "status": "贬谪",
     "evidence": "得调临洮府后例充兴州卫军",
     "confidence": 0.8},
    # ---- 13-002 潘若水屡调任 ----
    {"appointment_id": "APPT-6504", "item_id": "13-002",
     "person": {"text": "潘若水", "person_ent_ids": []},
     "office": {"text": "权翰林待诏", "official_ent_ids": []},
     "institution": {"text": "翰林院", "ent_ids": []},
     "when": "永乐中", "status": "兼领",
     "evidence": "王府引礼舎人以言事权翰林待诏与修永乐大典",
     "confidence": 0.8},
    {"appointment_id": "APPT-6505", "item_id": "13-002",
     "person": {"text": "潘若水", "person_ent_ids": []},
     "office": {"text": "西宁行太仆寺吏", "official_ent_ids": []},
     "institution": {"text": "西宁行太仆寺", "ent_ids": []},
     "when": "永乐中", "status": "贬谪",
     "evidence": "坐事黜为西宁行太仆寺吏",
     "confidence": 0.82},
    {"appointment_id": "APPT-6506", "item_id": "13-002",
     "person": {"text": "解缙", "person_ent_ids": []},
     "office": {"text": "河州卫吏", "official_ent_ids": []},
     "institution": {"text": "河州卫", "ent_ids": []},
     "when": "永乐中", "status": "贬谪",
     "evidence": "解学士大绅永乐中亦尝谪河州卫吏",
     "confidence": 0.85},
    # 缺口登记：
    # 13-003 为叶盛自寓输作梦境，无明确任职句；13-004 唐孙绪（宗绪）碑仅述先世官职未及本任，不单列。
]
