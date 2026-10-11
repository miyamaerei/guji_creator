# -*- coding: utf-8 -*-
"""《水东日记》卷 30 —— LIT 文献资产 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "30-001 | 祭社稷论", "30-002 | 文天祥像", "30-003 | 诛蚊赋",
    "30-004 | 均平徭役", "30-005 | 写像轶事",
]

# 字段键（打包器校验用）：lit_id, item_id, title, author, type, content_location, confidence
DATA = [
    # ---- 30-002 于谦赞文天祥像 ----
    {"lit_id": "LIT-15001", "item_id": "30-002",
     "title": "文山像赞",
     "author": {"text": "于谦", "author_ent_ids": []},
     "type": "题跋",
     "content_location": "卷三十30-002；张遂持文山像求题，像上有于谦少保兼太子太傅兵部尚书赞",
     "confidence": 0.82},
    # ---- 30-003 诛蚊赋 ----
    {"lit_id": "LIT-15002", "item_id": "30-003",
     "title": "诛蚊赋",
     "author": {"text": "虞集", "author_ent_ids": []},
     "type": "其他",
     "content_location": "卷三十30-003；虞集以水乡蚊蚋为苦，裒集蚊事二十七则作诛蚊赋",
     "confidence": 0.82},
    # ---- 30-004 朱熹答王子度二书 ----
    {"lit_id": "LIT-15003", "item_id": "30-004",
     "title": "答王子度论赋役书（二书）",
     "author": {"text": "朱熹（晦庵）", "author_ent_ids": []},
     "type": "书启",
     "content_location": "卷三十30-004；晦庵答王子度二书，论均平赋役之法",
     "confidence": 0.82},
]
