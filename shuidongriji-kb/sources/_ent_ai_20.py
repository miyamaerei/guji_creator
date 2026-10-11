# -*- coding: utf-8 -*-
"""《水东日记》卷 20 —— L1 实体标注 源数据（AI 判定逐条填写）

覆盖条目：20-001~20-009（共 9 条）。
只写解读字段；start/end 暂记 0/0，打包器可重算。
"""

ITEM_LIST = [
    "20-001 | 南雄杨氏谱本蜀唐祭酒两淮运副有文",
    "20-002 | 张篠庵有秋台清话未成卷",
    "20-003 | 雪庵者元僧云中人头陀教大宗师",
    "20-004 | 西斋亦元僧其谢事檇李归和陶归去来辞韵",
    "20-005 | 天顺四年过南京见夏时正寅卿中手临范文正公与监簿兄家书",
    "20-006 | 仲淹拜上三哥监簿",
    "20-007 | 邵复孺先生家藏老苏大全文集四十五卷",
    "20-008 | 吉安程源伊知府处见文山文集道体堂元编二书",
    "20-009 | 景泰辛未廷试盛预弥封",
]

DATA = [
    # ---- 20-001 南雄杨氏谱+虞文靖公帖 ----
    {"id": "ENT-10001", "item_id": "20-001", "text": "南雄杨氏谱", "type": "work", "start": 0, "end": 0, "normalized": "南雄杨氏谱", "confidence": 0.9, "source": "条1首句"},
    {"id": "ENT-10002", "item_id": "20-001", "text": "蜀", "type": "place", "start": 0, "end": 0, "normalized": "蜀", "confidence": 0.85, "source": "本蜀"},
    {"id": "ENT-10003", "item_id": "20-001", "text": "唐祭酒", "type": "official", "start": 0, "end": 0, "normalized": "祭酒", "confidence": 0.85, "source": "唐祭酒两淮运副"},
    {"id": "ENT-10004", "item_id": "20-001", "text": "两淮运副", "type": "official", "start": 0, "end": 0, "normalized": "两淮运副", "confidence": 0.85, "source": "两淮运副有文"},
    {"id": "ENT-10005", "item_id": "20-001", "text": "有文", "type": "person", "start": 0, "end": 0, "normalized": "有文", "confidence": 0.8, "source": "两淮运副有文"},
    {"id": "ENT-10006", "item_id": "20-001", "text": "虞文靖公", "type": "person", "start": 0, "end": 0, "normalized": "虞集", "confidence": 0.9, "source": "家藏虞文靖公所撰衡州府君墓碑"},
    {"id": "ENT-10007", "item_id": "20-001", "text": "衡州府君墓碑", "type": "work", "start": 0, "end": 0, "normalized": "衡州府君墓碑", "confidence": 0.88, "source": "虞文靖公所撰衡州府君墓碑"},
    {"id": "ENT-10008", "item_id": "20-001", "text": "子牧", "type": "person", "start": 0, "end": 0, "normalized": "子牧", "confidence": 0.85, "source": "子牧孝廉贤表侄"},
    {"id": "ENT-10009", "item_id": "20-001", "text": "集", "type": "person", "start": 0, "end": 0, "normalized": "虞集", "confidence": 0.9, "source": "集记事奉复子牧"},
    # ---- 20-002 张篠庵秋台清话 ----
    {"id": "ENT-10010", "item_id": "20-002", "text": "张篠庵", "type": "person", "start": 0, "end": 0, "normalized": "张篠庵", "confidence": 0.85, "source": "张篠庵有秋台清话"},
    {"id": "ENT-10011", "item_id": "20-002", "text": "秋台清话", "type": "work", "start": 0, "end": 0, "normalized": "秋台清话", "confidence": 0.88, "source": "秋台清话未成卷"},
    {"id": "ENT-10012", "item_id": "20-002", "text": "景泰", "type": "era", "start": 0, "end": 0, "normalized": "景泰", "confidence": 0.9, "source": "景泰甲戌冬"},
    {"id": "ENT-10013", "item_id": "20-002", "text": "雪庵长语", "type": "work", "start": 0, "end": 0, "normalized": "雪庵长语", "confidence": 0.9, "source": "雪庵长语"},
    {"id": "ENT-10014", "item_id": "20-002", "text": "西斋和陶集", "type": "work", "start": 0, "end": 0, "normalized": "西斋和陶集", "confidence": 0.9, "source": "西斋和陶集"},
    # ---- 20-003 雪庵诗 ----
    {"id": "ENT-10015", "item_id": "20-003", "text": "雪庵", "type": "person", "start": 0, "end": 0, "normalized": "雪庵（李玄晖）", "confidence": 0.9, "source": "雪庵者元僧云中人头陀教大宗师"},
    {"id": "ENT-10016", "item_id": "20-003", "text": "头陀教大宗师", "type": "official", "start": 0, "end": 0, "normalized": "头陀教大宗师", "confidence": 0.85, "source": "头陀教大宗师"},
    {"id": "ENT-10017", "item_id": "20-003", "text": "昭文馆大学士", "type": "official", "start": 0, "end": 0, "normalized": "昭文馆大学士", "confidence": 0.88, "source": "任昭文馆大学士"},
    {"id": "ENT-10018", "item_id": "20-003", "text": "李玄晖", "type": "person", "start": 0, "end": 0, "normalized": "李玄晖", "confidence": 0.88, "source": "俗姓李氏字玄晖"},
    # ---- 20-004 西斋和陶 ----
    {"id": "ENT-10019", "item_id": "20-004", "text": "西斋", "type": "person", "start": 0, "end": 0, "normalized": "西斋（元僧）", "confidence": 0.9, "source": "西斋亦元僧"},
    {"id": "ENT-10020", "item_id": "20-004", "text": "檇李", "type": "place", "start": 0, "end": 0, "normalized": "檇李（嘉兴）", "confidence": 0.85, "source": "谢事檇李归"},
    {"id": "ENT-10021", "item_id": "20-004", "text": "和陶归去来辞", "type": "work", "start": 0, "end": 0, "normalized": "和陶归去来辞", "confidence": 0.88, "source": "和陶归去来辞韵"},
    # ---- 20-005 夏时正临范文正家书 ----
    {"id": "ENT-10022", "item_id": "20-005", "text": "夏时正", "type": "person", "start": 0, "end": 0, "normalized": "夏时正（寅卿）", "confidence": 0.88, "source": "夏时正寅卿"},
    {"id": "ENT-10023", "item_id": "20-005", "text": "范文正公", "type": "person", "start": 0, "end": 0, "normalized": "范仲淹（谥文正）", "confidence": 0.95, "source": "范文正公与监簿兄家书"},
    {"id": "ENT-10024", "item_id": "20-005", "text": "南京", "type": "place", "start": 0, "end": 0, "normalized": "南京", "confidence": 0.9, "source": "过南京"},
    {"id": "ENT-10025", "item_id": "20-005", "text": "监簿", "type": "official", "start": 0, "end": 0, "normalized": "监簿", "confidence": 0.85, "source": "监簿兄"},
    # ---- 20-006 范仲淹家书 ----
    {"id": "ENT-10026", "item_id": "20-006", "text": "范仲淹", "type": "person", "start": 0, "end": 0, "normalized": "范仲淹", "confidence": 0.95, "source": "弟仲淹拜上"},
    {"id": "ENT-10027", "item_id": "20-006", "text": "三哥监簿", "type": "person", "start": 0, "end": 0, "normalized": "三哥（范氏兄，监簿）", "confidence": 0.8, "source": "仲淹拜上三哥监簿"},
    {"id": "ENT-10028", "item_id": "20-006", "text": "贰枢府", "type": "official", "start": 0, "end": 0, "normalized": "枢密副使", "confidence": 0.85, "source": "擢贰枢府"},
    {"id": "ENT-10029", "item_id": "20-006", "text": "参大政", "type": "official", "start": 0, "end": 0, "normalized": "参知政事", "confidence": 0.85, "source": "改参大政"},
    {"id": "ENT-10030", "item_id": "20-006", "text": "西府", "type": "institution", "start": 0, "end": 0, "normalized": "西府（枢密院）", "confidence": 0.8, "source": "且在西府"},
    # ---- 20-007 三苏文集 ----
    {"id": "ENT-10031", "item_id": "20-007", "text": "邵复孺", "type": "person", "start": 0, "end": 0, "normalized": "邵复孺（邵亨贞）", "confidence": 0.85, "source": "邵复孺先生"},
    {"id": "ENT-10032", "item_id": "20-007", "text": "老苏大全文集", "type": "work", "start": 0, "end": 0, "normalized": "老苏大全文集（苏洵）", "confidence": 0.9, "source": "老苏大全文集四十五卷"},
    {"id": "ENT-10033", "item_id": "20-007", "text": "东坡大全集", "type": "work", "start": 0, "end": 0, "normalized": "东坡大全集（苏轼）", "confidence": 0.9, "source": "东坡大全文集"},
    {"id": "ENT-10034", "item_id": "20-007", "text": "栾城集", "type": "work", "start": 0, "end": 0, "normalized": "栾城集（苏辙）", "confidence": 0.9, "source": "栾城集五十卷"},
    {"id": "ENT-10035", "item_id": "20-007", "text": "苏峤", "type": "person", "start": 0, "end": 0, "normalized": "苏峤", "confidence": 0.8, "source": "御制赐苏峤序"},
    # ---- 20-008 文山文集 ----
    {"id": "ENT-10036", "item_id": "20-008", "text": "程源伊知府", "type": "person", "start": 0, "end": 0, "normalized": "程源（伊姓知府）", "confidence": 0.8, "source": "吉安程源伊知府"},
    {"id": "ENT-10037", "item_id": "20-008", "text": "文山文集", "type": "work", "start": 0, "end": 0, "normalized": "文山文集（文天祥）", "confidence": 0.9, "source": "见文山文集"},
    {"id": "ENT-10038", "item_id": "20-008", "text": "文天祥", "type": "person", "start": 0, "end": 0, "normalized": "文天祥（号文山）", "confidence": 0.92, "source": "文山文集"},
    # ---- 20-009 景泰辛未廷试 ----
    {"id": "ENT-10039", "item_id": "20-009", "text": "徐珵", "type": "person", "start": 0, "end": 0, "normalized": "徐珵（即徐有贞）", "confidence": 0.9, "source": "徐侍讲珵"},
    {"id": "ENT-10040", "item_id": "20-009", "text": "陈叔绍", "type": "person", "start": 0, "end": 0, "normalized": "陈叔绍", "confidence": 0.85, "source": "陈御史同年叔绍"},
    {"id": "ENT-10041", "item_id": "20-009", "text": "王越", "type": "person", "start": 0, "end": 0, "normalized": "王越（濬县）", "confidence": 0.92, "source": "乃濬县王越也"},
    {"id": "ENT-10042", "item_id": "20-009", "text": "成凯", "type": "person", "start": 0, "end": 0, "normalized": "成凯", "confidence": 0.85, "source": "成凯卷以病录正不完"},
    {"id": "ENT-10043", "item_id": "20-009", "text": "王抑庵", "type": "person", "start": 0, "end": 0, "normalized": "王直（号抑庵）", "confidence": 0.9, "source": "抑庵王先生"},
    {"id": "ENT-10044", "item_id": "20-009", "text": "陈阁老", "type": "person", "start": 0, "end": 0, "normalized": "陈阁老（陈循）", "confidence": 0.82, "source": "陈阁老已得三卷"},
    {"id": "ENT-10045", "item_id": "20-009", "text": "商辂", "type": "person", "start": 0, "end": 0, "normalized": "商辂（字弘载）", "confidence": 0.9, "source": "商弘载至"},
    {"id": "ENT-10046", "item_id": "20-009", "text": "柯潜", "type": "person", "start": 0, "end": 0, "normalized": "柯潜（状元）", "confidence": 0.92, "source": "始得柯状元潜"},
    {"id": "ENT-10047", "item_id": "20-009", "text": "吴汇", "type": "person", "start": 0, "end": 0, "normalized": "吴汇", "confidence": 0.85, "source": "摸出一卷则吴汇也"},
    {"id": "ENT-10048", "item_id": "20-009", "text": "兵科", "type": "institution", "start": 0, "end": 0, "normalized": "兵科", "confidence": 0.9, "source": "至兵科书奏"},
    {"id": "ENT-10049", "item_id": "20-009", "text": "弥封", "type": "official", "start": 0, "end": 0, "normalized": "弥封官", "confidence": 0.8, "source": "盛预弥封"},
]
# 缺口登记：20-002/003/004 诗长文已按作者/文献标注；20-003 雪庵长诗中人名（范蠡/勾践/伯夷/叔齐等典故）不单建。
