# -*- coding: utf-8 -*-
"""《水东日记》卷 19 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "19-001 | 洪武戊申十一月十四日早朝宣圣五十五代袭封衍圣公臣孔克坚于谨身",
    "19-002 | 太宗文皇帝御制重修孔庙碑文道原于天而畀于圣人圣人者继天立极而",
    "19-003 | 上谕山西潞州壶关县儒士杜斆昔之御宇内者无幸位无遗贤致时和而世",
    "19-004 | 宋文鉴上中下凡一百五十卷朝奉郎行秘书省著作佐郎兼国史院编修官",
    "19-005 | 临江刘公淸之又以为此即删诗定书官使众材之意盖亦善观此书者故备",
    "19-006 | 广东参政仪真黎公恬追和故御史邓州守何公忠廷臣骂贼诗……",
    "19-007 | 元师渡江尝驻黄鹄山即黄鹤也有吕公矶俗传吕洞宾……",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 19-001 洪武戒谕衍圣公圣旨 ============
    {"item_id": "19-001", "text": "洪武戊申", "type": "era", "normalized": "洪武（明太祖年号，戊申=洪武元年）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "19-001", "text": "孔克坚", "type": "person", "normalized": "孔克坚（宣圣五十五代衍圣公）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "19-001", "text": "孔希学", "type": "person", "normalized": "孔希学（孔克坚子）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "19-001", "text": "衍圣公", "type": "official", "normalized": "衍圣公（孔子嫡裔封爵，秩视二品）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "19-001", "text": "谨身殿", "type": "place", "normalized": "谨身殿", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "19-001", "text": "曲阜", "type": "place", "normalized": "曲阜", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "19-001", "text": "朱元璋", "type": "person", "normalized": "朱元璋（明太祖高皇帝）", "confidence": 0.9, "source": "原文片段"},

    # ============ 19-002 御制重修孔庙碑 ============
    {"item_id": "19-002", "text": "太宗文皇帝", "type": "person", "normalized": "明太宗朱棣（永乐）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "19-002", "text": "孔子", "type": "person", "normalized": "孔子（宣圣）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "19-002", "text": "阙里", "type": "place", "normalized": "阙里（曲阜孔庙）", "confidence": 0.88, "source": "原文片段"},

    # ============ 19-003 上谕杜斆 ============
    {"item_id": "19-003", "text": "杜斆", "type": "person", "normalized": "杜斆（山西潞州壶关县儒士）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "19-003", "text": "潞州", "type": "place", "normalized": "潞州（壶关县）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "19-003", "text": "洪武十三年", "type": "era", "normalized": "洪武十三年", "confidence": 0.9, "source": "原文片段"},

    # ============ 19-004 宋文鉴 ============
    {"item_id": "19-004", "text": "宋文鉴", "type": "work", "normalized": "皇朝文鉴（宋文鉴，吕祖谦编）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "19-004", "text": "吕祖谦", "type": "person", "normalized": "吕祖谦（字伯恭，号东莱）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "19-004", "text": "周必大", "type": "person", "normalized": "周必大（益国公，跋宋文鉴）", "confidence": 0.88, "source": "原文片段"},

    # ============ 19-005 刘清之论删诗定书 ============
    {"item_id": "19-005", "text": "刘清之", "type": "person", "normalized": "刘清之（临江，字子澄）", "confidence": 0.85, "source": "原文片段"},

    # ============ 19-006 何忠骂贼诗 ============
    {"item_id": "19-006", "text": "何忠", "type": "person", "normalized": "何忠（御史，邓州守，谥忠）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "19-006", "text": "黎恬", "type": "person", "normalized": "黎恬（广东参政，仪真）", "confidence": 0.85, "source": "原文片段"},

    # ============ 19-007 元世祖渡江 ============
    {"item_id": "19-007", "text": "黄鹄山", "type": "place", "normalized": "黄鹄山（即黄鹤楼所在，武昌）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "19-007", "text": "吕公矶", "type": "place", "normalized": "吕公矶（吕洞宾矶）", "confidence": 0.85, "source": "原文片段"},
]
