# -*- coding: utf-8 -*-
"""《水东日记》卷 07 —— L1 实体标注 源数据（AI 判定逐条填写）

说明：实体标注：每条记录标注该条目中的实体（text=原文字面，type=实体类型，normalized=归一词形，confidence=置信度）

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：person=人物 / official=职官名 / institution=机构衙门 / place=地名 / era=年号朝代 / posthumous=谥号 / work=书名文献名 / unknown=类型待定
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

# 字段键（打包器校验用）：text, type, normalized, confidence, source
# 示例记录（保留作格式对照）：
# {"item_id": "01-001", "text": "礼部尚书", "type": "official", "normalized": "礼部尚书", "confidence": 0.97, "source": "原文片段"}

DATA = [
    # 07-001 天寿山/沐敬
    {"item_id": "07-001", "text": "太宗皇帝", "type": "person", "normalized": "明成祖（永乐）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "07-001", "text": "天寿山", "type": "place", "normalized": "天寿山（明陵）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-001", "text": "皇太子", "type": "person", "normalized": "明仁宗（仁庙，皇太子）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-001", "text": "汉赵二王", "type": "person", "normalized": "汉王/赵王（永乐弟）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-001", "text": "皇太孙", "type": "person", "normalized": "明宣宗（宣庙，皇太孙）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-001", "text": "沙河", "type": "place", "normalized": "沙河", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-001", "text": "沐敬", "type": "person", "normalized": "沐敬（太监）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-001", "text": "钱原溥", "type": "person", "normalized": "钱原溥（学士）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-001", "text": "交南", "type": "place", "normalized": "交南（交阯）", "confidence": 0.82, "source": "原文片段"},
    # 07-002 赏花集
    {"item_id": "07-002", "text": "刘学士", "type": "person", "normalized": "刘学士（永新）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "07-002", "text": "刘寅之", "type": "person", "normalized": "刘寅之（行人，刘学士弟）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "07-002", "text": "倪学士", "type": "person", "normalized": "倪学士（戍开平）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "07-002", "text": "黄学士", "type": "person", "normalized": "黄学士（降广州通判）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "07-002", "text": "开平", "type": "place", "normalized": "开平", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-002", "text": "广州通判", "type": "official", "normalized": "广州通判", "confidence": 0.8, "source": "原文片段"},
    # 07-003 交阯
    {"item_id": "07-003", "text": "交阯", "type": "place", "normalized": "交阯（安南）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-003", "text": "国子监", "type": "institution", "normalized": "国子监", "confidence": 0.85, "source": "原文片段"},
    # 07-004 薛简肃五女
    {"item_id": "07-004", "text": "薛简肃公", "type": "person", "normalized": "薛奎（谥简肃）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-004", "text": "王拱辰", "type": "person", "normalized": "王拱辰", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-004", "text": "欧阳公", "type": "person", "normalized": "欧阳修", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "07-004", "text": "瞿佑", "type": "person", "normalized": "瞿佑（山阳）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-004", "text": "陈璲", "type": "person", "normalized": "陈璲（北海佥事）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-004", "text": "陈登", "type": "person", "normalized": "陈登（善谑）", "confidence": 0.78, "source": "原文片段"},
    # 07-005 欧阳帖
    {"item_id": "07-005", "text": "苏长公", "type": "person", "normalized": "苏轼（号长公）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-005", "text": "叶石林", "type": "person", "normalized": "叶梦得（号石林）", "confidence": 0.82, "source": "原文片段"},
    # 07-006 星命
    {"item_id": "07-006", "text": "富郑公", "type": "person", "normalized": "富弼（封郑公）", "confidence": 0.85, "source": "原文片段"},
    # 07-007 陈僖敏
    {"item_id": "07-007", "text": "陈僖敏公", "type": "person", "normalized": "陈镒（谥僖敏）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-007", "text": "陕西", "type": "place", "normalized": "陕西", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-007", "text": "王文少保", "type": "person", "normalized": "王翱（谥忠肃，少保）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-007", "text": "金荣襄", "type": "person", "normalized": "金濂（谥荣襄）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-007", "text": "按察使", "type": "official", "normalized": "按察使", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-007", "text": "副使", "type": "official", "normalized": "按察副使", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-007", "text": "袁旭", "type": "person", "normalized": "袁旭", "confidence": 0.78, "source": "原文片段"},
    # 07-008 司马温公
    {"item_id": "07-008", "text": "司马温公", "type": "person", "normalized": "司马光（谥温公）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "07-008", "text": "吕惠卿", "type": "person", "normalized": "吕惠卿", "confidence": 0.82, "source": "原文片段"},
    # 07-009 范文正碑
    {"item_id": "07-009", "text": "范文正", "type": "person", "normalized": "范仲淹（谥文正）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-009", "text": "富韩公", "type": "person", "normalized": "富弼（封韩公）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-009", "text": "沈简庵", "type": "person", "normalized": "沈简庵", "confidence": 0.78, "source": "原文片段"},
    # 07-010 黄公/杨公
    {"item_id": "07-010", "text": "东莱黄公", "type": "person", "normalized": "黄公（东莱，少保户部尚书）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-010", "text": "襄城伯", "type": "person", "normalized": "襄城伯（李）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-010", "text": "庐陵杨公", "type": "person", "normalized": "杨士奇（庐陵，少师）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-010", "text": "武林", "type": "place", "normalized": "武林（杭州）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-010", "text": "马侍郎愉", "type": "person", "normalized": "马愉（侍郎）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-010", "text": "徐武功", "type": "person", "normalized": "徐有贞（封武功伯）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-010", "text": "李宫保", "type": "person", "normalized": "李贤（宫保）", "confidence": 0.82, "source": "原文片段"},
    # 07-012 印信
    {"item_id": "07-012", "text": "印史", "type": "work", "normalized": "印史（论印之书）", "confidence": 0.78, "source": "原文片段"},
    # 07-013 名印
    {"item_id": "07-013", "text": "草庐吴公", "type": "person", "normalized": "吴澄（号草庐）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-013", "text": "揭文安公", "type": "person", "normalized": "揭傒斯（谥文安）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-013", "text": "赵文敏", "type": "person", "normalized": "赵孟頫（谥文敏）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-013", "text": "李息斋", "type": "person", "normalized": "李衎（号息斋）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-013", "text": "袁子方", "type": "person", "normalized": "袁子方", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "07-013", "text": "鲜于伯几", "type": "person", "normalized": "鲜于枢（字伯几）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-013", "text": "吾子行", "type": "person", "normalized": "吾丘衍（字子行）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-013", "text": "魏国夫人", "type": "person", "normalized": "魏国夫人（管道昇）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-013", "text": "张绅", "type": "person", "normalized": "张绅（云门山樵）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-013", "text": "朱伯盛", "type": "person", "normalized": "朱珪（字伯盛，昆山）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-013", "text": "昆山", "type": "place", "normalized": "昆山", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-013", "text": "杭州", "type": "place", "normalized": "杭州", "confidence": 0.85, "source": "原文片段"},
    # 07-014 玺宝/玉带生
    {"item_id": "07-014", "text": "皇太后遗诰", "type": "work", "normalized": "皇太后遗诰", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-014", "text": "皇后制书", "type": "work", "normalized": "皇后制书", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-014", "text": "李学士贤", "type": "person", "normalized": "李贤（学士）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-014", "text": "赵尚书荣", "type": "person", "normalized": "赵荣（尚书）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-014", "text": "杨侍郎鼎", "type": "person", "normalized": "杨鼎（侍郎）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-014", "text": "刘廷美", "type": "person", "normalized": "刘廷美（主事）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "07-014", "text": "玉带生", "type": "work", "normalized": "玉带生（文天祥砚）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-014", "text": "文天祥", "type": "person", "normalized": "文天祥（庐陵宋丞相）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "07-014", "text": "谢翺", "type": "person", "normalized": "谢翺（号冬青）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-014", "text": "黄溍", "type": "person", "normalized": "黄溍（太史）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-014", "text": "杨维桢", "type": "person", "normalized": "杨维桢（号铁崖）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-014", "text": "张宪", "type": "person", "normalized": "张宪（号玉笥生）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-014", "text": "朱芾", "type": "person", "normalized": "朱芾（号沧洲生）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-014", "text": "庐陵", "type": "place", "normalized": "庐陵", "confidence": 0.82, "source": "原文片段"},
    # 07-015 仲尼/优人
    {"item_id": "07-015", "text": "仲尼", "type": "person", "normalized": "孔子（字仲尼）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "07-015", "text": "陈通政琏", "type": "person", "normalized": "陈琏（通政）", "confidence": 0.8, "source": "原文片段"},
    # 07-016 丰布政
    {"item_id": "07-016", "text": "丰文庆", "type": "person", "normalized": "丰文庆（布政）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-016", "text": "鄞", "type": "place", "normalized": "鄞（宁波）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-016", "text": "丰清敏公", "type": "person", "normalized": "丰稷（谥清敏）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-016", "text": "奉化", "type": "place", "normalized": "奉化", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-016", "text": "定海", "type": "place", "normalized": "定海", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-016", "text": "九江德化", "type": "place", "normalized": "九江德化", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-016", "text": "袁桷", "type": "person", "normalized": "袁桷（学士）", "confidence": 0.82, "source": "原文片段"},
    # 07-017 沈孟端
    {"item_id": "07-017", "text": "沈孟端", "type": "person", "normalized": "沈孟端（名方，世医）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-017", "text": "杨鼎", "type": "person", "normalized": "杨鼎（右侍郎）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-017", "text": "黄琛", "type": "person", "normalized": "黄琛（左布政）", "confidence": 0.82, "source": "原文片段"},
    # 07-018 陈嗣初
    {"item_id": "07-018", "text": "陈检讨嗣初", "type": "person", "normalized": "陈嗣初（检讨）", "confidence": 0.82, "source": "原文片段"},
    # 07-019 己巳南迁
    {"item_id": "07-019", "text": "己巳", "type": "era", "normalized": "己巳（正统十四年）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "07-019", "text": "金英", "type": "person", "normalized": "金英（太监）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-019", "text": "于谦", "type": "person", "normalized": "于谦（监察御史）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "07-019", "text": "寇准", "type": "person", "normalized": "寇准", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-019", "text": "王钦若", "type": "person", "normalized": "王钦若", "confidence": 0.82, "source": "原文片段"},
    # 07-020 何文渊
    {"item_id": "07-020", "text": "何文渊", "type": "person", "normalized": "何文渊", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-020", "text": "壬申", "type": "era", "normalized": "壬申（景泰三年易储）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "07-020", "text": "陈泰", "type": "person", "normalized": "陈泰（广东副使）", "confidence": 0.82, "source": "原文片段"},
    # 07-021 苏武李陵
    {"item_id": "07-021", "text": "苏武", "type": "person", "normalized": "苏武", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "07-021", "text": "李陵", "type": "person", "normalized": "李陵", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-021", "text": "喜宁", "type": "person", "normalized": "喜宁（叛阉）", "confidence": 0.82, "source": "原文片段"},
    # 07-022 蔡琰图
    {"item_id": "07-022", "text": "钱选", "type": "person", "normalized": "钱选（字舜举）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-022", "text": "蔡琰", "type": "person", "normalized": "蔡琰（文姬）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "07-022", "text": "夏佑", "type": "person", "normalized": "夏佑（字存贤，临海丞）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "07-022", "text": "蔡中郎", "type": "person", "normalized": "蔡邕（中郎）", "confidence": 0.85, "source": "原文片段"},
]
