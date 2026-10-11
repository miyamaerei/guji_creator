# -*- coding: utf-8 -*-
"""《水东日记》卷 24 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "24-001 | 宋理宗朝内珰有侮吾夫子者令马逺画一佛中坐老子侧立孔子问礼于前",
    "24-002 | 豫章熊天慵先生二百年前江右大儒也其遗文世不多见偶见其重修广州",
    "24-003 | 信史古今所称欧阳子曰有欲书而不得书有欲书而不敢书则遗漏一也讳",
    "24-004 | 安成李先生祭酒尝取古诗十九首刘履风雅翼所注释者锓梓以传",
    "24-005 | 杨廉夫作正统辨其文未易可否近见解学士缙所作周君墓表",
    "24-006 | 东里集中有宁国府庙学记其文可疑或者误编他人之文",
    "24-007 | 离骚经楚人高元之作变离骚其序文今录于此",
    "24-008 | 徐承宗临丧有毁瘠之誉一时称之",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 24-001 侮孔子图 ============
    {"item_id": "24-001", "text": "马远", "type": "person", "normalized": "马远（南宋画院待诏）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "24-001", "text": "江古心", "type": "person", "normalized": "江万里（号古心）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "24-001", "text": "张篠庵", "type": "person", "normalized": "张和（号篠庵）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "24-001", "text": "孔子", "type": "person", "normalized": "孔子", "confidence": 0.9, "source": "原文片段"},

    # ============ 24-002 熊天慵广州路学记 ============
    {"item_id": "24-002", "text": "熊天慵", "type": "person", "normalized": "熊朋来（号天慵，豫章大儒）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "24-002", "text": "豫章", "type": "place", "normalized": "豫章", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "24-002", "text": "广州路学", "type": "institution", "normalized": "广州路学（大成殿）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "24-002", "text": "李孝光", "type": "person", "normalized": "李孝光（五峰）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "24-002", "text": "泰不华", "type": "person", "normalized": "泰不华（元末大臣）", "confidence": 0.82, "source": "原文片段"},

    # ============ 24-003 信史论 ============
    {"item_id": "24-003", "text": "欧阳子", "type": "person", "normalized": "欧阳修（论史）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "24-003", "text": "曾巩", "type": "person", "normalized": "曾巩（南丰）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "24-003", "text": "朱熹", "type": "person", "normalized": "朱熹", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "24-003", "text": "揭文安", "type": "person", "normalized": "揭傒斯（谥文安）", "confidence": 0.82, "source": "原文片段"},

    # ============ 24-004 风雅翼注古诗 ============
    {"item_id": "24-004", "text": "安成李先生", "type": "person", "normalized": "李先生（安成，祭酒）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "24-004", "text": "刘履", "type": "person", "normalized": "刘履（编风雅翼）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "24-004", "text": "风雅翼", "type": "work", "normalized": "风雅翼（刘履注古诗）", "confidence": 0.82, "source": "原文片段"},

    # ============ 24-005 杨维桢正统辨 ============
    {"item_id": "24-005", "text": "杨廉夫", "type": "person", "normalized": "杨维桢（号廉夫，铁崖）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "24-005", "text": "解缙", "type": "person", "normalized": "解缙", "confidence": 0.88, "source": "原文片段"},

    # ============ 24-006 东里集庙学记可疑 ============
    {"item_id": "24-006", "text": "东里集", "type": "work", "normalized": "东里集（杨士奇著）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "24-006", "text": "杨士奇", "type": "person", "normalized": "杨士奇（东里）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "24-006", "text": "宁国府", "type": "place", "normalized": "宁国府", "confidence": 0.85, "source": "原文片段"},

    # ============ 24-007 变离骚序 ============
    {"item_id": "24-007", "text": "离骚经", "type": "work", "normalized": "离骚经（屈原）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "24-007", "text": "高元之", "type": "person", "normalized": "高元之（楚人，作变离骚）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "24-007", "text": "变离骚", "type": "work", "normalized": "变离骚（高元之作）", "confidence": 0.82, "source": "原文片段"},

    # ============ 24-008 徐承宗临丧 ============
    {"item_id": "24-008", "text": "徐承宗", "type": "person", "normalized": "徐承宗（临丧毁瘠）", "confidence": 0.82, "source": "原文片段"},
]
