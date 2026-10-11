# -*- coding: utf-8 -*-
"""《水东日记》卷 03 —— APPT 职官任职 源数据（AI 判定逐条填写）

说明：任职记录：person(人物含 person_ent_ids)/office(官职含 official_ent_ids)/institution(机构含 ent_ids)/when(时间，未明写'未明')/status(任职状态)/evidence(证据)

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：现任=在任 / 致仕=退休 / 升迁=晋升调任 / 贬谪=降职流放 / 罢黜=罢官 / 兼领=兼职兼任 / 暂代=暂时代理 / 追赠=死后追赠 / 未明=原文未明写
  * 未建模条目在下方注释中如实单列，不强行编造

填写方式：把 DATA 中的示例记录替换为本卷实际判定结果；
         每条记录为一个 dict；未判定条目保留注释占位。
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "03-001 | 詹孟举篆书唐人早朝诗四纸孙叔英得之谈以宗家用笔絶泰不华王贞",
    "03-002 | 松江曹云西善诗画家富盛极一时其孙幼交号雪林客授孙至德家言乃祖",
    "03-003 | 正统十年进士登科録凡天字皆作防云出内阁意景泰中幸太学谢表内阁",
    "03-004 | 袁子英晚年惟一子生申为县吏坐累并子英徙南京以卒詹孟举挽诗曰吴",
    "03-005 | 萧墅张汉杰伯庸父子一时豪俊与赵屯吴氏有姻防张吴皆元万户府官吴",
    "03-006 | 钱知府昕初习举子业从节之游其外祖吴思庵先生作小诗遗之曰阿昕近",
    "03-007 | 甚矣富贵权宠之能动人也王子明冦平仲皆伟然一代人豪然天书之谬一",
    "03-008 | 至讷无言福严寺僧善词翰所交皆一代名人赵松雪冯海粟柯丹丘郑尚左",
    "03-009 | 福严寺老僧景燮颇能诗先人极与相好尝中夜对饮时予八九嵗侍几傍僧",
    "03-010 | 杨文定公最善王检讨振张修譔益相见辄出所作就二人评有所改易即乐",
    "03-011 | 张仲珪先生家藏风雨归牧图杨廉夫题曰牧牛值风雨箬笠几去手不在风",
    "03-012 | 夏忠靖公使吴中馆于文正书院之偏室夜三鼓适范氏子孙有事于中堂公",
    "03-013 | 尝过光福叶子昌家阅其谱壻陈瓘宗人梦其皆有序所録宋金紫棐恭公墓",
    "03-014 | 邓尉山中峯东北向居人相传地名黄坟盖宋刑部尚书黄状元由墓也赠工",
    "03-015 | 训导吾豫景泰中膺荐至京以屡言边事兵部奏宜边用而在边久不得支俸",
    "03-016 | 庄伯和碛澳名医好诙谐一日李无易遣家僮持简诣伯和家僮误举伯和姓",
    "03-017 | 【阙】　　　　　　　　　旧驿连新驿前山接后山我心无愧怍天道有",
    "03-018 | 山隂花溪蒋贵达老先生显司训昆庠质实敢言一日郡守况侯钟行部侯严",
    "03-019 | 庄瑾字公瑾号采芝龙江章氏之后晚居李墟能诗善草书学二王而硬徤骨",
    "03-020 | 松江李墟沈梦萱先生资深永乐中举略通书史吏部试招抚四裔榜纳卷独",
    "03-021 | 朱文公答巩仲至曰用韵多所未晓古韵虽有此例然在今日却恐不无讹谬",
    "03-022 | 予在邑庠时庠友吴芳廷实家畦菜得故冢志石见题云高平郁氏之墓政和",
    "03-023 | 定襄伯郭登治大同廉而尚谋有古良将风一日敌兵迫城下人心汹汹自登",
    "03-024 | 余尚书茂本熂父尝为镊工茂本既贵毎造谢隣曲不遇辄曰烦为道余待诏",
    "03-025 | 范啓东言长公于书独重云间沈度于画最爱永嘉郭文通以度书丰温润",
    "03-026 | 霹于边墩高处歳恒有之震死者或不闻其人其击屋柱桅竿之常见其",
    "03-027 | 中贵有再造营火者珍珠皆灰化玉器窑器或裂或变浅黑色惟诸色鸦鹘石",
    "03-028 | 尝见胡毘陵应酬诗文藁皆片纸满书闻其虽破纸少许见辄用补窻罅不弃",
    "03-029 | 文章家误用古人爵谥文意字义近世虽名人不免熊敬方胡祭酒皆以程明",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
# 示例记录（保留作格式对照）：
# {"appointment_id": "APPT-001", "item_id": "01-004", "person": {"text": "汪澄", "person_ent_ids": ["ENT-xxx"]}, "office": {"text": "巡按御史", "official_ent_ids": ["ENT-xxx"]}, "institution": {"text": "福建（巡按）", "ent_ids": ["ENT-xxx"]}, "when": "正统十三年", "status": "现任", "evidence": "巡按御史汪澄将至延平", "confidence": 0.92}

DATA = [
    # 03-004 申为县吏
    {"appointment_id": "APPT-1501", "item_id": "03-004",
     "person": {"text": "申（袁子英子）", "person_ent_ids": []},
     "office": {"text": "县吏", "official_ent_ids": []},
     "institution": {"text": "未明", "ent_ids": []},
     "when": "元末明初", "status": "现任",
     "evidence": "袁子英晚年惟一子生申为县吏坐累并子英徙南京以卒",
     "confidence": 0.8},
    # 03-012 杨东里少师
    {"appointment_id": "APPT-1502", "item_id": "03-012",
     "person": {"text": "杨士奇", "person_ent_ids": []},
     "office": {"text": "少师", "official_ent_ids": []},
     "institution": {"text": "内阁", "ent_ids": []},
     "when": "明初", "status": "现任",
     "evidence": "杨东里少师一日新修门成戒儿曹亟治具邀杨仲举先生过饮",
     "confidence": 0.85},
    # 03-012 杨仲举礼部尚书
    {"appointment_id": "APPT-1503", "item_id": "03-012",
     "person": {"text": "杨翥（字仲举）", "person_ent_ids": []},
     "office": {"text": "礼部尚书", "official_ent_ids": []},
     "institution": {"text": "礼部", "ent_ids": []},
     "when": "明初", "status": "现任",
     "evidence": "仲举苏州人宋和王之后官至礼部尚书",
     "confidence": 0.82},
    # 03-014 黄由刑部尚书
    {"appointment_id": "APPT-1504", "item_id": "03-014",
     "person": {"text": "黄由（状元）", "person_ent_ids": []},
     "office": {"text": "刑部尚书", "official_ent_ids": []},
     "institution": {"text": "刑部", "ent_ids": []},
     "when": "宋代", "status": "追赠",
     "evidence": "宋刑部尚书黄状元由墓也",
     "confidence": 0.8},
    # 03-014 王永和工部尚书
    {"appointment_id": "APPT-1505", "item_id": "03-014",
     "person": {"text": "王永和", "person_ent_ids": []},
     "office": {"text": "工部尚书", "official_ent_ids": []},
     "institution": {"text": "工部", "ent_ids": []},
     "when": "明初", "status": "追赠",
     "evidence": "赠工部尚书昆山王公永和夫人卒得葬地于此敕营墓焉",
     "confidence": 0.8},
    # 03-015 吾豫训导
    {"appointment_id": "APPT-1506", "item_id": "03-015",
     "person": {"text": "吾豫", "person_ent_ids": []},
     "office": {"text": "训导", "official_ent_ids": []},
     "institution": {"text": "县学", "ent_ids": []},
     "when": "景泰中", "status": "现任",
     "evidence": "训导吾豫景泰中膺荐至京以屡言边事",
     "confidence": 0.85},
    # 03-015 项侍郎吏部
    {"appointment_id": "APPT-1507", "item_id": "03-015",
     "person": {"text": "项侍郎", "person_ent_ids": []},
     "office": {"text": "吏部侍郎", "official_ent_ids": []},
     "institution": {"text": "吏部", "ent_ids": []},
     "when": "景泰中", "status": "现任",
     "evidence": "请于吏部项侍郎曰是尝搅我兵部者何可与之",
     "confidence": 0.82},
    # 03-015 王直吏部尚书
    {"appointment_id": "APPT-1508", "item_id": "03-015",
     "person": {"text": "王直", "person_ent_ids": []},
     "office": {"text": "吏部尚书", "official_ent_ids": []},
     "institution": {"text": "吏部", "ent_ids": []},
     "when": "景泰中", "status": "现任",
     "evidence": "尚书泰和王公曰官必有俸自须与之",
     "confidence": 0.85},
    # 03-015 于谦兵部尚书
    {"appointment_id": "APPT-1509", "item_id": "03-015",
     "person": {"text": "于谦", "person_ent_ids": []},
     "office": {"text": "兵部尚书", "official_ent_ids": []},
     "institution": {"text": "兵部", "ent_ids": []},
     "when": "景泰中", "status": "现任",
     "evidence": "于公见公牍喟然曰柰何使应荐士至此遽与准",
     "confidence": 0.85},
    # 03-018 蒋贵达司训
    {"appointment_id": "APPT-1510", "item_id": "03-018",
     "person": {"text": "蒋贵达", "person_ent_ids": []},
     "office": {"text": "司训（教谕）", "official_ent_ids": []},
     "institution": {"text": "昆庠（昆山学）", "ent_ids": []},
     "when": "明初", "status": "现任",
     "evidence": "山阴花溪蒋贵达老先生显司训昆庠质实敢言",
     "confidence": 0.82},
    # 03-018 况钟郡守
    {"appointment_id": "APPT-1511", "item_id": "03-018",
     "person": {"text": "况钟", "person_ent_ids": []},
     "office": {"text": "郡守（苏州知府）", "official_ent_ids": []},
     "institution": {"text": "苏州府", "ent_ids": []},
     "when": "明初", "status": "现任",
     "evidence": "一日郡守况侯钟行部侯严不可近",
     "confidence": 0.85},
    # 03-020 沈梦萱新城知县
    {"appointment_id": "APPT-1512", "item_id": "03-020",
     "person": {"text": "沈梦萱（资深）", "person_ent_ids": []},
     "office": {"text": "知县", "official_ent_ids": []},
     "institution": {"text": "山东新城县", "ent_ids": []},
     "when": "永乐中", "status": "现任",
     "evidence": "第优等授山东新城知县",
     "confidence": 0.85},
    # 03-023 郭登定襄伯治大同
    {"appointment_id": "APPT-1513", "item_id": "03-023",
     "person": {"text": "郭登", "person_ent_ids": []},
     "office": {"text": "定襄伯（守大同）", "official_ent_ids": []},
     "institution": {"text": "大同镇", "ent_ids": []},
     "when": "明初", "status": "现任",
     "evidence": "定襄伯郭登治大同廉而尚谋有古良将风",
     "confidence": 0.88},
    # 03-024 余茂本尚书
    {"appointment_id": "APPT-1514", "item_id": "03-024",
     "person": {"text": "余茂本", "person_ent_ids": []},
     "office": {"text": "尚书", "official_ent_ids": []},
     "institution": {"text": "未明", "ent_ids": []},
     "when": "明初", "status": "升迁",
     "evidence": "余尚书茂本熂父尝为镊工茂本既贵",
     "confidence": 0.8},
    # 03-022 郁鼎智医学训科
    {"appointment_id": "APPT-1515", "item_id": "03-022",
     "person": {"text": "郁鼎智", "person_ent_ids": []},
     "office": {"text": "医学训科", "official_ent_ids": []},
     "institution": {"text": "常熟县", "ent_ids": []},
     "when": "宋代（政和）", "status": "现任",
     "evidence": "常熟医学训科郁鼎智",
     "confidence": 0.8},
]
