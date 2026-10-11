# -*- coding: utf-8 -*-
"""《水东日记》卷 30 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "30-001 | 南轩祭社稷论城隍祀典", "30-002 | 张遂持文天祥像于谦赞", "30-003 | 虞集诛蚊赋",
    "30-004 | 叶盛均平徭役朱熹答王子度书", "30-005 | 写像轶事",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 30-001 祭社稷论 ============
    {"item_id": "30-001", "text": "南轩张先生", "type": "person", "normalized": "张栻（号南轩）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "30-001", "text": "社稷", "type": "institution", "normalized": "社稷之祭", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "30-001", "text": "城隍", "type": "institution", "normalized": "城隍神祀典", "confidence": 0.85, "source": "原文片段"},

    # ============ 30-002 文天祥像 ============
    {"item_id": "30-002", "text": "张遂", "type": "person", "normalized": "张遂（郎中）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "30-002", "text": "文山", "type": "person", "normalized": "文天祥（号文山）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "30-002", "text": "于公", "type": "person", "normalized": "于谦（少保兵部尚书）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "30-002", "text": "郎中", "type": "official", "normalized": "郎中", "confidence": 0.85, "source": "原文片段"},

    # ============ 30-003 诛蚊赋 ============
    {"item_id": "30-003", "text": "虞雍公", "type": "person", "normalized": "虞雍公（虞集之先）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "30-003", "text": "虞集", "type": "person", "normalized": "虞集（元，伯生）", "confidence": 0.85, "source": "原文片段"},

    # ============ 30-004 均平徭役 朱熹书 ============
    {"item_id": "30-004", "text": "叶盛", "type": "person", "normalized": "叶盛（在广中均平徭役）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "30-004", "text": "晦庵", "type": "person", "normalized": "朱熹（号晦庵）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "30-004", "text": "王子度", "type": "person", "normalized": "王子度（朱熹答书对象）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "30-004", "text": "广中", "type": "place", "normalized": "广中（两广）", "confidence": 0.82, "source": "原文片段"},

    # ============ 30-005 写像轶事 ============
    {"item_id": "30-005", "text": "写像", "type": "unknown", "normalized": "写真肖像之事", "confidence": 0.78, "source": "原文片段"},
]
