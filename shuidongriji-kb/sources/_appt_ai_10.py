# -*- coding: utf-8 -*-
"""《水东日记》卷 10 —— APPT 职官任职 源数据（AI 判定逐条填写）

说明：任职记录：person(人物含 person_ent_ids)/office(官职含 official_ent_ids)/institution(机构含 ent_ids)/when(时间，未明写'未明')/status(任职状态)/evidence(证据)

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：现任=在任 / 致仕=退休 / 升迁=晋升调任 / 贬谪=降职流放 / 罢黜=罢官 / 兼领=兼职兼任 / 暂代=暂时代理 / 追赠=死后追赠 / 未明=原文未明写
  * 未建模条目在下方注释中如实单列，不强行编造

填写方式：把 DATA 中的示例记录替换为本卷实际判定结果；
         每条记录为一个 dict；未判定条目保留注释占位。
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "10-001 | 宋崔淸献公与之为四川路安抚制置使时与统制吴彦书帖并当时省劄见",
    "10-002 | 二月初奏剡已上并专书朝堂荐恳甚力旦夕当有峻除欲烦统制此来有一",
    "10-003 | 付吴统制",
    "10-004 | 御前劄字付金州都统吴　彦【御寳】封",
    "10-005 | 御寳实封枢宻院劄",
    "10-006 | 【此处疑有阙文】",
    "10-007 | 四川崔制置申与之窃惟人材难得而将材尤难得自非平时察访而收蓄之",
    "10-008 | 押　押　押",
    "10-009 | 嘉定十六年三月十八日",
    "10-010 | 十八日遣使臣樊厚前去想已到矣忽二十二日未时准庚牌逓到省劄有金",
    "10-011 | 上大人丘乙巳化三千七十士尔小生八九子佳作仁可知礼也尚士由山水",
    "10-012 | 宋南渡后行在百官有谢许乘轿表见汪浮溪集此亦乘轿事原然伊洛大儒",
    "10-013 | 范石湖为李结记濬塘浦云浦有五曰新洋江曰小虞曰茜泾曰下张曰顾浦",
    "10-014 | 宋杨惠之以塑工妙天下元刘正奉亦名世焉今北京东岳庙云尚有其迹两",
    "10-015 | 初予有关北之行叔简司丞手书渔家傲一阕见赠云是范魏公经畧西边时",
    "10-016 | 景泰元年三月予自开封还兵科见壁间贴记某月某日取回某本同僚言近",
    "10-017 | 范文正公尝用黄素楷书伯夷颂遗苏才翁刘原父以蜀素乌丝防求欧阳公",
    "10-018 | 盖与许洞诗僧事相云",
    "10-019 | 世称警悟有局干人曰乖觉于兵部奏内常用之然未见所出韩退之云亲朋",
    "10-020 | 萧墅张氏闻见录云石川张子才洪武二十四年以秀才举赴吏部尝有元宵",
    "10-021 | 三月二日秋官郎中彦谧贤友南行诗以识别杨生靑云器文采辉白壁腰间",
    "10-022 | 景泰中一时多两正官如吏部王何文渊继王翱礼部胡濙杨宁兵部于谦",
    "10-023 | 今时俗语事物纪名相传莫知所自而见诸唐人诗最多近读王建诗如卤簿",
    "10-024 | 大言无实专事表暴之人如唐之李元平李系石晋之景延广宋之雷简夫赵",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
# 示例记录（保留作格式对照）：
# {"appointment_id": "APPT-001", "item_id": "01-004", "person": {"text": "汪澄", "person_ent_ids": ["ENT-xxx"]}, "office": {"text": "巡按御史", "official_ent_ids": ["ENT-xxx"]}, "institution": {"text": "福建（巡按）", "ent_ids": ["ENT-xxx"]}, "when": "正统十三年", "status": "现任", "evidence": "巡按御史汪澄将至延平", "confidence": 0.92}

DATA = [
    # 10-001/10-007 崔与之吴彦
    {"appointment_id": "APPT-5001", "item_id": "10-001",
     "person": {"text": "崔与之（清献）", "person_ent_ids": []},
     "office": {"text": "四川路安抚制置使", "official_ent_ids": []},
     "institution": {"text": "四川制置司", "ent_ids": []},
     "when": "嘉定", "status": "现任",
     "evidence": "宋崔清献公与之为四川路安抚制置使时",
     "confidence": 0.85},
    {"appointment_id": "APPT-5002", "item_id": "10-007",
     "person": {"text": "吴彦", "person_ent_ids": []},
     "office": {"text": "金州都统制（权）", "official_ent_ids": []},
     "institution": {"text": "金州", "ent_ids": []},
     "when": "嘉定十六年", "status": "升迁",
     "evidence": "吴彦特差权金州都统制，任责措置捍御边面",
     "confidence": 0.85},
    # 10-013 石璞王孟坚
    {"appointment_id": "APPT-5003", "item_id": "10-013",
     "person": {"text": "石璞", "person_ent_ids": []},
     "office": {"text": "江西按察使（降副使）", "official_ent_ids": []},
     "institution": {"text": "江西按察司", "ent_ids": []},
     "when": "正统", "status": "贬谪",
     "evidence": "正统中石璞为江西按察使，适以失囚降副使",
     "confidence": 0.82},
    {"appointment_id": "APPT-5004", "item_id": "10-013",
     "person": {"text": "王孟坚", "person_ent_ids": []},
     "office": {"text": "江西按察佥事", "official_ent_ids": []},
     "institution": {"text": "江西按察司", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "王孟坚先生为佥事，清方端重",
     "confidence": 0.82},
    {"appointment_id": "APPT-5005", "item_id": "10-013",
     "person": {"text": "许振", "person_ent_ids": []},
     "office": {"text": "刑部员外郎", "official_ent_ids": []},
     "institution": {"text": "刑部", "ent_ids": []},
     "when": "正统", "status": "现任",
     "evidence": "刑部员外郎吉水许振先生",
     "confidence": 0.82},
    # 10-020 彭时
    {"appointment_id": "APPT-5006", "item_id": "10-020",
     "person": {"text": "彭时", "person_ent_ids": []},
     "office": {"text": "状元（正统戊辰）", "official_ent_ids": []},
     "institution": {"text": "翰林院", "ent_ids": []},
     "when": "正统戊辰", "status": "现任",
     "evidence": "正统戊辰状元彭时谢恩，以夜坐久误入朝被劾",
     "confidence": 0.85},
    # 10-022 两正官
    {"appointment_id": "APPT-5007", "item_id": "10-022",
     "person": {"text": "王直", "person_ent_ids": []},
     "office": {"text": "吏部尚书", "official_ent_ids": []},
     "institution": {"text": "吏部", "ent_ids": []},
     "when": "景泰", "status": "现任",
     "evidence": "景泰中一时多两正官，吏部王直、何文渊继王翱",
     "confidence": 0.85},
    {"appointment_id": "APPT-5008", "item_id": "10-022",
     "person": {"text": "于谦", "person_ent_ids": []},
     "office": {"text": "兵部尚书", "official_ent_ids": []},
     "institution": {"text": "兵部", "ent_ids": []},
     "when": "景泰", "status": "现任",
     "evidence": "兵部于谦、仪铭",
     "confidence": 0.85},
    {"appointment_id": "APPT-5009", "item_id": "10-022",
     "person": {"text": "陈镒", "person_ent_ids": []},
     "office": {"text": "都察院右都御史", "official_ent_ids": []},
     "institution": {"text": "都察院", "ent_ids": []},
     "when": "景泰", "status": "现任",
     "evidence": "都察院陈镒、王文继王翱",
     "confidence": 0.85},
]
