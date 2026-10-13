# -*- coding: utf-8 -*-
"""卷19 刑名部九·流程 PROC（4 条）。"""
RECORDS = [
    {"item_id": "19-001", "name": "烟户造报流程", "steps": [
        {"seq": 1, "text": "州县初至地方清查烟户为第一务——烟户男女有数须查其从来仝居久住或曾被掠及远来", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "邻佑甲长逐户查明有则报官亲自拘讯，如并无此等具结保长保长查明方具结州县存案", "agent": "甲长", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "平日偶有而生至家邻佑甲长察其语音装朿举止动静妇人有无重穿耳孔解放其脚，可疑即报保长", "agent": "甲长", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "保长即报官拘讯真则审明起解", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "19-001", "name": "审逃流程", "steps": [
        {"seq": 1, "text": "捕壮地方拿获逃人严谕实时呈报本官宜实时亲审——先问捕地某日在何处拿获何以知是逃人拿获之时有无行李器物并有无同行党伴", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "详问被掠/卖身/逃走年月旗色佐领主名住址官职、拐带花费、先后住地窝家姓名住址、租房雇工中保妻子子女等情由", "agent": "官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "一一问明将逃人收监，查本地方旧例或径解督捕或申详本府复审转解司院领文逓解", "agent": "官", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "解逃文中看语不可说煞——但据逃人口供叙完略增一二活语申解；逃人不可加刑", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "19-001", "name": "起解逓解流程", "steps": [
        {"seq": 1, "text": "逃人审明即宜起解——逃人起解时当堂验批唤名例加杻锁，一犯二解须要有身家房产之正身佥解不得穷役顶替", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "长解之外经过州县添差逓解者其添差人数即照原批之数添解以解到前州县交割", "agent": "官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "逓解一到官当堂照批文点明人数立刻具文差的当人役解交前途取收管回报——若解到天晚不便点交须俟明早点验差解", "agent": "官", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "如逃人在来处患病当官验明真病即取长解添解患病情由具结存案叙入前途文内，前途亦取甘结存案方给收管", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "19-002", "name": "鞫奸流程", "steps": [
        {"seq": 1, "text": "详阅告状内情由与供之口词虚实——先察本夫本妇词色是否义愤激切，再观被告是否凶悍及词色有无沮丧", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "详讯证佐被告素行及强奸有无可确据，细鞫强犯与被奸有名分否、何时何地、有无挟持凶器、毁伤身体损裂下衣、曾否成奸、有无喊救、是否亲夫拿获、有无所遗衣物", "agent": "官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "是强是和真情毕露——果系强奸状情所叙必直切口词所供与状情必吻合，和与强称则状情纽捏口词支离", "agent": "官", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "审奸狱最宜持重庄词肃容推情研讯——妇人进审不得唤近案前低声悄问退去不得定晴目送；奸狱止就本妇审理勿得节外生枝再牵妇女", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
]
