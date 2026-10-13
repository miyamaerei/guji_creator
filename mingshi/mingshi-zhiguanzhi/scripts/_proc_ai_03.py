# -*- coding: utf-8 -*-
"""
【卷03】L3 流程层源数据
本卷四类流程：祭祀礼乐 / 朝会仪礼 / 朝审传导 / 僧道管理。
"""

PROCS = [
    # ---------- 条2 太常寺祭祀流程 ----------
    {"slot": 1, "item_id": "03-002", "name": "太常寺祭祀流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "先冬十二月朔，奏进明年祭日，天子御奉天殿受之，乃颁于诸司",
          "agent": {"text": "太常寺卿", "agent_ent_ids": []}, "condition": "先冬十二月朔", "next": [2]},
         {"seq": 2, "text": "祭祀先期请省牲，进祝版、铜人，上殿奏请斋戒，亲署御名",
          "agent": {"text": "太常寺", "agent_ent_ids": []}, "condition": "祭祀先期", "next": [3]},
         {"seq": 3, "text": "省牲偕光禄卿。惟大祀车驾亲省，大臣日一省之",
          "agent": {"text": "太常寺、光禄寺", "agent_ent_ids": []}, "condition": "省牲", "next": [4]},
         {"seq": 4, "text": "凡祭，涤器、爨埋、香烛、玉帛，整拂神幄，必恭洁",
          "agent": {"text": "太常寺", "agent_ent_ids": []}, "condition": "祭日", "next": [5]},
         {"seq": 5, "text": "掌燎、看燎、读祝、奏礼、对引、司香、进俎、举麾、陈设、收支、导引、设位、典仪、通赞、奉帛、执爵、司樽、司罍洗，卿贰属各领其事",
          "agent": {"text": "太常寺卿贰属", "agent_ent_ids": []}, "condition": "祭时", "next": []},
     ], "confidence": 0.92},

    # ---------- 条6 光禄寺供办流程 ----------
    {"slot": 2, "item_id": "03-006", "name": "光禄寺祭享宴劳供办流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "凡祭祀，同太常省牲；天子亲祭，进饮福受胙；荐新，循月令献其品物；丧葬供奠馔",
          "agent": {"text": "光禄寺卿", "agent_ent_ids": []}, "condition": "祭祀", "next": [2]},
         {"seq": 2, "text": "所用牲、果、菜物，取之上林苑；不给，市诸民，视时估十加一，其市直季支天财库",
          "agent": {"text": "光禄寺", "agent_ent_ids": []}, "condition": "取物", "next": [3]},
         {"seq": 3, "text": "器皿移工部及募工兼作之，岁省其成败",
          "agent": {"text": "光禄寺、工部", "agent_ent_ids": []}, "condition": "器皿", "next": [4]},
         {"seq": 4, "text": "凡筵宴酒食及外使、降人，俱差其等而供给焉。传奉宣索，籍记而覆奏之",
          "agent": {"text": "光禄寺", "agent_ent_ids": []}, "condition": "筵宴", "next": [5]},
         {"seq": 5, "text": "监以科道官一员，察其出入，纠禁其奸弊",
          "agent": {"text": "科道官", "agent_ent_ids": []}, "condition": "监临", "next": []},
     ], "confidence": 0.9},

    # ---------- 条12 鸿胪寺朝会仪礼流程 ----------
    {"slot": 3, "item_id": "03-012", "name": "鸿胪寺朝会仪礼流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "掌朝会、宾客、吉凶仪礼之事",
          "agent": {"text": "鸿胪寺卿", "agent_ent_ids": []}, "condition": "未明", "next": [2]},
         {"seq": 2, "text": "凡国家大典礼、郊庙、祭祀、朝会、宴飨、经筵、册封、进历、进春、传制、奏捷，各供其事",
          "agent": {"text": "鸿胪寺", "agent_ent_ids": []}, "condition": "大典礼", "next": []},
     ], "confidence": 0.9},

    # ---------- 条18 六科封驳流程 ----------
    {"slot": 4, "item_id": "03-018", "name": "六科封驳章疏流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "凡制敕宣行，大事覆奏，小事署而颁之；有失，封还执奏",
          "agent": {"text": "六科都给事中", "agent_ent_ids": []}, "condition": "制敕宣行", "next": [2]},
         {"seq": 2, "text": "凡内外所上章疏下，分类抄出，参署付部，驳正其违误",
          "agent": {"text": "六科", "agent_ent_ids": []}, "condition": "章疏下", "next": [3]},
         {"seq": 3, "text": "凡吏部引选，则掌科同至御前请旨。外官领文凭，皆先赴科画字",
          "agent": {"text": "吏科掌科", "agent_ent_ids": []}, "condition": "吏部引选", "next": [4]},
         {"seq": 4, "text": "内外官考察自陈后，则与各科具奏。拾遗纠其不职者",
          "agent": {"text": "吏科", "agent_ent_ids": []}, "condition": "考察自陈", "next": []},
     ], "confidence": 0.92},

    # ---------- 条21 中书科书写诰敕流程 ----------
    {"slot": 5, "item_id": "03-021", "name": "中书科书写诰敕流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "掌书写诰敕、制诏、银册、铁券等事",
          "agent": {"text": "中书科舍人", "agent_ent_ids": []}, "condition": "未明", "next": [2]},
         {"seq": 2, "text": "凡草请诸翰林，宝请诸内府，左券及勘籍，归诸古今通集库",
          "agent": {"text": "中书科舍人", "agent_ent_ids": []}, "condition": "书写", "next": []},
     ], "confidence": 0.9},

    # ---------- 条23 行人司奉使流程 ----------
    {"slot": 6, "item_id": "03-023", "name": "行人司捧节奉使流程", "scope": "朝贡接待",
     "steps": [
         {"seq": 1, "text": "职专捧节、奉使之事。凡颁行诏赦，册封宗室，抚谕诸蕃，征聘贤才，与夫赏赐、慰问、赈济、军旅、祭祀，咸叙差焉",
          "agent": {"text": "行人司", "agent_ent_ids": []}, "condition": "奉使", "next": [2]},
         {"seq": 2, "text": "每岁朝审，则行人持节传旨法司，遣戍囚徒，送五府填精微册，批缴内府",
          "agent": {"text": "行人", "agent_ent_ids": []}, "condition": "每岁朝审", "next": []},
     ], "confidence": 0.9},

    # ---------- 条26 钦天监测候颁历流程 ----------
    {"slot": 7, "item_id": "03-026", "name": "钦天监测候颁历流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "掌察天文、定历数、占候、推步之事。凡日月、星辰、风云、气色，率其属而测候焉。有变异，密疏以闻",
          "agent": {"text": "钦天监监正、监副", "agent_ent_ids": []}, "condition": "测候", "next": [2]},
         {"seq": 2, "text": "每岁冬至日，呈奏明岁《大统历》，移送礼部颁行",
          "agent": {"text": "钦天监", "agent_ent_ids": []}, "condition": "每岁冬至日", "next": [3]},
         {"seq": 3, "text": "凡历注，御历注三十事，民历三十二事，壬遁历七十二事",
          "agent": {"text": "钦天监", "agent_ent_ids": []}, "condition": "历注", "next": [4]},
         {"seq": 4, "text": "凡祭日，前一年会选以进，移知太常。凡营建、征讨、冠婚、山陵之事，则选地而择日",
          "agent": {"text": "钦天监", "agent_ent_ids": []}, "condition": "择日", "next": []},
     ], "confidence": 0.9},

    # ---------- 条45 僧道管理流程 ----------
    {"slot": 8, "item_id": "03-045", "name": "僧道清理给牒流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "洪武元年，立善世、玄教二院。四年革。五年，给僧道度牒",
          "agent": {"text": "礼部", "agent_ent_ids": []}, "condition": "洪武初", "next": [2]},
         {"seq": 2, "text": "十五年，始置僧录司、道录司。僧凡三等：曰禅，曰讲，曰教。道凡二等：曰全真，曰正一",
          "agent": {"text": "僧录司、道录司", "agent_ent_ids": []}, "condition": "洪武十五年", "next": [3]},
         {"seq": 3, "text": "二十四年，清理释、道二教，限僧三年一度给牒。凡各府州县寺观，但存宽大者一所，并居之",
          "agent": {"text": "礼部", "agent_ent_ids": []}, "condition": "洪武二十四年", "next": []},
     ], "confidence": 0.9},

    # ---------- 条47 司礼监批红流程 ----------
    {"slot": 9, "item_id": "03-047", "name": "司礼监章奏批红流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "掌印掌理内外章奏及御前勘合",
          "agent": {"text": "司礼监掌印太监", "agent_ent_ids": []}, "condition": "章奏到", "next": [2]},
         {"seq": 2, "text": "秉笔、随堂掌章奏文书，照阁票批朱",
          "agent": {"text": "司礼监秉笔、随堂太监", "agent_ent_ids": []}, "condition": "阁票下", "next": [3]},
         {"seq": 3, "text": "提督掌督理皇城内一应仪礼刑名，及钤束长随、当差、听事各役，关防门禁，催督光禄供应等事",
          "agent": {"text": "司礼监提督太监", "agent_ent_ids": []}, "condition": "皇城事务", "next": []},
     ], "confidence": 0.88},
]
