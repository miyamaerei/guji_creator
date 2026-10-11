# -*- coding: utf-8 -*-
"""《水东日记》卷 38 —— LIT 文献资产 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "38-001 | 任事十臣", "38-002 | 宣府预备仓", "38-003 | 范梈钦廉记",
]

# 字段键（打包器校验用）：lit_id, item_id, title, author, type, content_location, confidence
DATA = [
    # ---- 38-003 范梈钦廉海北海南记 ----
    {"lit_id": "LIT-19001", "item_id": "38-003",
     "title": "钦廉海北海南记",
     "author": {"text": "范梈（德机）", "author_ent_ids": []},
     "type": "记",
     "content_location": "卷三十八38-003；范梈记钦廉在百粤、距中国万里、郡南临大洋、廉居其折故曰海角",
     "confidence": 0.82},
]
