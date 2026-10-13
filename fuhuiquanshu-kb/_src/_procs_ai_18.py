# -*- coding: utf-8 -*-
"""卷18 刑名部八·流程 PROC（2 条）。"""
RECORDS = [
    {"item_id": "18-001", "name": "起赃流程", "steps": [
        {"seq": 1, "text": "问官审出真盗供有真赃为失主报单所有之物，讯明本盗赃在何处（在家/寄顿/典铺）", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "遣捕役起赃须严谕禁止搜抢奸淫，差同庄地眼看起赃", "agent": "官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "当官令事主识认原是所失之物，将本赃挂小牌注明起获某盗之赃，令本盗照例画供候拟", "agent": "官", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "着庄地具结捕役并无抢奸等弊并捕役自认甘结存案；余赃登记暂伫库内俟定案后有主给主无主八官", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "18-001", "name": "土番编伍流程", "steps": [
        {"seq": 1, "text": "廉得渠魁（如西乡巨盗白五），密召至署，令其开列乡中谁强谁窃", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "先令渠魁具自认改过自新甘结并亲族邻佑甲长庄地各保结存案，着其拘唤所开者三日内俱集", "agent": "官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "各讯其所为，唤失主质讯果真皆宥勿治，录其所供行窃之事于卷，照取认保结状编为土番", "agent": "官", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "以渠魁为土番之总，居址相近者五人内以才具出众者一人为伍长，当堂给花红赏赐；四乡皆设总伍", "agent": "官", "agent_ent_ids": [], "next": 5},
        {"seq": 5, "text": "每朔望总伍率众赴县唱名点卯，四门置簿稽查出入，一月不时密查违犯立拿重究", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
]
