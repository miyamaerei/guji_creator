# -*- coding: utf-8 -*-
"""
【卷04】L2 规则层源数据
纪律：编制行不抽；职掌陈述句不抽；仅"凡/掌…之政令/不得/毋/须"等规范句抽。
卷04 特色：地方行政职责类规则密集（府/州/县/儒学/巡检司/驿）。
"""
RULES = [
    # ============ 条2 南京吏部（南京特有考察规则）============
    {"slot": 1, "item_id": "04-002", "type": "程序型", "modals": ["procedure", "deadline"],
     "condition": "凡南京官，六年考察",
     "subject": {"text": "南京吏部考功", "subject_ent_ids": []},
     "action": "考功掌之，不由北吏部",
     "object": "南京官考察", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    # ============ 条4 总督粮储 ============
    {"slot": 1, "item_id": "04-004", "type": "程序型", "modals": ["procedure"],
     "condition": "嘉靖以前，特设都御史。二十六年革",
     "subject": {"text": "总督粮储", "subject_ent_ids": []},
     "action": "以户部右侍郎加都御史衔领之",
     "object": "粮储", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条6 南京兵部参赞机务 ============
    {"slot": 1, "item_id": "04-006", "type": "义务型", "modals": ["obligation"],
     "condition": "成化二十三年，始奉敕谕，专以本部尚书参赞机务",
     "subject": {"text": "南京兵部尚书", "subject_ent_ids": []},
     "action": "同内外守备官操练军马，抚恤人民，禁戢盗贼，振举庶务，故其职视五部为特重",
     "object": "南京机务", "purpose": "视五部为特重", "punishment": "未明", "confidence": 0.92},

    # ============ 条7 南京刑部职掌 ============
    {"slot": 1, "item_id": "04-007", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "南京刑部十三司", "subject_ent_ids": []},
     "action": "分掌南京诸司，及公、侯、伯、五府、京卫所刑名之事",
     "object": "南京刑名", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条10 提督操江 ============
    {"slot": 1, "item_id": "04-010", "type": "义务型", "modals": ["obligation"],
     "condition": "以副佥都御史为之",
     "subject": {"text": "提督操江", "subject_ent_ids": []},
     "action": "领上、下江防之事",
     "object": "上、下江防", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    # ============ 条11 南京通政使司 ============
    {"slot": 1, "item_id": "04-011", "type": "程序型", "modals": ["procedure"],
     "condition": "未明",
     "subject": {"text": "南京通政使司", "subject_ent_ids": []},
     "action": "掌收呈状，付刑部审理",
     "object": "呈状", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条29 王府长史职掌（重要条目）============
    {"slot": 1, "item_id": "04-029", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "王府长史", "subject_ent_ids": []},
     "action": "掌王府之政讼，辅相规讽以匡王失，率府僚各供乃事，而总其庶务焉",
     "object": "王府政讼", "purpose": "匡王失", "punishment": "未明", "confidence": 0.92},
    {"slot": 2, "item_id": "04-029", "type": "程序型", "modals": ["procedure"],
     "condition": "凡请名、请封、请婚、请恩泽，及陈谢、进献表启、书疏",
     "subject": {"text": "长史", "subject_ent_ids": []},
     "action": "长史为王奏上",
     "object": "王府奏请", "purpose": "未明", "punishment": "未明", "confidence": 0.92},
    {"slot": 3, "item_id": "04-029", "type": "处罚型", "modals": ["penalty"],
     "condition": "若王有过",
     "subject": {"text": "长史", "subject_ent_ids": []},
     "action": "则诘长史",
     "object": "王过", "purpose": "未明", "punishment": "诘", "confidence": 0.92},
    {"slot": 4, "item_id": "04-029", "type": "禁止型", "modals": ["prohibit"],
     "condition": "曾经过犯之人",
     "subject": {"text": "长史", "subject_ent_ids": []},
     "action": "毋得选用是职",
     "object": "长史选任", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 5, "item_id": "04-029", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "审理", "subject_ent_ids": []},
     "action": "掌推按刑狱，禁诘横暴，无干国纪",
     "object": "王府刑狱", "purpose": "无干国纪", "punishment": "未明", "confidence": 0.9},
    {"slot": 6, "item_id": "04-029", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "教授", "subject_ent_ids": []},
     "action": "掌以德义迪王，校勘经籍。凡宗室年十岁以上，入宗学，教授与纪善为之师",
     "object": "王府教育", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 7, "item_id": "04-029", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "典膳", "subject_ent_ids": []},
     "action": "掌祭祀、宾客，王若妃之膳羞",
     "object": "王府膳食", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条32 布政使职掌（省级核心）============
    {"slot": 1, "item_id": "04-032", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "布政使", "subject_ent_ids": []},
     "action": "掌一省之政，朝廷有德泽、禁令，承流宣播，以下于有司",
     "object": "一省之政", "purpose": "承流宣播", "punishment": "未明", "confidence": 0.92},
    {"slot": 2, "item_id": "04-032", "type": "程序型", "modals": ["procedure", "deadline"],
     "condition": "凡僚属满秩",
     "subject": {"text": "布政使", "subject_ent_ids": []},
     "action": "廉其称职、不称职，上下其考，报抚、按以达于吏部、都察院",
     "object": "僚属考课", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    # ============ 条35 按察使职掌 ============
    {"slot": 1, "item_id": "04-035", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "按察使", "subject_ent_ids": []},
     "action": "掌一省刑名按劾之事。纠官邪，戢奸暴，平狱讼，雪冤抑，以振扬风纪，而澄清其吏治",
     "object": "一省刑名按劾", "purpose": "振扬风纪，澄清吏治", "punishment": "未明", "confidence": 0.92},
    {"slot": 2, "item_id": "04-035", "type": "程序型", "modals": ["procedure"],
     "condition": "大者暨都、布二司会议",
     "subject": {"text": "按察使", "subject_ent_ids": []},
     "action": "告抚、按，以听于（部院）",
     "object": "重大政务", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条55 知府职掌（地方核心）============
    {"slot": 1, "item_id": "04-055", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "知府", "subject_ent_ids": []},
     "action": "掌一府之政，宣风化，平狱讼，均赋役，以教养百姓",
     "object": "一府之政", "purpose": "以教养百姓", "punishment": "未明", "confidence": 0.92},
    {"slot": 2, "item_id": "04-055", "type": "程序型", "modals": ["procedure", "deadline"],
     "condition": "每三岁",
     "subject": {"text": "知府", "subject_ent_ids": []},
     "action": "察属吏之贤否，上下其考，以达于省，上吏部",
     "object": "属吏考课", "purpose": "未明", "punishment": "未明", "confidence": 0.92},
    {"slot": 3, "item_id": "04-055", "type": "程序型", "modals": ["procedure"],
     "condition": "凡朝贺、吊祭",
     "subject": {"text": "知府", "subject_ent_ids": []},
     "action": "视布政使（之仪）",
     "object": "朝贺吊祭", "purpose": "未明", "punishment": "未明", "confidence": 0.85},

    # ============ 条58 知州职掌 ============
    {"slot": 1, "item_id": "04-058", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "知州", "subject_ent_ids": []},
     "action": "掌一州之政。凡州二：有属州，有直隶州。属州视县，直隶州视府，而品秩则同",
     "object": "一州之政", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 2, "item_id": "04-058", "type": "程序型", "modals": ["procedure"],
     "condition": "同知、判官",
     "subject": {"text": "同知、判官", "subject_ent_ids": []},
     "action": "俱视其事州之繁简，以供厥职",
     "object": "州务", "purpose": "未明", "punishment": "未明", "confidence": 0.88},

    # ============ 条60 知县职掌 ============
    {"slot": 1, "item_id": "04-060", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "知县", "subject_ent_ids": []},
     "action": "掌一县之政",
     "object": "一县之政", "purpose": "未明", "punishment": "未明", "confidence": 0.92},
    {"slot": 2, "item_id": "04-060", "type": "程序型", "modals": ["procedure", "deadline"],
     "condition": "凡赋役，岁会实征，十年造黄册，以丁产为差",
     "subject": {"text": "知县", "subject_ent_ids": []},
     "action": "赋有金谷、布帛及诸货物之赋，役有力役、雇役、借债不时之役，皆视天时（休咎，地利丰耗，人力贫富，调剂而均节之）",
     "object": "赋役", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条62 儒学教官职掌 ============
    {"slot": 1, "item_id": "04-062", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "教授、学正、教谕", "subject_ent_ids": []},
     "action": "掌教诲所属生员，训导佐之",
     "object": "生员", "purpose": "未明", "punishment": "未明", "confidence": 0.92},
    {"slot": 2, "item_id": "04-062", "type": "义务型", "modals": ["obligation"],
     "condition": "凡学政遵卧碑，咸听于提学宪臣提调，府听于府，州听于州，县听于县",
     "subject": {"text": "儒学官", "subject_ent_ids": []},
     "action": "月课士子之艺业而奖励之。其殿最视乡举之有无多寡",
     "object": "学政", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条64 巡检司职掌 ============
    {"slot": 1, "item_id": "04-064", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "巡检、副巡检", "subject_ent_ids": []},
     "action": "主缉捕盗贼，盘诘奸伪。凡在外各府州县关津要害处俱设，俾率徭役弓兵警备不虞",
     "object": "关津要害", "purpose": "警备不虞", "punishment": "未明", "confidence": 0.92},

    # ============ 条65 驿丞职掌 ============
    {"slot": 1, "item_id": "04-065", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "驿丞", "subject_ent_ids": []},
     "action": "典邮传迎送之事。凡舟车、夫马、廪糗、庖馔、裯帐，视使客之品秩，仆夫之多寡，而谨供应之。支直于府若州县，而籍其出入",
     "object": "邮传迎送", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    # ============ 条66 税课司职掌 ============
    {"slot": 1, "item_id": "04-066", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "税课司大使", "subject_ent_ids": []},
     "action": "典税事。凡商贾、僧屠、杂市，皆有常征，以时榷而输其直于府若县",
     "object": "商税", "purpose": "未明", "punishment": "未明", "confidence": 0.92},
    {"slot": 2, "item_id": "04-066", "type": "程序型", "modals": ["procedure"],
     "condition": "凡民间贸田宅",
     "subject": {"text": "税课司", "subject_ent_ids": []},
     "action": "必操契券请印，乃得收户，则征其直百之三",
     "object": "田宅交易税", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条69 河泊所 / 闸坝官 ============
    {"slot": 1, "item_id": "04-069", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "河泊所官", "subject_ent_ids": []},
     "action": "掌收鱼税",
     "object": "鱼税", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 2, "item_id": "04-069", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "闸官、坝官", "subject_ent_ids": []},
     "action": "掌启闭蓄泄",
     "object": "闸坝", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 3, "item_id": "04-069", "type": "程序型", "modals": ["procedure"],
     "condition": "岁课粮五千石以上至万石者，设官三人；千石以（上者二人）",
     "subject": {"text": "河泊所", "subject_ent_ids": []},
     "action": "（按课额定员）",
     "object": "河泊所设官", "purpose": "未明", "punishment": "未明", "confidence": 0.88},

    # ============ 条70 批验所职掌 ============
    {"slot": 1, "item_id": "04-070", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "批验所", "subject_ent_ids": []},
     "action": "掌验茶盐引",
     "object": "茶盐引", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    # ============ 条71 递运所职掌 ============
    {"slot": 1, "item_id": "04-071", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "递运所", "subject_ent_ids": []},
     "action": "掌运递粮物",
     "object": "运递粮物", "purpose": "未明", "punishment": "未明", "confidence": 0.92},
    {"slot": 2, "item_id": "04-071", "type": "程序型", "modals": ["procedure"],
     "condition": "先是，在外多以卫所戍守军士传送军囚，太祖以其有妨练习守御",
     "subject": {"text": "兵部", "subject_ent_ids": []},
     "action": "乃命兵部增置（递运所）",
     "object": "递运", "purpose": "不妨练习守御", "punishment": "未明", "confidence": 0.88},

    # ============ 条51 市舶提举司职掌 ============
    {"slot": 1, "item_id": "04-051", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "市舶提举司", "subject_ent_ids": []},
     "action": "掌海外诸蕃朝贡市易之事，辨其使人表文勘合之真伪",
     "object": "海外朝贡市易", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    # ============ 条53 茶马司职掌 ============
    {"slot": 1, "item_id": "04-053", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "茶马司", "subject_ent_ids": []},
     "action": "掌市马之事",
     "object": "市马", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    # ============ 条48 都转运使职掌 ============
    {"slot": 1, "item_id": "04-048", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "都转运使", "subject_ent_ids": []},
     "action": "掌盐监之事。同知、副判分司之",
     "object": "盐政", "purpose": "未明", "punishment": "未明", "confidence": 0.92},
]
