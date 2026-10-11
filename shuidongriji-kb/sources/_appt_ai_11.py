# -*- coding: utf-8 -*-
"""《水东日记》卷 11 —— APPT 职官任职 源数据（AI 判定逐条填写）

说明：任职记录：person(人物含 person_ent_ids)/office(官职含 official_ent_ids)/institution(机构含 ent_ids)/when(时间，未明写'未明')/status(任职状态)/evidence(证据)

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：现任=在任 / 致仕=退休 / 升迁=晋升调任 / 贬谪=降职流放 / 罢黜=罢官 / 兼领=兼职兼任 / 暂代=暂时代理 / 追赠=死后追赠 / 未明=原文未明写
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

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
# 示例记录（保留作格式对照）：
# {"appointment_id": "APPT-001", "item_id": "01-004", "person": {"text": "汪澄", "person_ent_ids": ["ENT-xxx"]}, "office": {"text": "巡按御史", "official_ent_ids": ["ENT-xxx"]}, "institution": {"text": "福建（巡按）", "ent_ids": ["ENT-xxx"]}, "when": "正统十三年", "status": "现任", "evidence": "巡按御史汪澄将至延平", "confidence": 0.92}

DATA = [
    # 11-001 王轸
    {"appointment_id": "APPT-5501", "item_id": "11-001",
     "person": {"text": "王轸", "person_ent_ids": []},
     "office": {"text": "浙右登科举人（平凉司任所）", "official_ent_ids": []},
     "institution": {"text": "平凉", "ent_ids": []},
     "when": "洪武四年", "status": "现任",
     "evidence": "系浙右登科举人王轸之父，书欲管勾宇文桂转达平凉子之任所",
     "confidence": 0.82},
    {"appointment_id": "APPT-5502", "item_id": "11-001",
     "person": {"text": "宇文桂", "person_ent_ids": []},
     "office": {"text": "御史台管勾", "official_ent_ids": []},
     "institution": {"text": "御史台", "ent_ids": []},
     "when": "洪武", "status": "现任",
     "evidence": "御史台管勾宇文桂因事被问",
     "confidence": 0.82},
    # 11-006 仁庙宫僚
    {"appointment_id": "APPT-5503", "item_id": "11-006",
     "person": {"text": "徐善述", "person_ent_ids": []},
     "office": {"text": "左春坊左赞善（赠太子少保，谥文肃）", "official_ent_ids": []},
     "institution": {"text": "春坊", "ent_ids": []},
     "when": "永乐", "status": "追赠",
     "evidence": "宫僚邹济、徐善述、王汝玉以及杨士奇、梁潜、蒋用文等皆被诗文宝翰之赐",
     "confidence": 0.85},
    {"appointment_id": "APPT-5504", "item_id": "11-011",
     "person": {"text": "杨士奇", "person_ent_ids": []},
     "office": {"text": "翰林院学士兼左春坊左谕德", "official_ent_ids": []},
     "institution": {"text": "翰林院/左春坊", "ent_ids": []},
     "when": "永乐十七年", "status": "现任",
     "evidence": "翰林院学士兼左春坊左谕德杨士奇",
     "confidence": 0.88},
    {"appointment_id": "APPT-5505", "item_id": "11-011",
     "person": {"text": "邹济", "person_ent_ids": []},
     "office": {"text": "左春坊左庶子", "official_ent_ids": []},
     "institution": {"text": "左春坊", "ent_ids": []},
     "when": "永乐十七年", "status": "现任",
     "evidence": "左春坊庶子邹济",
     "confidence": 0.85},
    # 11-017 阮安
    {"appointment_id": "APPT-5506", "item_id": "11-017",
     "person": {"text": "阮安（阿留）", "person_ent_ids": []},
     "office": {"text": "太监（营建）", "official_ent_ids": []},
     "institution": {"text": "工部/内官监", "ent_ids": []},
     "when": "永乐至正统", "status": "现任",
     "evidence": "太监阮安，交阯人，清苦介洁，善谋画，尤长工作之事",
     "confidence": 0.85},
]
