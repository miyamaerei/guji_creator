# -*- coding: utf-8 -*-
"""【卷01 续】条21–53 L3 流程层源数据"""

PROCS = [
    # ---------- 条44 刑部审谳流程 ----------
    {"slot": 1, "item_id": "01-044", "name": "刑部审谳比议流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "凡军民、官吏及宗室、勋戚丽于法者，诘其辞，察其情伪",
          "agent": {"text": "刑部郎中", "agent_ent_ids": []}, "condition": "丽于法者", "next": [2]},
         {"seq": 2, "text": "傅律例而比议其罪之轻重以请",
          "agent": {"text": "刑部", "agent_ent_ids": []}, "condition": "议罪", "next": [3]},
         {"seq": 3, "text": "诏狱必（会官审录）",
          "agent": {"text": "刑部", "agent_ent_ids": []}, "condition": "诏狱", "next": []},
     ], "confidence": 0.9},

    # ---------- 条36 职方司舆图呈报流程 ----------
    {"slot": 2, "item_id": "01-036", "name": "职方司舆图呈报流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "凡天下地里险易远近，边腹疆界，俱有图本",
          "agent": {"text": "职方司郎中", "agent_ent_ids": []}, "condition": "图本", "next": [2]},
         {"seq": 2, "text": "三岁一报，与官军车骑之数偕上",
          "agent": {"text": "职方司郎中", "agent_ent_ids": []}, "condition": "三岁", "next": []},
     ], "confidence": 0.9},

    # ---------- 条29 主客司朝贡接待流程 ----------
    {"slot": 3, "item_id": "01-029", "name": "主客司朝贡接待流程", "scope": "朝贡接待",
     "steps": [
         {"seq": 1, "text": "诸蕃朝贡，辨其贡道、贡使、贡物远近多寡丰约之数",
          "agent": {"text": "主客司郎中", "agent_ent_ids": []}, "condition": "诸蕃朝贡", "next": [2]},
         {"seq": 2, "text": "以定王若使迎送、宴劳、庐帐、食料之等，赏赉之差",
          "agent": {"text": "主客司郎中", "agent_ent_ids": []}, "condition": "定等", "next": [3]},
         {"seq": 3, "text": "凡贡必省阅之",
          "agent": {"text": "主客司郎中", "agent_ent_ids": []}, "condition": "省阅", "next": []},
     ], "confidence": 0.9},

    # ---------- 条48 营缮司营造流程 ----------
    {"slot": 4, "item_id": "01-048", "name": "营缮司营造督工流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "凡宫殿、陵寝、城郭、坛场、祠庙、仓库、廨宇、营房、王府邸第之役",
          "agent": {"text": "营缮司郎中", "agent_ent_ids": []}, "condition": "营造之役", "next": [2]},
         {"seq": 2, "text": "鸠工会材，以时程督之",
          "agent": {"text": "营缮司郎中", "agent_ent_ids": []}, "condition": "督工", "next": []},
     ], "confidence": 0.9},

    # ---------- 条50 都水司水利修防流程 ----------
    {"slot": 5, "item_id": "01-050", "name": "都水司水利修防流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "水利曰转漕，曰灌田",
          "agent": {"text": "都水司郎中", "agent_ent_ids": []}, "condition": "水利", "next": [2]},
         {"seq": 2, "text": "岁储其金石、竹木、卷埽",
          "agent": {"text": "都水司郎中", "agent_ent_ids": []}, "condition": "岁储", "next": [3]},
         {"seq": 3, "text": "以时修其闸坝、洪浅、堰圩、堤防，谨蓄泄以备（旱潦）",
          "agent": {"text": "都水司郎中", "agent_ent_ids": []}, "condition": "修防", "next": []},
     ], "confidence": 0.9},

    # ---------- 条38 武库司器仗勘合流程 ----------
    {"slot": 6, "item_id": "01-038", "name": "武库司器仗勘合流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "凡内外官军有征行，移工部给器仗，籍纪其数，制敕下各边征发",
          "agent": {"text": "武库司郎中", "agent_ent_ids": []}, "condition": "征行", "next": [2]},
         {"seq": 2, "text": "及使人出关，必验勘合",
          "agent": {"text": "武库司郎中", "agent_ent_ids": []}, "condition": "出关", "next": []},
     ], "confidence": 0.9},

    # ---------- 条49 虞衡司采捕课额流程 ----------
    {"slot": 7, "item_id": "01-049", "name": "虞衡司岁课采捕流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "凡鸟兽之肉、皮革、骨角、羽毛，可以供祭祀、宾客、膳羞之需，礼器、军实之用",
          "agent": {"text": "虞衡司郎中", "agent_ent_ids": []}, "condition": "采捕", "next": [2]},
         {"seq": 2, "text": "岁下诸司采捕。水课禽十八、兽十二，陆课（有差）",
          "agent": {"text": "虞衡司郎中", "agent_ent_ids": []}, "condition": "岁课", "next": []},
     ], "confidence": 0.88},

    # ---------- 条51 屯田司设屯流程 ----------
    {"slot": 8, "item_id": "01-051", "name": "屯田司设屯益储流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "凡军马守镇之处，其有转运不给",
          "agent": {"text": "屯田司郎中", "agent_ent_ids": []}, "condition": "转运不给", "next": [2]},
         {"seq": 2, "text": "则设屯以益军储",
          "agent": {"text": "屯田司郎中", "agent_ent_ids": []}, "condition": "设屯", "next": []},
     ], "confidence": 0.9},

    # ---------- 条40 京营操练流程 ----------
    {"slot": 9, "item_id": "01-040", "name": "京营操练流程", "scope": "其他",
     "steps": [
         {"seq": 1, "text": "掌京营操练之事",
          "agent": {"text": "协理京营戎政", "agent_ent_ids": []}, "condition": "未明", "next": [2]},
         {"seq": 2, "text": "（三大营总于武将；景泰元年始设提督团营，命兵部尚书于谦兼领之）",
          "agent": {"text": "提督团营", "agent_ent_ids": []}, "condition": "团营", "next": []},
     ], "confidence": 0.85},
]
