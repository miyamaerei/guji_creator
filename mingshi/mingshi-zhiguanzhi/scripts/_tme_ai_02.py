# -*- coding: utf-8 -*-
"""
【卷02】TME 时间沿革层源数据 —— **本卷主战场**（差遣条目 46 条的沿革全靠 TME 承载）
era.year 存年号内年数；order 由打包器按 REIGN_ORDER 派生。
"""

TMES = [
    # ============ 都察院 ============
    {"slot": 1, "item_id": "02-005", "era": {"text": "吴元年", "dynasty": "明", "reign": "吴", "year": 1},
     "target": {"text": "都察院", "ent_ids": []}, "action": "置",
     "content": "初，吴元年置御史台", "category": "初置", "related_evo": [], "confidence": 0.95},
    {"slot": 2, "item_id": "02-005", "era": {"text": "洪武九年", "dynasty": "明", "reign": "洪武", "year": 9},
     "target": {"text": "都察院", "ent_ids": []}, "action": "汰",
     "content": "洪武九年汰侍御史及治书、殿中侍御史", "category": "裁并", "related_evo": [], "confidence": 0.92},
    {"slot": 3, "item_id": "02-005", "era": {"text": "洪武十年七月", "dynasty": "明", "reign": "洪武", "year": 10},
     "target": {"text": "都察院", "ent_ids": []}, "action": "诏遣",
     "content": "十年七月，诏遣监察御史巡按州县", "category": "职掌变更", "related_evo": [], "confidence": 0.92},
    {"slot": 4, "item_id": "02-005", "era": {"text": "洪武十三年", "dynasty": "明", "reign": "洪武", "year": 13},
     "target": {"text": "都察院", "ent_ids": []}, "action": "罢",
     "content": "十三年，专设左，右中丞，寻罢御史台", "category": "废置", "related_evo": [], "confidence": 0.95},
    {"slot": 5, "item_id": "02-005", "era": {"text": "洪武十五年", "dynasty": "明", "reign": "洪武", "year": 15},
     "target": {"text": "都察院", "ent_ids": []}, "action": "更置",
     "content": "十五年更置都察院，设监察都御史八人，秩正七品", "category": "改置", "related_evo": [], "confidence": 0.95},
    {"slot": 6, "item_id": "02-005", "era": {"text": "洪武十七年", "dynasty": "明", "reign": "洪武", "year": 17},
     "target": {"text": "都察院", "ent_ids": []}, "action": "升秩",
     "content": "十七年，升都察院秩", "category": "升秩降秩", "related_evo": [], "confidence": 0.85},
    {"slot": 7, "item_id": "02-005", "era": {"text": "宣德十年", "dynasty": "明", "reign": "宣德", "year": 10},
     "target": {"text": "都察院", "ent_ids": []}, "action": "定",
     "content": "宣德十年，始定为十三道", "category": "改置", "related_evo": [], "confidence": 0.9},

    # ============ 总督漕运 ============
    {"slot": 8, "item_id": "02-006", "era": {"text": "洪武元年", "dynasty": "明", "reign": "洪武", "year": 1},
     "target": {"text": "总督漕运", "ent_ids": []}, "action": "置",
     "content": "太祖时，尝置京畿都漕运司，设漕运使", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 9, "item_id": "02-006", "era": {"text": "洪武十四年", "dynasty": "明", "reign": "洪武", "year": 14},
     "target": {"text": "总督漕运", "ent_ids": []}, "action": "罢",
     "content": "十四年罢", "category": "废置", "related_evo": [], "confidence": 0.88},
    {"slot": 10, "item_id": "02-006", "era": {"text": "永乐间", "dynasty": "明", "reign": "永乐", "year": "未明"},
     "target": {"text": "总督漕运", "ent_ids": []}, "action": "设",
     "content": "永乐间，设漕运总兵官，以平江伯陈瑄治漕", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 11, "item_id": "02-006", "era": {"text": "宣德中", "dynasty": "明", "reign": "宣德", "year": "未明"},
     "target": {"text": "总督漕运", "ent_ids": []}, "action": "遣",
     "content": "宣德中，又遣侍郎、都御史、少卿等官督运", "category": "职掌变更", "related_evo": [], "confidence": 0.88},
    {"slot": 12, "item_id": "02-006", "era": {"text": "景泰二年", "dynasty": "明", "reign": "景泰", "year": 2},
     "target": {"text": "总督漕运", "ent_ids": []}, "action": "命",
     "content": "至景泰二年，始命副都御史王竑总督，因兼巡抚淮、扬、庐、凤四府，治淮安",
     "category": "初置", "related_evo": [], "confidence": 0.95},
    {"slot": 13, "item_id": "02-006", "era": {"text": "成化八年", "dynasty": "明", "reign": "成化", "year": 8},
     "target": {"text": "总督漕运", "ent_ids": []}, "action": "分设",
     "content": "成化八年，分设巡抚、总漕各一员。九年复旧", "category": "裁并", "related_evo": [], "confidence": 0.9},
    {"slot": 14, "item_id": "02-006", "era": {"text": "正德十三年", "dynasty": "明", "reign": "正德", "year": 13},
     "target": {"text": "总督漕运", "ent_ids": []}, "action": "分设",
     "content": "正德十三年又分设。十六年又复旧", "category": "裁并", "related_evo": [], "confidence": 0.88},
    {"slot": 15, "item_id": "02-006", "era": {"text": "嘉靖三十六年", "dynasty": "明", "reign": "嘉靖", "year": 36},
     "target": {"text": "总督漕运", "ent_ids": []}, "action": "添设",
     "content": "嘉靖三十六年，以倭警，添设提督军务巡抚凤阳都御史", "category": "增员", "related_evo": [], "confidence": 0.9},
    {"slot": 16, "item_id": "02-006", "era": {"text": "嘉靖四十年", "dynasty": "明", "reign": "嘉靖", "year": 40},
     "target": {"text": "总督漕运", "ent_ids": []}, "action": "归并改称",
     "content": "四十年归并，改总督漕运兼提督军务", "category": "改称", "related_evo": [], "confidence": 0.92},
    {"slot": 17, "item_id": "02-006", "era": {"text": "万历七年", "dynasty": "明", "reign": "万历", "year": 7},
     "target": {"text": "总督漕运", "ent_ids": []}, "action": "加",
     "content": "万历七年加兼管河道", "category": "职掌变更", "related_evo": [], "confidence": 0.9},

    # ============ 总督蓟辽 ============
    {"slot": 18, "item_id": "02-007", "era": {"text": "嘉靖二十九年", "dynasty": "明", "reign": "嘉靖", "year": 29},
     "target": {"text": "总督蓟辽", "ent_ids": []}, "action": "置",
     "content": "嘉靖二十九年置，开府密云，辖顺天、保定、辽东三巡抚",
     "category": "初置", "related_evo": [], "confidence": 0.95},
    {"slot": 19, "item_id": "02-007", "era": {"text": "万历九年", "dynasty": "明", "reign": "万历", "year": 9},
     "target": {"text": "总督蓟辽", "ent_ids": []}, "action": "加兼",
     "content": "万历九年加兼巡抚顺天等处。十一年复旧", "category": "职掌变更", "related_evo": [], "confidence": 0.88},
    {"slot": 20, "item_id": "02-007", "era": {"text": "天启元年", "dynasty": "明", "reign": "天启", "year": 1},
     "target": {"text": "总督蓟辽", "ent_ids": []}, "action": "置辽东经略",
     "content": "天启元年，置辽东经略", "category": "增员", "related_evo": [], "confidence": 0.9},
    {"slot": 21, "item_id": "02-007", "era": {"text": "崇祯四年", "dynasty": "明", "reign": "崇祯", "year": 4},
     "target": {"text": "总督蓟辽", "ent_ids": []}, "action": "并入",
     "content": "崇祯四年并入总督", "category": "裁并", "related_evo": [], "confidence": 0.9},

    # ============ 总督宣大 ============
    {"slot": 22, "item_id": "02-008", "era": {"text": "正统元年", "dynasty": "明", "reign": "正统", "year": 1},
     "target": {"text": "总督宣大", "ent_ids": []}, "action": "遣",
     "content": "正统元年，始遣佥都御史巡抚宣大", "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 23, "item_id": "02-008", "era": {"text": "景泰二年", "dynasty": "明", "reign": "景泰", "year": 2},
     "target": {"text": "总督宣大", "ent_ids": []}, "action": "设",
     "content": "景泰二年，宣府、大同各设巡抚，遣尚书石璞总理军务", "category": "改置", "related_evo": [], "confidence": 0.92},
    {"slot": 24, "item_id": "02-008", "era": {"text": "正德八年", "dynasty": "明", "reign": "正德", "year": 8},
     "target": {"text": "总督宣大", "ent_ids": []}, "action": "设总制",
     "content": "正德八年设总制", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 25, "item_id": "02-008", "era": {"text": "嘉靖二十九年", "dynasty": "明", "reign": "嘉靖", "year": 29},
     "target": {"text": "总督宣大", "ent_ids": []}, "action": "定设",
     "content": "二十九年，去偏、保，定设总督宣大、山西等处衔", "category": "改称", "related_evo": [], "confidence": 0.92},
    {"slot": 26, "item_id": "02-008", "era": {"text": "隆庆四年", "dynasty": "明", "reign": "隆庆", "year": 4},
     "target": {"text": "总督宣大", "ent_ids": []}, "action": "移驻",
     "content": "隆庆四年，移驻阳和", "category": "移驻", "related_evo": [], "confidence": 0.9},

    # ============ 总督陕西三边 ============
    {"slot": 27, "item_id": "02-009", "era": {"text": "弘治十年", "dynasty": "明", "reign": "弘治", "year": 10},
     "target": {"text": "总督陕西三边", "ent_ids": []}, "action": "起任",
     "content": "弘治十年，火筛入寇，乃起左都御史王越任之", "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 28, "item_id": "02-009", "era": {"text": "嘉靖四年", "dynasty": "明", "reign": "嘉靖", "year": 4},
     "target": {"text": "总督陕西三边", "ent_ids": []}, "action": "定设",
     "content": "至嘉靖四年，始定设，初称提督军务。七年改为总制。十九年改为总督，开府固原",
     "category": "改置", "related_evo": [], "confidence": 0.92},

    # ============ 总督两广 ============
    {"slot": 29, "item_id": "02-010", "era": {"text": "永乐二年", "dynasty": "明", "reign": "永乐", "year": 2},
     "target": {"text": "总督两广", "ent_ids": []}, "action": "遣",
     "content": "永乐二年，遣给事中雷填巡抚广西", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 30, "item_id": "02-010", "era": {"text": "景泰三年", "dynasty": "明", "reign": "景泰", "year": 3},
     "target": {"text": "总督两广", "ent_ids": []}, "action": "设",
     "content": "景泰三年，苗寇起，以两广宜协济应援，乃设总督", "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 31, "item_id": "02-010", "era": {"text": "成化元年", "dynasty": "明", "reign": "成化", "year": 1},
     "target": {"text": "总督两广", "ent_ids": []}, "action": "兼巡抚事",
     "content": "成化元年，兼巡抚事，驻梧州", "category": "改置", "related_evo": [], "confidence": 0.9},
    {"slot": 32, "item_id": "02-010", "era": {"text": "嘉靖四十五年", "dynasty": "明", "reign": "嘉靖", "year": 45},
     "target": {"text": "总督两广", "ent_ids": []}, "action": "改",
     "content": "嘉靖四十五年，另设广东巡抚，改提督为总督", "category": "改称", "related_evo": [], "confidence": 0.92},
    {"slot": 33, "item_id": "02-010", "era": {"text": "万历三年", "dynasty": "明", "reign": "万历", "year": 3},
     "target": {"text": "总督两广", "ent_ids": []}, "action": "改总督加带管盐法",
     "content": "万历三年，仍改总督，加带管盐法", "category": "改称", "related_evo": [], "confidence": 0.9},

    # ============ 总督川陕 ============
    {"slot": 34, "item_id": "02-011", "era": {"text": "正德五年", "dynasty": "明", "reign": "正德", "year": 5},
     "target": {"text": "总督川陕", "ent_ids": []}, "action": "设",
     "content": "正德五年设，寻罢", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 35, "item_id": "02-011", "era": {"text": "嘉靖二十七年", "dynasty": "明", "reign": "嘉靖", "year": 27},
     "target": {"text": "总督川陕", "ent_ids": []}, "action": "复设",
     "content": "嘉靖二十七年，以苗患，又设总督四川、湖广、贵州、云南等处军务",
     "category": "复设", "related_evo": [], "confidence": 0.92},
    {"slot": 36, "item_id": "02-011", "era": {"text": "天启元年", "dynasty": "明", "reign": "天启", "year": 1},
     "target": {"text": "总督川陕", "ent_ids": []}, "action": "复设",
     "content": "天启元年，以土官奢崇明反，又设五省总督", "category": "复设", "related_evo": [], "confidence": 0.9},

    # ============ 总督浙闽 ============
    {"slot": 37, "item_id": "02-012", "era": {"text": "嘉靖三十三年", "dynasty": "明", "reign": "嘉靖", "year": 33},
     "target": {"text": "总督浙闽", "ent_ids": []}, "action": "置",
     "content": "嘉靖三十三年，以倭犯杭州置", "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 38, "item_id": "02-012", "era": {"text": "嘉靖四十一年", "dynasty": "明", "reign": "嘉靖", "year": 41},
     "target": {"text": "总督浙闽", "ent_ids": []}, "action": "革",
     "content": "四十一年革", "category": "废置", "related_evo": [], "confidence": 0.9},

    # ============ 五省总督 / 崇祯新增 ============
    {"slot": 39, "item_id": "02-013", "era": {"text": "崇祯七年", "dynasty": "明", "reign": "崇祯", "year": 7},
     "target": {"text": "五省总督", "ent_ids": []}, "action": "置",
     "content": "崇祯七年置，或兼七省。十二年后，俱以内阁督师", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 40, "item_id": "02-014", "era": {"text": "崇祯十四年", "dynasty": "明", "reign": "崇祯", "year": 14},
     "target": {"text": "总督凤阳地方", "ent_ids": []}, "action": "设",
     "content": "崇祯十四年设", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 41, "item_id": "02-015", "era": {"text": "崇祯十一年", "dynasty": "明", "reign": "崇祯", "year": 11},
     "target": {"text": "总督保定地方", "ent_ids": []}, "action": "设",
     "content": "崇祯十一年设", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 42, "item_id": "02-016", "era": {"text": "崇祯十六年", "dynasty": "明", "reign": "崇祯", "year": 16},
     "target": {"text": "总督河南湖广", "ent_ids": []}, "action": "设",
     "content": "崇祯十六年设", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 43, "item_id": "02-017", "era": {"text": "崇祯十六年", "dynasty": "明", "reign": "崇祯", "year": 16},
     "target": {"text": "总督九江地方", "ent_ids": []}, "action": "设",
     "content": "崇祯十六年设", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 44, "item_id": "02-018", "era": {"text": "崇祯八年", "dynasty": "明", "reign": "崇祯", "year": 8},
     "target": {"text": "总理南直隶", "ent_ids": []}, "action": "设",
     "content": "崇祯八年设，以卢象升为之，与总督或分或并", "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 总理河漕 ============
    {"slot": 45, "item_id": "02-019", "era": {"text": "永乐九年", "dynasty": "明", "reign": "永乐", "year": 9},
     "target": {"text": "总理河漕", "ent_ids": []}, "action": "遣尚书治河",
     "content": "永乐九年遣尚书治河，自后间遣侍郎、都御史", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 46, "item_id": "02-019", "era": {"text": "正德四年", "dynasty": "明", "reign": "正德", "year": 4},
     "target": {"text": "总理河漕", "ent_ids": []}, "action": "定设",
     "content": "正德四年，定设都御史", "category": "改置", "related_evo": [], "confidence": 0.9},
    {"slot": 47, "item_id": "02-019", "era": {"text": "嘉靖二十年", "dynasty": "明", "reign": "嘉靖", "year": 20},
     "target": {"text": "总理河漕", "ent_ids": []}, "action": "加工部职衔",
     "content": "嘉靖二十年，以都御史加工部职衔，提督河南、山东、直隶河道",
     "category": "职掌变更", "related_evo": [], "confidence": 0.9},
    {"slot": 48, "item_id": "02-019", "era": {"text": "隆庆四年", "dynasty": "明", "reign": "隆庆", "year": 4},
     "target": {"text": "总理河漕", "ent_ids": []}, "action": "加提督军务",
     "content": "隆庆四年，加提督军务", "category": "职掌变更", "related_evo": [], "confidence": 0.9},
    {"slot": 49, "item_id": "02-019", "era": {"text": "万历五年", "dynasty": "明", "reign": "万历", "year": 5},
     "target": {"text": "总理河漕", "ent_ids": []}, "action": "改",
     "content": "万历五年，改总理河漕兼提督军务。八年革", "category": "改称", "related_evo": [], "confidence": 0.92},

    # ============ 总理粮储 ============
    {"slot": 50, "item_id": "02-020", "era": {"text": "宣德五年", "dynasty": "明", "reign": "宣德", "year": 5},
     "target": {"text": "总理粮储", "ent_ids": []}, "action": "命",
     "content": "宣德五年，初命侍郎总督粮储兼巡抚", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 51, "item_id": "02-020", "era": {"text": "嘉靖三十三年", "dynasty": "明", "reign": "嘉靖", "year": 33},
     "target": {"text": "总理粮储", "ent_ids": []}, "action": "加提督军务",
     "content": "嘉靖三十三年，以海警，加提督军务，驻苏州", "category": "职掌变更", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚浙江 ============
    {"slot": 52, "item_id": "02-021", "era": {"text": "嘉靖二十六年", "dynasty": "明", "reign": "嘉靖", "year": 26},
     "target": {"text": "巡抚浙江", "ent_ids": []}, "action": "命都御史巡抚",
     "content": "嘉靖二十六年，以海警，始命都御史巡抚浙江", "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 53, "item_id": "02-021", "era": {"text": "嘉靖三十一年", "dynasty": "明", "reign": "嘉靖", "year": 31},
     "target": {"text": "巡抚浙江", "ent_ids": []}, "action": "复设",
     "content": "二十七年改巡抚为巡视。二十八年罢。三十一年复设", "category": "复设", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚福建 ============
    {"slot": 54, "item_id": "02-022", "era": {"text": "嘉靖三十五年", "dynasty": "明", "reign": "嘉靖", "year": 35},
     "target": {"text": "巡抚福建", "ent_ids": []}, "action": "设",
     "content": "三十五年，以闽、浙道远，又设提督军务兼巡福、兴、漳、泉、福宁海道都御史",
     "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚顺天 ============
    {"slot": 55, "item_id": "02-023", "era": {"text": "成化二年", "dynasty": "明", "reign": "成化", "year": 2},
     "target": {"text": "巡抚顺天", "ent_ids": []}, "action": "专设都御史",
     "content": "成化二年，始专设都御史赞理军务，巡抚顺天、永平二府",
     "category": "初置", "related_evo": [], "confidence": 0.92},

    # ============ 巡抚保定 ============
    {"slot": 56, "item_id": "02-024", "era": {"text": "成化八年", "dynasty": "明", "reign": "成化", "year": 8},
     "target": {"text": "巡抚保定", "ent_ids": []}, "action": "另设",
     "content": "成化八年，分居庸关以西，另设巡抚保定、真定、河间、顺德、大名、广平六府，驻真定",
     "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 57, "item_id": "02-024", "era": {"text": "万历七年", "dynasty": "明", "reign": "万历", "year": 7},
     "target": {"text": "巡抚保定", "ent_ids": []}, "action": "兼管河道",
     "content": "万历七年，兼管河道", "category": "职掌变更", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚河南 ============
    {"slot": 58, "item_id": "02-025", "era": {"text": "宣德五年", "dynasty": "明", "reign": "宣德", "year": 5},
     "target": {"text": "巡抚河南", "ent_ids": []}, "action": "遣",
     "content": "宣德五年，遣兵部侍郎于谦巡抚山西、河南", "category": "初置", "related_evo": [], "confidence": 0.92},

    # ============ 巡抚山西 ============
    {"slot": 59, "item_id": "02-026", "era": {"text": "正统十三年", "dynasty": "明", "reign": "正统", "year": 13},
     "target": {"text": "巡抚山西", "ent_ids": []}, "action": "专抚",
     "content": "正统十三年，始命都御史专抚山西，镇守雁门", "category": "改置", "related_evo": [], "confidence": 0.92},

    # ============ 巡抚山东 ============
    {"slot": 60, "item_id": "02-027", "era": {"text": "正统五年", "dynasty": "明", "reign": "正统", "year": 5},
     "target": {"text": "巡抚山东", "ent_ids": []}, "action": "始设",
     "content": "正统五年始设巡抚。十三年，定遣都御史", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 61, "item_id": "02-027", "era": {"text": "嘉靖四十二年", "dynasty": "明", "reign": "嘉靖", "year": 42},
     "target": {"text": "巡抚山东", "ent_ids": []}, "action": "加督理营田",
     "content": "嘉靖四十二年，加督理营田", "category": "职掌变更", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚辽东 ============
    {"slot": 62, "item_id": "02-028", "era": {"text": "正统元年", "dynasty": "明", "reign": "正统", "year": 1},
     "target": {"text": "巡抚辽东", "ent_ids": []}, "action": "设",
     "content": "正统元年设，旧驻辽阳，后地日蹙，移驻广宁，驻山海关，后又驻宁远",
     "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚宣府 ============
    {"slot": 63, "item_id": "02-029", "era": {"text": "正统元年", "dynasty": "明", "reign": "正统", "year": 1},
     "target": {"text": "巡抚宣府", "ent_ids": []}, "action": "奏设",
     "content": "正统元年，命都御史出巡塞北，因奏设巡抚兼理大同",
     "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚大同 ============
    {"slot": 64, "item_id": "02-030", "era": {"text": "成化十年", "dynasty": "明", "reign": "成化", "year": 10},
     "target": {"text": "巡抚大同", "ent_ids": []}, "action": "专设",
     "content": "成化十年，复专设，加赞理军务", "category": "复设", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚延绥 ============
    {"slot": 65, "item_id": "02-031", "era": {"text": "宣德十年", "dynasty": "明", "reign": "宣德", "year": 10},
     "target": {"text": "巡抚延绥", "ent_ids": []}, "action": "遣都御史出镇",
     "content": "宣德十年，遣都御史出镇。景泰元年，专设巡抚加参赞军务",
     "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 66, "item_id": "02-031", "era": {"text": "成化九年", "dynasty": "明", "reign": "成化", "year": 9},
     "target": {"text": "巡抚延绥", "ent_ids": []}, "action": "徙镇",
     "content": "成化九年，徙镇榆林", "category": "移驻", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚宁夏 ============
    {"slot": 67, "item_id": "02-032", "era": {"text": "正统元年", "dynasty": "明", "reign": "正统", "year": 1},
     "target": {"text": "巡抚宁夏", "ent_ids": []}, "action": "镇抚",
     "content": "正统元年，以右佥都御史郭智镇抚宁夏，参赞军务", "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 68, "item_id": "02-032", "era": {"text": "天顺元年", "dynasty": "明", "reign": "天顺", "year": 1},
     "target": {"text": "巡抚宁夏", "ent_ids": []}, "action": "罢复设",
     "content": "天顺元年罢。二年复设，去参赞", "category": "废置", "related_evo": [], "confidence": 0.88},

    # ============ 巡抚甘肃 ============
    {"slot": 69, "item_id": "02-033", "era": {"text": "宣德十年", "dynasty": "明", "reign": "宣德", "year": 10},
     "target": {"text": "巡抚甘肃", "ent_ids": []}, "action": "命侍郎镇守",
     "content": "宣德十年，命侍郎镇守。正统元年，甘、凉用兵，命侍郎参赞军务",
     "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚陕西 ============
    {"slot": 70, "item_id": "02-034", "era": {"text": "景泰初", "dynasty": "明", "reign": "景泰", "year": "未明"},
     "target": {"text": "巡抚陕西", "ent_ids": []}, "action": "改都御史巡抚",
     "content": "景泰初，耿九畴以刑部侍郎出镇，特改都御史巡抚",
     "category": "改置", "related_evo": [], "confidence": 0.9},
    {"slot": 71, "item_id": "02-034", "era": {"text": "成化二年", "dynasty": "明", "reign": "成化", "year": 2},
     "target": {"text": "巡抚陕西", "ent_ids": []}, "action": "加提督军务后改赞理",
     "content": "成化二年，加提督军务，后改赞理，驻西安，防秋驻固原",
     "category": "职掌变更", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚四川 ============
    {"slot": 72, "item_id": "02-035", "era": {"text": "正统十四年", "dynasty": "明", "reign": "正统", "year": 14},
     "target": {"text": "巡抚四川", "ent_ids": []}, "action": "始设巡抚",
     "content": "宣德五年，命都御史镇抚，后停遣。正统十四年，始设巡抚",
     "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 73, "item_id": "02-035", "era": {"text": "万历十一年", "dynasty": "明", "reign": "万历", "year": 11},
     "target": {"text": "巡抚四川", "ent_ids": []}, "action": "加提督军务",
     "content": "万历十一年，加提督军务", "category": "职掌变更", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚湖广 ============
    {"slot": 74, "item_id": "02-036", "era": {"text": "正统三年", "dynasty": "明", "reign": "正统", "year": 3},
     "target": {"text": "巡抚湖广", "ent_ids": []}, "action": "命都御史镇守",
     "content": "正统三年，命都御史贾谅镇守", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 75, "item_id": "02-036", "era": {"text": "景泰元年", "dynasty": "明", "reign": "景泰", "year": 1},
     "target": {"text": "巡抚湖广", "ent_ids": []}, "action": "定设",
     "content": "景泰元年定设巡抚都御史兼赞理军务", "category": "改置", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚江西 ============
    {"slot": 76, "item_id": "02-037", "era": {"text": "嘉靖六年", "dynasty": "明", "reign": "嘉靖", "year": 6},
     "target": {"text": "巡抚江西", "ent_ids": []}, "action": "定设",
     "content": "成化以后，定为巡抚，或有时罢遣。嘉靖六年始定设。四十年加兼理军务",
     "category": "改置", "related_evo": [], "confidence": 0.88},

    # ============ 巡抚南赣汀韶 ============
    {"slot": 77, "item_id": "02-038", "era": {"text": "弘治十年", "dynasty": "明", "reign": "弘治", "year": 10},
     "target": {"text": "巡抚南赣汀韶", "ent_ids": []}, "action": "始设巡抚",
     "content": "弘治十年，始设巡抚。正德十一年，改提督军务",
     "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 78, "item_id": "02-038", "era": {"text": "嘉靖四十五年", "dynasty": "明", "reign": "嘉靖", "year": 45},
     "target": {"text": "巡抚南赣汀韶", "ent_ids": []}, "action": "定巡抚衔",
     "content": "嘉靖四十五年，定巡抚衔，所辖南安、赣州、南雄、韶州、汀州并郴州地方，驻赣州",
     "category": "改置", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚广东 ============
    {"slot": 79, "item_id": "02-039", "era": {"text": "嘉靖四十五年", "dynasty": "明", "reign": "嘉靖", "year": 45},
     "target": {"text": "巡抚广东", "ent_ids": []}, "action": "复另设",
     "content": "永乐中，设巡抚，后以总督兼巡抚事，遂罢不设。嘉靖四十五年，复另设巡抚，加赞理军务",
     "category": "复设", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚广西 ============
    {"slot": 80, "item_id": "02-040", "era": {"text": "隆庆三年", "dynasty": "明", "reign": "隆庆", "year": 3},
     "target": {"text": "巡抚广西", "ent_ids": []}, "action": "复专设",
     "content": "广西旧有巡抚，沿革不常。隆庆三年复专设", "category": "复设", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚云南 ============
    {"slot": 81, "item_id": "02-041", "era": {"text": "正统九年", "dynasty": "明", "reign": "正统", "year": 9},
     "target": {"text": "巡抚云南", "ent_ids": []}, "action": "命侍郎参赞军务",
     "content": "正统九年，命侍郎参赞军务。十年，设镇抚。天顺元年罢",
     "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚贵州 ============
    {"slot": 82, "item_id": "02-042", "era": {"text": "正统十四年", "dynasty": "明", "reign": "正统", "year": 14},
     "target": {"text": "巡抚贵州", "ent_ids": []}, "action": "置总督",
     "content": "正统十四年，以苗乱置总督，镇守贵州、湖北、川东等处",
     "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 83, "item_id": "02-042", "era": {"text": "景泰元年", "dynasty": "明", "reign": "景泰", "year": 1},
     "target": {"text": "巡抚贵州", "ent_ids": []}, "action": "另设巡抚",
     "content": "景泰元年，另设贵州巡抚", "category": "改置", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚天津 ============
    {"slot": 84, "item_id": "02-043", "era": {"text": "万历二十五年", "dynasty": "明", "reign": "万历", "year": 25},
     "target": {"text": "巡抚天津", "ent_ids": []}, "action": "暂设",
     "content": "万历二十五年，以倭陷朝鲜暂设，寻为定制", "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚登莱 ============
    {"slot": 85, "item_id": "02-044", "era": {"text": "天启元年", "dynasty": "明", "reign": "天启", "year": 1},
     "target": {"text": "巡抚登莱", "ent_ids": []}, "action": "设",
     "content": "天启元年设。崇祯二年罢。三年复设", "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚安庐 ============
    {"slot": 86, "item_id": "02-045", "era": {"text": "崇祯十年", "dynasty": "明", "reign": "崇祯", "year": 10},
     "target": {"text": "巡抚安庐", "ent_ids": []}, "action": "设",
     "content": "崇祯十年设，以史可法为之。十六年，又增设安、太、池、庐四府巡抚",
     "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 巡抚偏沅 ============
    {"slot": 87, "item_id": "02-046", "era": {"text": "万历二十七年", "dynasty": "明", "reign": "万历", "year": 27},
     "target": {"text": "巡抚偏沅", "ent_ids": []}, "action": "暂设",
     "content": "万历二十七年，以征播暂设，寻罢。天启二年后，或置或罢。崇祯二年定设",
     "category": "初置", "related_evo": [], "confidence": 0.88},

    # ============ 崇祯新增（密云/淮扬/承天）============
    {"slot": 88, "item_id": "02-047", "era": {"text": "崇祯十一年", "dynasty": "明", "reign": "崇祯", "year": 11},
     "target": {"text": "巡抚密云", "ent_ids": []}, "action": "设",
     "content": "崇祯十一年设", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 89, "item_id": "02-048", "era": {"text": "崇祯十一年", "dynasty": "明", "reign": "崇祯", "year": 11},
     "target": {"text": "巡抚淮扬", "ent_ids": []}, "action": "设",
     "content": "崇祯十一年设", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 90, "item_id": "02-049", "era": {"text": "崇祯十六年", "dynasty": "明", "reign": "崇祯", "year": 16},
     "target": {"text": "巡抚承天", "ent_ids": []}, "action": "设",
     "content": "崇祯十六年设", "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 抚治郧阳 ============
    {"slot": 91, "item_id": "02-050", "era": {"text": "成化十二年", "dynasty": "明", "reign": "成化", "year": 12},
     "target": {"text": "抚治郧阳", "ent_ids": []}, "action": "奏设",
     "content": "成化十二年，以郧、襄流民屡叛，遣都御史安抚，因奏设官抚治之",
     "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 92, "item_id": "02-050", "era": {"text": "万历二年", "dynasty": "明", "reign": "万历", "year": 2},
     "target": {"text": "抚治郧阳", "ent_ids": []}, "action": "改",
     "content": "万历二年以抚治事权不专，改（详后）", "category": "改置", "related_evo": [], "confidence": 0.85},

    # ============ 赞理松潘 ============
    {"slot": 93, "item_id": "02-051", "era": {"text": "正统四年", "dynasty": "明", "reign": "正统", "year": 4},
     "target": {"text": "赞理松潘", "ent_ids": []}, "action": "以王翱为之",
     "content": "正统四年，以王翱为之", "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 通政使司 ============
    {"slot": 94, "item_id": "02-054", "era": {"text": "洪武三年", "dynasty": "明", "reign": "洪武", "year": 3},
     "target": {"text": "通政使司", "ent_ids": []}, "action": "置察言司",
     "content": "初，洪武三年置察言司，设司令二人，掌受四方章奏，寻罢",
     "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 95, "item_id": "02-054", "era": {"text": "洪武十年", "dynasty": "明", "reign": "洪武", "year": 10},
     "target": {"text": "通政使司", "ent_ids": []}, "action": "置",
     "content": "十年置通政使司，以曾秉正为通政使，刘仁为左通政",
     "category": "初置", "related_evo": [], "confidence": 0.95},
    {"slot": 96, "item_id": "02-054", "era": {"text": "洪武十二年", "dynasty": "明", "reign": "洪武", "year": 12},
     "target": {"text": "通政使司", "ent_ids": []}, "action": "拨隶",
     "content": "十二年，拨承敕监给事中、殿廷仪礼司、九关通事使隶焉",
     "category": "增员", "related_evo": [], "confidence": 0.9},
    {"slot": 97, "item_id": "02-054", "era": {"text": "建文中", "dynasty": "明", "reign": "建文", "year": "未明"},
     "target": {"text": "通政使司", "ent_ids": []}, "action": "改司为寺",
     "content": "建文中，改司为寺，通政使为通政卿，通政参议为少卿",
     "category": "改称", "related_evo": [], "confidence": 0.9},
    {"slot": 98, "item_id": "02-054", "era": {"text": "成化二年", "dynasty": "明", "reign": "成化", "year": 2},
     "target": {"text": "通政使司", "ent_ids": []}, "action": "置提督誊黄右通政",
     "content": "成化二年，置提督誊黄右通政，不理司事，录武官黄卫所袭替之故，以征赞事",
     "category": "增员", "related_evo": [], "confidence": 0.9},
    {"slot": 99, "item_id": "02-054", "era": {"text": "万历九年", "dynasty": "明", "reign": "万历", "year": 9},
     "target": {"text": "通政使司", "ent_ids": []}, "action": "革",
     "content": "万历九年革", "category": "废置", "related_evo": [], "confidence": 0.9},

    # ============ 大理寺 ============
    {"slot": 100, "item_id": "02-057", "era": {"text": "吴元年", "dynasty": "明", "reign": "吴", "year": 1},
     "target": {"text": "大理寺", "ent_ids": []}, "action": "置",
     "content": "初，吴元年置大理司卿，秩正三品。洪武元年革",
     "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 101, "item_id": "02-057", "era": {"text": "洪武三年", "dynasty": "明", "reign": "洪武", "year": 3},
     "target": {"text": "大理寺", "ent_ids": []}, "action": "置磨勘司",
     "content": "三年，置磨勘司。寻亦革。十四年复置磨勘司，二十年复罢",
     "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 102, "item_id": "02-057", "era": {"text": "洪武十四年", "dynasty": "明", "reign": "洪武", "year": 14},
     "target": {"text": "大理寺", "ent_ids": []}, "action": "复置",
     "content": "十四年，复置大理寺，改卿秩正五品，左、右少卿从五品，左、右寺丞正六品",
     "category": "复设", "related_evo": [], "confidence": 0.92},
    {"slot": 103, "item_id": "02-057", "era": {"text": "洪武十七年", "dynasty": "明", "reign": "洪武", "year": 17},
     "target": {"text": "大理寺", "ent_ids": []}, "action": "改建官署",
     "content": "十七年，改建刑部、都察院、大理寺、审刑司、五军断事官署于太平门外",
     "category": "移驻", "related_evo": [], "confidence": 0.9},

    # ============ 翰林院 ============
    {"slot": 104, "item_id": "02-066", "era": {"text": "吴元年", "dynasty": "明", "reign": "吴", "year": 1},
     "target": {"text": "翰林院", "ent_ids": []}, "action": "初置",
     "content": "吴元年，初置翰林院，秩正三品", "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 105, "item_id": "02-066", "era": {"text": "洪武二年", "dynasty": "明", "reign": "洪武", "year": 2},
     "target": {"text": "翰林院", "ent_ids": []}, "action": "置学士承旨",
     "content": "洪武二年，置学士承旨，正三品，改学士，从三品",
     "category": "增员", "related_evo": [], "confidence": 0.9},
    {"slot": 106, "item_id": "02-066", "era": {"text": "洪武十四年", "dynasty": "明", "reign": "洪武", "year": 14},
     "target": {"text": "翰林院", "ent_ids": []}, "action": "定品革官",
     "content": "十四年，定学士为正五品，革承旨、直学士、待制、应奉、检阅、典簿，设孔目、《五经》博士、侍书、待诏、检讨",
     "category": "升秩降秩", "related_evo": [], "confidence": 0.92},
    {"slot": 107, "item_id": "02-066", "era": {"text": "洪武十八年", "dynasty": "明", "reign": "洪武", "year": 18},
     "target": {"text": "翰林院", "ent_ids": []}, "action": "更定品员",
     "content": "十八年，更定品员，以侍读先侍讲", "category": "改置", "related_evo": [], "confidence": 0.9},

    # ============ 庶吉士 ============
    {"slot": 108, "item_id": "02-068", "era": {"text": "永乐二年", "dynasty": "明", "reign": "永乐", "year": 2},
     "target": {"text": "庶吉士", "ent_ids": []}, "action": "定为翰林院庶吉士",
     "content": "永乐二年，始定为翰林院庶吉士，选进士文学优等及善书者为之",
     "category": "改置", "related_evo": [], "confidence": 0.92},
    {"slot": 109, "item_id": "02-068", "era": {"text": "宣德五年", "dynasty": "明", "reign": "宣德", "year": 5},
     "target": {"text": "庶吉士", "ent_ids": []}, "action": "命学士教习",
     "content": "宣德五年，始命学士教习", "category": "职掌变更", "related_evo": [], "confidence": 0.9},

    # ============ 弘文馆 ============
    {"slot": 110, "item_id": "02-069", "era": {"text": "洪武三年", "dynasty": "明", "reign": "洪武", "year": 3},
     "target": {"text": "弘文馆", "ent_ids": []}, "action": "置",
     "content": "明初，尝置弘文馆学士（洪武三年置，以胡铉为学士）",
     "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 国子监 ============
    {"slot": 111, "item_id": "02-072", "era": {"text": "乙巳九月", "dynasty": "明", "reign": "吴", "year": "未明"},
     "target": {"text": "国子监", "ent_ids": []}, "action": "置国子学",
     "content": "乙巳九月置国子学，以故集庆路学为之", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 112, "item_id": "02-072", "era": {"text": "洪武十四年", "dynasty": "明", "reign": "洪武", "year": 14},
     "target": {"text": "国子监", "ent_ids": []}, "action": "改建国子学",
     "content": "洪武十四年，改建国子学于鸡鸣山下", "category": "移驻", "related_evo": [], "confidence": 0.92},

    # ============ 衍圣公 ============
    {"slot": 113, "item_id": "02-074", "era": {"text": "洪武元年", "dynasty": "明", "reign": "洪武", "year": 1},
     "target": {"text": "衍圣公", "ent_ids": []}, "action": "袭封",
     "content": "洪武元年，太祖既以孔希学袭封衍圣公", "category": "改置", "related_evo": [], "confidence": 0.92},
]
