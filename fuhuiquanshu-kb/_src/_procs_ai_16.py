# -*- coding: utf-8 -*-
"""卷16 刑名部六·流程 PROC（2 条）。"""
RECORDS = [
    {"item_id": "16-001", "name": "检枯骨流程", "steps": [
        {"seq": 1, "text": "须择晴明天气，先以水洗净用麻依次穿成形骸以簟子铺定", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "开一地窖深二尺许长短与簟等，以柴炭烧窖红去火，用好酒二升米醋五升泼之", "agent": "官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "乘热扛簟骨入窖覆以草荐蒸一二时，俟地冷取出平明处将红油伞遮日照勘", "agent": "官", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "照日细看：骨有被打处即露红色微荫，骨断处两头各晕血色，红活者生前伤，无血晕虽有损折乃死后痕", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "16-001", "name": "保辜流程", "steps": [
        {"seq": 1, "text": "殴伤人未至于死难即定罪，当官立限以保之保人之伤正所保已之罪也", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "本官先验其伤之轻重，注明系某处伤照依圆长青赤分寸或手足或他物或金刃，依律立限状花押", "agent": "官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "取有身家及殴人亲属等的保状，本犯领殴伤人医治，领状附卷", "agent": "官", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "保辜限内平复免罪，限满不平复而死依律分别拟罪", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
]
