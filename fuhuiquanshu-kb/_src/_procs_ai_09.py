# -*- coding: utf-8 -*-
"""卷09 编审部·流程 PROC（3 条）。"""
RECORDS = [
    {"item_id": "09-001", "name": "编审均役主流程", "steps": [
        {"seq": 1, "text": "先取前届印册勘阅管收除在四柱，查上届实在田土户丁与全书额载相符", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "传集各图里书胥役当堂严饬，传各图里长以十甲长为户长按甲逐户据实开报", "agent": "官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "将审之先大张榜示开列前弊，许三日内开单自首改正", "agent": "官", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "推收业户具呈并契送验，发印票同两处里书册房眼同此推彼收登册钤图记花押", "agent": "官", "agent_ent_ids": [], "next": 5},
        {"seq": 5, "text": "册单分里甲户开造新旧丁粮，送宅磨对无差后发出候审", "agent": "里书户长", "agent_ent_ids": [], "next": 6},
        {"seq": 6, "text": "十日前示期，立局亲审逐户唤问，升擦增除丁粮朱笔点书红单", "agent": "官", "agent_ent_ids": [], "next": 7},
        {"seq": 7, "text": "审后按里逐户出示晓谕升擦增除，许三日呈控", "agent": "官", "agent_ent_ids": [], "next": 8},
        {"seq": 8, "text": "攒造审册照红单立旧管新收开除实在四柱，磨对无差取甘结存案方发房攒造", "agent": "册书", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "09-008", "name": "升擦丁则核算流程", "steps": [
        {"seq": 1, "text": "总计阖县地丁银若干，内丁银若干，计地银若干应派丁银若干", "agent": "里书", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "新收田地若干应增丁若干，按上中下九则派定（如粮银一万两该丁银三千三百两，每粮一石约银一两一钱有奇）", "agent": "里书", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "增粮者既升则减粮者应擦，升以九斗为准擦以一石一斗为准（升宜取多擦宜取少恐有缺额）", "agent": "里书", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "册单于新收新推田粮银米之后按九斗逓加则应升丁若干应增丁银若干，按一石一斗逓减则应擦丁若干应减丁银若干俱预为派造", "agent": "里书", "agent_ent_ids": [], "next": 5},
        {"seq": 5, "text": "各甲造完首户要一里总合十户以定甲合十甲以定里合十里以定图合各图以定一县田地丁粮，务期有增无减方合编审之例", "agent": "里书", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "09-010", "name": "立局亲审流程", "steps": [
        {"seq": 1, "text": "十日前大张告示预示审期，视州县冲僻里分多寡以为迟速，分四乡一日几里预先酌定晓示", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "审局设城隍庙或公馆务须宽大，肃清不许闲杂拥立阶下喧嚷，把门皂隶严行驱逐", "agent": "皂隶", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "审某乡某里某甲，新旧里书册房俱执新旧册单伺候查勘，本甲户长先投户单", "agent": "户长", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "逐户唤问名下田地丁粮是否与户单相符，防顶冐妆穷巧辩诡寄——查出重责", "agent": "官", "agent_ent_ids": [], "next": 5},
        {"seq": 5, "text": "新丁十六岁方许开报，绝丁无田粮者开除，逃亡之丁查有无成丁子弟承粮顶认，老丁年逾六十子报成丁应开除", "agent": "官", "agent_ent_ids": [], "next": 6},
        {"seq": 6, "text": "升过银米丁则朱笔连点，新丁与逃亡老绝之丁朱笔亲书增除，书总数于单后判日封押带内衙登记", "agent": "官", "agent_ent_ids": [], "next": 7},
        {"seq": 7, "text": "各里审毕着里书户长并乡约地方具并无受贿隐漏偏累孤贫甘罪结状存案", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
]
