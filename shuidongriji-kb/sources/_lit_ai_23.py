# -*- coding: utf-8 -*-
"""《水东日记》卷 23 —— LIT 文献资产 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "23-001 | 文彦博 翼城庙记", "23-002 | 许可用 中丞", "23-003 | 欧阳文忠公论鱼袋",
    "23-004 | 内府对类书", "23-005 | 王交山论寇准李纲", "23-006 | 古今文章精义",
    "23-007 | 孟氏祖庭碑磨字", "23-008 | 宦防录薏苡方",
]

# 字段键（打包器校验用）：lit_id, item_id, title, author, type, content_location, confidence
DATA = [
    # ---- 23-001 翼城庙记 ----
    {"lit_id": "LIT-11501", "item_id": "23-001",
     "title": "翼城县新修至圣文宣王庙记",
     "author": {"text": "文彦博", "author_ent_ids": []},
     "type": "碑文",
     "content_location": "卷二十三23-001；潞国文忠烈公文彦博撰翼城县新修孔子庙记",
     "confidence": 0.85},
    # ---- 23-002 晋宁路乡贤祠堂记 ----
    {"lit_id": "LIT-11502", "item_id": "23-002",
     "title": "晋宁路乡贤祠堂记",
     "author": {"text": "许可用", "author_ent_ids": []},
     "type": "记",
     "content_location": "卷二十三23-002；许可用所传文章，今可见者有晋宁路乡贤祠堂记",
     "confidence": 0.82},
    # ---- 23-006 古今文章精义 ----
    {"lit_id": "LIT-11503", "item_id": "23-006",
     "title": "古今文章精义",
     "author": {"text": "李性学（编）", "author_ent_ids": []},
     "type": "序",
     "content_location": "卷二十三23-006；李性学编，录先儒论文字语，其书行于世",
     "confidence": 0.82},
]
