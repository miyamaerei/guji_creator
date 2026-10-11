# -*- coding: utf-8 -*-
"""《水东日记》卷 30 —— NAM 名录谱牒（结构分类） 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "30-001~005 祭社稷、文天祥像、诛蚊赋、均徭朱熹书、写像",
]

# 字段键（打包器校验用）：nam_id, item_id, name, category, scope, entries, ent_ids, confidence
DATA = [
    # 卷三十通检：5 条无表格式人名名录或谱牒。
    {"nam_id": "NAM-15001", "item_id": "30-001",
     "name": "卷三十通检：表格式名录普查（无）",
     "category": "其他",
     "scope": "卷三十全 5 条通检",
     "entries": [],
     "ent_ids": [],
     "evidence": "卷三十 5 条为礼制论、像赞、赋、赋役论、写像轶事，未见表格式人名名录或谱牒，NAM 层本卷无可数组化条目。",
     "confidence": 0.9},
]
