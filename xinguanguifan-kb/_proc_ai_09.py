# -*- coding: utf-8 -*-
"""09 卷（礼仪第七）AI 流程/事件抽取（kg-proc-ai-v1）。original 由打包器从指纹库注入，不手抄。"""
PROCESSES = [
    dict(process_id="XGF-P-000", event_type="祭祀仪礼", title="家礼省谕", trigger="文公家礼颁行",
         timeline=[], steps=[
            dict(step_id="09-001-s1", state="省谕", action="须省谕里老各要遵奉", agent="官府", condition="其尸棺暴露、火作斋醮俱律法所禁", next="END"),
         ], next_process="09-002", source="09_卷下_礼仪第七.xhtml#条1", derived_from=["09-001"],
         confidence=0.85, analysis="家礼颁行：省谕里老遵奉，尸棺暴露斋醮为禁。"),
    dict(process_id="XGF-P-000", event_type="祭祀仪礼", title="习仪拜牌", trigger="习仪拜牌",
         timeline=[], steps=[
            dict(step_id="09-002-s1", state="定监", action="定礼生分投监", agent="官府", next="09-002-s2"),
            dict(step_id="09-002-s2", state="责吏", action="如礼生不循礼、先后不齐者，先责礼房该吏", agent="官府", condition="不许分外生事", next="END"),
         ], next_process="09-003", source="09_卷下_礼仪第七.xhtml#条2", derived_from=["09-002"],
         confidence=0.85, analysis="习仪拜牌：定礼生分监→违礼责礼房吏。"),
    dict(process_id="XGF-P-000", event_type="祭祀仪礼", title="救护行礼", trigger="救护",
         timeline=[], steps=[
            dict(step_id="09-003-s1", state="告示", action="须告示僚属，拘集僧道至期行礼", agent="官府", next="09-003-s2"),
            dict(step_id="09-003-s2", state="巡视", action="仍令地方总甲巡视，莫容闲人喧哗", agent="总甲", next="END"),
         ], next_process="09-004", source="09_卷下_礼仪第七.xhtml#条3", derived_from=["09-003"],
         confidence=0.85, analysis="救护行礼：告示拘集→总甲巡视禁喧哗。"),
    dict(process_id="XGF-P-000", event_type="祭祀仪礼", title="行礼齐集", trigger="习仪拜牌救护等项",
         timeline=[], steps=[
            dict(step_id="09-004-s1", state="请报", action="有乡宦位高者令该里长请报官；小者告示知悉", agent="里长", next="09-004-s2"),
            dict(step_id="09-004-s2", state="齐集", action="务查点齐集行礼", agent="官府", next="END"),
         ], next_process="09-005", source="09_卷下_礼仪第七.xhtml#条4", derived_from=["09-004"],
         confidence=0.8, analysis="行礼齐集：位高里长请报/位小告示→查点齐集。"),
    dict(process_id="XGF-P-000", event_type="祭祀仪礼", title="迎春", trigger="迎春",
         timeline=[], steps=[
            dict(step_id="09-005-s1", state="从容", action="迎春乃百姓乐事，宜从容为之", agent="官府", next="09-005-s2"),
            dict(step_id="09-005-s2", state="禁派", action="其春花、春杖所费不多，不可分派里甲", agent="官府", next="END"),
         ], next_process="09-006", source="09_卷下_礼仪第七.xhtml#条5", derived_from=["09-005"],
         confidence=0.85, analysis="迎春：从容为之→春花春杖禁分派里甲。"),
    dict(process_id="XGF-P-000", event_type="祭祀仪礼", title="乡饮酒掌礼", trigger="乡属乡饮酒",
         timeline=[], steps=[
            dict(step_id="09-006-s1", state="掌礼", action="须令教读掌礼，毕日回话", agent="教读", next="END"),
         ], next_process="09-007", source="09_卷下_礼仪第七.xhtml#条6", derived_from=["09-006"],
         confidence=0.8, analysis="乡饮酒：令教读掌礼毕日回话。"),
    dict(process_id="XGF-P-000", event_type="祭祀仪礼", title="祭祀采买", trigger="凡遇祭祀",
         timeline=["先期"], steps=[
            dict(step_id="09-007-s1", state="查案", action="先期查照旧案价值支钱", agent="官府", next="09-007-s2"),
            dict(step_id="09-007-s2", state="收买", action="与牙行收买牲口等项，完算以备公用", agent="牙行", condition="不可逼勒赊买及容情贵买", next="END"),
         ], next_process="09-008", source="09_卷下_礼仪第七.xhtml#条7", derived_from=["09-007"],
         confidence=0.88, analysis="祭祀采买：查旧案→牙行收买，禁逼勒贵买。"),
    dict(process_id="XGF-P-000", event_type="祭祀仪礼", title="祭坛诵经", trigger="祭坛",
         timeline=["自朝至暮"], steps=[
            dict(step_id="09-008-s1", state="诵经", action="令所属僧道分坛诵经，自朝至暮", agent="僧道", next="09-008-s2"),
            dict(step_id="09-008-s2", state="羹饮", action="祭毕分与羹饮", agent="官府", next="END"),
         ], next_process="09-009", source="09_卷下_礼仪第七.xhtml#条8", derived_from=["09-008"],
         confidence=0.8, analysis="祭坛：僧道分坛诵经→祭毕分羹饮。"),
    dict(process_id="XGF-P-000", event_type="祭祀仪礼", title="庙赛检束", trigger="祭神庙赛",
         timeline=[], steps=[
            dict(step_id="09-009-s1", state="分处", action="小处则当禁止；大处人众不可遏者，须与会赛日差人检朿", agent="官府", next="09-009-s2"),
            dict(step_id="09-009-s2", state="收香", action="收其香钱公用，勿容会首克落", agent="官府", next="END"),
         ], next_process="09-010", source="09_卷下_礼仪第七.xhtml#条9", derived_from=["09-009"],
         confidence=0.85, analysis="庙赛：小处禁/大处检束→香钱公用禁克落。"),
    dict(process_id="XGF-P-000", event_type="祭祀仪礼", title="淫祠改造", trigger="淫祠",
         timeline=[], steps=[
            dict(step_id="09-010-s1", state="量改", action="淫祠不必悉行拆毁，须量地方改为公廨社学等项", agent="官府", next="END"),
         ], next_process="09-011", source="09_卷下_礼仪第七.xhtml#条10", derived_from=["09-010"],
         confidence=0.85, analysis="淫祠改造：不悉拆，量改公廨社学。"),
    dict(process_id="XGF-P-000", event_type="祭祀仪礼", title="禁僧省谕", trigger="禁僧",
         timeline=[], steps=[
            dict(step_id="09-011-s1", state="省谕", action="先须省谕地方禁约", agent="官府", next="09-011-s2"),
            dict(step_id="09-011-s2", state="问罪", action="不许纵容妇人入寺烧香、听讲经会；如违先将地方问罪", agent="官府", next="END"),
         ], next_process="09-012", source="09_卷下_礼仪第七.xhtml#条11", derived_from=["09-011"],
         confidence=0.88, analysis="禁僧：省谕地方→违者问罪，禁纵妇入寺。"),
    dict(process_id="XGF-P-000", event_type="旌表举保", title="义夫节妇举保", trigger="举保义夫节妇孝子顺孙",
         timeline=[], steps=[
            dict(step_id="09-012-s1", state="密访", action="须自密访，的实着实举保", agent="官府", next="09-012-s2"),
            dict(step_id="09-012-s2", state="禁保", action="若里老呈报及乡宦保者不实，不可保举", agent="官府", next="END"),
         ], next_process="09-013", source="09_卷下_礼仪第七.xhtml#条12", derived_from=["09-012"],
         confidence=0.88, analysis="举保：自密访的实→不实不可保举。"),
    dict(process_id="XGF-P-000", event_type="学校考课", title="学校季考", trigger="学校生儒",
         timeline=["朔望"], steps=[
            dict(step_id="09-013-s1", state="案验", action="须遵上司案验季考，朔望抽签讲论", agent="生儒", next="09-013-s2"),
            dict(step_id="09-013-s2", state="附卷", action="如有不到仰令该吏附卷施行", agent="该吏", next="END"),
         ], next_process="09-014", source="09_卷下_礼仪第七.xhtml#条13", derived_from=["09-013"],
         confidence=0.85, analysis="学校季考：遵案验季考→不到附卷施行。"),
    dict(process_id="XGF-P-000", event_type="优免执照", title="生员乡宦优免", trigger="遇编差役均徭",
         timeline=[], steps=[
            dict(step_id="09-014-s1", state="取产", action="先取本家实在事产，免致临期告扰", agent="官府", next="09-014-s2"),
            dict(step_id="09-014-s2", state="执照", action="每人将应免供丁责令里书开写一帖，付之以为执照", agent="里书", next="END"),
         ], next_process="09-015", source="09_卷下_礼仪第七.xhtml#条14", derived_from=["09-014"],
         confidence=0.88, analysis="优免执照：取实在事产→里书开供丁帖为执照。"),
    dict(process_id="XGF-P-000", event_type="迎送支应", title="乡宦宽待", trigger="乡宦往来",
         timeline=[], steps=[
            dict(step_id="09-015-s1", state="宽待", action="不论存亡、高下、贫富，与些小事情亦宜宽待", agent="官府", next="09-015-s2"),
            dict(step_id="09-015-s2", state="尽礼", action="遇有凶吉须自尽礼", agent="官府", next="END"),
         ], next_process="09-016", source="09_卷下_礼仪第七.xhtml#条15", derived_from=["09-015"],
         confidence=0.8, analysis="乡宦宽待：不论存亡高下贫富宽待→凶吉尽礼。"),
    dict(process_id="XGF-P-000", event_type="祭祀仪礼", title="乡饮仪注", trigger="乡饮",
         timeline=["将晏之先","饮之后"], steps=[
            dict(step_id="09-016-s1", state="敦请", action="须自访实敦请，近县者自请，各乡遣礼生致请", agent="官府/礼生", condition="不许省祭生员混坐寓到", next="09-016-s2"),
            dict(step_id="09-016-s2", state="呈看", action="将晏之先，令具仪注呈看", agent="礼生", next="09-016-s3"),
            dict(step_id="09-016-s3", state="收散", action="即饮之后，候收完器皿，撤去桌椅方散", agent="官府", next="END"),
         ], next_process="09-017", source="09_卷下_礼仪第七.xhtml#条16", derived_from=["09-016"],
         confidence=0.88, analysis="乡饮仪注：访实敦请→仪注呈看→收完器皿方散。"),
    dict(process_id="XGF-P-000", event_type="祭祀仪礼", title="祭祀斋戒巡视", trigger="遇祭祀斋戒",
         timeline=[], steps=[
            dict(step_id="09-017-s1", state="禁办", action="不许粮里人等置酒办饭", agent="官府", next="09-017-s2"),
            dict(step_id="09-017-s2", state="巡视", action="临祭须自巡视祭品，亦先要仪注呈看", agent="官府", next="END"),
         ], next_process="09-018", source="09_卷下_礼仪第七.xhtml#条17", derived_from=["09-017"],
         confidence=0.88, analysis="祭祀斋戒：禁置酒办饭→临祭巡视祭品。"),
    dict(process_id="XGF-P-000", event_type="学校考课", title="季考问策", trigger="季考生员",
         timeline=[], steps=[
            dict(step_id="09-018-s1", state="问策", action="当问境内民情土俗，兴利除害之策，使人各得尽请", agent="生员", condition="愈于询访", next="END"),
         ], next_process="", source="09_卷下_礼仪第七.xhtml#条18", derived_from=["09-018"],
         confidence=0.8, analysis="季考问策：问民情土俗兴利除害。"),
]
EVENTS = []
