# -*- coding: utf-8 -*-
"""《水东日记》卷 11 —— NAM 名录谱牒（结构分类） 源数据（AI 判定逐条填写）

说明：名录记录：name/category/scope/entries(四元组数组 {seq,person,courtesy_name,hometown,office})/ent_ids；书信中仅提及族谱者 entries 空数组+evidence 注明

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：官员题名=官员任职题名（表格式） / 同僚题名=同僚共事题名（表格式） / 迁谪录=迁谪记录 / 谱牒=族谱家谱（含话题登记） / 题名记=题名记文 / 其他=其他
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

# 字段键（打包器校验用）：nam_id, item_id, name, category, scope, entries, ent_ids, confidence
# 示例记录（保留作格式对照）：
# {"nam_id": "NAM-001", "item_id": "17-002", "name": "都御史题名（天顺、景泰末年）", "category": "官员题名", "scope": "都察院·都御史（左/右/副/佥都御史）", "entries": [{"seq": 1, "person": "杨善", "courtesy_name": "未明", "hometown": "未明", "office": "左都御史（天顺）"}], "ent_ids": ["ENT-xxx"], "confidence": 0.95}

DATA = [
    # 11-011 永乐十七年谕祭徐善述官僚名单
    {"nam_id": "NAM-5501", "item_id": "11-011",
     "name": "永乐十七年谕祭徐善述同寅官僚题名",
     "category": "同僚题名",
     "scope": "翰林院/春坊/六部（谕祭故赞善徐善述）",
     "entries": [
         {"seq": 1, "person": "杨士奇", "courtesy_name": "未明", "hometown": "泰和", "office": "翰林院学士兼左春坊左谕德"},
         {"seq": 2, "person": "杨荣", "courtesy_name": "未明", "hometown": "建安", "office": "未明（翰林院）"},
         {"seq": 3, "person": "邹济", "courtesy_name": "未明", "hometown": "未明", "office": "左春坊左庶子"},
         {"seq": 4, "person": "钱习礼", "courtesy_name": "未明", "hometown": "吉水", "office": "翰林院侍读"},
         {"seq": 5, "person": "陈全", "courtesy_name": "未明", "hometown": "未明", "office": "侍讲"},
         {"seq": 6, "person": "王英", "courtesy_name": "未明", "hometown": "金溪", "office": "春坊右中允"},
         {"seq": 7, "person": "苗衷", "courtesy_name": "未明", "hometown": "凤阳", "office": "翰林院编修"},
         {"seq": 8, "person": "曾棨", "courtesy_name": "未明", "hometown": "永丰", "office": "检讨"},
         {"seq": 9, "person": "蹇义", "courtesy_name": "未明", "hometown": "巴县", "office": "吏部尚书"},
         {"seq": 10, "person": "杨溥", "courtesy_name": "未明", "hometown": "石首", "office": "翰林院修撰"},
         {"seq": 11, "person": "黄宗载", "courtesy_name": "未明", "hometown": "丰城", "office": "春坊右中允"},
         {"seq": 12, "person": "陈济", "courtesy_name": "未明", "hometown": "武进", "office": "赞善"},
         {"seq": 13, "person": "邹缉", "courtesy_name": "未明", "hometown": "未明", "office": "侍讲"},
         {"seq": 14, "person": "李兴", "courtesy_name": "未明", "hometown": "未明", "office": "郎中"},
         {"seq": 15, "person": "施显", "courtesy_name": "未明", "hometown": "未明", "office": "员外郎"},
         {"seq": 16, "person": "贞完", "courtesy_name": "未明", "hometown": "未明", "office": "主事"},
         {"seq": 17, "person": "陈璲", "courtesy_name": "未明", "hometown": "未明", "office": "检讨"},
     ],
     "ent_ids": ["ENT-1871", "ENT-484", "ENT-1868", "ENT-1877", "ENT-1920", "ENT-1878", "ENT-1879", "ENT-1880", "ENT-1279", "ENT-197", "ENT-1882", "ENT-1883", "ENT-1884", "ENT-1921", "ENT-1922", "ENT-1923", "ENT-1600"],  # 集成补建
     "evidence": "永乐十七年十一月丁未，杨士奇、杨荣、邹济等致祭于徐好古之灵",
     "confidence": 0.82},
]
