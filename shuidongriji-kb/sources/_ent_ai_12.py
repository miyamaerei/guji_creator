# -*- coding: utf-8 -*-
"""《水东日记》卷 12 —— L1 实体标注 源数据（AI 判定逐条填写）

说明：实体标注：每条记录标注该条目中的实体（text=原文字面，type=实体类型，normalized=归一词形，confidence=置信度）

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：person=人物 / official=职官名 / institution=机构衙门 / place=地名 / era=年号朝代 / posthumous=谥号 / work=书名文献名 / unknown=类型待定
  * 未建模条目在下方注释中如实单列，不强行编造
  * 先查后建：跨条目同人/同机构用同一 normalized 词形，build_ent_keys 自动合并复用 ENT ID

填写方式：把 DATA 中的示例记录替换为本卷实际判定结果；
         每条记录为一个 dict；未判定条目保留注释占位。
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "12-001 | 商状元载家藏宋时公牒一内凡朝廷语言皆朱书盖其先本西夏人以献密有",
    "12-002 | 胡参政拱辰藏其乡先生宋融堂钱时予是周易释传一册十二卷两汉笔记一",
    "12-003 | 録白宋省劄",
    "12-004 | 特进左丞相兼枢宻使肃国公乔某劄子臣辄有奏陈仰干天听臣昨任国子司",
    "12-005 | 右劄付秘阁钱校勘",
    "12-006 | 嘉熈二年五月　日　押　　【押押】",
    "12-007 | 録白严州进书缴状",
    "12-008 | 贴黄【严州恭奉圣防取发严州布衣钱时著述书上进事朝防大夫权知严州军",
    "12-009 | 尚书省劄备特进左丞相劄子奏陈严州布衣钱时山居读书理学淹贯特补迪",
    "12-010 | 劄付严州臣除已恭禀缮写钱时所著述书计壹百册开具数目如后须至上进",
    "12-011 | 钱时家塾尚书演义叄拾册",
    "12-012 | 学诗管见叁拾册",
    "12-013 | 周易释传贰拾册",
    "12-014 | 四书管见捌册",
    "12-015 | 两汉笔记壹拾贰册",
    "12-016 | 一右件书壹百册用黄绫装褙黄罗绢里夹复五条牙牌五面红茸条系防畵木",
    "12-017 | 嘉熈二年九月　　日【朝防大夫权知严州军州兼管内劝农事万荐上进】",
    "12-018 | 皇帝龙飞御天之三年十有一月诏天下郡县兴贤者能者明年行江浙中书省",
    "12-019 | 书中是知【缺】　　　　　　也其何以告若粹白庄逊以持其身幽深逺",
    "12-020 | 昆山进士张经字伯绪邢寛榜及第张篠庵兄弟业师也篠庵尝诵其格言曰人不",
    "12-021 | 建安杨文敏公行状云永乐十七年十二月己丑则进言十事皆斥五府六部三",
    "12-022 | 朝臣有倾巧迎合为公所抑者议欲间之防北京缺祭酒众请以公任焉上不",
    "12-023 | 宋定陵太中祥符四年吴兴姚集唐文粹百卷成自防言絶响圣道委地屈平宋",
    "12-024 | 故事书坊印本行世颇多而善本甚鲜惟建安虞韶以成日记故事以为一主",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 12-001 商辂家藏宋时公牒 ============
    {"item_id": "12-001", "text": "商状元载", "type": "person", "normalized": "商辂（商状元弘载，淳臣）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-001", "text": "翰林", "type": "institution", "normalized": "翰林院（翰林）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-001", "text": "西夏", "type": "place", "normalized": "西夏", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-001", "text": "浙中", "type": "place", "normalized": "浙中（浙江）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-001", "text": "浮安寥源", "type": "place", "normalized": "浮安寥源（浙中安插地）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "12-001", "text": "周公叙", "type": "person", "normalized": "周公（宋跋者，姓名待考）", "confidence": 0.7, "source": "原文片段"},

    # ============ 12-002 胡拱辰藏钱时书 ============
    {"item_id": "12-002", "text": "胡参政拱辰", "type": "person", "normalized": "胡拱辰（参政）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "12-002", "text": "参政", "type": "official", "normalized": "参政", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-002", "text": "融堂钱时", "type": "person", "normalized": "钱时（融堂，宋严州布衣）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "12-002", "text": "周易释传", "type": "work", "normalized": "周易释传（钱时撰）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "12-002", "text": "两汉笔记", "type": "work", "normalized": "两汉笔记（钱时撰）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "12-002", "text": "班孟坚", "type": "person", "normalized": "班固（班孟坚）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-002", "text": "艺文志", "type": "work", "normalized": "汉书艺文志", "confidence": 0.88, "source": "原文片段"},

    # ============ 12-003 録白宋省劄（标题行，无实体）============

    # ============ 12-004 乔某劄子荐钱时吴如愚 ============
    {"item_id": "12-004", "text": "乔某", "type": "person", "normalized": "乔某（特进左丞相兼枢密使肃国公）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-004", "text": "特进左丞相兼枢密使", "type": "official", "normalized": "左丞相兼枢密使", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-004", "text": "国子司业", "type": "official", "normalized": "国子司业", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-004", "text": "钱时", "type": "person", "normalized": "钱时（融堂，宋严州布衣）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "12-004", "text": "严州", "type": "place", "normalized": "严州", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-004", "text": "杨简", "type": "person", "normalized": "杨简（宝谟阁学士）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-004", "text": "宝谟阁学士", "type": "official", "normalized": "宝谟阁学士", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-004", "text": "袁甫", "type": "person", "normalized": "袁甫（宝章阁待制）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-004", "text": "宝章阁待制", "type": "official", "normalized": "宝章阁待制", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-004", "text": "郑之悌", "type": "person", "normalized": "郑之悌（太府寺丞）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-004", "text": "太府寺丞", "type": "official", "normalized": "太府寺丞", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-004", "text": "徽州", "type": "place", "normalized": "徽州", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-004", "text": "汪纲", "type": "person", "normalized": "汪纲（知绍兴府）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-004", "text": "绍兴府", "type": "place", "normalized": "绍兴府", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-004", "text": "尚书启蒙", "type": "work", "normalized": "尚书启蒙（钱时撰）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-004", "text": "诗学管见", "type": "work", "normalized": "学诗管见（钱时撰）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-004", "text": "四书管见", "type": "work", "normalized": "四书管见（钱时撰）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-004", "text": "国朝编年", "type": "work", "normalized": "国朝编年（钱时撰）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "12-004", "text": "靖康", "type": "era", "normalized": "靖康（宋钦宗）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-004", "text": "穆修", "type": "person", "normalized": "穆修", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-004", "text": "真宗皇帝", "type": "person", "normalized": "宋真宗", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-004", "text": "吴如愚", "type": "person", "normalized": "吴如愚（成忠郎，隐居学者）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-004", "text": "成忠郎", "type": "official", "normalized": "成忠郎", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-004", "text": "迪功郎", "type": "official", "normalized": "迪功郎", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-004", "text": "秘阁校勘", "type": "official", "normalized": "秘阁校勘", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-004", "text": "从事郎", "type": "official", "normalized": "从事郎", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-004", "text": "三省", "type": "institution", "normalized": "三省（中书门下尚书）", "confidence": 0.9, "source": "原文片段"},

    # ============ 12-005 右劄付秘阁钱校勘（公文尾）============
    {"item_id": "12-005", "text": "秘阁钱校勘", "type": "person", "normalized": "钱时（融堂，宋严州布衣）", "confidence": 0.85, "source": "原文片段"},

    # ============ 12-006 嘉熙二年五月日押 ============
    {"item_id": "12-006", "text": "嘉熙", "type": "era", "normalized": "嘉熙（宋理宗）", "confidence": 0.9, "source": "原文片段"},

    # ============ 12-007 録白严州进书缴状（标题行）============

    # ============ 12-008 贴黄进书 ============
    {"item_id": "12-008", "text": "钱时", "type": "person", "normalized": "钱时（融堂，宋严州布衣）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-008", "text": "万荐", "type": "person", "normalized": "万荐（朝散大夫权知严州军州）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-008", "text": "朝散大夫", "type": "official", "normalized": "朝散大夫", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-008", "text": "权知严州军州", "type": "official", "normalized": "权知严州军州事", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-008", "text": "严州", "type": "place", "normalized": "严州", "confidence": 0.9, "source": "原文片段"},

    # ============ 12-009 尚书省劄 ============
    {"item_id": "12-009", "text": "尚书省", "type": "institution", "normalized": "尚书省", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-009", "text": "钱时", "type": "person", "normalized": "钱时（融堂，宋严州布衣）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-009", "text": "迪功郎", "type": "official", "normalized": "迪功郎", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-009", "text": "秘阁校勘", "type": "official", "normalized": "秘阁校勘", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-009", "text": "三省", "type": "institution", "normalized": "三省（中书门下尚书）", "confidence": 0.88, "source": "原文片段"},

    # ============ 12-010 劄付严州缮书百册 ============
    {"item_id": "12-010", "text": "严州", "type": "place", "normalized": "严州", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-010", "text": "钱时", "type": "person", "normalized": "钱时（融堂，宋严州布衣）", "confidence": 0.85, "source": "原文片段"},

    # ============ 12-011 钱时家塾尚书演义 ============
    {"item_id": "12-011", "text": "钱时家塾尚书演义", "type": "work", "normalized": "尚书演义（钱时家塾本）", "confidence": 0.88, "source": "原文片段"},

    # ============ 12-012 学诗管见 ============
    {"item_id": "12-012", "text": "学诗管见", "type": "work", "normalized": "学诗管见（钱时撰）", "confidence": 0.88, "source": "原文片段"},

    # ============ 12-013 周易释传 ============
    {"item_id": "12-013", "text": "周易释传", "type": "work", "normalized": "周易释传（钱时撰）", "confidence": 0.9, "source": "原文片段"},

    # ============ 12-014 四书管见 ============
    {"item_id": "12-014", "text": "四书管见", "type": "work", "normalized": "四书管见（钱时撰）", "confidence": 0.9, "source": "原文片段"},

    # ============ 12-015 两汉笔记 ============
    {"item_id": "12-015", "text": "两汉笔记", "type": "work", "normalized": "两汉笔记（钱时撰）", "confidence": 0.9, "source": "原文片段"},

    # ============ 12-016 进书装褙状（套语，无独立实体）============

    # ============ 12-017 嘉熙二年九月万荐上进 ============
    {"item_id": "12-017", "text": "嘉熙", "type": "era", "normalized": "嘉熙（宋理宗）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-017", "text": "万荐", "type": "person", "normalized": "万荐（朝散大夫权知严州军州）", "confidence": 0.88, "source": "原文片段"},

    # ============ 12-018 元江浙行省试士/胡长孺送诸生序 ============
    {"item_id": "12-018", "text": "江浙中书省", "type": "institution", "normalized": "江浙等处行中书省", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-018", "text": "钱唐", "type": "place", "normalized": "钱唐（杭州）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-018", "text": "蒙古色目", "type": "era", "normalized": "蒙古色目（元朝族群）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "12-018", "text": "锡都", "type": "person", "normalized": "锡都（蒙古色目人，江浙乡试举首）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-018", "text": "朱嵘", "type": "person", "normalized": "朱嵘", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-018", "text": "卢可继", "type": "person", "normalized": "卢可继", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-018", "text": "铙抃", "type": "person", "normalized": "铙抃", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-018", "text": "胡长孺", "type": "person", "normalized": "胡长孺（石塘先生，字汲仲，永康人）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-018", "text": "永康", "type": "place", "normalized": "永康", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-018", "text": "丞相府", "type": "institution", "normalized": "丞相府", "confidence": 0.82, "source": "原文片段"},

    # ============ 12-019 胡石塘诗序+诗 ============
    {"item_id": "12-019", "text": "胡石塘先生", "type": "person", "normalized": "胡长孺（石塘先生，字汲仲，永康人）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-019", "text": "锡都", "type": "person", "normalized": "锡都（蒙古色目人，江浙乡试举首）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-019", "text": "仇远", "type": "person", "normalized": "仇远", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-019", "text": "戴表元", "type": "person", "normalized": "戴表元", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-019", "text": "揭文安公", "type": "person", "normalized": "揭傒斯（揭文安公）", "confidence": 0.85, "source": "原文片段"},

    # ============ 12-020 昆山张经/张篠庵格言 ============
    {"item_id": "12-020", "text": "昆山", "type": "place", "normalized": "昆山", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-020", "text": "张经", "type": "person", "normalized": "张经（字伯绪，昆山进士，邢宽榜）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-020", "text": "邢宽", "type": "person", "normalized": "邢宽（榜进士）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "12-020", "text": "张篠庵", "type": "person", "normalized": "张篠庵（张经兄弟业师）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-020", "text": "进士", "type": "official", "normalized": "进士", "confidence": 0.85, "source": "原文片段"},

    # ============ 12-021 杨文敏公行状/邓真奏事 ============
    {"item_id": "12-021", "text": "杨文敏公", "type": "person", "normalized": "杨荣（东杨文敏）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "12-021", "text": "永乐", "type": "era", "normalized": "永乐（明成祖年号）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "12-021", "text": "五府六部三法司", "type": "institution", "normalized": "五府六部三法司", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-021", "text": "邓真", "type": "person", "normalized": "邓真（监察御史）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-021", "text": "监察御史", "type": "official", "normalized": "监察御史", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-021", "text": "王文端公", "type": "person", "normalized": "王文端公（姓名待考，撰杨荣传）", "confidence": 0.72, "source": "原文片段"},

    # ============ 12-022 杨荣诸传记异同考 ============
    {"item_id": "12-022", "text": "杨文敏公", "type": "person", "normalized": "杨荣（东杨文敏）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-022", "text": "北京国子监祭酒", "type": "official", "normalized": "国子监祭酒", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-022", "text": "五府六部三法司", "type": "institution", "normalized": "五府六部三法司", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-022", "text": "杨文贞公", "type": "person", "normalized": "杨士奇（西杨文贞）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-022", "text": "杨文定公", "type": "person", "normalized": "杨溥（南杨文定）", "confidence": 0.9, "source": "原文片段"},

    # ============ 12-023 姚铉唐文粹序 ============
    {"item_id": "12-023", "text": "姚铉", "type": "person", "normalized": "姚铉（吴兴，《唐文粹》编者）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-023", "text": "吴兴", "type": "place", "normalized": "吴兴", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-023", "text": "唐文粹", "type": "work", "normalized": "唐文粹（姚铉编，百卷）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "12-023", "text": "祥符", "type": "era", "normalized": "大中祥符（宋真宗）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-023", "text": "昭明太子", "type": "person", "normalized": "萧统（昭明太子）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-023", "text": "文选", "type": "work", "normalized": "文选（昭明太子编）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-023", "text": "韩吏部", "type": "person", "normalized": "韩愈（韩吏部，退之）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "12-023", "text": "柳子厚", "type": "person", "normalized": "柳宗元（柳子厚）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-023", "text": "白尚书居易", "type": "person", "normalized": "白居易", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-023", "text": "刘賔客禹锡", "type": "person", "normalized": "刘禹锡（刘宾客）", "confidence": 0.85, "source": "原文片段"},

    # ============ 12-024 日记故事善本考 ============
    {"item_id": "12-024", "text": "建安", "type": "place", "normalized": "建安（建宁）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-024", "text": "虞韶", "type": "person", "normalized": "虞韶（字以成，建安）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-024", "text": "日记故事", "type": "work", "normalized": "日记故事（虞韶编）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-024", "text": "杨文公", "type": "person", "normalized": "杨亿（杨文公）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "12-024", "text": "朱晦庵", "type": "person", "normalized": "朱熹（晦庵，即朱文公）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "12-024", "text": "襄城李公", "type": "person", "normalized": "襄城李公（重刊日记故事者，姓名待考）", "confidence": 0.7, "source": "原文片段"},
    {"item_id": "12-024", "text": "沈易", "type": "person", "normalized": "沈易（五伦诗作者）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "12-024", "text": "五伦诗", "type": "work", "normalized": "五伦诗（沈易撰）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "12-024", "text": "刘贡父", "type": "person", "normalized": "刘攽（刘贡父）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "12-024", "text": "宋太宗", "type": "person", "normalized": "宋太宗", "confidence": 0.85, "source": "原文片段"},
]
# 缺口登记：
# 12-003/12-007 为标题行（録白宋省劄/録白严州进书缴状），无独立实体；
# 12-005/12-016 为公文尾/装褙状套语，实体并入上下条；
# 12-023 唐文粹序历数历代文家（屈宋贾董班曹刘潘陆颜谢徐庾沈宋李杜张燕苏许萧常李翱皇甫湜元结独孤及吕温梁肃权德舆元稹等），择其 Structural 者标注，余从略。
