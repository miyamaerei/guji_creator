# -*- coding: utf-8 -*-
"""《水东日记》卷 26 —— LIT 文献资产 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "26-001 | 七言集句诗序", "26-002 | 于谦旧居", "26-003 | 刑律五品奏请",
    "26-004 | 张泰宁夏石彪", "26-005 | 国朝文物杜佑碑",
]

# 字段键（打包器校验用）：lit_id, item_id, title, author, type, content_location, confidence
DATA = [
    # ---- 26-001 七言集句诗序 ----
    {"lit_id": "LIT-13001", "item_id": "26-001",
     "title": "七言集句诗序（孙蒉、林志、张洪、黄容诸家序）",
     "author": {"text": "孙蒉、林志、张洪、黄容", "author_ent_ids": []},
     "type": "序",
     "content_location": "卷二十六26-001；以唐人七言绝句分类作集句诗，诸家为序，录台阁/山林/边塞诸体",
     "confidence": 0.82},
    # ---- 26-005 杜佑旌儒庙碑 ----
    {"lit_id": "LIT-13002", "item_id": "26-005",
     "title": "旌儒庙碑",
     "author": {"text": "杜佑", "author_ent_ids": []},
     "type": "碑文",
     "content_location": "卷二十六26-005；唐杜佑所作旌儒庙碑，叶盛记其可考",
     "confidence": 0.8},
]
