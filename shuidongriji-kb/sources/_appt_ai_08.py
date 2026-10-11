# -*- coding: utf-8 -*-
"""《水东日记》卷 08 —— APPT 职官任职 源数据（AI 判定逐条填写）

说明：任职记录：person(人物含 person_ent_ids)/office(官职含 official_ent_ids)/institution(机构含 ent_ids)/when(时间，未明写'未明')/status(任职状态)/evidence(证据)

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：现任=在任 / 致仕=退休 / 升迁=晋升调任 / 贬谪=降职流放 / 罢黜=罢官 / 兼领=兼职兼任 / 暂代=暂时代理 / 追赠=死后追赠 / 未明=原文未明写
  * 未建模条目在下方注释中如实单列，不强行编造

填写方式：把 DATA 中的示例记录替换为本卷实际判定结果；
         每条记录为一个 dict；未判定条目保留注释占位。
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "08-001 | 詹事刘先生简静端确士也久在翰林初为祭酒人或以不更事为先生疑久",
    "08-002 | 张翼字文翔太仓人性嫉恶至不容人小过御史按吴中不律翼忿忿不能平",
    "08-003 | 衣和庵主苏州昆山人也居雪窦之栖云畜二虎恒跨之以游后徙二灵终",
    "08-004 | 山东叅政海宁孙子良与同年进士西昌杨相交游极厚相为主事坐谷府累",
    "08-005 | 郑太师府佥判位本贯开封府开封县今寓平江府昆山县三代曾祖南皇任",
    "08-006 | 苏长公雪中饮王定国清虚堂诗真迹自注云旧说佛经所言如人入檐卜林",
    "08-007 | 都察院右都御史太康顾公佐洪武庚辰进士永乐初自庄浪令为监察御史",
    "08-008 | 尝闻宋景濂先生过佛寺方孝儒实从先生见佛叅拜孝儒不为礼或以为请",
    "08-009 | 吾家唐相履水之后旧有家谱咸通十一年一枝度江为处州丽水县丞讳隋",
    "08-010 | 翰林编修梁禋先生既病语家人曰朋游中惟隣居同年陈汝同心地好且有",
    "08-011 | 杨文贞公传王抑庵尚书作公尝三致书适确书削再致润笔且求其亲书俾",
    "08-012 | 黄霸只是州郡之才为宰相而事钩距固无如许精神天下亦将无所容而弊",
    "08-013 | 元人为宰相须福德才量四者兼备之说诚亦前人所未道也然君子所务亦",
    "08-014 | 东坡赤壁赋真迹寄傅尧俞者尝于俞尚书家见之洗盏更酌更字下自注一",
    "08-015 | 元诗人果啰罗纳延字易之金台集前后序题跋出虞伯生欧阳元功黄晋卿",
    "08-016 | 张文忠公养浩全集有欧阳圭斋序今在故副都御史云中孙廷瑞家盖齐府",
    "08-017 | 诧异差【去】异阘靸衰飒録续等字非必古有所出亦迁就仿佛耳",
    "08-018 | 天地间事凡有人用如此工夫则必有如此効验有是工夫无是効验虽间有",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
# 示例记录（保留作格式对照）：
# {"appointment_id": "APPT-001", "item_id": "01-004", "person": {"text": "汪澄", "person_ent_ids": ["ENT-xxx"]}, "office": {"text": "巡按御史", "official_ent_ids": ["ENT-xxx"]}, "institution": {"text": "福建（巡按）", "ent_ids": ["ENT-xxx"]}, "when": "正统十三年", "status": "现任", "evidence": "巡按御史汪澄将至延平", "confidence": 0.92}

DATA = [
    # 08-001 刘先生祭酒
    {"appointment_id": "APPT-4001", "item_id": "08-001",
     "person": {"text": "刘先生", "person_ent_ids": []},
     "office": {"text": "国子监祭酒", "official_ent_ids": []},
     "institution": {"text": "国子监", "ent_ids": []},
     "when": "永乐宣德", "status": "现任",
     "evidence": "久在翰林，初为祭酒",
     "confidence": 0.82},
    # 08-002 张翼
    {"appointment_id": "APPT-4002", "item_id": "08-002",
     "person": {"text": "张翼（文翔）", "person_ent_ids": []},
     "office": {"text": "御史（按吴中）", "official_ent_ids": []},
     "institution": {"text": "吴中", "ent_ids": []},
     "when": "正统", "status": "贬谪",
     "evidence": "御史按吴中不律，翼忿忿不能平，竟为众所倾，谪开平数年",
     "confidence": 0.82},
    # 08-004 孙子良等
    {"appointment_id": "APPT-4003", "item_id": "08-004",
     "person": {"text": "孙子良", "person_ent_ids": []},
     "office": {"text": "山东参政", "official_ent_ids": []},
     "institution": {"text": "山东", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "山东参政海宁孙子良",
     "confidence": 0.82},
    {"appointment_id": "APPT-4004", "item_id": "08-004",
     "person": {"text": "杨仲举", "person_ent_ids": []},
     "office": {"text": "王府长史", "official_ent_ids": []},
     "institution": {"text": "未明", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "杨仲举先生时为王府长史",
     "confidence": 0.8},
    {"appointment_id": "APPT-4005", "item_id": "08-004",
     "person": {"text": "耿公", "person_ent_ids": []},
     "office": {"text": "右都御史", "official_ent_ids": []},
     "institution": {"text": "都察院", "ent_ids": []},
     "when": "景泰", "status": "贬谪",
     "evidence": "右都御史耿公初以石氏事补外",
     "confidence": 0.8},
    # 08-007 顾佐魏源
    {"appointment_id": "APPT-4006", "item_id": "08-007",
     "person": {"text": "顾佐", "person_ent_ids": []},
     "office": {"text": "右都御史（掌台事）", "official_ent_ids": []},
     "institution": {"text": "都察院", "ent_ids": []},
     "when": "宣德初", "status": "致仕",
     "evidence": "永乐初自庄浪令为监察御史，升江西按察司副使，入为应天府尹，转通政司，宣德初进掌台事",
     "confidence": 0.88},
    {"appointment_id": "APPT-4007", "item_id": "08-007",
     "person": {"text": "魏源", "person_ent_ids": []},
     "office": {"text": "刑部尚书", "official_ent_ids": []},
     "institution": {"text": "刑部", "ent_ids": []},
     "when": "永乐至正统", "status": "致仕",
     "evidence": "永乐丙戌进士，监察御史、浙江副使，入署刑部右侍郎，升河南左布政使，赈饥三年，为刑部左侍郎进尚书",
     "confidence": 0.88},
    # 08-009 范信
    {"appointment_id": "APPT-4008", "item_id": "08-009",
     "person": {"text": "范信", "person_ent_ids": []},
     "office": {"text": "广西叅将都指挥使", "official_ent_ids": []},
     "institution": {"text": "广西", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "此谱见于今广西叅将都指挥使范信所谱",
     "confidence": 0.82},
    # 08-010 梁禋陈汝同
    {"appointment_id": "APPT-4009", "item_id": "08-010",
     "person": {"text": "梁禋", "person_ent_ids": []},
     "office": {"text": "翰林编修", "official_ent_ids": []},
     "institution": {"text": "翰林院", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "翰林编修梁禋先生既病",
     "confidence": 0.82},
    {"appointment_id": "APPT-4010", "item_id": "08-010",
     "person": {"text": "陈汝同（古庵）", "person_ent_ids": []},
     "office": {"text": "国子祭酒（致仕）", "official_ent_ids": []},
     "institution": {"text": "国子监", "ent_ids": []},
     "when": "正统", "status": "致仕",
     "evidence": "国子祭酒致仕陈古庵先生",
     "confidence": 0.82},
    {"appointment_id": "APPT-4011", "item_id": "08-010",
     "person": {"text": "黄瑜", "person_ent_ids": []},
     "office": {"text": "肇庆知府", "official_ent_ids": []},
     "institution": {"text": "肇庆", "ent_ids": []},
     "when": "天顺", "status": "现任",
     "evidence": "嫁女得今肇庆知府黄瑜",
     "confidence": 0.8},
    # 08-018 彭祖期
    {"appointment_id": "APPT-4012", "item_id": "08-018",
     "person": {"text": "彭祖期", "person_ent_ids": []},
     "office": {"text": "监察御史（提督南畿学校）", "official_ent_ids": []},
     "institution": {"text": "南畿", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "庐陵彭祖期先生以监察御史提督南畿学校",
     "confidence": 0.82},
    {"appointment_id": "APPT-4013", "item_id": "08-018",
     "person": {"text": "周忱", "person_ent_ids": []},
     "office": {"text": "巡抚侍郎", "official_ent_ids": []},
     "institution": {"text": "苏松", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "巡抚侍郎周公忱始一新之",
     "confidence": 0.85},
]
