# -*- coding: utf-8 -*-
"""《水东日记》卷 06 —— APPT 职官任职 源数据（AI 判定逐条填写）

说明：任职记录：person(人物含 person_ent_ids)/office(官职含 official_ent_ids)/institution(机构含 ent_ids)/when(时间，未明写'未明')/status(任职状态)/evidence(证据)

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：现任=在任 / 致仕=退休 / 升迁=晋升调任 / 贬谪=降职流放 / 罢黜=罢官 / 兼领=兼职兼任 / 暂代=暂时代理 / 追赠=死后追赠 / 未明=原文未明写
  * 未建模条目在下方注释中如实单列，不强行编造

填写方式：把 DATA 中的示例记录替换为本卷实际判定结果；
         每条记录为一个 dict；未判定条目保留注释占位。
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "06-001 | 叅赞军务等名始于洪熙初元以武臣疎于文墨选任方面官于各总兵官处",
    "06-002 | 顔征夷云都指挥马良最为上所爱尝得骑行禁中中官以为言上曰吾欲压",
    "06-003 | 叅将范信兵既入大同里俘获甚多旗牌官人给贼妇一二人值昏莫拘系一",
    "06-004 | 广州知府沈琮尝为南京兵部武库司主事武库司典皁凡诸司多属意焉",
    "06-005 | 顔总戎养疴广州问谈命者右卫军李名远梁万方二人先后至先叩李名逺",
    "06-006 | 六科衙门右砖城内尚寳司西永乐中灾暂于午门外直房署事遂以至今自",
    "06-007 | 午门外东直房六部都察院大理寺堂上官候朝之所两门入惟都御史正官",
    "06-008 | 岭北仓库草场中皆有土地祠仓中奉萧王问之则曰鄼侯盖以鄼侯尝督馈",
    "06-009 | 陈汝言宠幸时一日论学士进官或以过多为言汝言曰唐太宗时十八人今",
    "06-010 | 孙状元贤未第时尝梦金甲神人持黄旗揷其门上有状元字先人一夕梦双",
    "06-011 | 今都察院堂中扁肃政二字当撤去盖前元及建文中有此衔号宋以观文称",
    "06-012 | 周新广城人永乐中浙江按察使廉公正直声称籍甚为纪纲所间死仁庙每",
    "06-013 | 京师印卖春帖有曰雨露有恩沾万物乾坤何处不三阳好事者遂以为用三",
    "06-014 | 太祖皇帝尝及大臣所居曰大官人必得大宅第即与刑部尚书开济创为之",
    "06-015 | 侍郎于公巡抚河南山西妙年敏手下视无人尚书海丰王公学行朴实时以",
    "06-016 | 国子祭酒云间陈先生与前按察使黄翰为童丱交翰既败去士夫中有毁责",
    "06-017 | 昆山郏亶正夫显于宋熙宁元祐间事具玉峯志中吴纪闻等书近见南海志",
    "06-018 | 年之内无鸡鸣犬吠之【缺】　　　　叛民始被其害迄",
    "06-019 | 今十五六年諰諰【缺】　　　　　　燔灭之暴兹城之",
    "06-020 | 成穉女相庆昔之【缺】　　　　　　而惊驰者固已按堵而无虞矣夫兴",
    "06-021 | 或曰杨文定公尝云范文正高季迪皆出姑苏两人气象甚不同盖于其所赋",
    "06-022 | 松江老儒天台陶九成所著书颇为杨文贞公所不取盖如所谓书史会要是",
    "06-023 | 陈都御史智以教官多猥茸且锋铓畧尽难称激扬之任以是不得任御史有",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
# 示例记录（保留作格式对照）：
# {"appointment_id": "APPT-001", "item_id": "01-004", "person": {"text": "汪澄", "person_ent_ids": ["ENT-xxx"]}, "office": {"text": "巡按御史", "official_ent_ids": ["ENT-xxx"]}, "institution": {"text": "福建（巡按）", "ent_ids": ["ENT-xxx"]}, "when": "正统十三年", "status": "现任", "evidence": "巡按御史汪澄将至延平", "confidence": 0.92}

DATA = [
    # 06-001
    {"appointment_id": "APPT-3001", "item_id": "06-001",
     "person": {"text": "沈固", "person_ent_ids": []},
     "office": {"text": "户部尚书（致仕，叅赞大同军务）", "official_ent_ids": []},
     "institution": {"text": "大同", "ent_ids": []},
     "when": "洪熙宣德", "status": "致仕",
     "evidence": "如大同则今户部尚书致仕丹阳沈固",
     "confidence": 0.85},
    {"appointment_id": "APPT-3002", "item_id": "06-001",
     "person": {"text": "刘琏", "person_ent_ids": []},
     "office": {"text": "户部侍郎（叅赞宣府永宁伯军务）", "official_ent_ids": []},
     "institution": {"text": "宣府", "ent_ids": []},
     "when": "洪熙宣德", "status": "现任",
     "evidence": "宣府永宁伯处则户部侍郎昆山刘琏",
     "confidence": 0.85},
    {"appointment_id": "APPT-3003", "item_id": "06-001",
     "person": {"text": "颜彪", "person_ent_ids": []},
     "office": {"text": "征夷将军总兵官都督佥事", "official_ent_ids": []},
     "institution": {"text": "两广", "ent_ids": []},
     "when": "辛巳（天顺五年）", "status": "现任",
     "evidence": "协征夷将军总兵官都督佥事颜彪赞理戎务",
     "confidence": 0.85},
    # 06-002
    {"appointment_id": "APPT-3004", "item_id": "06-002",
     "person": {"text": "马良", "person_ent_ids": []},
     "office": {"text": "都指挥", "official_ent_ids": []},
     "institution": {"text": "未明", "ent_ids": []},
     "when": "宣德正统", "status": "现任",
     "evidence": "颜征夷云都指挥马良最为上所爱",
     "confidence": 0.82},
    # 06-004
    {"appointment_id": "APPT-3005", "item_id": "06-004",
     "person": {"text": "沈琮", "person_ent_ids": []},
     "office": {"text": "广州知府（前南京兵部武库司主事）", "official_ent_ids": []},
     "institution": {"text": "广州", "ent_ids": []},
     "when": "正统", "status": "升迁",
     "evidence": "广州知府沈琮尝为南京兵部武库司主事",
     "confidence": 0.82},
    # 06-006
    {"appointment_id": "APPT-3006", "item_id": "06-006",
     "person": {"text": "马显", "person_ent_ids": []},
     "office": {"text": "户科都给事中", "official_ent_ids": []},
     "institution": {"text": "六科", "ent_ids": []},
     "when": "景泰", "status": "现任",
     "evidence": "景泰间户科都给事中马显强欲称六科都给事中",
     "confidence": 0.82},
    {"appointment_id": "APPT-3007", "item_id": "06-006",
     "person": {"text": "和勇", "person_ent_ids": []},
     "office": {"text": "两广游击将军都督同知", "official_ent_ids": []},
     "institution": {"text": "两广", "ent_ids": []},
     "when": "天顺", "status": "现任",
     "evidence": "两广游击将军都督同知和勇",
     "confidence": 0.82},
    # 06-007
    {"appointment_id": "APPT-3008", "item_id": "06-007",
     "person": {"text": "顾佐", "person_ent_ids": []},
     "office": {"text": "都御史", "official_ent_ids": []},
     "institution": {"text": "都察院", "ent_ids": []},
     "when": "宣德", "status": "现任",
     "evidence": "近岁都御史顾公佐非公聚未尝与诸司群坐立",
     "confidence": 0.85},
    # 06-012
    {"appointment_id": "APPT-3009", "item_id": "06-012",
     "person": {"text": "周新", "person_ent_ids": []},
     "office": {"text": "浙江按察使", "official_ent_ids": []},
     "institution": {"text": "浙江", "ent_ids": []},
     "when": "永乐", "status": "罢黜",
     "evidence": "永乐中浙江按察使廉公正直……为纪纲所谮死",
     "confidence": 0.88},
    # 06-014
    {"appointment_id": "APPT-3010", "item_id": "06-014",
     "person": {"text": "开济", "person_ent_ids": []},
     "office": {"text": "刑部尚书", "official_ent_ids": []},
     "institution": {"text": "刑部", "ent_ids": []},
     "when": "洪武", "status": "现任",
     "evidence": "即与刑部尚书开济创为之",
     "confidence": 0.85},
    # 06-015
    {"appointment_id": "APPT-3011", "item_id": "06-015",
     "person": {"text": "于谦", "person_ent_ids": []},
     "office": {"text": "兵部侍郎（巡抚河南山西）", "official_ent_ids": []},
     "institution": {"text": "河南山西", "ent_ids": []},
     "when": "宣德正统", "status": "升迁",
     "evidence": "侍郎于公巡抚河南山西妙年敏手",
     "confidence": 0.88},
    {"appointment_id": "APPT-3012", "item_id": "06-015",
     "person": {"text": "孙原贞、王来", "person_ent_ids": []},
     "office": {"text": "参政（荐代于谦巡抚）", "official_ent_ids": []},
     "institution": {"text": "河南山西", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "于因有参政孙原贞王来荐代之举，坐降官",
     "confidence": 0.82},
    # 06-016
    {"appointment_id": "APPT-3013", "item_id": "06-016",
     "person": {"text": "卢睿", "person_ent_ids": []},
     "office": {"text": "都御史（在边）", "official_ent_ids": []},
     "institution": {"text": "边方", "ent_ids": []},
     "when": "正统", "status": "贬谪",
     "evidence": "卢都御史睿在边以敌使入境节省供给为中贵人所毁得罪下狱",
     "confidence": 0.82},
    # 06-023
    {"appointment_id": "APPT-3014", "item_id": "06-023",
     "person": {"text": "陈智", "person_ent_ids": []},
     "office": {"text": "左佥都御史", "official_ent_ids": []},
     "institution": {"text": "都察院", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "陈都御史智以教官多猥茸……不得任御史",
     "confidence": 0.82},
]
