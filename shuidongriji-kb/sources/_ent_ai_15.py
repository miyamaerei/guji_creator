# -*- coding: utf-8 -*-
"""《水东日记》卷 15 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "15-001 | 今山隂陆氏谱有唐观察使庶吴郡陆氏四十九枝族谱欧阳修唐书陆氏宰相世",
    "15-002 | 吾见平时丧家百费方兴而遇俗又侈于道塲斋施之事彼初不知佛为何人佛",
    "15-003 | 升济神明之説惟出佛经黄老之学本于淸浄自然地狱天宫何尝言及黄冠",
    "15-004 | 吾平生未尝害人人之害吾者或出忌嫉或偶不相知或以为利其情多可谅",
    "15-005 | 祸有不可避者避之得祸弥甚旣不能而仕小则谴斥大则死自是其分若逃",
    "15-006 | 风俗方日壊可忧者非一事吾幸老且死矣若使未遽死亦决不复出仕惟顾",
    "15-007 | 厚塟于存殁无益古今达人言之已详余家旣贫甚自无此虑不待形言至",
    "15-008 | 近世出塟或作香亭魂亭寓人寓马之一切当屏去僧徒引导尤非敬佛之",
    "15-009 | 古者植木塜上以识其处耳吾家自先太傅以上塜上松木多不过数十太尉",
    "15-010 | 石人石虎之皆当罢之欲识墓处立一二石柱可也守墓以僧非旧也太傅",
    "15-011 | 人生才固有限然世人多不能克尽其实至老必抱遗恨吾虽不才然亦一人",
    "15-012 | 人与万物同受一气生天地间但有中正偏驳之异尔理不应相害圣人所谓数",
    "15-013 | 世之贪夫谿壑无餍固不足责至若常人之情见他人服玩不能不动亦是",
    "15-014 | 人士有与吾辈行同者虽位有贵贱交有厚薄汝辈见之当极恭逊已虽高",
    "15-015 | 吾惟文辞一事颇得名过其实其余自勉于善而不见知于人盖有之矣初无",
    "15-016 | 居丧之礼不可不勉人固有体气素弱不能常去肉食者礼亦许之然亦不",
    "15-017 | 诉讼一事最当谨始使官司公明可恃尚不当为况官司闗节更取货贿或官",
    "15-018 | 吾居贫不喜为人言故知者少今啓予足之后乃至不能办棺敛度不免以",
    "15-019 | 九里家防大墓及太傅太尉左丞少师荣国夫人康国夫人诸墓岁时切宜省",
    "15-020 | 余庆藏书阁色色已具不幸中遭扰乱迄今未能建立吾寝食未尝去心若神",
    "15-021 | 子孙才分有限无如之何然不可不使读书贫则教训童稚以给衣食但书种",
    "15-022 | 后生才鋭者最易壊若有之父兄当以为忧不可以为喜也切须常加检束",
    "15-023 | 南京大理少卿宜兴杨公复能诗有盛名其家僮往往于武湖壖取萍藻为豚",
    "15-024 | 吕尚书震与学士解公缙一日谈及食中美味吕曰驼峰珎美震未之识也解",
]

DATA = [
    # ============ 15-001 山阴陆氏谱+放翁家训 ============
    {"item_id": "15-001", "text": "山阴陆氏", "type": "place", "normalized": "山阴陆氏（山阴，陆氏郡望聚居）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "15-001", "text": "陆氏谱", "type": "work", "normalized": "山阴陆氏谱（含放翁家训）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "15-001", "text": "陆庶", "type": "person", "normalized": "陆庶（唐观察使）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "15-001", "text": "吴郡陆氏", "type": "place", "normalized": "吴郡陆氏", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "15-001", "text": "欧阳修", "type": "person", "normalized": "欧阳修", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "15-001", "text": "唐书", "type": "work", "normalized": "新唐书（欧阳修撰宰相世系表）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "15-001", "text": "陆游", "type": "person", "normalized": "陆游（放翁，宝谟阁待制）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "15-001", "text": "放翁家训", "type": "work", "normalized": "放翁家训（陆游撰）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "15-001", "text": "钱氏", "type": "person", "normalized": "钱氏（吴越割据）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "15-001", "text": "吴越", "type": "place", "normalized": "吴越", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "15-001", "text": "祥符", "type": "era", "normalized": "大中祥符（宋真宗）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "15-001", "text": "泰山", "type": "place", "normalized": "泰山", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "15-001", "text": "鲁墟", "type": "place", "normalized": "鲁墟（陆氏故居）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "15-001", "text": "太傅", "type": "official", "normalized": "太傅（陆氏先人）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "15-001", "text": "太尉", "type": "official", "normalized": "太尉（陆氏先人）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "15-001", "text": "左丞", "type": "official", "normalized": "左丞（陆氏先人）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "15-001", "text": "宝谟阁待制", "type": "official", "normalized": "宝谟阁待制", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "15-001", "text": "乾道", "type": "era", "normalized": "乾道（宋孝宗）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "15-001", "text": "九里", "type": "place", "normalized": "九里（陆氏墓地）", "confidence": 0.82, "source": "原文片段"},

    # ============ 15-002 丧家侈佛 ============
    {"item_id": "15-002", "text": "金刚经", "type": "work", "normalized": "金刚经", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "15-002", "text": "法华经", "type": "work", "normalized": "法华经", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "15-002", "text": "华严经", "type": "work", "normalized": "华严经", "confidence": 0.85, "source": "原文片段"},

    # ============ 15-003 黄老/链度 ============
    {"item_id": "15-003", "text": "黄老", "type": "person", "normalized": "黄老（黄帝老子，道家）", "confidence": 0.82, "source": "原文片段"},

    # ============ 15-007 厚葬/四明临安倭船 ============
    {"item_id": "15-007", "text": "四明", "type": "place", "normalized": "四明（宁波）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "15-007", "text": "临安", "type": "place", "normalized": "临安", "confidence": 0.85, "source": "原文片段"},

    # ============ 15-009 墓木 ============
    {"item_id": "15-009", "text": "宝峰", "type": "place", "normalized": "宝峰（陆氏葬地）", "confidence": 0.82, "source": "原文片段"},

    # ============ 15-017 李汉老论诉讼 ============
    {"item_id": "15-017", "text": "李参政汉老", "type": "person", "normalized": "李汉老（参政）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "15-017", "text": "成季", "type": "person", "normalized": "成季（李汉老叔父）", "confidence": 0.75, "source": "原文片段"},

    # ============ 15-019 九里陆氏诸墓 ============
    {"item_id": "15-019", "text": "九里", "type": "place", "normalized": "九里（陆氏墓地）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "15-019", "text": "太傅太尉左丞少师", "type": "official", "normalized": "太傅/太尉/左丞/少师（陆氏先人）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "15-019", "text": "荣国夫人", "type": "person", "normalized": "荣国夫人（陆氏先人）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "15-019", "text": "康国夫人", "type": "person", "normalized": "康国夫人（陆氏先人）", "confidence": 0.78, "source": "原文片段"},

    # ============ 15-020 余庆藏书阁 ============
    {"item_id": "15-020", "text": "余庆藏书阁", "type": "work", "normalized": "余庆藏书阁（陆氏拟建）", "confidence": 0.8, "source": "原文片段"},

    # ============ 15-021 魏郑公庄 ============
    {"item_id": "15-021", "text": "魏郑公", "type": "person", "normalized": "魏徵（魏郑公）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "15-021", "text": "关中", "type": "place", "normalized": "关中", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "15-021", "text": "张浮休", "type": "person", "normalized": "张浮休", "confidence": 0.8, "source": "原文片段"},

    # ============ 15-023 杨复诗拒吴思庵 ============
    {"item_id": "15-023", "text": "杨公复", "type": "person", "normalized": "杨复（南京大理少卿，宜兴）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "15-023", "text": "南京大理少卿", "type": "official", "normalized": "南京大理寺少卿", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "15-023", "text": "宜兴", "type": "place", "normalized": "宜兴", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "15-023", "text": "玄武湖", "type": "place", "normalized": "玄武湖", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "15-023", "text": "吴思庵", "type": "person", "normalized": "吴思庵", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "15-023", "text": "都察院", "type": "institution", "normalized": "都察院", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "15-023", "text": "节之", "type": "person", "normalized": "节之（叶盛友，闻此故事者）", "confidence": 0.7, "source": "原文片段"},

    # ============ 15-024 吕震解缙驼峰谑 ============
    {"item_id": "15-024", "text": "吕震", "type": "person", "normalized": "吕震（吕尚书）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "15-024", "text": "解缙", "type": "person", "normalized": "解缙（解学士）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "15-024", "text": "光禄寺", "type": "institution", "normalized": "光禄寺", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "15-024", "text": "京师", "type": "place", "normalized": "京师", "confidence": 0.85, "source": "原文片段"},
]
# 缺口登记：15-004/005/006/008/010/011/012/013/014/015/016/018/022 皆放翁家训家训正文，为戒子之语，无具名新实体。
