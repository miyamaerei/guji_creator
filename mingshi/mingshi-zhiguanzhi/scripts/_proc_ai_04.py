# -*- coding: utf-8 -*-
"""【卷04】L3 流程层源数据 —— 地方行政职责链"""

PROCS = [
    # ---------- 条32 布政使考课流程 ----------
    {"slot": 1, "item_id": "04-032", "name": "布政使承流宣播流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "掌一省之政，朝廷有德泽、禁令，承流宣播，以下于有司",
          "agent": {"text": "布政使", "agent_ent_ids": []}, "condition": "朝廷政令下", "next": [2]},
         {"seq": 2, "text": "凡僚属满秩，廉其称职、不称职，上下其考",
          "agent": {"text": "布政使", "agent_ent_ids": []}, "condition": "僚属满秩", "next": [3]},
         {"seq": 3, "text": "报抚、按以达于吏部、都察院",
          "agent": {"text": "布政使", "agent_ent_ids": []}, "condition": "考课上报", "next": []},
     ], "confidence": 0.92},

    # ---------- 条55 知府考课流程 ----------
    {"slot": 2, "item_id": "04-055", "name": "知府考课属吏流程", "scope": "考察",
     "steps": [
         {"seq": 1, "text": "掌一府之政，宣风化，平狱讼，均赋役，以教养百姓",
          "agent": {"text": "知府", "agent_ent_ids": []}, "condition": "未明", "next": [2]},
         {"seq": 2, "text": "每三岁，察属吏之贤否，上下其考",
          "agent": {"text": "知府", "agent_ent_ids": []}, "condition": "每三岁", "next": [3]},
         {"seq": 3, "text": "以达于省，上吏部",
          "agent": {"text": "知府", "agent_ent_ids": []}, "condition": "考课上达", "next": []},
     ], "confidence": 0.92},

    # ---------- 条60 知县赋役流程 ----------
    {"slot": 3, "item_id": "04-060", "name": "知县赋役征派流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "掌一县之政。凡赋役，岁会实征，十年造黄册，以丁产为差",
          "agent": {"text": "知县", "agent_ent_ids": []}, "condition": "每岁/十年", "next": [2]},
         {"seq": 2, "text": "赋有金谷、布帛及诸货物之赋，役有力役、雇役、借债不时之役",
          "agent": {"text": "知县", "agent_ent_ids": []}, "condition": "赋役分类", "next": [3]},
         {"seq": 3, "text": "皆视天时（休咎，地利丰耗，人力贫富，调剂而均节之）",
          "agent": {"text": "知县", "agent_ent_ids": []}, "condition": "调剂", "next": []},
     ], "confidence": 0.9},

    # ---------- 条35 按察使刑名按劾流程 ----------
    {"slot": 4, "item_id": "04-035", "name": "按察使刑名按劾流程", "scope": "考察",
     "steps": [
         {"seq": 1, "text": "掌一省刑名按劾之事",
          "agent": {"text": "按察使", "agent_ent_ids": []}, "condition": "未明", "next": [2]},
         {"seq": 2, "text": "纠官邪，戢奸暴，平狱讼，雪冤抑，以振扬风纪，而澄清其吏治",
          "agent": {"text": "按察使", "agent_ent_ids": []}, "condition": "按劾", "next": [3]},
         {"seq": 3, "text": "大者暨都、布二司会议，告抚、按，以听于（部院）",
          "agent": {"text": "按察使", "agent_ent_ids": []}, "condition": "大事会议", "next": []},
     ], "confidence": 0.92},

    # ---------- 条29 王府长史奏请流程 ----------
    {"slot": 5, "item_id": "04-029", "name": "王府长史奏请流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "掌王府之政讼，辅相规讽以匡王失，率府僚各供乃事，而总其庶务焉",
          "agent": {"text": "长史", "agent_ent_ids": []}, "condition": "未明", "next": [2]},
         {"seq": 2, "text": "凡请名、请封、请婚、请恩泽，及陈谢、进献表启、书疏，长史为王奏上",
          "agent": {"text": "长史", "agent_ent_ids": []}, "condition": "王府奏请", "next": [3]},
         {"seq": 3, "text": "若王有过，则诘长史",
          "agent": {"text": "长史", "agent_ent_ids": []}, "condition": "王有过", "next": []},
     ], "confidence": 0.92},

    # ---------- 条62 儒学教诲流程 ----------
    {"slot": 6, "item_id": "04-062", "name": "儒学教诲考课流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "教授、学正、教谕，掌教诲所属生员，训导佐之",
          "agent": {"text": "教授/学正/教谕", "agent_ent_ids": []}, "condition": "未明", "next": [2]},
         {"seq": 2, "text": "凡生员廪膳、增广，府学四十人，州学三十人，县学二十人，附学生无定数",
          "agent": {"text": "儒学官", "agent_ent_ids": []}, "condition": "生员额数", "next": [3]},
         {"seq": 3, "text": "儒学官月课士子之艺业而奖励之。凡学政遵卧碑，咸听于提学宪臣提调",
          "agent": {"text": "儒学官", "agent_ent_ids": []}, "condition": "月课", "next": [4]},
         {"seq": 4, "text": "其殿最视乡举之有无多寡",
          "agent": {"text": "提学宪臣", "agent_ent_ids": []}, "condition": "岁考殿最", "next": []},
     ], "confidence": 0.9},

    # ---------- 条64 巡检司缉捕流程 ----------
    {"slot": 7, "item_id": "04-064", "name": "巡检司缉捕警备流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "主缉捕盗贼，盘诘奸伪",
          "agent": {"text": "巡检、副巡检", "agent_ent_ids": []}, "condition": "关津要害", "next": [2]},
         {"seq": 2, "text": "凡在外各府州县关津要害处俱设，俾率徭役弓兵警备不虞",
          "agent": {"text": "巡检", "agent_ent_ids": []}, "condition": "警备", "next": []},
     ], "confidence": 0.9},

    # ---------- 条65 驿丞迎送流程 ----------
    {"slot": 8, "item_id": "04-065", "name": "驿丞邮传迎送流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "典邮传迎送之事",
          "agent": {"text": "驿丞", "agent_ent_ids": []}, "condition": "使客至", "next": [2]},
         {"seq": 2, "text": "凡舟车、夫马、廪糗、庖馔、裯帐，视使客之品秩，仆夫之多寡，而谨供应之",
          "agent": {"text": "驿丞", "agent_ent_ids": []}, "condition": "按品秩供应", "next": [3]},
         {"seq": 3, "text": "支直于府若州县，而籍其出入",
          "agent": {"text": "驿丞", "agent_ent_ids": []}, "condition": "支销登记", "next": []},
     ], "confidence": 0.92},

    # ---------- 条66 税课司征税流程 ----------
    {"slot": 9, "item_id": "04-066", "name": "税课司征税流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "典税事。凡商贾、僧屠、杂市，皆有常征",
          "agent": {"text": "税课司大使", "agent_ent_ids": []}, "condition": "商贾交易", "next": [2]},
         {"seq": 2, "text": "以时榷而输其直于府若县",
          "agent": {"text": "税课司大使", "agent_ent_ids": []}, "condition": "按时榷征", "next": [3]},
         {"seq": 3, "text": "凡民间贸田宅，必操契券请印，乃得收户，则征其直百之三",
          "agent": {"text": "税课司", "agent_ent_ids": []}, "condition": "田宅交易", "next": []},
     ], "confidence": 0.9},

    # ---------- 条71 递运所运递流程 ----------
    {"slot": 10, "item_id": "04-071", "name": "递运所运递粮物流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "掌运递粮物",
          "agent": {"text": "递运所大使", "agent_ent_ids": []}, "condition": "粮物待运", "next": [2]},
         {"seq": 2, "text": "洪武九年始置。先是，在外多以卫所戍守军士传送军囚，太祖以其有妨练习守御",
          "agent": {"text": "兵部", "agent_ent_ids": []}, "condition": "妨守御", "next": [3]},
         {"seq": 3, "text": "乃命兵部增置（递运所）",
          "agent": {"text": "兵部", "agent_ent_ids": []}, "condition": "增置", "next": []},
     ], "confidence": 0.88},
]
