# -*- coding: utf-8 -*-
"""
【卷01 续】条21–53 L1 实体层源数据 —— 户部余条/礼部/兵部/刑部/工部
AI 只写 slot/item_id/text/type；original 由打包器注入。
"""
ENTITIES = [
    # ============ 条21 户部十三司职掌 ============
    {"slot": 1, "item_id": "01-021", "text": "十三司", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-021", "text": "浙江司", "type": "institution", "confidence": 0.92},
    {"slot": 3, "item_id": "01-021", "text": "两京", "type": "place", "confidence": 0.9},
    {"slot": 4, "item_id": "01-021", "text": "直隶", "type": "place", "confidence": 0.9},
    {"slot": 5, "item_id": "01-021", "text": "羽林右", "type": "institution", "confidence": 0.85},
    {"slot": 6, "item_id": "01-021", "text": "留守左", "type": "institution", "confidence": 0.85},
    {"slot": 7, "item_id": "01-021", "text": "龙虎", "type": "institution", "confidence": 0.85},
    {"slot": 8, "item_id": "01-021", "text": "应天", "type": "institution", "confidence": 0.85},
    {"slot": 9, "item_id": "01-021", "text": "禄俸", "type": "system", "confidence": 0.88},
    {"slot": 10, "item_id": "01-021", "text": "边镇粮饷", "type": "system", "confidence": 0.88},
    {"slot": 11, "item_id": "01-021", "text": "仓场", "type": "institution", "confidence": 0.88},
    {"slot": 12, "item_id": "01-021", "text": "盐课", "type": "system", "confidence": 0.88},
    {"slot": 13, "item_id": "01-021", "text": "钞关", "type": "institution", "confidence": 0.88},

    # ============ 条22 户部四科 ============
    {"slot": 1, "item_id": "01-022", "text": "民科", "type": "institution", "confidence": 0.92},
    {"slot": 2, "item_id": "01-022", "text": "度支", "type": "institution", "confidence": 0.92},
    {"slot": 3, "item_id": "01-022", "text": "金科", "type": "institution", "confidence": 0.88},
    {"slot": 4, "item_id": "01-022", "text": "仓科", "type": "institution", "confidence": 0.88},
    {"slot": 5, "item_id": "01-022", "text": "图志", "type": "doc", "confidence": 0.88},
    {"slot": 6, "item_id": "01-022", "text": "夏税", "type": "system", "confidence": 0.9},
    {"slot": 7, "item_id": "01-022", "text": "秋粮", "type": "system", "confidence": 0.9},
    {"slot": 8, "item_id": "01-022", "text": "户口", "type": "system", "confidence": 0.88},

    # ============ 条23 户部沿革 ============
    {"slot": 1, "item_id": "01-023", "text": "户部", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-023", "text": "五科", "type": "institution", "confidence": 0.9},
    {"slot": 3, "item_id": "01-023", "text": "总科", "type": "institution", "confidence": 0.9},
    {"slot": 4, "item_id": "01-023", "text": "洪武元年", "type": "era", "confidence": 0.95},
    {"slot": 5, "item_id": "01-023", "text": "六年，设尚书二人", "type": "era", "confidence": 0.92},
    {"slot": 6, "item_id": "01-023", "text": "十三年，升部秩", "type": "era", "confidence": 0.92},
    {"slot": 7, "item_id": "01-023", "text": "八年，中书省奏户、刑、工三部事繁", "type": "era", "confidence": 0.9},
    {"slot": 8, "item_id": "01-023", "text": "行用库", "type": "institution", "confidence": 0.9},

    # ============ 条24 总督仓场 ============
    {"slot": 1, "item_id": "01-024", "text": "总督仓场", "type": "official", "confidence": 0.95},
    {"slot": 2, "item_id": "01-024", "text": "通州", "type": "place", "confidence": 0.9},
    {"slot": 3, "item_id": "01-024", "text": "军储仓", "type": "institution", "confidence": 0.9},
    {"slot": 4, "item_id": "01-024", "text": "北京", "type": "place", "confidence": 0.92},
    {"slot": 5, "item_id": "01-024", "text": "京仓", "type": "institution", "confidence": 0.9},
    {"slot": 6, "item_id": "01-024", "text": "宣德五年", "type": "era", "confidence": 0.92},
    {"slot": 7, "item_id": "01-024", "text": "天启五年", "type": "era", "confidence": 0.88},

    # ============ 条25 礼部编制 ============
    {"slot": 1, "item_id": "01-025", "text": "礼部。", "type": "institution", "confidence": 0.98},
    {"slot": 2, "item_id": "01-025", "text": "尚书", "type": "official", "confidence": 0.98},
    {"slot": 3, "item_id": "01-025", "text": "左、右侍郎", "type": "official", "confidence": 0.98},
    {"slot": 4, "item_id": "01-025", "text": "司务厅", "type": "institution", "confidence": 0.95},
    {"slot": 5, "item_id": "01-025", "text": "司务", "type": "official", "confidence": 0.95},
    {"slot": 6, "item_id": "01-025", "text": "仪制、祠祭、主客、精膳四清吏司", "type": "institution", "confidence": 0.95},
    {"slot": 7, "item_id": "01-025", "text": "郎中", "type": "official", "confidence": 0.98},
    {"slot": 8, "item_id": "01-025", "text": "员外郎", "type": "official", "confidence": 0.98},
    {"slot": 9, "item_id": "01-025", "text": "主事", "type": "official", "confidence": 0.98},
    {"slot": 10, "item_id": "01-025", "text": "铸印局", "type": "institution", "confidence": 0.95},
    {"slot": 11, "item_id": "01-025", "text": "大使", "type": "official", "confidence": 0.95},
    {"slot": 12, "item_id": "01-025", "text": "副使", "type": "official", "confidence": 0.95},
    {"slot": 13, "item_id": "01-025", "text": "会同馆", "type": "institution", "confidence": 0.92},
    {"slot": 14, "item_id": "01-025", "text": "正二品", "type": "quantity", "confidence": 0.98},
    {"slot": 15, "item_id": "01-025", "text": "正统六年", "type": "era", "confidence": 0.92},
    {"slot": 16, "item_id": "01-025", "text": "弘治五年", "type": "era", "confidence": 0.92},
    {"slot": 17, "item_id": "01-025", "text": "万历九年", "type": "era", "confidence": 0.9},

    # ============ 条26 礼部尚书职掌 ============
    {"slot": 1, "item_id": "01-026", "text": "尚书", "type": "official", "confidence": 0.98},
    {"slot": 2, "item_id": "01-026", "text": "侍郎", "type": "official", "confidence": 0.98},
    {"slot": 3, "item_id": "01-026", "text": "礼仪", "type": "system", "confidence": 0.9},
    {"slot": 4, "item_id": "01-026", "text": "祭祀", "type": "system", "confidence": 0.92},
    {"slot": 5, "item_id": "01-026", "text": "宴飨", "type": "system", "confidence": 0.9},
    {"slot": 6, "item_id": "01-026", "text": "贡举", "type": "system", "confidence": 0.92},

    # ============ 条27 仪制司职掌 ============
    {"slot": 1, "item_id": "01-027", "text": "仪制", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-027", "text": "宗封", "type": "system", "confidence": 0.9},
    {"slot": 3, "item_id": "01-027", "text": "学校", "type": "system", "confidence": 0.9},
    {"slot": 4, "item_id": "01-027", "text": "皇太子", "type": "official", "confidence": 0.9},
    {"slot": 5, "item_id": "01-027", "text": "大婚", "type": "system", "confidence": 0.88},
    {"slot": 6, "item_id": "01-027", "text": "朝贺", "type": "system", "confidence": 0.88},
    {"slot": 7, "item_id": "01-027", "text": "大射", "type": "system", "confidence": 0.85},
    {"slot": 8, "item_id": "01-027", "text": "宴射", "type": "system", "confidence": 0.85},

    # ============ 条28 祠祭司职掌 ============
    {"slot": 1, "item_id": "01-028", "text": "祠祭", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-028", "text": "天神", "type": "system", "confidence": 0.88},
    {"slot": 3, "item_id": "01-028", "text": "地祇", "type": "system", "confidence": 0.88},
    {"slot": 4, "item_id": "01-028", "text": "人鬼", "type": "system", "confidence": 0.88},
    {"slot": 5, "item_id": "01-028", "text": "大祀", "type": "system", "confidence": 0.9},
    {"slot": 6, "item_id": "01-028", "text": "中祀", "type": "system", "confidence": 0.9},
    {"slot": 7, "item_id": "01-028", "text": "小祀", "type": "system", "confidence": 0.9},
    {"slot": 8, "item_id": "01-028", "text": "坛壝", "type": "place", "confidence": 0.88},
    {"slot": 9, "item_id": "01-028", "text": "陵寝", "type": "place", "confidence": 0.9},

    # ============ 条29 主客司职掌 ============
    {"slot": 1, "item_id": "01-029", "text": "主客", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-029", "text": "朝贡", "type": "system", "confidence": 0.92},
    {"slot": 3, "item_id": "01-029", "text": "贡道", "type": "system", "confidence": 0.88},
    {"slot": 4, "item_id": "01-029", "text": "贡使", "type": "official", "confidence": 0.88},
    {"slot": 5, "item_id": "01-029", "text": "贡物", "type": "doc", "confidence": 0.88},
    {"slot": 6, "item_id": "01-029", "text": "赏赉", "type": "system", "confidence": 0.88},
    {"slot": 7, "item_id": "01-029", "text": "土官", "type": "system", "confidence": 0.88},

    # ============ 条30 精膳司职掌 ============
    {"slot": 1, "item_id": "01-030", "text": "精膳", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-030", "text": "牲豆", "type": "system", "confidence": 0.85},
    {"slot": 3, "item_id": "01-030", "text": "酒膳", "type": "system", "confidence": 0.85},
    {"slot": 4, "item_id": "01-030", "text": "下程", "type": "system", "confidence": 0.85},

    # ============ 条31 礼部沿革 ============
    {"slot": 1, "item_id": "01-031", "text": "礼部", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-031", "text": "总部", "type": "institution", "confidence": 0.9},
    {"slot": 3, "item_id": "01-031", "text": "祠部", "type": "institution", "confidence": 0.9},
    {"slot": 4, "item_id": "01-031", "text": "膳部", "type": "institution", "confidence": 0.9},
    {"slot": 5, "item_id": "01-031", "text": "主客部", "type": "institution", "confidence": 0.9},
    {"slot": 6, "item_id": "01-031", "text": "洪武元年", "type": "era", "confidence": 0.95},
    {"slot": 7, "item_id": "01-031", "text": "六年，设尚书二人", "type": "era", "confidence": 0.92},
    {"slot": 8, "item_id": "01-031", "text": "十三年，升部秩", "type": "era", "confidence": 0.92},

    # ============ 条32 礼部按语 ============
    {"slot": 1, "item_id": "01-032", "text": "周宗伯", "type": "official", "confidence": 0.85},
    {"slot": 2, "item_id": "01-032", "text": "司徒", "type": "official", "confidence": 0.88},
    {"slot": 3, "item_id": "01-032", "text": "邦礼", "type": "system", "confidence": 0.85},
    {"slot": 4, "item_id": "01-032", "text": "邦教", "type": "system", "confidence": 0.85},
    {"slot": 5, "item_id": "01-032", "text": "宗藩", "type": "system", "confidence": 0.85},

    # ============ 条33 兵部编制 ============
    {"slot": 1, "item_id": "01-033", "text": "兵部。", "type": "institution", "confidence": 0.98},
    {"slot": 2, "item_id": "01-033", "text": "尚书", "type": "official", "confidence": 0.98},
    {"slot": 3, "item_id": "01-033", "text": "左、右侍郎", "type": "official", "confidence": 0.98},
    {"slot": 4, "item_id": "01-033", "text": "司务厅", "type": "institution", "confidence": 0.95},
    {"slot": 5, "item_id": "01-033", "text": "司务", "type": "official", "confidence": 0.95},
    {"slot": 6, "item_id": "01-033", "text": "武选、职方、车驾、武库四清吏司", "type": "institution", "confidence": 0.95},
    {"slot": 7, "item_id": "01-033", "text": "郎中", "type": "official", "confidence": 0.98},
    {"slot": 8, "item_id": "01-033", "text": "员外郎", "type": "official", "confidence": 0.98},
    {"slot": 9, "item_id": "01-033", "text": "主事", "type": "official", "confidence": 0.98},
    {"slot": 10, "item_id": "01-033", "text": "会同馆", "type": "institution", "confidence": 0.92},
    {"slot": 11, "item_id": "01-033", "text": "大通关", "type": "institution", "confidence": 0.9},
    {"slot": 12, "item_id": "01-033", "text": "大使", "type": "official", "confidence": 0.95},
    {"slot": 13, "item_id": "01-033", "text": "副使", "type": "official", "confidence": 0.95},
    {"slot": 14, "item_id": "01-033", "text": "正二品", "type": "quantity", "confidence": 0.98},
    {"slot": 15, "item_id": "01-033", "text": "正统十年", "type": "era", "confidence": 0.92},
    {"slot": 16, "item_id": "01-033", "text": "成化三年", "type": "era", "confidence": 0.9},
    {"slot": 17, "item_id": "01-033", "text": "弘治九年", "type": "era", "confidence": 0.9},
    {"slot": 18, "item_id": "01-033", "text": "嘉靖十二年", "type": "era", "confidence": 0.9},
    {"slot": 19, "item_id": "01-033", "text": "万历十一年", "type": "era", "confidence": 0.9},

    # ============ 条34 兵部尚书职掌 ============
    {"slot": 1, "item_id": "01-034", "text": "尚书", "type": "official", "confidence": 0.98},
    {"slot": 2, "item_id": "01-034", "text": "武卫官军", "type": "system", "confidence": 0.9},
    {"slot": 3, "item_id": "01-034", "text": "选授", "type": "system", "confidence": 0.9},
    {"slot": 4, "item_id": "01-034", "text": "简练", "type": "system", "confidence": 0.9},

    # ============ 条35 武选司职掌 ============
    {"slot": 1, "item_id": "01-035", "text": "武选", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-035", "text": "卫所土官", "type": "system", "confidence": 0.9},
    {"slot": 3, "item_id": "01-035", "text": "升调", "type": "system", "confidence": 0.9},
    {"slot": 4, "item_id": "01-035", "text": "袭替", "type": "system", "confidence": 0.92},
    {"slot": 5, "item_id": "01-035", "text": "功赏", "type": "system", "confidence": 0.9},
    {"slot": 6, "item_id": "01-035", "text": "左、右柱国", "type": "official", "confidence": 0.95},
    {"slot": 7, "item_id": "01-035", "text": "柱国", "type": "official", "confidence": 0.95},
    {"slot": 8, "item_id": "01-035", "text": "上护军", "type": "official", "confidence": 0.95},
    {"slot": 9, "item_id": "01-035", "text": "护军", "type": "official", "confidence": 0.95},
    {"slot": 4, "item_id": "01-035", "text": "散阶三十", "type": "system", "confidence": 0.9},

    # ============ 条36 职方司职掌 ============
    {"slot": 1, "item_id": "01-036", "text": "职方", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-036", "text": "舆图", "type": "doc", "confidence": 0.92},
    {"slot": 3, "item_id": "01-036", "text": "军制", "type": "system", "confidence": 0.9},
    {"slot": 4, "item_id": "01-036", "text": "城隍", "type": "system", "confidence": 0.88},
    {"slot": 5, "item_id": "01-036", "text": "镇戍", "type": "system", "confidence": 0.9},
    {"slot": 6, "item_id": "01-036", "text": "征讨", "type": "system", "confidence": 0.9},
    {"slot": 7, "item_id": "01-036", "text": "图本", "type": "doc", "confidence": 0.88},

    # ============ 条37 车驾司职掌 ============
    {"slot": 1, "item_id": "01-037", "text": "车驾", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-037", "text": "卤簿", "type": "system", "confidence": 0.92},
    {"slot": 3, "item_id": "01-037", "text": "仪仗", "type": "system", "confidence": 0.92},
    {"slot": 4, "item_id": "01-037", "text": "禁卫", "type": "system", "confidence": 0.9},
    {"slot": 5, "item_id": "01-037", "text": "驿传", "type": "system", "confidence": 0.9},
    {"slot": 6, "item_id": "01-037", "text": "厩牧", "type": "system", "confidence": 0.88},
    {"slot": 7, "item_id": "01-037", "text": "大驾", "type": "system", "confidence": 0.88},
    {"slot": 8, "item_id": "01-037", "text": "丹陛驾", "type": "system", "confidence": 0.88},
    {"slot": 9, "item_id": "01-037", "text": "武陈驾", "type": "system", "confidence": 0.85},
    {"slot": 10, "item_id": "01-037", "text": "世宗", "type": "person", "confidence": 0.88},
    {"slot": 11, "item_id": "01-037", "text": "南巡", "type": "system", "confidence": 0.85},

    # ============ 条38 武库司职掌 ============
    {"slot": 1, "item_id": "01-038", "text": "武库", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-038", "text": "戎器", "type": "system", "confidence": 0.9},
    {"slot": 3, "item_id": "01-038", "text": "符勘", "type": "system", "confidence": 0.88},
    {"slot": 4, "item_id": "01-038", "text": "尺籍", "type": "doc", "confidence": 0.88},
    {"slot": 5, "item_id": "01-038", "text": "武学", "type": "institution", "confidence": 0.9},
    {"slot": 6, "item_id": "01-038", "text": "勘合", "type": "doc", "confidence": 0.9},

    # ============ 条39 兵部沿革 ============
    {"slot": 1, "item_id": "01-039", "text": "兵部", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-039", "text": "总部", "type": "institution", "confidence": 0.9},
    {"slot": 3, "item_id": "01-039", "text": "驾部", "type": "institution", "confidence": 0.9},
    {"slot": 4, "item_id": "01-039", "text": "职方", "type": "institution", "confidence": 0.9},
    {"slot": 5, "item_id": "01-039", "text": "洪武元年", "type": "era", "confidence": 0.95},
    {"slot": 6, "item_id": "01-039", "text": "六年，增尚书一人", "type": "era", "confidence": 0.92},
    {"slot": 7, "item_id": "01-039", "text": "十三年，升部秩", "type": "era", "confidence": 0.92},

    # ============ 条40 协理京营戎政 ============
    {"slot": 1, "item_id": "01-040", "text": "协理京营戎政", "type": "official", "confidence": 0.95},
    {"slot": 2, "item_id": "01-040", "text": "京营", "type": "institution", "confidence": 0.92},
    {"slot": 3, "item_id": "01-040", "text": "三大营", "type": "institution", "confidence": 0.9},
    {"slot": 4, "item_id": "01-040", "text": "团营", "type": "institution", "confidence": 0.9},
    {"slot": 5, "item_id": "01-040", "text": "于谦", "type": "person", "confidence": 0.92},
    {"slot": 6, "item_id": "01-040", "text": "永乐初", "type": "era", "confidence": 0.92},
    {"slot": 7, "item_id": "01-040", "text": "景泰元年", "type": "era", "confidence": 0.95},
    {"slot": 8, "item_id": "01-040", "text": "嘉靖二十年", "type": "era", "confidence": 0.88},
    {"slot": 9, "item_id": "01-040", "text": "崇祯二年复增一人", "type": "era", "confidence": 0.88},

    # ============ 条41 刑部编制 ============
    {"slot": 1, "item_id": "01-041", "text": "刑部。", "type": "institution", "confidence": 0.98},
    {"slot": 2, "item_id": "01-041", "text": "尚书", "type": "official", "confidence": 0.98},
    {"slot": 3, "item_id": "01-041", "text": "左、右侍郎", "type": "official", "confidence": 0.98},
    {"slot": 4, "item_id": "01-041", "text": "司务厅", "type": "institution", "confidence": 0.95},
    {"slot": 5, "item_id": "01-041", "text": "司务", "type": "official", "confidence": 0.95},
    {"slot": 6, "item_id": "01-041", "text": "十三清吏司", "type": "institution", "confidence": 0.95},
    {"slot": 7, "item_id": "01-041", "text": "郎中", "type": "official", "confidence": 0.98},
    {"slot": 8, "item_id": "01-041", "text": "员外郎", "type": "official", "confidence": 0.98},
    {"slot": 9, "item_id": "01-041", "text": "主事", "type": "official", "confidence": 0.98},
    {"slot": 10, "item_id": "01-041", "text": "照磨所", "type": "institution", "confidence": 0.95},
    {"slot": 11, "item_id": "01-041", "text": "照磨", "type": "official", "confidence": 0.95},
    {"slot": 12, "item_id": "01-041", "text": "检校", "type": "official", "confidence": 0.95},
    {"slot": 13, "item_id": "01-041", "text": "司狱司", "type": "institution", "confidence": 0.95},
    {"slot": 14, "item_id": "01-041", "text": "司狱", "type": "official", "confidence": 0.95},
    {"slot": 15, "item_id": "01-041", "text": "正二品", "type": "quantity", "confidence": 0.98},
    {"slot": 16, "item_id": "01-041", "text": "正统六年", "type": "era", "confidence": 0.92},
    {"slot": 17, "item_id": "01-041", "text": "成化元年", "type": "era", "confidence": 0.9},

    # ============ 条42 刑部尚书职掌 ============
    {"slot": 1, "item_id": "01-042", "text": "尚书", "type": "official", "confidence": 0.98},
    {"slot": 2, "item_id": "01-042", "text": "刑名", "type": "system", "confidence": 0.92},
    {"slot": 3, "item_id": "01-042", "text": "徒隶", "type": "system", "confidence": 0.88},
    {"slot": 4, "item_id": "01-042", "text": "勾覆", "type": "system", "confidence": 0.88},
    {"slot": 5, "item_id": "01-042", "text": "关禁", "type": "system", "confidence": 0.88},

    # ============ 条43 刑部十三司职掌 ============
    {"slot": 1, "item_id": "01-043", "text": "十三司", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-043", "text": "崇府", "type": "institution", "confidence": 0.85},
    {"slot": 3, "item_id": "01-043", "text": "中军都督府", "type": "institution", "confidence": 0.9},
    {"slot": 4, "item_id": "01-043", "text": "刑科", "type": "institution", "confidence": 0.9},
    {"slot": 5, "item_id": "01-043", "text": "御用", "type": "institution", "confidence": 0.88},
    {"slot": 6, "item_id": "01-043", "text": "司设", "type": "institution", "confidence": 0.88},
    {"slot": 7, "item_id": "01-043", "text": "京府", "type": "institution", "confidence": 0.88},

    # ============ 条44 刑部照磨司狱职掌 ============
    {"slot": 1, "item_id": "01-044", "text": "照磨", "type": "official", "confidence": 0.95},
    {"slot": 2, "item_id": "01-044", "text": "检校", "type": "official", "confidence": 0.95},
    {"slot": 3, "item_id": "01-044", "text": "赃赎", "type": "system", "confidence": 0.88},
    {"slot": 4, "item_id": "01-044", "text": "司狱", "type": "official", "confidence": 0.95},
    {"slot": 5, "item_id": "01-044", "text": "诏狱", "type": "system", "confidence": 0.9},
    {"slot": 6, "item_id": "01-044", "text": "律例", "type": "doc", "confidence": 0.9},

    # ============ 条45 刑部沿革 ============
    {"slot": 1, "item_id": "01-045", "text": "刑部", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-045", "text": "总部", "type": "institution", "confidence": 0.9},
    {"slot": 3, "item_id": "01-045", "text": "比部", "type": "institution", "confidence": 0.9},
    {"slot": 4, "item_id": "01-045", "text": "都官部", "type": "institution", "confidence": 0.9},
    {"slot": 5, "item_id": "01-045", "text": "司门部", "type": "institution", "confidence": 0.9},
    {"slot": 6, "item_id": "01-045", "text": "洪武元年", "type": "era", "confidence": 0.95},
    {"slot": 7, "item_id": "01-045", "text": "六年，增尚书、侍郎各一人", "type": "era", "confidence": 0.92},
    {"slot": 8, "item_id": "01-045", "text": "二十三年，分四部为河南、北平", "type": "era", "confidence": 0.9},

    # ============ 条46 工部编制 ============
    {"slot": 1, "item_id": "01-046", "text": "工部。", "type": "institution", "confidence": 0.98},
    {"slot": 2, "item_id": "01-046", "text": "尚书", "type": "official", "confidence": 0.98},
    {"slot": 3, "item_id": "01-046", "text": "左、右侍郎", "type": "official", "confidence": 0.98},
    {"slot": 4, "item_id": "01-046", "text": "司务厅", "type": "institution", "confidence": 0.95},
    {"slot": 5, "item_id": "01-046", "text": "司务", "type": "official", "confidence": 0.95},
    {"slot": 6, "item_id": "01-046", "text": "营缮、虞衡、都水、屯田四清吏司", "type": "institution", "confidence": 0.95},
    {"slot": 7, "item_id": "01-046", "text": "郎中", "type": "official", "confidence": 0.98},
    {"slot": 8, "item_id": "01-046", "text": "员外郎", "type": "official", "confidence": 0.98},
    {"slot": 9, "item_id": "01-046", "text": "主事", "type": "official", "confidence": 0.98},
    {"slot": 10, "item_id": "01-046", "text": "营缮所", "type": "institution", "confidence": 0.95},
    {"slot": 11, "item_id": "01-046", "text": "所正", "type": "official", "confidence": 0.92},
    {"slot": 12, "item_id": "01-046", "text": "所副", "type": "official", "confidence": 0.92},
    {"slot": 13, "item_id": "01-046", "text": "所丞", "type": "official", "confidence": 0.92},
    {"slot": 14, "item_id": "01-046", "text": "文思院", "type": "institution", "confidence": 0.95},
    {"slot": 15, "item_id": "01-046", "text": "皮作局", "type": "institution", "confidence": 0.95},
    {"slot": 16, "item_id": "01-046", "text": "鞍辔局", "type": "institution", "confidence": 0.95},
    {"slot": 17, "item_id": "01-046", "text": "宝源局", "type": "institution", "confidence": 0.95},
    {"slot": 18, "item_id": "01-046", "text": "大使", "type": "official", "confidence": 0.95},
    {"slot": 19, "item_id": "01-046", "text": "副使", "type": "official", "confidence": 0.95},
    {"slot": 20, "item_id": "01-046", "text": "正二品", "type": "quantity", "confidence": 0.98},
    {"slot": 21, "item_id": "01-046", "text": "隆庆元年", "type": "era", "confidence": 0.9},

    # ============ 条47 工部尚书职掌 ============
    {"slot": 1, "item_id": "01-047", "text": "尚书", "type": "official", "confidence": 0.98},
    {"slot": 2, "item_id": "01-047", "text": "山泽", "type": "system", "confidence": 0.88},
    {"slot": 3, "item_id": "01-047", "text": "百官", "type": "system", "confidence": 0.88},

    # ============ 条48 营缮司职掌 ============
    {"slot": 1, "item_id": "01-048", "text": "营缮", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-048", "text": "兴作", "type": "system", "confidence": 0.88},
    {"slot": 3, "item_id": "01-048", "text": "宫殿", "type": "place", "confidence": 0.9},
    {"slot": 4, "item_id": "01-048", "text": "陵寝", "type": "place", "confidence": 0.9},
    {"slot": 5, "item_id": "01-048", "text": "城郭", "type": "place", "confidence": 0.88},
    {"slot": 6, "item_id": "01-048", "text": "王府邸第", "type": "place", "confidence": 0.88},
    {"slot": 7, "item_id": "01-048", "text": "鸠工会材", "type": "system", "confidence": 0.85},

    # ============ 条49 虞衡司职掌 ============
    {"slot": 1, "item_id": "01-049", "text": "虞衡", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-049", "text": "采捕", "type": "system", "confidence": 0.88},
    {"slot": 3, "item_id": "01-049", "text": "陶冶", "type": "system", "confidence": 0.88},
    {"slot": 4, "item_id": "01-049", "text": "水课", "type": "system", "confidence": 0.85},
    {"slot": 5, "item_id": "01-049", "text": "陆课", "type": "system", "confidence": 0.85},

    # ============ 条50 都水司职掌 ============
    {"slot": 1, "item_id": "01-050", "text": "都水", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-050", "text": "川泽", "type": "place", "confidence": 0.88},
    {"slot": 3, "item_id": "01-050", "text": "陂池", "type": "place", "confidence": 0.88},
    {"slot": 4, "item_id": "01-050", "text": "桥道", "type": "system", "confidence": 0.88},
    {"slot": 5, "item_id": "01-050", "text": "转漕", "type": "system", "confidence": 0.9},
    {"slot": 6, "item_id": "01-050", "text": "灌田", "type": "system", "confidence": 0.88},
    {"slot": 7, "item_id": "01-050", "text": "闸坝", "type": "system", "confidence": 0.88},
    {"slot": 8, "item_id": "01-050", "text": "堰圩", "type": "system", "confidence": 0.85},
    {"slot": 9, "item_id": "01-050", "text": "堤防", "type": "system", "confidence": 0.88},

    # ============ 条51 屯田司职掌 ============
    {"slot": 1, "item_id": "01-051", "text": "屯田", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-051", "text": "屯种", "type": "system", "confidence": 0.9},
    {"slot": 3, "item_id": "01-051", "text": "抽分", "type": "system", "confidence": 0.88},
    {"slot": 4, "item_id": "01-051", "text": "薪炭", "type": "system", "confidence": 0.88},
    {"slot": 5, "item_id": "01-051", "text": "夫役", "type": "system", "confidence": 0.88},
    {"slot": 6, "item_id": "01-051", "text": "坟茔", "type": "place", "confidence": 0.85},
    {"slot": 7, "item_id": "01-051", "text": "军储", "type": "system", "confidence": 0.88},

    # ============ 条52 工部沿革 ============
    {"slot": 1, "item_id": "01-052", "text": "工部", "type": "institution", "confidence": 0.95},
    {"slot": 2, "item_id": "01-052", "text": "将作司", "type": "institution", "confidence": 0.92},
    {"slot": 3, "item_id": "01-052", "text": "提举司", "type": "institution", "confidence": 0.9},
    {"slot": 4, "item_id": "01-052", "text": "吴元年", "type": "era", "confidence": 0.95},
    {"slot": 5, "item_id": "01-052", "text": "洪武初", "type": "era", "confidence": 0.92},
    {"slot": 6, "item_id": "01-052", "text": "营造提举司", "type": "institution", "confidence": 0.88},

    # ============ 条53 提督易州山厂 ============
    {"slot": 1, "item_id": "01-053", "text": "提督易州山厂", "type": "official", "confidence": 0.92},
    {"slot": 2, "item_id": "01-053", "text": "易州", "type": "place", "confidence": 0.9},
    {"slot": 3, "item_id": "01-053", "text": "芦洲", "type": "place", "confidence": 0.88},
    {"slot": 4, "item_id": "01-053", "text": "龙江", "type": "place", "confidence": 0.88},
    {"slot": 5, "item_id": "01-053", "text": "瓦屑", "type": "place", "confidence": 0.85},
    {"slot": 6, "item_id": "01-053", "text": "白羊口", "type": "place", "confidence": 0.85},
    {"slot": 7, "item_id": "01-053", "text": "黄花镇", "type": "place", "confidence": 0.85},
    {"slot": 8, "item_id": "01-053", "text": "红螺山", "type": "place", "confidence": 0.85},
    {"slot": 9, "item_id": "01-053", "text": "宣德四年", "type": "era", "confidence": 0.92},
    {"slot": 10, "item_id": "01-053", "text": "永乐间", "type": "era", "confidence": 0.9},
]
