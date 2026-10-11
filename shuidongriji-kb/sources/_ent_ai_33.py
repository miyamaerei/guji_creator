# -*- coding: utf-8 -*-
"""《水东日记》卷 33 —— L1 实体标注（S4 片填写）

文献优先卷：兰亭诗文。标注序跋所涉作者（晋唐宋明人物）、地名、年号；
兰亭会诸人诗（33-005~087）中的人名随诗题行承载，不逐一建独立 person 实体。
"""

DATA = [
    {"item_id": "33-001", "text": "王右军", "type": "person", "normalized": "王羲之（右军将军，东晋书家）", "confidence": 0.95, "source": "王右军羲之"},
    {"item_id": "33-001", "text": "王羲之", "type": "person", "normalized": "王羲之（王右军）", "confidence": 0.95, "source": "王右军羲之"},
    {"item_id": "33-001", "text": "桓温", "type": "person", "normalized": "桓温（东晋）", "confidence": 0.9, "source": "其与桓温戒谢万"},
    {"item_id": "33-001", "text": "谢万", "type": "person", "normalized": "谢万（东晋）", "confidence": 0.9, "source": "戒谢万"},
    {"item_id": "33-001", "text": "李伯时", "type": "person", "normalized": "李公麟（字伯时，北宋画家）", "confidence": 0.95, "source": "李伯时禊图"},
    {"item_id": "33-001", "text": "曾宏父", "type": "person", "normalized": "曾宏父（庐陵，南宋，刻禊图于凤山别墅）", "confidence": 0.85, "source": "庐陵曾宏父刻于其凤山别墅"},
    {"item_id": "33-001", "text": "绍兴", "type": "place", "normalized": "绍兴（宋绍兴府，今浙江绍兴）", "confidence": 0.9, "source": "今在绍兴"},
    {"item_id": "33-001", "text": "永和", "type": "era", "normalized": "永和（东晋穆帝年号）", "confidence": 0.95, "source": "永和九年岁在癸丑"},
    {"item_id": "33-001", "text": "会稽", "type": "place", "normalized": "会稽（郡，今浙江绍兴一带）", "confidence": 0.95, "source": "会稽山阴之兰亭"},
    {"item_id": "33-001", "text": "兰亭", "type": "place", "normalized": "兰亭（会稽山阴，修禊处）", "confidence": 0.95, "source": "会稽山阴之兰亭"},
    {"item_id": "33-026", "text": "谢安", "type": "person", "normalized": "谢安（东晋，兰亭会主人）", "confidence": 0.9, "source": "琅琊山人谢安"},
    {"item_id": "33-033", "text": "孙绰", "type": "person", "normalized": "孙绰（东晋，作兰亭后序）", "confidence": 0.9, "source": "左司马孙绰"},
    {"item_id": "33-010", "text": "郄昙", "type": "person", "normalized": "郗昙（散骑常侍，东晋）", "confidence": 0.85, "source": "散骑常侍郄昙"},
    {"item_id": "33-090", "text": "公权", "type": "person", "normalized": "柳公权（唐中书舍人/谏议大夫，书家）", "confidence": 0.95, "source": "柳公权续得者亦上…十二日公权状上"},
    {"item_id": "33-092", "text": "褚遂良", "type": "person", "normalized": "褚遂良（唐中书令河南公，榻兰亭序）", "confidence": 0.95, "source": "唐中书令河南公褚遂良所榻"},
    {"item_id": "33-092", "text": "柳公权", "type": "person", "normalized": "柳公权（唐谏议大夫，得群贤诗）", "confidence": 0.95, "source": "谏议大夫柳公权所得群贤诗"},
    {"item_id": "33-092", "text": "李公麟", "type": "person", "normalized": "李公麟（御史检法，制图）", "confidence": 0.9, "source": "御史检法李公麟制图"},
    {"item_id": "33-092", "text": "王晋卿", "type": "person", "normalized": "王诜（字晋卿，北宋驸马，藏三绝）", "confidence": 0.9, "source": "驸马王晋卿家所藏"},
    {"item_id": "33-092", "text": "米芾", "type": "person", "normalized": "米芾（元章，襄阳，北宋书家）", "confidence": 0.95, "source": "襄阳米芾书"},
    {"item_id": "33-093", "text": "韩魏公", "type": "person", "normalized": "韩琦（封魏国公，北宋）", "confidence": 0.85, "source": "问韩魏公之后"},
    {"item_id": "33-093", "text": "杨文贞", "type": "person", "normalized": "杨士奇（谥文贞，明代）", "confidence": 0.85, "source": "杨文贞公尝见刘松年临本"},
    {"item_id": "33-093", "text": "杨文定", "type": "person", "normalized": "杨溥（谥文定，明代）", "confidence": 0.85, "source": "杨文定公尝见赵子昂临本"},
    {"item_id": "33-093", "text": "刘松年", "type": "person", "normalized": "刘松年（南宋画院待诏）", "confidence": 0.85, "source": "刘松年临本"},
    {"item_id": "33-093", "text": "赵子昂", "type": "person", "normalized": "赵孟頫（字子昂，元）", "confidence": 0.9, "source": "赵子昂临本"},
    {"item_id": "33-093", "text": "董仲鲁", "type": "person", "normalized": "董仲鲁（明代中舍）", "confidence": 0.8, "source": "董仲鲁中舍家"},
]
# 缺口：兰亭会诸人诗（33-005~087）中散骑常侍郄昙、礼部谢瑰、王凝之等二十余人，
# 随诗题行承载，不逐一建 person 实体（引录古人事迹，非明代人物图谱重点）。
