# -*- coding: utf-8 -*-
"""卷06 钱谷部一·流程 PROC（2 条）。"""
RECORDS = [
    {"item_id": "06-002", "name": "完粮收银入柜流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "纳户买棉纸封袋（三寸阔四寸长，每袋止偿纸张工价二文），自将官等称准银数", "agent": "纳户", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "柜吏看明银色纹足（不许执等代称），纳户自封袋口", "agent": "柜吏", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "柜吏于银袋上填明某图里某人完纳某项某限银若干某年月日某字第几号收役某人，随照式登记流水收簿", "agent": "柜吏", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "眼同纳户穿连入柜，随填串票（执照/查截二票）付纳户收执", "agent": "柜吏", "agent_ent_ids": [], "next": "s5"},
         {"step_id": "s5", "seq": 5, "text": "每晚柜吏同流水日收、用过票根并未用串票一齐送宅，票根缴入内衙存算", "agent": "柜吏", "agent_ent_ids": [], "next": "s6"},
         {"step_id": "s6", "seq": 6, "text": "折封之日禀领柜钥当堂拆封，按号查对流水查擦改，拆封后另匣验低潮钱文", "agent": "官", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "06-002", "name": "滚单催征流程",
     "steps": [
         {"step_id": "s1", "seq": 1, "text": "钱粮开征头二限听纳，至三四限完不如数照簿甲分每五户列一单挨填各户欠数，分作四限完纳", "agent": "官", "agent_ent_ids": [], "next": "s2"},
         {"step_id": "s2", "seq": 2, "text": "五户中以欠数最多者为催头，甲长领给，催头逢卯执单赴比", "agent": "催头", "agent_ent_ids": [], "next": "s3"},
         {"step_id": "s3", "seq": 3, "text": "比后又交与下手欠数多者为催头，逐户挨催", "agent": "催头", "agent_ent_ids": [], "next": "s4"},
         {"step_id": "s4", "seq": 4, "text": "单到不照限完纳及卧单不赴比者立即差拿罚完欠数；其余户不照限催头禀拿重责亦罚全完方释；过限再不完枷示仍责全完", "agent": "官", "agent_ent_ids": [], "next": ""},
     ],
     "state_machine": "", "events": [], "confidence": "high"},
]
