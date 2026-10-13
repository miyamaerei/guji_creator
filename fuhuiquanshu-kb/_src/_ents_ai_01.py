# -*- coding: utf-8 -*-
"""卷01 筮仕部·实体（20 条全）。"""
RECORDS = [
    # 01-001 总论 / 01-002 谒选（试点已建）
    {"item_id": "01-001", "text": "投牒需铨", "type": "behavior", "normalized": "投牒需铨", "confidence": "medium"},
    {"item_id": "01-001", "text": "捧檄司牧", "type": "behavior", "normalized": "捧檄司牧", "confidence": "medium"},
    {"item_id": "01-001", "text": "筮仕之地", "type": "place", "normalized": "筮仕之地", "confidence": "medium"},
    {"item_id": "01-002", "text": "江宁", "type": "place", "normalized": "江宁", "confidence": "high"},
    {"item_id": "01-002", "text": "大清律", "type": "work", "normalized": "大清律", "confidence": "high"},
    {"item_id": "01-002", "text": "六部条例", "type": "work", "normalized": "六部条例", "confidence": "high"},
    {"item_id": "01-002", "text": "京债", "type": "behavior", "normalized": "京债", "confidence": "high"},
    {"item_id": "01-002", "text": "铨曹", "type": "institution", "normalized": "铨曹", "confidence": "high"},
    {"item_id": "01-002", "text": "梵宇", "type": "place", "normalized": "梵宇", "confidence": "medium"},
    {"item_id": "01-002", "text": "六部", "type": "institution", "normalized": "六部", "confidence": "high"},
    # 01-003 投供验到
    {"item_id": "01-003", "text": "文选司", "type": "institution", "normalized": "文选司", "confidence": "high"},
    {"item_id": "01-003", "text": "互结", "type": "doc", "normalized": "互结", "confidence": "high"},
    {"item_id": "01-003", "text": "供状式", "type": "doc", "normalized": "供状式", "confidence": "high"},
    {"item_id": "01-003", "text": "天部", "type": "institution", "normalized": "天部", "confidence": "medium"},
    # 01-004 掣签
    {"item_id": "01-004", "text": "东长安门", "type": "place", "normalized": "东长安门", "confidence": "high"},
    {"item_id": "01-004", "text": "天安门", "type": "place", "normalized": "天安门", "confidence": "high"},
    {"item_id": "01-004", "text": "吏部", "type": "institution", "normalized": "吏部", "confidence": "high"},
    {"item_id": "01-004", "text": "缺签筒", "type": "object", "normalized": "缺签筒", "confidence": "medium"},
    {"item_id": "01-004", "text": "名签", "type": "object", "normalized": "名签", "confidence": "medium"},
    # 01-005 查全书
    {"item_id": "01-005", "text": "全书", "type": "work", "normalized": "全书", "confidence": "high"},
    {"item_id": "01-005", "text": "户部", "type": "institution", "normalized": "户部", "confidence": "high"},
    {"item_id": "01-005", "text": "由单", "type": "doc", "normalized": "由单", "confidence": "high"},
    # 01-008 发谕单
    {"item_id": "01-008", "text": "赋役全书", "type": "work", "normalized": "赋役全书", "confidence": "high"},
    # 01-006 访风俗
    {"item_id": "01-006", "text": "京师", "type": "place", "normalized": "京师", "confidence": "high"},
    {"item_id": "01-006", "text": "衙役", "type": "person", "normalized": "衙役", "confidence": "high"},
    {"item_id": "01-006", "text": "土豪", "type": "person", "normalized": "土豪", "confidence": "high"},
    # 01-007 拜客宴会
    {"item_id": "01-007", "text": "乡绅", "type": "person", "normalized": "乡绅", "confidence": "high"},
    {"item_id": "01-007", "text": "父母", "type": "official", "normalized": "父母官", "confidence": "medium"},
    # 01-008 发谕单
    {"item_id": "01-008", "text": "提塘报房", "type": "institution", "normalized": "提塘报房", "confidence": "medium"},
    {"item_id": "01-008", "text": "谕单", "type": "doc", "normalized": "谕单", "confidence": "high"},
    {"item_id": "01-008", "text": "经承", "type": "person", "normalized": "经承", "confidence": "high"},
    # 01-009 邮禀帖
    {"item_id": "01-009", "text": "禀启", "type": "doc", "normalized": "禀启", "confidence": "high"},
    {"item_id": "01-009", "text": "四六启", "type": "doc", "normalized": "四六启", "confidence": "high"},
    {"item_id": "01-009", "text": "封套", "type": "doc", "normalized": "封套", "confidence": "high"},
    {"item_id": "01-009", "text": "上台", "type": "official", "normalized": "上台", "confidence": "high"},
    {"item_id": "01-009", "text": "建溪", "type": "place", "normalized": "建溪", "confidence": "medium"},
    {"item_id": "01-009", "text": "延郡", "type": "place", "normalized": "延郡", "confidence": "medium"},
    {"item_id": "01-009", "text": "邹公", "type": "person", "normalized": "匪石邹公", "confidence": "medium"},
    # 01-010 延幕友
    {"item_id": "01-010", "text": "幕友", "type": "person", "normalized": "幕友", "confidence": "high"},
    {"item_id": "01-010", "text": "刑名", "type": "official", "normalized": "刑名", "confidence": "high"},
    {"item_id": "01-010", "text": "钱谷", "type": "official", "normalized": "钱谷", "confidence": "high"},
    {"item_id": "01-010", "text": "书启", "type": "doc", "normalized": "书启", "confidence": "high"},
    # 01-011 募家丁
    {"item_id": "01-011", "text": "家丁", "type": "person", "normalized": "家丁", "confidence": "high"},
    {"item_id": "01-011", "text": "长班", "type": "person", "normalized": "长班", "confidence": "high"},
    {"item_id": "01-011", "text": "管家", "type": "person", "normalized": "管家", "confidence": "high"},
    {"item_id": "01-011", "text": "保甲", "type": "system", "normalized": "保甲", "confidence": "high"},
    {"item_id": "01-011", "text": "中保", "type": "person", "normalized": "中保", "confidence": "high"},
    # 01-012 待接役
    {"item_id": "01-012", "text": "红批", "type": "doc", "normalized": "红批", "confidence": "high"},
    {"item_id": "01-012", "text": "吏书", "type": "person", "normalized": "吏书", "confidence": "high"},
    {"item_id": "01-012", "text": "丞簿", "type": "official", "normalized": "丞簿", "confidence": "high"},
    {"item_id": "01-012", "text": "典史", "type": "official", "normalized": "典史", "confidence": "high"},
    {"item_id": "01-012", "text": "驿廵", "type": "official", "normalized": "驿廵", "confidence": "high"},
    # 01-013 立号簿
    {"item_id": "01-013", "text": "总号薄", "type": "doc", "normalized": "总号簿", "confidence": "high"},
    {"item_id": "01-013", "text": "门簿", "type": "doc", "normalized": "门簿", "confidence": "high"},
    {"item_id": "01-013", "text": "收仪簿", "type": "doc", "normalized": "收仪簿", "confidence": "high"},
    {"item_id": "01-013", "text": "请饯簿", "type": "doc", "normalized": "请饯簿", "confidence": "high"},
    # 01-014 择到任吉期
    {"item_id": "01-014", "text": "天德", "type": "system", "normalized": "天德", "confidence": "high"},
    {"item_id": "01-014", "text": "月德", "type": "system", "normalized": "月德", "confidence": "high"},
    {"item_id": "01-014", "text": "黄道", "type": "system", "normalized": "黄道", "confidence": "high"},
    {"item_id": "01-014", "text": "东光", "type": "place", "normalized": "东光", "confidence": "high"},
    {"item_id": "01-014", "text": "发微历", "type": "work", "normalized": "发微历", "confidence": "medium"},
    {"item_id": "01-014", "text": "窦萍", "type": "person", "normalized": "窦萍", "confidence": "medium"},
    {"item_id": "01-014", "text": "康熙", "type": "era", "normalized": "康熙", "confidence": "high"},
    # 01-015 畵凭领凭
    {"item_id": "01-015", "text": "吏科", "type": "institution", "normalized": "吏科", "confidence": "high"},
    {"item_id": "01-015", "text": "选司", "type": "institution", "normalized": "选司", "confidence": "high"},
    {"item_id": "01-015", "text": "文凭", "type": "doc", "normalized": "文凭", "confidence": "high"},
    {"item_id": "01-015", "text": "脚色", "type": "doc", "normalized": "脚色", "confidence": "high"},
    {"item_id": "01-015", "text": "领状式", "type": "doc", "normalized": "领状式", "confidence": "high"},
    {"item_id": "01-015", "text": "出印结式", "type": "doc", "normalized": "出印结式", "confidence": "high"},
    # 01-016 辞朝
    {"item_id": "01-016", "text": "鸿胪寺", "type": "institution", "normalized": "鸿胪寺", "confidence": "high"},
    {"item_id": "01-016", "text": "河南道", "type": "institution", "normalized": "河南道", "confidence": "high"},
    {"item_id": "01-016", "text": "午门", "type": "place", "normalized": "午门", "confidence": "high"},
    {"item_id": "01-016", "text": "左掖门", "type": "place", "normalized": "左掖门", "confidence": "high"},
    # 01-017 辞行
    {"item_id": "01-017", "text": "座主", "type": "person", "normalized": "座主", "confidence": "high"},
    # 01-018 荐托
    {"item_id": "01-018", "text": "上司", "type": "official", "normalized": "上司", "confidence": "high"},
    # 01-020 起程
    {"item_id": "01-020", "text": "印结", "type": "doc", "normalized": "印结", "confidence": "high"},
    {"item_id": "01-020", "text": "甘结", "type": "doc", "normalized": "甘结", "confidence": "high"},
    {"item_id": "01-020", "text": "医生", "type": "person", "normalized": "医生", "confidence": "medium"},
]
