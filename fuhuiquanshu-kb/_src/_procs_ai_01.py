# -*- coding: utf-8 -*-
"""卷01 PROC_RECORDS（拆分自 multi）。"""
RECORDS = [
    {"item_id": "01-008", "name": "发谕单流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "命下之日即书谕单一纸", "agent": "官", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "附提塘报房邮去（近京本处探马至则发马夫赍去）", "agent": "提塘报房", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "各房开造简明须知册并赋役全书", "agent": "各房", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "头接赍送查阅", "agent": "头接", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "01-012", "name": "待接役流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "谕单既到本治吏书头役公议佥拨赍红批迎接", "agent": "吏书头役", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "照批点名令出安歇", "agent": "官", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "次日按班分别犒劳酒饭赏银给与批回遣发回县", "agent": "官", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "或便道至家凭限尚远未即临任亦应使之先回，届期于本境迎接", "agent": "官", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "01-015", "name": "畵凭领凭流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "命下半月后赴吏科畵凭（红手揭写脚色投吏部并选司，具脚色手本互结供状京官印结投科）", "agent": "官", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "于凭册书一押是谓畵凭", "agent": "吏科", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "又半月赴吏部领凭（写领状一纸脚色二本先投选司）", "agent": "吏部", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "凭给入手详看明白如有伤损洗补即当官禀明或求葢印", "agent": "官", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "凭用绢幅包好护以油纸置缎囊悬项下暗置胸前夜置枕畔", "agent": "官", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "01-016", "name": "辞朝谢恩流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "领凭后用红单照脚色写投鸿胪寺报名", "agent": "官", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "逢五报名逢十引入朝午门外谢恩", "agent": "鸿胪寺", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "如遇皇上升殿先于午门外齐集，用职名投河南道鸿胪寺吏部", "agent": "官", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "入左掖门于文官东班坐，听螭头传呼起立，行三跪九叩头", "agent": "官", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "礼毕仍归班俟饮茶散", "agent": "官", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "01-020", "name": "起程赴任流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "束装时记行李细单编号字号，另记行李点单", "agent": "官", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "就道时按号派人押行，每至宿店按号查点", "agent": "仆役", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "濒行预带手本职名单帖，亲友差人候送者夹原帖璧还", "agent": "官", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "途次取经过州县患病印结粘连医生店家甘结为据（照凭限约在中途）", "agent": "官", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "到任后于缴凭文书声说明白将印结连凭申", "agent": "官", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
]
