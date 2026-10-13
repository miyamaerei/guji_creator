# -*- coding: utf-8 -*-
"""
【卷02】L3 流程层源数据
本书四类流程：选官 / 考察 / 封赠荫叙 / 朝贡接待。
卷02 涉及：都察院考察纠劾链、巡按出巡流程、大理寺审谳流程。
不建 state_machine；不写 events 字段。
"""

PROCS = [
    # ---------- 条2 都御史纠劾考察流程 ----------
    {"slot": 1, "item_id": "02-002", "name": "都御史纠劾流程", "scope": "考察",
     "steps": [
         {"seq": 1, "text": "凡大臣奸邪、小人构党、作威福乱政者，劾",
          "agent": {"text": "都御史", "agent_ent_ids": []}, "condition": "大臣奸邪乱政", "next": [2]},
         {"seq": 2, "text": "凡百官猥茸贪冒坏官纪者，劾",
          "agent": {"text": "都御史", "agent_ent_ids": []}, "condition": "百官坏官纪", "next": [3]},
         {"seq": 3, "text": "凡学术不正、上书陈言变乱成宪、希进用者，劾",
          "agent": {"text": "都御史", "agent_ent_ids": []}, "condition": "学术不正希进用", "next": [4]},
         {"seq": 4, "text": "遇朝觐、考察，同吏部司贤否陟黜",
          "agent": {"text": "都御史", "agent_ent_ids": []}, "condition": "朝觐考察", "next": [5]},
         {"seq": 5, "text": "大狱重囚会鞫于外朝，偕刑部、大理谳平之",
          "agent": {"text": "都御史", "agent_ent_ids": []}, "condition": "大狱重囚", "next": []},
     ], "confidence": 0.92},

    # ---------- 条3 巡按御史出巡流程 ----------
    {"slot": 2, "item_id": "02-003", "name": "巡按御史出巡流程", "scope": "考察",
     "steps": [
         {"seq": 1, "text": "在内两京刷卷，巡视京营，监临乡、会试及武举，巡视光禄，巡视仓场，巡视内库、皇城、五城，轮值登闻鼓",
          "agent": {"text": "监察御史", "agent_ent_ids": []}, "condition": "在内", "next": [2]},
         {"seq": 2, "text": "在外巡按，(北直隶二人，南直隶三人，宣大一人，辽东一人，甘肃一人，十三省各一人。)清军，提督学校，巡盐，茶马，巡漕，巡关，攒运，印马，屯田",
          "agent": {"text": "监察御史", "agent_ent_ids": []}, "condition": "在外", "next": [3]},
         {"seq": 3, "text": "师行则监军纪功，各以其事专监察",
          "agent": {"text": "监察御史", "agent_ent_ids": []}, "condition": "师行", "next": [4]},
         {"seq": 4, "text": "按临所至，必先审录罪囚，吊刷案卷",
          "agent": {"text": "巡按御史", "agent_ent_ids": []}, "condition": "按临所至", "next": [5]},
         {"seq": 5, "text": "所按藩服大臣、府州县官诸考察，举劾尤专，大事奏裁，小事立断",
          "agent": {"text": "巡按御史", "agent_ent_ids": []}, "condition": "考察地方官", "next": []},
     ], "confidence": 0.9},

    # ---------- 条53 通政使司受章流程 ----------
    {"slot": 3, "item_id": "02-053", "name": "通政使司受理章疏流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "凡四方陈情建言，申诉冤滞，或告不法等事",
          "agent": {"text": "通政使", "agent_ent_ids": []}, "condition": "四方陈情申诉", "next": [2]},
         {"seq": 2, "text": "于底簿内誊写诉告缘由，赍状奏闻",
          "agent": {"text": "通政使", "agent_ent_ids": []}, "condition": "受理登记", "next": [3]},
         {"seq": 3, "text": "当执奏者勿忌避，当驳正者勿阿随，当敷陈者毋隐蔽，当引见者毋留难",
          "agent": {"text": "通政使", "agent_ent_ids": []}, "condition": "审命令以正百司，达幽隐以通庶务", "next": []},
     ], "confidence": 0.9},

    # ---------- 条56 大理寺审谳流程 ----------
    {"slot": 4, "item_id": "02-056", "name": "大理寺审谳平反流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "凡刑部、都察院、五军断事官所推问狱讼，皆移案牍，引囚徒，诣寺详谳",
          "agent": {"text": "大理寺卿", "agent_ent_ids": []}, "condition": "刑部等都察院移案", "next": [2]},
         {"seq": 2, "text": "左、右寺分理京畿、十三布政司刑名之事",
          "agent": {"text": "左、右寺正", "agent_ent_ids": []}, "condition": "分理刑名", "next": [3]},
         {"seq": 3, "text": "掌审谳平反刑狱之政令。少卿、寺丞赞之",
          "agent": {"text": "大理寺卿", "agent_ent_ids": []}, "condition": "审谳平反", "next": []},
     ], "confidence": 0.9},

    # ---------- 条57 审刑司复详议流程 ----------
    {"slot": 5, "item_id": "02-057", "name": "审刑司复详议流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "凡诸司刑名、钱粮，有冤滥隐匿者，稽其功过以闻（磨勘司）",
          "agent": {"text": "磨勘司", "agent_ent_ids": []}, "condition": "冤滥隐匿", "next": [2]},
         {"seq": 2, "text": "凡大理寺所理之刑，审刑司复详议之",
          "agent": {"text": "审刑司", "agent_ent_ids": []}, "condition": "大理寺所理之刑", "next": []},
     ], "confidence": 0.9},

    # ---------- 条59 詹事府辅导太子流程 ----------
    {"slot": 6, "item_id": "02-059", "name": "詹事府辅导太子流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "掌统府、坊、局之政事，以辅导太子。少詹事佐之",
          "agent": {"text": "詹事", "agent_ent_ids": []}, "condition": "未明", "next": [2]},
         {"seq": 2, "text": "凡入侍太子，与坊、局翰林官番直进讲《尚书》、《春秋》、《资治通鉴》",
          "agent": {"text": "坊、局翰林官", "agent_ent_ids": []}, "condition": "入侍太子", "next": []},
     ], "confidence": 0.88},

    # ---------- 条64 翰林院制诰修书流程 ----------
    {"slot": 7, "item_id": "02-064", "name": "翰林院制诰考议流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "掌制诰、史册、文翰之事，以考议制度，详正文书，备天子顾问",
          "agent": {"text": "翰林院学士", "agent_ent_ids": []}, "condition": "未明", "next": [2]},
         {"seq": 2, "text": "凡经筵日讲，纂修实录、玉牒、史志诸书，编纂六曹章奏，皆预焉",
          "agent": {"text": "翰林院", "agent_ent_ids": []}, "condition": "经筵纂修", "next": []},
     ], "confidence": 0.9},

    # ---------- 条65 史官记注纂修流程 ----------
    {"slot": 8, "item_id": "02-065", "name": "史官记注纂修流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "掌修国史。凡天文、地理、宗潢、礼乐、兵刑诸大政，及诏敕、书檄，批答王言，皆籍而记之，以备实录",
          "agent": {"text": "史官", "agent_ent_ids": []}, "condition": "诸大政及诏敕", "next": [2]},
         {"seq": 2, "text": "国家有纂修著作之书，则分掌考辑撰述之事",
          "agent": {"text": "史官", "agent_ent_ids": []}, "condition": "纂修著作", "next": [3]},
         {"seq": 3, "text": "经筵充展卷官，乡试充考试官，会试充同考官，殿试充收卷官",
          "agent": {"text": "史官", "agent_ent_ids": []}, "condition": "经筵考试", "next": []},
     ], "confidence": 0.9},

    # ---------- 条71 国子监训导流程 ----------
    {"slot": 9, "item_id": "02-071", "name": "国子监训导诸生流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "掌国学诸生训导之政令",
          "agent": {"text": "祭酒、司业", "agent_ent_ids": []}, "condition": "未明", "next": [2]},
         {"seq": 2, "text": "凡举人、贡生、官生、恩生、功生、例生、土官、外国生、幼勋臣及勋戚大臣子弟之入监者，奉监规而训课之，造以明体达用之学",
          "agent": {"text": "祭酒、司业", "agent_ent_ids": []}, "condition": "诸生入监", "next": []},
     ], "confidence": 0.9},
]
