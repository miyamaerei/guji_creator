# -*- coding: utf-8 -*-
"""卷03（明职·卷一，26 条）实体层源数据（AI 逐条判定，2026-10-12）。
text 一律用原文词形（含异体字如廵/飬）；normalized 为规范归一词形；original 由打包器注入。"""
RECORDS = [
    # 03-001 吏承出身：说理劝勉，实体极少
    {"slot": 1, "item_id": "03-001", "text": "吏承", "type": "system", "normalized": "吏承", "confidence": "medium"},
    # 03-002 仓官之职
    {"slot": 2, "item_id": "03-002", "text": "仓官", "type": "official", "normalized": "仓官", "confidence": "high"},
    {"slot": 3, "item_id": "03-002", "text": "册籍", "type": "doc", "normalized": "册籍", "confidence": "medium"},
    # 03-003 廵检之职
    {"slot": 4, "item_id": "03-003", "text": "廵检", "type": "official", "normalized": "巡检", "confidence": "high"},
    {"slot": 5, "item_id": "03-003", "text": "弓兵", "type": "official", "normalized": "弓兵", "confidence": "high"},
    # 03-004 驿递之职
    {"slot": 6, "item_id": "03-004", "text": "驿递", "type": "institution", "normalized": "驿递", "confidence": "high"},
    {"slot": 7, "item_id": "03-004", "text": "驿丞大使", "type": "official", "normalized": "驿丞大使", "confidence": "high"},
    {"slot": 8, "item_id": "03-004", "text": "马头", "type": "official", "normalized": "马头", "confidence": "medium"},
    {"slot": 9, "item_id": "03-004", "text": "站银", "type": "system", "normalized": "站银", "confidence": "medium"},
    # 03-005 税课司之职
    {"slot": 10, "item_id": "03-005", "text": "税课司", "type": "institution", "normalized": "税课司", "confidence": "high"},
    {"slot": 11, "item_id": "03-005", "text": "廵拦", "type": "official", "normalized": "巡拦", "confidence": "medium"},
    {"slot": 12, "item_id": "03-005", "text": "集头老人", "type": "official", "normalized": "集头老人", "confidence": "medium"},
    # 03-006 司狱官之职
    {"slot": 13, "item_id": "03-006", "text": "司狱官", "type": "official", "normalized": "司狱官", "confidence": "high"},
    {"slot": 14, "item_id": "03-006", "text": "牢头狱霸", "type": "person", "normalized": "牢头狱霸", "confidence": "medium"},
    {"slot": 15, "item_id": "03-006", "text": "女监", "type": "institution", "normalized": "女监", "confidence": "high"},
    # 03-007 库官之职
    {"slot": 16, "item_id": "03-007", "text": "库官", "type": "official", "normalized": "库官", "confidence": "high"},
    {"slot": 17, "item_id": "03-007", "text": "库吏", "type": "official", "normalized": "库吏", "confidence": "high"},
    {"slot": 18, "item_id": "03-007", "text": "大户解官", "type": "official", "normalized": "大户解官", "confidence": "medium"},
    {"slot": 19, "item_id": "03-007", "text": "火耗", "type": "system", "normalized": "火耗", "confidence": "high"},
    {"slot": 20, "item_id": "03-007", "text": "天平", "type": "object", "normalized": "天平", "confidence": "medium"},
    # 03-008 官恩例贡出身
    {"slot": 21, "item_id": "03-008", "text": "汲黯", "type": "person", "normalized": "汲黯", "confidence": "high"},
    {"slot": 22, "item_id": "03-008", "text": "霍光", "type": "person", "normalized": "霍光", "confidence": "high"},
    {"slot": 23, "item_id": "03-008", "text": "张释之", "type": "person", "normalized": "张释之", "confidence": "high"},
    {"slot": 24, "item_id": "03-008", "text": "卜式", "type": "person", "normalized": "卜式", "confidence": "high"},
    {"slot": 25, "item_id": "03-008", "text": "官恩生", "type": "system", "normalized": "官恩生", "confidence": "medium"},
    {"slot": 26, "item_id": "03-008", "text": "例贡生", "type": "system", "normalized": "例贡生", "confidence": "medium"},
    # 03-009 贡士出身
    {"slot": 27, "item_id": "03-009", "text": "庠序", "type": "institution", "normalized": "庠序", "confidence": "high"},
    {"slot": 28, "item_id": "03-009", "text": "廪膳", "type": "system", "normalized": "廪膳", "confidence": "medium"},
    {"slot": 29, "item_id": "03-009", "text": "国学", "type": "institution", "normalized": "国学", "confidence": "high"},
    # 03-010 科甲出身
    {"slot": 30, "item_id": "03-010", "text": "科甲", "type": "system", "normalized": "科甲", "confidence": "high"},
    {"slot": 31, "item_id": "03-010", "text": "守令", "type": "official", "normalized": "守令", "confidence": "high"},
    {"slot": 32, "item_id": "03-010", "text": "监司", "type": "official", "normalized": "监司", "confidence": "high"},
    {"slot": 33, "item_id": "03-010", "text": "抚按", "type": "official", "normalized": "抚按", "confidence": "high"},
    # 03-011 教官之职
    {"slot": 34, "item_id": "03-011", "text": "教官", "type": "official", "normalized": "教官", "confidence": "high"},
    {"slot": 35, "item_id": "03-011", "text": "曹月川", "type": "person", "normalized": "曹端", "confidence": "high"},
    {"slot": 36, "item_id": "03-011", "text": "霍州", "type": "place", "normalized": "霍州", "confidence": "high"},
    {"slot": 37, "item_id": "03-011", "text": "蒲州", "type": "place", "normalized": "蒲州", "confidence": "high"},
    {"slot": 38, "item_id": "03-011", "text": "编修", "type": "official", "normalized": "编修", "confidence": "high"},
    {"slot": 39, "item_id": "03-011", "text": "检讨", "type": "official", "normalized": "检讨", "confidence": "high"},
    {"slot": 40, "item_id": "03-011", "text": "御史", "type": "official", "normalized": "御史", "confidence": "high"},
    {"slot": 41, "item_id": "03-011", "text": "给事中", "type": "official", "normalized": "给事中", "confidence": "high"},
    # 03-012 弟子之职（一读书缘由）
    {"slot": 42, "item_id": "03-012", "text": "经史", "type": "work", "normalized": "经史", "confidence": "high"},
    {"slot": 43, "item_id": "03-012", "text": "伊尹", "type": "person", "normalized": "伊尹", "confidence": "high"},
    {"slot": 44, "item_id": "03-012", "text": "周公", "type": "person", "normalized": "周公", "confidence": "high"},
    {"slot": 45, "item_id": "03-012", "text": "管仲", "type": "person", "normalized": "管仲", "confidence": "high"},
    {"slot": 46, "item_id": "03-012", "text": "范睢", "type": "person", "normalized": "范睢", "confidence": "high"},
    {"slot": 47, "item_id": "03-012", "text": "苏张", "type": "person", "normalized": "苏张", "confidence": "medium"},
    {"slot": 48, "item_id": "03-012", "text": "文中子", "type": "person", "normalized": "文中子", "confidence": "high"},
    {"slot": 49, "item_id": "03-012", "text": "漆雕开", "type": "person", "normalized": "漆雕开", "confidence": "high"},
    {"slot": 50, "item_id": "03-012", "text": "孔子", "type": "person", "normalized": "孔子", "confidence": "high"},
    {"slot": 51, "item_id": "03-012", "text": "孟子", "type": "person", "normalized": "孟子", "confidence": "high"},
    # 03-013 弟子之职二（作人道理）
    {"slot": 52, "item_id": "03-013", "text": "皇祖", "type": "person", "normalized": "明太祖", "confidence": "medium"},
    {"slot": 53, "item_id": "03-013", "text": "四方平定巾", "type": "object", "normalized": "四方平定巾", "confidence": "high"},
    {"slot": 54, "item_id": "03-013", "text": "儒巾", "type": "object", "normalized": "儒巾", "confidence": "high"},
    {"slot": 55, "item_id": "03-013", "text": "刘凤起", "type": "person", "normalized": "刘凤起", "confidence": "high"},
    {"slot": 56, "item_id": "03-013", "text": "刘凤仪", "type": "person", "normalized": "刘凤仪", "confidence": "high"},
    {"slot": 57, "item_id": "03-013", "text": "周继登", "type": "person", "normalized": "周继登", "confidence": "high"},
    {"slot": 58, "item_id": "03-013", "text": "李锺翠", "type": "person", "normalized": "李锺翠", "confidence": "high"},
    # 03-014 州县佐贰之职
    {"slot": 59, "item_id": "03-014", "text": "州同", "type": "official", "normalized": "州同", "confidence": "high"},
    {"slot": 60, "item_id": "03-014", "text": "州判", "type": "official", "normalized": "州判", "confidence": "high"},
    {"slot": 61, "item_id": "03-014", "text": "县丞", "type": "official", "normalized": "县丞", "confidence": "high"},
    {"slot": 62, "item_id": "03-014", "text": "主簿", "type": "official", "normalized": "主簿", "confidence": "high"},
    {"slot": 63, "item_id": "03-014", "text": "佐贰", "type": "official", "normalized": "佐贰", "confidence": "high"},
    {"slot": 64, "item_id": "03-014", "text": "里书", "type": "official", "normalized": "里书", "confidence": "medium"},
    {"slot": 65, "item_id": "03-014", "text": "皂快", "type": "official", "normalized": "皂快", "confidence": "medium"},
    # 03-015 太原谕属
    {"slot": 66, "item_id": "03-015", "text": "太原", "type": "place", "normalized": "太原", "confidence": "high"},
    {"slot": 67, "item_id": "03-015", "text": "伊尹", "type": "person", "normalized": "伊尹", "confidence": "high"},
    # 03-016 知州知县之职
    {"slot": 68, "item_id": "03-016", "text": "知州知县", "type": "official", "normalized": "知州知县", "confidence": "high"},
    {"slot": 69, "item_id": "03-016", "text": "守令", "type": "official", "normalized": "守令", "confidence": "high"},
    # 03-017 同知通判推官之职
    {"slot": 70, "item_id": "03-017", "text": "同知", "type": "official", "normalized": "同知", "confidence": "high"},
    {"slot": 71, "item_id": "03-017", "text": "通判", "type": "official", "normalized": "通判", "confidence": "high"},
    {"slot": 72, "item_id": "03-017", "text": "推官", "type": "official", "normalized": "推官", "confidence": "high"},
    {"slot": 73, "item_id": "03-017", "text": "查盘", "type": "system", "normalized": "查盘", "confidence": "high"},
    # 03-018 知府之职
    {"slot": 74, "item_id": "03-018", "text": "知府", "type": "official", "normalized": "知府", "confidence": "high"},
    {"slot": 75, "item_id": "03-018", "text": "知州知县", "type": "official", "normalized": "知州知县", "confidence": "high"},
    # 03-019 盐运司之职
    {"slot": 76, "item_id": "03-019", "text": "盐运司", "type": "institution", "normalized": "盐运司", "confidence": "high"},
    {"slot": 77, "item_id": "03-019", "text": "解池", "type": "place", "normalized": "解池", "confidence": "high"},
    {"slot": 78, "item_id": "03-019", "text": "河东", "type": "place", "normalized": "河东", "confidence": "high"},
    {"slot": 79, "item_id": "03-019", "text": "西安", "type": "place", "normalized": "西安", "confidence": "high"},
    {"slot": 80, "item_id": "03-019", "text": "山西", "type": "place", "normalized": "山西", "confidence": "high"},
    {"slot": 81, "item_id": "03-019", "text": "太汾", "type": "place", "normalized": "太汾", "confidence": "high"},
    {"slot": 82, "item_id": "03-019", "text": "富平", "type": "place", "normalized": "富平", "confidence": "high"},
    {"slot": 83, "item_id": "03-019", "text": "商盐", "type": "object", "normalized": "商盐", "confidence": "medium"},
    {"slot": 84, "item_id": "03-019", "text": "土盐", "type": "object", "normalized": "土盐", "confidence": "medium"},
    # 03-020 守廵道之职
    {"slot": 85, "item_id": "03-020", "text": "守廵道", "type": "official", "normalized": "守巡道", "confidence": "high"},
    {"slot": 86, "item_id": "03-020", "text": "布政司", "type": "institution", "normalized": "布政司", "confidence": "high"},
    {"slot": 87, "item_id": "03-020", "text": "按察司", "type": "institution", "normalized": "按察司", "confidence": "high"},
    # 03-021 提学道之职
    {"slot": 88, "item_id": "03-021", "text": "提学道", "type": "official", "normalized": "提学道", "confidence": "high"},
    {"slot": 89, "item_id": "03-021", "text": "督学使君", "type": "official", "normalized": "督学使君", "confidence": "medium"},
    {"slot": 90, "item_id": "03-021", "text": "桓荣", "type": "person", "normalized": "桓荣", "confidence": "high"},
    # 03-022 按察司之职
    {"slot": 91, "item_id": "03-022", "text": "按察司", "type": "institution", "normalized": "按察司", "confidence": "high"},
    {"slot": 92, "item_id": "03-022", "text": "按察使", "type": "official", "normalized": "按察使", "confidence": "high"},
    {"slot": 93, "item_id": "03-022", "text": "都察院", "type": "institution", "normalized": "都察院", "confidence": "high"},
    {"slot": 94, "item_id": "03-022", "text": "廷尉", "type": "official", "normalized": "廷尉", "confidence": "high"},
    {"slot": 95, "item_id": "03-022", "text": "提刑", "type": "official", "normalized": "提刑", "confidence": "medium"},
    {"slot": 96, "item_id": "03-022", "text": "山西臬司", "type": "institution", "normalized": "山西臬司", "confidence": "medium"},
    # 03-023 布政司之职
    {"slot": 97, "item_id": "03-023", "text": "布政司", "type": "institution", "normalized": "布政司", "confidence": "high"},
    {"slot": 98, "item_id": "03-023", "text": "行中书省", "type": "institution", "normalized": "行中书省", "confidence": "high"},
    {"slot": 99, "item_id": "03-023", "text": "中书省", "type": "institution", "normalized": "中书省", "confidence": "high"},
    # 03-024 武职一
    {"slot": 100, "item_id": "03-024", "text": "武职", "type": "official", "normalized": "武职", "confidence": "high"},
    {"slot": 101, "item_id": "03-024", "text": "太原营", "type": "institution", "normalized": "太原营", "confidence": "high"},
    {"slot": 102, "item_id": "03-024", "text": "马军", "type": "official", "normalized": "马军", "confidence": "medium"},
    {"slot": 103, "item_id": "03-024", "text": "步军", "type": "official", "normalized": "步军", "confidence": "medium"},
    # 03-025 武职二
    {"slot": 104, "item_id": "03-025", "text": "武经要览", "type": "work", "normalized": "武经要览", "confidence": "high"},
    {"slot": 105, "item_id": "03-025", "text": "百战奇法", "type": "work", "normalized": "百战奇法", "confidence": "high"},
    {"slot": 106, "item_id": "03-025", "text": "古今将畧", "type": "work", "normalized": "古今将略", "confidence": "high"},
    {"slot": 107, "item_id": "03-025", "text": "方畧摘要", "type": "work", "normalized": "方略摘要", "confidence": "high"},
    {"slot": 108, "item_id": "03-025", "text": "六壬", "type": "work", "normalized": "六壬", "confidence": "medium"},
    # 03-026 督抚之职
    {"slot": 109, "item_id": "03-026", "text": "督抚", "type": "official", "normalized": "督抚", "confidence": "high"},
    {"slot": 110, "item_id": "03-026", "text": "总兵", "type": "official", "normalized": "总兵", "confidence": "high"},
    {"slot": 111, "item_id": "03-026", "text": "参将", "type": "official", "normalized": "参将", "confidence": "high"},
    {"slot": 112, "item_id": "03-026", "text": "游击", "type": "official", "normalized": "游击", "confidence": "high"},
    {"slot": 113, "item_id": "03-026", "text": "守备", "type": "official", "normalized": "守备", "confidence": "high"},
    {"slot": 114, "item_id": "03-026", "text": "操防", "type": "official", "normalized": "操防", "confidence": "medium"},
    {"slot": 115, "item_id": "03-026", "text": "都司", "type": "official", "normalized": "都司", "confidence": "high"},
    {"slot": 116, "item_id": "03-026", "text": "兵备", "type": "official", "normalized": "兵备", "confidence": "high"},
    {"slot": 117, "item_id": "03-026", "text": "三关", "type": "place", "normalized": "三关", "confidence": "high"},
    {"slot": 118, "item_id": "03-026", "text": "鴈门", "type": "place", "normalized": "雁门", "confidence": "high"},
]
