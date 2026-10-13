# -*- coding: utf-8 -*-
"""
【开发验证切片】L1 实体层源数据 —— 卷01 条01~条20
AI 只写 slot/item_id/text/type/解读字段；original 由打包器注入，不手抄。
text 必须逐字命中指纹库原文（否则记 GAP）。
实体类型：person/official/institution/place/era/work/system/posthumous/time/quantity/punishment/doc/unknown
"""
ENTITIES = [
    # ---------------- 条01 卷序论 ----------------
    {"slot": 1, "item_id": "01-001", "text": "中书省", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-001", "text": "六部", "type": "institution", "confidence": 0.98},
    {"slot": 3, "item_id": "01-001", "text": "尚书", "type": "official", "confidence": 0.98},
    {"slot": 4, "item_id": "01-001", "text": "侍郎", "type": "official", "confidence": 0.98},
    {"slot": 5, "item_id": "01-001", "text": "殿阁大学士", "type": "official", "confidence": 0.95},
    {"slot": 6, "item_id": "01-001", "text": "都察院", "type": "institution", "confidence": 0.98},
    {"slot": 7, "item_id": "01-001", "text": "通政司", "type": "institution", "confidence": 0.98},
    {"slot": 8, "item_id": "01-001", "text": "大理寺", "type": "institution", "confidence": 0.98},
    {"slot": 9, "item_id": "01-001", "text": "洪武十三年", "type": "era", "confidence": 0.98},

    # ---------------- 条02 宗人府 ----------------
    {"slot": 1, "item_id": "01-002", "text": "宗人府", "type": "institution", "confidence": 0.98},
    {"slot": 2, "item_id": "01-002", "text": "宗人令", "type": "official", "confidence": 0.98},
    {"slot": 3, "item_id": "01-002", "text": "左、右宗正", "type": "official", "confidence": 0.98},
    {"slot": 4, "item_id": "01-002", "text": "左、右宗人", "type": "official", "confidence": 0.98},
    {"slot": 5, "item_id": "01-002", "text": "正一品", "type": "quantity", "confidence": 0.98},
    {"slot": 6, "item_id": "01-002", "text": "玉牒", "type": "doc", "confidence": 0.95},
    {"slot": 7, "item_id": "01-002", "text": "经历司", "type": "institution", "confidence": 0.95},
    {"slot": 8, "item_id": "01-002", "text": "经历", "type": "official", "confidence": 0.95},
    {"slot": 9, "item_id": "01-002", "text": "正五品", "type": "quantity", "confidence": 0.98},
    {"slot": 10, "item_id": "01-002", "text": "洪武三年", "type": "era", "confidence": 0.98},
    {"slot": 11, "item_id": "01-002", "text": "大宗正院", "type": "institution", "confidence": 0.95},
    {"slot": 12, "item_id": "01-002", "text": "秦王樉", "type": "person", "confidence": 0.9},
    {"slot": 13, "item_id": "01-002", "text": "晋王", "type": "person", "confidence": 0.85},

    # ---------------- 条03 三公三孤 ----------------
    {"slot": 1, "item_id": "01-003", "text": "太师", "type": "official", "confidence": 0.98},
    {"slot": 2, "item_id": "01-003", "text": "太傅", "type": "official", "confidence": 0.98},
    {"slot": 3, "item_id": "01-003", "text": "太保", "type": "official", "confidence": 0.98},
    {"slot": 4, "item_id": "01-003", "text": "少师", "type": "official", "confidence": 0.98},
    {"slot": 5, "item_id": "01-003", "text": "少傅", "type": "official", "confidence": 0.98},
    {"slot": 6, "item_id": "01-003", "text": "少保", "type": "official", "confidence": 0.98},
    {"slot": 7, "item_id": "01-003", "text": "三公", "type": "institution", "confidence": 0.95},
    {"slot": 8, "item_id": "01-003", "text": "三孤", "type": "institution", "confidence": 0.95},
    {"slot": 9, "item_id": "01-003", "text": "李善长", "type": "person", "confidence": 0.95},
    {"slot": 10, "item_id": "01-003", "text": "徐达", "type": "person", "confidence": 0.95},
    {"slot": 11, "item_id": "01-003", "text": "常遇春", "type": "person", "confidence": 0.95},
    {"slot": 12, "item_id": "01-003", "text": "张辅", "type": "person", "confidence": 0.9},
    {"slot": 13, "item_id": "01-003", "text": "蹇义", "type": "person", "confidence": 0.9},
    {"slot": 14, "item_id": "01-003", "text": "杨士奇", "type": "person", "confidence": 0.95},
    {"slot": 15, "item_id": "01-003", "text": "夏原吉", "type": "person", "confidence": 0.9},
    {"slot": 16, "item_id": "01-003", "text": "英国公", "type": "official", "confidence": 0.9},
    {"slot": 17, "item_id": "01-003", "text": "华盖殿大学士", "type": "official", "confidence": 0.95},
    {"slot": 18, "item_id": "01-003", "text": "正一品", "type": "quantity", "confidence": 0.98},
    {"slot": 19, "item_id": "01-003", "text": "从一品", "type": "quantity", "confidence": 0.98},

    # ---------------- 条04 太子三师三少 ----------------
    {"slot": 1, "item_id": "01-004", "text": "太子太师", "type": "official", "confidence": 0.98},
    {"slot": 2, "item_id": "01-004", "text": "太子太傅", "type": "official", "confidence": 0.98},
    {"slot": 3, "item_id": "01-004", "text": "太子太保", "type": "official", "confidence": 0.98},
    {"slot": 4, "item_id": "01-004", "text": "太子少师", "type": "official", "confidence": 0.98},
    {"slot": 5, "item_id": "01-004", "text": "太子宾客", "type": "official", "confidence": 0.98},
    {"slot": 6, "item_id": "01-004", "text": "姚广孝", "type": "person", "confidence": 0.95},
    {"slot": 7, "item_id": "01-004", "text": "并从一品", "type": "quantity", "confidence": 0.95},
    {"slot": 8, "item_id": "01-004", "text": "并正二品", "type": "quantity", "confidence": 0.95},

    # ---------------- 条05 内阁 ----------------
    {"slot": 1, "item_id": "01-005", "text": "中极殿大学士", "type": "official", "confidence": 0.95},
    {"slot": 2, "item_id": "01-005", "text": "文渊阁大学士", "type": "official", "confidence": 0.95},
    {"slot": 3, "item_id": "01-005", "text": "东阁大学士", "type": "official", "confidence": 0.95},
    {"slot": 4, "item_id": "01-005", "text": "内阁", "type": "institution", "confidence": 0.98},
    {"slot": 5, "item_id": "01-005", "text": "票拟", "type": "system", "confidence": 0.95},
    {"slot": 6, "item_id": "01-005", "text": "并正五品", "type": "quantity", "confidence": 0.95},
    {"slot": 7, "item_id": "01-005", "text": "诏", "type": "doc", "confidence": 0.9},
    {"slot": 8, "item_id": "01-005", "text": "诰", "type": "doc", "confidence": 0.9},
    {"slot": 9, "item_id": "01-005", "text": "制", "type": "doc", "confidence": 0.85},
    {"slot": 10, "item_id": "01-005", "text": "题", "type": "doc", "confidence": 0.85},
    {"slot": 11, "item_id": "01-005", "text": "奏", "type": "doc", "confidence": 0.9},
    {"slot": 12, "item_id": "01-005", "text": "揭帖", "type": "doc", "confidence": 0.9},

    # ---------------- 条06 中书省 ----------------
    {"slot": 1, "item_id": "01-006", "text": "左、右丞相", "type": "official", "confidence": 0.98},
    {"slot": 2, "item_id": "01-006", "text": "平章政事", "type": "official", "confidence": 0.95},
    {"slot": 3, "item_id": "01-006", "text": "参知政事", "type": "official", "confidence": 0.95},
    {"slot": 4, "item_id": "01-006", "text": "左、右相国", "type": "official", "confidence": 0.9},
    {"slot": 5, "item_id": "01-006", "text": "中书舍人", "type": "official", "confidence": 0.95},
    {"slot": 6, "item_id": "01-006", "text": "李善长", "type": "person", "confidence": 0.95},
    {"slot": 7, "item_id": "01-006", "text": "徐达", "type": "person", "confidence": 0.95},

    # ---------------- 条07 罢中书省 ----------------
    {"slot": 1, "item_id": "01-007", "text": "胡惟庸", "type": "person", "confidence": 0.95},
    {"slot": 2, "item_id": "01-007", "text": "四辅官", "type": "official", "confidence": 0.95},
    {"slot": 3, "item_id": "01-007", "text": "王本", "type": "person", "confidence": 0.9},
    {"slot": 4, "item_id": "01-007", "text": "杜佑", "type": "person", "confidence": 0.85},
    {"slot": 5, "item_id": "01-007", "text": "洪武九年", "type": "era", "confidence": 0.95},
    {"slot": 6, "item_id": "01-007", "text": "十三年", "type": "era", "confidence": 0.9},
    {"slot": 7, "item_id": "01-007", "text": "十五年", "type": "era", "confidence": 0.85},
    {"slot": 8, "item_id": "01-007", "text": "中书舍人", "type": "official", "confidence": 0.95},

    # ---------------- 条08 内阁职权演变 ----------------
    {"slot": 1, "item_id": "01-008", "text": "杨士奇", "type": "person", "confidence": 0.95},
    {"slot": 2, "item_id": "01-008", "text": "杨荣", "type": "person", "confidence": 0.95},
    {"slot": 3, "item_id": "01-008", "text": "王文", "type": "person", "confidence": 0.9},
    {"slot": 4, "item_id": "01-008", "text": "左都御史", "type": "official", "confidence": 0.95},
    {"slot": 5, "item_id": "01-008", "text": "吏部尚书", "type": "official", "confidence": 0.95},

    # ---------------- 条09 吏部编制 ----------------
    {"slot": 1, "item_id": "01-009", "text": "吏部。", "type": "institution", "confidence": 0.98},
    {"slot": 2, "item_id": "01-009", "text": "文选、验封、稽勋、考功四清吏司", "type": "institution", "confidence": 0.95},
    {"slot": 3, "item_id": "01-009", "text": "司务厅", "type": "institution", "confidence": 0.95},
    {"slot": 4, "item_id": "01-009", "text": "郎中", "type": "official", "confidence": 0.98},
    {"slot": 5, "item_id": "01-009", "text": "员外郎", "type": "official", "confidence": 0.98},
    {"slot": 6, "item_id": "01-009", "text": "主事", "type": "official", "confidence": 0.98},
    {"slot": 7, "item_id": "01-009", "text": "司务", "type": "official", "confidence": 0.95},
    {"slot": 8, "item_id": "01-009", "text": "从九品", "type": "quantity", "confidence": 0.98},

    # ---------------- 条10 吏部尚书职掌 ----------------
    {"slot": 1, "item_id": "01-010", "text": "冢宰", "type": "official", "confidence": 0.9},

    # ---------------- 条11 司务 ----------------
    {"slot": 1, "item_id": "01-011", "text": "簿书", "type": "doc", "confidence": 0.9},
    {"slot": 2, "item_id": "01-011", "text": "主事印", "type": "doc", "confidence": 0.85},

    # ---------------- 条12 文选司职掌 ----------------
    {"slot": 1, "item_id": "01-012", "text": "文选", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-012", "text": "未入流", "type": "system", "confidence": 0.95},
    {"slot": 3, "item_id": "01-012", "text": "大选", "type": "system", "confidence": 0.95},
    {"slot": 4, "item_id": "01-012", "text": "急选", "type": "system", "confidence": 0.95},
    {"slot": 5, "item_id": "01-012", "text": "远方选", "type": "system", "confidence": 0.95},
    {"slot": 6, "item_id": "01-012", "text": "岁贡就教选", "type": "system", "confidence": 0.95},
    {"slot": 7, "item_id": "01-012", "text": "拣选", "type": "system", "confidence": 0.95},
    {"slot": 8, "item_id": "01-012", "text": "举人乞恩选", "type": "system", "confidence": 0.95},
    {"slot": 9, "item_id": "01-012", "text": "资簿", "type": "doc", "confidence": 0.9},
    {"slot": 10, "item_id": "01-012", "text": "推升", "type": "system", "confidence": 0.95},
    {"slot": 11, "item_id": "01-012", "text": "廷推", "type": "system", "confidence": 0.95},
    {"slot": 12, "item_id": "01-012", "text": "考满", "type": "system", "confidence": 0.95},
    {"slot": 13, "item_id": "01-012", "text": "传升", "type": "system", "confidence": 0.9},
    {"slot": 14, "item_id": "01-012", "text": "乞升", "type": "system", "confidence": 0.9},
    {"slot": 15, "item_id": "01-012", "text": "署职", "type": "system", "confidence": 0.95},
    {"slot": 16, "item_id": "01-012", "text": "试职", "type": "system", "confidence": 0.95},
    {"slot": 17, "item_id": "01-012", "text": "实授", "type": "system", "confidence": 0.95},
    {"slot": 18, "item_id": "01-012", "text": "科道", "type": "institution", "confidence": 0.9},

    # ---------------- 条13 验封司职掌 ----------------
    {"slot": 1, "item_id": "01-013", "text": "验封", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-013", "text": "诰券", "type": "doc", "confidence": 0.95},
    {"slot": 3, "item_id": "01-013", "text": "衍圣公", "type": "official", "confidence": 0.95},
    {"slot": 4, "item_id": "01-013", "text": "荫叙", "type": "system", "confidence": 0.95},
    {"slot": 5, "item_id": "01-013", "text": "官生", "type": "system", "confidence": 0.9},
    {"slot": 6, "item_id": "01-013", "text": "恩生", "type": "system", "confidence": 0.9},
    {"slot": 7, "item_id": "01-013", "text": "封赠", "type": "system", "confidence": 0.95},
    {"slot": 8, "item_id": "01-013", "text": "诰命", "type": "doc", "confidence": 0.95},
    {"slot": 9, "item_id": "01-013", "text": "敕命", "type": "doc", "confidence": 0.95},
    {"slot": 10, "item_id": "01-013", "text": "特进荣禄大夫", "type": "official", "confidence": 0.95},
    {"slot": 11, "item_id": "01-013", "text": "资善大夫", "type": "official", "confidence": 0.95},
    {"slot": 12, "item_id": "01-013", "text": "承务郎", "type": "official", "confidence": 0.95},
    {"slot": 13, "item_id": "01-013", "text": "一品夫人", "type": "posthumous", "confidence": 0.85},
    {"slot": 14, "item_id": "01-013", "text": "淑人", "type": "posthumous", "confidence": 0.85},
    {"slot": 15, "item_id": "01-013", "text": "洪武十六年", "type": "era", "confidence": 0.95},

    # ---------------- 条14 稽勋司职掌 ----------------
    {"slot": 1, "item_id": "01-014", "text": "稽勋", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-014", "text": "左、右柱国", "type": "official", "confidence": 0.95},
    {"slot": 3, "item_id": "01-014", "text": "柱国", "type": "official", "confidence": 0.95},
    {"slot": 4, "item_id": "01-014", "text": "正治上卿", "type": "official", "confidence": 0.95},
    {"slot": 5, "item_id": "01-014", "text": "资治尹", "type": "official", "confidence": 0.95},
    {"slot": 6, "item_id": "01-014", "text": "贴黄", "type": "system", "confidence": 0.95},
    {"slot": 7, "item_id": "01-014", "text": "清黄", "type": "system", "confidence": 0.95},
    {"slot": 8, "item_id": "01-014", "text": "钦天监", "type": "institution", "confidence": 0.95},

    # ---------------- 条15 考功司职掌 ----------------
    {"slot": 1, "item_id": "01-015", "text": "考功", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-015", "text": "初考", "type": "system", "confidence": 0.95},
    {"slot": 3, "item_id": "01-015", "text": "再考", "type": "system", "confidence": 0.95},
    {"slot": 4, "item_id": "01-015", "text": "通考", "type": "system", "confidence": 0.95},
    {"slot": 5, "item_id": "01-015", "text": "考察", "type": "system", "confidence": 0.95},
    {"slot": 6, "item_id": "01-015", "text": "黜陟", "type": "system", "confidence": 0.95},
    {"slot": 7, "item_id": "01-015", "text": "弹章", "type": "doc", "confidence": 0.9},

    # ---------------- 条16 六部沿革 ----------------
    {"slot": 1, "item_id": "01-016", "text": "四部", "type": "institution", "confidence": 0.9},
    {"slot": 2, "item_id": "01-016", "text": "周官", "type": "work", "confidence": 0.95},
    {"slot": 3, "item_id": "01-016", "text": "总部", "type": "institution", "confidence": 0.9},
    {"slot": 4, "item_id": "01-016", "text": "司勋", "type": "institution", "confidence": 0.9},
    {"slot": 5, "item_id": "01-016", "text": "清吏司", "type": "institution", "confidence": 0.95},
    {"slot": 6, "item_id": "01-016", "text": "洪武元年", "type": "era", "confidence": 0.98},
    {"slot": 7, "item_id": "01-016", "text": "二十九年", "type": "era", "confidence": 0.9},
    {"slot": 8, "item_id": "01-016", "text": "正三品", "type": "quantity", "confidence": 0.95},

    # ---------------- 条17 北京行部沿革 ----------------
    {"slot": 1, "item_id": "01-017", "text": "北京行部", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-017", "text": "六曹清吏司", "type": "institution", "confidence": 0.9},
    {"slot": 3, "item_id": "01-017", "text": "南京", "type": "place", "confidence": 0.98},
    {"slot": 4, "item_id": "01-017", "text": "北京", "type": "place", "confidence": 0.98},
    {"slot": 5, "item_id": "01-017", "text": "永乐元年", "type": "era", "confidence": 0.98},
    {"slot": 6, "item_id": "01-017", "text": "正统六年", "type": "era", "confidence": 0.98},
    {"slot": 7, "item_id": "01-017", "text": "行在", "type": "system", "confidence": 0.85},

    # ---------------- 条18 吏部尚书班位 ----------------
    {"slot": 1, "item_id": "01-018", "text": "丘濬", "type": "person", "confidence": 0.92},
    {"slot": 2, "item_id": "01-018", "text": "王恕", "type": "person", "confidence": 0.92},
    {"slot": 3, "item_id": "01-018", "text": "弘治六年", "type": "era", "confidence": 0.95},

    # ---------------- 条19 户部编制 ----------------
    {"slot": 1, "item_id": "01-019", "text": "户部。", "type": "institution", "confidence": 0.98},
    {"slot": 2, "item_id": "01-019", "text": "浙江、江西、湖广、陕西、广东、山东、福建、河南、山西、四川、广西、贵州、云南十三清吏司", "type": "institution", "confidence": 0.9},
    {"slot": 3, "item_id": "01-019", "text": "宝钞提举司", "type": "institution", "confidence": 0.95},
    {"slot": 4, "item_id": "01-019", "text": "提举", "type": "official", "confidence": 0.95},
    {"slot": 5, "item_id": "01-019", "text": "副提举", "type": "official", "confidence": 0.95},
    {"slot": 6, "item_id": "01-019", "text": "钞纸局", "type": "institution", "confidence": 0.95},
    {"slot": 7, "item_id": "01-019", "text": "印钞局", "type": "institution", "confidence": 0.95},
    {"slot": 8, "item_id": "01-019", "text": "大使", "type": "official", "confidence": 0.98},
    {"slot": 9, "item_id": "01-019", "text": "副使", "type": "official", "confidence": 0.98},
    {"slot": 10, "item_id": "01-019", "text": "典史", "type": "official", "confidence": 0.95},
    {"slot": 11, "item_id": "01-019", "text": "照磨", "type": "official", "confidence": 0.95},
    {"slot": 12, "item_id": "01-019", "text": "检校", "type": "official", "confidence": 0.95},
    {"slot": 13, "item_id": "01-019", "text": "太仓银库", "type": "institution", "confidence": 0.95},
    {"slot": 14, "item_id": "01-019", "text": "宣德七年", "type": "era", "confidence": 0.95},
    {"slot": 15, "item_id": "01-019", "text": "嘉靖中", "type": "era", "confidence": 0.9},

    # ---------------- 条20 户部尚书职掌 ----------------
    {"slot": 1, "item_id": "01-020", "text": "黄册", "type": "doc", "confidence": 0.95},
    {"slot": 2, "item_id": "01-020", "text": "岁会", "type": "system", "confidence": 0.9},
    {"slot": 3, "item_id": "01-020", "text": "赋役", "type": "system", "confidence": 0.95},
    {"slot": 4, "item_id": "01-020", "text": "投献", "type": "system", "confidence": 0.8},
    {"slot": 5, "item_id": "01-020", "text": "诡寄", "type": "system", "confidence": 0.8},
    {"slot": 6, "item_id": "01-020", "text": "影射", "type": "system", "confidence": 0.8},
    {"slot": 7, "item_id": "01-020", "text": "漕运", "type": "system", "confidence": 0.95},
    {"slot": 8, "item_id": "01-020", "text": "禄廪之制", "type": "system", "confidence": 0.9},
    {"slot": 9, "item_id": "01-020", "text": "洪武二十五年", "type": "era", "confidence": 0.95},
    {"slot": 10, "item_id": "01-020", "text": "一千四十四石", "type": "quantity", "confidence": 0.95},
]
