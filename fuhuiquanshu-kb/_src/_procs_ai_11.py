# -*- coding: utf-8 -*-
"""卷11 刑名部一·流程 PROC（2 条，覆盖试点残留）。"""
RECORDS = [
    {"item_id": "11-002", "name": "词讼收理流程", "steps": [
        {"seq": 1, "text": "三六九告期放告：状人鱼贯而进逐名挨次将状展开亲压桌上，直堂吏点明张数逐张唤名点过，收状完白纸封束朱笔点封", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "本日批阅：验堂封未动折开，不合状式者批明不准，合式者判日批准注承行吏书姓名", "agent": "官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "挂号：内号簿登记朱语原被姓名批语承行差役，内号挂讫副状汇入封套发承发房，承发科挂号方发（外号）", "agent": "官", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "签差：平常婚户发房签差照例均轮（名签掣筩），命盗重案预择老成小心者差遣，差票刻需索填注长条印", "agent": "官", "agent_ent_ids": [], "next": 5},
        {"seq": 5, "text": "拘提：量事难易人之多寡路之远近定确限按期回销，违限摘比，回销注销", "agent": "差役", "agent_ent_ids": [], "next": 6},
        {"seq": 6, "text": "听审：早堂带齐点过照单挂牌次日午堂听审，逐名详问原告被告干证，口供亲看一遍", "agent": "官", "agent_ent_ids": [], "next": 7},
        {"seq": 7, "text": "销差结案：一审即结者原差禀销票收入内衙销号粘卷，取保者原票标取押出取保归结缴票附卷", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
    {"item_id": "11-002", "name": "听审七术流程", "steps": [
        {"seq": 1, "text": "观状时先有成竹于胸：先看原告词内主意输人问罪破绽渗漏处逐句△出人名地名月日□出，次看诉词如何驳他剖说有理无理逐一照前，再看投禀内两家辩论真情渐露", "agent": "官", "agent_ent_ids": [], "next": 2},
        {"seq": 2, "text": "钩：以我意探彼意，姑微以一语钩之看其如何回荅", "agent": "官", "agent_ent_ids": [], "next": 3},
        {"seq": 3, "text": "袭：不受饵仍敷说前词，从他意料不到处诘问之", "agent": "官", "agent_ent_ids": [], "next": 4},
        {"seq": 4, "text": "攻：所对一有空隙即从空隙处连驳之", "agent": "官", "agent_ent_ids": [], "next": 5},
        {"seq": 5, "text": "逼：情巳难掩假作威严拍案大怒命取夹棍吓之，两班牙爪疾呼跃出提摔而下", "agent": "官", "agent_ent_ids": [], "next": 6},
        {"seq": 6, "text": "摄：对干证预瞋目厉容以待择极肯綮处严讯，命加刑彼自连声称吐", "agent": "官", "agent_ent_ids": [], "next": 7},
        {"seq": 7, "text": "合：逐名详问原告供毕令出被告供毕令出干证各问毕令出——所供合与不合可知", "agent": "官", "agent_ent_ids": [], "next": 8},
        {"seq": 8, "text": "挠：众口所供既定不能为彼改移，造证当前仝词共质彼虽有口如簧安能巧鼓于羣言之下", "agent": "官", "agent_ent_ids": [], "next": 0},
    ], "state_machine": "", "events": [], "confidence": "high"},
]
