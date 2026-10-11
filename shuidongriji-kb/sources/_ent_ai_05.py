# -*- coding: utf-8 -*-
"""《水东日记》卷 05 —— L1 实体标注 源数据（AI 判定逐条填写）

说明：实体标注：每条记录标注该条目中的实体（text=原文字面，type=实体类型，normalized=归一词形，confidence=置信度）

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：person=人物 / official=职官名 / institution=机构衙门 / place=地名 / era=年号朝代 / posthumous=谥号 / work=书名文献名 / unknown=类型待定
  * 未建模条目在下方注释中如实单列，不强行编造

填写方式：把 DATA 中的示例记录替换为本卷实际判定结果；
         每条记录为一个 dict；未判定条目保留注释占位。
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "05-001 | 左都御史自刘观后不轻受观以前亦可数也近年有陈镒王翺杨善王文马",
    "05-002 | 总督军务自总兵官以下悉听节制盖始于王靖远麓川之役己巳多事以来",
    "05-003 | 礼部尚书致仕毘陵胡公予赴广时谒之尚强徤取酒命酌因有请曰老先生",
    "05-004 | 国朝将官专生杀如都督韩观守广西尚然观师行庆远生员迎候悉命斩之",
    "05-005 | 广西守将韩都督观英武有文颇喜诛杀山忠毅公继之则光前絶后矣公深",
    "05-006 | 聂大年诗翰著名一时不得预京衔或曰大年尝署桃符云文章高似翰林院",
    "05-007 | 武安侯郑亨守大同年已七十余刚正有为一志为国而性稍每议事辄不",
    "05-008 | 兴安侯徐亨正统中守关中一日御史张文昌语及时将徐云以亨观今之将",
    "05-009 | 故事凡各部请勅行事该部备词奏请既得防移文翰林即今文渊阁下学士",
    "05-010 | 上复寳位二三日间诸文武首功之臣列侍文华殿上喜见眉宇呼诸臣曰弟",
    "05-011 | 张学士士谦夏太常仲昭两人同登第乡甚欵密皆及与陈嗣初王孟端诸",
    "05-012 | 近代杂书著述考据多不精如翰墨全书以彭思永为明道母舅事文聚以",
    "05-013 | 珍珠初采一万四千五百余两大约三石五斗次年采九千六百余两每百两",
    "05-014 | 范德机古见推当时近见廉州海角亭记为其自书无疑此碑亦用汉唐碑",
    "05-015 | 刘侍郎廉夫清余同年乡举自负文武才筹边论兵歴歴如见景泰初为庶吉",
    "05-016 | 文渊阁宥密之地外臣非公事不能至廷陛机宜无敢泄者杨文贞文定文敏",
    "05-017 | 广西总帅府一郑牢者老也性鲠直敢言都督韩观威严不可犯亦知牢观",
    "05-018 | 夏太常仲昭常闻之杨文敏公荣曰吾见人臣以伉直受祸者每深惜之事人",
    "05-019 | 近年大臣各醵白金送寺观祈报行礼云始于陈汝言万寿节亦然云始于杨",
    "05-020 | 耿恒庵云吴思庵集解小学翟黑子章取熊氏所解脱字二十一字可删盖吾",
    "05-021 | 李祭酒先生哭侄诗所谓朝餐对按浑无味暮骑逢人不记名其死生骨肉之",
    "05-022 | 中书舎人卢儒字为己号重齐昆山人博学能文善笔札文学韩栁书法欧顔",
    "05-023 | 景泰中盛奏旌褒用兵地方死节之臣以浙江都指挥脱纲佥事王晟为首盖",
    "05-024 | 吴人耕作或舟行之劳多作讴歌以自遣名唱山歌中亦多可为警劝者谩记",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
# 示例记录（保留作格式对照）：
# {"item_id": "01-001", "text": "礼部尚书", "type": "official", "normalized": "礼部尚书", "confidence": 0.97, "source": "原文片段"}

DATA = [
    # 05-001 左都御史沿革
    {"item_id": "05-001", "text": "左都御史", "type": "official", "normalized": "左都御史", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "05-001", "text": "刘观", "type": "person", "normalized": "刘观", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-001", "text": "陈镒", "type": "person", "normalized": "陈镒", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-001", "text": "王翺", "type": "person", "normalized": "王翺", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-001", "text": "杨善", "type": "person", "normalized": "杨善", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-001", "text": "王文", "type": "person", "normalized": "王文", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-001", "text": "马昻", "type": "person", "normalized": "马昻", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-001", "text": "萧维祯", "type": "person", "normalized": "萧维祯", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-001", "text": "寇深", "type": "person", "normalized": "寇深", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-001", "text": "轩輗", "type": "person", "normalized": "轩輗", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-001", "text": "刑部尚书", "type": "official", "normalized": "刑部尚书", "confidence": 0.85, "source": "原文片段"},
    # 05-002 总督军务沿革
    {"item_id": "05-002", "text": "总督军务", "type": "official", "normalized": "总督军务", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "05-002", "text": "总兵官", "type": "official", "normalized": "总兵官", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-002", "text": "王靖远", "type": "person", "normalized": "王骥（封靖远伯）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-002", "text": "麓川", "type": "place", "normalized": "麓川", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-002", "text": "侯尚书璡", "type": "person", "normalized": "侯璡（尚书）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-002", "text": "于少保", "type": "person", "normalized": "于谦（少保）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-002", "text": "石璞", "type": "person", "normalized": "石璞", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-002", "text": "王来", "type": "person", "normalized": "王来", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-002", "text": "两广", "type": "place", "normalized": "两广", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-002", "text": "湖贵", "type": "place", "normalized": "湖贵（湖广贵州）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-002", "text": "宣德", "type": "era", "normalized": "宣德（明宣宗年号）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-002", "text": "巡抚", "type": "official", "normalized": "巡抚", "confidence": 0.88, "source": "原文片段"},
    # 05-003 胡濙自述
    {"item_id": "05-003", "text": "礼部尚书", "type": "official", "normalized": "礼部尚书", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "05-003", "text": "致仕", "type": "official", "normalized": "致仕", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-003", "text": "毘陵胡公", "type": "person", "normalized": "胡濙（毗陵，礼部尚书）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "05-003", "text": "太宗", "type": "person", "normalized": "明成祖（太宗）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-003", "text": "东宫", "type": "person", "normalized": "东宫（太子）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-003", "text": "南京", "type": "place", "normalized": "南京", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "05-003", "text": "杨学士士奇", "type": "person", "normalized": "杨士奇（学士）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-003", "text": "锦衣", "type": "institution", "normalized": "锦衣卫", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-003", "text": "安庆", "type": "place", "normalized": "安庆", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-003", "text": "吏部", "type": "institution", "normalized": "吏部", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-003", "text": "礼部侍郎", "type": "official", "normalized": "礼部侍郎", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-003", "text": "都给事中", "type": "official", "normalized": "都给事中", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-003", "text": "宣宗皇帝", "type": "person", "normalized": "明宣宗", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-003", "text": "户部", "type": "institution", "normalized": "户部", "confidence": 0.85, "source": "原文片段"},
    # 05-004 将官专生杀
    {"item_id": "05-004", "text": "都督", "type": "official", "normalized": "都督", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-004", "text": "韩观", "type": "person", "normalized": "韩观（都督）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-004", "text": "广西", "type": "place", "normalized": "广西", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-004", "text": "庆远", "type": "place", "normalized": "庆远", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-004", "text": "山忠毅公", "type": "person", "normalized": "山忠毅（名待考）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "05-004", "text": "英国", "type": "person", "normalized": "英国公（张辅）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-004", "text": "杨洪", "type": "person", "normalized": "杨洪", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-004", "text": "石亨", "type": "person", "normalized": "石亨", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-004", "text": "百户", "type": "official", "normalized": "百户", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-004", "text": "额森", "type": "person", "normalized": "额森（也先）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-004", "text": "兵科", "type": "institution", "normalized": "兵科", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-004", "text": "王忠毅公", "type": "person", "normalized": "王骥（谥忠毅？即王靖远）", "confidence": 0.75, "source": "原文片段"},
    # 05-005 广西守将
    {"item_id": "05-005", "text": "韩都督观", "type": "person", "normalized": "韩观", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-005", "text": "山忠毅公", "type": "person", "normalized": "山忠毅", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "05-005", "text": "柳安远", "type": "person", "normalized": "柳安远（名待考）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "05-005", "text": "田州知府岑绍", "type": "person", "normalized": "岑绍（田州知府）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-005", "text": "岑镛", "type": "person", "normalized": "岑镛（岑绍幼子）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "05-005", "text": "陈旺", "type": "person", "normalized": "陈旺（都督）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "05-005", "text": "朱瑛", "type": "person", "normalized": "朱瑛（武进伯）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-005", "text": "土官", "type": "official", "normalized": "土官", "confidence": 0.85, "source": "原文片段"},
    # 05-006 聂大年
    {"item_id": "05-006", "text": "聂大年", "type": "person", "normalized": "聂大年", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-006", "text": "翰林院", "type": "institution", "normalized": "翰林院", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-006", "text": "按察司", "type": "institution", "normalized": "按察司", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-006", "text": "梅圣俞", "type": "person", "normalized": "梅尧臣（字圣俞）", "confidence": 0.82, "source": "原文片段"},
    # 05-007 郑亨守大同
    {"item_id": "05-007", "text": "武安侯郑亨", "type": "person", "normalized": "郑亨（封武安侯）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-007", "text": "大同", "type": "place", "normalized": "大同", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "05-007", "text": "中贵", "type": "person", "normalized": "中贵（太监）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-007", "text": "栢玉", "type": "person", "normalized": "柏玉（中贵）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "05-007", "text": "刘公琏", "type": "person", "normalized": "刘琏（侍郎）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-007", "text": "布政张文昌", "type": "person", "normalized": "张文昌（布政/断事）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "05-007", "text": "宣府", "type": "place", "normalized": "宣府", "confidence": 0.85, "source": "原文片段"},
    # 05-008 徐亨守关中
    {"item_id": "05-008", "text": "兴安侯徐亨", "type": "person", "normalized": "徐亨（封兴安侯）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-008", "text": "关中", "type": "place", "normalized": "关中", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-008", "text": "张文昌", "type": "person", "normalized": "张文昌（御史）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-008", "text": "成国公", "type": "person", "normalized": "成国公（朱勇）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-008", "text": "英国公", "type": "person", "normalized": "英国公（张辅）", "confidence": 0.85, "source": "原文片段"},
    # 05-009 请敕故事
    {"item_id": "05-009", "text": "文渊阁", "type": "place", "normalized": "文渊阁", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-009", "text": "景泰六年", "type": "era", "normalized": "景泰六年", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-009", "text": "独石", "type": "place", "normalized": "独石", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-009", "text": "兵部", "type": "institution", "normalized": "兵部", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-009", "text": "宣府总兵", "type": "official", "normalized": "宣府总兵官", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-009", "text": "阁老", "type": "person", "normalized": "阁老（权臣）", "confidence": 0.78, "source": "原文片段"},
    # 05-010 上复位
    {"item_id": "05-010", "text": "文华殿", "type": "place", "normalized": "文华殿", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-010", "text": "都督刘深", "type": "person", "normalized": "刘深（都督）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-010", "text": "左都督", "type": "official", "normalized": "左都督", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-010", "text": "征蛮将军印", "type": "official", "normalized": "征蛮将军印", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-010", "text": "广西", "type": "place", "normalized": "广西", "confidence": 0.85, "source": "原文片段"},
    # 05-011 张士谦夏仲昭
    {"item_id": "05-011", "text": "张学士士谦", "type": "person", "normalized": "张士谦（学士）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-011", "text": "夏太常仲昭", "type": "person", "normalized": "夏仲昭（太常）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-011", "text": "陈嗣初", "type": "person", "normalized": "陈嗣初", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "05-011", "text": "王孟端", "type": "person", "normalized": "王孟端（王绂）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-011", "text": "石渠阁", "type": "place", "normalized": "石渠阁", "confidence": 0.82, "source": "原文片段"},
    # 05-012 杂书考据/采珠
    {"item_id": "05-012", "text": "翰墨全书", "type": "work", "normalized": "翰墨全书", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-012", "text": "彭思永", "type": "person", "normalized": "彭思永", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-012", "text": "程明道", "type": "person", "normalized": "程颢（号明道）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-012", "text": "事文类聚", "type": "work", "normalized": "事文类聚", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-012", "text": "氏族大全", "type": "work", "normalized": "氏族大全", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-012", "text": "汤公让", "type": "person", "normalized": "汤公让（指挥）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "05-012", "text": "赵明诚", "type": "person", "normalized": "赵明诚", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-012", "text": "赵抃", "type": "person", "normalized": "赵抃", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-012", "text": "徐元玉", "type": "person", "normalized": "徐元玉", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-012", "text": "广州十贤", "type": "work", "normalized": "广州十贤（传）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "05-012", "text": "李商隐", "type": "person", "normalized": "李商隐（李商隠）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-012", "text": "珠池", "type": "place", "normalized": "珠池（采珠海池）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-012", "text": "永乐", "type": "era", "normalized": "永乐（明成祖年号）", "confidence": 0.88, "source": "原文片段"},
    # 05-013 珍珠采额
    {"item_id": "05-013", "text": "御史吕洪", "type": "person", "normalized": "吕洪（御史）", "confidence": 0.8, "source": "原文片段"},
    # 05-014 范德机碑
    {"item_id": "05-014", "text": "范德机", "type": "person", "normalized": "范梈（字德机）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-014", "text": "廉州海角亭记", "type": "work", "normalized": "廉州海角亭记（碑）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-014", "text": "廉州", "type": "place", "normalized": "廉州", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-014", "text": "范惇文", "type": "person", "normalized": "范惇文（高平）", "confidence": 0.78, "source": "原文片段"},
    # 05-015 刘廉夫
    {"item_id": "05-015", "text": "刘侍郎廉夫", "type": "person", "normalized": "刘廉夫（侍郎）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-015", "text": "景泰初", "type": "era", "normalized": "景泰初", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-015", "text": "庶吉士", "type": "official", "normalized": "庶吉士", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-015", "text": "刑部右侍郎", "type": "official", "normalized": "刑部右侍郎", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-015", "text": "四川参政", "type": "official", "normalized": "四川布政司参政", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-015", "text": "四川", "type": "place", "normalized": "四川", "confidence": 0.85, "source": "原文片段"},
    # 05-016 文渊阁宥密
    {"item_id": "05-016", "text": "文渊阁", "type": "place", "normalized": "文渊阁", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-016", "text": "杨文贞", "type": "person", "normalized": "杨士奇（谥文贞）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-016", "text": "杨文定", "type": "person", "normalized": "杨溥（谥文定）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-016", "text": "杨文敏", "type": "person", "normalized": "杨荣（谥文敏）", "confidence": 0.85, "source": "原文片段"},
    # 05-017 郑牢
    {"item_id": "05-017", "text": "郑牢", "type": "person", "normalized": "郑牢（广西总帅府老隶）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-017", "text": "韩观", "type": "person", "normalized": "韩观（都督）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-017", "text": "山忠毅公", "type": "person", "normalized": "山忠毅", "confidence": 0.78, "source": "原文片段"},
    # 05-018 夏仲昭/杨文敏
    {"item_id": "05-018", "text": "夏太常仲昭", "type": "person", "normalized": "夏仲昭（太常）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-018", "text": "杨文敏公荣", "type": "person", "normalized": "杨荣（谥文敏）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-018", "text": "千文", "type": "work", "normalized": "千文（千字文）", "confidence": 0.82, "source": "原文片段"},
    # 05-019 醵金送寺观/于节庵
    {"item_id": "05-019", "text": "陈汝言", "type": "person", "normalized": "陈汝言", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-019", "text": "杨鸿胪", "type": "person", "normalized": "杨鸿胪（名待考）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "05-019", "text": "石亨", "type": "person", "normalized": "石亨", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-019", "text": "于节庵", "type": "person", "normalized": "于谦（号节庵）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "05-019", "text": "河南山西", "type": "place", "normalized": "河南山西（巡抚）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-019", "text": "大理少卿", "type": "official", "normalized": "大理少卿", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-019", "text": "兵部侍郎", "type": "official", "normalized": "兵部侍郎", "confidence": 0.85, "source": "原文片段"},
    # 05-020 小学解
    {"item_id": "05-020", "text": "耿恒庵", "type": "person", "normalized": "耿恒庵", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "05-020", "text": "吴思庵", "type": "person", "normalized": "吴思庵", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-020", "text": "小学", "type": "work", "normalized": "小学（朱熹辑）", "confidence": 0.85, "source": "原文片段"},
    # 05-021 李祭酒哭侄
    {"item_id": "05-021", "text": "李祭酒", "type": "person", "normalized": "李祭酒（名待考）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "05-021", "text": "祭十二郎文", "type": "work", "normalized": "祭十二郎文（韩愈）", "confidence": 0.82, "source": "原文片段"},
    # 05-022 卢儒
    {"item_id": "05-022", "text": "中书舍人卢儒", "type": "person", "normalized": "卢儒（字为己，号重斋，昆山）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-022", "text": "昆山", "type": "place", "normalized": "昆山", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "05-022", "text": "萧状元", "type": "person", "normalized": "萧状元（名待考）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "05-022", "text": "雪赋", "type": "work", "normalized": "雪赋", "confidence": 0.8, "source": "原文片段"},
    # 05-023 旌褒死节
    {"item_id": "05-023", "text": "盛", "type": "person", "normalized": "叶盛（盛）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "05-023", "text": "脱纲", "type": "person", "normalized": "脱纲（浙江都指挥）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-023", "text": "王晟", "type": "person", "normalized": "王晟（佥事）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-023", "text": "都指挥", "type": "official", "normalized": "都指挥", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-023", "text": "佥事", "type": "official", "normalized": "佥事", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-023", "text": "林廷举", "type": "person", "normalized": "林廷举（御史）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "05-023", "text": "两浙", "type": "place", "normalized": "两浙", "confidence": 0.82, "source": "原文片段"},
    # 05-024 唱山歌
    {"item_id": "05-024", "text": "吴人", "type": "place", "normalized": "吴人（苏州一带）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "05-024", "text": "唱山歌", "type": "work", "normalized": "唱山歌（吴地民歌）", "confidence": 0.82, "source": "原文片段"},
]
