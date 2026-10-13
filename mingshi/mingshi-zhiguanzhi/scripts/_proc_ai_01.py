# -*- coding: utf-8 -*-
"""
【开发验证切片】L3 流程层源数据 —— 卷01
本书四类流程：选官 / 考察 / 封赠荫叙 / 朝贡接待。本切片覆盖前三类。
不建 state_machine（本书时序为散点，判"点不是线"）；不写 events（未启用事件层）。
"""

PROCS = [
    # ---------- 吏部文选司选官流程（条12）----------
    {"slot": 1, "item_id": "01-012", "name": "吏部文选司选官流程", "scope": "选官",
     "steps": [
         {"seq": 1, "text": "凡选，每岁有大选，有急选，有远方选，有岁贡就教选，间有拣选，有举人乞恩选",
          "agent": {"text": "文选司郎中", "agent_ent_ids": []}, "condition": "每岁", "next": [2]},
         {"seq": 2, "text": "选人或登资簿，厘其流品，平其铨注，而序迁之",
          "agent": {"text": "文选司郎中", "agent_ent_ids": []}, "condition": "未明", "next": [3]},
         {"seq": 3, "text": "凡升必考满；若员缺当补，不待考满，曰推升。类推上一人，单推上二人",
          "agent": {"text": "文选司郎中", "agent_ent_ids": []}, "condition": "员缺当补", "next": [4]},
         {"seq": 4, "text": "三品以上，九卿及佥都御史、祭酒，廷推上二人或三人；内阁，吏、兵二部尚书，廷推上二人",
          "agent": {"text": "吏部", "agent_ent_ids": []}, "condition": "三品以上", "next": []},
         {"seq": 5, "text": "以署职、试职、实授奠年资，以开设、裁并、兼摄适繁简",
          "agent": {"text": "文选司郎中", "agent_ent_ids": []}, "condition": "未明", "next": []},
     ], "confidence": 0.92},

    # ---------- 吏部考功司考察流程（条15）----------
    {"slot": 2, "item_id": "01-015", "name": "吏部考功司考课黜陟流程", "scope": "考察",
     "steps": [
         {"seq": 1, "text": "凡内外官给由，三年初考",
          "agent": {"text": "考功司郎中", "agent_ent_ids": []}, "condition": "三年", "next": [2]},
         {"seq": 2, "text": "六年再考，并引请",
          "agent": {"text": "考功司郎中", "agent_ent_ids": []}, "condition": "六年", "next": [3]},
         {"seq": 3, "text": "九年通考，奏请综其称职、平常、不称职而陟黜之",
          "agent": {"text": "考功司郎中", "agent_ent_ids": []}, "condition": "九年", "next": [4]},
         {"seq": 4, "text": "陟无过二等，降无过三等，其甚者黜之、罪之",
          "agent": {"text": "考功司郎中", "agent_ent_ids": []}, "condition": "考满", "next": []},
     ], "confidence": 0.95},

    {"slot": 3, "item_id": "01-015", "name": "京官六年一察流程", "scope": "考察",
     "steps": [
         {"seq": 1, "text": "京官六年一察，察以巳、亥年",
          "agent": {"text": "考功司郎中", "agent_ent_ids": []}, "condition": "巳、亥年", "next": [2]},
         {"seq": 2, "text": "五品下考察其不职者，降罚有差",
          "agent": {"text": "考功司郎中", "agent_ent_ids": []}, "condition": "五品以下", "next": []},
         {"seq": 3, "text": "四品上自陈，去留取旨",
          "agent": {"text": "考功司郎中", "agent_ent_ids": []}, "condition": "四品以上", "next": []},
     ], "confidence": 0.92},

    {"slot": 4, "item_id": "01-015", "name": "外官三年一朝考察流程", "scope": "考察",
     "steps": [
         {"seq": 1, "text": "外官三年一朝，朝以辰、戌、丑、未年",
          "agent": {"text": "考功司郎中", "agent_ent_ids": []}, "condition": "辰、戌、丑、未年", "next": [2]},
         {"seq": 2, "text": "前期移抚、按官，各综其属三年内功过状注考",
          "agent": {"text": "抚、按官", "agent_ent_ids": []}, "condition": "朝觐前期", "next": [3]},
         {"seq": 3, "text": "汇送覆核以定黜陟",
          "agent": {"text": "考功司郎中", "agent_ent_ids": []}, "condition": "未明", "next": []},
     ], "confidence": 0.92},

    # ---------- 吏部验封司封赠荫叙流程（条13）----------
    {"slot": 5, "item_id": "01-013", "name": "验封司封爵给券流程", "scope": "封赠荫叙",
     "steps": [
         {"seq": 1, "text": "凡爵非社稷军功不得封，封号非特旨不得与",
          "agent": {"text": "验封司郎中", "agent_ent_ids": []}, "condition": "封爵", "next": [2]},
         {"seq": 2, "text": "或世或不世，皆给诰券。凡券，左右各一，左藏内府，右给功臣之家",
          "agent": {"text": "验封司郎中", "agent_ent_ids": []}, "condition": "给券", "next": [3]},
         {"seq": 3, "text": "袭封则征其诰券，稽其功过，核其宗支，以第其世流降除之等",
          "agent": {"text": "验封司郎中", "agent_ent_ids": []}, "condition": "袭封", "next": []},
     ], "confidence": 0.92},

    {"slot": 6, "item_id": "01-013", "name": "验封司荫叙流程", "scope": "封赠荫叙",
     "steps": [
         {"seq": 1, "text": "明初，自一品至七品，皆得荫一子以世其禄（洪武十六年定职官子孙荫叙）",
          "agent": {"text": "验封司郎中", "agent_ent_ids": []}, "condition": "明初", "next": [2]},
         {"seq": 2, "text": "后乃渐为限制，京官三品以上，考满著绩，始荫一子曰官生",
          "agent": {"text": "验封司郎中", "agent_ent_ids": []}, "condition": "后渐限制", "next": []},
         {"seq": 3, "text": "其出自特恩者曰恩生",
          "agent": {"text": "验封司郎中", "agent_ent_ids": []}, "condition": "特恩", "next": []},
     ], "confidence": 0.9},

    {"slot": 7, "item_id": "01-013", "name": "验封司封赠流程", "scope": "封赠荫叙",
     "steps": [
         {"seq": 1, "text": "凡封赠，公、侯、伯之追封，皆递进一等",
          "agent": {"text": "验封司郎中", "agent_ent_ids": []}, "condition": "追封", "next": [2]},
         {"seq": 2, "text": "三品以上政绩显异及死谏、死节、阵亡者，皆得赠官",
          "agent": {"text": "验封司郎中", "agent_ent_ids": []}, "condition": "三品以上显异", "next": [3]},
         {"seq": 3, "text": "其见任则初授散阶，京官满一考，及外官满一考而以最闻者，皆给本身诰敕",
          "agent": {"text": "验封司郎中", "agent_ent_ids": []}, "condition": "考满", "next": [4]},
         {"seq": 4, "text": "七品以上皆得推恩其先。五品以上授诰命，六品以下授敕命",
          "agent": {"text": "验封司郎中", "agent_ent_ids": []}, "condition": "推恩", "next": []},
     ], "confidence": 0.9},

    # ---------- 稽勋司勋级授给流程（条14）----------
    {"slot": 8, "item_id": "01-014", "name": "稽勋司授勋流程", "scope": "封赠荫叙",
     "steps": [
         {"seq": 1, "text": "凡文勋十（正一品左、右柱国…从五品协正庶尹）",
          "agent": {"text": "稽勋司郎中", "agent_ent_ids": []}, "condition": "未明", "next": [2]},
         {"seq": 2, "text": "自五品以上，历再考，乃授勋",
          "agent": {"text": "稽勋司郎中", "agent_ent_ids": []}, "condition": "五品以上历再考", "next": []},
     ], "confidence": 0.9},
]
