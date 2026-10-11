# -*- coding: utf-8 -*-
"""《水东日记》卷 09 —— APPT 职官任职 源数据（AI 判定逐条填写）

说明：任职记录：person(人物含 person_ent_ids)/office(官职含 official_ent_ids)/institution(机构含 ent_ids)/when(时间，未明写'未明')/status(任职状态)/evidence(证据)

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：现任=在任 / 致仕=退休 / 升迁=晋升调任 / 贬谪=降职流放 / 罢黜=罢官 / 兼领=兼职兼任 / 暂代=暂时代理 / 追赠=死后追赠 / 未明=原文未明写
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

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
# 示例记录（保留作格式对照）：
# {"appointment_id": "APPT-001", "item_id": "01-004", "person": {"text": "汪澄", "person_ent_ids": ["ENT-xxx"]}, "office": {"text": "巡按御史", "official_ent_ids": ["ENT-xxx"]}, "institution": {"text": "福建（巡按）", "ent_ids": ["ENT-xxx"]}, "when": "正统十三年", "status": "现任", "evidence": "巡按御史汪澄将至延平", "confidence": 0.92}

DATA = [
    # 09-001 欧阳玄
    {"appointment_id": "APPT-4501", "item_id": "09-001",
     "person": {"text": "欧阳玄（圭斋）", "person_ent_ids": []},
     "office": {"text": "翰林侍讲学士、知制诰", "official_ent_ids": []},
     "institution": {"text": "翰林院", "ent_ids": []},
     "when": "后至元六年", "status": "现任",
     "evidence": "翰林侍讲学士、通奉大夫、知制诰、同修国史欧阳玄书",
     "confidence": 0.85},
    # 09-002/09-013 王仲杰
    {"appointment_id": "APPT-4502", "item_id": "09-013",
     "person": {"text": "王仲杰", "person_ent_ids": []},
     "office": {"text": "星子县令", "official_ent_ids": []},
     "institution": {"text": "南康军星子县", "ent_ids": []},
     "when": "淳熙六年", "status": "现任",
     "evidence": "星子县令王君仲杰董其事",
     "confidence": 0.82},
    {"appointment_id": "APPT-4503", "item_id": "09-013",
     "person": {"text": "朱熹", "person_ent_ids": []},
     "office": {"text": "知南康军", "official_ent_ids": []},
     "institution": {"text": "南康军", "ent_ids": []},
     "when": "淳熙六年", "status": "现任",
     "evidence": "郡守新安朱侯熹行视陂塘",
     "confidence": 0.85},
    {"appointment_id": "APPT-4504", "item_id": "09-013",
     "person": {"text": "杨大法", "person_ent_ids": []},
     "office": {"text": "军学教授", "official_ent_ids": []},
     "institution": {"text": "南康军学", "ent_ids": []},
     "when": "淳熙六年", "status": "现任",
     "evidence": "属军学教授杨君大法",
     "confidence": 0.8},
    # 09-017 陈南宾
    {"appointment_id": "APPT-4505", "item_id": "09-017",
     "person": {"text": "陈南宾", "person_ent_ids": []},
     "office": {"text": "蜀府长史", "official_ent_ids": []},
     "institution": {"text": "蜀王府", "ent_ids": []},
     "when": "洪武", "status": "现任",
     "evidence": "蜀府长史长沙陈南宾名士也",
     "confidence": 0.85},
    {"appointment_id": "APPT-4506", "item_id": "09-017",
     "person": {"text": "刘三吾", "person_ent_ids": []},
     "office": {"text": "学士", "official_ent_ids": []},
     "institution": {"text": "未明", "ent_ids": []},
     "when": "洪武", "status": "现任",
     "evidence": "藏刘学士三吾手笔与其先生书一缄",
     "confidence": 0.85},
]
