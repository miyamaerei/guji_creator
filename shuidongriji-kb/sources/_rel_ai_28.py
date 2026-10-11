# -*- coding: utf-8 -*-
"""《水东日记》卷 28 —— REL 人物关系 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "28-001 | 胡杨序谱", "28-002 | 文章正宗", "28-003 | 东华铁狮子宅",
    "28-004 | 杀虎射生", "28-005 | 宣府庙学碑", "28-006 | 己巳北狩",
    "28-007 | 军医服药",
]

# 字段键（打包器校验用）：rel_id, item_id, person_a, person_b, relation_type, direction, evidence, confidence
DATA = [
    # ---- 28-001 胡广与杨士奇同僚 ----
    {"rel_id": "REL-14001", "item_id": "28-001",
     "person_a": {"text": "胡广", "person_a_ent_ids": []},
     "person_b": {"text": "杨士奇", "person_b_ent_ids": []},
     "relation_type": "同僚", "direction": "双向",
     "evidence": "庐陵胡文穆公杨文贞公两人同被文皇馆阁之命一时文誉",
     "confidence": 0.85},
]
