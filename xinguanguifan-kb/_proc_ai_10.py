# -*- coding: utf-8 -*-
"""10 卷（御灾第八）AI 流程/事件抽取（kg-proc-ai-v1）。original 由打包器从指纹库注入，不手抄。"""
PROCESSES = [
    dict(process_id="XGF-P-000", event_type="御灾赈济", title="陂塘修理", trigger="陂岸塘堰闸损坏",
         timeline=[], steps=[
            dict(step_id="10-001-s1", state="并工", action="即令附近富实居民量力并工修理", agent="富实居民", condition="不可另起民夫及科敛民财", next="10-001-s2"),
            dict(step_id="10-001-s2", state="分修", action="委信实人分投修理", agent="信实人", next="10-001-s3"),
            dict(step_id="10-001-s3", state="呈报", action="若遇大水后具结呈报", agent="官府", next="END"),
         ], next_process="10-002", source="10_卷下_御灾第八.xhtml#条1", derived_from=["10-001"],
         confidence=0.9, analysis="陂塘修理：居民并工→信实人分修→大水后具结。"),
    dict(process_id="XGF-P-000", event_type="御灾赈济", title="火患防护", trigger="旱干之时",
         timeline=["不分昏夜"], steps=[
            dict(step_id="10-002-s1", state="谕火", action="须谕各乡及街坊火烛", agent="官府", next="10-002-s2"),
            dict(step_id="10-002-s2", state="救护", action="倘遇火发不分昏夜，须亲往视，拨人救护", agent="官府", next="10-002-s3"),
            dict(step_id="10-002-s3", state="禁抢", action="仍严禁抢夺", agent="官府", next="END"),
         ], next_process="10-003", source="10_卷下_御灾第八.xhtml#条2", derived_from=["10-002"],
         confidence=0.9, analysis="火患：谕火烛→亲往救护→严禁抢夺。"),
    dict(process_id="XGF-P-000", event_type="御灾赈济", title="灾伤开报踏勘", trigger="遇灾伤",
         timeline=[], steps=[
            dict(step_id="10-003-s1", state="告示", action="须出告示省谕被灾人民，将本户所种田粮委被灾者逐一开报四至土名及该免粮数，具告以凭", agent="被灾人民", next="10-003-s2"),
            dict(step_id="10-003-s2", state="查算", action="附簿查算，总撒相同即与申闻上司", agent="官府", next="10-003-s3"),
            dict(step_id="10-003-s3", state="踏勘", action="亦于亲自履亩，或门点踏勘", agent="官府", condition="毋凭里老总报作弊", next="END"),
         ], next_process="10-004", source="10_卷下_御灾第八.xhtml#条3", derived_from=["10-003"],
         confidence=0.9, analysis="灾伤勘报：开报四至免粮→附簿查算→申闻上司→履亩踏勘。"),
    dict(process_id="XGF-P-000", event_type="御灾赈济", title="勘灾罚谷济贫", trigger="踏勘灾伤之时",
         timeline=[], steps=[
            dict(step_id="10-004-s1", state="押带", action="就将该问轻犯有力押带，遇假就问", agent="官府", next="10-004-s2"),
            dict(step_id="10-004-s2", state="罚谷", action="即于各犯名下量情罚谷或米", agent="官府", next="10-004-s3"),
            dict(step_id="10-004-s3", state="给贫", action="给被灾贫民", agent="官府", next="END"),
         ], next_process="10-005", source="10_卷下_御灾第八.xhtml#条4", derived_from=["10-004"],
         confidence=0.85, analysis="勘灾兼罚：押带轻犯→遇假就问→罚谷米济贫。"),
    dict(process_id="XGF-P-000", event_type="御灾赈济", title="荒田开垦", trigger="遇有荒芜田地",
         timeline=["三年之后"], steps=[
            dict(step_id="10-005-s1", state="召垦", action="里长须要及时召令附田人户开垦耕种", agent="里长", next="10-005-s2"),
            dict(step_id="10-005-s2", state="纳粮", action="其纳粮待三年之后成熟", agent="附田人户", next="10-005-s3"),
            dict(step_id="10-005-s3", state="佃种", action="或逃户不行复业，量情派与收银，仍与佃种", agent="官府", next="10-005-s4"),
            dict(step_id="10-005-s4", state="罪里长", action="如违里长当罪税租，俱看附田之人", agent="官府", next="END"),
         ], next_process="10-006", source="10_卷下_御灾第八.xhtml#条5", derived_from=["10-005"],
         confidence=0.88, analysis="荒田开垦：召垦→三年纳粮→逃户佃种→违者罪里长。"),
    dict(process_id="XGF-P-000", event_type="御灾赈济", title="水塌覆勘", trigger="水塌以压田土",
         timeline=[], steps=[
            dict(step_id="10-006-s1", state="自写", action="须令该户自写四至田叚地方及该陪粮，呈告以凭", agent="田户", next="10-006-s2"),
            dict(step_id="10-006-s2", state="覆勘", action="查算覆勘", agent="官府", condition="不可差委他官", next="END"),
         ], next_process="10-007", source="10_卷下_御灾第八.xhtml#条6", derived_from=["10-006"],
         confidence=0.85, analysis="水塌覆勘：该户自写四至→查算覆勘，禁委他官。"),
    dict(process_id="XGF-P-000", event_type="御灾赈济", title="捕蝗给赏", trigger="蝗虫害苗",
         timeline=[], steps=[
            dict(step_id="10-007-s1", state="告示", action="须出告示，许诸人不拘多少捕来", agent="诸人", next="10-007-s2"),
            dict(step_id="10-007-s2", state="给赏", action="量类给赏米谷", agent="官府", next="END"),
         ], next_process="10-008", source="10_卷下_御灾第八.xhtml#条7", derived_from=["10-007"],
         confidence=0.85, analysis="捕蝗：告示许捕→量类给赏。"),
    dict(process_id="XGF-P-000", event_type="缉捕防盗", title="防盗防讹", trigger="闻境内有盗贼妖邪讹言",
         timeline=[], steps=[
            dict(step_id="10-008-s1", state="省谕", action="须先省谕平日有见识富家人户", agent="官府", next="10-008-s2"),
            dict(step_id="10-008-s2", state="防守", action="各于交界地方传晓防守", agent="富家人户", condition="不可容令惑众", next="END"),
         ], next_process="10-009", source="10_卷下_御灾第八.xhtml#条8", derived_from=["10-008"],
         confidence=0.88, analysis="防盗防讹：省谕富家→交界传晓防守。"),
    dict(process_id="XGF-P-000", event_type="御灾赈济", title="祈祷雨泽", trigger="祈祷雨泽",
         timeline=[], steps=[
            dict(step_id="10-009-s1", state="省谕", action="但当省谕耆宿、生员、官吏、僧道，躬行早领祝祷", agent="耆宿/生员/官吏/僧道", condition="不可点集里老人等行礼", next="10-009-s2"),
            dict(step_id="10-009-s2", state="放归", action="其它役放归，自行救济田业", agent="官府", next="END"),
         ], next_process="10-010", source="10_卷下_御灾第八.xhtml#条9", derived_from=["10-009"],
         confidence=0.88, analysis="祈祷雨泽：省谕祝祷→役夫放归救济田业。"),
    dict(process_id="XGF-P-000", event_type="缉捕防盗", title="缉盗挨访", trigger="贼盗生发",
         timeline=[], steps=[
            dict(step_id="10-010-s1", state="挨究", action="先于地方开张赌博、淫宰牛马、遭充警迹人家挨究不获", agent="官府", next="10-010-s2"),
            dict(step_id="10-010-s2", state="挨访", action="然后将附近地方内挨访", agent="官府", next="10-010-s3"),
            dict(step_id="10-010-s3", state="邻里", action="仍要省谕邻里跟寻□路", agent="邻里", next="10-010-s4"),
            dict(step_id="10-010-s4", state="分巡", action="如窃五里内挨究，强盗于十里内巡捕", agent="官府", condition="违者治罪；亦不可泛罪总甲", next="END"),
         ], next_process="10-011", source="10_卷下_御灾第八.xhtml#条10", derived_from=["10-010"],
         confidence=0.88, analysis="缉盗：赌淫之家挨究→附近挨访→邻里跟寻→窃五里盗十里。"),
    dict(process_id="XGF-P-000", event_type="缉捕防盗", title="侵损告理", trigger="盗掠禾稻及放火决水",
         timeline=[], steps=[
            dict(step_id="10-011-s1", state="指名", action="须省令被害人将来与仇隙者指名告理以凭", agent="被害人", next="10-011-s2"),
            dict(step_id="10-011-s2", state="惩治", action="查审惩治", agent="官府", condition="不可因无指害不与受理", next="END"),
         ], next_process="10-012", source="10_卷下_御灾第八.xhtml#条11", derived_from=["10-011"],
         confidence=0.88, analysis="侵损告理：被害人指名→查审惩治，禁不受理。"),
    dict(process_id="XGF-P-000", event_type="缉捕防盗", title="窃盗分等究治", trigger="窃盗",
         timeline=[], steps=[
            dict(step_id="10-012-s1", state="初犯", action="窃盗初犯者依律究治", agent="官府", next="10-012-s2"),
            dict(step_id="10-012-s2", state="屡犯", action="若屡犯者取定供招，牢固镣杻押发被害之处，各行笞责，呈报收减赃", agent="官府", condition="初犯不可打死，须屡犯", next="END"),
         ], next_process="10-013", source="10_卷下_御灾第八.xhtml#条12", derived_from=["10-012"],
         confidence=0.9, analysis="窃盗分等：初犯依律→屡犯镣杻笞责，打死仅限屡犯。"),
    dict(process_id="XGF-P-000", event_type="缉捕防盗", title="防盗告示", trigger="盗贼生发去处",
         timeline=[], steps=[
            dict(step_id="10-013-s1", state="告示", action="大写“此处有贼”四字告示，以便众知防戒", agent="官府", next="10-013-s2"),
            dict(step_id="10-013-s2", state="告鸣", action="若遇失贼虽无指实，亦须告鸣，追问地方", agent="官府", next="END"),
         ], next_process="", source="10_卷下_御灾第八.xhtml#条13", derived_from=["10-013"],
         confidence=0.85, analysis="防盗告示：大字示众→失贼告鸣追问。"),
]
EVENTS = []
