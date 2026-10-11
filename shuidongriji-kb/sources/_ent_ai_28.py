# -*- coding: utf-8 -*-
"""《水东日记》卷 28 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "28-001 | 胡文穆杨文贞序谱", "28-002 | 文章正宗许有壬诗", "28-003 | 王暕东华铁狮子宅",
    "28-004 | 帅府杀虎法海寿射生", "28-005 | 宣府庙学碑进士碑磨字",
    "28-006 | 己巳北狩兴安于谦", "28-007 | 军医范真栢玉王宇服药",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 28-001 胡杨序谱 ============
    {"item_id": "28-001", "text": "胡文穆", "type": "person", "normalized": "胡广（谥文穆）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "28-001", "text": "杨文贞", "type": "person", "normalized": "杨士奇（谥文贞）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "28-001", "text": "文皇", "type": "person", "normalized": "明成祖（文皇帝）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "28-001", "text": "庐陵", "type": "place", "normalized": "庐陵", "confidence": 0.85, "source": "原文片段"},

    # ============ 28-002 文章正宗 ============
    {"item_id": "28-002", "text": "文章正宗", "type": "work", "normalized": "文章正宗（真德秀编）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "28-002", "text": "西山", "type": "person", "normalized": "真德秀（号西山）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "28-002", "text": "许有壬", "type": "person", "normalized": "许有壬（元，中丞）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "28-002", "text": "吴闲闲", "type": "person", "normalized": "吴闲闲（元，诗）", "confidence": 0.8, "source": "原文片段"},

    # ============ 28-003 东华铁狮子宅 ============
    {"item_id": "28-003", "text": "王暕", "type": "person", "normalized": "王暕（中书舍人）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "28-003", "text": "少师杨公", "type": "person", "normalized": "杨士奇（少师）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "28-003", "text": "东华铁狮子", "type": "place", "normalized": "东华门铁狮子胡同", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "28-003", "text": "中书舍人", "type": "official", "normalized": "中书舍人", "confidence": 0.85, "source": "原文片段"},

    # ============ 28-004 杀虎射生 ============
    {"item_id": "28-004", "text": "帅府", "type": "institution", "normalized": "帅府", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "28-004", "text": "海寿", "type": "person", "normalized": "海寿（射生）", "confidence": 0.8, "source": "原文片段"},

    # ============ 28-005 宣府庙学碑 ============
    {"item_id": "28-005", "text": "宣府", "type": "place", "normalized": "宣府", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "28-005", "text": "庙学", "type": "institution", "normalized": "宣府庙学", "confidence": 0.82, "source": "原文片段"},

    # ============ 28-006 己巳北狩 ============
    {"item_id": "28-006", "text": "己巳", "type": "era", "normalized": "己巳（正统十四年）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "28-006", "text": "兴安", "type": "person", "normalized": "兴安（太监）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "28-006", "text": "于谦", "type": "person", "normalized": "于谦", "confidence": 0.9, "source": "原文片段"},

    # ============ 28-007 军医服药 ============
    {"item_id": "28-007", "text": "范真栢玉", "type": "person", "normalized": "范真栢玉（军医）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "28-007", "text": "王宇", "type": "person", "normalized": "王宇（服药）", "confidence": 0.8, "source": "原文片段"},
]
