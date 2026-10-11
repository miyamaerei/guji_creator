# -*- coding: utf-8 -*-
"""《水东日记》卷 01 —— L1 实体标注 源数据（AI 判定逐条填写）

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
    "01-001 | 冬至正旦节早礼部鸿胪寺及科道导驾等官最先入左掖门至中左门立俟",
    "01-002 | 晦庵与刘清之书云小学近畧修改又别为题词韵语庶便童习又一书云见",
    "01-003 | 王忠毅公为京尹时公退即坐后堂召鼓手打得胜鼓以为乐鼔失节者有罚",
    "01-004 | 己巳之变徐元玉最有时名亦锐意功业太监金英趣问计以南迁对英怫然",
    "01-005 | 三五年前翰林名人送行文一首润笔银二三钱可求事变后文价顿高非五",
    "01-006 | 己巳七月十五日六师明日在行六科议兵刑二科文书多独用二人兵科都",
    "01-007 | 正统十四年八月二十三日殿下驾御午门左门言官大臣次第宣劾王振章",
    "01-008 | 季聦尝授经京邸多门生学子因多知内外事一日谓予曰闻禁中近习划龙",
    "01-009 | 初京都最重冬年节贺礼不问贵贱奔走往来者数日家置一册题名满幅己",
    "01-010 | 宣德正统间名臣称三杨先生以文贞为西杨文敏为东杨盖初以姓同亦畧",
    "01-011 | 盛奏选京师官舍家人操习以备非常及乞榜禁谕流言事见奏草当时有宥",
    "01-012 | 景泰元年九月二十六日礼部会奏敌请遣使迎复当从明日上立文华殿门",
    "01-013 | 大理少卿致仕云间沈简庵先生草圣擅一时真行皆佳尤长于诗有集二千",
    "01-014 | 毘陵王绂孟端高介絶俗之士所与交皆一时名人遇流俗辈辄白眼视之工",
    "01-015 | 驾将旋礼部累有会奏言迎复事上多以敌情多诈为言将抵居庸一奏始得",
    "01-016 | 初凡有弹纠必六科先承密防十三道则因之若不由先言实自盛等始都督",
    "01-017 | 永乐中俞行之试记里鼓正统中冯益试事道皆不知所谓莫能措一辞所谓",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
# 示例记录（保留作格式对照）：
# {"item_id": "01-001", "text": "礼部尚书", "type": "official", "normalized": "礼部尚书", "confidence": 0.97, "source": "原文片段"}

DATA = [
    # ============ 01-001 冬至正旦节早朝（示例 A，schemas.md §11）============
    {"item_id": "01-001", "text": "礼部", "type": "institution", "normalized": "礼部", "confidence": 0.97, "source": "原文片段"},
    {"item_id": "01-001", "text": "鸿胪寺", "type": "institution", "normalized": "鸿胪寺", "confidence": 0.97, "source": "原文片段"},
    {"item_id": "01-001", "text": "科道", "type": "official", "normalized": "科道", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-001", "text": "左掖门", "type": "place", "normalized": "左掖门", "confidence": 0.97, "source": "原文片段"},
    {"item_id": "01-001", "text": "中左门", "type": "place", "normalized": "中左门", "confidence": 0.97, "source": "原文片段"},
    {"item_id": "01-001", "text": "华盖殿", "type": "place", "normalized": "华盖殿", "confidence": 0.97, "source": "原文片段"},
    {"item_id": "01-001", "text": "奉天殿", "type": "place", "normalized": "奉天殿", "confidence": 0.97, "source": "原文片段"},
    {"item_id": "01-001", "text": "礼部尚书", "type": "official", "normalized": "礼部尚书", "confidence": 0.97, "source": "原文片段"},
    {"item_id": "01-001", "text": "毘陵", "type": "place", "normalized": "毘陵（毗陵）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-001", "text": "胡公", "type": "person", "normalized": "胡公（毘陵胡公=礼部尚书胡濙，待 alias 映射）", "confidence": 0.85, "source": "原文片段"},

    # ============ 01-002 晦庵小学书版本考 ============
    {"item_id": "01-002", "text": "晦庵", "type": "person", "normalized": "朱熹（晦庵，即朱文公）", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-002", "text": "刘清之", "type": "person", "normalized": "刘清之", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-002", "text": "小学", "type": "work", "normalized": "小学（朱熹编）", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-002", "text": "北京国子监", "type": "institution", "normalized": "北京国子监", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-002", "text": "元至正十三年", "type": "era", "normalized": "至正（元顺帝）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-002", "text": "元统癸酉", "type": "era", "normalized": "元统（元）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-002", "text": "王思诚", "type": "person", "normalized": "王思诚", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-002", "text": "危素", "type": "person", "normalized": "危素", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-002", "text": "熊太古", "type": "person", "normalized": "熊太古", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-002", "text": "朱文公", "type": "person", "normalized": "朱熹（晦庵，即朱文公）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-002", "text": "吴思庵", "type": "person", "normalized": "吴思庵", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-002", "text": "朱子大全", "type": "work", "normalized": "朱子大全", "confidence": 0.9, "source": "原文片段"},

    # ============ 01-003 王忠毅公击鼓 ============
    {"item_id": "01-003", "text": "王忠毅公", "type": "person", "normalized": "王忠毅公（王骥？谥忠毅，待考）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "01-003", "text": "京尹", "type": "official", "normalized": "京尹（顺天府尹）", "confidence": 0.9, "source": "原文片段"},

    # ============ 01-004 己巳之变（示例 B，schemas.md §11；保留原10条并扩展）============
    {"item_id": "01-004", "text": "徐元玉", "type": "person", "normalized": "徐元玉", "confidence": 0.97, "source": "原文片段"},
    {"item_id": "01-004", "text": "金英", "type": "person", "normalized": "金英（太监）", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-004", "text": "王通", "type": "person", "normalized": "王通（成山侯）", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-004", "text": "兴安", "type": "person", "normalized": "兴安（太监）", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-004", "text": "汪澄", "type": "person", "normalized": "汪澄", "confidence": 0.97, "source": "原文片段"},
    {"item_id": "01-004", "text": "张海", "type": "person", "normalized": "张海", "confidence": 0.97, "source": "原文片段"},
    {"item_id": "01-004", "text": "姚铣", "type": "person", "normalized": "姚铣（兵科给事中）", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-004", "text": "延平", "type": "place", "normalized": "延平", "confidence": 0.97, "source": "原文片段"},
    {"item_id": "01-004", "text": "处州", "type": "place", "normalized": "处州", "confidence": 0.97, "source": "原文片段"},
    {"item_id": "01-004", "text": "京师", "type": "place", "normalized": "京师", "confidence": 0.95, "source": "原文片段"},
    # ---- 01-004 扩展 ----
    {"item_id": "01-004", "text": "正统", "type": "era", "normalized": "正统（明英宗）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-004", "text": "邓茂七", "type": "person", "normalized": "邓茂七（闽寇）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-004", "text": "巡按御史", "type": "official", "normalized": "巡按御史", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-004", "text": "刷卷御史", "type": "official", "normalized": "刷卷御史", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-004", "text": "丁瑄", "type": "person", "normalized": "丁瑄", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-004", "text": "兵科给事中", "type": "official", "normalized": "兵科给事中", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-004", "text": "唐世良", "type": "person", "normalized": "唐世良", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-004", "text": "兵部", "type": "institution", "normalized": "兵部", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-004", "text": "林廷举", "type": "person", "normalized": "林廷举", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-004", "text": "两浙", "type": "place", "normalized": "两浙", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-004", "text": "盛", "type": "person", "normalized": "叶盛（作者，自称盛）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-004", "text": "山西", "type": "place", "normalized": "山西", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-004", "text": "参政", "type": "official", "normalized": "参政", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-004", "text": "厚", "type": "person", "normalized": "林厚（林廷举父，山西参政）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "01-004", "text": "代州", "type": "place", "normalized": "代州", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-004", "text": "都御史", "type": "official", "normalized": "都御史", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-004", "text": "张楷", "type": "person", "normalized": "张楷", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-004", "text": "都督", "type": "official", "normalized": "都督", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-004", "text": "刘聚", "type": "person", "normalized": "刘聚", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-004", "text": "尚书", "type": "official", "normalized": "尚书", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-004", "text": "石璞", "type": "person", "normalized": "石璞", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-004", "text": "徐恭", "type": "person", "normalized": "徐恭", "confidence": 0.92, "source": "原文片段"},

    # ============ 01-005 翰林文价与相者 ============
    {"item_id": "01-005", "text": "翰林", "type": "institution", "normalized": "翰林院（翰林）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-005", "text": "钱原溥", "type": "person", "normalized": "钱原溥", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-005", "text": "张士谦", "type": "person", "normalized": "张士谦", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-005", "text": "永乐", "type": "era", "normalized": "永乐（明成祖）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-005", "text": "中书舍人", "type": "official", "normalized": "中书舍人", "confidence": 0.88, "source": "原文片段"},

    # ============ 01-006 六科点差 ============
    {"item_id": "01-006", "text": "六科", "type": "institution", "normalized": "六科", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-006", "text": "兵科都给事中", "type": "official", "normalized": "兵科都给事中", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-006", "text": "姚铣", "type": "person", "normalized": "姚铣（兵科给事中）", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-006", "text": "鲍煇", "type": "person", "normalized": "鲍煇", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-006", "text": "季聦", "type": "person", "normalized": "季聪（季聦）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-006", "text": "都察院", "type": "institution", "normalized": "都察院", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-006", "text": "尚寳司", "type": "institution", "normalized": "尚宝司", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-006", "text": "瑾", "type": "person", "normalized": "瑾（六科掌印官？待考）", "confidence": 0.6, "source": "原文片段"},

    # ============ 01-007 午门击杀王振党 ============
    {"item_id": "01-007", "text": "午门", "type": "place", "normalized": "午门", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-007", "text": "王振", "type": "person", "normalized": "王振", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-007", "text": "仪公", "type": "person", "normalized": "仪公（长史，姓名待考）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "01-007", "text": "王给事中竑", "type": "person", "normalized": "王竑（给事中）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-007", "text": "马顺", "type": "person", "normalized": "马顺", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-007", "text": "王长随", "type": "person", "normalized": "王长随", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-007", "text": "毛长随", "type": "person", "normalized": "毛长随", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-007", "text": "锦衣卫", "type": "institution", "normalized": "锦衣卫", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-007", "text": "左掖门", "type": "place", "normalized": "左掖门", "confidence": 0.95, "source": "原文片段"},

    # ============ 01-008 季聪京邸/太常除官/户口 ============
    {"item_id": "01-008", "text": "季聦", "type": "person", "normalized": "季聪（季聦）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-008", "text": "兴安", "type": "person", "normalized": "兴安（太监）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-008", "text": "南京", "type": "place", "normalized": "南京", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-008", "text": "南京太常卿", "type": "official", "normalized": "南京太常寺卿", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-008", "text": "徐初", "type": "person", "normalized": "徐初", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-008", "text": "王检讨资", "type": "person", "normalized": "王资（检讨）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "01-008", "text": "冯必政", "type": "person", "normalized": "冯必政", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-008", "text": "焦奉真", "type": "person", "normalized": "焦奉真", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-008", "text": "张文", "type": "person", "normalized": "张文", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "01-008", "text": "吏部", "type": "institution", "normalized": "吏部", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-008", "text": "包孝肃", "type": "person", "normalized": "包拯（包孝肃）", "confidence": 0.85, "source": "原文片段"},

    # ============ 01-009 京都贺礼/龙旗宝纛/太祖文集 ============
    {"item_id": "01-009", "text": "京都", "type": "place", "normalized": "京师", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-009", "text": "景泰", "type": "era", "normalized": "景泰（明代宗）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-009", "text": "鸿胪", "type": "institution", "normalized": "鸿胪寺", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-009", "text": "三千营", "type": "institution", "normalized": "三千营", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-009", "text": "都督", "type": "official", "normalized": "都督", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-009", "text": "张軏", "type": "person", "normalized": "张軏", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-009", "text": "杨俊", "type": "person", "normalized": "杨俊", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-009", "text": "都指挥", "type": "official", "normalized": "都指挥", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-009", "text": "王琦", "type": "person", "normalized": "王琦", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-009", "text": "季聦", "type": "person", "normalized": "季聪（季聦）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-009", "text": "太祖皇帝", "type": "person", "normalized": "明太祖（太祖皇帝朱元璋）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-009", "text": "刘伯温", "type": "person", "normalized": "刘基（刘伯温）", "confidence": 0.9, "source": "原文片段"},

    # ============ 01-010 三杨两王 ============
    {"item_id": "01-010", "text": "宣德", "type": "era", "normalized": "宣德（明宣宗）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-010", "text": "三杨", "type": "person", "normalized": "三杨（杨士奇/杨荣/杨溥）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-010", "text": "文贞", "type": "person", "normalized": "杨士奇（西杨文贞）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-010", "text": "文敏", "type": "person", "normalized": "杨荣（东杨文敏）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-010", "text": "文定", "type": "person", "normalized": "杨溥（南杨文定）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-010", "text": "抑庵", "type": "person", "normalized": "王英（抑庵，东王）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "01-010", "text": "泉坡", "type": "person", "normalized": "王直（泉坡，吏部尚书）", "confidence": 0.85, "source": "原文片段"},

    # ============ 01-011 盛奏官舍被谤 ============
    {"item_id": "01-011", "text": "盛", "type": "person", "normalized": "叶盛（作者，自称盛）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-011", "text": "京师", "type": "place", "normalized": "京师", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-011", "text": "给事中", "type": "official", "normalized": "给事中", "confidence": 0.9, "source": "原文片段"},

    # ============ 01-012 文华殿面谕迎复 ============
    {"item_id": "01-012", "text": "景泰", "type": "era", "normalized": "景泰（明代宗）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-012", "text": "礼部", "type": "institution", "normalized": "礼部", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-012", "text": "文华殿", "type": "place", "normalized": "文华殿", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-012", "text": "吏部", "type": "institution", "normalized": "吏部", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-012", "text": "王公", "type": "person", "normalized": "王直（泉坡，吏部尚书）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "01-012", "text": "于公", "type": "person", "normalized": "于谦（少保于公）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-012", "text": "兴安", "type": "person", "normalized": "兴安（太监）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-012", "text": "文天祥", "type": "person", "normalized": "文天祥", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-012", "text": "富弼", "type": "person", "normalized": "富弼", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-012", "text": "李实", "type": "person", "normalized": "李实（礼部侍郎）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-012", "text": "礼部侍郎", "type": "official", "normalized": "礼部侍郎", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-012", "text": "内閤", "type": "institution", "normalized": "内阁（内閤）", "confidence": 0.88, "source": "原文片段"},

    # ============ 01-013 沈简庵 ============
    {"item_id": "01-013", "text": "大理少卿", "type": "official", "normalized": "大理少卿", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-013", "text": "云间", "type": "place", "normalized": "云间（松江）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-013", "text": "沈简庵", "type": "person", "normalized": "沈简庵（云间，大理少卿）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-013", "text": "自乐学士", "type": "person", "normalized": "沈氏兄（号自乐，翰林学士）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "01-013", "text": "翰林", "type": "institution", "normalized": "翰林院（翰林）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-013", "text": "正统", "type": "era", "normalized": "正统（明英宗）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-013", "text": "直沽", "type": "place", "normalized": "直沽", "confidence": 0.88, "source": "原文片段"},

    # ============ 01-014 王绂 ============
    {"item_id": "01-014", "text": "毘陵", "type": "place", "normalized": "毘陵（毗陵）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-014", "text": "王绂", "type": "person", "normalized": "王绂（孟端）", "confidence": 0.95, "source": "原文片段"},
    {"item_id": "01-014", "text": "京师", "type": "place", "normalized": "京师", "confidence": 0.9, "source": "原文片段"},

    # ============ 01-015 迎复仪注之议 ============
    {"item_id": "01-015", "text": "居庸", "type": "place", "normalized": "居庸（居庸关）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-015", "text": "礼部", "type": "institution", "normalized": "礼部", "confidence": 0.93, "source": "原文片段"},
    {"item_id": "01-015", "text": "兵部", "type": "institution", "normalized": "兵部", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-015", "text": "都御史", "type": "official", "normalized": "都御史", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-015", "text": "王文", "type": "person", "normalized": "王文（都御史）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-015", "text": "于公", "type": "person", "normalized": "于谦（少保于公）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-015", "text": "胡公", "type": "person", "normalized": "胡公（毘陵胡公=礼部尚书胡濙，待 alias 映射）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "01-015", "text": "王公", "type": "person", "normalized": "王直（泉坡，吏部尚书）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "01-015", "text": "通政司", "type": "institution", "normalized": "通政司", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-015", "text": "大理寺", "type": "institution", "normalized": "大理寺", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-015", "text": "六科", "type": "institution", "normalized": "六科", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-015", "text": "邢让", "type": "person", "normalized": "邢让（翰林检讨）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-015", "text": "户科给事中", "type": "official", "normalized": "户科给事中", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-015", "text": "李侃", "type": "person", "normalized": "李侃", "confidence": 0.9, "source": "原文片段"},

    # ============ 01-016 六科先言劾杨俊 ============
    {"item_id": "01-016", "text": "六科", "type": "institution", "normalized": "六科", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-016", "text": "十三道", "type": "institution", "normalized": "十三道（监察御史）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "01-016", "text": "都督", "type": "official", "normalized": "都督", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-016", "text": "杨俊", "type": "person", "normalized": "杨俊", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-016", "text": "盛", "type": "person", "normalized": "叶盛（作者，自称盛）", "confidence": 0.92, "source": "原文片段"},
    {"item_id": "01-016", "text": "鸿胪", "type": "institution", "normalized": "鸿胪寺", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-016", "text": "左掖门", "type": "place", "normalized": "左掖门", "confidence": 0.95, "source": "原文片段"},

    # ============ 01-017 俞行之冯益 ============
    {"item_id": "01-017", "text": "永乐", "type": "era", "normalized": "永乐（明成祖）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-017", "text": "俞行之", "type": "person", "normalized": "俞行之", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-017", "text": "正统", "type": "era", "normalized": "正统（明英宗）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "01-017", "text": "冯益", "type": "person", "normalized": "冯益", "confidence": 0.9, "source": "原文片段"},
]
