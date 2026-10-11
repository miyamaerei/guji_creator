# -*- coding: utf-8 -*-
"""《水东日记》卷 14 —— APPT 职官任职 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "14-001 | 皇祐四年夏五月邕獠刦库兵称乱陈船顺江絶数郡郡之守臣狃于承平弛",
    "14-002 | 王抑庵先生还政归泰和日有叹落花一首最爱东园桃李花可堪飘荡委泥",
    "14-003 | 王贞妇淸风岭事昭然在金石灿然在简册可征也夏宪使言昔有一人以为",
    "14-004 | 东广人言其地有宋坟无唐坟盖自宋南渡后衣冠家多流落至此始变其族",
    "14-005 | 庐陵李祯字昌祺河南左布政使为人耿介亷洁自始仕至归老始终一致人",
    "14-006 | 广州府学教授长乐郑万奎藏其父躭犁手卷有洪武甲戌国子博士临安钱宰",
    "14-007 | 右程子遗书二十五篇二先生门人记其所见闻荅问之书也始诸公各自为",
    "14-008 | 杭州西湖傍近编竹节水可专菱芡之利而惟时有势力者可得之故杭人有",
    "14-009 | 韩都御史雍坐事被收西江术者周季龙曰此都御史官也及左迁按察司",
    "14-010 | 李景瓒占命闻京师至山东谓陆布政瑜曰刑部刘尚书休矣公宜促装代之",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
DATA = [
    # ---- 14-001 赵师旦知康州 ----
    {"appointment_id": "APPT-7001", "item_id": "14-001",
     "person": {"text": "赵师旦", "person_ent_ids": []},
     "office": {"text": "康州知州", "official_ent_ids": []},
     "institution": {"text": "康州", "ent_ids": []},
     "when": "皇祐四年", "status": "现任",
     "evidence": "题赠光禄少卿康州赵使君师旦……城门既开度必死坚坐廷上贼捽而害之",
     "confidence": 0.88},
    {"appointment_id": "APPT-7002", "item_id": "14-001",
     "person": {"text": "曹觐", "person_ent_ids": []},
     "office": {"text": "封州知州", "official_ent_ids": []},
     "institution": {"text": "封州", "ent_ids": []},
     "when": "皇祐四年", "status": "现任",
     "evidence": "大夫赠太常少卿封州曹使君觐……军吏潜遯力穷被禽使之拜又訹以伪官皆不屈",
     "confidence": 0.88},
    {"appointment_id": "APPT-7003", "item_id": "14-001",
     "person": {"text": "元绛", "person_ent_ids": []},
     "office": {"text": "广南东路转运使", "official_ent_ids": []},
     "institution": {"text": "广南东路", "ent_ids": []},
     "when": "皇祐后", "status": "现任",
     "evidence": "广南东路转运使尚书司封员外郎直集贤院武林元绛题",
     "confidence": 0.82},
    # ---- 14-005 李祯河南左布政使 ----
    {"appointment_id": "APPT-7004", "item_id": "14-005",
     "person": {"text": "李祯（昌祺）", "person_ent_ids": []},
     "office": {"text": "河南左布政使", "official_ent_ids": []},
     "institution": {"text": "河南布政司", "ent_ids": []},
     "when": "未明", "status": "致仕",
     "evidence": "庐陵李祯字昌祺河南左布政使为人耿介廉洁自始仕至归老始终一致",
     "confidence": 0.85},
    # ---- 14-006 张显宗国子祭酒 ----
    {"appointment_id": "APPT-7005", "item_id": "14-006",
     "person": {"text": "张显宗", "person_ent_ids": []},
     "office": {"text": "国子祭酒", "official_ent_ids": []},
     "institution": {"text": "国子监", "ent_ids": []},
     "when": "洪武建文间", "status": "升迁",
     "evidence": "显宗状元及第……后任国子祭酒往江西起义兵不知所终",
     "confidence": 0.8},
    # 缺口登记：14-008/009/010 诸人官称已在 ent 标注，占命相术条不另抽任职句。
]
