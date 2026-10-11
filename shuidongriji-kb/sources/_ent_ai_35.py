# -*- coding: utf-8 -*-
"""《水东日记》卷 35 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "35-001 | 张耀卿纪行录王恽中堂事记", "35-002 | 羊祜碑全文",
    "35-003 | 羊祜碑残句", "35-004 | 郑达后题羊祜碑",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 35-001 纪行录中堂事记 ============
    {"item_id": "35-001", "text": "周伯温", "type": "person", "normalized": "周伯温（近光集）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "35-001", "text": "近光集", "type": "work", "normalized": "近光集（周伯温）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "35-001", "text": "张耀卿", "type": "person", "normalized": "张耀卿（纪行录）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "35-001", "text": "纪行录", "type": "work", "normalized": "张耀卿纪行录", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "35-001", "text": "王恽", "type": "person", "normalized": "王恽（元，中堂事记）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "35-001", "text": "中堂事记", "type": "work", "normalized": "王恽中堂事记", "confidence": 0.82, "source": "原文片段"},

    # ============ 35-002 羊祜碑 ============
    {"item_id": "35-002", "text": "羊公", "type": "person", "normalized": "羊祜（叔子，钜平成侯）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "35-002", "text": "泰山南城", "type": "place", "normalized": "泰山南城（羊祜故里）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "35-002", "text": "钜平成侯", "type": "posthumous", "normalized": "钜平成侯（羊祜封谥）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "35-002", "text": "使持节侍中太傅", "type": "official", "normalized": "使持节侍中太傅", "confidence": 0.82, "source": "原文片段"},

    # ============ 35-003 碑残句 ============
    {"item_id": "35-003", "text": "羊祜碑", "type": "work", "normalized": "羊祜碑（残句）", "confidence": 0.8, "source": "原文片段"},

    # ============ 35-004 郑达后题 ============
    {"item_id": "35-004", "text": "郑达", "type": "person", "normalized": "郑达（后题羊祜碑）", "confidence": 0.82, "source": "原文片段"},
]
