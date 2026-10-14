# -*- coding: utf-8 -*-
"""C14 时间沿革层源数据 —— 卷二（食货二：赋役）。

纪律（schemas §8 / validate_layers）：必填 office/category/reign；
category 用 TME_CATEGORIES；reign 用 REIGN_ORDER（无据未明）。
office 记沿革主体（制度 / 机构 / 官署，以原文为凭）。
"""

AI_RECORDS = [
    # ---------- 两税 ----------
    {
        "item_id": "02-001",
        "office": "两税法",
        "category": "初置",
        "reign": "未明",
        "evidence": "自杨炎作两税法，简而易行，历代相沿，至明不改",
    },
    {
        "item_id": "02-001",
        "office": "赋役法",
        "category": "初置",
        "reign": "洪武",
        "evidence": "即位之初，定赋役法，一以黄册为准",
    },
    # ---------- 折色 ----------
    {
        "item_id": "02-004",
        "office": "折色法",
        "category": "初置",
        "reign": "洪武",
        "evidence": "洪武九年，令民以银、钞、钱、绢代输，於是谓米麦为本色，而诸折纳税粮者谓之折色",
    },
    {
        "item_id": "02-006",
        "office": "金花银",
        "category": "初置",
        "reign": "正统",
        "evidence": "正统元年，遂仿其制，米麦一石折银二钱五分，入内承运库，谓之金花银",
    },
    {
        "item_id": "02-006",
        "office": "金花银",
        "category": "定额变更",
        "reign": "正统",
        "evidence": "自起运兑军外，粮四石收银一两解京，以为永例",
    },
    # ---------- 官民田则 ----------
    {
        "item_id": "02-007",
        "office": "官民田赋则",
        "category": "初置",
        "reign": "洪武",
        "evidence": "太祖定天下官、民田赋，凡官田亩税五升三合五勺，民田减二升",
    },
    {
        "item_id": "02-007",
        "office": "苏松嘉湖官田",
        "category": "改置",
        "reign": "洪武",
        "evidence": "籍诸豪族及富民田以为官田，按私租簿为税额；司农卿杨宪增其赋，亩加二倍",
    },
    {
        "item_id": "02-008",
        "office": "浙西官民田科则",
        "category": "改置",
        "reign": "建文",
        "evidence": "建文二年诏苏、松准私租起科之赋悉与减免，亩不得过一斗",
    },
    {
        "item_id": "02-008",
        "office": "浙西官民田科则",
        "category": "复设",
        "reign": "永乐",
        "evidence": "成祖尽革建文政，浙西之赋复重",
    },
    {
        "item_id": "02-008",
        "office": "旧额官田租",
        "category": "定额变更",
        "reign": "宣德",
        "evidence": "宣德五年二月诏旧额官田租亩一斗至四斗者各减十之二，四斗一升至一石以上者减十之三",
    },
    {
        "item_id": "02-008",
        "office": "苏松官田科则",
        "category": "改置",
        "reign": "正统",
        "evidence": "正统元年令苏、松、浙江等处官田，准民田起科",
    },
    {
        "item_id": "02-008",
        "office": "杭嘉湖则例",
        "category": "改置",
        "reign": "天顺",
        "evidence": "英宗复辟之初，令孙原贞等定杭、嘉、湖则例，凡重者轻之，轻者重之，欲使科则适均",
    },
    # ---------- 均田均粮 ----------
    {
        "item_id": "02-014",
        "office": "经赋册",
        "category": "初置",
        "reign": "嘉靖",
        "evidence": "欧阳铎与苏州知府王仪尽括官、民田裒益之，履亩清丈，定为等则，所造经赋册著为例",
    },
    {
        "item_id": "02-015",
        "office": "徵一法",
        "category": "初置",
        "reign": "嘉靖",
        "evidence": "徵一者，总徵银米之凡，而计亩均输之",
    },
    {
        "item_id": "02-016",
        "office": "纲银、一串铃",
        "category": "初置",
        "reign": "嘉靖",
        "evidence": "时又有纲银、一串铃诸法，自是民间输纳止收本色及折色银矣",
    },
    # ---------- 加派 ----------
    {
        "item_id": "02-018",
        "office": "增赋加派",
        "category": "初置",
        "reign": "嘉靖",
        "evidence": "三十年，议於南畿、浙江等州县增赋百二十万，加派於是始",
    },
    {
        "item_id": "02-019",
        "office": "提编",
        "category": "改置",
        "reign": "嘉靖",
        "evidence": "东南被倭，南畿、浙、闽多额外提编，江南至四十万。提编者，加派之名也",
    },
    {
        "item_id": "02-021",
        "office": "一条鞭法",
        "category": "初置",
        "reign": "嘉靖",
        "evidence": "一条鞭法者，总括一州县之赋役……嘉靖间，数行数止",
    },
    {
        "item_id": "02-021",
        "office": "一条鞭法",
        "category": "改置",
        "reign": "万历",
        "evidence": "至万历九年乃尽行之，赖行一条鞭法，无他科扰，民力不大绌",
    },
    {
        "item_id": "02-022",
        "office": "辽饷",
        "category": "初置",
        "reign": "万历",
        "evidence": "至四十六年，骤增辽饷三百万，亩加三厘五毫",
    },
    {
        "item_id": "02-022",
        "office": "辽饷",
        "category": "改置",
        "reign": "万历",
        "evidence": "通前后九厘，增赋五百二十万，遂为岁额",
    },
    {
        "item_id": "02-024",
        "office": "助饷均输练饷",
        "category": "改置",
        "reign": "崇祯",
        "evidence": "九厘外亩复徵三厘；既而概徵每两一钱名曰助饷；越二年复行均输法；越二年亩加练饷银一分",
    },
    # ---------- 役法 ----------
    {
        "item_id": "02-025",
        "office": "均工夫",
        "category": "初置",
        "reign": "洪武",
        "evidence": "役法定於洪武元年，田一顷出丁夫一人，不及顷者以他田足之，名曰均工夫",
    },
    {
        "item_id": "02-025",
        "office": "里甲均徭",
        "category": "初置",
        "reign": "洪武",
        "evidence": "迨造黄册成，以一百十户为一里，里分十甲曰里甲；以上中下户为三等，五岁均役，十岁一更造",
    },
    {
        "item_id": "02-026",
        "office": "鼠尾册均徭",
        "category": "初置",
        "reign": "正统",
        "evidence": "论丁粮多少编次先后，曰鼠尾册，按而徵之；正统初，佥事夏时创行於江西，他省仿行之",
    },
    # ---------- 赈济 ----------
    {
        "item_id": "02-032",
        "office": "预备仓",
        "category": "初置",
        "reign": "洪武",
        "evidence": "太祖设预备仓，令老人运钞易米以储粟，以备振济",
    },
    {
        "item_id": "02-033",
        "office": "振米",
        "category": "定额变更",
        "reign": "永乐",
        "evidence": "振米之法，明初大口六斗小口三斗，永乐以后减其数",
    },
    {
        "item_id": "02-034",
        "office": "捐纳事例",
        "category": "初置",
        "reign": "成化",
        "evidence": "捐纳事例，自宪宗始，生员纳米百石以上人国子监",
    },
    {
        "item_id": "02-035",
        "office": "振粥",
        "category": "初置",
        "reign": "嘉靖",
        "evidence": "振粥之法，自世宗始",
    },
    {
        "item_id": "02-036",
        "office": "报灾时限",
        "category": "改置",
        "reign": "弘治",
        "evidence": "报灾之法，洪武时不拘时限。弘治中，始限夏灾不得过五月终，秋灾不得过九月终",
    },
    {
        "item_id": "02-036",
        "office": "报灾时限",
        "category": "改置",
        "reign": "万历",
        "evidence": "万历时，又分近地五月、七月，边地七月、九月",
    },
]
