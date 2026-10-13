# -*- coding: utf-8 -*-
"""卷五 L3 流程层源数据 —— 《明史·职官志》卷五十二。

卷五为军事/卫所/勋爵制度条，可抽流程者为「职掌行」中具步骤性的办事流程：
  条4  都督府掌军旅之事（武职袭替与选授链路）
  条10 锦衣卫掌侍卫缉捕刑狱之事
  条48 都司掌一方之军政
  条51 卫指挥使司军政考选
  条52 千户所管军层级
  条53 卫所编制层级
  条60 土官朝贡征调
"""
VERSION = "1.0"

PROCS = [
    # ---------- 条4 都督府武职选授流程 ----------
    {"slot": 1, "item_id": "05-004", "name": "都督府武职选授与袭替流程", "scope": "选授",
     "steps": [
         {"seq": 1, "text": "都督府掌军旅之事，各领其都司、卫所，以达于兵部",
          "agent": {"text": "五军都督府", "agent_ent_ids": []}, "condition": "军旅之事", "next": [2]},
         {"seq": 2, "text": "凡武职，世官流官、土官袭替、优养、优给，所属上之府，移兵部请选",
          "agent": {"text": "所属", "agent_ent_ids": []}, "condition": "武职袭替", "next": [3]},
         {"seq": 3, "text": "既选，移府，以下之都司、卫所",
          "agent": {"text": "兵部", "agent_ent_ids": []}, "condition": "选授已定", "next": [4]},
         {"seq": 4, "text": "首领官听吏部选授，给由亦如之",
          "agent": {"text": "吏部", "agent_ent_ids": []}, "condition": "首领官选授", "next": []},
     ], "confidence": 0.92},

    # ---------- 条4 出征挂印流程 ----------
    {"slot": 2, "item_id": "05-004", "name": "都督府大征讨挂印流程", "scope": "出征",
     "steps": [
         {"seq": 1, "text": "凡各省、各镇镇守总兵官，副总兵，并以三等真、署都督及公、侯、伯充之",
          "agent": {"text": "兵部", "agent_ent_ids": []}, "condition": "镇守设置", "next": [2]},
         {"seq": 2, "text": "有大征讨，则挂诸号将军或大将军、前将军、副将军印总兵出",
          "agent": {"text": "总兵官", "agent_ent_ids": []}, "condition": "有大征讨", "next": [3]},
         {"seq": 3, "text": "既事，纳之",
          "agent": {"text": "总兵官", "agent_ent_ids": []}, "condition": "事毕", "next": []},
     ], "confidence": 0.92},

    # ---------- 条10 锦衣卫掌事流程 ----------
    {"slot": 3, "item_id": "05-010", "name": "锦衣卫侍卫缉捕刑狱流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "锦衣卫，掌侍卫、缉捕、刑狱之事，恒以勋戚都督领之",
          "agent": {"text": "锦衣卫", "agent_ent_ids": []}, "condition": "未明", "next": [2, 3, 4]},
         {"seq": 2, "text": "凡朝会、巡幸，则具卤簿仪仗，率大汉将军等侍从扈行",
          "agent": {"text": "锦衣卫", "agent_ent_ids": []}, "condition": "朝会、巡幸", "next": []},
         {"seq": 3, "text": "盗贼奸宄，街途沟洫，密缉而时省之",
          "agent": {"text": "锦衣卫", "agent_ent_ids": []}, "condition": "缉捕", "next": []},
         {"seq": 4, "text": "凡承制鞫狱录囚勘事，偕三法司",
          "agent": {"text": "锦衣卫", "agent_ent_ids": []}, "condition": "鞫狱录囚", "next": []},
     ], "confidence": 0.92},

    # ---------- 条48 都司掌军政流程 ----------
    {"slot": 4, "item_id": "05-048", "name": "都司掌一方军政流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "都司，掌一方之军政，各率其卫所以隶于五府，而听于兵部",
          "agent": {"text": "都指挥使司", "agent_ent_ids": []}, "condition": "未明", "next": [2]},
         {"seq": 2, "text": "凡都司并流官，或得世官，岁抚、按察其贤否",
          "agent": {"text": "抚、按", "agent_ent_ids": []}, "condition": "岁察", "next": [3]},
         {"seq": 3, "text": "五岁考选军政而废置之",
          "agent": {"text": "兵部", "agent_ent_ids": []}, "condition": "五岁考选", "next": [4]},
         {"seq": 4, "text": "都指挥使及同知佥事，常以一人统司事，曰掌印，一人练兵，一人屯田，曰佥书",
          "agent": {"text": "都指挥使司", "agent_ent_ids": []}, "condition": "掌印佥书分职", "next": []},
     ], "confidence": 0.92},

    # ---------- 条51 卫指挥使司军政流程 ----------
    {"slot": 5, "item_id": "05-051", "name": "卫指挥使司军政考选流程", "scope": "考察",
     "steps": [
         {"seq": 1, "text": "凡袭替、升授、优给、优养及属所军政，掌印、佥事报都指挥使司",
          "agent": {"text": "卫掌印、佥事", "agent_ent_ids": []}, "condition": "袭替升授", "next": [2]},
         {"seq": 2, "text": "达所隶都督府，移兵部",
          "agent": {"text": "都指挥使司", "agent_ent_ids": []}, "condition": "上报", "next": [3]},
         {"seq": 3, "text": "每岁抚、按察其贤否，五岁一考选军政，废置之",
          "agent": {"text": "抚、按", "agent_ent_ids": []}, "condition": "每岁、五岁", "next": [4]},
         {"seq": 4, "text": "凡管理卫事，惟属掌印、佥书。不论指挥使、同知、佥事，考选其才者充之",
          "agent": {"text": "卫", "agent_ent_ids": []}, "condition": "考选才者", "next": []},
     ], "confidence": 0.92},

    # ---------- 条52 千户所管军流程 ----------
    {"slot": 6, "item_id": "05-052", "name": "千户所管军层级流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "凡军政，卫下于所，千户督百户",
          "agent": {"text": "卫", "agent_ent_ids": []}, "condition": "军政下行", "next": [2]},
         {"seq": 2, "text": "百户下总旗、小旗，率其卒伍以听令",
          "agent": {"text": "百户", "agent_ent_ids": []}, "condition": "层递统辖", "next": [3]},
         {"seq": 3, "text": "其守御千户所，不隶卫，而自达于都司",
          "agent": {"text": "守御千户所", "agent_ent_ids": []}, "condition": "守御千户所特例", "next": [4]},
         {"seq": 4, "text": "凡卫所皆隶都司，而都司又分隶五军都督府",
          "agent": {"text": "都司", "agent_ent_ids": []}, "condition": "统隶归属", "next": []},
     ], "confidence": 0.92},

    # ---------- 条60 土官朝贡征调流程 ----------
    {"slot": 7, "item_id": "05-060", "name": "土官朝贡征调流程", "scope": "朝贡",
     "steps": [
         {"seq": 1, "text": "命因元官授之，稍与约束，定征徭差发之法",
          "agent": {"text": "土官", "agent_ent_ids": []}, "condition": "西南诸蛮夷朝贡", "next": [2]},
         {"seq": 2, "text": "皆因其俗，使之附辑诸蛮，谨守疆土，修职贡，供征调，无相携贰",
          "agent": {"text": "土官", "agent_ent_ids": []}, "condition": "常职", "next": [3]},
         {"seq": 3, "text": "有相仇者，疏上听命于天子",
          "agent": {"text": "土官", "agent_ent_ids": []}, "condition": "有相仇者", "next": []},
     ], "confidence": 0.92},
]
