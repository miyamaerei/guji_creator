# -*- coding: utf-8 -*-
"""卷04 莅任部三·流程 PROC（1 条）。"""
RECORDS = [
    {"item_id": "04-010", "name": "书札酬荅流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "本治乡绅投书：阴阳生不得传进，候堂事毕先禀着来使当堂亲投", "agent": "阴阳生", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "邻邑同寅邻绅远友差人投书：柬房置簿挨次登号，注明某月日某处差投书一封，先具禀单讨示", "agent": "柬房", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "来书封面于挂号时记某年月日某人札，发起草之人问明荅意具草送阅", "agent": "官", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "具草送阅后发写人誊正，誊完并原书送覆阅，方用图章封实", "agent": "写人", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "应付柬房者付柬房，应付来使者付来使；来使或送下处米面下程或留住内衙或送路费", "agent": "官", "agent_ent_ids": [], "next": "s6"},
         {"step_id": "s6", "seq": 6, "text": "回书临发仍登号，前件下注某日发回书讫用销号小戳；来书每月一束粘挂票签记明月分收贮，回书藁置簿誊录", "agent": "柬房", "agent_ent_ids": [], "next": "s7"},
         {"step_id": "s7", "seq": 7, "text": "年终或管理人更换，原书并草藁录册俱送官内查收免落人手以为把柄", "agent": "官", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
]
