# -*- coding: utf-8 -*-
"""卷13 刑名部三·流程 PROC（1 条）。"""
RECORDS = [
    {"item_id": "13-001", "name": "监犯病治流程", "steps": [
        {"seq": 1, "text": "监犯有病狱卒即逓病呈，拨医调治，摘取医生是何病症用何汤药结状存案", "agent": "狱卒", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "病尚未愈有亲属者准令亲属一人搜检明白并无夹带放进照看，无亲属者责令仝牢人代为煎药扶持", "agent": "官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "如病故取狱卒同牢各犯医生三面甘结存案，本官入监亲验身尸查问众犯", "agent": "官", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "具文申报该管上司着令掩埋取埋讫结状存案，有亲属者许亲属具领尸结状存案", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
]
