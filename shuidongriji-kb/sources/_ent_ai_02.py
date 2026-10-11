# -*- coding: utf-8 -*-
"""《水东日记》卷 02 —— L1 实体标注 源数据（AI 判定逐条填写）

说明：实体标注：每条记录标注该条目中的实体（text=原文字面，type=实体类型，normalized=归一词形，confidence=置信度）
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "02-001 | 景泰元年太上皇万寿圣节礼部请羣臣朝诏免朝二年盛与季聪约当草疏",
    "02-002 | 居庸以北俗择塟地以验蛇盘兎为上昌平侯杨洪赤城塟母处亦然意者地",
    "02-003 | 景泰二年予为殿试弥封官知读卷事第一甲盖閤老预属意于受卷官已得",
    "02-004 | 独石城堡今治开平卫初阳武侯薛禄奏筑城迁卫于此有僧庆西堂者号精",
    "02-005 | 尹鳯岐先生在翰林好作诗讽切时事节之最能记予仅记其一首时应诏举",
    "02-006 | 真定逻卒获一人为敌语甚习以为先被掳见留敌酋额森将窥临清使我等",
    "02-007 | 【阙】　　　　　　　以贸易习敌语不事作业被捶楚潜匿于外妄为此",
    "02-008 | 吴思庵先生谈及浅学后进曰此韵府羣玉秀才好趁航船尔航船吴中所谓",
    "02-009 | 弋谦代州人累任显官有声仁庙时歳己巳布衣走阙下疏前成山侯王通龙",
    "02-010 | 古人制作名集编次多出于己各有深意存焉或身后出于门生故吏子孙学",
    "02-011 | 景泰二年冬文渊阁办事中书舍人何观言大臣旧老少保兼吏部尚书王直",
    "02-012 | 祭酒安成李先生初以言事得罪系狱宣庙登极后一日御别殿以其激怒先",
    "02-013 | 景泰元年八月十一日朝退禁门侧尚书胡公手一揭帖文武重臣羣立传观",
    "02-014 | 南都数年前一时人物之盛勲旧之贤如襄城伯李公通材重望如少保黄公",
    "02-015 | 题秋胡图诗二首其一曰郎恩叶薄妾氷清郎说黄金妾不譍若使偶然通一",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 02-001 上皇万寿节朝贺之议 ============
    {"item_id": "02-001", "text": "景泰", "type": "era", "normalized": "景泰（明代宗年号）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-001", "text": "太上皇", "type": "person", "normalized": "太上皇（明英宗，被俘放回后称）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-001", "text": "万寿圣节", "type": "unknown", "normalized": "万寿圣节（皇帝生日）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "02-001", "text": "礼部", "type": "institution", "normalized": "礼部", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "02-001", "text": "盛", "type": "person", "normalized": "叶盛（作者，自称盛）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-001", "text": "季聪", "type": "person", "normalized": "季聪（季聦）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-001", "text": "科道", "type": "official", "normalized": "科道", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-001", "text": "御史防", "type": "person", "normalized": "御史防（姓名待考，'盛防'连读，防为御史）", "confidence": 0.7, "source": "原文片段"},
    {"item_id": "02-001", "text": "刘溥原溥", "type": "person", "normalized": "刘溥（字原溥）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-001", "text": "卢指挥", "type": "person", "normalized": "卢指挥（卢姓武官，名待考）", "confidence": 0.75, "source": "原文片段"},

    # ============ 02-002 居庸葬俗/于节庵家世 ============
    {"item_id": "02-002", "text": "居庸", "type": "place", "normalized": "居庸（居庸关）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-002", "text": "昌平侯杨洪", "type": "person", "normalized": "杨洪（昌平侯）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-002", "text": "赤城", "type": "place", "normalized": "赤城", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-002", "text": "于节庵", "type": "person", "normalized": "于节庵（名待考，董镛婿）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-002", "text": "黄鹤山", "type": "place", "normalized": "黄鹤山", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-002", "text": "董镛", "type": "person", "normalized": "董镛（先生，藏书家）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-002", "text": "黄文献公溍", "type": "person", "normalized": "黄溍（谥文献）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-002", "text": "于九思", "type": "person", "normalized": "于九思（湖南宣慰）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-002", "text": "董璵", "type": "person", "normalized": "董璵（董镛子，中书舍人）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-002", "text": "中书舍人", "type": "official", "normalized": "中书舍人", "confidence": 0.88, "source": "原文片段"},

    # ============ 02-003 殿试读卷弥封之制 ============
    {"item_id": "02-003", "text": "景泰二年", "type": "era", "normalized": "景泰二年", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-003", "text": "殿试", "type": "institution", "normalized": "殿试（科举）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-003", "text": "弥封官", "type": "official", "normalized": "弥封官", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-003", "text": "读卷", "type": "official", "normalized": "读卷官", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-003", "text": "閤老", "type": "person", "normalized": "閤老（内阁元老，指首辅）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "02-003", "text": "受卷官", "type": "official", "normalized": "受卷官", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-003", "text": "文华", "type": "place", "normalized": "文华殿", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-003", "text": "黄榜", "type": "unknown", "normalized": "黄榜（殿试榜）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-003", "text": "周文襄公", "type": "person", "normalized": "周忱（谥文襄）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-003", "text": "昆", "type": "place", "normalized": "昆（昆山）", "confidence": 0.85, "source": "原文片段"},

    # ============ 02-004 独石城堡开平卫 ============
    {"item_id": "02-004", "text": "独石城堡", "type": "place", "normalized": "独石城堡", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-004", "text": "开平卫", "type": "institution", "normalized": "开平卫", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-004", "text": "阳武侯薛禄", "type": "person", "normalized": "薛禄（封阳武侯）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-004", "text": "僧庆西堂", "type": "person", "normalized": "僧庆西堂（精地理术僧）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-004", "text": "百户", "type": "official", "normalized": "百户", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-004", "text": "杨昌平", "type": "person", "normalized": "杨洪（昌平侯，时为百户）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-004", "text": "己巳", "type": "era", "normalized": "己巳（正统十四年）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-004", "text": "都御史李公", "type": "person", "normalized": "都御史李公（名待考）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "02-004", "text": "宋学士", "type": "person", "normalized": "宋学士（宋濂？撰开平王碑文）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "02-004", "text": "开平王常忠武公", "type": "person", "normalized": "常遇春（封开平王，谥忠武）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-004", "text": "开平王祠", "type": "place", "normalized": "开平王祠（独石城）", "confidence": 0.88, "source": "原文片段"},

    # ============ 02-005 尹鳯岐翰林诗/鸿胪杨公读卷 ============
    {"item_id": "02-005", "text": "尹鳯岐", "type": "person", "normalized": "尹鳯岐（在翰林）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-005", "text": "翰林", "type": "institution", "normalized": "翰林院（翰林）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-005", "text": "贤良方正", "type": "official", "normalized": "贤良方正（举科目）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-005", "text": "太学生", "type": "official", "normalized": "太学生", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-005", "text": "景泰二年", "type": "era", "normalized": "景泰二年", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-005", "text": "廷试", "type": "institution", "normalized": "廷试（殿试）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-005", "text": "鸿胪杨公", "type": "person", "normalized": "鸿胪杨公（名待考）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "02-005", "text": "泰和王公", "type": "person", "normalized": "王直（泰和人，尚书）", "confidence": 0.85, "source": "原文片段"},

    # ============ 02-006 真定逻卒谍案 ============
    {"item_id": "02-006", "text": "真定", "type": "place", "normalized": "真定", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-006", "text": "额森", "type": "person", "normalized": "额森（瓦剌也先）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-006", "text": "临清", "type": "place", "normalized": "临清", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-006", "text": "宣府", "type": "place", "normalized": "宣府", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-006", "text": "紫荆等关口", "type": "place", "normalized": "紫荆关等关口", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-006", "text": "兵部", "type": "institution", "normalized": "兵部", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-006", "text": "郎中陈汝言", "type": "person", "normalized": "陈汝言（郎中）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-006", "text": "陈金", "type": "person", "normalized": "陈金", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "02-006", "text": "都察院", "type": "institution", "normalized": "都察院", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-006", "text": "锦衣卫", "type": "institution", "normalized": "锦衣卫", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-006", "text": "巡按御史", "type": "official", "normalized": "巡按御史", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-006", "text": "张鹏", "type": "person", "normalized": "张鹏（涞水人，御史）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-006", "text": "平定州", "type": "place", "normalized": "平定州", "confidence": 0.85, "source": "原文片段"},

    # ============ 02-007 谍案辨释（阙文） ============
    {"item_id": "02-007", "text": "台省", "type": "institution", "normalized": "台省（御史台/省台）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "02-007", "text": "御史", "type": "official", "normalized": "御史（张鹏）", "confidence": 0.85, "source": "原文片段"},

    # ============ 02-008 吴思庵论学/季聪劾善增 ============
    {"item_id": "02-008", "text": "吴思庵", "type": "person", "normalized": "吴思庵", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-008", "text": "韵府羣玉", "type": "work", "normalized": "韵府群玉（类书）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-008", "text": "航船", "type": "unknown", "normalized": "夜航船（吴中夜航船）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "02-008", "text": "吴中", "type": "place", "normalized": "吴中", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-008", "text": "景泰二年", "type": "era", "normalized": "景泰二年", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-008", "text": "内官善增", "type": "person", "normalized": "善增（内官太监）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-008", "text": "王振", "type": "person", "normalized": "王振", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-008", "text": "季聪", "type": "person", "normalized": "季聪（季聦）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-008", "text": "六科", "type": "institution", "normalized": "六科", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-008", "text": "十三道", "type": "institution", "normalized": "十三道（监察御史）", "confidence": 0.88, "source": "原文片段"},

    # ============ 02-009 弋谦论用王通 ============
    {"item_id": "02-009", "text": "弋谦", "type": "person", "normalized": "弋谦（代州人）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-009", "text": "代州", "type": "place", "normalized": "代州", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-009", "text": "成山侯王通", "type": "person", "normalized": "王通（成山侯）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-009", "text": "甯懋", "type": "person", "normalized": "甯懋（龙门致仕指挥）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "02-009", "text": "阮迁干", "type": "person", "normalized": "阮迁干（真定同知）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "02-009", "text": "真定同知", "type": "official", "normalized": "真定同知", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "02-009", "text": "额森", "type": "person", "normalized": "额森（瓦剌也先）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-009", "text": "紫荆口", "type": "place", "normalized": "紫荆口", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-009", "text": "石亨", "type": "person", "normalized": "石亨", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-009", "text": "于尚书", "type": "person", "normalized": "于谦（兵部尚书）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-009", "text": "左顺门", "type": "place", "normalized": "左顺门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-009", "text": "六科", "type": "institution", "normalized": "六科", "confidence": 0.88, "source": "原文片段"},

    # ============ 02-010 文集编次之谬 ============
    {"item_id": "02-010", "text": "周必大", "type": "person", "normalized": "周必大", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-010", "text": "欧阳文忠公", "type": "person", "normalized": "欧阳修（谥文忠）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-010", "text": "处州叶学士", "type": "person", "normalized": "叶适（水心，处州学士）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-010", "text": "水心文集", "type": "work", "normalized": "水心文集（叶适）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-010", "text": "文山先生", "type": "person", "normalized": "文天祥（号文山）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-010", "text": "宋学士", "type": "person", "normalized": "宋濂（宋学士）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-010", "text": "高太史", "type": "person", "normalized": "高启（号青丘，翰林院国史编修，称太史）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-010", "text": "缶鸣集", "type": "work", "normalized": "缶鸣集（高启）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-010", "text": "姑苏杂咏", "type": "work", "normalized": "姑苏杂咏（高启）", "confidence": 0.85, "source": "原文片段"},

    # ============ 02-011 何观建言得罪 ============
    {"item_id": "02-011", "text": "景泰二年", "type": "era", "normalized": "景泰二年", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-011", "text": "文渊阁", "type": "institution", "normalized": "文渊阁", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-011", "text": "中书舍人何观", "type": "person", "normalized": "何观（中书舍人）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-011", "text": "少保兼吏部尚书王直", "type": "person", "normalized": "王直（少保兼吏部尚书）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-011", "text": "正统", "type": "era", "normalized": "正统（明英宗）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-011", "text": "吏科给事中毛玉", "type": "person", "normalized": "毛玉（吏科给事中）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-011", "text": "季聪", "type": "person", "normalized": "季聪（季聦）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-011", "text": "盛", "type": "person", "normalized": "叶盛（作者，自称盛）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-011", "text": "春秋", "type": "work", "normalized": "春秋（经）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-011", "text": "胡传", "type": "work", "normalized": "胡传（胡安国春秋传）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "02-011", "text": "东坡", "type": "person", "normalized": "苏轼（号东坡）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-011", "text": "刘球", "type": "person", "normalized": "刘球", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-011", "text": "王振", "type": "person", "normalized": "王振", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-011", "text": "马顺", "type": "person", "normalized": "马顺", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-011", "text": "锦衣卫", "type": "institution", "normalized": "锦衣卫", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-011", "text": "门谢二镇抚", "type": "person", "normalized": "门谢二镇抚（锦衣镇抚，姓名待考）", "confidence": 0.72, "source": "原文片段"},

    # ============ 02-012 安成李先生/解胡契好 ============
    {"item_id": "02-012", "text": "安成李先生", "type": "person", "normalized": "李先生（安成人，祭酒，疑李时勉）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "02-012", "text": "祭酒", "type": "official", "normalized": "祭酒（国子监祭酒）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-012", "text": "宣庙", "type": "era", "normalized": "宣德（明宣宗）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-012", "text": "锦衣指挥王某", "type": "person", "normalized": "锦衣指挥王某（名待考）", "confidence": 0.72, "source": "原文片段"},
    {"item_id": "02-012", "text": "端门", "type": "place", "normalized": "端门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-012", "text": "西长安门", "type": "place", "normalized": "西长安门", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-012", "text": "解学士", "type": "person", "normalized": "解缙（学士）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-012", "text": "胡祭酒", "type": "person", "normalized": "胡祭酒（名待考，与解缙契好）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "02-012", "text": "进士榜", "type": "unknown", "normalized": "进士榜（黄榜）", "confidence": 0.82, "source": "原文片段"},

    # ============ 02-013 匿名揭帖议迎复 ============
    {"item_id": "02-013", "text": "景泰元年", "type": "era", "normalized": "景泰元年", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-013", "text": "尚书胡公", "type": "person", "normalized": "胡濙（礼部尚书）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-013", "text": "尚书王公", "type": "person", "normalized": "王直（吏部尚书）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-013", "text": "盛", "type": "person", "normalized": "叶盛（作者，自称盛）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-013", "text": "上皇", "type": "person", "normalized": "上皇（明英宗）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-013", "text": "高学士", "type": "person", "normalized": "高学士（疑高谷）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "02-013", "text": "三法司", "type": "institution", "normalized": "三法司（刑部/都察院/大理寺）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "02-013", "text": "都御史王文", "type": "person", "normalized": "王文（都御史）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-013", "text": "少保于", "type": "person", "normalized": "于谦（少保）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "02-013", "text": "礼科", "type": "institution", "normalized": "礼科", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-013", "text": "龚千户遂荣", "type": "person", "normalized": "龚遂荣（千户）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "02-013", "text": "门谢二镇抚", "type": "person", "normalized": "门谢二镇抚（锦衣镇抚）", "confidence": 0.7, "source": "原文片段"},

    # ============ 02-014 南都人物之盛 ============
    {"item_id": "02-014", "text": "南都", "type": "place", "normalized": "南都（南京）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "02-014", "text": "襄城伯李公", "type": "person", "normalized": "襄城伯李公（名待考）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "02-014", "text": "少保黄公", "type": "person", "normalized": "黄福（少保）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "02-014", "text": "都御史吴公", "type": "person", "normalized": "都御史吴公（名待考）", "confidence": 0.72, "source": "原文片段"},
    {"item_id": "02-014", "text": "侍郎徐公", "type": "person", "normalized": "侍郎徐公（名待考）", "confidence": 0.7, "source": "原文片段"},
    {"item_id": "02-014", "text": "侍郎金公", "type": "person", "normalized": "侍郎金公（名待考）", "confidence": 0.7, "source": "原文片段"},
    {"item_id": "02-014", "text": "通政陈公", "type": "person", "normalized": "通政陈公（名待考）", "confidence": 0.7, "source": "原文片段"},
    {"item_id": "02-014", "text": "尚书黄公", "type": "person", "normalized": "尚书黄公（名待考）", "confidence": 0.7, "source": "原文片段"},
    {"item_id": "02-014", "text": "少卿杨公", "type": "person", "normalized": "少卿杨公（名待考）", "confidence": 0.7, "source": "原文片段"},
    {"item_id": "02-014", "text": "学士周公", "type": "person", "normalized": "学士周公（名待考）", "confidence": 0.7, "source": "原文片段"},
    {"item_id": "02-014", "text": "祭酒陈公", "type": "person", "normalized": "祭酒陈公（名待考）", "confidence": 0.7, "source": "原文片段"},
    {"item_id": "02-014", "text": "尚书魏公", "type": "person", "normalized": "尚书魏公（名待考）", "confidence": 0.7, "source": "原文片段"},
    {"item_id": "02-014", "text": "南京十三道", "type": "institution", "normalized": "南京十三道（监察御史）", "confidence": 0.85, "source": "原文片段"},

    # ============ 02-015 秋胡图诗 ============
    {"item_id": "02-015", "text": "秋胡图", "type": "work", "normalized": "秋胡图（画）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-015", "text": "秋胡", "type": "person", "normalized": "秋胡（春秋鲁人）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "02-015", "text": "赵松雪", "type": "person", "normalized": "赵孟頫（号松雪）", "confidence": 0.88, "source": "原文片段"},
]
