# -*- coding: utf-8 -*-
"""卷03 莅任部二·流程 PROC（3 条）。"""
RECORDS = [
    {"item_id": "03-001", "name": "郯城到任整饬流程（三日点卯）",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "未出京之先廉得衙蠹土豪，以次犒迎役即日令回不留一役", "agent": "官", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "入境先诣驿局验马：锁兵书马牌责三十，道快王某责二十，次日申详本道修禀谢罪", "agent": "官", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "十九日城隍庙斋宿，二十日谒神焚誓，上任入署", "agent": "官", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "命皂头选惯行刑皂隶八名并毛头大板十片进验", "agent": "官", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "三日行香视事，出示次日午堂各役过堂点卯：卯簿详注年貌籍贯住址着役日期经管某事", "agent": "官", "agent_ent_ids": [], "next": "s6"},
         {"step_id": "s6", "seq": 6, "text": "点时闭东西两角门，各役挨班逐名至阶下跪，念年貌籍贯与卯簿同否，相面貌良恶默记", "agent": "官", "agent_ent_ids": [], "next": "s7"},
         {"step_id": "s7", "seq": 7, "text": "点毕数其罪，按罪轻重酌责，共受杖二十余人，逾旬毙者一，杖而黜革者五（积年头役执掌科书豪棍党羽）", "agent": "官", "agent_ent_ids": [], "next": "s8"},
         {"step_id": "s8", "seq": 8, "text": "更进其余申儆，令改过自新；钱谷刑名严为法制使无弊窦", "agent": "官", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "03-003", "name": "盘库流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "先请前任及佐贰等官俱至，然后诣库门序坐", "agent": "官", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "驱闲役尽出仪门外，皂隶把定两角门，设长案天平南向", "agent": "官", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "库书展库簿，将存库银两查明数目是否与交代册同，仍逐平弹凖纹足（银低潮着官银匠估确补色）", "agent": "库书", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "赃械等物逐件验明与库贮簿点过，判日存库，库书另造盘过银两簿赃械簿送宅", "agent": "官", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "取库书并无隐漏存剩在库物件甘结存案，亲身入库内上下墙壁地间用火通照再无别物方散", "agent": "官", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "03-005", "name": "交盘清查流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "先查全书会计（钱粮额编以赋役全书为据，杂项钞课逐款要查，额征以部核由单及司核会计册为据）", "agent": "官", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "查征收：交代册四柱管收除在照柱先查；接征民欠吊上手交代民欠册并粮里认完花户册查对；本任征收吊流水日收串根与拆封库簿对", "agent": "官", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "查起解：与会计合则对批回，批向光处细照银数上年月无洗补痕迹，无批回者唤问经承原解之人不得作准开销申请追掣", "agent": "官", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "查存留：起解查验批回，应支给对领状，重领及无款项擅发掣回不准开销；各项支给于前官离任日扣住不得过领", "agent": "官", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "查民欠：与实征册查对，欠户花名与交代未完相合令粮里具实在民欠甘结准作接征；逃亡虚报者详请经手赔补", "agent": "官", "agent_ent_ids": [], "next": "s6"},
         {"step_id": "s6", "seq": 6, "text": "查存库：交兑不足，一年钱粮通盘打算，除民欠可抵解外其余无着即系侵亏详请经手赔补", "agent": "官", "agent_ent_ids": [], "next": "s7"},
         {"step_id": "s7", "seq": 7, "text": "各项查明无弊俱取各房经管甘结粘连用印成卷方可交代", "agent": "官", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
]
