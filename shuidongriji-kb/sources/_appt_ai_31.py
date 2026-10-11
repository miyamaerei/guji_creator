# -*- coding: utf-8 -*-
"""《水东日记》卷 31 —— APPT 职官任职 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "31-001 | 江南并海之河江港汊通潮汐者",
    "31-002 | 戏谈于凡四方人多以其土名",
    "31-003 | 前人所作墓文碑志序称述子妇者甚少",
    "31-004 | 安阳公居政府之五年",
    "31-005 | 别记独不云小臣廉乎",
    "31-006 | 允矣鲁公生而敦厖",
    "31-007 | 翰林侍讲学士通奉大夫知制诰同修国史兼国子祭酒欧阳玄撰",
    "31-008 | 翰林学士承旨荣禄大夫知制诰兼修国史赵孟頫书篆",
    "31-009 | 至元四年岁在戊寅八月吉日建",
    "31-010 | 天顺七年予在广东肇庆军前用旧韵集赵子昂诗五绝句",
    "31-011 | 登州蓬莱县纳布老人言海市",
    "31-012 | 朱子答张仁叔之问曰李悝百亩而收百五十石",
]

DATA = [
    # ---- 31-004 许熙载历官 ----
    {"appointment_id": "APPT-15501", "item_id": "31-004",
     "person": {"text": "许熙载（鲁公）", "person_ent_ids": []},
     "office": {"text": "德庆路提控按牍", "official_ent_ids": []},
     "institution": {"text": "德庆路", "ent_ids": []},
     "when": "元初", "status": "现任",
     "evidence": "以行省檄辟德庆路提控按牍",
     "confidence": 0.82},
    {"appointment_id": "APPT-15502", "item_id": "31-004",
     "person": {"text": "许熙载（鲁公）", "person_ent_ids": []},
     "office": {"text": "临江、抚州两路总管府照磨", "official_ent_ids": []},
     "institution": {"text": "临江抚州路", "ent_ids": []},
     "when": "元", "status": "升迁",
     "evidence": "迁临江抚州两路总管府照磨进将仕郎",
     "confidence": 0.82},
    # ---- 31-007 欧阳玄 ----
    {"appointment_id": "APPT-15503", "item_id": "31-007",
     "person": {"text": "欧阳玄", "person_ent_ids": []},
     "office": {"text": "翰林侍讲学士、通奉大夫、知制诰、同修国史、兼国子祭酒", "official_ent_ids": []},
     "institution": {"text": "翰林院", "ent_ids": []},
     "when": "元至元四年", "status": "现任",
     "evidence": "翰林侍讲学士通奉大夫知制诰同修国史兼国子祭酒欧阳玄撰",
     "confidence": 0.9},
    # ---- 31-008 赵孟頫 ----
    {"appointment_id": "APPT-15504", "item_id": "31-008",
     "person": {"text": "赵孟頫", "person_ent_ids": []},
     "office": {"text": "翰林学士承旨、荣禄大夫、知制诰、兼修国史", "official_ent_ids": []},
     "institution": {"text": "翰林院", "ent_ids": []},
     "when": "元至元四年", "status": "现任",
     "evidence": "翰林学士承旨荣禄大夫知制诰兼修国史赵孟頫书篆",
     "confidence": 0.9},
]
# 缺口登记：其余条目为风物/碑文/考据，不单列任职。
