# -*- coding: utf-8 -*-
"""《水东日记》卷 16 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "16-001 | 今印行宋名臣言行録前集赵普曹彬范质窦仪李昉吕蒙正张齐贤吕端钱若",
    "16-002 | 元人挽文丞相近体之字韵诗史家以为翰林王磐作或又云徐世隆作朱知孰",
    "16-003 | 今人似大舒气作声为打呵欠韩昌黎诗噫欠为飘风注噫乌介切欠或作",
    "16-004 | 真清三韵本不宜通用张篠庵兄弟云窃知忌此但诗与楚辞多有之盖时或",
    "16-005 | 独石将黄瑄往日言少尝事武安侯郑亨阳武侯薛禄两总戎如斯人今",
    "16-006 | 庄浪属环雪山其北生牦牛毛杂黑白二色长甚军中红黑缨皆用之红即",
    "16-007 | 凡人荣辱进退等事固亦有命所谓饮啄有前定况死生祸福其大者耶兹举",
    "16-008 | 正统丙辰廷试阁老将进读卷问同事诸公曰孰能识周旋否其人物何如",
    "16-009 | 己巳冬边方骚动兵部郎中罗通守居庸复以给事中孙祥守紫荆廷仪皆",
    "16-010 | 统幕围一戍卒尝语其家人曰乱中吾见一神人谓曰尔非此中人豆腐人也",
    "16-011 | 余在兵科急欲询将官应诏同年夏季爵主事曰闻南京陈旺者正统中黄",
    "16-012 | 文字著述官制称谓器物名号以至歌谣语戏谑之言多有征应亦皆有当",
    "16-013 | 汉高帝忌柏人之名岑壮侯恶彭亡之地",
    "16-014 | 宋神宗改元大成丰亨之议三省台印乖戾倒屈宣抚使印从亡之应刘原",
    "16-015 | 吴之马鞍山阴叠浪轩面湖水数百顷宋时有识者曰车干水宜良田今湖",
    "16-016 | 贾似道福华编诚覆国矣",
    "16-017 | 咸淳中将作监杨文仲两侍经幄屡得赐诗中有一元肇始大原壹正之语",
    "16-018 | 王翰林玉初名子璠乡试当魁时初平高煦拆卷以其音类王子反也已",
    "16-019 | 正统中京师旱小儿舆土龙祷雨类云雨地雨地城隍土地雨若大来谢了",
    "16-020 | 陈者自号安止任会稽知县后调淳安竟坐事罢官朱晦庵庐山纪行诗有",
    "16-021 | 东里居士还家诗一则曰犹有黄花待我回二则曰定有黄花待客回岂亦",
    "16-022 | 正统十三年彭时榜进士诏选北士林为庶吉士命儒臣教督之长州刘",
    "16-023 | 予尝记宋嘉定中地理厉伯韶事兹读开化江氏谱见秉心纪善赞曾学世",
]

DATA = [
    # ============ 16-001 宋名臣言行録书目 ============
    {"item_id": "16-001", "text": "宋名臣言行录", "type": "work", "normalized": "宋名臣言行录（前集/后集/别集/外录）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "16-001", "text": "朱熹", "type": "person", "normalized": "朱熹（朱夫子，纂言行录）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "16-001", "text": "李衡", "type": "person", "normalized": "李衡（太平老圃，校正言行录）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-001", "text": "李居安", "type": "person", "normalized": "李居安（庐陵，宝祐戊子续集）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "16-001", "text": "李幼武", "type": "person", "normalized": "李幼武（明溪，字士英，辑言行录）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "16-001", "text": "苏天爵", "type": "person", "normalized": "苏天爵（元，编名臣事略）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-001", "text": "许有壬", "type": "person", "normalized": "许有壬（元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-001", "text": "耶律楚材", "type": "person", "normalized": "耶律楚材（元）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-001", "text": "姚枢", "type": "person", "normalized": "姚枢（元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-001", "text": "许衡", "type": "person", "normalized": "许衡（元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-001", "text": "郭守敬", "type": "person", "normalized": "郭守敬（元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-001", "text": "刘秉忠", "type": "person", "normalized": "刘秉忠（元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-001", "text": "史天泽", "type": "person", "normalized": "史天泽（元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-001", "text": "郝经", "type": "person", "normalized": "郝经（元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-001", "text": "虞集", "type": "person", "normalized": "虞集（欧阳圭斋，误）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "16-001", "text": "南海神庙", "type": "place", "normalized": "南海神庙", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-001", "text": "铜鼓", "type": "unknown", "normalized": "铜鼓（南海神庙藏）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "16-001", "text": "马伏波", "type": "person", "normalized": "马援（马伏波，传作铜鼓）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "16-001", "text": "武侯", "type": "person", "normalized": "诸葛亮（武侯，传作云南贵州铜鼓）", "confidence": 0.8, "source": "原文片段"},

    # ============ 16-002 挽文丞相诗 ============
    {"item_id": "16-002", "text": "文丞相", "type": "person", "normalized": "文天祥（文丞相）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "16-002", "text": "王磐", "type": "person", "normalized": "王磐（元翰林）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-002", "text": "徐世隆", "type": "person", "normalized": "徐世隆（元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-002", "text": "赵松雪", "type": "person", "normalized": "赵孟頫（赵松雪）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-002", "text": "钱起", "type": "person", "normalized": "钱起（唐）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-002", "text": "黄谏", "type": "person", "normalized": "黄谏（侍讲）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-002", "text": "解缙", "type": "person", "normalized": "解缙", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-002", "text": "宋景濂", "type": "person", "normalized": "宋濂（宋景濂）", "confidence": 0.82, "source": "原文片段"},

    # ============ 16-003 打呵欠 ============
    {"item_id": "16-003", "text": "韩昌黎", "type": "person", "normalized": "韩愈（韩昌黎）", "confidence": 0.88, "source": "原文片段"},

    # ============ 16-004 进士题名録考 ============
    {"item_id": "16-004", "text": "湖广进士题名録", "type": "work", "normalized": "湖广新编国朝进士题名录", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-004", "text": "王抑庵", "type": "person", "normalized": "王直（王抑庵，史官）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "16-004", "text": "陈德遵", "type": "person", "normalized": "陈德遵（史官）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "16-004", "text": "洪武", "type": "era", "normalized": "洪武", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "16-004", "text": "正统", "type": "era", "normalized": "正统", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "16-004", "text": "景泰", "type": "era", "normalized": "景泰", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "16-004", "text": "武经总要", "type": "work", "normalized": "武经总要", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "16-004", "text": "大观本草", "type": "work", "normalized": "大观本草", "confidence": 0.8, "source": "原文片段"},

    # ============ 16-005 黄瑄言郑亨薛禄 ============
    {"item_id": "16-005", "text": "独石", "type": "place", "normalized": "独石（边堡）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-005", "text": "黄瑄", "type": "person", "normalized": "黄瑄（独石参将）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-005", "text": "郑亨", "type": "person", "normalized": "郑亨（武安侯）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-005", "text": "薛禄", "type": "person", "normalized": "薛禄（阳武侯）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-005", "text": "大同", "type": "place", "normalized": "大同", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-005", "text": "沈清", "type": "person", "normalized": "沈清（修武伯，继薛禄）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "16-005", "text": "参将", "type": "official", "normalized": "参将", "confidence": 0.85, "source": "原文片段"},

    # ============ 16-006 庄浪牦牛 ============
    {"item_id": "16-006", "text": "庄浪", "type": "place", "normalized": "庄浪", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-006", "text": "西番", "type": "place", "normalized": "西番", "confidence": 0.82, "source": "原文片段"},

    # ============ 16-008 正统丙辰读卷 ============
    {"item_id": "16-008", "text": "正统", "type": "era", "normalized": "正统", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "16-008", "text": "周旋", "type": "person", "normalized": "周旋（温州人，状元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-008", "text": "周瑄", "type": "person", "normalized": "周瑄（淳安人）", "confidence": 0.82, "source": "原文片段"},

    # ============ 16-009 己巳罗通孙祥 ============
    {"item_id": "16-009", "text": "罗通", "type": "person", "normalized": "罗通（兵部郎中，守居庸）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "16-009", "text": "孙祥", "type": "person", "normalized": "孙祥（给事中，守紫荆）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-009", "text": "居庸关", "type": "place", "normalized": "居庸关", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "16-009", "text": "紫荆关", "type": "place", "normalized": "紫荆关", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "16-009", "text": "佥都御史", "type": "official", "normalized": "佥都御史", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "16-009", "text": "吏部", "type": "institution", "normalized": "吏部", "confidence": 0.9, "source": "原文片段"},

    # ============ 16-010 统幕豆腐闸 ============
    {"item_id": "16-010", "text": "统幕", "type": "place", "normalized": "统幕（地名）", "confidence": 0.78, "source": "原文片段"},

    # ============ 16-011 陈旺黄福荐 ============
    {"item_id": "16-011", "text": "陈旺", "type": "person", "normalized": "陈旺", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-011", "text": "黄福", "type": "person", "normalized": "黄福（黄尚书）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-011", "text": "宗载", "type": "person", "normalized": "宗载（尚书）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "16-011", "text": "兵科", "type": "institution", "normalized": "兵科", "confidence": 0.85, "source": "原文片段"},

    # ============ 16-013 汉高祖岑彭 ============
    {"item_id": "16-013", "text": "汉高祖", "type": "person", "normalized": "汉高祖（刘邦）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-013", "text": "岑彭", "type": "person", "normalized": "岑彭（岑壮侯）", "confidence": 0.82, "source": "原文片段"},

    # ============ 16-014 宋神宗改元 ============
    {"item_id": "16-014", "text": "宋神宗", "type": "person", "normalized": "宋神宗", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-014", "text": "刘敞", "type": "person", "normalized": "刘原父（刘敞）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-014", "text": "梅尧臣", "type": "person", "normalized": "梅都官（梅尧臣）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-014", "text": "欧阳修", "type": "person", "normalized": "欧阳公（欧阳修）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-014", "text": "刘羲叟", "type": "person", "normalized": "刘羲叟", "confidence": 0.78, "source": "原文片段"},

    # ============ 16-016 贾似道福华编 ============
    {"item_id": "16-016", "text": "贾似道", "type": "person", "normalized": "贾似道", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "16-016", "text": "福华编", "type": "work", "normalized": "福华编（贾似道）", "confidence": 0.8, "source": "原文片段"},

    # ============ 16-017 杨文仲经幄 ============
    {"item_id": "16-017", "text": "杨文仲", "type": "person", "normalized": "杨文仲（宋咸淳中将作监）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-017", "text": "咸淳", "type": "era", "normalized": "咸淳（宋度宗）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-017", "text": "朝元观", "type": "place", "normalized": "朝元观（宣府）", "confidence": 0.78, "source": "原文片段"},

    # ============ 16-018 王玉高煦 ============
    {"item_id": "16-018", "text": "王玉", "type": "person", "normalized": "王翰林玉（初名子璠）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-018", "text": "高煦", "type": "person", "normalized": "高煦（汉王，平之）", "confidence": 0.82, "source": "原文片段"},

    # ============ 16-020 陈皥朱熹庐山诗 ============
    {"item_id": "16-020", "text": "陈皥", "type": "person", "normalized": "陈皥（号安止）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "16-020", "text": "朱熹", "type": "person", "normalized": "朱熹（晦庵，庐山纪行诗）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "16-020", "text": "庐山", "type": "place", "normalized": "庐山", "confidence": 0.85, "source": "原文片段"},

    # ============ 16-021 杨东里还家诗 ============
    {"item_id": "16-021", "text": "杨东里", "type": "person", "normalized": "杨士奇（东里居士）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "16-021", "text": "黄山谷", "type": "person", "normalized": "黄庭坚（黄山谷）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-021", "text": "谢玄晖", "type": "person", "normalized": "谢朓（谢玄晖）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-021", "text": "黄东发", "type": "person", "normalized": "黄震（黄东发）", "confidence": 0.82, "source": "原文片段"},

    # ============ 16-022 彭时榜庶吉士 ============
    {"item_id": "16-022", "text": "彭时", "type": "person", "normalized": "彭时（正统十三年状元榜）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-022", "text": "刘俨", "type": "person", "normalized": "刘俨（字宗器，长州詹事）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-022", "text": "尹旻", "type": "person", "normalized": "尹旻（同仁，山东）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "16-022", "text": "孙昱", "type": "person", "normalized": "孙昱（廷昭，山东）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "16-022", "text": "庶吉士", "type": "official", "normalized": "庶吉士", "confidence": 0.85, "source": "原文片段"},

    # ============ 16-023 开化江氏谱赖布衣 ============
    {"item_id": "16-023", "text": "开化江氏谱", "type": "work", "normalized": "开化江氏谱", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-023", "text": "厉伯韶", "type": "person", "normalized": "厉伯韶（宋嘉定地理家）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "16-023", "text": "景房", "type": "person", "normalized": "江景房（侍御，开化江氏墓）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "16-023", "text": "赖布衣", "type": "person", "normalized": "赖布衣（宋季相地者）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "16-023", "text": "开化", "type": "place", "normalized": "开化", "confidence": 0.85, "source": "原文片段"},
]
# 缺口登记：16-007/16-012 泛论荣辱有命、文字讳避，无具名实体。
