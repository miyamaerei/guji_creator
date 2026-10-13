# -*- coding: utf-8 -*-
"""卷05（民务卷三，8 条）实体层源数据（AI 逐条判定，2026-10-12）。
text 一律原文词形；normalized 规范归一词形；original 由打包器注入。"""
RECORDS = [
    # 条1 查理乡甲
    {"slot": 1, "item_id": "05-001", "text": "乡甲约", "type": "work", "normalized": "乡甲约", "confidence": "high"},
    {"slot": 2, "item_id": "05-001", "text": "保甲", "type": "system", "normalized": "保甲", "confidence": "high"},
    {"slot": 3, "item_id": "05-001", "text": "乡约", "type": "system", "normalized": "乡约", "confidence": "high"},
    {"slot": 4, "item_id": "05-001", "text": "明伦堂", "type": "institution", "normalized": "明伦堂", "confidence": "high"},
    {"slot": 5, "item_id": "05-001", "text": "圣谕牌", "type": "object", "normalized": "圣谕牌", "confidence": "high"},
    {"slot": 6, "item_id": "05-001", "text": "襄垣约", "type": "work", "normalized": "襄垣约", "confidence": "high"},
    {"slot": 7, "item_id": "05-001", "text": "约正", "type": "official", "normalized": "约正", "confidence": "high"},
    {"slot": 8, "item_id": "05-001", "text": "甲长", "type": "official", "normalized": "甲长", "confidence": "high"},
    {"slot": 9, "item_id": "05-001", "text": "讲史", "type": "official", "normalized": "讲史", "confidence": "medium"},
    # 条2 附乡甲劝语（白话劝语，无新实体）
    # 条3 兴复社学
    {"slot": 10, "item_id": "05-003", "text": "社学", "type": "institution", "normalized": "社学", "confidence": "high"},
    {"slot": 11, "item_id": "05-003", "text": "文庙", "type": "institution", "normalized": "文庙", "confidence": "high"},
    {"slot": 12, "item_id": "05-003", "text": "小学", "type": "work", "normalized": "小学", "confidence": "high"},
    {"slot": 13, "item_id": "05-003", "text": "孝经", "type": "work", "normalized": "孝经", "confidence": "high"},
    {"slot": 14, "item_id": "05-003", "text": "三字经", "type": "work", "normalized": "三字经", "confidence": "high"},
    {"slot": 15, "item_id": "05-003", "text": "百家姓", "type": "work", "normalized": "百家姓", "confidence": "high"},
    {"slot": 16, "item_id": "05-003", "text": "千字文", "type": "work", "normalized": "千字文", "confidence": "high"},
    {"slot": 17, "item_id": "05-003", "text": "姜字体", "type": "system", "normalized": "姜体字", "confidence": "medium"},
    {"slot": 18, "item_id": "05-003", "text": "陟岵", "type": "work", "normalized": "陟岵", "confidence": "high"},
    {"slot": 19, "item_id": "05-003", "text": "蓼莪", "type": "work", "normalized": "蓼莪", "confidence": "high"},
    {"slot": 20, "item_id": "05-003", "text": "凯风", "type": "work", "normalized": "凯风", "confidence": "high"},
    {"slot": 21, "item_id": "05-003", "text": "棠棣", "type": "work", "normalized": "棠棣", "confidence": "high"},
    {"slot": 22, "item_id": "05-003", "text": "采苓", "type": "work", "normalized": "采苓", "confidence": "high"},
    {"slot": 23, "item_id": "05-003", "text": "青蝇", "type": "work", "normalized": "青蝇", "confidence": "high"},
    {"slot": 24, "item_id": "05-003", "text": "伐木", "type": "work", "normalized": "伐木", "confidence": "high"},
    {"slot": 25, "item_id": "05-003", "text": "相鼠", "type": "work", "normalized": "相鼠", "confidence": "high"},
    {"slot": 26, "item_id": "05-003", "text": "白驹", "type": "work", "normalized": "白驹", "confidence": "high"},
    # 条4 修举学政
    {"slot": 27, "item_id": "05-004", "text": "风宪约", "type": "work", "normalized": "风宪约", "confidence": "high"},
    {"slot": 28, "item_id": "05-004", "text": "洪武正韵", "type": "work", "normalized": "洪武正韵", "confidence": "high"},
    {"slot": 29, "item_id": "05-004", "text": "海篇直音", "type": "work", "normalized": "海篇直音", "confidence": "high"},
    {"slot": 30, "item_id": "05-004", "text": "四书", "type": "work", "normalized": "四书", "confidence": "high"},
    {"slot": 31, "item_id": "05-004", "text": "进德簿", "type": "doc", "normalized": "进德簿", "confidence": "high"},
    {"slot": 32, "item_id": "05-004", "text": "修业簿", "type": "doc", "normalized": "修业簿", "confidence": "high"},
    {"slot": 33, "item_id": "05-004", "text": "文山", "type": "person", "normalized": "文天祥", "confidence": "high"},
    {"slot": 34, "item_id": "05-004", "text": "燕台", "type": "place", "normalized": "燕台", "confidence": "medium"},
    {"slot": 35, "item_id": "05-004", "text": "济南", "type": "place", "normalized": "济南", "confidence": "high"},
    {"slot": 36, "item_id": "05-004", "text": "云中", "type": "place", "normalized": "云中", "confidence": "medium"},
    {"slot": 37, "item_id": "05-004", "text": "圣谕六条", "type": "doc", "normalized": "圣谕六条", "confidence": "high"},
    # 条5 禁约风俗
    {"slot": 38, "item_id": "05-005", "text": "汾州府", "type": "place", "normalized": "汾州府", "confidence": "high"},
    {"slot": 39, "item_id": "05-005", "text": "王府", "type": "institution", "normalized": "王府", "confidence": "high"},
    {"slot": 40, "item_id": "05-005", "text": "宪纲", "type": "work", "normalized": "宪纲", "confidence": "medium"},
    {"slot": 41, "item_id": "05-005", "text": "洪武", "type": "era", "normalized": "洪武", "confidence": "high"},
    # 条6 恶风当戒者十
    {"slot": 42, "item_id": "05-006", "text": "大明会典", "type": "work", "normalized": "大明会典", "confidence": "high"},
    {"slot": 43, "item_id": "05-006", "text": "申明亭", "type": "institution", "normalized": "申明亭", "confidence": "high"},
    {"slot": 44, "item_id": "05-006", "text": "刁民簿", "type": "doc", "normalized": "刁民簿", "confidence": "high"},
    # 条7 有司杂禁
    {"slot": 45, "item_id": "05-007", "text": "纲银", "type": "system", "normalized": "纲银", "confidence": "high"},
    {"slot": 46, "item_id": "05-007", "text": "军粮", "type": "system", "normalized": "军粮", "confidence": "high"},
    {"slot": 47, "item_id": "05-007", "text": "洪武旧样", "type": "era", "normalized": "洪武旧样", "confidence": "medium"},
    {"slot": 48, "item_id": "05-007", "text": "赤历", "type": "doc", "normalized": "赤历", "confidence": "high"},
    # 条8 官问
    {"slot": 49, "item_id": "05-008", "text": "延绥", "type": "place", "normalized": "延绥", "confidence": "high"},
    {"slot": 50, "item_id": "05-008", "text": "朔方", "type": "place", "normalized": "朔方", "confidence": "medium"},
    {"slot": 51, "item_id": "05-008", "text": "庄明", "type": "person", "normalized": "庄明", "confidence": "low"},
    {"slot": 52, "item_id": "05-008", "text": "长河", "type": "place", "normalized": "黄河", "confidence": "medium"},
]
