# -*- coding: utf-8 -*-
"""C14 时间沿革层源数据 —— 卷一（食货一）。

纪律（schemas §8 / validate_layers）：必填 office/category/reign；
category 用 TME_CATEGORIES；reign 用 REIGN_ORDER（无据未明）。
office 记沿革主体（制度 / 机构 / 官署，以原文为凭）。
"""

AI_RECORDS = [
    # ---------- 户籍黄册 ----------
    {
        "item_id": "01-003",
        "office": "户帖户籍",
        "category": "初置",
        "reign": "洪武",
        "evidence": "太祖籍天下户口，置户帖、户籍，具书名、岁、居地",
    },
    {
        "item_id": "01-003",
        "office": "赋役黄册",
        "category": "初置",
        "reign": "洪武",
        "evidence": "洪武十四年诏天下编赋役黄册，以一百十户为一里",
    },
    {
        "item_id": "01-003",
        "office": "赋役黄册",
        "category": "法弊",
        "reign": "未明",
        "evidence": "其后黄册只具文，有司征税、编徭，自为一册，曰白册",
    },
    # ---------- 逃户流民 ----------
    {
        "item_id": "01-005",
        "office": "逃户周知册",
        "category": "初置",
        "reign": "正统",
        "evidence": "正统时，造逃户周知册，核其丁粮",
    },
    {
        "item_id": "01-007",
        "office": "附籍",
        "category": "改置",
        "reign": "正统",
        "evidence": "正统时，附籍者复还原籍",
    },
    # ---------- 富户 ----------
    {
        "item_id": "01-009",
        "office": "富户",
        "category": "初置",
        "reign": "洪武",
        "evidence": "太祖徙富户实京师，谓之富户",
    },
    {
        "item_id": "01-009",
        "office": "富户",
        "category": "定额变更",
        "reign": "弘治",
        "evidence": "弘治五年始免解在逃富户，每户徵银三两，与厢民助役",
    },
    {
        "item_id": "01-009",
        "office": "富户",
        "category": "定额变更",
        "reign": "嘉靖",
        "evidence": "嘉靖中减为二两，以充边饷",
    },
    # ---------- 田制 ----------
    {
        "item_id": "01-012",
        "office": "鱼鳞图册",
        "category": "初置",
        "reign": "洪武",
        "evidence": "洪武二十年命国子生武淳等分行州县，编类为册，号曰鱼鳞图册",
    },
    {
        "item_id": "01-012",
        "office": "司农司",
        "category": "初置",
        "reign": "洪武",
        "evidence": "设司农司，开治河南，掌其事",
    },
    {
        "item_id": "01-013",
        "office": "田亩丈量",
        "category": "职掌变更",
        "reign": "万历",
        "evidence": "万历六年帝用大学士张居正议，天下田亩通行丈量",
    },
    # ---------- 屯田 ----------
    {
        "item_id": "01-014",
        "office": "民兵万户府",
        "category": "初置",
        "reign": "洪武",
        "evidence": "太祖初，立民兵万户府，寓兵於农，其法最善",
    },
    {
        "item_id": "01-015",
        "office": "军屯科则",
        "category": "定额变更",
        "reign": "建文",
        "evidence": "三十五年定科则：军田一分，正粮十二石，贮屯仓",
    },
    {
        "item_id": "01-015",
        "office": "屯田赏罚例",
        "category": "初置",
        "reign": "永乐",
        "evidence": "永乐初，定屯田官军赏罚例",
    },
    {
        "item_id": "01-017",
        "office": "屯政",
        "category": "法弊",
        "reign": "正统",
        "evidence": "自正统后，屯政稍弛，屯粮多为内监军官占夺",
    },
    # ---------- 开中 / 庄田 ----------
    {
        "item_id": "01-018",
        "office": "商屯开中",
        "category": "初置",
        "reign": "洪武",
        "evidence": "明初，募盐商於各边开中，谓之商屯",
    },
    {
        "item_id": "01-018",
        "office": "商屯开中",
        "category": "法弊",
        "reign": "弘治",
        "evidence": "迨弘治中，叶淇变法，而开中始坏，商屯尽废",
    },
    {
        "item_id": "01-020",
        "office": "皇庄",
        "category": "初置",
        "reign": "成化",
        "evidence": "以没入曹吉祥地为宫中庄田，皇庄之名由此始",
    },
    {
        "item_id": "01-021",
        "office": "皇庄",
        "category": "增员",
        "reign": "正德",
        "evidence": "武宗即位，逾月即建皇庄七，其后增至三百馀处",
    },
    {
        "item_id": "01-022",
        "office": "皇庄",
        "category": "改称",
        "reign": "嘉靖",
        "evidence": "夏言清核皇庄田，孙交造皇庄新册；改称官地，不复名皇庄",
    },
    {
        "item_id": "01-023",
        "office": "庄田世次递减",
        "category": "定额变更",
        "reign": "隆庆",
        "evidence": "穆宗从御史王廷瞻言，复定世次递减之限，公主国公庄田世远者存什三",
    },
]
