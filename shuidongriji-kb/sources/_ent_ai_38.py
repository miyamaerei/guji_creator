# -*- coding: utf-8 -*-
"""《水东日记》卷 38 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "38-001 | 太宗问解缙任事十臣", "38-002 | 宣府预备仓社仓", "38-003 | 范梈钦廉海北海南记",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 38-001 任事十臣 ============
    {"item_id": "38-001", "text": "太宗皇帝", "type": "person", "normalized": "明成祖（太宗文皇帝）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "38-001", "text": "解缙", "type": "person", "normalized": "解缙", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "38-001", "text": "黄福", "type": "person", "normalized": "黄福（交趾名臣）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "38-001", "text": "蹇义", "type": "person", "normalized": "蹇义", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "38-001", "text": "夏原吉", "type": "person", "normalized": "夏原吉", "confidence": 0.85, "source": "原文片段"},

    # ============ 38-002 预备仓 ============
    {"item_id": "38-002", "text": "宣府", "type": "place", "normalized": "宣府", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "38-002", "text": "预备仓", "type": "institution", "normalized": "宣府军民预备仓", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "38-002", "text": "张海", "type": "person", "normalized": "张海（御史）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "38-002", "text": "御史", "type": "official", "normalized": "御史", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "38-002", "text": "黄震", "type": "person", "normalized": "黄震（宋，社仓记）", "confidence": 0.82, "source": "原文片段"},

    # ============ 38-003 范梈钦廉记 ============
    {"item_id": "38-003", "text": "范梈", "type": "person", "normalized": "范梈（元，德机）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "38-003", "text": "钦廉", "type": "place", "normalized": "钦州廉州（海角）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "38-003", "text": "百粤", "type": "place", "normalized": "百粤（岭南）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "38-003", "text": "海北海南", "type": "place", "normalized": "海北海南道", "confidence": 0.82, "source": "原文片段"},
]
