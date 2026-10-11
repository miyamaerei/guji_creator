# -*- coding: utf-8 -*-
"""《水东日记》卷 20 —— APPT 职官任职 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "20-001 | 南雄杨氏谱本蜀唐祭酒两淮运副有文",
    "20-002 | 张篠庵有秋台清话未成卷",
    "20-003 | 雪庵者元僧云中人头陀教大宗师",
    "20-004 | 西斋亦元僧其谢事檇李归和陶归去来辞韵",
    "20-005 | 天顺四年过南京见夏时正寅卿中手临范文正公与监簿兄家书",
    "20-006 | 仲淹拜上三哥监簿",
    "20-007 | 邵复孺先生家藏老苏大全文集四十五卷",
    "20-008 | 吉安程源伊知府处见文山文集道体堂元编二书",
    "20-009 | 景泰辛未廷试盛预弥封",
]

DATA = [
    # ---- 20-001 有文两淮运副 ----
    {"appointment_id": "APPT-10001", "item_id": "20-001",
     "person": {"text": "有文", "person_ent_ids": []},
     "office": {"text": "两淮运副", "official_ent_ids": []},
     "institution": {"text": "两淮", "ent_ids": []},
     "when": "正统初（杨氏谱重修时）", "status": "现任",
     "evidence": "南雄杨氏谱本蜀唐祭酒两淮运副有文正统初所重修",
     "confidence": 0.82},
    # ---- 20-003 雪庵昭文馆大学士 ----
    {"appointment_id": "APPT-10002", "item_id": "20-003",
     "person": {"text": "雪庵（李玄晖）", "person_ent_ids": []},
     "office": {"text": "昭文馆大学士", "official_ent_ids": []},
     "institution": {"text": "昭文馆", "ent_ids": []},
     "when": "元代", "status": "现任",
     "evidence": "元僧云中人头陀教大宗师任昭文馆大学士雪庵盖其号",
     "confidence": 0.85},
    # ---- 20-006 范仲淹擢贰枢府改参大政 ----
    {"appointment_id": "APPT-10003", "item_id": "20-006",
     "person": {"text": "范仲淹", "person_ent_ids": []},
     "office": {"text": "枢密副使（贰枢府）", "official_ent_ids": []},
     "institution": {"text": "西府（枢密院）", "ent_ids": []},
     "when": "宋仁宗时", "status": "升迁",
     "evidence": "制恩擢贰枢府累让不允今月二日已签署勾当",
     "confidence": 0.85},
    {"appointment_id": "APPT-10004", "item_id": "20-006",
     "person": {"text": "范仲淹", "person_ent_ids": []},
     "office": {"text": "参知政事（参大政）", "official_ent_ids": []},
     "institution": {"text": "西府", "ent_ids": []},
     "when": "宋仁宗时", "status": "升迁",
     "evidence": "十二日蒙恩改参大政寻面陈利害已得指挥让且在西府",
     "confidence": 0.85},
    # ---- 20-009 徐珵侍讲 / 陈叔绍御史 ----
    {"appointment_id": "APPT-10005", "item_id": "20-009",
     "person": {"text": "徐珵（徐有贞）", "person_ent_ids": []},
     "office": {"text": "侍讲", "official_ent_ids": []},
     "institution": {"text": "翰林院", "ent_ids": []},
     "when": "景泰辛未", "status": "现任",
     "evidence": "徐侍讲珵受卷",
     "confidence": 0.85},
    {"appointment_id": "APPT-10006", "item_id": "20-009",
     "person": {"text": "陈叔绍", "person_ent_ids": []},
     "office": {"text": "御史", "official_ent_ids": []},
     "institution": {"text": "都察院", "ent_ids": []},
     "when": "景泰辛未", "status": "现任",
     "evidence": "陈御史同年叔绍等监试",
     "confidence": 0.85},
]
# 缺口登记：其余条目为官守/藏书记述，无明确任职动词。
