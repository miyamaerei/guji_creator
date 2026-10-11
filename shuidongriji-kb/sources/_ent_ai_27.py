# -*- coding: utf-8 -*-
"""《水东日记》卷 27 —— L1 实体标注 源数据（AI 判定逐条填写）

覆盖条目：27-001~27-015（共 15 条）。
"""

ITEM_LIST = [
    "27-001 | 姚文公燧撰宋太常少卿陈希亮神道碑",
    "27-002 | 李杜诗虽齐名而器识夐不同",
    "27-003 | 今驸马都尉周景父前监察御史秦颙",
    "27-004 | 高昌王世勋碑",
    "27-005 | 冯昱御史濮州人",
    "27-006 | 景泰三年四月十日独石都督孙安奏墩军",
    "27-007 | 山西参议孙敬前兵科给事中",
    "27-008 | 国朝定制母止封两人",
    "27-009 | 故事朝官结衔皆有一定之序",
    "27-010 | 人性好恶偏忌",
    "27-011 | 今怀来城东南旧石桥遗址",
    "27-012 | 宣府儒学圣人土像",
    "27-013 | 国初孔庙城隍皆木主",
    "27-014 | 于节庵养子于康颇好聚图画",
    "27-015 | 史记所载如纣囚西伯于羑里",
]

