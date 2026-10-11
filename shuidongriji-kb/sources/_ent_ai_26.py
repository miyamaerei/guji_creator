# -*- coding: utf-8 -*-
"""《水东日记》卷 26 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "26-001 | 七言集句诗序予尝欲以唐人七言絶句分为十如王建宫词金殿当头紫",
    "26-002 | 于节庵公旧居小苏州巷与余南北隣其自河南以大理少卿塟父囘始相识",
    "26-003 | 律凡京官及在外五品以上官有犯奏闻请防不许擅问今刑部都察院于京",
    "26-004 | 张泰都督宁夏石彪尝索古瓶于泰泰不与彪衔之",
    "26-005 | 国朝文物之盛岳季方在内阁尝言今之文章",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 26-001 七言集句诗序 ============
    {"item_id": "26-001", "text": "孙蒉", "type": "person", "normalized": "孙蒉（中山，集句诗）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "26-001", "text": "林志", "type": "person", "normalized": "林志（诗序作者）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "26-001", "text": "张洪", "type": "person", "normalized": "张洪（诗序作者）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "26-001", "text": "黄容", "type": "person", "normalized": "黄容（诗序作者）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "26-001", "text": "王建", "type": "person", "normalized": "王建（唐，宫词）", "confidence": 0.85, "source": "原文片段"},

    # ============ 26-002 于谦旧居 ============
    {"item_id": "26-002", "text": "于节庵公", "type": "person", "normalized": "于谦（谥忠肃，号节庵）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "26-002", "text": "叶盛", "type": "person", "normalized": "叶盛（与于谦为邻）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "26-002", "text": "金氏", "type": "person", "normalized": "金氏（叶盛妻）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "26-002", "text": "大理少卿", "type": "official", "normalized": "大理寺少卿", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "26-002", "text": "小苏州巷", "type": "place", "normalized": "小苏州巷（京师）", "confidence": 0.82, "source": "原文片段"},

    # ============ 26-003 刑律五品奏请 ============
    {"item_id": "26-003", "text": "刑部", "type": "institution", "normalized": "刑部", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "26-003", "text": "都察院", "type": "institution", "normalized": "都察院", "confidence": 0.9, "source": "原文片段"},

    # ============ 26-004 张泰宁夏 ============
    {"item_id": "26-004", "text": "张泰", "type": "person", "normalized": "张泰（都督，镇宁夏）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "26-004", "text": "石彪", "type": "person", "normalized": "石彪（西宁侯，骄横）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "26-004", "text": "宁夏", "type": "place", "normalized": "宁夏", "confidence": 0.88, "source": "原文片段"},

    # ============ 26-005 国朝文物 杜佑碑 ============
    {"item_id": "26-005", "text": "岳季方", "type": "person", "normalized": "岳季方（在内阁）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "26-005", "text": "杜佑", "type": "person", "normalized": "杜佑（唐，旌儒庙碑）", "confidence": 0.85, "source": "原文片段"},
]
