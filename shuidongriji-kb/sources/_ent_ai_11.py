# -*- coding: utf-8 -*-
"""《水东日记》卷 11 —— L1 实体标注 源数据（AI 判定逐条填写）

说明：实体标注：每条记录标注该条目中的实体（text=原文字面，type=实体类型，normalized=归一词形，confidence=置信度）

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：person=人物 / official=职官名 / institution=机构衙门 / place=地名 / era=年号朝代 / posthumous=谥号 / work=书名文献名 / unknown=类型待定
  * 未建模条目在下方注释中如实单列，不强行编造

填写方式：把 DATA 中的示例记录替换为本卷实际判定结果；
         每条记录为一个 dict；未判定条目保留注释占位。
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "11-001 | 五伦书已载有王轸家书事示劝万世矣轸嘉兴人也尝询得之今恭録诏文",
    "11-002 | 洪武四年闰三月　　日",
    "11-003 | 布衣臣王某言伏圣恩赐臣诏书并银绢椒药谨上表称谢者伏以圣明御",
    "11-004 | 自旧年十一月初二日南浔别后至今年凡四得书鎭江髙邮宁陵郑州者余",
    "11-005 | 今俗呼五十两重银锭曰元寳尝见独石内官弓胜得埋藏银数十锭形制皆",
    "11-006 | 仁庙好文之主宫僚邹济徐善述王汝玉以及杨士奇梁潜蒋御医用文等皆",
    "11-007 | 令防说与好古尔将选诗内取易入手解意的诗分赋比兴三字每字要十",
    "11-008 | 皇太子致书賛善好古先生余今欲学作表卿可一如诗题立例意思余为搆",
    "11-009 | 冬至赐賛善徐好古淸朝盛文治辅德资儒耆念彼筋力倦趋朝谅非宜赋诗",
    "11-010 | 皇太子特以牲醴之奠致祭于故赞善徐好古之灵曰卿伟量渊宏博览古今",
    "11-011 | 皇帝遣天台县某官谕祭于故赞善赠太子少保谥文肃善述曰卿昔从朕于",
    "11-012 | 东驾文出亲制洪熈中文意当笔词臣有深意焉盖尝见一时王文靖祭文内",
    "11-013 | 戏言辩口轻为讦迫亦足以取怨得罪于人尝闻修永乐大典时诸儒羣集一",
    "11-014 | 虞文靖公为秘书少监日着朱宜人吉氏墓碣【石本作碣铭】其畧曰鎭【",
    "11-015 | 黾勉依伯生先生命抄録一过愿并请先生书之庶永传也巙敬吿泽民提学",
    "11-016 | 朱文公先生考定欧阳文忠公事迹有云平心保州妖尼三事公平生学问根",
    "11-017 | 太监阮安一名阿留交阯人为人淸苦介洁善谋画尤长于工作之事其修营",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
# 示例记录（保留作格式对照）：
# {"item_id": "01-001", "text": "礼部尚书", "type": "official", "normalized": "礼部尚书", "confidence": 0.97, "source": "原文片段"}

DATA = [
    # 11-001 王轸家书
    {"item_id": "11-001", "text": "五伦书", "type": "work", "normalized": "五伦书", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-001", "text": "王轸", "type": "person", "normalized": "王轸（嘉兴，登科举人）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-001", "text": "嘉兴", "type": "place", "normalized": "嘉兴", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-001", "text": "宇文桂", "type": "person", "normalized": "宇文桂（御史台管勾）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-001", "text": "平凉", "type": "place", "normalized": "平凉（府）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-001", "text": "洪武", "type": "era", "normalized": "洪武（明太祖）", "confidence": 0.88, "source": "原文片段"},
    # 11-003 谢表
    {"item_id": "11-003", "text": "布衣臣王某", "type": "person", "normalized": "王轸之父（布衣）", "confidence": 0.82, "source": "原文片段"},
    # 11-004 家书
    {"item_id": "11-004", "text": "南浔", "type": "place", "normalized": "南浔", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-004", "text": "德清", "type": "place", "normalized": "德清", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-004", "text": "里长", "type": "official", "normalized": "里长", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-004", "text": "甲首", "type": "official", "normalized": "甲首", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-004", "text": "弓兵", "type": "official", "normalized": "弓兵", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-004", "text": "康节先生", "type": "person", "normalized": "邵雍（谥康节）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-004", "text": "盩厔", "type": "place", "normalized": "盩厔", "confidence": 0.8, "source": "原文片段"},
    # 11-005 元宝
    {"item_id": "11-005", "text": "独石", "type": "place", "normalized": "独石", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-005", "text": "弓胜", "type": "person", "normalized": "弓胜（内官）", "confidence": 0.8, "source": "原文片段"},
    # 11-006 仁庙
    {"item_id": "11-006", "text": "仁庙", "type": "person", "normalized": "明仁宗（洪熙）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "11-006", "text": "邹济", "type": "person", "normalized": "邹济（春坊官）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-006", "text": "徐善述", "type": "person", "normalized": "徐善述（赞善，谥文肃）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-006", "text": "王汝玉", "type": "person", "normalized": "王汝玉", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-006", "text": "杨士奇", "type": "person", "normalized": "杨士奇", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "11-006", "text": "梁潜", "type": "person", "normalized": "梁潜", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-006", "text": "马尚书", "type": "person", "normalized": "马尚书", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "11-006", "text": "永乐", "type": "era", "normalized": "永乐（明成祖）", "confidence": 0.88, "source": "原文片段"},
    # 11-007/11-008 好古
    {"item_id": "11-007", "text": "好古", "type": "person", "normalized": "徐好古（赞善）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-007", "text": "王燧真", "type": "person", "normalized": "王燧真", "confidence": 0.78, "source": "原文片段"},
    # 11-011 祭文
    {"item_id": "11-011", "text": "杨荣", "type": "person", "normalized": "杨荣（文敏）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "11-011", "text": "钱习礼", "type": "person", "normalized": "钱习礼", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-011", "text": "王英", "type": "person", "normalized": "王英", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-011", "text": "苗衷", "type": "person", "normalized": "苗衷", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-011", "text": "曾棨", "type": "person", "normalized": "曾棨", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-011", "text": "蹇义", "type": "person", "normalized": "蹇义（谥忠定）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-011", "text": "杨溥", "type": "person", "normalized": "杨溥（文定）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-011", "text": "黄宗载", "type": "person", "normalized": "黄宗载", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "11-011", "text": "陈济", "type": "person", "normalized": "陈济（赞善）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "11-011", "text": "邹缉", "type": "person", "normalized": "邹缉（侍讲）", "confidence": 0.8, "source": "原文片段"},
    # 11-013 王偁
    {"item_id": "11-013", "text": "王偁", "type": "person", "normalized": "王偁（永乐大典）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "11-013", "text": "徐有贞", "type": "person", "normalized": "徐有贞（武功伯）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-013", "text": "于谦", "type": "person", "normalized": "于谦（少保）", "confidence": 0.88, "source": "原文片段"},
    # 11-014 朱德润
    {"item_id": "11-014", "text": "虞文靖公", "type": "person", "normalized": "虞集（谥文靖）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-014", "text": "朱德润", "type": "person", "normalized": "朱德润（字泽民）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-014", "text": "阳抱山", "type": "place", "normalized": "阳抱山", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-014", "text": "陆绩", "type": "person", "normalized": "陆绩（吴郁林太守）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-014", "text": "昆山", "type": "place", "normalized": "昆山", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-014", "text": "泰定四年", "type": "era", "normalized": "泰定四年（元泰定帝）", "confidence": 0.82, "source": "原文片段"},
    # 11-016 朱文公欧阳公
    {"item_id": "11-016", "text": "朱文公", "type": "person", "normalized": "朱熹", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "11-016", "text": "欧阳文忠公", "type": "person", "normalized": "欧阳修", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-016", "text": "青苗", "type": "unknown", "normalized": "青苗法", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-016", "text": "韩魏公", "type": "person", "normalized": "韩琦（封魏公）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-016", "text": "王安石", "type": "person", "normalized": "王安石", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-016", "text": "吕思诚", "type": "person", "normalized": "吕思诚（谥忠肃，平定）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "11-016", "text": "耿九畴", "type": "person", "normalized": "耿九畴（号恒庵，尚书）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-016", "text": "南村辍耕录", "type": "work", "normalized": "南村辍耕录（陶宗仪）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-016", "text": "天顺四年", "type": "era", "normalized": "天顺四年（1460）", "confidence": 0.85, "source": "原文片段"},
    # 11-017 阮安
    {"item_id": "11-017", "text": "阮安", "type": "person", "normalized": "阮安（一名阿留，交阯太监）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "11-017", "text": "交阯", "type": "place", "normalized": "交阯", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-017", "text": "北京城池", "type": "place", "normalized": "北京城池/九门/两宫三殿", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "11-017", "text": "王振", "type": "person", "normalized": "王振（太监）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "11-017", "text": "张秋河", "type": "place", "normalized": "张秋河（决口）", "confidence": 0.82, "source": "原文片段"},
]
