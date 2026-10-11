# -*- coding: utf-8 -*-
"""《水东日记》卷 37 —— LIT 文献资产 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "37-001 | 瀛国公诗", "37-002 | 刘江杀倭", "37-003 | 王恽纪梦",
    "37-004 | 志石昭穆", "37-005 | 北方试马", "37-006 | 马莲花方",
]

# 字段键（打包器校验用）：lit_id, item_id, title, author, type, content_location, confidence
DATA = [
    # ---- 37-001 瀛国公诗 ----
    {"lit_id": "LIT-18501", "item_id": "37-001",
     "title": "瀛国公诗（皇宋第十六飞龙）",
     "author": {"text": "瀛国公（宋幼主）", "author_ent_ids": []},
     "type": "诗",
     "content_location": "卷三十七37-001；瀛国公入元后诗，'皇宋第十六飞龙……'",
     "confidence": 0.82},
    {"lit_id": "LIT-18502", "item_id": "37-001",
     "title": "虞台岭观音堂记",
     "author": {"text": "未明", "author_ent_ids": []},
     "type": "记",
     "content_location": "卷三十七37-001；虞台岭观音堂记",
     "confidence": 0.8},
    # ---- 37-003 王恽纪梦 ----
    {"lit_id": "LIT-18503", "item_id": "37-003",
     "title": "纪梦（王恽）",
     "author": {"text": "王恽", "author_ent_ids": []},
     "type": "记",
     "content_location": "卷三十七37-003；至元十七年王恽官真定梦先祖敦武府君",
     "confidence": 0.82},
]
