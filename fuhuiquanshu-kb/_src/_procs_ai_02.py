# -*- coding: utf-8 -*-
"""卷02 莅任部一·流程 PROC（4 条）。"""
RECORDS = [
    {"item_id": "02-006", "name": "受印流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "新官入境日，委本州县佐贰官同吏房送印至公馆", "agent": "佐贰官吏房", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "设案居中奉印案上，新官肃立眼同佐贰官吏房送匙验封启匣", "agent": "官", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "请印验封呈印，详看背面篆文四角及柄，记明嵌补缺损几处", "agent": "官", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "照旧封固，同印匙亲受讫", "agent": "官", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "取吏房眼同验明嵌补缺损若干处甘结存案（甘结存宅内防日后上司查验）", "agent": "吏房", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "02-007", "name": "到任受事流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "上任日择定某时穿吉服（或穿朝服省谢恩再换）诣城隍神前行祭礼，牲帛照例备办，礼生赞唱行献礼，宣读誓文并帛焚化", "agent": "官", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "乘舆执事鼓乐前导至衙署大门内，祭仪门土地祠毕", "agent": "官", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "从中道步至香案前望阙谢恩，与僚属拱手上堂升公座", "agent": "官", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "僚属照位次坐，阴阳生报时，皂隶禀排衙，吏书以次书押，书公座（先首领佐贰而后印官）", "agent": "官", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "承送到任文书佥押，直印吏禀开印请匙，将所佥文书用印封讫", "agent": "官", "agent_ent_ids": [], "next": "s6"},
         {"step_id": "s6", "seq": 6, "text": "前官或署篆持帖送仓库监狱城门等钥匙，该经承吏当堂逐一验明交割", "agent": "经承吏", "agent_ent_ids": [], "next": "s7"},
         {"step_id": "s7", "seq": 7, "text": "吏房率各房投逓县志县图须知，书门皂快各人役依次参谒，佐贰官谒贺堂前行交拜礼，首领官庭参礼", "agent": "吏房", "agent_ent_ids": [], "next": "s8"},
         {"step_id": "s8", "seq": 8, "text": "掩门乃退，直印吏承印前导，门子捧匙匣印牌各钥随进交内衙", "agent": "官", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "02-010", "name": "缴凭流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "上任之日将部凭细加检点照式誊写一张收存", "agent": "官", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "照例申缴该衙门", "agent": "官", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "转申布政司", "agent": "布政司", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "司详抚院", "agent": "布政司", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "咨缴部科查销", "agent": "部科", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "02-014", "name": "买办流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "置买办簿一扇托亲信老成人经管，将明日需用菜蔬先日晚开写簿上", "agent": "经管人", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "送本官验明朱发", "agent": "官", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "买办照簿买进，某物下注用银若干计本日买价未行共结一总", "agent": "买办", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "上班之日买办具价领，朱封纹银若干同头役面给，其领粘卷名曰买办领银卷", "agent": "头役", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "买完之日将用过价银存剩若干具结状，并无赊取户行短少价值字样与剩银同缴经管人查明附卷", "agent": "买办", "agent_ent_ids": [], "next": "s6"},
         {"step_id": "s6", "seq": 6, "text": "如遇冲途供应过差用印票发买，本行户当堂具领即照时给价销票", "agent": "行户", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
]
