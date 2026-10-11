# -*- coding: utf-8 -*-
"""《水东日记》卷 31 —— REL 人物关系 源数据（AI 判定逐条填写）"""

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
    # ---- 31-004 许有壬与许熙载 ----
    {"rel_id": "REL-15501", "item_id": "31-004",
     "person_a": {"text": "许有壬（安阳公）", "person_a_ent_ids": []},
     "person_b": {"text": "许熙载（鲁公）", "person_b_ent_ids": []},
     "relation_type": "父子亲属", "direction": "双向",
     "evidence": "以显考鲁公行状命其友欧阳玄……鲁公讳熙载即安阳公之父",
     "confidence": 0.88},
    # ---- 31-004 欧阳玄与许有壬 ----
    {"rel_id": "REL-15502", "item_id": "31-004",
     "person_a": {"text": "欧阳玄", "person_a_ent_ids": []},
     "person_b": {"text": "许有壬（安阳公）", "person_b_ent_ids": []},
     "relation_type": "同僚", "direction": "双向",
     "evidence": "命其友欧阳玄文诸神道之石",
     "confidence": 0.85},
    # ---- 31-005 三人皆安阳公同年进士 ----
    {"rel_id": "REL-15503", "item_id": "31-005",
     "person_a": {"text": "张起岩", "person_a_ent_ids": []},
     "person_b": {"text": "许有壬（安阳公）", "person_b_ent_ids": []},
     "relation_type": "同科", "direction": "双向",
     "evidence": "状公行者为今南台侍御史济南张公起岩……三人皆安阳公同年进士",
     "confidence": 0.85},
    {"rel_id": "REL-15504", "item_id": "31-005",
     "person_a": {"text": "马祖常", "person_a_ent_ids": []},
     "person_b": {"text": "许有壬（安阳公）", "person_b_ent_ids": []},
     "relation_type": "同科", "direction": "双向",
     "evidence": "志公圹者为今御史中丞浚仪马公祖常……三人皆安阳公同年进士",
     "confidence": 0.85},
]
# 缺口登记：其余条目为风物/考据，无明确人物关系。
