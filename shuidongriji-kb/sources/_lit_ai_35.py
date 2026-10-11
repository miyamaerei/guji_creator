# -*- coding: utf-8 -*-
"""《水东日记》卷 35 —— LIT 文献资产 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "35-001 | 纪行录中堂事记", "35-002 | 羊祜碑全文",
    "35-003 | 羊祜碑残句", "35-004 | 郑达后题羊祜碑",
]

# 字段键（打包器校验用）：lit_id, item_id, title, author, type, content_location, confidence
DATA = [
    # ---- 35-001 纪行录、中堂事记 ----
    {"lit_id": "LIT-17501", "item_id": "35-001",
     "title": "张耀卿纪行录",
     "author": {"text": "张耀卿", "author_ent_ids": []},
     "type": "记",
     "content_location": "卷三十五35-001；张耀卿纪行录，记元时北出道里风土",
     "confidence": 0.82},
    {"lit_id": "LIT-17502", "item_id": "35-001",
     "title": "中堂事记",
     "author": {"text": "王恽", "author_ent_ids": []},
     "type": "记",
     "content_location": "卷三十五35-001；王恽中堂事记节取",
     "confidence": 0.82},
    # ---- 35-002 羊祜碑 ----
    {"lit_id": "LIT-17503", "item_id": "35-002",
     "title": "晋故使持节侍中太傅钜平成侯羊公之碑",
     "author": {"text": "未明（羊祜碑）", "author_ent_ids": []},
     "type": "碑文",
     "content_location": "卷三十五35-002；羊祜碑全文，记羊祜叔子泰山南城人、历官德政",
     "confidence": 0.85},
    # ---- 35-004 郑达后题 ----
    {"lit_id": "LIT-17504", "item_id": "35-004",
     "title": "后题羊祜碑",
     "author": {"text": "郑达", "author_ent_ids": []},
     "type": "题跋",
     "content_location": "卷三十五35-004；郑达见羊祜碑作后题",
     "confidence": 0.82},
]
