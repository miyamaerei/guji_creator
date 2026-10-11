# -*- coding: utf-8 -*-
"""《水东日记》卷 32 —— L1 实体标注 源数据（AI 判定逐条填写）

覆盖条目：32-001~32-021（共 21 条）。
"""

ITEM_LIST = [
    "32-001 | 英宗皇帝一日御祥凤楼",
    "32-002 | 二月十一日熹顿首再拜上记",
    "32-003 | 德修宫使直阁左史舍人老兄",
    "32-004 | 熹顿首再拜上记",
    "32-005 | 山西疆理图",
    "32-006 | 此图盖据今山西左布政使丘陵",
    "32-007 | 左布政使杨鼎廷器扶沟县人",
    "32-008 | 张茂景芳咸宁县人",
    "32-009 | 右布政使侯复昌平县人",
    "32-010 | 陈翌冲霄虹县人",
    "32-011 | 左参政王英闽县人",
    "32-012 | 刘训忠言麻城县人",
    "32-013 | 右参政王庾仲京江夏县人",
    "32-014 | 杨璿叔玑无锡县人",
    "32-015 | 左参议祝颢维清长洲县人",
    "32-016 | 右参议郭恕安仁鸡泽县人",
    "32-017 | 魏琳廷珪肥乡县人",
    "32-018 | 于泰伯亨德州人",
    "32-019 | 毕鸾冲霄井陉县人",
    "32-020 | 昆山龚钝庵老先生今年八十七矣",
    "32-021 | 丞相雍国忠肃公奏议序",
]

