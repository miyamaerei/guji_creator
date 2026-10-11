# -*- coding: utf-8 -*-
"""《水东日记》卷 28 —— LIT 文献资产 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "28-001 | 胡杨序谱", "28-002 | 文章正宗", "28-003 | 东华铁狮子宅",
    "28-004 | 杀虎射生", "28-005 | 宣府庙学碑", "28-006 | 己巳北狩",
    "28-007 | 军医服药",
]

# 字段键（打包器校验用）：lit_id, item_id, title, author, type, content_location, confidence
DATA = [
    # ---- 28-002 文章正宗 ----
    {"lit_id": "LIT-14001", "item_id": "28-002",
     "title": "文章正宗序",
     "author": {"text": "真德秀（西山）", "author_ent_ids": []},
     "type": "序",
     "content_location": "卷二十八28-002；西山谓正宗者，欲学者识文源流之正",
     "confidence": 0.85},
    {"lit_id": "LIT-14002", "item_id": "28-002",
     "title": "吴闲闲诗（许有壬所录）",
     "author": {"text": "吴闲闲", "author_ent_ids": []},
     "type": "诗",
     "content_location": "卷二十八28-002；许有壬所传吴闲闲诗",
     "confidence": 0.82},
    # ---- 28-005 宣府庙学碑 ----
    {"lit_id": "LIT-14003", "item_id": "28-005",
     "title": "宣府庙学碑（附前元进士碑）",
     "author": {"text": "未明", "author_ent_ids": []},
     "type": "碑文",
     "content_location": "卷二十八28-005；宣府庙学碑及前元进士题名碑，碑字磨泐",
     "confidence": 0.8},
]
