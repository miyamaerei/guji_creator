# -*- coding: utf-8 -*-
"""《水东日记》卷 04 —— APPT 职官任职 源数据（AI 判定逐条填写）

说明：任职记录：person(人物含 person_ent_ids)/office(官职含 official_ent_ids)/institution(机构含 ent_ids)/when(时间，未明写'未明')/status(任职状态)/evidence(证据)

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：现任=在任 / 致仕=退休 / 升迁=晋升调任 / 贬谪=降职流放 / 罢黜=罢官 / 兼领=兼职兼任 / 暂代=暂时代理 / 追赠=死后追赠 / 未明=原文未明写
  * 未建模条目在下方注释中如实单列，不强行编造

填写方式：把 DATA 中的示例记录替换为本卷实际判定结果；
         每条记录为一个 dict；未判定条目保留注释占位。
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "04-001 | 正统四年廷试榜出华亭钱溥原溥仿宋人王十李三之诗自诵曰举头暂且",
    "04-002 | 长洲民杨芳景泰中尝以十事上巡抚邹都御史其均税额以为古昔井田养",
    "04-003 | 刘洗马定之朝遇王伟兵侍王戏之曰吾太仆马多洗马须一一洗之刘应声",
    "04-004 | 余姚陈惟寅先生教谕昆山颇喜谈风鉴尝曰举子梁昱当甲科瞿泰安不失",
    "04-005 | 临安钱宰子予武肃王之裔元末老儒也高庙礼徴同诸儒修纂尚书会选孟",
    "04-006 | 国子祭酒四明陈先生遇僚属诸生极严有怀忿而讼之者法司将覆请就逮",
    "04-007 | 王抑庵先生典选遇不如意事好诵古人诗以自寛一日有新得给事中即欲",
    "04-008 | 范啓东闻之前辈云士大夫游艺必审轻重且当先有迹者谓学文胜学诗学",
    "04-009 | 欧阳文忠公平生聚观金石刻动数百卷题识真迹甚多尝自言平生喜学书",
    "04-010 | 杨武襄洪为人虽尚权谲然有威严将士知畏之此其所长不可掩者亦赖朝",
    "04-011 | 景泰元年春久旱两京灾异亦迭见偶会礼科都给事中李实吏科给事中毛",
    "04-012 | 予为举子时闻同举者云国朝状元多不能至金带时陈泰和马临朐曹恒山",
    "04-013 | 今人燕客杯酌劝尽饮曰千歳南北士人多亦然但莫知其字义意者为请嗺",
    "04-014 | 鲜于困学圹志赵文敏公书小楷精絶篆笔出石鼓文少师庐陵杨公得之吴",
    "04-015 | 尚书吕震前左都御史刘观皆洪武中人物熟知政事故实故廷论之际每下",
    "04-016 | 宋黄震东发尝采董槐丞相之说以大学经文知止而后有定至则近道矣两",
    "04-017 | 先舅氏野水周先生念先外祖之无后有歳时祭甚盛德也而吾友进士郑时",
    "04-018 | 方言语音暗合古韵者多今山西人以去为库闽人以口为苦走为祖是也吾",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
# 示例记录（保留作格式对照）：
# {"appointment_id": "APPT-001", "item_id": "01-004", "person": {"text": "汪澄", "person_ent_ids": ["ENT-xxx"]}, "office": {"text": "巡按御史", "official_ent_ids": ["ENT-xxx"]}, "institution": {"text": "福建（巡按）", "ent_ids": ["ENT-xxx"]}, "when": "正统十三年", "status": "现任", "evidence": "巡按御史汪澄将至延平", "confidence": 0.92}

DATA = [
    # 04-004 陈惟寅教谕
    {"appointment_id": "APPT-2001", "item_id": "04-004",
     "person": {"text": "陈惟寅", "person_ent_ids": []},
     "office": {"text": "教谕", "official_ent_ids": []},
     "institution": {"text": "昆山县学", "ent_ids": []},
     "when": "明初", "status": "现任",
     "evidence": "余姚陈惟寅先生教谕昆山颇喜谈风鉴",
     "confidence": 0.82},
    # 04-004 瞿泰安刑部郎中
    {"appointment_id": "APPT-2002", "item_id": "04-004",
     "person": {"text": "瞿泰安", "person_ent_ids": []},
     "office": {"text": "刑部郎中", "official_ent_ids": []},
     "institution": {"text": "刑部", "ent_ids": []},
     "when": "明初", "status": "现任",
     "evidence": "泰安官至刑部郎中",
     "confidence": 0.82},
    # 04-004 梁昱平定知州
    {"appointment_id": "APPT-2003", "item_id": "04-004",
     "person": {"text": "梁昱", "person_ent_ids": []},
     "office": {"text": "知州", "official_ent_ids": []},
     "institution": {"text": "山西平定州", "ent_ids": []},
     "when": "明初", "status": "现任",
     "evidence": "竟以国子生选平定知州",
     "confidence": 0.8},
    # 04-005 钱宰国子博士致仕
    {"appointment_id": "APPT-2004", "item_id": "04-005",
     "person": {"text": "钱宰", "person_ent_ids": []},
     "office": {"text": "国子博士", "official_ent_ids": []},
     "institution": {"text": "国子监", "ent_ids": []},
     "when": "洪武初", "status": "致仕",
     "evidence": "宰以国子博士致仕家会稽",
     "confidence": 0.85},
    # 04-006 陈祭酒
    {"appointment_id": "APPT-2005", "item_id": "04-006",
     "person": {"text": "陈祭酒（四明）", "person_ent_ids": []},
     "office": {"text": "国子祭酒", "official_ent_ids": []},
     "institution": {"text": "国子监", "ent_ids": []},
     "when": "明初", "status": "现任",
     "evidence": "国子祭酒四明陈先生遇僚属诸生极严",
     "confidence": 0.82},
    # 04-007 卢熊兖州知州
    {"appointment_id": "APPT-2006", "item_id": "04-007",
     "person": {"text": "卢熊（字公武）", "person_ent_ids": []},
     "office": {"text": "知州", "official_ent_ids": []},
     "institution": {"text": "兖州", "ent_ids": []},
     "when": "洪武初", "status": "现任",
     "evidence": "昆山卢熊字公武洪武初名儒尝为兖州知州",
     "confidence": 0.85},
    # 04-007 卢熈睢州同知
    {"appointment_id": "APPT-2007", "item_id": "04-007",
     "person": {"text": "卢熈（字公暨）", "person_ent_ids": []},
     "office": {"text": "同知", "official_ent_ids": []},
     "institution": {"text": "睢州", "ent_ids": []},
     "when": "洪武初", "status": "现任",
     "evidence": "弟熈字公暨睢州同知有贤名",
     "confidence": 0.82},
    # 04-010 杨洪
    {"appointment_id": "APPT-2008", "item_id": "04-010",
     "person": {"text": "杨洪（武襄）", "person_ent_ids": []},
     "office": {"text": "都督/总戎（总兵）", "official_ent_ids": []},
     "institution": {"text": "宣府镇", "ent_ids": []},
     "when": "宣德正统", "status": "现任",
     "evidence": "杨武襄洪为人虽尚权谲然有威严将士知畏之",
     "confidence": 0.85},
    # 04-010 魏源尚书
    {"appointment_id": "APPT-2009", "item_id": "04-010",
     "person": {"text": "魏源", "person_ent_ids": []},
     "office": {"text": "尚书", "official_ent_ids": []},
     "institution": {"text": "未明", "ent_ids": []},
     "when": "明初", "status": "现任",
     "evidence": "初为指挥杜衡所诬以魏尚书源覆辨而衡贬广西",
     "confidence": 0.82},
    # 04-011 李实礼科都给事中
    {"appointment_id": "APPT-2010", "item_id": "04-011",
     "person": {"text": "李实", "person_ent_ids": []},
     "office": {"text": "礼科都给事中", "official_ent_ids": []},
     "institution": {"text": "六科（礼科）", "ent_ids": []},
     "when": "景泰元年", "status": "现任",
     "evidence": "礼科都给事中李实",
     "confidence": 0.85},
    # 04-011 毛玉吏科给事中
    {"appointment_id": "APPT-2011", "item_id": "04-011",
     "person": {"text": "毛玉", "person_ent_ids": []},
     "office": {"text": "吏科给事中", "official_ent_ids": []},
     "institution": {"text": "六科（吏科）", "ent_ids": []},
     "when": "景泰元年", "status": "现任",
     "evidence": "吏科给事中毛玉",
     "confidence": 0.82},
    # 04-011 于谦兵部尚书
    {"appointment_id": "APPT-2012", "item_id": "04-011",
     "person": {"text": "于谦", "person_ent_ids": []},
     "office": {"text": "兵部尚书", "official_ent_ids": []},
     "institution": {"text": "兵部", "ent_ids": []},
     "when": "景泰元年", "status": "现任",
     "evidence": "兵部尚书于公谦谓盛言中官事",
     "confidence": 0.88},
    # 04-011 陈镒左都御史
    {"appointment_id": "APPT-2013", "item_id": "04-011",
     "person": {"text": "陈镒", "person_ent_ids": []},
     "office": {"text": "左都御史", "official_ent_ids": []},
     "institution": {"text": "都察院", "ent_ids": []},
     "when": "景泰元年", "status": "现任",
     "evidence": "时惟左都御史陈镒力赞会奏",
     "confidence": 0.85},
    # 04-011 马显户科都给事中
    {"appointment_id": "APPT-2014", "item_id": "04-011",
     "person": {"text": "马显", "person_ent_ids": []},
     "office": {"text": "户科都给事中", "official_ent_ids": []},
     "institution": {"text": "六科（户科）", "ent_ids": []},
     "when": "景泰元年", "status": "现任",
     "evidence": "户科都给事中马显忽言此事近日兵部有奏",
     "confidence": 0.82},
    # 04-011 俞士悦刑部尚书
    {"appointment_id": "APPT-2015", "item_id": "04-011",
     "person": {"text": "俞士悦", "person_ent_ids": []},
     "office": {"text": "刑部尚书", "official_ent_ids": []},
     "institution": {"text": "刑部", "ent_ids": []},
     "when": "景泰元年", "status": "现任",
     "evidence": "刑部尚书俞士悦以为当准拟",
     "confidence": 0.82},
    # 04-015 吕震尚书
    {"appointment_id": "APPT-2016", "item_id": "04-015",
     "person": {"text": "吕震", "person_ent_ids": []},
     "office": {"text": "尚书", "official_ent_ids": []},
     "institution": {"text": "未明", "ent_ids": []},
     "when": "洪武中", "status": "现任",
     "evidence": "尚书吕震前左都御史刘观皆洪武中人物",
     "confidence": 0.82},
    # 04-015 刘观左都御史
    {"appointment_id": "APPT-2017", "item_id": "04-015",
     "person": {"text": "刘观", "person_ent_ids": []},
     "office": {"text": "左都御史", "official_ent_ids": []},
     "institution": {"text": "都察院", "ent_ids": []},
     "when": "洪武中", "status": "现任",
     "evidence": "尚书吕震前左都御史刘观皆洪武中人物",
     "confidence": 0.82},
]
