# -*- coding: utf-8 -*-
"""卷09 编审部·结构化四维（LGR 文簿台账 5 条 + ACT 1 条 + FRD 2 条 + TME 2 条）。"""
RECORDS = [
    {"item_id": "09-006", "dim": "LGR", "lgr_type": "ledger", "name": "自报册", "content": "前届自报改正者另立自报册一样二本一存房一存宅以便查考", "target": "", "confidence": "high"},
    {"item_id": "09-007", "dim": "LGR", "lgr_type": "ledger", "name": "推收小册", "content": "本届推收另立一推收小册送署备查；推收业户具呈并契送验，本官批准发房给一印票付业主，同两处里书并册房眼同此推彼收，将姓名田地数自对明登册上钤里书推收图记并册书业户花押", "target": "", "confidence": "high"},
    {"item_id": "09-008", "dim": "LGR", "lgr_type": "ledger", "name": "编审册单", "content": "册者里书所造本届编审之册也，单者户长开报本届编审之单也；造册单须分各里里分各甲甲分各户，先查上届丁粮实在若干实征银米若干，接开新收田地若干应增征银米若干；实在丁粮实征银米既清则据之以定升擦", "target": "", "confidence": "high"},
    {"item_id": "09-011", "dim": "LGR", "lgr_type": "ledger", "name": "攒造审册（四柱）", "content": "将逐日审过各里甲红单照造册稿分立旧管新收开除实在四柱；各甲首系一本里总数各里首系一本图总数各图首系一合县总数俱照四柱开造；磨对与红单相合送内衙磨对无差取具总里书册房等甘结存案方发房攒造，一样若干本除申送该衙门外一本存房一本存署备查", "target": "", "confidence": "high"},
    {"item_id": "09-010", "dim": "LGR", "lgr_type": "ledger", "name": "红单", "content": "投审尸单除实在田地银米外，如新收田地银米与所定丁则相符即用朱笔将升过银米丁则连点而下，新推擦减之数亦朱笔如前连点；其新丁与逃亡老绝之丁俱用朱笔于逐名下亲书增除，仍查新丁若干除免若干书总数于单后判日将本日审过户单若干张封押随带内衙登记", "target": "", "confidence": "high"},
    {"item_id": "09-003", "dim": "ACT", "act_type": "clerk_role", "name": "户长职责", "content": "报丁户长多系积年奸逓土棍钻充希图取利——申饬里胥之后即传各图里长以十甲长为户长，如甲长中不符公论者另举殷实老成补之；严行切谕令其按甲逐户据实开报", "target": "", "confidence": "high"},
    {"item_id": "09-002", "dim": "FRD", "frd_type": "abuse", "name": "里书编审作奸", "content": "粮房里书遇编审届期是一场大生意，预先勾通户长受贿分肥——田粮以多作少人丁卖富栽贫牢不可破", "target": "", "confidence": "high"},
    {"item_id": "09-001", "dim": "FRD", "frd_type": "abuse", "name": "奸豪诡寄飞洒诸弊", "content": "花立户名（产本一人管业乃立数人诡名）、诡寄别里（产本坐落一里乃于数里立户）、飞洒各户（将丁产应办银粮分派他人银粮之内使彼代纳）、移换斗则（移甲之重换乙之轻）、脱漏顷亩（产业竟不入册隐地漏粮）、冐栽田地（将已产暗造他人名下害彼代纳）", "target": "", "confidence": "high"},
    {"item_id": "09-008", "dim": "FRD", "frd_type": "abuse", "name": "立局亲审各弊", "content": "棍状顶冐应点、破衣轮流穿换妆扮穷人、利口能言骋其巧辩希图擦免、新报成丁不因粮起止编下下却诡寄收粮名下、幼小子女搪塞隐漏成丁、假冐寄庄指称地差", "target": "", "confidence": "high"},
    {"item_id": "09-001", "dim": "TME", "tme_type": "deadline", "name": "编审周期", "content": "编审之时有二：一在十年大造将钱粮户口攒造黄册进呈御览，一在五年均役清核丁差；今黄册停造惟五年均役直省遵行无异", "target": "", "confidence": "high"},
    {"item_id": "09-006", "dim": "TME", "tme_type": "deadline", "name": "自首限期", "content": "所有前届飞洒诡寄及妄增丁粮并本地积习锢陋诸弊逐欵开列，许三日内开单自首免其前罪", "target": "", "confidence": "high"},
]
