# -*- coding: utf-8 -*-
"""《水东日记》卷 04 —— L1 实体标注 源数据（AI 判定逐条填写）

说明：实体标注：每条记录标注该条目中的实体（text=原文字面，type=实体类型，normalized=归一词形，confidence=置信度）

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：person=人物 / official=职官名 / institution=机构衙门 / place=地名 / era=年号朝代 / posthumous=谥号 / work=书名文献名 / unknown=类型待定
  * 未建模条目在下方注释中如实单列，不强行编造

填写方式：把 DATA 中的示例记录替换为本卷实际判定结果；
         每条记录为一个 dict；未判定条目保留注释占位。
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "04-001 | 正统四年廷试榜出华亭钱溥原溥仿宋人王十李三之诗自诵曰举头暂且",
    "04-002 | 长洲民杨芳景泰中尝以十事上巡抚邹都御史其均税额以为古昔井田养",
    "04-003 | 刘洗马定之朝遇王伟兵侍王戏之曰吾太仆马多洗马须一一洗之刘应声",
    "04-004 | 余姚陈惟寅先生教谕昆山颇喜谈风鉴尝曰举子梁昱当甲科瞿泰安不失",
    "04-005 | 临安钱宰子予武肃王之裔元末老儒也高庙礼徴同诸儒修纂尚书会选孟",
    "04-006 | 国子祭酒四明陈先生遇僚属诸生极严有怀忿而讼之者法司将覆请就逮",
    "04-007 | 王抑庵先生典选遇不如意事好诵古人诗以自寛一日有新得给事中即欲",
    "04-008 | 范啓东闻之前辈云士大夫游艺必审轻重且当先有迹者谓学文胜学诗学",
    "04-009 | 欧阳文忠公平生聚观金石刻动数百卷题识真迹甚多尝自言平生喜学书",
    "04-010 | 杨武襄洪为人虽尚权谲然有威严将士知畏之此其所长不可掩者亦赖朝",
    "04-011 | 景泰元年春久旱两京灾异亦迭见偶会礼科都给事中李实吏科给事中毛",
    "04-012 | 予为举子时闻同举者云国朝状元多不能至金带时陈泰和马临朐曹恒山",
    "04-013 | 今人燕客杯酌劝尽饮曰千歳南北士人多亦然但莫知其字义意者为请嗺",
    "04-014 | 鲜于困学圹志赵文敏公书小楷精絶篆笔出石鼓文少师庐陵杨公得之吴",
    "04-015 | 尚书吕震前左都御史刘观皆洪武中人物熟知政事故实故廷论之际每下",
    "04-016 | 宋黄震东发尝采董槐丞相之说以大学经文知止而后有定至则近道矣两",
    "04-017 | 先舅氏野水周先生念先外祖之无后有歳时祭甚盛德也而吾友进士郑时",
    "04-018 | 方言语音暗合古韵者多今山西人以去为库闽人以口为苦走为祖是也吾",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
# 示例记录（保留作格式对照）：
# {"item_id": "01-001", "text": "礼部尚书", "type": "official", "normalized": "礼部尚书", "confidence": 0.97, "source": "原文片段"}

DATA = [
    # 04-001 廷试榜
    {"item_id": "04-001", "text": "正统四年", "type": "era", "normalized": "正统四年", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "04-001", "text": "华亭钱溥", "type": "person", "normalized": "钱溥（字原溥，华亭）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-001", "text": "昆山张穆", "type": "person", "normalized": "张穆（字敬之，昆山）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-001", "text": "昆山张和", "type": "person", "normalized": "张和（字节之，昆山，张穆母兄）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-001", "text": "陈少卿", "type": "person", "normalized": "陈少卿（名待考）", "confidence": 0.72, "source": "原文片段"},
    {"item_id": "04-001", "text": "华亭", "type": "place", "normalized": "华亭", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-001", "text": "昆山", "type": "place", "normalized": "昆山", "confidence": 0.85, "source": "原文片段"},
    # 04-002 均税额
    {"item_id": "04-002", "text": "长洲民杨芳", "type": "person", "normalized": "杨芳（长洲民）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-002", "text": "景泰", "type": "era", "normalized": "景泰（明代宗年号）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "04-002", "text": "巡抚邹都御史", "type": "person", "normalized": "邹都御史（巡抚）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "04-002", "text": "巡抚", "type": "official", "normalized": "巡抚", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-002", "text": "王方贽", "type": "person", "normalized": "王方贽（宋，均两浙田）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "04-002", "text": "耶律楚材", "type": "person", "normalized": "耶律楚材（元）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-002", "text": "苏松", "type": "place", "normalized": "苏松（苏州松江）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-002", "text": "长洲", "type": "place", "normalized": "长洲", "confidence": 0.85, "source": "原文片段"},
    # 04-003 刘洗马戏对
    {"item_id": "04-003", "text": "刘洗马定之", "type": "person", "normalized": "刘定之（洗马）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-003", "text": "王伟兵侍", "type": "person", "normalized": "王伟（兵部侍郎）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-003", "text": "洗马", "type": "official", "normalized": "洗马（东宫官）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-003", "text": "太仆", "type": "institution", "normalized": "太仆寺", "confidence": 0.82, "source": "原文片段"},
    # 04-004 陈惟寅风鉴
    {"item_id": "04-004", "text": "余姚陈惟寅", "type": "person", "normalized": "陈惟寅（余姚，教谕昆山）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-004", "text": "教谕", "type": "official", "normalized": "教谕", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-004", "text": "梁昱", "type": "person", "normalized": "梁昱（举子）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "04-004", "text": "瞿泰安", "type": "person", "normalized": "瞿泰安", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "04-004", "text": "岳正", "type": "person", "normalized": "岳正", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-004", "text": "陈鉴", "type": "person", "normalized": "陈鉴", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "04-004", "text": "萧祭酒", "type": "person", "normalized": "萧祭酒（名待考）", "confidence": 0.72, "source": "原文片段"},
    {"item_id": "04-004", "text": "平定知州", "type": "official", "normalized": "平定知州", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "04-004", "text": "刑部郎中", "type": "official", "normalized": "刑部郎中", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "04-004", "text": "余姚", "type": "place", "normalized": "余姚", "confidence": 0.82, "source": "原文片段"},
    # 04-005 钱宰
    {"item_id": "04-005", "text": "临安钱宰子予", "type": "person", "normalized": "钱宰（字子予，临安）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-005", "text": "武肃王", "type": "person", "normalized": "钱镠（武肃王）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-005", "text": "高庙", "type": "person", "normalized": "朱元璋（明太祖）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-005", "text": "孟子节文", "type": "work", "normalized": "孟子节文", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-005", "text": "文华", "type": "place", "normalized": "文华殿", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-005", "text": "国子博士", "type": "official", "normalized": "国子博士", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-005", "text": "会稽", "type": "place", "normalized": "会稽", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-005", "text": "铁券", "type": "work", "normalized": "吴越国铁券", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "04-005", "text": "宋宣和", "type": "era", "normalized": "宣和（宋徽宗年号）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-005", "text": "唐昭宗", "type": "person", "normalized": "唐昭宗", "confidence": 0.8, "source": "原文片段"},
    # 04-006 陈祭酒纯臣
    {"item_id": "04-006", "text": "四明陈先生", "type": "person", "normalized": "陈祭酒（四明人）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "04-006", "text": "国子祭酒", "type": "official", "normalized": "国子祭酒", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-006", "text": "周文襄公", "type": "person", "normalized": "周忱（谥文襄公）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-006", "text": "法司", "type": "institution", "normalized": "法司（三法司）", "confidence": 0.82, "source": "原文片段"},
    # 04-007 王抑庵/卢熊
    {"item_id": "04-007", "text": "王抑庵", "type": "person", "normalized": "王抑庵（典选，名待考）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "04-007", "text": "给事中", "type": "official", "normalized": "给事中", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-007", "text": "昆山卢熊字公武", "type": "person", "normalized": "卢熊（字公武，昆山）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-007", "text": "洪武", "type": "era", "normalized": "洪武（明太祖年号）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "04-007", "text": "兖州知州", "type": "official", "normalized": "兖州知州", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-007", "text": "卢熈字公暨", "type": "person", "normalized": "卢熈（字公暨，卢熊弟）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "04-007", "text": "睢州同知", "type": "official", "normalized": "睢州同知", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "04-007", "text": "中书舍人", "type": "official", "normalized": "中书舍人", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-007", "text": "昆山", "type": "place", "normalized": "昆山", "confidence": 0.85, "source": "原文片段"},
    # 04-008 范启东论游艺
    {"item_id": "04-008", "text": "范启东", "type": "person", "normalized": "范启东", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-008", "text": "范苇斋", "type": "person", "normalized": "范苇斋（范启东）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "04-008", "text": "馆阁", "type": "institution", "normalized": "馆阁（内阁翰林）", "confidence": 0.82, "source": "原文片段"},
    # 04-009 欧阳文忠/东坡/聂大年
    {"item_id": "04-009", "text": "欧阳文忠公", "type": "person", "normalized": "欧阳修（谥文忠）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "04-009", "text": "东坡居士", "type": "person", "normalized": "苏轼（号东坡）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "04-009", "text": "聂大年", "type": "person", "normalized": "聂大年", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-009", "text": "袁衷", "type": "person", "normalized": "袁衷（主事）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "04-009", "text": "王翰林", "type": "person", "normalized": "王翰林（名待考）", "confidence": 0.72, "source": "原文片段"},
    {"item_id": "04-009", "text": "张篠庵", "type": "person", "normalized": "张篠庵（叶盛友）", "confidence": 0.75, "source": "原文片段"},
    # 04-010 杨武襄洪
    {"item_id": "04-010", "text": "杨武襄洪", "type": "person", "normalized": "杨洪（谥武襄）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "04-010", "text": "宣德", "type": "era", "normalized": "宣德（明宣宗年号）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-010", "text": "正统", "type": "era", "normalized": "正统（明英宗年号）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-010", "text": "庐陵杨公", "type": "person", "normalized": "杨士奇（庐陵，阁老）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-010", "text": "杜衡", "type": "person", "normalized": "杜衡（指挥）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "04-010", "text": "魏尚书源", "type": "person", "normalized": "魏源（尚书）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-010", "text": "李友全", "type": "person", "normalized": "李友全（部卒）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "04-010", "text": "郭进", "type": "person", "normalized": "郭进（宋太祖时将）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "04-010", "text": "张英", "type": "person", "normalized": "张英（大同指挥）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "04-010", "text": "石公", "type": "person", "normalized": "石公（总戎）", "confidence": 0.72, "source": "原文片段"},
    {"item_id": "04-010", "text": "张宣", "type": "person", "normalized": "张宣（蔚州千户）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "04-010", "text": "刘侍郎琏", "type": "person", "normalized": "刘琏（侍郎）", "confidence": 0.78, "source": "原文片段"},
    # 04-011 久旱台谏言事（长条目）
    {"item_id": "04-011", "text": "景泰元年", "type": "era", "normalized": "景泰元年", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "04-011", "text": "两京", "type": "place", "normalized": "两京（北京南京）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-011", "text": "李实", "type": "person", "normalized": "李实（礼科都给事中）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-011", "text": "毛玉", "type": "person", "normalized": "毛玉（吏科给事中）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-011", "text": "陈叔绍", "type": "person", "normalized": "陈叔绍（御史）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "04-011", "text": "罗箎", "type": "person", "normalized": "罗箎（御史）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "04-011", "text": "盛", "type": "person", "normalized": "叶盛（盛）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "04-011", "text": "金尚书", "type": "person", "normalized": "金尚书（名待考）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "04-011", "text": "于谦", "type": "person", "normalized": "于谦（兵部尚书）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "04-011", "text": "周叙", "type": "person", "normalized": "周叙（南京学士）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "04-011", "text": "陈镒", "type": "person", "normalized": "陈镒（左都御史）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-011", "text": "马显", "type": "person", "normalized": "马显（户科都给事中）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-011", "text": "胡公", "type": "person", "normalized": "胡濙（礼部）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-011", "text": "俞士悦", "type": "person", "normalized": "俞士悦（刑部尚书）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-011", "text": "锦衣卫", "type": "institution", "normalized": "锦衣卫", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "04-011", "text": "六科", "type": "institution", "normalized": "六科", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "04-011", "text": "六部", "type": "institution", "normalized": "六部", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-011", "text": "大理寺", "type": "institution", "normalized": "大理寺", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-011", "text": "通政司", "type": "institution", "normalized": "通政司", "confidence": 0.85, "source": "原文片段"},
    # 04-012 状元金带
    {"item_id": "04-012", "text": "陈泰和", "type": "person", "normalized": "陈循（泰和，状元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-012", "text": "马临朐", "type": "person", "normalized": "马愉（临朐，状元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-012", "text": "曹恒山", "type": "person", "normalized": "曹鼐（恒山，状元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-012", "text": "商同年", "type": "person", "normalized": "商辂（状元）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-012", "text": "彭纯道", "type": "person", "normalized": "彭纯道（状元）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "04-012", "text": "己巳", "type": "era", "normalized": "己巳（正统十四年）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-012", "text": "太常少卿", "type": "official", "normalized": "太常少卿", "confidence": 0.8, "source": "原文片段"},
    # 04-013 千岁劝饮
    {"item_id": "04-013", "text": "嗺酒", "type": "unknown", "normalized": "嗺酒（唐人劝饮语）", "confidence": 0.72, "source": "原文片段"},
    # 04-014 鲜于困学圹志
    {"item_id": "04-014", "text": "鲜于困学", "type": "person", "normalized": "鲜于枢（号困学）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-014", "text": "赵文敏公", "type": "person", "normalized": "赵孟頫（谥文敏）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "04-014", "text": "石鼓文", "type": "work", "normalized": "石鼓文", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-014", "text": "庐陵杨公", "type": "person", "normalized": "杨士奇（少师，庐陵）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-014", "text": "陈士谦", "type": "person", "normalized": "陈士谦（武昌，藏家）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "04-014", "text": "虞文靖公", "type": "person", "normalized": "虞集（谥文靖）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-014", "text": "刘廷美", "type": "person", "normalized": "刘廷美（上舍）", "confidence": 0.75, "source": "原文片段"},
    # 04-015 吕震刘观/土官
    {"item_id": "04-015", "text": "吕震", "type": "person", "normalized": "吕震（尚书）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-015", "text": "刘观", "type": "person", "normalized": "刘观（左都御史）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-015", "text": "左都御史", "type": "official", "normalized": "左都御史", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-015", "text": "王文", "type": "person", "normalized": "王文（都御史）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-015", "text": "萧都御史", "type": "person", "normalized": "萧都御史（名待考）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "04-015", "text": "诸司职掌", "type": "work", "normalized": "诸司职掌", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-015", "text": "湖广", "type": "place", "normalized": "湖广", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-015", "text": "四川", "type": "place", "normalized": "四川", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-015", "text": "云南", "type": "place", "normalized": "云南", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-015", "text": "广西", "type": "place", "normalized": "广西", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-015", "text": "天顺", "type": "era", "normalized": "天顺（明英宗年号）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-015", "text": "邓錤", "type": "person", "normalized": "邓錤（重庆民）", "confidence": 0.78, "source": "原文片段"},
    {"item_id": "04-015", "text": "魏相", "type": "person", "normalized": "魏相（汉名相）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "04-015", "text": "重庆", "type": "place", "normalized": "重庆", "confidence": 0.82, "source": "原文片段"},
    # 04-016 大学格物传
    {"item_id": "04-016", "text": "黄震东发", "type": "person", "normalized": "黄震（字东发，宋）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-016", "text": "董槐", "type": "person", "normalized": "董槐（宋丞相）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "04-016", "text": "王巽卿", "type": "person", "normalized": "王巽卿（名柏？）", "confidence": 0.72, "source": "原文片段"},
    {"item_id": "04-016", "text": "草庐吴先生", "type": "person", "normalized": "吴澄（号草庐）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-016", "text": "大学", "type": "work", "normalized": "大学", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-016", "text": "袁明善", "type": "person", "normalized": "袁明善（吴澄门人）", "confidence": 0.75, "source": "原文片段"},
    # 04-017 野水周先生/外氏
    {"item_id": "04-017", "text": "野水周先生", "type": "person", "normalized": "周某（号野水，叶盛舅氏）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "04-017", "text": "郑时", "type": "person", "normalized": "郑时（进士，叶盛友）", "confidence": 0.8, "source": "原文片段"},
    {"item_id": "04-017", "text": "薛氏", "type": "person", "normalized": "薛氏（医世）", "confidence": 0.75, "source": "原文片段"},
    {"item_id": "04-017", "text": "晦翁", "type": "person", "normalized": "朱熹（号晦翁）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-017", "text": "汪尚书", "type": "person", "normalized": "汪尚书（名待考）", "confidence": 0.72, "source": "原文片段"},
    # 04-018 方言古韵
    {"item_id": "04-018", "text": "山西", "type": "place", "normalized": "山西", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-018", "text": "闽", "type": "place", "normalized": "闽（福建）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "04-018", "text": "昆山", "type": "place", "normalized": "昆山", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "04-018", "text": "吴淞江南", "type": "place", "normalized": "吴淞江南", "confidence": 0.8, "source": "原文片段"},
]