DATA = [
    # ---- 32-001 英宗祥凤楼 ----
    {"id": "ENT-16001", "item_id": "32-001", "text": "英宗皇帝", "type": "person", "start": 0, "end": 0, "normalized": "明英宗朱祁镇", "confidence": 0.95, "source": "英宗皇帝一日御祥凤楼"},
    {"id": "ENT-16002", "item_id": "32-001", "text": "祥凤楼", "type": "place", "start": 0, "end": 0, "normalized": "祥凤楼", "confidence": 0.88, "source": "御祥凤楼"},
    {"id": "ENT-16003", "item_id": "32-001", "text": "吴瑾", "type": "person", "start": 0, "end": 0, "normalized": "吴瑾（恭顺侯）", "confidence": 0.88, "source": "恭顺侯吴瑾"},
    {"id": "ENT-16004", "item_id": "32-001", "text": "朱永", "type": "person", "start": 0, "end": 0, "normalized": "朱永（抚宁伯）", "confidence": 0.88, "source": "抚宁伯朱永"},
    {"id": "ENT-16005", "item_id": "32-001", "text": "忠国公", "type": "person", "start": 0, "end": 0, "normalized": "石亨（封忠国公）", "confidence": 0.92, "source": "忠国公新第成"},
    {"id": "ENT-16006", "item_id": "32-001", "text": "裴当", "type": "person", "start": 0, "end": 0, "normalized": "裴当（太监）", "confidence": 0.85, "source": "太监裴当"},
    {"id": "ENT-16007", "item_id": "32-001", "text": "景昌", "type": "person", "start": 0, "end": 0, "normalized": "景昌（抚宁侯、平北将军总兵官）", "confidence": 0.82, "source": "抚宁侯景昌"},
    {"id": "ENT-16008", "item_id": "32-001", "text": "刘文节公光祖", "type": "person", "start": 0, "end": 0, "normalized": "刘光祖（谥文节）", "confidence": 0.92, "source": "宋刘文节公光祖"},
    {"id": "ENT-16009", "item_id": "32-001", "text": "晦庵", "type": "person", "start": 0, "end": 0, "normalized": "朱熹（号晦庵）", "confidence": 0.92, "source": "与晦庵同时同道"},
    {"id": "ENT-16010", "item_id": "32-001", "text": "刘德修", "type": "person", "start": 0, "end": 0, "normalized": "刘光祖（字德修）", "confidence": 0.88, "source": "与刘德修书"},
    {"id": "ENT-16011", "item_id": "32-001", "text": "范石湖", "type": "person", "start": 0, "end": 0, "normalized": "范成大（号石湖）", "confidence": 0.88, "source": "范石湖书"},
    # ---- 32-005~019 山西疆理图+同僚题名 ----
    {"id": "ENT-16012", "item_id": "32-005", "text": "山西疆理图", "type": "work", "start": 0, "end": 0, "normalized": "山西疆理图", "confidence": 0.9, "source": "山西疆理图"},
    {"id": "ENT-16013", "item_id": "32-006", "text": "山西左布政使", "type": "official", "start": 0, "end": 0, "normalized": "山西左布政使", "confidence": 0.9, "source": "山西左布政使丘陵"},
    {"id": "ENT-16014", "item_id": "32-006", "text": "丘陵", "type": "person", "start": 0, "end": 0, "normalized": "丘陵（山西左布政使）", "confidence": 0.85, "source": "左布政使丘陵"},
    {"id": "ENT-16015", "item_id": "32-006", "text": "太原", "type": "place", "start": 0, "end": 0, "normalized": "太原", "confidence": 0.9, "source": "太原有晋王府"},
    {"id": "ENT-16016", "item_id": "32-006", "text": "大同", "type": "place", "start": 0, "end": 0, "normalized": "大同", "confidence": 0.9, "source": "大同有大王府"},
    {"id": "ENT-16017", "item_id": "32-007", "text": "杨鼎", "type": "person", "start": 0, "end": 0, "normalized": "杨鼎（字廷器，扶沟）", "confidence": 0.88, "source": "左布政使杨鼎廷器"},
    {"id": "ENT-16018", "item_id": "32-008", "text": "张茂", "type": "person", "start": 0, "end": 0, "normalized": "张茂（字景芳，咸宁）", "confidence": 0.85, "source": "张茂景芳咸宁"},
    {"id": "ENT-16019", "item_id": "32-009", "text": "侯复", "type": "person", "start": 0, "end": 0, "normalized": "侯复（昌平）", "confidence": 0.85, "source": "右布政使侯复"},
    {"id": "ENT-16020", "item_id": "32-010", "text": "陈翌", "type": "person", "start": 0, "end": 0, "normalized": "陈翌（字冲霄，虹县）", "confidence": 0.85, "source": "陈翌冲霄虹县"},
    {"id": "ENT-16021", "item_id": "32-011", "text": "王英", "type": "person", "start": 0, "end": 0, "normalized": "王英（闽县）", "confidence": 0.85, "source": "左参政王英"},
    {"id": "ENT-16022", "item_id": "32-012", "text": "刘训", "type": "person", "start": 0, "end": 0, "normalized": "刘训（字忠言，麻城）", "confidence": 0.85, "source": "刘训忠言麻城"},
    {"id": "ENT-16023", "item_id": "32-013", "text": "王庾", "type": "person", "start": 0, "end": 0, "normalized": "王庾（字仲京，江夏）", "confidence": 0.85, "source": "右参政王庾仲京"},
    {"id": "ENT-16024", "item_id": "32-014", "text": "杨璿", "type": "person", "start": 0, "end": 0, "normalized": "杨璿（字叔玑，无锡）", "confidence": 0.85, "source": "杨璿叔玑无锡"},
    {"id": "ENT-16025", "item_id": "32-015", "text": "祝颢", "type": "person", "start": 0, "end": 0, "normalized": "祝颢（字维清，长洲）", "confidence": 0.85, "source": "左参议祝颢维清"},
    {"id": "ENT-16026", "item_id": "32-016", "text": "郭恕", "type": "person", "start": 0, "end": 0, "normalized": "郭恕（字安仁，鸡泽）", "confidence": 0.85, "source": "右参议郭恕安仁"},
    {"id": "ENT-16027", "item_id": "32-017", "text": "魏琳", "type": "person", "start": 0, "end": 0, "normalized": "魏琳（字廷珪，肥乡）", "confidence": 0.85, "source": "魏琳廷珪肥乡"},
    {"id": "ENT-16028", "item_id": "32-018", "text": "于泰", "type": "person", "start": 0, "end": 0, "normalized": "于泰（字伯亨，德州）", "confidence": 0.85, "source": "于泰伯亨德州"},
    {"id": "ENT-16029", "item_id": "32-019", "text": "毕鸾", "type": "person", "start": 0, "end": 0, "normalized": "毕鸾（字冲霄，井陉）", "confidence": 0.85, "source": "毕鸾冲霄井陉"},
    # ---- 32-020 龚钝庵 ----
    {"id": "ENT-16030", "item_id": "32-020", "text": "龚钝庵", "type": "person", "start": 0, "end": 0, "normalized": "龚钝庵（昆山）", "confidence": 0.85, "source": "昆山龚钝庵老先生"},
    # ---- 32-021 雍国忠肃公奏议序 ----
    {"id": "ENT-16031", "item_id": "32-021", "text": "雍国忠肃公", "type": "person", "start": 0, "end": 0, "normalized": "虞允文（封雍国公，谥忠肃）", "confidence": 0.92, "source": "丞相雍国忠肃公"},
    {"id": "ENT-16032", "item_id": "32-021", "text": "虞允文奏议", "type": "work", "start": 0, "end": 0, "normalized": "雍国忠肃公奏议", "confidence": 0.9, "source": "雍国忠肃公奏议二百二十七篇"},
    {"id": "ENT-16033", "item_id": "32-021", "text": "高宗皇帝", "type": "person", "start": 0, "end": 0, "normalized": "宋高宗", "confidence": 0.9, "source": "高宗皇帝擢为中书舍人"},
    {"id": "ENT-16034", "item_id": "32-021", "text": "陈康伯", "type": "person", "start": 0, "end": 0, "normalized": "陈康伯（封福国公）", "confidence": 0.85, "source": "白宰相陈福公康伯"},
    {"id": "ENT-16035", "item_id": "32-021", "text": "魏了翁", "type": "person", "start": 0, "end": 0, "normalized": "魏了翁", "confidence": 0.88, "source": "东漕魏了翁"},
    {"id": "ENT-16036", "item_id": "32-021", "text": "赵雄", "type": "person", "start": 0, "end": 0, "normalized": "赵雄（卫国文定）", "confidence": 0.85, "source": "卫国文定赵公雄"},
    {"id": "ENT-16037", "item_id": "32-021", "text": "采石之战", "type": "event", "start": 0, "end": 0, "normalized": "采石之战", "confidence": 0.88, "source": "采石之战有七千之卒"},
]
# 缺口登记：32-003 朱熹书中人物（黄仲本、刘主簿等）不单列；32-020 龚钝庵诗中郑前政/新令郑公不具名。
