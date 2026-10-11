# -*- coding: utf-8 -*-
"""《水东日记》卷 09 —— L1 实体标注 源数据（AI 判定逐条填写）

说明：实体标注：每条记录标注该条目中的实体（text=原文字面，type=实体类型，normalized=归一词形，confidence=置信度）

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：person=人物 / official=职官名 / institution=机构衙门 / place=地名 / era=年号朝代 / posthumous=谥号 / work=书名文献名 / unknown=类型待定
  * 未建模条目在下方注释中如实单列，不强行编造

填写方式：把 DATA 中的示例记录替换为本卷实际判定结果；
         每条记录为一个 dict；未判定条目保留注释占位。
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "09-001 | 予性颇不喜场屋程文异时所作四书经义亦不多惟书经大小题俱有破题",
    "09-002 | 文章不许他人轻改一字盖昔大贤君子如欧阳文忠公已然若王半山以下",
    "09-003 | 今日得蕲州寄来王信伯集并语録读之骇人此洞记所为作也然以一噎而",
    "09-004 | 明道程先生【止】卑忠信而小之也",
    "09-005 | 世固有忠信而不知道者如孔子所称忠信而不好学者伊川所讥笃学力行",
    "09-006 | 关洛绪言【止】盍思所以反之也",
    "09-007 | 程氏之言学之本末始终无所不具非专立为成德者言也今此语意似亦少",
    "09-008 | 政使止于章句文义之间【止】三代之始终也",
    "09-009 | 三代之教自离经辨志以后节次有进步处是以始乎为士而终乎为圣人也",
    "09-010 | 自有此山以来【止】亦君子之意也",
    "09-011 | 所谓与日月叅光者不知何所指更望批喻其曰区区濬之者又恐卑之已甚",
    "09-012 | 鄙意欲如第一段所论引明道劄子后即云不幸其说不试而王氏得政知俗",
    "09-013 | 淳熙六年南康军秋雨不时高仰之田告病郡守新安朱侯熹行眂陂塘竝庐",
    "09-014 | 人至辱手书得闻春来尊体益轻徤放杖徐行又有问花随栁之乐甚慰记文",
    "09-015 | 尤首祸自创干戈之制轩辕因戮之处则象吻于宫行则悬旄于纛以示戒",
    "09-016 | 元儒三山梁益题黄筌三雀图谓院画皆有名义是图盖取诗礼春秋传三爵",
    "09-017 | 前年过泰和谒杨尚书淑简王抑庵尚书见杨氏春帖云世承良吏德门倚素",
    "09-018 | 老姻家自今夏总裁校书天下老儒凡廿七人悉在",
    "09-019 | 下处取决劳心之甚又孟氏之书词气抑扬之太过者八十五条卒九月间方",
    "09-020 | 宋儒批选文章今可见者前有吕东莱次则楼迂斋周应龙又其次则谢叠山",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
# 示例记录（保留作格式对照）：
# {"item_id": "01-001", "text": "礼部尚书", "type": "official", "normalized": "礼部尚书", "confidence": 0.97, "source": "原文片段"}

DATA = [
    # 09-001 程文/彭氏一经
    {"item_id": "09-001", "text": "王滹南", "type": "person", "normalized": "王滹南（王若虚，金）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-001", "text": "欧阳圭斋", "type": "person", "normalized": "欧阳玄（号圭斋）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-001", "text": "彭士楚", "type": "person", "normalized": "彭士楚（庐陵）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-001", "text": "彭冲", "type": "person", "normalized": "彭冲（泰定甲子进士）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "09-001", "text": "泰定甲子", "type": "era", "normalized": "泰定甲子（元泰定元年）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-001", "text": "至元六年庚辰", "type": "era", "normalized": "至元六年庚辰（后至元六年，1340）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-001", "text": "翰林侍讲学士", "type": "official", "normalized": "翰林侍讲学士", "confidence": 0.82, "source": "原文片段"},
    # 09-002 白鹿书院记
    {"item_id": "09-002", "text": "欧阳文忠公", "type": "person", "normalized": "欧阳修（谥文忠）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-002", "text": "王半山", "type": "person", "normalized": "王安石（号半山）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-002", "text": "晦庵", "type": "person", "normalized": "朱熹（号晦庵）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "09-002", "text": "东莱", "type": "person", "normalized": "吕祖谦（号东莱）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-002", "text": "白鹿书院记", "type": "work", "normalized": "白鹿书院记", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-002", "text": "庐山", "type": "place", "normalized": "庐山", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-002", "text": "星子令王仲杰", "type": "person", "normalized": "王仲杰（星子令）", "confidence": 0.8, "source": "原文片段"},
    # 09-003 王信伯集
    {"item_id": "09-003", "text": "王信伯", "type": "person", "normalized": "王信伯（王蘋，宋）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "09-003", "text": "蕲州", "type": "place", "normalized": "蕲州", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-003", "text": "程张先生", "type": "person", "normalized": "程颢、程颐、张载", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-003", "text": "明道", "type": "person", "normalized": "程颢（号明道）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-003", "text": "王氏", "type": "person", "normalized": "王安石（新学）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-003", "text": "熙丰崇宣", "type": "era", "normalized": "熙宁元丰崇宁宣和", "confidence": 0.8, "source": "原文片段"},
    # 09-004/09-005 忠信不知道
    {"item_id": "09-005", "text": "伊川", "type": "person", "normalized": "程颐（号伊川）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-005", "text": "孔子", "type": "person", "normalized": "孔子", "confidence": 0.85, "source": "原文片段"},
    # 09-011 马伏波
    {"item_id": "09-011", "text": "马伏波", "type": "person", "normalized": "马援（封伏波将军）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-011", "text": "杜季良", "type": "person", "normalized": "杜季良（汉）", "confidence": 0.8, "source": "原文片段"},
    # 09-012 书院之立
    {"item_id": "09-012", "text": "建炎中兴", "type": "era", "normalized": "建炎（南宋高宗）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-012", "text": "嘉祐治平", "type": "era", "normalized": "嘉祐治平（北宋仁宗英宗）", "confidence": 0.82, "source": "原文片段"},
    # 09-013 白鹿书院
    {"item_id": "09-013", "text": "淳熙六年", "type": "era", "normalized": "淳熙六年（南宋孝宗，1179）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-013", "text": "南康军", "type": "place", "normalized": "南康军", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-013", "text": "朱侯熹", "type": "person", "normalized": "朱熹（知南康军）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "09-013", "text": "李渤", "type": "person", "normalized": "李渤（唐，白鹿洞隐居）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-013", "text": "太宗皇帝", "type": "person", "normalized": "宋太宗", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-013", "text": "南唐", "type": "era", "normalized": "南唐", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-013", "text": "杨大灋", "type": "person", "normalized": "杨大法（军学教授）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "09-013", "text": "祖谦", "type": "person", "normalized": "吕祖谦（作记）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-013", "text": "嵩阳岳麓睢阳", "type": "place", "normalized": "嵩阳/岳麓/睢阳书院", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-013", "text": "河南程氏", "type": "person", "normalized": "程颢程颐（洛阳）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-013", "text": "横渠张氏", "type": "person", "normalized": "张载（横渠）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-013", "text": "熙宁", "type": "era", "normalized": "熙宁（北宋神宗）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-013", "text": "郭祥正", "type": "person", "normalized": "郭祥正（当涂）", "confidence": 0.8, "source": "原文片段"},
    # 09-014 黄子厚
    {"item_id": "09-014", "text": "黄子厚", "type": "person", "normalized": "黄子厚（隶书）", "confidence": 0.8, "source": "原文片段"},
    # 09-015 鸱吻
    {"item_id": "09-015", "text": "蚩尤", "type": "person", "normalized": "蚩尤", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-015", "text": "轩辕", "type": "person", "normalized": "轩辕黄帝", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-015", "text": "鸱吻", "type": "unknown", "normalized": "鸱吻（屋脊兽）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-015", "text": "夏忠靖公", "type": "person", "normalized": "夏原吉（谥忠靖）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-015", "text": "解大绅", "type": "person", "normalized": "解缙（字大绅）", "confidence": 0.85, "source": "原文片段"},
    # 09-016 黄筌三雀图
    {"item_id": "09-016", "text": "梁益", "type": "person", "normalized": "梁益（三山，元儒）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "09-016", "text": "黄筌", "type": "person", "normalized": "黄筌（蜀画家）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-016", "text": "三雀图", "type": "work", "normalized": "黄筌三雀图", "confidence": 0.82, "source": "原文片段"},
    # 09-017 刘三吾与陈南宾书
    {"item_id": "09-017", "text": "杨尚书淑简", "type": "person", "normalized": "杨尚书淑简（泰和）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "09-017", "text": "王抑庵", "type": "person", "normalized": "王直（号抑庵）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-017", "text": "东里公", "type": "person", "normalized": "杨士奇（号东里）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-017", "text": "杨文定公", "type": "person", "normalized": "杨溥（谥文定）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-017", "text": "陈南宾", "type": "person", "normalized": "陈南宾（长沙，蜀府长史）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "09-017", "text": "刘三吾", "type": "person", "normalized": "刘三吾（刘学士）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "09-017", "text": "戈佥事立", "type": "person", "normalized": "戈立（佥事）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "09-017", "text": "钱子予", "type": "person", "normalized": "钱子予（校书，老儒）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-017", "text": "泰和", "type": "place", "normalized": "泰和", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-017", "text": "蜀府", "type": "institution", "normalized": "蜀王府", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-017", "text": "安老堂", "type": "place", "normalized": "安老堂（蜀府堂名）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "09-017", "text": "钱子瑜", "type": "person", "normalized": "钱子瑜", "confidence": 0.8, "source": "原文片段"},
    # 09-020 宋儒批选文章
    {"item_id": "09-020", "text": "楼迂斋", "type": "person", "normalized": "楼昉（号迂斋）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "09-020", "text": "周应龙", "type": "person", "normalized": "周应龙（宋）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "09-020", "text": "谢叠山", "type": "person", "normalized": "谢枋得（号叠山）", "confidence": 0.85, "source": "原文片段"},
]
