# -*- coding: utf-8 -*-
"""【卷04】TME 时间沿革层源数据 —— 南京官沿革 + 地方官制沿革"""

TMES = [
    # ============ 条27 南京官（虚拟锚点，主战场）============
    {"slot": 1, "item_id": "04-027", "era": {"text": "永乐四年", "dynasty": "明", "reign": "永乐", "year": 4},
     "target": {"text": "南京官", "ent_ids": []}, "action": "置行部尚书",
     "content": "南京官，自永乐四年成祖往北京，置行部尚书，备行在九卿印以从。是时，皇太子监国，大小庶务悉以委之",
     "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 2, "item_id": "04-027", "era": {"text": "永乐十八年", "dynasty": "明", "reign": "永乐", "year": 18},
     "target": {"text": "南京官", "ent_ids": []}, "action": "官属悉移而北",
     "content": "十八年，官属悉移而北，南京六部所存惟礼、刑、工三部，各一侍郎，在南之官加“南京”字于职衔上",
     "category": "移驻", "related_evo": [], "confidence": 0.95},
    {"slot": 3, "item_id": "04-027", "era": {"text": "洪熙元年", "dynasty": "明", "reign": "洪熙", "year": 1},
     "target": {"text": "南京官", "ent_ids": []}, "action": "补设官属除南京字",
     "content": "仁宗时补设官属，除“南京”字",
     "category": "复设", "related_evo": [], "confidence": 0.9},
    {"slot": 4, "item_id": "04-027", "era": {"text": "正统六年", "dynasty": "明", "reign": "正统", "year": 6},
     "target": {"text": "南京官", "ent_ids": []}, "action": "定制复如永乐时",
     "content": "正统六年，定制复如永乐时",
     "category": "改置", "related_evo": [], "confidence": 0.95},

    # ============ 条2 南京吏部（侍郎沿革）============
    {"slot": 5, "item_id": "04-002", "era": {"text": "弘治后", "dynasty": "明", "reign": "弘治", "year": "未明"},
     "target": {"text": "南京吏部", "ent_ids": []}, "action": "专设右侍郎",
     "content": "六部侍郎，至弘治后始专设右。万历三年俱革。十一年复设。天启中，每部增侍郎一人。崇祯间革",
     "category": "改置", "related_evo": [], "confidence": 0.9},
    {"slot": 6, "item_id": "04-002", "era": {"text": "万历三年", "dynasty": "明", "reign": "万历", "year": 3},
     "target": {"text": "南京吏部", "ent_ids": []}, "action": "革侍郎",
     "content": "万历三年俱革。十一年复设", "category": "裁并", "related_evo": [], "confidence": 0.92},
    {"slot": 7, "item_id": "04-002", "era": {"text": "天启中", "dynasty": "明", "reign": "天启", "year": "未明"},
     "target": {"text": "南京吏部", "ent_ids": []}, "action": "增侍郎一人",
     "content": "天启中，每部增侍郎一人。崇祯间革", "category": "增员", "related_evo": [], "confidence": 0.9},

    # ============ 条4 南京总督粮储 ============
    {"slot": 8, "item_id": "04-004", "era": {"text": "嘉靖以前", "dynasty": "明", "reign": "嘉靖", "year": "未明"},
     "target": {"text": "南京总督粮储", "ent_ids": []}, "action": "特设都御史",
     "content": "嘉靖以前，特设都御史。二十六年革，以户部右侍郎加都御史衔领之",
     "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 9, "item_id": "04-004", "era": {"text": "嘉靖二十六年", "dynasty": "明", "reign": "嘉靖", "year": 26},
     "target": {"text": "南京总督粮储", "ent_ids": []}, "action": "革以侍郎领之",
     "content": "二十六年革，以户部右侍郎加都御史衔领之", "category": "改置", "related_evo": [], "confidence": 0.92},

    # ============ 条6 南京兵部参赞机务 ============
    {"slot": 10, "item_id": "04-006", "era": {"text": "宣德八年", "dynasty": "明", "reign": "宣德", "year": 8},
     "target": {"text": "南京兵部", "ent_ids": []}, "action": "始有参赞机务",
     "content": "按参赞机务，自宣德八年黄福始", "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 11, "item_id": "04-006", "era": {"text": "成化二十三年", "dynasty": "明", "reign": "成化", "year": 23},
     "target": {"text": "南京兵部", "ent_ids": []}, "action": "奉敕谕专以尚书参赞机务",
     "content": "成化二十三年，始奉敕谕，专以本部尚书参赞机务，同内外守备官操练军马，抚恤人民，禁戢盗贼，振举庶务，故其职视五部为特重云",
     "category": "职掌变更", "related_evo": [], "confidence": 0.95},

    # ============ 条9 南京都察院 ============
    {"slot": 12, "item_id": "04-009", "era": {"text": "嘉靖三十七年", "dynasty": "明", "reign": "嘉靖", "year": 37},
     "target": {"text": "南京都察院", "ent_ids": []}, "action": "革司狱一人",
     "content": "嘉靖三十七年，革司狱一人。隆庆（间复）", "category": "裁并", "related_evo": [], "confidence": 0.9},

    # ============ 条12 南京大理寺 ============
    {"slot": 13, "item_id": "04-012", "era": {"text": "隆庆三年", "dynasty": "明", "reign": "隆庆", "year": 3},
     "target": {"text": "南京大理寺", "ent_ids": []}, "action": "革评事各一人",
     "content": "隆庆三年，革左、右评事各一人", "category": "裁并", "related_evo": [], "confidence": 0.92},

    # ============ 条17 南京光禄寺 ============
    {"slot": 14, "item_id": "04-017", "era": {"text": "隆庆四年", "dynasty": "明", "reign": "隆庆", "year": 4},
     "target": {"text": "南京光禄寺", "ent_ids": []}, "action": "革少卿",
     "content": "隆庆四年，革少卿", "category": "裁并", "related_evo": [], "confidence": 0.92},
    {"slot": 15, "item_id": "04-017", "era": {"text": "嘉靖中", "dynasty": "明", "reign": "嘉靖", "year": "未明"},
     "target": {"text": "南京光禄寺", "ent_ids": []}, "action": "革良酝（署官）",
     "content": "嘉靖中，革良酝（四署之一）", "category": "裁并", "related_evo": [], "confidence": 0.88},

    # ============ 条18 南京太仆寺 ============
    {"slot": 16, "item_id": "04-018", "era": {"text": "隆庆中", "dynasty": "明", "reign": "隆庆", "year": "未明"},
     "target": {"text": "南京太仆寺", "ent_ids": []}, "action": "革少卿寺丞各一人",
     "content": "隆庆中，革少卿一人，寺丞一人", "category": "裁并", "related_evo": [], "confidence": 0.9},

    # ============ 条25 南京五城兵马司 ============
    {"slot": 17, "item_id": "04-025", "era": {"text": "万历中", "dynasty": "明", "reign": "万历", "year": "未明"},
     "target": {"text": "南京五城兵马司", "ent_ids": []}, "action": "革副指挥每城二人",
     "content": "万历中，革副指挥每城二人", "category": "裁并", "related_evo": [], "confidence": 0.9},

    # ============ 条26 应天府 ============
    {"slot": 18, "item_id": "04-026", "era": {"text": "洪武三年", "dynasty": "明", "reign": "洪武", "year": 3},
     "target": {"text": "应天府", "ent_ids": []}, "action": "改知府为府尹升秩",
     "content": "洪武三年，改应天府知府为府尹，秩正三品，赐银印",
     "category": "升秩降秩", "related_evo": [], "confidence": 0.95},
    {"slot": 19, "item_id": "04-026", "era": {"text": "洪武十三年", "dynasty": "明", "reign": "洪武", "year": 13},
     "target": {"text": "应天府", "ent_ids": []}, "action": "始立儒学",
     "content": "十三年，始立儒学", "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 条30 王府长史司沿革 ============
    {"slot": 20, "item_id": "04-030", "era": {"text": "洪武三年", "dynasty": "明", "reign": "洪武", "year": 3},
     "target": {"text": "王府长史司", "ent_ids": []}, "action": "置王相府",
     "content": "洪武三年，置王相府，左、右相各一人，左、右傅各一人。参军府，参军一人，录事二人，纪善一人",
     "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 21, "item_id": "04-030", "era": {"text": "洪武四年", "dynasty": "明", "reign": "洪武", "year": 4},
     "target": {"text": "王府长史司", "ent_ids": []}, "action": "更定官制",
     "content": "四年，更定官制（左、右相正二品，文武傅从二品，参军从五品，录事正七品，审理正正六品，纪善正七品等）",
     "category": "改置", "related_evo": [], "confidence": 0.9},

    # ============ 条33 承宣布政使司沿革 ============
    {"slot": 22, "item_id": "04-033", "era": {"text": "戊戌", "dynasty": "明", "reign": "洪武", "year": "未明"},
     "target": {"text": "承宣布政使司", "ent_ids": []}, "action": "置中书分省于婺州",
     "content": "初，太祖下集庆，自领江南行中书省。戊戌，置中书分省于婺州。后每略定地方，即置行省，其官自平章政事以下，大略与中书省同",
     "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 23, "item_id": "04-033", "era": {"text": "洪武九年", "dynasty": "明", "reign": "洪武", "year": 9},
     "target": {"text": "承宣布政使司", "ent_ids": []}, "action": "改行省为布政使司",
     "content": "洪武九年，改行省为承宣布政使司", "category": "改称", "related_evo": [], "confidence": 0.92},

    # ============ 条36 提刑按察使司沿革 ============
    {"slot": 24, "item_id": "04-036", "era": {"text": "吴元年", "dynasty": "明", "reign": "吴", "year": 1},
     "target": {"text": "提刑按察使司", "ent_ids": []}, "action": "置各道按察司",
     "content": "明初，置提刑按察司。吴元年，置各道按察司，设按察使，正三品，副使，正四品，佥事，正五品",
     "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 25, "item_id": "04-036", "era": {"text": "洪武十三年", "dynasty": "明", "reign": "洪武", "year": 13},
     "target": {"text": "提刑按察使司", "ent_ids": []}, "action": "改使秩正四品寻罢",
     "content": "十三年，改使秩正四品，寻罢。十四年复置，并置各道按察分司",
     "category": "升秩降秩", "related_evo": [], "confidence": 0.92},
    {"slot": 26, "item_id": "04-036", "era": {"text": "洪武十五年", "dynasty": "明", "reign": "洪武", "year": 15},
     "target": {"text": "提刑按察使司", "ent_ids": []}, "action": "置天下府州县按察分司",
     "content": "十五年，又置天下府州县按察分司。以儒士王存中等五百三十一人为试佥事，人按二县",
     "category": "增员", "related_evo": [], "confidence": 0.92},
    {"slot": 27, "item_id": "04-036", "era": {"text": "洪武十六年", "dynasty": "明", "reign": "洪武", "year": 16},
     "target": {"text": "提刑按察使司", "ent_ids": []}, "action": "尽罢试佥事改使为从三品",
     "content": "十六年，尽罢试佥事，改按察使为从三品，副使二人，从四品，佥事从五品，多寡从其分道之数",
     "category": "改置", "related_evo": [], "confidence": 0.9},
    {"slot": 28, "item_id": "04-036", "era": {"text": "洪武二十二年", "dynasty": "明", "reign": "洪武", "year": 22},
     "target": {"text": "提刑按察使司", "ent_ids": []}, "action": "复定按察使为正三品",
     "content": "二十二年，复定按察使为正三品", "category": "升秩降秩", "related_evo": [], "confidence": 0.92},
    {"slot": 29, "item_id": "04-036", "era": {"text": "洪武二十九年", "dynasty": "明", "reign": "洪武", "year": 29},
     "target": {"text": "提刑按察使司", "ent_ids": []}, "action": "改按察分司为四十一道",
     "content": "二十九年，改置按察分司为四十一道（直隶六：曰淮西道，曰淮东道，曰苏松道，曰建安徽宁道，曰常镇道，曰京畿…）",
     "category": "改置", "related_evo": [], "confidence": 0.92},

    # ============ 条42 道制沿革 ============
    {"slot": 30, "item_id": "04-042", "era": {"text": "明初", "dynasty": "明", "reign": "洪武", "year": "未明"},
     "target": {"text": "道", "ent_ids": []}, "action": "设巡按御史与试佥事",
     "content": "按明初制，恐守令贪鄙不法，故于直隶府州县设巡按御史，各布政司所属设试佥事。已罢试佥事，改按察分司四十一道，此分巡之始也",
     "category": "初置", "related_evo": [], "confidence": 0.9},

    # ============ 条44 行太仆寺 ============
    {"slot": 31, "item_id": "04-044", "era": {"text": "洪武三十年", "dynasty": "明", "reign": "洪武", "year": 30},
     "target": {"text": "行太仆寺", "ent_ids": []}, "action": "置行太仆寺于五处",
     "content": "洪武三十年，置行太仆寺于山西、北平、陕西、甘肃、辽东。山西、北平、陕西，每寺设少卿一人，丞三人；甘肃、辽东，每寺设少卿、丞各一人",
     "category": "初置", "related_evo": [], "confidence": 0.95},

    # ============ 条46 苑马寺 ============
    {"slot": 32, "item_id": "04-046", "era": {"text": "永乐四年", "dynasty": "明", "reign": "永乐", "year": 4},
     "target": {"text": "苑马寺", "ent_ids": []}, "action": "置苑马寺凡四",
     "content": "永乐四年，置苑马寺凡四：北直隶、辽东、平凉、甘肃",
     "category": "初置", "related_evo": [], "confidence": 0.95},
    {"slot": 33, "item_id": "04-046", "era": {"text": "永乐五年", "dynasty": "明", "reign": "永乐", "year": 5},
     "target": {"text": "苑马寺", "ent_ids": []}, "action": "增设六监二十四苑",
     "content": "五年，增设北直隶苑马寺六监二十四苑（顺义、长春、咸和、驯良四苑，隶清河监）",
     "category": "增员", "related_evo": [], "confidence": 0.92},

    # ============ 条50 都转运盐使司 ============
    {"slot": 34, "item_id": "04-050", "era": {"text": "吴元年", "dynasty": "明", "reign": "吴", "year": 1},
     "target": {"text": "都转运盐使司", "ent_ids": []}, "action": "置两浙都转运司于杭州",
     "content": "明初，置都转运司于两淮。吴元年，置两浙都转运司于杭州，定都转运使秩正三品，设同知，正四品，副使，正五品，运判，正六品",
     "category": "初置", "related_evo": [], "confidence": 0.92},

    # ============ 条52 市舶提举司 ============
    {"slot": 35, "item_id": "04-052", "era": {"text": "吴元年", "dynasty": "明", "reign": "吴", "year": 1},
     "target": {"text": "市舶提举司", "ent_ids": []}, "action": "置市舶提举司",
     "content": "吴元年，置市舶提举司", "category": "初置", "related_evo": [], "confidence": 0.95},
    {"slot": 36, "item_id": "04-052", "era": {"text": "洪武三年", "dynasty": "明", "reign": "洪武", "year": 3},
     "target": {"text": "市舶提举司", "ent_ids": []}, "action": "罢太仓黄渡市舶司",
     "content": "洪武三年，罢太仓、黄渡市舶司", "category": "废置", "related_evo": [], "confidence": 0.92},
    {"slot": 37, "item_id": "04-052", "era": {"text": "洪武七年", "dynasty": "明", "reign": "洪武", "year": 7},
     "target": {"text": "市舶提举司", "ent_ids": []}, "action": "罢三市舶司",
     "content": "七年，罢福建之泉州、浙江之明州、广东之广州三市舶司",
     "category": "废置", "related_evo": [], "confidence": 0.95},
    {"slot": 38, "item_id": "04-052", "era": {"text": "永乐元年", "dynasty": "明", "reign": "永乐", "year": 1},
     "target": {"text": "市舶提举司", "ent_ids": []}, "action": "复置",
     "content": "永乐元年复置，设官如（旧制）", "category": "复设", "related_evo": [], "confidence": 0.95},

    # ============ 条53 茶马司 ============
    {"slot": 39, "item_id": "04-053", "era": {"text": "洪武中", "dynasty": "明", "reign": "洪武", "year": "未明"},
     "target": {"text": "茶马司", "ent_ids": []}, "action": "置三茶马司",
     "content": "洪武中，置洮州、秦州、河州三茶马司，设司令、司丞。十五年改设大使",
     "category": "初置", "related_evo": [], "confidence": 0.92},
    {"slot": 40, "item_id": "04-053", "era": {"text": "洪武十五年", "dynasty": "明", "reign": "洪武", "year": 15},
     "target": {"text": "茶马司", "ent_ids": []}, "action": "改设大使副使",
     "content": "十五年改设大使（副使）", "category": "改置", "related_evo": [], "confidence": 0.9},

    # ============ 条56 府制沿革 ============
    {"slot": 41, "item_id": "04-056", "era": {"text": "明初", "dynasty": "明", "reign": "洪武", "year": "未明"},
     "target": {"text": "府", "ent_ids": []}, "action": "改诸路为府",
     "content": "明初，改诸路为府", "category": "改称", "related_evo": [], "confidence": 0.92},
    {"slot": 42, "item_id": "04-056", "era": {"text": "洪武六年", "dynasty": "明", "reign": "洪武", "year": 6},
     "target": {"text": "府", "ent_ids": []}, "action": "分天下府三等",
     "content": "洪武六年，分天下府三等：粮二十万石以上为上府，知府秩从三品；二十万石以下为中府，知府正四品；十万石以下为下府（知府从三品/正四品）",
     "category": "改置", "related_evo": [], "confidence": 0.92},

    # ============ 条61 县制沿革 ============
    {"slot": 43, "item_id": "04-061", "era": {"text": "吴元年", "dynasty": "明", "reign": "吴", "year": 1},
     "target": {"text": "县", "ent_ids": []}, "action": "定县三等",
     "content": "吴元年，定县三等：粮十万石以下为上县，知县从六品；六万石以下为中县，知县正七品；三万石以下为下县，知县从七品。已，并为正七品",
     "category": "改置", "related_evo": [], "confidence": 0.92},

    # ============ 条63 儒学沿革 ============
    {"slot": 44, "item_id": "04-063", "era": {"text": "明初", "dynasty": "明", "reign": "洪武", "year": "未明"},
     "target": {"text": "儒学", "ent_ids": []}, "action": "置儒学提举司",
     "content": "明初，置儒学提举司", "category": "初置", "related_evo": [], "confidence": 0.9},
    {"slot": 45, "item_id": "04-063", "era": {"text": "洪武二年", "dynasty": "明", "reign": "洪武", "year": 2},
     "target": {"text": "儒学", "ent_ids": []}, "action": "诏天下府州县皆立学",
     "content": "洪武二年，诏天下府州县皆立学", "category": "初置", "related_evo": [], "confidence": 0.95},
    {"slot": 46, "item_id": "04-063", "era": {"text": "洪武十三年", "dynasty": "明", "reign": "洪武", "year": 13},
     "target": {"text": "儒学", "ent_ids": []}, "action": "改州学正为未入流",
     "content": "十三年，改各州学正为未入流（先是从九品）", "category": "升秩降秩", "related_evo": [], "confidence": 0.92},
    {"slot": 47, "item_id": "04-063", "era": {"text": "洪武二十四年", "dynasty": "明", "reign": "洪武", "year": 24},
     "target": {"text": "儒学", "ent_ids": []}, "action": "定训导位杂职上",
     "content": "二十四年，定儒学训导位杂职上", "category": "改置", "related_evo": [], "confidence": 0.92},

    # ============ 条64 巡检司 ============
    {"slot": 48, "item_id": "04-064", "era": {"text": "洪武二年", "dynasty": "明", "reign": "洪武", "year": 2},
     "target": {"text": "巡检司", "ent_ids": []}, "action": "始于广西设巡检司",
     "content": "初，洪武二年，以广西地接瑶、僮，始于关隘冲要之处设巡检司，以警奸盗，后遂增置各处",
     "category": "初置", "related_evo": [], "confidence": 0.95},
    {"slot": 49, "item_id": "04-064", "era": {"text": "洪武十三年二月", "dynasty": "明", "reign": "洪武", "year": 13},
     "target": {"text": "巡检司", "ent_ids": []}, "action": "赐敕谕改为杂职",
     "content": "十三年二月，特赐敕谕之，寻改为杂职", "category": "改置", "related_evo": [], "confidence": 0.92},

    # ============ 条66 税课司 ============
    {"slot": 50, "item_id": "04-066", "era": {"text": "明初", "dynasty": "明", "reign": "洪武", "year": "未明"},
     "target": {"text": "税课司", "ent_ids": []}, "action": "改官店为宣课司通课司",
     "content": "明初，改在京官店为宣课司，府州县官店为通课司，后改通课司为税课司、局",
     "category": "改称", "related_evo": [], "confidence": 0.92},

    # ============ 条69 河泊所 ============
    {"slot": 51, "item_id": "04-069", "era": {"text": "洪武十五年", "dynasty": "明", "reign": "洪武", "year": 15},
     "target": {"text": "河泊所", "ent_ids": []}, "action": "定天下河泊所凡二百五十二",
     "content": "洪武十五年，定天下河泊所凡二百五十二",
     "category": "改置", "related_evo": [], "confidence": 0.95},

    # ============ 条71 递运所 ============
    {"slot": 52, "item_id": "04-071", "era": {"text": "洪武九年", "dynasty": "明", "reign": "洪武", "year": 9},
     "target": {"text": "递运所", "ent_ids": []}, "action": "始置递运所",
     "content": "洪武九年始置。先是，在外多以卫所戍守军士传送军囚，太祖以其有妨练习守御，乃命兵部增置",
     "category": "初置", "related_evo": [], "confidence": 0.95},

    # ============ 条72 铁冶所 ============
    {"slot": 53, "item_id": "04-072", "era": {"text": "洪武七年", "dynasty": "明", "reign": "洪武", "year": 7},
     "target": {"text": "铁冶所", "ent_ids": []}, "action": "初置十三所",
     "content": "洪武七年初置。凡十三所，每所置大使、副使各一人（初，大使正八品，副使正九品，后俱为未入流）",
     "category": "初置", "related_evo": [], "confidence": 0.95},

    # ============ 条73-74 医学/阴阳学 ============
    {"slot": 54, "item_id": "04-073", "era": {"text": "洪武十七年", "dynasty": "明", "reign": "洪武", "year": 17},
     "target": {"text": "医学", "ent_ids": []}, "action": "置医学",
     "content": "洪武十七年置，设官不给禄", "category": "初置", "related_evo": [], "confidence": 0.95},
    {"slot": 55, "item_id": "04-074", "era": {"text": "洪武十七年", "dynasty": "明", "reign": "洪武", "year": 17},
     "target": {"text": "阴阳学", "ent_ids": []}, "action": "置阴阳学",
     "content": "亦洪武十七年置，设官不给禄", "category": "初置", "related_evo": [], "confidence": 0.95},
]
