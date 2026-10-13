# -*- coding: utf-8 -*-
"""卷17 刑名部七·流程 PROC（2 条）。"""
RECORDS = [
    {"item_id": "17-001", "name": "失事查勘流程", "steps": [
        {"seq": 1, "text": "庄村失事取事主邻佑庄地等口供，道路失事将被盗情由逐项取供", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "印官亲诣其处验明前问逐项是否与所供相合；道路失事亲至旅寓验行李箱垛货物伤痕兵器", "agent": "官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "如有被伤验明所伤轻重曾否中其要害；人少而无凶器无论白昼黑夜俱为抢夺不得作盗刼", "agent": "官", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "勘盗既真方可具文申报，报文以初文为据与报呈字眼斟酌一致", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "17-001", "name": "密擒巨盗流程", "steps": [
        {"seq": 1, "text": "印官问得极真访得极确，除却原告及心腹一二人知之此外并不得与闻", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "潜遣细作预为侦探，印官率领捕快人役借名他事出其不意亲自擒拿（防驻防营弁潜报，秘之）", "agent": "官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "但得正身即行回治，随拿审随审随解，密禀上官迅为定案", "agent": "官", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "罪止及正犯余无所问，家口取保，户牖封鐍责地方佃户看守", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
]
