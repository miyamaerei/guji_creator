# -*- coding: utf-8 -*-
"""《水东日记》卷 37 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "37-001 | 瀛国公诗顺帝考观音堂记", "37-002 | 刘江望海埚杀倭", "37-003 | 王恽纪梦叶谱杨荣",
    "37-004 | 朱熹论志石昭穆", "37-005 | 北方试马", "37-006 | 马莲花药方",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 37-001 瀛国公诗 ============
    {"item_id": "37-001", "text": "瀛国公", "type": "person", "normalized": "瀛国公（宋幼主）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "37-001", "text": "元君", "type": "person", "normalized": "元君（元宗室尚主者）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "37-001", "text": "明光宫", "type": "place", "normalized": "明光宫", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "37-001", "text": "虞台岭", "type": "place", "normalized": "虞台岭", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "37-001", "text": "观音堂", "type": "institution", "normalized": "虞台岭观音堂", "confidence": 0.8, "source": "原文片段"},

    # ============ 37-002 刘江杀倭 ============
    {"item_id": "37-002", "text": "刘江", "type": "person", "normalized": "刘江（刘荣，望海埚杀倭）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "37-002", "text": "中军左都督", "type": "official", "normalized": "中军左都督", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "37-002", "text": "辽东", "type": "place", "normalized": "辽东", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "37-002", "text": "望海埚", "type": "place", "normalized": "望海埚", "confidence": 0.85, "source": "原文片段"},

    # ============ 37-003 王恽纪梦 ============
    {"item_id": "37-003", "text": "王恽", "type": "person", "normalized": "王恽（元，纪梦）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "37-003", "text": "至元", "type": "era", "normalized": "至元（元世祖年号）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "37-003", "text": "真定", "type": "place", "normalized": "真定", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "37-003", "text": "杨荣", "type": "person", "normalized": "杨荣（图书）", "confidence": 0.82, "source": "原文片段"},

    # ============ 37-004 志石昭穆 ============
    {"item_id": "37-004", "text": "朱熹", "type": "person", "normalized": "朱熹（论志石昭穆）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "37-004", "text": "昭穆", "type": "unknown", "normalized": "昭穆（坟地位次之制）", "confidence": 0.82, "source": "原文片段"},

    # ============ 37-005 北方试马 ============
    {"item_id": "37-005", "text": "北方", "type": "place", "normalized": "北方", "confidence": 0.8, "source": "原文片段"},

    # ============ 37-006 马莲花方 ============
    {"item_id": "37-006", "text": "马莲花", "type": "unknown", "normalized": "马莲花（药草）", "confidence": 0.8, "source": "原文片段"},
]
