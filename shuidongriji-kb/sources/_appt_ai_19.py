# -*- coding: utf-8 -*-
"""《水东日记》卷 19 —— APPT 职官任职 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "19-001 | 洪武戊申十一月十四日早朝宣圣五十五代袭封衍圣公臣孔克坚于谨身",
    "19-002 | 太宗文皇帝御制重修孔庙碑文道原于天而畀于圣人圣人者继天立极而",
    "19-003 | 上谕山西潞州壶关县儒士杜斆昔之御宇内者无幸位无遗贤致时和而世",
    "19-004 | 宋文鉴上中下凡一百五十卷朝奉郎行秘书省著作佐郎兼国史院编修官",
    "19-005 | 临江刘公淸之又以为此即删诗定书官使众材之意盖亦善观此书者故备",
    "19-006 | 广东参政仪真黎公恬追和故御史邓州守何公忠廷臣骂贼诗……",
    "19-007 | 元师渡江尝驻黄鹄山即黄鹤也有吕公矶俗传吕洞宾……",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
DATA = [
    # ---- 19-001 孔克坚袭衍圣公 ----
    {"appointment_id": "APPT-9501", "item_id": "19-001",
     "person": {"text": "孔克坚", "person_ent_ids": []},
     "office": {"text": "衍圣公", "official_ent_ids": []},
     "institution": {"text": "曲阜孔府", "ent_ids": []},
     "when": "洪武戊申", "status": "现任",
     "evidence": "宣圣五十五代袭封衍圣公臣孔克坚于谨身殿",
     "confidence": 0.88},
    # ---- 19-006 黎恬广东参政 ----
    {"appointment_id": "APPT-9502", "item_id": "19-006",
     "person": {"text": "黎恬", "person_ent_ids": []},
     "office": {"text": "广东布政司参政", "official_ent_ids": []},
     "institution": {"text": "广东布政司", "ent_ids": []},
     "when": "未明", "status": "现任",
     "evidence": "广东参政仪真黎公恬追和故御史邓州守何公忠廷臣骂贼诗",
     "confidence": 0.82},
    # 缺口登记：19-003 杜斆受诏应征，未明具体授官，不单列。
]
