# -*- coding: utf-8 -*-
"""《水东日记》卷 36 —— L1 实体标注（S4 片填写）

文事优先卷：叶盛诗话。标注诗评所涉主要诗人与诗话作者；引录诗句随 LIT 承载。
"""

DATA = [
    {"item_id": "36-001", "text": "蔡正孙", "type": "person", "normalized": "蔡正孙（元代，《诗林广记》编者）", "confidence": 0.9, "source": "元至正中蔡正孙氏所著"},
    {"item_id": "36-001", "text": "诗林广记", "type": "work", "normalized": "《诗林广记》（蔡正孙编，前集十卷）", "confidence": 0.95, "source": "诗林广记"},
    {"item_id": "36-002", "text": "陶渊明", "type": "person", "normalized": "陶渊明（晋，诗人）", "confidence": 0.9, "source": "陶渊明诗"},
    {"item_id": "36-006", "text": "杜子美", "type": "person", "normalized": "杜甫（字子美，唐诗人）", "confidence": 0.95, "source": "杜子美诗"},
    {"item_id": "36-007", "text": "朱文公", "type": "person", "normalized": "朱熹（号文公，南宋）", "confidence": 0.9, "source": "朱文公云云"},
    {"item_id": "36-008", "text": "胡苕溪", "type": "person", "normalized": "胡仔（号苕溪渔隐，南宋诗话作者）", "confidence": 0.85, "source": "胡苕溪云"},
    {"item_id": "36-008", "text": "山谷", "type": "person", "normalized": "黄庭坚（号山谷，北宋）", "confidence": 0.9, "source": "山谷之言"},
    {"item_id": "36-013", "text": "杨诚斋", "type": "person", "normalized": "杨万里（号诚斋，南宋）", "confidence": 0.9, "source": "杨诚斋云云"},
    {"item_id": "36-021", "text": "李太白", "type": "person", "normalized": "李白（字太白，唐诗人）", "confidence": 0.95, "source": "李太白登凤凰台诗"},
    {"item_id": "36-021", "text": "刘后村", "type": "person", "normalized": "刘克庄（号后村，南宋）", "confidence": 0.9, "source": "刘后村诗话"},
    {"item_id": "36-027", "text": "韦苏州", "type": "person", "normalized": "韦应物（唐，苏州刺史）", "confidence": 0.9, "source": "韦苏州"},
    {"item_id": "36-029", "text": "刘禹锡", "type": "person", "normalized": "刘禹锡（唐诗人）", "confidence": 0.9, "source": "刘禹锡杨柳枝辞"},
    {"item_id": "36-032", "text": "柳子厚", "type": "person", "normalized": "柳宗元（字子厚，唐）", "confidence": 0.9, "source": "酬柳子厚"},
    {"item_id": "36-039", "text": "柳子厚", "type": "person", "normalized": "柳宗元（子厚南涧中题）", "confidence": 0.9, "source": "柳子厚南涧中题诗"},
    {"item_id": "36-041", "text": "王摩诘", "type": "person", "normalized": "王维（字摩诘，唐）", "confidence": 0.9, "source": "王摩诘辋川庄诗"},
    {"item_id": "36-045", "text": "李义山", "type": "person", "normalized": "李商隐（字义山，唐）", "confidence": 0.9, "source": "李义山诗"},
    {"item_id": "36-050", "text": "沈文敏", "type": "person", "normalized": "沈文敏（叶盛亡友，宪副）", "confidence": 0.8, "source": "亡友沈文敏宪副"},
    {"item_id": "36-057", "text": "杜牧之", "type": "person", "normalized": "杜牧（字牧之，唐）", "confidence": 0.9, "source": "杜牧之赤壁诗"},
    {"item_id": "36-068", "text": "贾阆仙", "type": "person", "normalized": "贾岛（字阆仙，唐）", "confidence": 0.9, "source": "贾阆仙下第诗"},
    {"item_id": "36-070", "text": "卢玉川", "type": "person", "normalized": "卢仝（号玉川子，唐）", "confidence": 0.9, "source": "卢玉川山中诗"},
    {"item_id": "36-073", "text": "李长吉", "type": "person", "normalized": "李贺（字长吉，唐）", "confidence": 0.9, "source": "李长吉雁门太守诗"},
    {"item_id": "36-075", "text": "韩致光", "type": "person", "normalized": "韩偓（字致光，唐）", "confidence": 0.9, "source": "韩致光雷公诗"},
    {"item_id": "36-077", "text": "杜荀鹤", "type": "person", "normalized": "杜荀鹤（唐诗人）", "confidence": 0.9, "source": "杜荀鹤闻子规诗"},
    {"item_id": "36-086", "text": "张继", "type": "person", "normalized": "张继（唐，枫桥夜泊）", "confidence": 0.9, "source": "张继枫桥夜泊诗"},
    {"item_id": "36-087", "text": "欧阳公", "type": "person", "normalized": "欧阳修（北宋）", "confidence": 0.9, "source": "欧阳公以夜半钟为语病"},
]