DATA = [
    # ---- 27-001 姚燧撰陈希亮神道碑 ----
    {"id": "ENT-13501", "item_id": "27-001", "text": "姚燧", "type": "person", "start": 0, "end": 0, "normalized": "姚燧（谥文）", "confidence": 0.92, "source": "姚文公燧"},
    {"id": "ENT-13502", "item_id": "27-001", "text": "陈希亮", "type": "person", "start": 0, "end": 0, "normalized": "陈希亮（字公弼）", "confidence": 0.92, "source": "宋太常少卿陈希亮"},
    {"id": "ENT-13503", "item_id": "27-001", "text": "陈元凯", "type": "person", "start": 0, "end": 0, "normalized": "陈元凯", "confidence": 0.85, "source": "陈公元凯"},
    {"id": "ENT-13504", "item_id": "27-001", "text": "苏文忠公", "type": "person", "start": 0, "end": 0, "normalized": "苏轼（谥文忠）", "confidence": 0.92, "source": "苏文忠公尝为其父子作传"},
    {"id": "ENT-13505", "item_id": "27-001", "text": "青神", "type": "place", "start": 0, "end": 0, "normalized": "眉州青神", "confidence": 0.85, "source": "家眉之青神"},
    {"id": "ENT-13506", "item_id": "27-001", "text": "范镇", "type": "person", "start": 0, "end": 0, "normalized": "范镇", "confidence": 0.82, "source": "果得范公镇所撰志铭"},
    {"id": "ENT-13507", "item_id": "27-001", "text": "叶之先", "type": "person", "start": 0, "end": 0, "normalized": "叶氏先世", "confidence": 0.8, "source": "吾叶之先仅有传家数语"},
    {"id": "ENT-13508", "item_id": "27-001", "text": "夏玑", "type": "person", "start": 0, "end": 0, "normalized": "夏玑（德干）", "confidence": 0.82, "source": "吴友夏玑德干"},
    # ---- 27-002 李杜 ----
    {"id": "ENT-13509", "item_id": "27-002", "text": "子美", "type": "person", "start": 0, "end": 0, "normalized": "杜甫（字子美）", "confidence": 0.92, "source": "子美之言曰"},
    {"id": "ENT-13510", "item_id": "27-002", "text": "太白", "type": "person", "start": 0, "end": 0, "normalized": "李白（字太白）", "confidence": 0.92, "source": "若太白所谓"},
    # ---- 27-003 ----
    {"id": "ENT-13511", "item_id": "27-003", "text": "周景", "type": "person", "start": 0, "end": 0, "normalized": "周景（驸马都尉）", "confidence": 0.85, "source": "驸马都尉周景"},
    {"id": "ENT-13512", "item_id": "27-003", "text": "秦颙", "type": "person", "start": 0, "end": 0, "normalized": "秦颙", "confidence": 0.85, "source": "前监察御史秦颙"},
    {"id": "ENT-13513", "item_id": "27-003", "text": "耿恒庵", "type": "person", "start": 0, "end": 0, "normalized": "耿九畴（号恒庵）", "confidence": 0.82, "source": "耿恒庵尚书所荐士"},
    {"id": "ENT-13514", "item_id": "27-003", "text": "季聪", "type": "person", "start": 0, "end": 0, "normalized": "季聪（都御史）", "confidence": 0.82, "source": "季聪都宪"},
    {"id": "ENT-13515", "item_id": "27-003", "text": "李忠刚", "type": "person", "start": 0, "end": 0, "normalized": "李忠刚（华亭）", "confidence": 0.82, "source": "华亭李忠刚尚书"},
    {"id": "ENT-13516", "item_id": "27-003", "text": "虞拳", "type": "person", "start": 0, "end": 0, "normalized": "虞拳（吴江）", "confidence": 0.8, "source": "吴江虞拳言"},
    {"id": "ENT-13517", "item_id": "27-003", "text": "邵庵", "type": "person", "start": 0, "end": 0, "normalized": "邵庵（虞集号）", "confidence": 0.85, "source": "家有邵庵三像"},
    # ---- 27-004 高昌王碑 ----
    {"id": "ENT-13518", "item_id": "27-004", "text": "高昌王世勋碑", "type": "work", "start": 0, "end": 0, "normalized": "高昌王世勋碑", "confidence": 0.9, "source": "高昌王世勋碑"},
    {"id": "ENT-13519", "item_id": "27-004", "text": "虞公", "type": "person", "start": 0, "end": 0, "normalized": "虞集", "confidence": 0.88, "source": "雍虞公叙之"},
    {"id": "ENT-13520", "item_id": "27-004", "text": "特穆尔布哈", "type": "person", "start": 0, "end": 0, "normalized": "特穆尔布哈（帖木儿不花）", "confidence": 0.82, "source": "副在特穆尔布哈之五世孙"},
    {"id": "ENT-13521", "item_id": "27-004", "text": "宁", "type": "person", "start": 0, "end": 0, "normalized": "宁（宣府前卫指挥使）", "confidence": 0.82, "source": "指挥佥事宁家"},
    {"id": "ENT-13522", "item_id": "27-004", "text": "鲜于枢", "type": "person", "start": 0, "end": 0, "normalized": "鲜于枢", "confidence": 0.88, "source": "鲜于枢之甥"},
    {"id": "ENT-13523", "item_id": "27-004", "text": "宋国公", "type": "person", "start": 0, "end": 0, "normalized": "冯胜（封宋国公）", "confidence": 0.82, "source": "宋国公西征"},
    # ---- 27-005 冯昱 ----
    {"id": "ENT-13524", "item_id": "27-005", "text": "冯昱", "type": "person", "start": 0, "end": 0, "normalized": "冯昱（濮州人，御史）", "confidence": 0.85, "source": "冯昱御史濮州人"},
    # ---- 27-006 独石墩 ----
    {"id": "ENT-13525", "item_id": "27-006", "text": "孙安", "type": "person", "start": 0, "end": 0, "normalized": "孙安（独石都督）", "confidence": 0.85, "source": "独石都督孙安"},
    {"id": "ENT-13526", "item_id": "27-006", "text": "武安侯", "type": "person", "start": 0, "end": 0, "normalized": "郑亨（封武安侯）", "confidence": 0.85, "source": "总兵官武安侯"},
    {"id": "ENT-13527", "item_id": "27-006", "text": "独石", "type": "place", "start": 0, "end": 0, "normalized": "独石（边堡）", "confidence": 0.88, "source": "独石都督"},
    # ---- 27-007 孙敬 ----
    {"id": "ENT-13528", "item_id": "27-007", "text": "孙敬", "type": "person", "start": 0, "end": 0, "normalized": "孙敬（山西参议）", "confidence": 0.85, "source": "山西参议孙敬"},
    {"id": "ENT-13529", "item_id": "27-007", "text": "安远侯柳溥", "type": "person", "start": 0, "end": 0, "normalized": "柳溥（封安远侯）", "confidence": 0.82, "source": "劾安远侯柳溥"},
    # ---- 27-008 封母 ----
    {"id": "ENT-13530", "item_id": "27-008", "text": "曹文襄公", "type": "person", "start": 0, "end": 0, "normalized": "曹鼐（谥文襄）", "confidence": 0.85, "source": "曹文襄公陈情"},
    {"id": "ENT-13531", "item_id": "27-008", "text": "杨宁", "type": "person", "start": 0, "end": 0, "normalized": "杨宁", "confidence": 0.8, "source": "杨宁江渊薛希琏萧维祯"},
    {"id": "ENT-13532", "item_id": "27-008", "text": "江渊", "type": "person", "start": 0, "end": 0, "normalized": "江渊", "confidence": 0.82, "source": "江渊"},
    {"id": "ENT-13533", "item_id": "27-008", "text": "薛希琏", "type": "person", "start": 0, "end": 0, "normalized": "薛希琏", "confidence": 0.82, "source": "薛希琏"},
    {"id": "ENT-13534", "item_id": "27-008", "text": "萧维祯", "type": "person", "start": 0, "end": 0, "normalized": "萧维祯", "confidence": 0.82, "source": "萧维祯"},
    # ---- 27-009 结衔 ----
    {"id": "ENT-13535", "item_id": "27-009", "text": "文渊阁", "type": "institution", "start": 0, "end": 0, "normalized": "文渊阁", "confidence": 0.9, "source": "掌文渊阁事"},
    {"id": "ENT-13536", "item_id": "27-009", "text": "英国公", "type": "person", "start": 0, "end": 0, "normalized": "张辅（封英国公）", "confidence": 0.82, "source": "知经筵属英国"},
    # ---- 27-010 桂衡 ----
    {"id": "ENT-13537", "item_id": "27-010", "text": "石璞", "type": "person", "start": 0, "end": 0, "normalized": "石璞（太保）", "confidence": 0.85, "source": "石璞太保"},
    {"id": "ENT-13538", "item_id": "27-010", "text": "寇庄愍", "type": "person", "start": 0, "end": 0, "normalized": "寇深（谥庄愍）", "confidence": 0.85, "source": "寇庄愍左宪"},
    {"id": "ENT-13539", "item_id": "27-010", "text": "年尚书", "type": "person", "start": 0, "end": 0, "normalized": "年富（尚书）", "confidence": 0.85, "source": "年尚书富"},
    {"id": "ENT-13540", "item_id": "27-010", "text": "杨文贞公", "type": "person", "start": 0, "end": 0, "normalized": "杨士奇（谥文贞）", "confidence": 0.92, "source": "杨文贞公布衣"},
    {"id": "ENT-13541", "item_id": "27-010", "text": "桂衡", "type": "person", "start": 0, "end": 0, "normalized": "桂衡（字孟平，睦人）", "confidence": 0.85, "source": "睦人桂衡孟平"},
    {"id": "ENT-13542", "item_id": "27-010", "text": "钱塘儒学", "type": "institution", "start": 0, "end": 0, "normalized": "钱塘儒学", "confidence": 0.85, "source": "钱塘儒学修业斋训导"},
    {"id": "ENT-13543", "item_id": "27-010", "text": "张升", "type": "person", "start": 0, "end": 0, "normalized": "张升（万全训导）", "confidence": 0.8, "source": "命万全训导张升选"},
    # ---- 27-011 怀来 ----
    {"id": "ENT-13544", "item_id": "27-011", "text": "怀来城", "type": "place", "start": 0, "end": 0, "normalized": "怀来城", "confidence": 0.88, "source": "今怀来城东南"},
    {"id": "ENT-13545", "item_id": "27-011", "text": "文皇帝", "type": "person", "start": 0, "end": 0, "normalized": "明成祖朱棣", "confidence": 0.9, "source": "洪武中文皇帝兵北出"},
    # ---- 27-012 宣府儒学 ----
    {"id": "ENT-13546", "item_id": "27-012", "text": "宣府儒学", "type": "institution", "start": 0, "end": 0, "normalized": "宣府儒学", "confidence": 0.88, "source": "宣府儒学圣人土像"},
    {"id": "ENT-13547", "item_id": "27-012", "text": "谭总戎", "type": "person", "start": 0, "end": 0, "normalized": "谭广（总戎）", "confidence": 0.82, "source": "初谭总戎以银帛作心脏"},
    # ---- 27-013 孔庙 ----
    {"id": "ENT-13548", "item_id": "27-013", "text": "孔庙", "type": "institution", "start": 0, "end": 0, "normalized": "孔庙", "confidence": 0.9, "source": "国初孔庙城隍皆木主"},
    {"id": "ENT-13549", "item_id": "27-013", "text": "王公", "type": "person", "start": 0, "end": 0, "normalized": "王翱（太子太保左都御史）", "confidence": 0.82, "source": "今冢宰王公易塑像"},
    # ---- 27-014 于节庵 ----
    {"id": "ENT-13550", "item_id": "27-014", "text": "于节庵", "type": "person", "start": 0, "end": 0, "normalized": "于谦（号节庵）", "confidence": 0.95, "source": "于节庵养子于康"},
    {"id": "ENT-13551", "item_id": "27-014", "text": "于康", "type": "person", "start": 0, "end": 0, "normalized": "于康（于谦养子）", "confidence": 0.85, "source": "于节庵养子于康"},
    {"id": "ENT-13552", "item_id": "27-014", "text": "卢永", "type": "person", "start": 0, "end": 0, "normalized": "卢永（太监）", "confidence": 0.82, "source": "太监卢永后被宥免"},
    # ---- 27-015 史记 ----
    {"id": "ENT-13553", "item_id": "27-015", "text": "史记", "type": "work", "start": 0, "end": 0, "normalized": "史记", "confidence": 0.92, "source": "史记所载"},
    {"id": "ENT-13554", "item_id": "27-015", "text": "西伯", "type": "person", "start": 0, "end": 0, "normalized": "周文王（西伯）", "confidence": 0.85, "source": "纣囚西伯于羑里"},
    {"id": "ENT-13555", "item_id": "27-015", "text": "史迁", "type": "person", "start": 0, "end": 0, "normalized": "司马迁", "confidence": 0.9, "source": "此史迁之所以为史迁"},
]
# 缺口登记：27-010 桂衡诗多首已作文献标注；诗中王惟中、孙性初等不另建。
