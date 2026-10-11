# -*- coding: utf-8 -*-
"""《水东日记》卷 10 —— L1 实体标注 源数据（AI 判定逐条填写）

说明：实体标注：每条记录标注该条目中的实体（text=原文字面，type=实体类型，normalized=归一词形，confidence=置信度）

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：person=人物 / official=职官名 / institution=机构衙门 / place=地名 / era=年号朝代 / posthumous=谥号 / work=书名文献名 / unknown=类型待定
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

# 字段键（打包器校验用）：text, type, normalized, confidence, source
# 示例记录（保留作格式对照）：
# {"item_id": "01-001", "text": "礼部尚书", "type": "official", "normalized": "礼部尚书", "confidence": 0.97, "source": "原文片段"}

DATA = [
    # 10-001 崔与之吴彦
    {"item_id": "10-001", "text": "崔清献公", "type": "person", "normalized": "崔与之（谥清献，宋）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "10-001", "text": "吴彦", "type": "person", "normalized": "吴彦（统制/金州都统）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-001", "text": "四川路安抚制置使", "type": "official", "normalized": "四川路安抚制置使", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-001", "text": "统制", "type": "official", "normalized": "统制", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-001", "text": "枢密院", "type": "institution", "normalized": "枢密院", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "10-001", "text": "御前劄字", "type": "official", "normalized": "御前劄（御札）", "confidence": 0.82, "source": "原文片段"},
    # 10-007 金州都统
    {"item_id": "10-007", "text": "金州都统制", "type": "official", "normalized": "金州都统制", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-007", "text": "修武郎", "type": "official", "normalized": "修武郎（武阶）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-007", "text": "嘉定十六年", "type": "era", "normalized": "嘉定十六年（宋宁宗，1223）", "confidence": 0.85, "source": "原文片段"},
    # 10-010 黄山谷
    {"item_id": "10-010", "text": "黄山谷", "type": "person", "normalized": "黄庭坚（号山谷）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-010", "text": "泗州僧伽塔", "type": "place", "normalized": "泗州僧伽塔", "confidence": 0.82, "source": "原文片段"},
    # 10-011 描朱
    {"item_id": "10-011", "text": "宋学士", "type": "person", "normalized": "宋濂（学士）", "confidence": 0.85, "source": "原文片段"},
    # 10-012 乘轿/斯文盛举
    {"item_id": "10-012", "text": "汪浮溪", "type": "person", "normalized": "汪藻（号浮溪）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-012", "text": "伊洛大儒", "type": "person", "normalized": "程朱（伊洛）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "10-012", "text": "文华堂", "type": "institution", "normalized": "文华堂（洪武育才）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-012", "text": "曾棨", "type": "person", "normalized": "曾棨（永乐状元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-012", "text": "王琏", "type": "person", "normalized": "王琏（汝器）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "10-012", "text": "高启", "type": "person", "normalized": "高启（明）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-012", "text": "谢徽", "type": "person", "normalized": "谢徽（明）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-012", "text": "永乐大典", "type": "work", "normalized": "永乐大典", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "10-012", "text": "王汝嘉", "type": "person", "normalized": "王汝嘉", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "10-012", "text": "赵友同", "type": "person", "normalized": "赵友同", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "10-012", "text": "陈继", "type": "person", "normalized": "陈继（嗣初）", "confidence": 0.8, "source": "原文片段"},
    # 10-013 水利/石璞
    {"item_id": "10-013", "text": "范石湖", "type": "person", "normalized": "范成大（号石湖）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-013", "text": "王荆公", "type": "person", "normalized": "王安石（封荆公）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-013", "text": "石璞", "type": "person", "normalized": "石璞（江西按察使）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-013", "text": "王孟坚", "type": "person", "normalized": "王孟坚（佥事）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-013", "text": "许振", "type": "person", "normalized": "许振（吉水，刑部员外郎）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-013", "text": "夏埙", "type": "person", "normalized": "夏埙（御史）", "confidence": 0.82, "source": "原文片段"},
    # 10-014 塑工
    {"item_id": "10-014", "text": "杨惠之", "type": "person", "normalized": "杨惠之（唐塑工）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-014", "text": "刘正奉", "type": "person", "normalized": "刘正奉（元塑工）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-014", "text": "北京东岳庙", "type": "place", "normalized": "北京东岳庙", "confidence": 0.82, "source": "原文片段"},
    # 10-015 渔家傲/诗
    {"item_id": "10-015", "text": "范魏公", "type": "person", "normalized": "范仲淹（封魏国公）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-015", "text": "裴晋公", "type": "person", "normalized": "裴度（封晋公）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-015", "text": "周公恂如", "type": "person", "normalized": "周忱（字恂如，巡抚南畿）", "confidence": 0.85, "source": "原文片段"},
    # 10-016 景泰遣使
    {"item_id": "10-016", "text": "太上皇帝", "type": "person", "normalized": "明英宗（北狩）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-016", "text": "兵科", "type": "institution", "normalized": "兵科", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "10-016", "text": "景泰元年", "type": "era", "normalized": "景泰元年（1450）", "confidence": 0.85, "source": "原文片段"},
    # 10-017 黄素伯夷颂
    {"item_id": "10-017", "text": "苏才翁", "type": "person", "normalized": "苏舜元（字才翁）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-017", "text": "刘原父", "type": "person", "normalized": "刘敞（字原父）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-017", "text": "欧阳公", "type": "person", "normalized": "欧阳修", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-017", "text": "杨东里", "type": "person", "normalized": "杨士奇（号东里）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-017", "text": "苏平", "type": "person", "normalized": "苏平（秉衡，海昌诗人）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-017", "text": "王禹玉", "type": "person", "normalized": "王珪（字禹玉）", "confidence": 0.82, "source": "原文片段"},
    # 10-019 乖觉
    {"item_id": "10-019", "text": "韩退之", "type": "person", "normalized": "韩愈（字退之）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-019", "text": "罗隐", "type": "person", "normalized": "罗隐（唐）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-019", "text": "柏子庭", "type": "person", "normalized": "柏子庭（僧）", "confidence": 0.82, "source": "原文片段"},
    # 10-020 张子才彭时
    {"item_id": "10-020", "text": "张子才", "type": "person", "normalized": "张子才（石川，洪武秀才）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-020", "text": "彭时", "type": "person", "normalized": "彭时（正统戊辰状元）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "10-020", "text": "锦衣卫", "type": "institution", "normalized": "锦衣卫", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "10-020", "text": "郑时乂", "type": "person", "normalized": "郑时乂（叶盛友）", "confidence": 0.8, "source": "原文片段"},
    # 10-021 杨士奇诗
    {"item_id": "10-021", "text": "秋官郎中彦谧", "type": "person", "normalized": "彦谧（秋官郎中）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "10-021", "text": "杨士奇", "type": "person", "normalized": "杨士奇（庐陵）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "10-021", "text": "王忠毅公", "type": "person", "normalized": "王骥（谥忠毅）", "confidence": 0.85, "source": "原文片段"},
    # 10-022 两正官
    {"item_id": "10-022", "text": "吏部", "type": "institution", "normalized": "吏部", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "10-022", "text": "王直", "type": "person", "normalized": "王直（吏部尚书）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-022", "text": "何文渊", "type": "person", "normalized": "何文渊", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-022", "text": "王翱", "type": "person", "normalized": "王翱", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-022", "text": "胡濙", "type": "person", "normalized": "胡濙（礼部）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "10-022", "text": "于谦", "type": "person", "normalized": "于谦（兵部）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "10-022", "text": "陈镒", "type": "person", "normalized": "陈镒（都察院）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-022", "text": "国子监", "type": "institution", "normalized": "国子监", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "10-022", "text": "武功伯", "type": "person", "normalized": "徐有贞（封武功伯）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-022", "text": "靖远伯", "type": "person", "normalized": "王骥（封靖远伯）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-022", "text": "李贤", "type": "person", "normalized": "李贤（少保）", "confidence": 0.85, "source": "原文片段"},
    # 10-023 王建诗
    {"item_id": "10-023", "text": "王建", "type": "person", "normalized": "王建（唐诗人）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-023", "text": "昌黎", "type": "person", "normalized": "韩愈（昌黎）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "10-023", "text": "韦庄", "type": "person", "normalized": "韦庄（唐）", "confidence": 0.85, "source": "原文片段"},
    # 10-024 奏本题本
    {"item_id": "10-024", "text": "杜祁公", "type": "person", "normalized": "杜衍（封祁公）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-024", "text": "蹇忠定", "type": "person", "normalized": "蹇义（谥忠定）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-024", "text": "吕夷简", "type": "person", "normalized": "吕夷简（宋）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-024", "text": "崔菊坡", "type": "person", "normalized": "崔与之（号菊坡）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "10-024", "text": "洪武正韵", "type": "work", "normalized": "洪武正韵", "confidence": 0.85, "source": "原文片段"},
]
