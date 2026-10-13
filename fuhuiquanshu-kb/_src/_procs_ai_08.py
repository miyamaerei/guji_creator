# -*- coding: utf-8 -*-
"""卷08 钱谷部三+杂课部·流程 PROC（2 条）。"""
RECORDS = [
    {"item_id": "08-001", "name": "漕粮收兑流程", "steps": [
        {"seq": 1, "text": "开征之时经收日日在廒仓，多置搧箱斗斛以便速收", "agent": "经收", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "粮户到仓亲纳，仓胥验明米色干净即与平斛收兑，毋许借端留难恣意淋踢", "agent": "仓胥", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "收粮簿照依收银流水循环填写送查，在城打日报存查，粮串依银票用完再发", "agent": "粮房", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "运船到次随到随兑，印官眼同运官亲为掣廒受兑，不得任凭旗甲拣廒及仓胥私拨零分", "agent": "印官", "agent_ent_ids": [], "next": 5},
        {"seq": 5, "text": "兑毕取弁丁印甘结状申报开行日期，催攒远离口岸不得阻塞河路", "agent": "印官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "08-011", "name": "芦课清丈流程", "steps": [
        {"seq": 1, "text": "考志书历稽碑劵按原界而求之，查清芦洲坍涨隐占实况", "agent": "印官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "坍则应豁涨则应升隐占则应报增，清丈所以利升涨以补坍课额无亏而民不偏累", "agent": "印官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "止令本州县印官照例据实清丈（不委官丈量），密芦稀芦泥滩水影草荡各按其等课征", "agent": "印官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
]
