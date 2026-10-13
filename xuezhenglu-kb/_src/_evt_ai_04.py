# -*- coding: utf-8 -*-
"""《政学录》卷四 事件层源数据（L5，AI 逐条判定，2026-10-12）。
卷四叙事锚点：04-001 吕坤历述万历陕甘饥荒死事；04-002 附康熙六年董笃行讳盗疏。"""

RECORDS = [
    {"item_id": "04-001", "type": "calamity", "who": "陕甘百姓", "who_ent_ids": [],
     "action": "遭旱", "what": "万历九年十年连年天旱，平凉固原城外掘万人大坑三五十处处处都满，同州朝邑一带饥民抛撇儿女、夫妻投河，百姓逃亡北直河南",
     "when": "万历九年十年", "where": "平凉/固原/同州/朝邑", "confidence": "high"},
    {"item_id": "04-001", "type": "calamity", "who": "邯郸饥民", "who_ent_ids": [],
     "action": "饥死", "what": "万历十四年邯郸路上妇人携三小儿女走步难前，其夫弃之复返，妇人与三孩儿吊死树上，其夫亦自缢",
     "when": "万历十四年", "where": "邯郸", "confidence": "high"},
    {"item_id": "04-001", "type": "disaster_relief", "who": "朝廷", "who_ent_ids": [],
     "action": "赈济", "what": "朝廷差官将四五十万银子放赈济，一人分得一钱半钱不能救一家饥；官府开仓散谷子一人得一斗半斗",
     "when": "万历九年十年间", "where": "陕甘", "confidence": "high"},
    {"item_id": "04-001", "type": "disaster_relief", "who": "西安知府", "who_ent_ids": [],
     "action": "劝留", "what": "西安府城外大村千余家逃走，知府慌忙亲来劝留许放赈济，百姓满街跪下诉说，知府恸哭放他散了",
     "when": "万历九年十年间", "where": "西安府", "confidence": "high"},
    {"item_id": "04-002", "type": "remonstrance", "who": "左副都御史董笃行", "who_ent_ids": [],
     "action": "疏称", "what": "疏称频岁每遇盗警失主未经首告文武各官辄扶同欺隐甚且胁之以刑，讳则仅失财物不讳并荡业产，法太密则群下畏威责过严则职司避罪；请城守官照例议处外鞭长莫及者责其申报，州不报责府府不报责守巡道府不报责督抚督抚不报科道纠参，失主既报后勿得羁留拖累",
     "when": "康熙六年五月", "where": "", "confidence": "high"},
    {"item_id": "04-002", "type": "justice", "who": "祁县黄典史", "who_ent_ids": [],
     "action": "夹折", "what": "祁县黄典史审盗情未问真腿已夹折（吕坤引为审盗酷刑之戒）",
     "when": "未明", "where": "祁县", "confidence": "medium"},
    {"item_id": "04-002", "type": "justice", "who": "太原毛通判", "who_ent_ids": [],
     "action": "辨赃", "what": "有司将良民为盗搜其家黄裙指为失主物，失主认之；太原毛通判取当铺黄裙数条杂置堂上，失主莫知所认，良民则应手而得曰此吾裙也，失主无辞良民遂释（吕坤引为审赃之戒）",
     "when": "未明", "where": "太原", "confidence": "medium"},
    {"item_id": "04-002", "type": "justice", "who": "苍南吕公（吕坤）", "who_ent_ids": [],
     "action": "审狱", "what": "吕坤巡海右时一寡妇被劫获盗十人搜赃俱在内有女鞋一对，快壮过寡妇家令其认鞋有样，县官审赃寡妇一一俱认，十人临刑前真盗悉获真赃悉出，十人得释（吕坤引为审赃之戒）",
     "when": "未明", "where": "海右", "confidence": "medium"},
]
