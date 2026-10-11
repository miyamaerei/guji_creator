# -*- coding: utf-8 -*-
"""《水东日记》卷 34 —— L1 实体标注（S4 片填写）

文事·名录卷：前 6 条文论/太监/画像/边政，34-007~089 宣府守将题名。
题名中人名随 NAM entries 承载；本层标注叙事所涉人物/地名/机构。
"""

DATA = [
    {"item_id": "34-001", "text": "欧阳文忠公", "type": "person", "normalized": "欧阳修（谥文忠，北宋）", "confidence": 0.95, "source": "宋欧阳文忠公"},
    {"item_id": "34-001", "text": "朱文公", "type": "person", "normalized": "朱熹（谥文，南宋）", "confidence": 0.95, "source": "朱文公"},
    {"item_id": "34-001", "text": "范文正公", "type": "person", "normalized": "范仲淹（谥文正，北宋）", "confidence": 0.9, "source": "范文正公用水陆斋"},
    {"item_id": "34-001", "text": "文山丞相", "type": "person", "normalized": "文天祥（号文山，南宋丞相）", "confidence": 0.9, "source": "文山丞相"},
    {"item_id": "34-001", "text": "杨东里", "type": "person", "normalized": "杨士奇（号东里，明代）", "confidence": 0.9, "source": "杨东里先生"},
    {"item_id": "34-001", "text": "于节庵", "type": "person", "normalized": "于谦（号节庵，明代）", "confidence": 0.9, "source": "于节庵巡抚河南山西"},
    {"item_id": "34-002", "text": "陈芜", "type": "person", "normalized": "陈芜（赐姓名王瑾，字润德，交阯人，御用监太监）", "confidence": 0.95, "source": "御用监太监陈芜交阯人…赐姓名曰王瑾"},
    {"item_id": "34-002", "text": "交阯", "type": "place", "normalized": "交阯（今越南北部）", "confidence": 0.9, "source": "交阯人"},
    {"item_id": "34-002", "text": "永乐", "type": "era", "normalized": "永乐（明成祖年号）", "confidence": 0.95, "source": "永乐丁亥入内府"},
    {"item_id": "34-003", "text": "白乐天", "type": "person", "normalized": "白居易（字乐天，唐）", "confidence": 0.95, "source": "白乐天画像"},
    {"item_id": "34-004", "text": "李伯时", "type": "person", "normalized": "李公麟（字伯时，北宋画家）", "confidence": 0.9, "source": "临伯时者"},
    {"item_id": "34-004", "text": "王晋卿", "type": "person", "normalized": "王诜（字晋卿，北宋驸马）", "confidence": 0.9, "source": "李伯时王晋卿"},
    {"item_id": "34-004", "text": "刘松年", "type": "person", "normalized": "刘松年（南宋画院待诏）", "confidence": 0.85, "source": "刘松年临本"},
    {"item_id": "34-005", "text": "宣府", "type": "place", "normalized": "宣府（明九边重镇，今河北宣化）", "confidence": 0.95, "source": "宣府在居庸西北"},
    {"item_id": "34-005", "text": "居庸", "type": "place", "normalized": "居庸关（长城关隘）", "confidence": 0.9, "source": "居庸西北"},
    {"item_id": "34-005", "text": "万全都指挥使司", "type": "institution", "normalized": "万全都指挥使司（明边防军事机构）", "confidence": 0.95, "source": "万全都指挥使司为卫所者十有九"},
    {"item_id": "34-005", "text": "镇朔将军", "type": "official", "normalized": "镇朔将军（宣府总兵挂印）", "confidence": 0.9, "source": "镇守镇朔将军总兵官"},
    {"item_id": "34-006", "text": "纪广", "type": "person", "normalized": "纪广（都督，宣府总兵）", "confidence": 0.85, "source": "总戎则都督纪广"},
    {"item_id": "34-006", "text": "李秉", "type": "person", "normalized": "李秉（曹州，总督边储赞理军务）", "confidence": 0.9, "source": "曹州李公秉总督边储"},
    {"item_id": "34-006", "text": "杨信", "type": "person", "normalized": "杨信（都督，宣府副将）", "confidence": 0.85, "source": "参将都督杨信升副总兵"},
    {"item_id": "34-006", "text": "赵辅", "type": "person", "normalized": "赵辅（署都督佥事，代杨信）", "confidence": 0.85, "source": "署都督佥事赵辅实代之"},
]
# 缺口：宣府守将题名（34-007~089）百余人以 NAM-17001 entries 承载，不逐一建 person 实体。
