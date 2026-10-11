# -*- coding: utf-8 -*-
"""《水东日记》卷 07 —— APPT 职官任职 源数据（AI 判定逐条填写）

说明：任职记录：person(人物含 person_ent_ids)/office(官职含 official_ent_ids)/institution(机构含 ent_ids)/when(时间，未明写'未明')/status(任职状态)/evidence(证据)

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：现任=在任 / 致仕=退休 / 升迁=晋升调任 / 贬谪=降职流放 / 罢黜=罢官 / 兼领=兼职兼任 / 暂代=暂时代理 / 追赠=死后追赠 / 未明=原文未明写
  * 未建模条目在下方注释中如实单列，不强行编造

填写方式：把 DATA 中的示例记录替换为本卷实际判定结果；
         每条记录为一个 dict；未判定条目保留注释占位。
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "07-001 | 太宗皇帝初营天寿山命皇太子偕汉赵二王暨皇太孙往视之过沙河冻王",
    "07-002 | 近内阁翰苑诸公有赏芍药黄字韵诗号玉堂赏花集盛行于时永新刘学士",
    "07-003 | 钱学士原溥言交阯伪学士承防某颇有文学其言曰国人多往来中国诗文",
    "07-004 | 宋薛简肃公五女长适张竒次乔易从次王拱辰次欧阳公次又适拱辰载于",
    "07-005 | 欧阳文忠公与十二侄帖苏长公题其后曰凡人勉强于外何所不至惟考诸",
    "07-006 | 吾平日行李出入未尝有意择日每为同事将官中贵所恳留闻士夫中喜谈",
    "07-007 | 陈僖敏公治陜西王文少保为按察使金荣襄为副使两人皆僖敏先后保荐",
    "07-008 | 司马温公尝手书其所荐朝士为一册其卷端曰举贤才此纸百年前尚在",
    "07-009 | 欧阳公撰范文正神道碑富韩公以差叙官次为言公以为此碑直叙事系天",
    "07-010 | 吴下举子有作诗自掲防壁间者乃兄誉之座客曰舍弟此诗云有唐气一客",
    "07-011 | 今人书简后具礼或误作礼如初或具礼如初或礼如左右前等虽名公卿亦",
    "07-012 | 图书印信之说具印史等书盖自汉以来固有之而元为特盛但多官封爵邑",
    "07-013 | 馆阁诸公无不喜用名印虽草庐吴公所尚质朴亦所不免惟掲文安公絶不",
    "07-014 | 尝见勑内阁杨学士盖勤民之玺皇太后遗诰盖德昭顺之寳皇后制书盖",
    "07-015 | 天不生仲尼万世如长夜两语其来已久而优人尝以为言闻有举子卷中曾",
    "07-016 | 丰布政文庆世居鄞宋清敏公稷之后也高祖庚六徙居奉化曾祖茂四徙定",
    "07-017 | 沈孟端先生方学虽本世医而通知古今有儒者风寓南京最久卿大夫若南",
    "07-018 | 陈检讨嗣初以文章擅名翰林一日见同官于碑志中叙还金事太繁者曰使",
    "07-019 | 己巳敌骑之薄都城朝野汹汹廷议有以南迁为言者盖亦冦准所非王钦若",
    "07-020 | 壬申易立之诏就下何文渊尝告人曰诏语天佑下民作之君父有天下传之",
    "07-021 | 苏武传名匈奴功显汉室即昌黎春猿秋鹤之李陵欲効曹柯之盟是虽",
    "07-022 | 钱选舜举有蔡琰南归图今在前临海丞夏佑存贤家元人多有题咏偶记其",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
# 示例记录（保留作格式对照）：
# {"appointment_id": "APPT-001", "item_id": "01-004", "person": {"text": "汪澄", "person_ent_ids": ["ENT-xxx"]}, "office": {"text": "巡按御史", "official_ent_ids": ["ENT-xxx"]}, "institution": {"text": "福建（巡按）", "ent_ids": ["ENT-xxx"]}, "when": "正统十三年", "status": "现任", "evidence": "巡按御史汪澄将至延平", "confidence": 0.92}

DATA = [
    # 07-007 陈僖敏治陕西
    {"appointment_id": "APPT-3501", "item_id": "07-007",
     "person": {"text": "陈镒（僖敏）", "person_ent_ids": []},
     "office": {"text": "陕西（镇守/巡抚）", "official_ent_ids": []},
     "institution": {"text": "陕西", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "陈僖敏公治陕西",
     "confidence": 0.85},
    {"appointment_id": "APPT-3502", "item_id": "07-007",
     "person": {"text": "王翱（少保）", "person_ent_ids": []},
     "office": {"text": "按察使", "official_ent_ids": []},
     "institution": {"text": "陕西", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "王文少保为按察使",
     "confidence": 0.85},
    {"appointment_id": "APPT-3503", "item_id": "07-007",
     "person": {"text": "金濂（荣襄）", "person_ent_ids": []},
     "office": {"text": "按察副使", "official_ent_ids": []},
     "institution": {"text": "陕西", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "金荣襄为副使",
     "confidence": 0.82},
    # 07-010 黄公南京
    {"appointment_id": "APPT-3504", "item_id": "07-010",
     "person": {"text": "黄公（东莱）", "person_ent_ids": []},
     "office": {"text": "少保户部尚书（南京）", "official_ent_ids": []},
     "institution": {"text": "南京户部", "ent_ids": []},
     "when": "景泰", "status": "现任",
     "evidence": "少保户部尚书东莱黄公在南京才识通敏",
     "confidence": 0.82},
    {"appointment_id": "APPT-3505", "item_id": "07-010",
     "person": {"text": "杨士奇（庐陵）", "person_ent_ids": []},
     "office": {"text": "少师（归省）", "official_ent_ids": []},
     "institution": {"text": "内阁", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "少师庐陵杨公归省过南京",
     "confidence": 0.85},
    # 07-016 丰文庆
    {"appointment_id": "APPT-3506", "item_id": "07-016",
     "person": {"text": "丰文庆", "person_ent_ids": []},
     "office": {"text": "布政使", "official_ent_ids": []},
     "institution": {"text": "未明", "ent_ids": []},
     "when": "正统景泰", "status": "现任",
     "evidence": "丰布政文庆世居鄞",
     "confidence": 0.82},
    {"appointment_id": "APPT-3507", "item_id": "07-016",
     "person": {"text": "丰寅初", "person_ent_ids": []},
     "office": {"text": "九江德化教谕", "official_ent_ids": []},
     "institution": {"text": "九江德化", "ent_ids": []},
     "when": "洪武", "status": "现任",
     "evidence": "考寅初洪武中授训导升九江德化教谕",
     "confidence": 0.8},
    # 07-017 杨鼎黄琛
    {"appointment_id": "APPT-3508", "item_id": "07-017",
     "person": {"text": "杨鼎", "person_ent_ids": []},
     "office": {"text": "右侍郎", "official_ent_ids": []},
     "institution": {"text": "未明", "ent_ids": []},
     "when": "正统", "status": "升迁",
     "evidence": "今杨右侍郎",
     "confidence": 0.82},
    {"appointment_id": "APPT-3509", "item_id": "07-017",
     "person": {"text": "黄琛", "person_ent_ids": []},
     "office": {"text": "左布政使", "official_ent_ids": []},
     "institution": {"text": "未明", "ent_ids": []},
     "when": "正统", "status": "升迁",
     "evidence": "黄左布政使",
     "confidence": 0.82},
    # 07-019 于谦
    {"appointment_id": "APPT-3510", "item_id": "07-019",
     "person": {"text": "于谦", "person_ent_ids": []},
     "office": {"text": "监察御史", "official_ent_ids": []},
     "institution": {"text": "都察院", "ent_ids": []},
     "when": "己巳（正统十四年）", "status": "现任",
     "evidence": "明日监察御史于谦上疏及论兹事",
     "confidence": 0.85},
    # 07-020 陈泰
    {"appointment_id": "APPT-3511", "item_id": "07-020",
     "person": {"text": "陈泰", "person_ent_ids": []},
     "office": {"text": "广东按察副使", "official_ent_ids": []},
     "institution": {"text": "广东", "ent_ids": []},
     "when": "天顺初", "status": "现任",
     "evidence": "广东陈副使泰取便道过家",
     "confidence": 0.82},
]
