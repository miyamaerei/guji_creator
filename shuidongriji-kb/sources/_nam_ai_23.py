# -*- coding: utf-8 -*-
"""《水东日记》卷 23 —— NAM 名录谱牒（结构分类） 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "23-001~008 碑记文章考论巧对史论书目碑考药方",
]

# 字段键（打包器校验用）：nam_id, item_id, name, category, scope, entries, ent_ids, confidence
DATA = [
    # 卷二十三通检：8 条为碑记、文章、考论、巧对、史论、书目、碑考、药方，无表格式人名名录或谱牒。
    {"nam_id": "NAM-11501", "item_id": "23-001",
     "name": "卷二十三通检：表格式名录普查（无）",
     "category": "其他",
     "scope": "卷二十三全 8 条通检",
     "entries": [],
     "ent_ids": [],
     "evidence": "卷二十三 8 条均为金石碑记、文论考订、巧对、史论、药方，未见官员题名/同僚题名/迁谪录/谱牒等表格式名录，NAM 层本卷无可数组化条目。",
     "confidence": 0.9},
]
