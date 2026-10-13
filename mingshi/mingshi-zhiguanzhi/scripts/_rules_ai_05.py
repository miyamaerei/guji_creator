# -*- coding: utf-8 -*-
"""
【卷05】L2 规则层源数据
纪律：编制行不抽；职掌陈述句不抽；仅"凡/掌…之政令/不得/毋/须"等规范句抽。
卷05 特色：军政纪律类规则密集（卫所世袭/袭替/考选/军法/土司承袭/朝贡约束）。
"""
RULES = [
    # ============ 条1 公侯伯勋爵（封赠荫叙）============
    {"slot": 1, "item_id": "05-001", "type": "程序型", "modals": ["procedure"],
     "condition": "凡爵非社稷军功不得封",
     "subject": {"text": "吏部验封", "subject_ent_ids": []},
     "action": "封拜非社稷军功不得封，授爵止其身，非特恩不给世券",
     "object": "公侯伯勋爵", "purpose": "重军功", "punishment": "未明", "confidence": 0.93},

    {"slot": 2, "item_id": "05-001", "type": "义务型", "modals": ["obligation"],
     "condition": "凡铁券",
     "subject": {"text": "受券者", "subject_ent_ids": []},
     "action": "第一面镌其本身及父祖名，第二面镌本身免死之数，子免死之数，以别其功之大小",
     "object": "铁券", "purpose": "别功之大小", "punishment": "未明", "confidence": 0.9},

    {"slot": 3, "item_id": "05-001", "type": "优先级型", "modals": ["priority"],
     "condition": "驸马都尉位在伯上",
     "subject": {"text": "驸马都尉", "subject_ent_ids": []},
     "action": "位在伯上，仪宾不与",
     "object": "勋爵位次", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条2 勋爵袭替 ============
    {"slot": 1, "item_id": "05-002", "type": "程序型", "modals": ["procedure"],
     "condition": "凡袭替",
     "subject": {"text": "吏部验封司", "subject_ent_ids": []},
     "action": "先核实，乃许袭，非军功不得封，非特恩不给世券",
     "object": "勋爵袭替", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条3 五军都督府职掌（核心）============
    {"slot": 1, "item_id": "05-003", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "五军都督府", "subject_ent_ids": []},
     "action": "掌军旅之事，各领其都司、卫所，以达于兵部",
     "object": "军旅之事", "purpose": "未明", "punishment": "未明", "confidence": 0.95},

    {"slot": 2, "item_id": "05-003", "type": "程序型", "modals": ["procedure"],
     "condition": "凡武职",
     "subject": {"text": "五军都督府", "subject_ent_ids": []},
     "action": "凡武职，世官流官、土官袭替、优给、优养，及所属军政，掌印、佥事报都指挥使司，达所隶都督府，移兵部",
     "object": "武职世官流官", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    {"slot": 3, "item_id": "05-003", "type": "优先级型", "modals": ["priority"],
     "condition": "凡朝廷有大征讨",
     "subject": {"text": "五军都督府", "subject_ent_ids": []},
     "action": "命将出师，则五府合推一人为将，兵部覆奏，请旨点用",
     "object": "命将出师", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    {"slot": 4, "item_id": "05-003", "type": "程序型", "modals": ["procedure"],
     "condition": "凡武职官犯罪",
     "subject": {"text": "五军都督府", "subject_ent_ids": []},
     "action": "凡武职官犯罪，与兵部、法司会问，其情轻者，径自提问，重者奏请",
     "object": "武职官犯罪", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条4 五军都督府分职 ============
    {"slot": 1, "item_id": "05-004", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "中军都督府", "subject_ent_ids": []},
     "action": "掌中军，统辖在京留守等卫，及在外某都司、卫所",
     "object": "中军军政", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条5 五军都督府沿革（规则较少，只抽世袭相关）============
    {"slot": 1, "item_id": "05-005", "type": "禁止型", "modals": ["prohibit"],
     "condition": "未明",
     "subject": {"text": "京卫", "subject_ent_ids": []},
     "action": "惟锦衣等亲军、上直卫不隶五府",
     "object": "亲军卫", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条6 京营（团营）============
    {"slot": 1, "item_id": "05-006", "type": "程序型", "modals": ["procedure"],
     "condition": "凡团营，先以五十人为一队，队长统之",
     "subject": {"text": "京营提督", "subject_ent_ids": []},
     "action": "择三大营精锐分团营，营以武臣一人统之，文臣一人提督之",
     "object": "团营操练", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条8 京卫 ============
    {"slot": 1, "item_id": "05-008", "type": "义务型", "modals": ["obligation"],
     "condition": "凡上直卫亲军指挥使司",
     "subject": {"text": "上直卫", "subject_ent_ids": []},
     "action": "番上宿卫名亲军，以护宫禁，不隶五都督府",
     "object": "宫禁宿卫", "purpose": "护宫禁", "punishment": "未明", "confidence": 0.95},

    # ============ 条9 亲军卫沿革 ============
    {"slot": 1, "item_id": "05-009", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "锦衣卫", "subject_ent_ids": []},
     "action": "主巡察、缉捕、理诏狱，以都督、都指挥领之",
     "object": "诏狱缉捕", "purpose": "特异于诸卫", "punishment": "未明", "confidence": 0.93},

    {"slot": 2, "item_id": "05-009", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "留守卫", "subject_ent_ids": []},
     "action": "专领军马守御各城门，及巡警皇城与城垣造作之事",
     "object": "城门守御", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条10 锦衣卫（核心）============
    {"slot": 1, "item_id": "05-010", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "锦衣卫", "subject_ent_ids": []},
     "action": "掌侍卫、缉捕、刑狱之事，恒以勋戚都督领之，恩荫寄禄无常员",
     "object": "侍卫缉捕刑狱", "purpose": "未明", "punishment": "未明", "confidence": 0.95},

    {"slot": 2, "item_id": "05-010", "type": "义务型", "modals": ["obligation"],
     "condition": "凡朝会、巡幸",
     "subject": {"text": "锦衣卫", "subject_ent_ids": []},
     "action": "具卤簿仪仗，率大汉将军等侍从扈行；宿卫则分番入直",
     "object": "卤簿仪仗扈行", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    {"slot": 3, "item_id": "05-010", "type": "义务型", "modals": ["obligation"],
     "condition": "凡承制鞫狱录囚勘事",
     "subject": {"text": "锦衣卫", "subject_ent_ids": []},
     "action": "偕三法司；五军官舍比试并枪，同兵部莅视",
     "object": "鞫狱录囚", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    {"slot": 4, "item_id": "05-010", "type": "义务型", "modals": ["obligation"],
     "condition": "盗贼奸宄，街途沟洫",
     "subject": {"text": "锦衣卫", "subject_ent_ids": []},
     "action": "密缉而时省之",
     "object": "京师缉捕", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条11 锦衣卫沿革 ============
    {"slot": 1, "item_id": "05-011", "type": "处罚型", "modals": ["penalty"],
     "condition": "洪武二十年，以治锦衣卫者多非法凌虐",
     "subject": {"text": "太祖", "subject_ent_ids": []},
     "action": "焚刑具，出系囚，送刑部审录，诏内外狱咸归三法司，罢锦衣狱",
     "object": "锦衣狱", "purpose": "惩非法凌虐", "punishment": "罢锦衣狱", "confidence": 0.95},

    {"slot": 2, "item_id": "05-011", "type": "程序型", "modals": ["procedure"],
     "condition": "成化间，刻印畀之",
     "subject": {"text": "北镇抚司", "subject_ent_ids": []},
     "action": "狱成得专达，不关白锦衣，锦衣官亦不得干预",
     "object": "诏狱", "purpose": "专治诏狱", "punishment": "未明", "confidence": 0.93},

    # ============ 条12 南京守备 ============
    {"slot": 1, "item_id": "05-012", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "南京守备", "subject_ent_ids": []},
     "action": "掌南京一切留守、防护之事，以公、侯、伯充之",
     "object": "南京留守防护", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    # ============ 条13 协同守备 ============
    {"slot": 1, "item_id": "05-013", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "协同守备", "subject_ent_ids": []},
     "action": "协同守备，掌同守备，以侯、伯、都督充之",
     "object": "南京守备", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条14 南京五军都督府 ============
    {"slot": 1, "item_id": "05-014", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "南京五军都督府", "subject_ent_ids": []},
     "action": "分掌南京卫所，以达于南京兵部",
     "object": "南京卫所", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条15 南京京营 ============
    {"slot": 1, "item_id": "05-015", "type": "义务型", "modals": ["obligation"],
     "condition": "凡管领大教场及江上操备等事",
     "subject": {"text": "南京五府", "subject_ent_ids": []},
     "action": "各府奉敕分掌之；城门之管钥，中府专掌之",
     "object": "南京操备", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条16 南京京卫 ============
    {"slot": 1, "item_id": "05-016", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "南京京卫", "subject_ent_ids": []},
     "action": "掌守卫南京皇城、城门及巡警之事",
     "object": "南京守卫", "purpose": "未明", "punishment": "未明", "confidence": 0.88},

    # ============ 条17 南京五军都督府职掌 ============
    {"slot": 1, "item_id": "05-017", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "南京五军都督府", "subject_ent_ids": []},
     "action": "掌南京卫所之政，凡军旅之事，受成于南京兵部",
     "object": "南京卫所之政", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条18 王府护卫（核心）============
    {"slot": 1, "item_id": "05-018", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "王府护卫", "subject_ent_ids": []},
     "action": "掌防御非常，护卫王邸；有征调，则听命于朝",
     "object": "王府护卫", "purpose": "未明", "punishment": "未明", "confidence": 0.93},

    {"slot": 2, "item_id": "05-018", "type": "禁止型", "modals": ["prohibit"],
     "condition": "王府护卫有征调",
     "subject": {"text": "王府护卫", "subject_ent_ids": []},
     "action": "不得擅调，必听命于朝",
     "object": "护卫征调", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条20 王府仪卫司 ============
    {"slot": 1, "item_id": "05-020", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "王府仪卫司", "subject_ent_ids": []},
     "action": "仪卫，掌侍卫仪仗；护卫，掌防御非常，护卫王邸",
     "object": "王府仪卫", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    # ============ 条21 总兵官（核心）============
    {"slot": 1, "item_id": "05-021", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "总兵官", "subject_ent_ids": []},
     "action": "总镇一方，率其属以听所命主帅调度，凡军务皆专断之",
     "object": "一方军务", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    {"slot": 2, "item_id": "05-021", "type": "程序型", "modals": ["procedure"],
     "condition": "凡总兵官，旧用公、侯、伯，后以都督、佥事充之",
     "subject": {"text": "总兵官", "subject_ent_ids": []},
     "action": "遇有征战，则挂印充总兵官，事平还印",
     "object": "挂印出征", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条22 副总兵 ============
    {"slot": 1, "item_id": "05-022", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "副总兵", "subject_ent_ids": []},
     "action": "协守、分守，各掌其地之防守，听总兵官节制",
     "object": "防守", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条23 参将 ============
    {"slot": 1, "item_id": "05-023", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "参将", "subject_ent_ids": []},
     "action": "分守各路城堡，听总兵官调度",
     "object": "分守城堡", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条24 游击将军 ============
    {"slot": 1, "item_id": "05-024", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "游击将军", "subject_ent_ids": []},
     "action": "统领游兵，往来策应，听总兵官调度",
     "object": "游兵策应", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条25 守备 ============
    {"slot": 1, "item_id": "05-025", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "守备", "subject_ent_ids": []},
     "action": "守御城堡，听参将、总兵官节制",
     "object": "城堡守御", "purpose": "未明", "punishment": "未明", "confidence": 0.88},

    # ============ 条26 把总 ============
    {"slot": 1, "item_id": "05-026", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "把总", "subject_ent_ids": []},
     "action": "分领兵卒，听守备、参将调度",
     "object": "兵卒", "purpose": "未明", "punishment": "未明", "confidence": 0.88},

    # ============ 条45 总督漕运总兵官 ============
    {"slot": 1, "item_id": "05-045", "type": "义务型", "modals": ["obligation"],
     "condition": "永乐二年，设总兵、副总兵，统领官军海运。后海运罢",
     "subject": {"text": "总督漕运总兵官", "subject_ent_ids": []},
     "action": "专督漕运；天顺元年又令兼理河道",
     "object": "漕运", "purpose": "未明", "punishment": "未明", "confidence": 0.93},

    # ============ 条46 留守司 ============
    {"slot": 1, "item_id": "05-046", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "留守司", "subject_ent_ids": []},
     "action": "掌中都、兴都守御防护之事",
     "object": "中都兴都防护", "purpose": "未明", "punishment": "未明", "confidence": 0.93},

    # ============ 条48 都司（核心）============
    {"slot": 1, "item_id": "05-048", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "都指挥使司", "subject_ent_ids": []},
     "action": "掌一方之军政，率其卫所以隶于五府，而听于兵部",
     "object": "一方军政", "purpose": "未明", "punishment": "未明", "confidence": 0.95},

    {"slot": 2, "item_id": "05-048", "type": "程序型", "modals": ["procedure"],
     "condition": "凡朝廷遣将征讨",
     "subject": {"text": "都司", "subject_ent_ids": []},
     "action": "则率所部兵以从，事平还卫",
     "object": "征讨", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条49 都司沿革 ============
    {"slot": 1, "item_id": "05-049", "type": "禁止型", "modals": ["prohibit"],
     "condition": "都卫节制方面，职系甚重",
     "subject": {"text": "都卫", "subject_ent_ids": []},
     "action": "从朝廷选择升调，不许世袭",
     "object": "都卫官", "purpose": "职系甚重", "punishment": "未明", "confidence": 0.93},

    # ============ 条51 卫指挥使司（核心）============
    {"slot": 1, "item_id": "05-051", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "卫指挥使司", "subject_ent_ids": []},
     "action": "外卫各统于都司、行都司或留守司，率世官，或有流官",
     "object": "卫所军务", "purpose": "未明", "punishment": "未明", "confidence": 0.93},

    {"slot": 2, "item_id": "05-051", "type": "程序型", "modals": ["procedure"],
     "condition": "凡袭替、升授、优给、优养及属所军政",
     "subject": {"text": "掌印、佥事", "subject_ent_ids": []},
     "action": "报都指挥使司，达所隶都督府，移兵部",
     "object": "袭替升授", "purpose": "未明", "punishment": "未明", "confidence": 0.93},

    {"slot": 3, "item_id": "05-051", "type": "时限型", "modals": ["deadline"],
     "condition": "每岁抚、按察其贤否",
     "subject": {"text": "抚、按", "subject_ent_ids": []},
     "action": "每岁察其贤否，五岁一考选军政，废置之",
     "object": "卫所官考选", "purpose": "未明", "punishment": "废置之", "confidence": 0.93},

    {"slot": 4, "item_id": "05-051", "type": "程序型", "modals": ["procedure"],
     "condition": "凡管理卫事，惟属掌印、佥书",
     "subject": {"text": "掌印、佥书", "subject_ent_ids": []},
     "action": "不论指挥使、同知、佥事，考选其才者充之；分理屯田、验军、营操、巡捕、漕运、备御、出哨、入卫、戍守、军器诸杂务，曰见任管事；不任事入队，曰带俸差操",
     "object": "卫事分理", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    {"slot": 5, "item_id": "05-051", "type": "义务型", "modals": ["obligation"],
     "condition": "征行",
     "subject": {"text": "卫指挥使司", "subject_ent_ids": []},
     "action": "率其属，听所命主帅调度",
     "object": "征行", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条53 千户所沿革 ============
    {"slot": 1, "item_id": "05-053", "type": "程序型", "modals": ["procedure"],
     "condition": "核诸将所部",
     "subject": {"text": "太祖", "subject_ent_ids": []},
     "action": "有兵五千者为指挥使，千人者为千户，百人者为百户，五十人为总旗，十人为小旗",
     "object": "卫所编制", "purpose": "名实相称", "punishment": "未明", "confidence": 0.93},

    {"slot": 2, "item_id": "05-053", "type": "程序型", "modals": ["procedure"],
     "condition": "洪武七年，申定卫所之制",
     "subject": {"text": "卫所", "subject_ent_ids": []},
     "action": "每卫设前、后、中、左、右五千户所，大率以五千六百人为一卫，一千一百二十人为一千户所，一百一十二人为一百户所，每百户所设总旗二人，小旗十人",
     "object": "卫所编制", "purpose": "更定其制", "punishment": "未明", "confidence": 0.95},

    {"slot": 3, "item_id": "05-053", "type": "义务型", "modals": ["obligation"],
     "condition": "洪武二十年，始命各卫立掌印、佥书",
     "subject": {"text": "掌印、佥书", "subject_ent_ids": []},
     "action": "专职理事，以指挥使掌印，同知、佥事各领一所；士卒有武艺不娴、器械不利者，皆责所领之官",
     "object": "卫所理事", "purpose": "未明", "punishment": "责所领之官", "confidence": 0.93},

    {"slot": 4, "item_id": "05-053", "type": "义务型", "modals": ["obligation"],
     "condition": "自卫指挥以下",
     "subject": {"text": "卫所官", "subject_ent_ids": []},
     "action": "其官多世袭，其军士亦父子相继，为一代定制",
     "object": "卫所世袭", "purpose": "为一代定制", "punishment": "未明", "confidence": 0.95},

    # ============ 条54 土官宣慰使司 ============
    {"slot": 1, "item_id": "05-054", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "土官", "subject_ent_ids": []},
     "action": "附辑诸蛮，谨守疆土，修职贡，供征调，无相携贰",
     "object": "土司治理", "purpose": "未明", "punishment": "未明", "confidence": 0.93},

    # ============ 条55 土官承袭 ============
    {"slot": 1, "item_id": "05-055", "type": "程序型", "modals": ["procedure"],
     "condition": "凡土官承袭",
     "subject": {"text": "土官", "subject_ent_ids": []},
     "action": "先具其宗图、亲供、册结，及邻封具结，报部，验实乃许承袭",
     "object": "土官承袭", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    {"slot": 2, "item_id": "05-055", "type": "优先级型", "modals": ["priority"],
     "condition": "其承袭",
     "subject": {"text": "土官", "subject_ent_ids": []},
     "action": "以嫡长，无嫡长则以次，无次则以亲，皆以次降等",
     "object": "土官承袭次序", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条56 土官纳粮 ============
    {"slot": 1, "item_id": "05-056", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "土官", "subject_ent_ids": []},
     "action": "各随其地所产，岁输贡赋，以供军国之需",
     "object": "土司贡赋", "purpose": "未明", "punishment": "未明", "confidence": 0.88},

    # ============ 条58 土司衙门等级 ============
    {"slot": 1, "item_id": "05-058", "type": "优先级型", "modals": ["priority"],
     "condition": "未明",
     "subject": {"text": "土司", "subject_ent_ids": []},
     "action": "以宣慰使司为上，宣抚司次之，安抚司又次之，长官司为下",
     "object": "土司等级", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条60 朝贡约束（核心）============
    {"slot": 1, "item_id": "05-060", "type": "义务型", "modals": ["obligation"],
     "condition": "洪武七年，西南诸蛮夷朝贡，多因元官授之，稍与约束，定征徭差发之法",
     "subject": {"text": "西南诸蛮夷", "subject_ent_ids": []},
     "action": "皆因其俗，使之附辑诸蛮，谨守疆土，修职贡，供征调，无相携贰",
     "object": "朝贡征调", "purpose": "未明", "punishment": "未明", "confidence": 0.93},

    {"slot": 2, "item_id": "05-060", "type": "程序型", "modals": ["procedure"],
     "condition": "有相仇者",
     "subject": {"text": "诸蛮夷", "subject_ent_ids": []},
     "action": "疏上听命于天子",
     "object": "蛮夷相仇", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条44 南京守备（补）============
    {"slot": 1, "item_id": "05-044", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "南京守备", "subject_ent_ids": []},
     "action": "掌南京一切留守、防护之事，凡南京内外守备、参赞机务，皆与议之",
     "object": "南京留守", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条47 都指挥使司（补：与兵部关系）============
    {"slot": 1, "item_id": "05-047", "type": "程序型", "modals": ["procedure"],
     "condition": "凡都司之政",
     "subject": {"text": "都司", "subject_ent_ids": []},
     "action": "大者奏请，小者径行，皆达于兵部",
     "object": "都司政务", "purpose": "未明", "punishment": "未明", "confidence": 0.88},

    # ============ 条52 卫所军器 ============
    {"slot": 1, "item_id": "05-052", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "卫所", "subject_ent_ids": []},
     "action": "掌军器之制造、保管，凡军器不足者，奏请给之",
     "object": "军器", "purpose": "未明", "punishment": "未明", "confidence": 0.85},
]
