# -*- coding: utf-8 -*-
"""《水东日记》卷 26 —— REG 典章制度 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "26-001 | 七言集句诗序", "26-002 | 于谦旧居", "26-003 | 刑律五品奏请",
    "26-004 | 张泰宁夏石彪", "26-005 | 国朝文物杜佑碑",
]

# 字段键（打包器校验用）：reg_id, item_id, name, type, content, institutions, officials, confidence
DATA = [
    # ---- 26-003 五品以上官犯罪奏请之律 ----
    {"reg_id": "REG-13001", "item_id": "26-003",
     "name": "五品以上官犯罪奏闻请逮之律",
     "type": "司法",
     "content": "律：凡京官及在外五品以上官有犯，须奏闻请逮，不许官司擅自推问；今刑部、都察院于京官皆遵此制",
     "institutions": [], "officials": [],
     "confidence": 0.85},
]
