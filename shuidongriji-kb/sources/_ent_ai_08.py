# -*- coding: utf-8 -*-
"""《水东日记》卷 08 —— L1 实体标注 源数据（AI 判定逐条填写）

说明：实体标注：每条记录标注该条目中的实体（text=原文字面，type=实体类型，normalized=归一词形，confidence=置信度）

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：person=人物 / official=职官名 / institution=机构衙门 / place=地名 / era=年号朝代 / posthumous=谥号 / work=书名文献名 / unknown=类型待定
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

# 字段键（打包器校验用）：text, type, normalized, confidence, source
# 示例记录（保留作格式对照）：
# {"item_id": "01-001", "text": "礼部尚书", "type": "official", "normalized": "礼部尚书", "confidence": 0.97, "source": "原文片段"}

DATA = [
    # 08-001 刘先生祭酒
    {"item_id": "08-001", "text": "刘先生", "type": "person", "normalized": "刘（詹事，简静端确）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "08-001", "text": "祭酒", "type": "official", "normalized": "国子监祭酒", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "08-001", "text": "吕洪", "type": "person", "normalized": "吕洪（御史）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-001", "text": "高世用", "type": "person", "normalized": "高世用", "confidence": 0.78, "source": "原文片段"},
    # 08-002 张翼
    {"item_id": "08-002", "text": "张翼", "type": "person", "normalized": "张翼（字文翔，太仓）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-002", "text": "太仓", "type": "place", "normalized": "太仓", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-002", "text": "开平", "type": "place", "normalized": "开平", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-002", "text": "欧颜", "type": "person", "normalized": "欧阳询、颜真卿", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-002", "text": "龙门谏院题名记", "type": "work", "normalized": "龙门谏院题名记", "confidence": 0.78, "source": "原文片段"},
    # 08-003 衣和庵
    {"item_id": "08-003", "text": "衣和庵主", "type": "person", "normalized": "衣和庵主（昆山，隐者）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "08-003", "text": "雪窦", "type": "place", "normalized": "雪窦（山）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-003", "text": "栖云", "type": "place", "normalized": "栖云（庵名）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "08-003", "text": "二灵", "type": "place", "normalized": "二灵（山）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "08-003", "text": "大德丁未", "type": "era", "normalized": "大德丁未（元成宗大德十一年）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "08-003", "text": "奉化志", "type": "work", "normalized": "奉化志", "confidence": 0.8, "source": "原文片段"},
    # 08-004 孙子良/杨相
    {"item_id": "08-004", "text": "孙子良", "type": "person", "normalized": "孙子良（海宁，山东参政）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-004", "text": "海宁", "type": "place", "normalized": "海宁", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-004", "text": "杨相", "type": "person", "normalized": "杨相（西昌，同年进士）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "08-004", "text": "谷府", "type": "person", "normalized": "谷王（府）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "08-004", "text": "东里杨公", "type": "person", "normalized": "杨士奇（号东里）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-004", "text": "陈智", "type": "person", "normalized": "陈智（都御史）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-004", "text": "李庸", "type": "person", "normalized": "李庸", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "08-004", "text": "成规", "type": "person", "normalized": "成规（苏州御史）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "08-004", "text": "章珪", "type": "person", "normalized": "章珪（敢言之士）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "08-004", "text": "杨仲举", "type": "person", "normalized": "杨仲举（王府长史）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "08-004", "text": "耿公", "type": "person", "normalized": "耿公（右都御史）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "08-004", "text": "孙状元贤", "type": "person", "normalized": "孙贤（状元）", "confidence": 0.82, "source": "原文片段"},
    # 08-005 郑府婚启
    {"item_id": "08-005", "text": "郑太师府", "type": "person", "normalized": "郑太师（宋郑居中家族）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "08-005", "text": "开封府开封县", "type": "place", "normalized": "开封府开封县", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-005", "text": "昆山", "type": "place", "normalized": "昆山", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-005", "text": "沂国文正公", "type": "person", "normalized": "沂国文正公（宋郑珏？）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "08-005", "text": "景定元年", "type": "era", "normalized": "景定元年（宋理宗）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-005", "text": "文康", "type": "person", "normalized": "文康（七世裔孙进士）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "08-005", "text": "梧州", "type": "place", "normalized": "梧州", "confidence": 0.8, "source": "原文片段"},
    # 08-006 苏长公诗
    {"item_id": "08-006", "text": "苏长公", "type": "person", "normalized": "苏轼（号长公）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-006", "text": "王定国", "type": "person", "normalized": "王定国（王巩）", "confidence": 0.82, "source": "原文片段"},
    # 08-007 顾佐魏源
    {"item_id": "08-007", "text": "顾公佐", "type": "person", "normalized": "顾佐（太康，右都御史）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "08-007", "text": "太康", "type": "place", "normalized": "太康", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-007", "text": "洪武庚辰", "type": "era", "normalized": "洪武庚辰（洪武三十三年，1400）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-007", "text": "庄浪令", "type": "official", "normalized": "庄浪令", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "08-007", "text": "江西按察司副使", "type": "official", "normalized": "江西按察司副使", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-007", "text": "应天府尹", "type": "official", "normalized": "应天府尹", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-007", "text": "通政司", "type": "institution", "normalized": "通政司", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-007", "text": "魏公源", "type": "person", "normalized": "魏源（南昌，刑部尚书）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-007", "text": "刑部尚书", "type": "official", "normalized": "刑部尚书", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "08-007", "text": "河南左布政使", "type": "official", "normalized": "河南左布政使", "confidence": 0.82, "source": "原文片段"},
    # 08-008 宋濂方孝孺
    {"item_id": "08-008", "text": "宋景濂", "type": "person", "normalized": "宋濂（字景濂）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-008", "text": "方孝孺", "type": "person", "normalized": "方孝孺", "confidence": 0.85, "source": "原文片段"},
    # 08-009 范仲淹家谱/范信
    {"item_id": "08-009", "text": "范仲淹", "type": "person", "normalized": "范仲淹（唐相履之后）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "08-009", "text": "咸通十一年", "type": "era", "normalized": "咸通十一年（唐懿宗）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-009", "text": "处州丽水县丞", "type": "official", "normalized": "处州丽水县丞", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-009", "text": "皇祐三年", "type": "era", "normalized": "皇祐三年（宋仁宗）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-009", "text": "范信", "type": "person", "normalized": "范信（广西叅将都指挥使）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-009", "text": "纯仁", "type": "person", "normalized": "范纯仁（范仲淹子）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-009", "text": "辰州教授", "type": "official", "normalized": "辰州教授", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "08-009", "text": "密云", "type": "place", "normalized": "密云", "confidence": 0.8, "source": "原文片段"},
    # 08-010 梁禋陈汝
    {"item_id": "08-010", "text": "梁禋", "type": "person", "normalized": "梁禋（翰林编修）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-010", "text": "陈汝同", "type": "person", "normalized": "陈汝同（国子祭酒致仕，号古庵）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-010", "text": "黄瑜", "type": "person", "normalized": "黄瑜（肇庆知府）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "08-010", "text": "肇庆知府", "type": "official", "normalized": "肇庆知府", "confidence": 0.8, "source": "原文片段"},
    # 08-011 杨文贞遗嘱
    {"item_id": "08-011", "text": "杨文贞公", "type": "person", "normalized": "杨士奇（谥文贞）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "08-011", "text": "王抑庵", "type": "person", "normalized": "王直（号抑庵，尚书）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-011", "text": "王忠毅", "type": "person", "normalized": "王骥（谥忠毅）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-011", "text": "徐尚书", "type": "person", "normalized": "徐尚书", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "08-011", "text": "龙州", "type": "place", "normalized": "龙州", "confidence": 0.8, "source": "原文片段"},
    # 08-012 黄霸丙吉
    {"item_id": "08-012", "text": "黄霸", "type": "person", "normalized": "黄霸（汉丞相）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-012", "text": "丙吉", "type": "person", "normalized": "丙吉（汉丞相）", "confidence": 0.85, "source": "原文片段"},
    # 08-014 赤壁赋
    {"item_id": "08-014", "text": "东坡", "type": "person", "normalized": "苏轼（号东坡）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "08-014", "text": "傅尧俞", "type": "person", "normalized": "傅尧俞", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-014", "text": "赤壁赋", "type": "work", "normalized": "赤壁赋（苏轼）", "confidence": 0.85, "source": "原文片段"},
    # 08-015 纳延金台集
    {"item_id": "08-015", "text": "果啰罗纳延", "type": "person", "normalized": "纳延（字易之，元诗人）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-015", "text": "金台集", "type": "work", "normalized": "金台集（纳延）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-015", "text": "虞伯生", "type": "person", "normalized": "虞集（字伯生）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-015", "text": "欧阳元功", "type": "person", "normalized": "欧阳玄（字元功）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-015", "text": "钱元溥", "type": "person", "normalized": "钱原溥（检讨）", "confidence": 0.82, "source": "原文片段"},
    # 08-016 张养浩
    {"item_id": "08-016", "text": "张文忠公养浩", "type": "person", "normalized": "张养浩（谥文忠）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-016", "text": "欧阳圭斋", "type": "person", "normalized": "欧阳玄（号圭斋）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-016", "text": "孙廷瑞", "type": "person", "normalized": "孙廷瑞（副都御史）", "confidence": 0.8, "source": "原文片段"},
    # 08-018 彭祖期/施槃
    {"item_id": "08-018", "text": "彭祖期", "type": "person", "normalized": "彭祖期（庐陵，监察御史）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-018", "text": "南畿学校", "type": "institution", "normalized": "南畿学校（提督）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-018", "text": "施槃", "type": "person", "normalized": "施槃（状元）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-018", "text": "倪谦", "type": "person", "normalized": "倪谦（探花）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-018", "text": "张和", "type": "person", "normalized": "张和（二甲）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "08-018", "text": "钱溥", "type": "person", "normalized": "钱溥（二甲）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "08-018", "text": "周忱", "type": "person", "normalized": "周忱（巡抚侍郎）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "08-018", "text": "孙鼎", "type": "person", "normalized": "孙鼎（教授松江）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-018", "text": "朱士章", "type": "person", "normalized": "朱士章（昆山教谕）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "08-018", "text": "郑文康", "type": "person", "normalized": "郑文康（昆山）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "08-018", "text": "陈铨", "type": "person", "normalized": "陈铨（太仓军生）", "confidence": 0.78, "source": "原文片段"},
]
