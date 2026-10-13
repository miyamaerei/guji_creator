# -*- coding: utf-8 -*-
"""
【卷01 续】条21–53 L2 规则层源数据 —— 户部余条/礼部/兵部/刑部/工部
纪律：编制行不抽（条25/33/41/46 头段）；职掌陈述句不抽；仅"凡/掌…之政令/不得"等规范句抽。
"""
RULES = [
    # ============ 条21 户部十三司职掌（陈述为主，1 条义务型）============
    {"slot": 1, "item_id": "01-021", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "户部十三司", "subject_ent_ids": []},
     "action": "各掌其分省之事，兼领所分两京、直隶贡赋，及诸司、卫所禄俸，边镇粮饷，并各仓场盐课、钞关",
     "object": "分省之事", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条22 户部四科职掌 ============
    {"slot": 1, "item_id": "01-022", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "户部民科", "subject_ent_ids": []},
     "action": "主所属省府州县地理、人物、图志、古今沿革、山川险易、土地肥瘠宽狭、户口物产多寡登耗之数",
     "object": "民科事务", "purpose": "未明", "punishment": "未明", "confidence": 0.88},
    {"slot": 2, "item_id": "01-022", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "户部度支", "subject_ent_ids": []},
     "action": "主会计夏税、秋粮、存留、起运",
     "object": "度支", "purpose": "未明", "punishment": "未明", "confidence": 0.88},

    # ============ 条24 总督仓场职掌 ============
    {"slot": 1, "item_id": "01-024", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "总督仓场", "subject_ent_ids": []},
     "action": "掌督在京及通州等处仓场粮储",
     "object": "仓场粮储", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 2, "item_id": "01-024", "type": "程序型", "modals": ["procedure"],
     "condition": "以后，或尚书，或侍郎",
     "subject": {"text": "总督仓场", "subject_ent_ids": []},
     "action": "俱不治部事",
     "object": "仓场督理", "purpose": "未明", "punishment": "未明", "confidence": 0.88},
    {"slot": 3, "item_id": "01-024", "type": "时限型", "modals": ["deadline"],
     "condition": "万历二年，另拨户部主事一人陪库",
     "subject": {"text": "户部主事", "subject_ent_ids": []},
     "action": "每日偕管库主事收放银两，季终更替",
     "object": "库银收放", "purpose": "未明", "punishment": "未明", "confidence": 0.88},

    # ============ 条26 礼部尚书职掌 ============
    {"slot": 1, "item_id": "01-026", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "礼部尚书", "subject_ent_ids": []},
     "action": "掌天下礼仪、祭祀、宴飨、贡举之政令。侍郎佐之",
     "object": "礼仪祭祀宴飨贡举", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    # ============ 条27 仪制司职掌 ============
    {"slot": 1, "item_id": "01-027", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "仪制司", "subject_ent_ids": []},
     "action": "分掌诸礼文、宗封、贡举、学校之事",
     "object": "礼文宗封贡举学校", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 2, "item_id": "01-027", "type": "程序型", "modals": ["procedure"],
     "condition": "天子即位，天子冠、大婚，册立皇太子、妃嫔、太子妃，上慈宫徽号，朝贺、朝见，大飨、宴飨，大射、宴射",
     "subject": {"text": "仪制司", "subject_ent_ids": []},
     "action": "则（备其仪）",
     "object": "各项大礼", "purpose": "未明", "punishment": "未明", "confidence": 0.85},

    # ============ 条28 祠祭司职掌 ============
    {"slot": 1, "item_id": "01-028", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "祠祭司", "subject_ent_ids": []},
     "action": "分掌诸祀典及天文、国恤、庙讳之事",
     "object": "祀典天文国恤庙讳", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 2, "item_id": "01-028", "type": "程序型", "modals": ["procedure"],
     "condition": "凡祭有三，曰天神、地祇、人鬼",
     "subject": {"text": "祠祭司", "subject_ent_ids": []},
     "action": "辨其大祀、中祀、小祀而敬供之。饬其坛壝、祠庙、陵寝而数省阅之",
     "object": "祭祀", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条29 主客司职掌 ============
    {"slot": 1, "item_id": "01-029", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "主客司", "subject_ent_ids": []},
     "action": "分掌诸蕃朝贡接待给赐之事",
     "object": "朝贡接待给赐", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 2, "item_id": "01-029", "type": "程序型", "modals": ["procedure"],
     "condition": "诸蕃朝贡",
     "subject": {"text": "主客司", "subject_ent_ids": []},
     "action": "辨其贡道、贡使、贡物远近多寡丰约之数，以定王若使迎送、宴劳、庐帐、食料之等，赏赉之差。凡贡必省阅之",
     "object": "朝贡", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条30 精膳司职掌 ============
    {"slot": 1, "item_id": "01-030", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "精膳司", "subject_ent_ids": []},
     "action": "分掌宴飨、牲豆、酒膳之事",
     "object": "宴飨牲豆酒膳", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 2, "item_id": "01-030", "type": "程序型", "modals": ["procedure"],
     "condition": "凡御赐百官礼食，曰宴，曰酒饭，为上中下三等，视其品秩。番使、土官有宴，有下程",
     "subject": {"text": "精膳司", "subject_ent_ids": []},
     "action": "（供其品物）",
     "object": "礼食", "purpose": "未明", "punishment": "未明", "confidence": 0.85},

    # ============ 条34 兵部尚书职掌 ============
    {"slot": 1, "item_id": "01-034", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "兵部尚书", "subject_ent_ids": []},
     "action": "掌天下武卫官军选授、简练之政令。侍郎佐之",
     "object": "武卫官军选授简练", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    # ============ 条35 武选司职掌（含勋级散阶）============
    {"slot": 1, "item_id": "01-035", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "武选司", "subject_ent_ids": []},
     "action": "掌卫所土官选授、升调、袭替、功赏之事",
     "object": "卫所土官", "purpose": "未明", "punishment": "未明", "confidence": 0.92},
    {"slot": 2, "item_id": "01-035", "type": "义务型", "modals": ["obligation"],
     "condition": "凡武官六品",
     "subject": {"text": "武选司", "subject_ent_ids": []},
     "action": "其勋十有二（正一品左、右柱国…从六品武骑尉）。散阶三十",
     "object": "武官勋级散阶", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条36 职方司职掌 ============
    {"slot": 1, "item_id": "01-036", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "职方司", "subject_ent_ids": []},
     "action": "掌舆图、军制、城隍、镇戍、简练、征讨之事",
     "object": "舆图军制镇戍", "purpose": "未明", "punishment": "未明", "confidence": 0.92},
    {"slot": 2, "item_id": "01-036", "type": "时限型", "modals": ["deadline"],
     "condition": "凡天下地里险易远近，边腹疆界，俱有图本",
     "subject": {"text": "职方司", "subject_ent_ids": []},
     "action": "三岁一报，与官军车骑之数偕上",
     "object": "舆图", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条37 车驾司职掌 ============
    {"slot": 1, "item_id": "01-037", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "车驾司", "subject_ent_ids": []},
     "action": "掌卤簿、仪仗、禁卫、驿传、厩牧之事",
     "object": "卤簿仪仗驿传厩牧", "purpose": "未明", "punishment": "未明", "confidence": 0.92},
    {"slot": 2, "item_id": "01-037", "type": "程序型", "modals": ["procedure"],
     "condition": "凡卤簿大驾，大典礼、大朝会设之；丹陛驾，常朝设之；武陈驾，世宗南巡时设之",
     "subject": {"text": "车驾司", "subject_ent_ids": []},
     "action": "皆辨其物数，以授所司",
     "object": "卤簿", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条38 武库司职掌 ============
    {"slot": 1, "item_id": "01-038", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "武库司", "subject_ent_ids": []},
     "action": "掌戎器、符勘、尺籍、武学、薪隶之事",
     "object": "戎器符勘尺籍武学", "purpose": "未明", "punishment": "未明", "confidence": 0.92},
    {"slot": 2, "item_id": "01-038", "type": "程序型", "modals": ["procedure"],
     "condition": "凡内外官军有征行",
     "subject": {"text": "武库司", "subject_ent_ids": []},
     "action": "移工部给器仗，籍纪其数，制敕下各边征发。及使人出关，必验勘合",
     "object": "戎器勘合", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 3, "item_id": "01-038", "type": "程序型", "modals": ["procedure"],
     "condition": "军伍缺",
     "subject": {"text": "武库司", "subject_ent_ids": []},
     "action": "下诸省府州县（取补）",
     "object": "军伍", "purpose": "未明", "punishment": "未明", "confidence": 0.85},

    # ============ 条40 协理京营戎政职掌 ============
    {"slot": 1, "item_id": "01-040", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "协理京营戎政", "subject_ent_ids": []},
     "action": "掌京营操练之事",
     "object": "京营操练", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条42 刑部尚书职掌 ============
    {"slot": 1, "item_id": "01-042", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "刑部尚书", "subject_ent_ids": []},
     "action": "掌天下刑名及徒隶、勾覆、关禁之政令。侍郎佐之",
     "object": "刑名徒隶勾覆关禁", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    # ============ 条43 刑部十三司职掌 ============
    {"slot": 1, "item_id": "01-043", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "刑部十三司", "subject_ent_ids": []},
     "action": "各掌其分省及兼领所分京府、直隶之刑名",
     "object": "分省刑名", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条44 刑部照磨司狱职掌（含诏狱程序）============
    {"slot": 1, "item_id": "01-044", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "照磨、检校", "subject_ent_ids": []},
     "action": "照刷文卷，计录赃赎",
     "object": "文卷赃赎", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 2, "item_id": "01-044", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "司狱", "subject_ent_ids": []},
     "action": "率狱吏，典囚徒",
     "object": "囚徒", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 3, "item_id": "01-044", "type": "程序型", "modals": ["procedure"],
     "condition": "凡军民、官吏及宗室、勋戚丽于法者",
     "subject": {"text": "刑部", "subject_ent_ids": []},
     "action": "诘其辞，察其情伪，傅律例而比议其罪之轻重以请",
     "object": "刑狱", "purpose": "未明", "punishment": "未明", "confidence": 0.92},
    {"slot": 4, "item_id": "01-044", "type": "程序型", "modals": ["procedure"],
     "condition": "诏狱",
     "subject": {"text": "刑部", "subject_ent_ids": []},
     "action": "必（会官审录）",
     "object": "诏狱", "purpose": "未明", "punishment": "未明", "confidence": 0.85},

    # ============ 条47 工部尚书职掌 ============
    {"slot": 1, "item_id": "01-047", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "工部尚书", "subject_ent_ids": []},
     "action": "掌天下百官、山泽之政令。侍郎佐之",
     "object": "百官山泽", "purpose": "未明", "punishment": "未明", "confidence": 0.92},

    # ============ 条48 营缮司职掌 ============
    {"slot": 1, "item_id": "01-048", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "营缮司", "subject_ent_ids": []},
     "action": "典经营兴作之事",
     "object": "兴作", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 2, "item_id": "01-048", "type": "程序型", "modals": ["procedure"],
     "condition": "凡宫殿、陵寝、城郭、坛场、祠庙、仓库、廨宇、营房、王府邸第之役",
     "subject": {"text": "营缮司", "subject_ent_ids": []},
     "action": "鸠工会材，以时程督之",
     "object": "营造工程", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条49 虞衡司职掌 ============
    {"slot": 1, "item_id": "01-049", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "虞衡司", "subject_ent_ids": []},
     "action": "典山泽采捕、陶冶之事",
     "object": "山泽采捕陶冶", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 2, "item_id": "01-049", "type": "程序型", "modals": ["procedure"],
     "condition": "凡鸟兽之肉、皮革、骨角、羽毛，可以供祭祀、宾客、膳羞之需，礼器、军实之用",
     "subject": {"text": "虞衡司", "subject_ent_ids": []},
     "action": "岁下诸司采捕。水课禽十八、兽十二，陆课（有差）",
     "object": "采捕课额", "purpose": "未明", "punishment": "未明", "confidence": 0.88},

    # ============ 条50 都水司职掌 ============
    {"slot": 1, "item_id": "01-050", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "都水司", "subject_ent_ids": []},
     "action": "典川泽、陂池、桥道、舟车、织造、券契、量衡之事",
     "object": "川泽桥道舟车", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 2, "item_id": "01-050", "type": "程序型", "modals": ["procedure"],
     "condition": "水利曰转漕，曰灌田",
     "subject": {"text": "都水司", "subject_ent_ids": []},
     "action": "岁储其金石、竹木、卷埽，以时修其闸坝、洪浅、堰圩、堤防，谨蓄泄以备（旱潦）",
     "object": "水利", "purpose": "未明", "punishment": "未明", "confidence": 0.9},

    # ============ 条51 屯田司职掌 ============
    {"slot": 1, "item_id": "01-051", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "屯田司", "subject_ent_ids": []},
     "action": "典屯种、抽分、薪炭、夫役、坟茔之事",
     "object": "屯种抽分薪炭", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
    {"slot": 2, "item_id": "01-051", "type": "程序型", "modals": ["procedure"],
     "condition": "凡军马守镇之处，其有转运不给",
     "subject": {"text": "屯田司", "subject_ent_ids": []},
     "action": "则设屯以益军储",
     "object": "军储", "purpose": "益军储", "punishment": "未明", "confidence": 0.9},

    # ============ 条53 提督易州山厂职掌 ============
    {"slot": 1, "item_id": "01-053", "type": "义务型", "modals": ["obligation"],
     "condition": "未明",
     "subject": {"text": "提督易州山厂", "subject_ent_ids": []},
     "action": "掌督御用柴炭之事",
     "object": "御用柴炭", "purpose": "未明", "punishment": "未明", "confidence": 0.9},
]
