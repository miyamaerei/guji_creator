# -*- coding: utf-8 -*-
"""《水东日记》卷 24 —— LIT 文献资产 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "24-001 | 侮孔子图", "24-002 | 熊天慵广州路学记", "24-003 | 信史论",
    "24-004 | 风雅翼注古诗", "24-005 | 杨维桢正统辨", "24-006 | 东里集庙学记可疑",
    "24-007 | 变离骚序", "24-008 | 徐承宗临丧",
]

# 字段键（打包器校验用）：lit_id, item_id, title, author, type, content_location, confidence
DATA = [
    # ---- 24-001 侮孔子图赞诗 ----
    {"lit_id": "LIT-12001", "item_id": "24-001",
     "title": "释老侮孔子图赞（江万里赞）、口占诗（张和）",
     "author": {"text": "江万里（赞）、张和（诗）", "author_ent_ids": []},
     "type": "诗",
     "content_location": "卷二十四24-001；马远画佛中坐老子侧立孔子问礼图，江古心为赞、张篠庵口占诗",
     "confidence": 0.82},
    # ---- 24-002 广州路学大成殿记 ----
    {"lit_id": "LIT-12002", "item_id": "24-002",
     "title": "重修广州路学大成殿记",
     "author": {"text": "熊朋来（天慵）", "author_ent_ids": []},
     "type": "记",
     "content_location": "卷二十四24-002；熊天慵遗文，重修广州路学大成殿记全文（附清风岭王妇事）",
     "confidence": 0.85},
    # ---- 24-004 风雅翼 ----
    {"lit_id": "LIT-12003", "item_id": "24-004",
     "title": "风雅翼（注古诗十九首）",
     "author": {"text": "刘履（注）", "author_ent_ids": []},
     "type": "序",
     "content_location": "卷二十四24-004；刘履风雅翼所注古诗十九首，安成李先生锓梓以传",
     "confidence": 0.82},
    # ---- 24-005 正统辨 ----
    {"lit_id": "LIT-12004", "item_id": "24-005",
     "title": "正统辨",
     "author": {"text": "杨维桢（廉夫）", "author_ent_ids": []},
     "type": "其他",
     "content_location": "卷二十四24-005；杨廉夫作正统辨，辨历代正闰之统",
     "confidence": 0.82},
    # ---- 24-007 变离骚序 ----
    {"lit_id": "LIT-12005", "item_id": "24-007",
     "title": "变离骚序",
     "author": {"text": "高元之", "author_ent_ids": []},
     "type": "序",
     "content_location": "卷二十四24-007；高元之变离骚序文，叶盛录于此",
     "confidence": 0.82},
]
