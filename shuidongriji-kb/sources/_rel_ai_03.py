# -*- coding: utf-8 -*-
"""《水东日记》卷 03 —— REL 人物关系 源数据（AI 判定逐条填写）

说明：关系记录：person_a/person_b(含各自 ent_ids)/relation_type/direction(单向/双向/未明)/evidence；只建文本有直接证据的关系，宁缺毋滥

字段说明：
  * 只写条号 + 解读字段，不手抄原文（original 由打包器从指纹库注入）
  * 枚举（封闭+兜底）：同僚=同衙门共事 / 师生=师生授受 / 姻亲=婚姻亲属 / 同乡=同籍贯乡里 / 同科=同科进士/同学 / 举荐=举荐保任 / 弹劾=弹劾参奏 / 恩怨=恩怨嫌隙 / 上下级=隶属统辖 / 父子亲属=直系血亲 / 敌对=敌对冲突 / 其他=其他
  * 未建模条目在下方注释中如实单列，不强行编造

填写方式：把 DATA 中的示例记录替换为本卷实际判定结果；
         每条记录为一个 dict；未判定条目保留注释占位。
"""

ITEM_LIST = [  # 本卷条目清单（条号 | 原文首 30 字，供对照）
    "03-001 | 詹孟举篆书唐人早朝诗四纸孙叔英得之谈以宗家用笔絶泰不华王贞",
    "03-002 | 松江曹云西善诗画家富盛极一时其孙幼交号雪林客授孙至德家言乃祖",
    "03-003 | 正统十年进士登科録凡天字皆作防云出内阁意景泰中幸太学谢表内阁",
    "03-004 | 袁子英晚年惟一子生申为县吏坐累并子英徙南京以卒詹孟举挽诗曰吴",
    "03-005 | 萧墅张汉杰伯庸父子一时豪俊与赵屯吴氏有姻防张吴皆元万户府官吴",
    "03-006 | 钱知府昕初习举子业从节之游其外祖吴思庵先生作小诗遗之曰阿昕近",
    "03-007 | 甚矣富贵权宠之能动人也王子明冦平仲皆伟然一代人豪然天书之谬一",
    "03-008 | 至讷无言福严寺僧善词翰所交皆一代名人赵松雪冯海粟柯丹丘郑尚左",
    "03-009 | 福严寺老僧景燮颇能诗先人极与相好尝中夜对饮时予八九嵗侍几傍僧",
    "03-010 | 杨文定公最善王检讨振张修譔益相见辄出所作就二人评有所改易即乐",
    "03-011 | 张仲珪先生家藏风雨归牧图杨廉夫题曰牧牛值风雨箬笠几去手不在风",
    "03-012 | 夏忠靖公使吴中馆于文正书院之偏室夜三鼓适范氏子孙有事于中堂公",
    "03-013 | 尝过光福叶子昌家阅其谱壻陈瓘宗人梦其皆有序所録宋金紫棐恭公墓",
    "03-014 | 邓尉山中峯东北向居人相传地名黄坟盖宋刑部尚书黄状元由墓也赠工",
    "03-015 | 训导吾豫景泰中膺荐至京以屡言边事兵部奏宜边用而在边久不得支俸",
    "03-016 | 庄伯和碛澳名医好诙谐一日李无易遣家僮持简诣伯和家僮误举伯和姓",
    "03-017 | 【阙】　　　　　　　　　旧驿连新驿前山接后山我心无愧怍天道有",
    "03-018 | 山隂花溪蒋贵达老先生显司训昆庠质实敢言一日郡守况侯钟行部侯严",
    "03-019 | 庄瑾字公瑾号采芝龙江章氏之后晚居李墟能诗善草书学二王而硬徤骨",
    "03-020 | 松江李墟沈梦萱先生资深永乐中举略通书史吏部试招抚四裔榜纳卷独",
    "03-021 | 朱文公答巩仲至曰用韵多所未晓古韵虽有此例然在今日却恐不无讹谬",
    "03-022 | 予在邑庠时庠友吴芳廷实家畦菜得故冢志石见题云高平郁氏之墓政和",
    "03-023 | 定襄伯郭登治大同廉而尚谋有古良将风一日敌兵迫城下人心汹汹自登",
    "03-024 | 余尚书茂本熂父尝为镊工茂本既贵毎造谢隣曲不遇辄曰烦为道余待诏",
    "03-025 | 范啓东言长公于书独重云间沈度于画最爱永嘉郭文通以度书丰温润",
    "03-026 | 霹于边墩高处歳恒有之震死者或不闻其人其击屋柱桅竿之常见其",
    "03-027 | 中贵有再造营火者珍珠皆灰化玉器窑器或裂或变浅黑色惟诸色鸦鹘石",
    "03-028 | 尝见胡毘陵应酬诗文藁皆片纸满书闻其虽破纸少许见辄用补窻罅不弃",
    "03-029 | 文章家误用古人爵谥文意字义近世虽名人不免熊敬方胡祭酒皆以程明",
]

# 字段键（打包器校验用）：rel_id, item_id, person_a, person_b, relation_type, direction, evidence, confidence
# 示例记录（保留作格式对照）：
# {"rel_id": "REL-001", "item_id": "01-004", "person_a": {"text": "姚铣", "person_a_ent_ids": ["ENT-xxx"]}, "person_b": {"text": "汪澄", "person_b_ent_ids": ["ENT-xxx"]}, "relation_type": "弹劾", "direction": "单向", "evidence": "兵科给事中姚铣等以为澄畏避且忌嫉当言之", "confidence": 0.9}

