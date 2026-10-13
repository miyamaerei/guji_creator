# -*- coding: utf-8 -*-
"""卷07 钱谷部二·流程 PROC（2 条）。"""
RECORDS = [
    {"item_id": "07-002", "name": "拆封流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "钱粮每限摘比之后方可拆封；临拆早堂事毕诸务尽却，川堂或后堂将闲人避开，止许一门子远立伺候", "agent": "官", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "库吏管称粮书管算，先验各柜原封锁门未动，然后挨次启拆", "agent": "库吏", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "唱拆某里即持某里收簿呈案，粮书按数号高唱若干号，柜封就线逐封取起，对封簿姓名银数无差", "agent": "粮书", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "库吏放定等陀在星方许放银在盘，逐封对簿号不少方拆开总兑，每封带看银色置银筐内", "agent": "库吏", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "低潮及短少者另放开单托明朱笔点过，拘问补后点销，银封仍归本日所拆数内", "agent": "官", "agent_ent_ids": [], "next": "s6"},
         {"step_id": "s6", "seq": 6, "text": "兑准一平粮书逐平包封，总点所兑与收簿数合，于月日下朱判拆讫二字；拆完一柜柜吏另具拆单，库吏查前次拆单亲填连前共拆银若干逓粘成卷", "agent": "柜吏", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "07-003", "name": "解银掣批流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "应解钱粮该房禀请，批定解某项若干另案放行，然后发批令填；批回须挨号填用，一字不许潦草，照看银数年月无模糊洗补然后葢印", "agent": "官", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "选择殷实老成胥役佥解，取粮库诸人的保；多则移营拨兵护送并遣亲信守法内丁协解；解饷银鞘外蒙生牛皮铁篐密钉", "agent": "官", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "差役管解赴某衙门交收，原约路程以定限期，守候掣批回实收", "agent": "解役", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "比批簿登记，批收获到即于获字上填批已收二字；无已字者限日比较，逾限不掣批回即宜查比", "agent": "官", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "批收掣获置一橱严为封识，候全欵解完挨序月日夹入实收粘连成卷，下用骑缝斜印收贮，待奏销后取该房领状", "agent": "官", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
]
