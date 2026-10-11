# -*- coding: utf-8 -*-
"""《水东日记》卷 04 —— REL 人物关系 源数据（AI 判定逐条填写）

说明：关系记录：person_a/person_b(含各自 ent_ids)/relation_type/direction(单向/双向/未明)/evidence；只建文本有直接证据的关系，宁缺毋滥

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：同僚=同衙门共事 / 师生=师生授受 / 姻亲=婚姻亲属 / 同乡=同籍贯乡里 / 同科=同科进士/同学 / 举荐=举荐保任 / 弹劾=弹劾参奏 / 恩怨=恩怨嫌隙 / 上下级=隶属统辖 / 父子亲属=直系血亲 / 敌对=敌对冲突 / 其他=其他
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

# 字段键（打包器校验用）：rel_id, item_id, person_a, person_b, relation_type, direction, evidence, confidence
# 示例记录（保留作格式对照）：
# {"rel_id": "REL-001", "item_id": "01-004", "person_a": {"text": "姚铣", "person_a_ent_ids": ["ENT-xxx"]}, "person_b": {"text": "汪澄", "person_b_ent_ids": ["ENT-xxx"]}, "relation_type": "弹劾", "direction": "单向", "evidence": "兵科给事中姚铣等以为澄畏避且忌嫉当言之", "confidence": 0.9}

DATA = [
    # 04-001 张和张穆母兄
    {"rel_id": "REL-2001", "item_id": "04-001",
     "person_a": {"text": "张和（字节之）", "person_a_ent_ids": []},
     "person_b": {"text": "张穆（字敬之）", "person_b_ent_ids": []},
     "relation_type": "父子亲属", "direction": "双向",
     "evidence": "廷试第二甲昆山张和节之第一溥第二而和则穆之母兄也",
     "confidence": 0.8},
    # 04-004 陈惟寅同考取士
    {"rel_id": "REL-2002", "item_id": "04-004",
     "person_a": {"text": "陈惟寅（同考官）", "person_a_ent_ids": []},
     "person_b": {"text": "瞿泰安（本房）", "person_b_ent_ids": []},
     "relation_type": "师生", "direction": "单向",
     "evidence": "未几部檄先生会试同考……先生本房也比揭晓泰安名在第五",
     "confidence": 0.82},
    # 04-006 陈祭酒周忱同年
    {"rel_id": "REL-2003", "item_id": "04-006",
     "person_a": {"text": "陈祭酒（四明）", "person_a_ent_ids": []},
     "person_b": {"text": "周忱（文襄公）", "person_b_ent_ids": []},
     "relation_type": "同科", "direction": "双向",
     "evidence": "法司将覆请就逮周文襄公其同年谓先生当具疏申雪",
     "confidence": 0.82},
    # 04-007 卢熊卢熈兄弟
    {"rel_id": "REL-2004", "item_id": "04-007",
     "person_a": {"text": "卢熊（字公武）", "person_a_ent_ids": []},
     "person_b": {"text": "卢熈（字公暨，弟）", "person_b_ent_ids": []},
     "relation_type": "父子亲属", "direction": "双向",
     "evidence": "弟熈字公暨睢州同知有贤名公武寄以诗",
     "confidence": 0.85},
    # 04-010 杨洪杜衡恩怨
    {"rel_id": "REL-2005", "item_id": "04-010",
     "person_a": {"text": "杨洪", "person_a_ent_ids": []},
     "person_b": {"text": "杜衡（指挥）", "person_b_ent_ids": []},
     "relation_type": "恩怨", "direction": "单向",
     "evidence": "初为指挥杜衡所诬以魏尚书源覆辨而衡贬广西",
     "confidence": 0.82},
    # 04-010 杨洪受知于杨士奇
    {"rel_id": "REL-2006", "item_id": "04-010",
     "person_a": {"text": "杨洪", "person_a_ent_ids": []},
     "person_b": {"text": "杨士奇（庐陵阁老）", "person_b_ent_ids": []},
     "relation_type": "举荐", "direction": "双向",
     "evidence": "盖自宣德正统来已受知于阁中庐陵杨公辈皆爱重之",
     "confidence": 0.8},
    # 04-011 叶盛与李实毛玉同列
    {"rel_id": "REL-2007", "item_id": "04-011",
     "person_a": {"text": "叶盛（盛）", "person_a_ent_ids": []},
     "person_b": {"text": "李实、毛玉（科道同列）", "person_b_ent_ids": []},
     "relation_type": "同僚", "direction": "双向",
     "evidence": "偶会礼科都给事中李实吏科给事中毛玉御史陈叔绍罗箎相与惋叹盛因曰",
     "confidence": 0.85},
    # 04-011 叶盛与于谦
    {"rel_id": "REL-2008", "item_id": "04-011",
     "person_a": {"text": "叶盛", "person_a_ent_ids": []},
     "person_b": {"text": "于谦（兵部尚书）", "person_b_ent_ids": []},
     "relation_type": "上下级", "direction": "单向",
     "evidence": "一日兵部尚书于公谦谓盛言中官事言之有名矣",
     "confidence": 0.82},
    # 04-015 吕震刘观同僚
    {"rel_id": "REL-2009", "item_id": "04-015",
     "person_a": {"text": "吕震（尚书）", "person_a_ent_ids": []},
     "person_b": {"text": "刘观（左都御史）", "person_b_ent_ids": []},
     "relation_type": "同僚", "direction": "双向",
     "evidence": "尚书吕震前左都御史刘观皆洪武中人物熟知政事故实",
     "confidence": 0.82},
]