DATA = [
    # 03-005 张汉杰父子
    {"rel_id": "REL-1501", "item_id": "03-005",
     "person_a": {"text": "张汉杰", "person_a_ent_ids": []},
     "person_b": {"text": "张伯庸（父）", "person_b_ent_ids": []},
     "relation_type": "父子亲属", "direction": "双向",
     "evidence": "萧墅张汉杰伯庸父子一时豪俊",
     "confidence": 0.85},
    # 03-005 张吴姻亲
    {"rel_id": "REL-1502", "item_id": "03-005",
     "person_a": {"text": "张汉杰", "person_a_ent_ids": []},
     "person_b": {"text": "赵屯吴氏", "person_b_ent_ids": []},
     "relation_type": "姻亲", "direction": "双向",
     "evidence": "与赵屯吴氏有姻（婚）",
     "confidence": 0.8},
    # 03-005 张汉杰拒钱皋
    {"rel_id": "REL-1503", "item_id": "03-005",
     "person_a": {"text": "张汉杰", "person_a_ent_ids": []},
     "person_b": {"text": "钱皋", "person_b_ent_ids": []},
     "relation_type": "敌对", "direction": "单向",
     "evidence": "毅然曰此叛贼也吾从汝叛耶大书叛贼二字黏诸所遣人之背",
     "confidence": 0.85},
    # 03-006 钱昕-吴思庵外祖
    {"rel_id": "REL-1504", "item_id": "03-006",
     "person_a": {"text": "钱昕", "person_a_ent_ids": []},
     "person_b": {"text": "吴思庵（外祖）", "person_b_ent_ids": []},
     "relation_type": "姻亲", "direction": "双向",
     "evidence": "其外祖吴思庵先生作小诗遗之",
     "confidence": 0.85},
    # 03-006 钱昕-节之师从
    {"rel_id": "REL-1505", "item_id": "03-006",
     "person_a": {"text": "钱昕", "person_a_ent_ids": []},
     "person_b": {"text": "节之（师）", "person_b_ent_ids": []},
     "relation_type": "师生", "direction": "单向",
     "evidence": "初习举子业从节之游",
     "confidence": 0.8},
    # 03-009 景燮-宗潮乡里并推
    {"rel_id": "REL-1506", "item_id": "03-009",
     "person_a": {"text": "景燮", "person_a_ent_ids": []},
     "person_b": {"text": "宗潮", "person_b_ent_ids": []},
     "relation_type": "同僚", "direction": "双向",
     "evidence": "二僧为一时乡里所推先人尝云潮外而燮内",
     "confidence": 0.78},
    # 03-010 杨文定公-王张友善
    {"rel_id": "REL-1507", "item_id": "03-010",
     "person_a": {"text": "杨文定公（杨溥）", "person_a_ent_ids": []},
     "person_b": {"text": "王振（检讨）、张益（修撰）", "person_b_ent_ids": []},
     "relation_type": "同僚", "direction": "双向",
     "evidence": "杨文定公最善王检讨振张修撰益相见辄出所作就二人评",
     "confidence": 0.82},
    # 03-010 曹文襄讥马状元
    {"rel_id": "REL-1508", "item_id": "03-010",
     "person_a": {"text": "曹文襄", "person_a_ent_ids": []},
     "person_b": {"text": "马状元", "person_b_ent_ids": []},
     "relation_type": "恩怨", "direction": "单向",
     "evidence": "马状元尚书措词颇澁每为文襄所讥切",
     "confidence": 0.78},
    # 03-012 杨东里-杨仲举
    {"rel_id": "REL-1509", "item_id": "03-012",
     "person_a": {"text": "杨东里少师（杨士奇）", "person_a_ent_ids": []},
     "person_b": {"text": "杨仲举（杨翥）", "person_b_ent_ids": []},
     "relation_type": "同僚", "direction": "双向",
     "evidence": "戒儿曹亟治具邀杨仲举先生过饮曰门户初辟必一君子先行",
     "confidence": 0.82},
    # 03-015 吾豫-项侍郎
    {"rel_id": "REL-1510", "item_id": "03-015",
     "person_a": {"text": "吾豫", "person_a_ent_ids": []},
     "person_b": {"text": "项侍郎（吏部）", "person_b_ent_ids": []},
     "relation_type": "恩怨", "direction": "单向",
     "evidence": "请于吏部项侍郎曰是尝搅我兵部者何可与之",
     "confidence": 0.8},
    # 03-016 庄伯和-李无易
    {"rel_id": "REL-1511", "item_id": "03-016",
     "person_a": {"text": "庄伯和", "person_a_ent_ids": []},
     "person_b": {"text": "李无易", "person_b_ent_ids": []},
     "relation_type": "其他", "direction": "双向",
     "evidence": "前辈善谑风味如此伯和子允恭老医常往来吾家",
     "confidence": 0.78},
    # 03-019 庄瑾-沈梦萱契厚
    {"rel_id": "REL-1512", "item_id": "03-019",
     "person_a": {"text": "庄瑾（采芝）", "person_a_ent_ids": []},
     "person_b": {"text": "沈梦萱", "person_b_ent_ids": []},
     "relation_type": "其他", "direction": "双向",
     "evidence": "与同里沈梦萱先生契厚今沈氏收书迹画本特多",
     "confidence": 0.8},
    # 03-020 程明道-彭思永翁婿
    {"rel_id": "REL-1513", "item_id": "03-020",
     "person_a": {"text": "程明道（程颢）", "person_a_ent_ids": []},
     "person_b": {"text": "彭思永（侍郎，外舅）", "person_b_ent_ids": []},
     "relation_type": "姻亲", "direction": "双向",
     "evidence": "程明道先生外舅彭侍郎思永行状",
     "confidence": 0.85},
]
