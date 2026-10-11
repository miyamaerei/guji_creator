# -*- coding: utf-8 -*-
"""《水东日记》卷 06 —— L1 实体标注 源数据（AI 判定逐条填写）

说明：实体标注：每条记录标注该条目中的实体（text=原文字面，type=实体类型，normalized=归一词形，confidence=置信度）

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：person=人物 / official=职官名 / institution=机构衙门 / place=地名 / era=年号朝代 / posthumous=谥号 / work=书名文献名 / unknown=类型待定
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

# 字段键（打包器校验用）：text, type, normalized, confidence, source
# 示例记录（保留作格式对照）：
# {"item_id": "01-001", "text": "礼部尚书", "type": "official", "normalized": "礼部尚书", "confidence": 0.97, "source": "原文片段"}

DATA = [
    # 06-001 叅赞军务沿革
    {"item_id": "06-001", "text": "叅赞军务", "type": "official", "normalized": "叅赞军务（参赞军务）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "06-001", "text": "洪熙初元", "type": "era", "normalized": "洪熙（明仁宗年号）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "06-001", "text": "沈固", "type": "person", "normalized": "沈固（丹阳，户部尚书致仕）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-001", "text": "刘琏", "type": "person", "normalized": "刘琏（昆山，户部侍郎）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-001", "text": "周颐", "type": "person", "normalized": "周颐（会稽，福建布政）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-001", "text": "刘绍", "type": "person", "normalized": "刘绍（副使，人称刘司马）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "06-001", "text": "王靖远", "type": "person", "normalized": "王骥（封靖远伯）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-001", "text": "白圭", "type": "person", "normalized": "白圭（都御史）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-001", "text": "颜彪", "type": "person", "normalized": "颜彪（征夷将军总兵官都督佥事）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-001", "text": "盛", "type": "person", "normalized": "叶盛（盛）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "06-001", "text": "户部尚书", "type": "official", "normalized": "户部尚书", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "06-001", "text": "宣府", "type": "place", "normalized": "宣府", "confidence": 0.85, "source": "原文片段"},
    # 06-002 颜征夷/马良
    {"item_id": "06-002", "text": "颜征夷", "type": "person", "normalized": "颜彪（征夷将军）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-002", "text": "马良", "type": "person", "normalized": "马良（都指挥）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-002", "text": "御马监", "type": "institution", "normalized": "御马监", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-002", "text": "宁阳侯", "type": "person", "normalized": "宁阳侯（陈懋）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-002", "text": "刘静修", "type": "person", "normalized": "刘因（号静修）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-002", "text": "岳珂", "type": "person", "normalized": "岳珂", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-002", "text": "欧阳子", "type": "person", "normalized": "欧阳修（欧阳子）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-002", "text": "钱思公", "type": "person", "normalized": "钱惟演（思公）", "confidence": 0.78, "source": "原文片段"},
    # 06-003 范信兵
    {"item_id": "06-003", "text": "叅将范信", "type": "person", "normalized": "范信（参将）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-003", "text": "大同", "type": "place", "normalized": "大同", "confidence": 0.88, "source": "原文片段"},
    # 06-004 沈琮
    {"item_id": "06-004", "text": "沈琮", "type": "person", "normalized": "沈琮（广州知府）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-004", "text": "南京兵部武库司", "type": "institution", "normalized": "南京兵部武库司", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-004", "text": "魏公骥", "type": "person", "normalized": "魏骥（尚书）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-004", "text": "轩公輗", "type": "person", "normalized": "轩輗（都御史）", "confidence": 0.85, "source": "原文片段"},
    # 06-005 颜总戎/李名远梁万方
    {"item_id": "06-005", "text": "颜总戎", "type": "person", "normalized": "颜彪（总戎）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-005", "text": "李名远", "type": "person", "normalized": "李名远（右卫军）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "06-005", "text": "梁万方", "type": "person", "normalized": "梁万方（右卫军）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "06-005", "text": "周宁", "type": "person", "normalized": "周宁（右卫百户）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "06-005", "text": "刘升", "type": "person", "normalized": "刘升（右卫百户）", "confidence": 0.78, "source": "原文片段"},
    # 06-006 六科衙门
    {"item_id": "06-006", "text": "六科衙门", "type": "institution", "normalized": "六科（给事中署）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "06-006", "text": "尚宝司", "type": "institution", "normalized": "尚宝司", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-006", "text": "午门", "type": "place", "normalized": "午门", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-006", "text": "五府六部都察院六科给事中", "type": "institution", "normalized": "五府六部都察院六科给事中", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-006", "text": "马显", "type": "person", "normalized": "马显（户科都给事中）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-006", "text": "喜信", "type": "person", "normalized": "喜信（都督，回回人）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "06-006", "text": "和勇", "type": "person", "normalized": "和勇（两广游击将军都督同知）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-006", "text": "阿噜台", "type": "person", "normalized": "阿鲁台（鞑靼）", "confidence": 0.8, "source": "原文片段"},
    # 06-007 候朝直房
    {"item_id": "06-007", "text": "大理寺", "type": "institution", "normalized": "大理寺", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-007", "text": "顾公佐", "type": "person", "normalized": "顾佐（都御史）", "confidence": 0.85, "source": "原文片段"},
    # 06-008 土地祠/试录
    {"item_id": "06-008", "text": "萧王", "type": "person", "normalized": "萧何（酂侯，仓神）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-008", "text": "吉知陀圣母", "type": "person", "normalized": "吉知陀圣母（厫神配）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "06-008", "text": "桂林府仓", "type": "place", "normalized": "广西桂林府仓", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-008", "text": "周文襄公", "type": "person", "normalized": "周忱（谥文襄，苏松）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-008", "text": "德庆州儒学", "type": "institution", "normalized": "广东德庆州儒学", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-008", "text": "赵师旦", "type": "person", "normalized": "赵师旦", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-008", "text": "霍端友", "type": "person", "normalized": "霍端友（宋崇宁状元）", "confidence": 0.78, "source": "原文片段"},
    # 06-009 陈汝言
    {"item_id": "06-009", "text": "陈汝言", "type": "person", "normalized": "陈汝言", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-009", "text": "唐太宗", "type": "person", "normalized": "唐太宗（李世民）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-009", "text": "曾状元", "type": "person", "normalized": "曾棨（状元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-009", "text": "侍讲学士", "type": "official", "normalized": "侍讲学士", "confidence": 0.82, "source": "原文片段"},
    # 06-010 孙状元
    {"item_id": "06-010", "text": "孙状元贤", "type": "person", "normalized": "孙贤（状元）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-010", "text": "驸马都尉周景", "type": "person", "normalized": "周景（驸马都尉）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-010", "text": "永平", "type": "place", "normalized": "永平", "confidence": 0.8, "source": "原文片段"},
    # 06-011 肃政匾
    {"item_id": "06-011", "text": "都察院", "type": "institution", "normalized": "都察院", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "06-011", "text": "建文", "type": "era", "normalized": "建文（明惠帝年号）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-011", "text": "正统", "type": "era", "normalized": "正统（明英宗年号）", "confidence": 0.88, "source": "原文片段"},
    # 06-012 周新
    {"item_id": "06-012", "text": "周新", "type": "person", "normalized": "周新（浙江按察使）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "06-012", "text": "浙江按察使", "type": "official", "normalized": "浙江按察使", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-012", "text": "纪纲", "type": "person", "normalized": "纪纲（锦衣卫）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-012", "text": "仁庙", "type": "person", "normalized": "明仁宗（仁庙）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-012", "text": "叶惟洁", "type": "person", "normalized": "叶惟洁（南京太仆丞）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "06-012", "text": "宗行", "type": "person", "normalized": "宗行（钱塘知县）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "06-012", "text": "阮随", "type": "person", "normalized": "阮随（监丞）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "06-012", "text": "陈濂", "type": "person", "normalized": "陈濂（广东佥事）", "confidence": 0.8, "source": "原文片段"},
    # 06-013 春帖
    {"item_id": "06-013", "text": "春帖", "type": "work", "normalized": "春帖（春联）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-013", "text": "丁丑", "type": "era", "normalized": "丁丑（天顺元年）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-013", "text": "京闱", "type": "place", "normalized": "京闱（顺天乡试）", "confidence": 0.82, "source": "原文片段"},
    # 06-014 太祖/样房
    {"item_id": "06-014", "text": "太祖皇帝", "type": "person", "normalized": "明太祖（洪武）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "06-014", "text": "开济", "type": "person", "normalized": "开济（刑部尚书）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-014", "text": "刑部尚书", "type": "official", "normalized": "刑部尚书", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "06-014", "text": "金陵", "type": "place", "normalized": "金陵（南京）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-014", "text": "萧公", "type": "person", "normalized": "萧维祯（前左都御史）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-014", "text": "古廉李先生", "type": "person", "normalized": "李时勉（号古廉，祭酒）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-014", "text": "孙鼎", "type": "person", "normalized": "孙鼎（诗义集说）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "06-014", "text": "东里杨先生", "type": "person", "normalized": "杨士奇（号东里）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-014", "text": "吴祭酒节", "type": "person", "normalized": "吴节（祭酒）", "confidence": 0.8, "source": "原文片段"},
    # 06-015 于谦
    {"item_id": "06-015", "text": "侍郎于公", "type": "person", "normalized": "于谦（巡抚河南山西）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "06-015", "text": "海丰王公", "type": "person", "normalized": "王（海丰，户部尚书）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "06-015", "text": "孙原贞", "type": "person", "normalized": "孙原贞（参政）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-015", "text": "王来", "type": "person", "normalized": "王来", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-015", "text": "罗绮", "type": "person", "normalized": "罗绮（四川侍郎）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-015", "text": "寇深", "type": "person", "normalized": "寇深（都宪）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-015", "text": "李秉", "type": "person", "normalized": "李秉（都宪）", "confidence": 0.82, "source": "原文片段"},
    # 06-016 陈祭酒/卢睿
    {"item_id": "06-016", "text": "陈先生", "type": "person", "normalized": "陈祭酒（云间）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "06-016", "text": "黄翰", "type": "person", "normalized": "黄翰（前按察使）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "06-016", "text": "卢睿", "type": "person", "normalized": "卢睿（都御史）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-016", "text": "杨文敏", "type": "person", "normalized": "杨荣（谥文敏）", "confidence": 0.85, "source": "原文片段"},
    # 06-017 郏亶
    {"item_id": "06-017", "text": "郏亶", "type": "person", "normalized": "郏亶（字正夫，昆山）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-017", "text": "熙宁", "type": "era", "normalized": "熙宁（宋神宗年号）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-017", "text": "昆山", "type": "place", "normalized": "昆山", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-017", "text": "广州新城记", "type": "work", "normalized": "郏亶修东城记（广州新城）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-017", "text": "吕居简", "type": "person", "normalized": "吕居简（龙图直学士）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-017", "text": "王靖之", "type": "person", "normalized": "王靖之（转运使）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "06-017", "text": "袁子英", "type": "person", "normalized": "袁子英", "confidence": 0.78, "source": "原文片段"},
    # 06-021 高季迪/王冕
    {"item_id": "06-021", "text": "杨文定", "type": "person", "normalized": "杨溥（谥文定）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-021", "text": "范文正", "type": "person", "normalized": "范仲淹（谥文正）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-021", "text": "高季迪", "type": "person", "normalized": "高启（字季迪）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-021", "text": "姑苏", "type": "place", "normalized": "姑苏（苏州）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-021", "text": "王冕元章", "type": "person", "normalized": "王冕（字元章）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-021", "text": "宋潜溪", "type": "person", "normalized": "宋濂（号潜溪）", "confidence": 0.82, "source": "原文片段"},
    # 06-022 陶九成
    {"item_id": "06-022", "text": "陶九成", "type": "person", "normalized": "陶宗仪（字九成，号南村）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-022", "text": "书史会要", "type": "work", "normalized": "书史会要（陶宗仪）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-022", "text": "南村辍耕录", "type": "work", "normalized": "南村辍耕录（陶宗仪）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-022", "text": "说郛", "type": "work", "normalized": "说郛（陶宗仪辑百卷）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-022", "text": "天台", "type": "place", "normalized": "天台", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-022", "text": "独石", "type": "place", "normalized": "独石", "confidence": 0.82, "source": "原文片段"},
    # 06-023 陈智
    {"item_id": "06-023", "text": "陈智", "type": "person", "normalized": "陈智（都御史）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "06-023", "text": "御史", "type": "official", "normalized": "御史", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "06-023", "text": "教官", "type": "official", "normalized": "教官", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-023", "text": "曹泰", "type": "person", "normalized": "曹泰（坐言灾异）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "06-023", "text": "魏骥", "type": "person", "normalized": "魏骥（尚书）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "06-023", "text": "年富", "type": "person", "normalized": "年富（尚书）", "confidence": 0.85, "source": "原文片段"},
]
