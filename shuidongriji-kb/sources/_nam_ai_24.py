# -*- coding: utf-8 -*-
"""《水东日记》卷 24 —— NAM 名录谱牒（结构分类） 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "24-001~008 图画赞诗碑记史论注本史辨文集辨伪辞赋序临丧轶事",
]

# 字段键（打包器校验用）：nam_id, item_id, name, category, scope, entries, ent_ids, confidence
DATA = [
    # 卷二十四通检：8 条无表格式人名名录或谱牒。
    {"nam_id": "NAM-12001", "item_id": "24-001",
     "name": "卷二十四通检：表格式名录普查（无）",
     "category": "其他",
     "scope": "卷二十四全 8 条通检",
     "entries": [],
     "ent_ids": [],
     "evidence": "卷二十四 8 条均为图画赞诗、碑记、史论、注本、史辨、辞赋序、临丧轶事，未见表格式人名名录或谱牒，NAM 层本卷无可数组化条目。",
     "confidence": 0.9},
]
