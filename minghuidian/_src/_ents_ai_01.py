# -*- coding: utf-8 -*-
"""卷一 宗人府 实体层 AI 判定（text 从指纹库原文词形取）。"""
RECORDS = [
    # org 衙门
    {"item_id": "001-001", "text": "大宗正院", "type": "institution", "rank_order": "未明", "confidence": "high"},
    {"item_id": "001-001", "text": "宗人府", "type": "institution", "rank_order": "文职衙门之首", "confidence": "high"},
    {"item_id": "001-001", "text": "行在宗人府", "type": "institution", "rank_order": "未明", "confidence": "high"},
    {"item_id": "001-015", "text": "南京宗人府", "type": "institution", "rank_order": "南京位次", "confidence": "high"},
    {"item_id": "001-016", "text": "经历司", "type": "institution", "rank_order": "未明", "confidence": "high"},
    {"item_id": "001-007", "text": "礼部", "type": "institution", "rank_order": "六部第三", "confidence": "high"},
    {"item_id": "001-008", "text": "吏部", "type": "institution", "rank_order": "六部之首", "confidence": "high"},
    {"item_id": "001-008", "text": "长史司", "type": "institution", "rank_order": "未明", "confidence": "high"},
    {"item_id": "001-009", "text": "户部", "type": "institution", "rank_order": "六部第二", "confidence": "high"},
    {"item_id": "001-009", "text": "兵部", "type": "institution", "rank_order": "六部第四", "confidence": "high"},
    {"item_id": "001-009", "text": "仪卫司", "type": "institution", "rank_order": "未明", "confidence": "high"},
    {"item_id": "001-009", "text": "群牧所", "type": "institution", "rank_order": "未明", "confidence": "high"},
    {"item_id": "001-010", "text": "工部", "type": "institution", "rank_order": "六部第六", "confidence": "high"},
    {"item_id": "001-011", "text": "翰林院", "type": "institution", "rank_order": "诸文职次序", "confidence": "high"},
    {"item_id": "001-011", "text": "史馆", "type": "institution", "rank_order": "未明", "confidence": "high"},
    {"item_id": "001-012", "text": "司礼监", "type": "institution", "rank_order": "未明", "confidence": "high"},
    {"item_id": "001-013", "text": "刑部", "type": "institution", "rank_order": "六部第五", "confidence": "high"},
    {"item_id": "001-013", "text": "顺天府", "type": "institution", "rank_order": "未明", "confidence": "high"},
    # off 官职
    {"item_id": "001-001", "text": "宗人令", "type": "official", "confidence": "high"},
    {"item_id": "001-001", "text": "左右宗正", "type": "official", "confidence": "high"},
    {"item_id": "001-001", "text": "左右宗人", "type": "official", "confidence": "high"},
    {"item_id": "001-008", "text": "长史", "type": "official", "confidence": "high"},
    {"item_id": "001-014", "text": "知印", "type": "official", "confidence": "high"},
    {"item_id": "001-014", "text": "办事吏", "type": "official", "confidence": "high"},
    # era 年号
    {"item_id": "001-001", "text": "洪武", "type": "era", "confidence": "high"},
    {"item_id": "001-001", "text": "永乐", "type": "era", "confidence": "high"},
    {"item_id": "001-001", "text": "洪熙", "type": "era", "confidence": "high"},
    {"item_id": "001-001", "text": "正统", "type": "era", "confidence": "high"},
    {"item_id": "001-012", "text": "宣德", "type": "era", "confidence": "high"},
    {"item_id": "001-013", "text": "弘治", "type": "era", "confidence": "high"},
    # doc 典籍文册
    {"item_id": "001-002", "text": "皇明祖训", "type": "doc", "confidence": "high"},
    {"item_id": "001-011", "text": "玉牒", "type": "doc", "confidence": "high"},
    {"item_id": "001-005", "text": "宗支簿籍", "type": "doc", "confidence": "high"},
]
