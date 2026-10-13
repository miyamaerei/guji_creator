# -*- coding: utf-8 -*-
"""卷10 清丈部·流程 PROC（1 条）。"""
RECORDS = [
    {"item_id": "10-001", "name": "清丈自首抽丈流程", "steps": [
        {"seq": 1, "text": "先出示通谕四乡，刊刻丈册式令业户自丈照式填写，晓谕利害（不用印册不照式填写立行拿究）", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "里社乡地率同业户逐亩逐段详细丈量，随丈随填先登草册照填真册送县，丈册每户后写弓手乡地图里等姓名", "agent": "里社乡地", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "业主自丈填册后自具结状投逓，连书乡地里社等姓名并业主花押粘卷存案", "agent": "业户", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "劝令自首：丈原额之外果有多余即行自首止照数起科免其欺隐之罪，以某日为始某日为止", "agent": "官", "agent_ent_ids": [], "next": 5},
        {"seq": 5, "text": "过期不首方行亲掣（抽丈），履亩勘出隐漏除按律科罪外仍追历年籽粒钱粮", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
]
