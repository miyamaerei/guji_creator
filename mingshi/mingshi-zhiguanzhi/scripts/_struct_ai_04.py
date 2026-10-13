# -*- coding: utf-8 -*-
"""
【卷04】L4 结构化层源数据（四维 ORG/RANK/LINE/EVO）
v7（2026-10-14）三项决定落地（模板容器已取消）：
  ① 南京段（条1-26）RANK 关联北京 node：posts[] 元素带 link_to_bj{org_id, rank_id, grade_ref}，
     grade="同北京"，grade_order 由打包器取 grade_ref 实际品级值
  ② 条37-42 道制 / 条54-61 府州县 / 条62-75 杂职 → 直接作 ORGS 正式节点
     （v6 曾置于 ORG_TEMPLATES 容器，用户裁定取消：这些首先是机构，通用编制只是额外属性）
  ③ 条27 南京官总述 → 虚拟锚点（is_virtual=True）
"""

# ============ ORG 机构树 ============
ORGS = [
    # ---- 条1-26 南京官（level="南京"，parent=天子）----
    {"slot": 1, "item_id": "04-001", "name": "南京宗人府", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["经历"], "total_posts": 1,
     "note": "南京官品秩，俱同北京", "children": [
         {"name": "经历司", "level": "司", "parent": "南京宗人府",
          "posts": [{"office": "经历", "count": 1, "grade": "同北京"}], "children": []}
     ], "ent_ids": [], "confidence": 0.92},
    {"slot": 2, "item_id": "04-002", "name": "南京吏部", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["尚书", "右侍郎"], "total_posts": 0,
     "note": "南京官品秩，俱同北京；凡南京官，六年考察，考功掌之，不由北吏部", "children": [
         {"name": "司务厅", "level": "司", "parent": "南京吏部",
          "posts": [{"office": "司务", "count": 1, "grade": "同北京"}], "children": []},
         {"name": "四清吏司", "level": "司", "parent": "南京吏部",
          "posts": [{"office": "郎中", "count": 4, "grade": "同北京"},
                    {"office": "主事", "count": 4, "grade": "同北京"}], "children": [],
          "note": "文选、考功、验封、稽勋四清吏司，各郎中一人，主事一人　（验封、稽勋二司主事，后并革）"}
     ], "ent_ids": [], "confidence": 0.92},
    {"slot": 3, "item_id": "04-003", "name": "南京户部", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["尚书", "右侍郎"], "total_posts": 0,
     "note": "南京官品秩，俱同北京", "children": [
         {"name": "十三司", "level": "司", "parent": "南京户部",
          "posts": [{"office": "郎中", "count": 13, "grade": "同北京"},
                    {"office": "员外郎", "count": 9, "grade": "同北京"},
                    {"office": "主事", "count": 0, "grade": "同北京"}], "children": []}
     ], "ent_ids": [], "confidence": 0.9},
    {"slot": 4, "item_id": "04-005", "name": "南京礼部", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["尚书", "右侍郎"], "total_posts": 0,
     "note": "南京官品秩，俱同北京", "children": [
         {"name": "四司", "level": "司", "parent": "南京礼部",
          "posts": [{"office": "郎中", "count": 4, "grade": "同北京"},
                    {"office": "主事", "count": 2, "grade": "同北京"}], "children": [],
          "note": "仪制、祠祭、主客、精膳四司，各郎中一人；仪制、祠祭二司，各主事一人"},
         {"name": "铸印局", "level": "局", "parent": "南京礼部",
          "posts": [{"office": "副使", "count": 1, "grade": "同北京"}], "children": []}
     ], "ent_ids": [], "confidence": 0.9},
    {"slot": 5, "item_id": "04-006", "name": "南京兵部", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["尚书参赞机务", "右侍郎"], "total_posts": 0,
     "note": "南京官品秩，俱同北京；参赞机务自宣德八年黄福始，成化二十三年奉敕谕专以本部尚书参赞机务",
     "children": [
         {"name": "四司", "level": "司", "parent": "南京兵部",
          "posts": [{"office": "郎中", "count": 4, "grade": "同北京"},
                    {"office": "员外郎", "count": 2, "grade": "同北京"},
                    {"office": "主事", "count": 5, "grade": "同北京"}], "children": [],
          "note": "武选、职方、车驾、武库四司，郎中四人，员外郎二人（武选、武库无员外郎），主事五人"},
         {"name": "典牧所", "level": "所", "parent": "南京兵部",
          "posts": [{"office": "提领", "count": 1, "grade": "正八品"}], "children": []},
         {"name": "会同馆", "level": "局", "parent": "南京兵部",
          "posts": [{"office": "大使", "count": 1, "grade": "同北京"}], "children": []},
         {"name": "大胜关", "level": "局", "parent": "南京兵部",
          "posts": [{"office": "大使", "count": 1, "grade": "同北京"}], "children": []}
     ], "ent_ids": [], "confidence": 0.9},
    {"slot": 6, "item_id": "04-007", "name": "南京刑部", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["尚书", "右侍郎"], "total_posts": 0,
     "note": "南京官品秩，俱同北京；分掌南京诸司，及公、侯、伯、五府、京卫所刑名之事", "children": [
         {"name": "十三司", "level": "司", "parent": "南京刑部",
          "posts": [{"office": "郎中", "count": 13, "grade": "同北京"},
                    {"office": "员外郎", "count": 5, "grade": "同北京"},
                    {"office": "主事", "count": 14, "grade": "同北京"}], "children": [],
          "note": "十三司郎中十三人，员外郎五人（惟浙江、江西、河南、陕西、广东五司设），主事十四人（广东司二人）"},
         {"name": "司狱司", "level": "司", "parent": "南京刑部",
          "posts": [{"office": "司狱", "count": 2, "grade": "同北京"}], "children": []}
     ], "ent_ids": [], "confidence": 0.9},
    {"slot": 7, "item_id": "04-008", "name": "南京工部", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["尚书", "右侍郎"], "total_posts": 0,
     "note": "南京官品秩，俱同北京", "children": [
         {"name": "四司", "level": "司", "parent": "南京工部",
          "posts": [{"office": "郎中", "count": 4, "grade": "同北京"},
                    {"office": "员外郎", "count": 2, "grade": "同北京"}], "children": [],
          "note": "营缮、虞衡、都水、屯田四司，郎中四人，员外郎二人（营缮司一人，都水司一人）"}
     ], "ent_ids": [], "confidence": 0.9},
    {"slot": 8, "item_id": "04-009", "name": "南京都察院", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["右都御史", "右副都御史", "右佥都御史"],
     "total_posts": 0, "note": "南京官品秩，俱同北京", "children": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 9, "item_id": "04-011", "name": "南京通政使司", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["通政使", "右通政", "右参议"], "total_posts": 4,
     "note": "掌收呈状，付刑部审理", "children": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 10, "item_id": "04-012", "name": "南京大理寺", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["卿", "右寺丞"], "total_posts": 0,
     "note": "南京官品秩，俱同北京", "children": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 11, "item_id": "04-013", "name": "南京詹事府", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["主簿"], "total_posts": 1,
     "note": "南京官品秩，俱同北京", "children": [], "ent_ids": [], "confidence": 0.88},
    {"slot": 12, "item_id": "04-014", "name": "南京翰林院", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["学士", "孔目"], "total_posts": 2,
     "note": "学士不常置，以翰林坊局官署职", "children": [], "ent_ids": [], "confidence": 0.88},
    {"slot": 13, "item_id": "04-015", "name": "南京国子监", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["祭酒", "司业"], "total_posts": 0,
     "note": "南京官品秩，俱同北京", "children": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 14, "item_id": "04-016", "name": "南京太常寺", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["卿", "少卿"], "total_posts": 0,
     "note": "南京官品秩，俱同北京", "children": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 15, "item_id": "04-017", "name": "南京光禄寺", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["卿", "少卿"], "total_posts": 0,
     "note": "南京官品秩，俱同北京", "children": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 16, "item_id": "04-018", "name": "南京太仆寺", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["卿", "少卿", "寺丞", "主簿"], "total_posts": 0,
     "note": "南京官品秩，俱同北京；隆庆中革少卿一人、寺丞一人", "children": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 17, "item_id": "04-019", "name": "南京鸿胪寺", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["卿", "主簿"], "total_posts": 0,
     "note": "南京官品秩，俱同北京", "children": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 18, "item_id": "04-020", "name": "南京尚宝司", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["卿"], "total_posts": 1,
     "note": "南京官品秩，俱同北京", "children": [], "ent_ids": [], "confidence": 0.88},
    {"slot": 19, "item_id": "04-021", "name": "南京六科", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["给事中"], "total_posts": 7,
     "note": "吏、户、礼、兵、刑、工六科给事中六人，又户科给事中一人管理后湖黄册",
     "children": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 20, "item_id": "04-022", "name": "南京行人司", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["左司副"], "total_posts": 1,
     "note": "南京官品秩，俱同北京", "children": [], "ent_ids": [], "confidence": 0.88},
    {"slot": 21, "item_id": "04-023", "name": "南京钦天监", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["监正", "监副"], "total_posts": 0,
     "note": "南京官品秩，俱同北京", "children": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 22, "item_id": "04-024", "name": "南京太医院", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["院判", "吏目"], "total_posts": 0,
     "note": "南京官品秩，俱同北京", "children": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 23, "item_id": "04-025", "name": "南京五城兵马司", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["指挥", "副指挥", "吏目"], "total_posts": 0,
     "note": "南京官品秩，俱同北京；万历中革副指挥每城二人", "children": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 24, "item_id": "04-004", "name": "南京总督粮储", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["总督粮储"], "total_posts": 1,
     "note": "嘉靖以前特设都御史；二十六年革，以户部右侍郎加都御史衔领之（南京特设，北京无对应）",
     "children": [], "ent_ids": [], "confidence": 0.88},
    {"slot": 25, "item_id": "04-010", "name": "南京提督操江", "level": "南京", "org_type": "南京",
     "parent": "天子", "core_officials": ["提督操江"], "total_posts": 1,
     "note": "以副佥都御史为之，领上、下江防之事（南京特设，北京无对应）",
     "children": [], "ent_ids": [], "confidence": 0.88},
    # 应天府（南京独有，北京为顺天府）
    {"slot": 26, "item_id": "04-026", "name": "应天府", "level": "府", "org_type": "府",
     "parent": "天子", "core_officials": ["府尹", "府丞", "治中", "通判", "推官"],
     "total_posts": 0,
     "note": "洪武三年改应天府知府为府尹，秩正三品，赐银印；十三年始立儒学",
     "children": [
         {"name": "宛平县", "level": "州县", "parent": "应天府", "posts": [], "children": [],
          "note": "对应北京顺天府之宛平"},
         {"name": "江宁", "level": "州县", "parent": "应天府",
          "posts": [{"office": "知县", "count": 1, "grade": "同北京"},
                    {"office": "县丞", "count": 1, "grade": "同北京"}], "children": []},
         {"name": "司狱司", "level": "司", "parent": "应天府",
          "posts": [{"office": "司狱", "count": 1, "grade": "同北京"}], "children": []},
         {"name": "织染局", "level": "局", "parent": "应天府",
          "posts": [{"office": "大使", "count": 1, "grade": "同北京"},
                    {"office": "左、右副使", "count": 2, "grade": "同北京"}], "children": []}
     ], "ent_ids": [], "confidence": 0.9},

    # ---- 条27 南京官（虚拟锚点）----
    {"slot": 27, "item_id": "04-027", "name": "南京官", "level": "虚拟锚点", "org_type": "虚拟锚点",
     "parent": "天子", "core_officials": [], "total_posts": 0,
     "note": "虚拟节点：南京官制整体沿革的 TME 承载锚点，非实体机构",
     "children": [], "ent_ids": [], "confidence": 0.8, "is_virtual": True},

    # ---- 条28 王府长史司 ----
    {"slot": 28, "item_id": "04-028", "name": "王府长史司", "level": "王府", "org_type": "王府",
     "parent": "天子", "core_officials": ["左、右长史"], "total_posts": 0,
     "note": "洪武三年置王相府，后改置；长史掌王府之政讼",
     "children": [
         {"name": "审理所", "level": "所", "parent": "王府长史司",
          "posts": [{"office": "审理正", "count": 1, "grade": "正六品"},
                    {"office": "审理副", "count": 1, "grade": "正七品"}], "children": []},
         {"name": "典膳所", "level": "所", "parent": "王府长史司",
          "posts": [{"office": "典膳正", "count": 1, "grade": "正八品"},
                    {"office": "典膳副", "count": 1, "grade": "从八品"}], "children": []},
         {"name": "奉祠所", "level": "所", "parent": "王府长史司",
          "posts": [{"office": "奉祠正", "count": 1, "grade": "正八品"},
                    {"office": "奉祠副", "count": 1, "grade": "从八品"},
                    {"office": "典乐", "count": 1, "grade": "正九品"}], "children": []},
         {"name": "典宝所", "level": "所", "parent": "王府长史司",
          "posts": [{"office": "典宝正", "count": 1, "grade": "正八品"},
                    {"office": "典宝副", "count": 1, "grade": "从八品"}], "children": []},
         {"name": "纪善所", "level": "所", "parent": "王府长史司",
          "posts": [{"office": "纪善", "count": 2, "grade": "正八品"}], "children": []},
         {"name": "良医所", "level": "所", "parent": "王府长史司",
          "posts": [{"office": "良医正", "count": 1, "grade": "正八品"},
                    {"office": "良医副", "count": 1, "grade": "从八品"}], "children": []},
         {"name": "典仪所", "level": "所", "parent": "王府长史司",
          "posts": [{"office": "典仪正", "count": 1, "grade": "正九品"},
                    {"office": "典仪副", "count": 1, "grade": "从九品"}], "children": []},
         {"name": "工正所", "level": "所", "parent": "王府长史司",
          "posts": [{"office": "工正", "count": 1, "grade": "正八品"},
                    {"office": "工正副", "count": 1, "grade": "从八品"}], "children": []},
         {"name": "典簿", "level": "司", "parent": "王府长史司",
          "posts": [{"office": "典簿", "count": 1, "grade": "正九品"}], "children": []},
         {"name": "郡王府", "level": "王府", "parent": "王府长史司",
          "posts": [{"office": "教授", "count": 1, "grade": "从九品"},
                    {"office": "典膳", "count": 1, "grade": "正八品"}], "children": []},
         {"name": "镇国将军府", "level": "王府", "parent": "王府长史司",
          "posts": [{"office": "教授", "count": 1, "grade": "从九品"}], "children": []}
     ], "ent_ids": [], "confidence": 0.9},

    # ---- 条31 承宣布政使司 ----
    {"slot": 29, "item_id": "04-031", "name": "承宣布政使司", "level": "布政按察",
     "org_type": "布政按察", "parent": "天子",
     "core_officials": ["左、右布政使", "左、右参政", "左、右参议"], "total_posts": 0,
     "note": "掌一省之政，朝廷有德泽、禁令，承流宣播，以下于有司",
     "children": [
         {"name": "经历司", "level": "司", "parent": "承宣布政使司",
          "posts": [{"office": "经历", "count": 1, "grade": "从六品"},
                    {"office": "都事", "count": 1, "grade": "从七品"}], "children": []},
         {"name": "照磨所", "level": "所", "parent": "承宣布政使司",
          "posts": [{"office": "照磨", "count": 1, "grade": "从八品"},
                    {"office": "检校", "count": 1, "grade": "正九品"}], "children": []},
         {"name": "理问所", "level": "所", "parent": "承宣布政使司",
          "posts": [{"office": "理问", "count": 1, "grade": "从六品"},
                    {"office": "副理问", "count": 1, "grade": "从七品"},
                    {"office": "提控案牍", "count": 1, "grade": "未明"}], "children": []},
         {"name": "司狱司", "level": "司", "parent": "承宣布政使司",
          "posts": [{"office": "司狱", "count": 1, "grade": "从九品"}], "children": []},
         {"name": "杂造局", "level": "局", "parent": "承宣布政使司",
          "posts": [{"office": "大使", "count": 1, "grade": "从九品"},
                    {"office": "副使", "count": 1, "grade": "未明"}], "children": [],
          "note": "军器局、宝泉局、织染局同　（所辖衙门各省不同，详见杂职）"}
     ], "ent_ids": [], "confidence": 0.92},

    # ---- 条34 提刑按察使司 ----
    {"slot": 30, "item_id": "04-034", "name": "提刑按察使司", "level": "布政按察",
     "org_type": "布政按察", "parent": "天子",
     "core_officials": ["按察使", "副使", "佥事"], "total_posts": 0,
     "note": "掌一省刑名按劾之事。纠官邪，戢奸暴，平狱讼，雪冤抑，以振扬风纪，而澄清其吏治",
     "children": [
         {"name": "经历司", "level": "司", "parent": "提刑按察使司",
          "posts": [{"office": "经历", "count": 1, "grade": "正七品"},
                    {"office": "知事", "count": 1, "grade": "正八品"}], "children": []},
         {"name": "照磨所", "level": "所", "parent": "提刑按察使司",
          "posts": [{"office": "照磨", "count": 1, "grade": "正九品"},
                    {"office": "检校", "count": 1, "grade": "从九品"}], "children": []},
         {"name": "司狱司", "level": "司", "parent": "提刑按察使司",
          "posts": [{"office": "司狱", "count": 1, "grade": "从九品"}], "children": []}
     ], "ent_ids": [], "confidence": 0.92},

    # ---- 条43 行太仆寺 ----
    {"slot": 31, "item_id": "04-043", "name": "行太仆寺", "level": "寺", "org_type": "寺",
     "parent": "天子", "core_officials": ["卿", "少卿", "寺丞"], "total_posts": 0,
     "note": "掌各边卫所营堡之马政，以听于兵部；洪武三十年置行太仆寺于山西、北平、陕西、甘肃、辽东",
     "children": [
         {"name": "主簿", "level": "司", "parent": "行太仆寺",
          "posts": [{"office": "主簿", "count": 1, "grade": "从七品"}], "children": []}
     ], "ent_ids": [], "confidence": 0.9},

    # ---- 条45 苑马寺 ----
    {"slot": 32, "item_id": "04-045", "name": "苑马寺", "level": "寺", "org_type": "寺",
     "parent": "天子", "core_officials": ["卿", "少卿", "寺丞"], "total_posts": 0,
     "note": "永乐四年置苑马寺凡四：北直隶、辽东、平凉、甘肃；五年增设北直隶苑马寺六监二十四苑",
     "children": [
         {"name": "主簿", "level": "司", "parent": "苑马寺",
          "posts": [{"office": "主簿", "count": 1, "grade": "从七品"}], "children": []},
         {"name": "各牧监", "level": "监", "parent": "苑马寺",
          "posts": [{"office": "监正", "count": 1, "grade": "正九品"},
                    {"office": "监副", "count": 1, "grade": "从九品"},
                    {"office": "录事", "count": 1, "grade": "未明"}], "children": []},
         {"name": "各苑", "level": "所", "parent": "苑马寺",
          "posts": [{"office": "圉长", "count": 1, "grade": "未明"}], "children": []}
     ], "ent_ids": [], "confidence": 0.88},

    # ---- 条47 都转运盐使司 ----
    {"slot": 33, "item_id": "04-047", "name": "都转运盐使司", "level": "布政按察",
     "org_type": "布政按察", "parent": "天子",
     "core_officials": ["都转运使", "同知", "副使", "判官"], "total_posts": 0,
     "note": "掌盐监之事；都转运盐使司凡六：两淮、两浙、长芦、河东、山东、福建；分司十四",
     "children": [
         {"name": "经历司", "level": "司", "parent": "都转运盐使司",
          "posts": [{"office": "经历", "count": 1, "grade": "从七品"},
                    {"office": "知事", "count": 1, "grade": "从八品"}], "children": []}
     ], "ent_ids": [], "confidence": 0.9},

    # ---- 条49 盐课提举司 ----
    {"slot": 34, "item_id": "04-049", "name": "盐课提举司", "level": "司", "org_type": "司",
     "parent": "天子", "core_officials": ["提举", "同提举"], "total_posts": 0,
     "note": "掌盐课；提举一人，同提举一人，副提举无定员",
     "children": [], "ent_ids": [], "confidence": 0.88},

    # ---- 条51 市舶提举司 ----
    {"slot": 35, "item_id": "04-051", "name": "市舶提举司", "level": "司", "org_type": "司",
     "parent": "天子", "core_officials": ["提举", "副提举"], "total_posts": 3,
     "note": "掌海外诸蕃朝贡市易之事；吴元年置，洪武三年罢太仓、黄渡，七年罢泉州、明州、广州，永乐元年复置",
     "children": [], "ent_ids": [], "confidence": 0.9},

    # ---- 条53 茶马司 ----
    {"slot": 36, "item_id": "04-053", "name": "茶马司", "level": "司", "org_type": "地方",
     "parent": "天子", "core_officials": ["大使", "副使"], "total_posts": 2,
     "note": "掌市马之事；洪武中置洮州、秦州、河州三茶马司，十五年改设大使、副使",
     "children": [], "ent_ids": [], "confidence": 0.9},
]

# ============ RANK 品级员额（南京段带 link_to_bj）============
RANKS = [
    # 南京吏部
    {"slot": 1, "item_id": "04-002", "owner": "南京吏部", "rank_type": "品级员额",
     "posts": [
         {"office": "尚书", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-505", "rank_id": "RANK-505", "grade_ref": "正二品"},
          "count_form": "P4", "count_evidence": "吏部。尚书一人，右侍郎一人。",
          "note": "南京官品秩，俱同北京"},
         {"office": "右侍郎", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-505", "rank_id": "RANK-505", "grade_ref": "正三品"},
          "count_form": "P4", "count_evidence": "尚书一人，右侍郎一人。",
          "note": "六部侍郎，至弘治后始专设右；万历三年俱革，十一年复设"},
         {"office": "司务", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-505", "rank_id": "RANK-505", "grade_ref": "从九品"},
          "count_form": "P4", "count_evidence": "司务厅，司务一人。", "note": "未明"},
         {"office": "郎中", "office_parts": [], "count": 4, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-505", "rank_id": "RANK-505", "grade_ref": "正五品"},
          "count_form": "P4", "count_evidence": "各郎中一人，主事一人。",
          "note": "四清吏司各一人"},
         {"office": "主事", "office_parts": [], "count": 4, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-505", "rank_id": "RANK-505", "grade_ref": "正六品"},
          "count_form": "P4", "count_evidence": "各郎中一人，主事一人。",
          "note": "验封、稽勋二司主事，后并革"},
     ], "confidence": 0.92},

    # 南京户部
    {"slot": 2, "item_id": "04-003", "owner": "南京户部", "rank_type": "品级员额",
     "posts": [
         {"office": "尚书", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-506", "rank_id": "RANK-506", "grade_ref": "正二品"},
          "count_form": "P4", "count_evidence": "户部。尚书一人，右侍郎一人，", "note": "未明"},
         {"office": "右侍郎", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-506", "rank_id": "RANK-506", "grade_ref": "正三品"},
          "count_form": "P4", "count_evidence": "尚书一人，右侍郎一人，", "note": "未明"},
         {"office": "司务", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-506", "rank_id": "RANK-506", "grade_ref": "从九品"},
          "count_form": "P4", "count_evidence": "司务一人，照磨一人。", "note": "未明"},
         {"office": "照磨", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-506", "rank_id": "RANK-506", "grade_ref": "正八品"},
          "count_form": "P4", "count_evidence": "司务一人，照磨一人。", "note": "未明"},
         {"office": "郎中", "office_parts": [], "count": 13, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-506", "rank_id": "RANK-506", "grade_ref": "正五品"},
          "count_form": "P4", "count_evidence": "十三司，郎中十三人，", "note": "十三司各一人"},
         {"office": "员外郎", "office_parts": [], "count": 9, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-506", "rank_id": "RANK-506", "grade_ref": "从五品"},
          "count_form": "P4", "count_evidence": "员外郎九人，",
          "note": "浙江、江西、湖广、广东、广西、福建、山西等九司"},
     ], "confidence": 0.9},

    # 南京礼部
    {"slot": 3, "item_id": "04-005", "owner": "南京礼部", "rank_type": "品级员额",
     "posts": [
         {"office": "尚书", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-508", "rank_id": "", "grade_ref": "正二品"},
          "count_form": "P4", "count_evidence": "礼部。尚书一人，右侍郎一人，", "note": "未明"},
         {"office": "右侍郎", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-508", "rank_id": "", "grade_ref": "正三品"},
          "count_form": "P4", "count_evidence": "礼部。尚书一人，右侍郎一人，", "note": "未明"},
         {"office": "郎中", "office_parts": [], "count": 4, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-508", "rank_id": "", "grade_ref": "正五品"},
          "count_form": "P4", "count_evidence": "四司，各郎中一人。", "note": "四司各一人"},
         {"office": "主事", "office_parts": [], "count": 2, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-508", "rank_id": "", "grade_ref": "正六品"},
          "count_form": "P4", "count_evidence": "仪制、祠祭二司，各主事一人。", "note": "二司各一人"},
     ], "confidence": 0.9},

    # 南京兵部
    {"slot": 4, "item_id": "04-006", "owner": "南京兵部", "rank_type": "品级员额",
     "posts": [
         {"office": "尚书参赞机务", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-509", "rank_id": "", "grade_ref": "正二品"},
          "count_form": "P4", "count_evidence": "兵部。尚书参赞机务一人，右侍郎一人，",
          "note": "参赞机务，自宣德八年黄福始；其职视五部为特重"},
         {"office": "右侍郎", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-509", "rank_id": "", "grade_ref": "正三品"},
          "count_form": "P4", "count_evidence": "尚书参赞机务一人，右侍郎一人，", "note": "未明"},
         {"office": "郎中", "office_parts": [], "count": 4, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-509", "rank_id": "", "grade_ref": "正五品"},
          "count_form": "P4", "count_evidence": "四司，郎中四人，", "note": "四司各一人"},
         {"office": "员外郎", "office_parts": [], "count": 2, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-509", "rank_id": "", "grade_ref": "从五品"},
          "count_form": "P4", "count_evidence": "员外郎二人，(武选、武库无员外郎。)", "note": "武选、武库无员外郎"},
         {"office": "主事", "office_parts": [], "count": 5, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-509", "rank_id": "", "grade_ref": "正六品"},
          "count_form": "P4", "count_evidence": "主事五人。(车驾主事二人。)", "note": "车驾主事二人"},
         {"office": "提领", "office_parts": [], "count": 1, "grade": "正八品",
          "link_to_bj": {},
          "count_form": "P4", "count_evidence": "典牧所，提领一人。(正八品)",
          "note": "南京特设，北京无对应"},
     ], "confidence": 0.9},

    # 南京刑部
    {"slot": 5, "item_id": "04-007", "owner": "南京刑部", "rank_type": "品级员额",
     "posts": [
         {"office": "尚书", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-511", "rank_id": "RANK-1511", "grade_ref": "正二品"},
          "count_form": "P4", "count_evidence": "刑部。尚书一人，右侍郎一人，", "note": "未明"},
         {"office": "右侍郎", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-511", "rank_id": "RANK-1511", "grade_ref": "正三品"},
          "count_form": "P4", "count_evidence": "刑部。尚书一人，右侍郎一人，", "note": "未明"},
         {"office": "郎中", "office_parts": [], "count": 13, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-511", "rank_id": "RANK-1511", "grade_ref": "正五品"},
          "count_form": "P4", "count_evidence": "十三司郎中十三人，", "note": "十三司各一人"},
         {"office": "员外郎", "office_parts": [], "count": 5, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-511", "rank_id": "RANK-1511", "grade_ref": "从五品"},
          "count_form": "P4", "count_evidence": "员外郎五人，(惟浙江、江西、河南、陕西、广东五司设。)",
          "note": "惟浙江、江西、河南、陕西、广东五司设"},
         {"office": "主事", "office_parts": [], "count": 14, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-511", "rank_id": "RANK-1511", "grade_ref": "正六品"},
          "count_form": "P4", "count_evidence": "主事十四人，(广东司二人。)", "note": "广东司二人"},
         {"office": "司狱", "office_parts": [], "count": 2, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-511", "rank_id": "RANK-1511", "grade_ref": "从九品"},
          "count_form": "P4", "count_evidence": "司狱二人。", "note": "未明"},
     ], "confidence": 0.9},

    # 南京工部
    {"slot": 6, "item_id": "04-008", "owner": "南京工部", "rank_type": "品级员额",
     "posts": [
         {"office": "尚书", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-512", "rank_id": "", "grade_ref": "正二品"},
          "count_form": "P4", "count_evidence": "工部。尚书一人，右侍郎一人，", "note": "未明"},
         {"office": "右侍郎", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-512", "rank_id": "", "grade_ref": "正三品"},
          "count_form": "P4", "count_evidence": "工部。尚书一人，右侍郎一人，", "note": "未明"},
         {"office": "郎中", "office_parts": [], "count": 4, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-512", "rank_id": "", "grade_ref": "正五品"},
          "count_form": "P4", "count_evidence": "四司，郎中四人，", "note": "四司各一人"},
         {"office": "员外郎", "office_parts": [], "count": 2, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-512", "rank_id": "", "grade_ref": "从五品"},
          "count_form": "P4", "count_evidence": "员外郎二人，(营缮司一人，都水司一人", "note": "营缮司一人，都水司一人"},
     ], "confidence": 0.9},

    # 南京都察院
    {"slot": 7, "item_id": "04-009", "owner": "南京都察院", "rank_type": "品级员额",
     "posts": [
         {"office": "右都御史", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1001", "rank_id": "RANK-1001", "grade_ref": "正二品"},
          "count_form": "P4", "count_evidence": "都察院。右都御史一人，", "note": "未明"},
         {"office": "右副都御史", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1001", "rank_id": "RANK-1001", "grade_ref": "正三品"},
          "count_form": "P4", "count_evidence": "右副都御史一人，", "note": "未明"},
         {"office": "右佥都御史", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1001", "rank_id": "RANK-1001", "grade_ref": "正四品"},
          "count_form": "P4", "count_evidence": "右佥都御史一人，", "note": "未明"},
         {"office": "司狱", "office_parts": [], "count": 2, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1001", "rank_id": "RANK-1001", "grade_ref": "从九品"},
          "count_form": "P4", "count_evidence": "司狱二人。(嘉靖三十七年，革司狱一人。",
          "note": "嘉靖三十七年革司狱一人"},
     ], "confidence": 0.9},

    # 南京通政使司
    {"slot": 8, "item_id": "04-011", "owner": "南京通政使司", "rank_type": "品级员额",
     "posts": [
         {"office": "通政使", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1048", "rank_id": "RANK-1048", "grade_ref": "正三品"},
          "count_form": "P4", "count_evidence": "通政使司。通政使一人，右通政一人，右参议一人，",
          "note": "未明"},
         {"office": "右通政", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1048", "rank_id": "RANK-1048", "grade_ref": "正四品"},
          "count_form": "P4", "count_evidence": "通政使一人，右通政一人，", "note": "未明"},
         {"office": "右参议", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1048", "rank_id": "RANK-1048", "grade_ref": "正五品"},
          "count_form": "P4", "count_evidence": "右参议一人，", "note": "未明"},
         {"office": "经历", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1048", "rank_id": "RANK-1048", "grade_ref": "正七品"},
          "count_form": "P4", "count_evidence": "经历一人。", "note": "未明"},
     ], "confidence": 0.9},

    # 南京大理寺
    {"slot": 9, "item_id": "04-012", "owner": "南京大理寺", "rank_type": "品级员额",
     "posts": [
         {"office": "卿", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1049", "rank_id": "RANK-1049", "grade_ref": "正三品"},
          "count_form": "P4", "count_evidence": "大理寺。卿一人，右寺丞一人，", "note": "未明"},
         {"office": "右寺丞", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1049", "rank_id": "RANK-1049", "grade_ref": "正五品"},
          "count_form": "P4", "count_evidence": "卿一人，右寺丞一人，", "note": "未明"},
         {"office": "左、右评事", "office_parts": ["左评事", "右评事"], "count": 3, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1049", "rank_id": "RANK-1049", "grade_ref": "正七品"},
          "count_form": "P4", "count_evidence": "左、右评事各三人。(隆庆三年，革左、右评事各一人。)",
          "note": "隆庆三年革左、右评事各一人"},
     ], "confidence": 0.9},

    # 应天府
    {"slot": 10, "item_id": "04-026", "owner": "应天府", "rank_type": "品级员额",
     "posts": [
         {"office": "府尹", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1514", "rank_id": "RANK-1514", "grade_ref": "正三品"},
          "count_form": "P4", "count_evidence": "应天府。府尹一人，府丞一人，",
          "note": "对应北京顺天府；洪武三年改应天府知府为府尹，秩正三品，赐银印"},
         {"office": "府丞", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1514", "rank_id": "RANK-1514", "grade_ref": "正四品"},
          "count_form": "P4", "count_evidence": "府尹一人，府丞一人，", "note": "未明"},
         {"office": "治中", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1514", "rank_id": "RANK-1514", "grade_ref": "正五品"},
          "count_form": "P4", "count_evidence": "治中一人，通判二人，", "note": "未明"},
         {"office": "通判", "office_parts": [], "count": 2, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1514", "rank_id": "RANK-1514", "grade_ref": "正六品"},
          "count_form": "P4", "count_evidence": "通判二人，推官一人，", "note": "未明"},
         {"office": "推官", "office_parts": [], "count": 1, "grade": "同北京",
          "link_to_bj": {"org_id": "ORG-1514", "rank_id": "RANK-1514", "grade_ref": "从六品"},
          "count_form": "P4", "count_evidence": "推官一人，经历、知事、照磨、检校各一人。",
          "note": "未明"},
     ], "confidence": 0.9},

    # 王府长史司
    {"slot": 11, "item_id": "04-028", "owner": "王府长史司", "rank_type": "品级员额",
     "posts": [
         {"office": "左、右长史", "office_parts": ["左长史", "右长史"], "count": 2, "grade": "正五品",
          "count_form": "P1", "count_evidence": "左、右长史各一人。(正五品)", "note": "未明"},
         {"office": "典簿", "office_parts": [], "count": 1, "grade": "正九品",
          "count_form": "P4", "count_evidence": "其属，典簿一人，(正九品)", "note": "未明"},
         {"office": "审理正", "office_parts": [], "count": 1, "grade": "正六品",
          "count_form": "P4", "count_evidence": "审理所，审理正一人，(正六品)", "note": "未明"},
         {"office": "纪善", "office_parts": [], "count": 2, "grade": "正八品",
          "count_form": "P4", "count_evidence": "纪善所，纪善二人，(正八品)", "note": "未明"},
         {"office": "教授", "office_parts": [], "count": 0, "grade": "从九品",
          "count_form": "P4", "count_evidence": "教授无定员，(从九品)", "note": "无定员"},
         {"office": "伴读", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "伴读四人，(从九品，后止设一人。)", "note": "初四人，后止设一人"},
     ], "confidence": 0.9},

    # 承宣布政使司
    {"slot": 12, "item_id": "04-031", "owner": "承宣布政使司", "rank_type": "品级员额",
     "posts": [
         {"office": "左、右布政使", "office_parts": ["左布政使", "右布政使"], "count": 2,
          "grade": "从二品", "count_form": "P1",
          "count_evidence": "左、右布政使各一人，(从二品)", "note": "未明"},
         {"office": "左、右参政", "office_parts": ["左参政", "右参政"], "count": 2, "grade": "从三品",
          "count_form": "P1", "count_evidence": "左、右参政，(从三品)", "note": "未明"},
         {"office": "左、右参议", "office_parts": ["左参议", "右参议"], "count": 0, "grade": "从四品",
          "count_form": "P4", "count_evidence": "左、右参议，无定员。(从四品。",
          "note": "无定员；参政、参议因事添设，各省不等"},
         {"office": "经历", "office_parts": [], "count": 1, "grade": "从六品",
          "count_form": "P4", "count_evidence": "经历司，经历一人，(从六品)", "note": "未明"},
         {"office": "都事", "office_parts": [], "count": 1, "grade": "从七品",
          "count_form": "P4", "count_evidence": "都事一人。(从七品)", "note": "未明"},
         {"office": "理问", "office_parts": [], "count": 1, "grade": "从六品",
          "count_form": "P4", "count_evidence": "理问所，理问一人，(从六品)", "note": "未明"},
         {"office": "司狱", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "司狱司，司狱一人，(从九品)", "note": "未明"},
     ], "confidence": 0.92},

    # 提刑按察使司
    {"slot": 13, "item_id": "04-034", "owner": "提刑按察使司", "rank_type": "品级员额",
     "posts": [
         {"office": "按察使", "office_parts": [], "count": 1, "grade": "正三品",
          "count_form": "P4", "count_evidence": "按察使一人，(正三品)", "note": "未明"},
         {"office": "副使", "office_parts": [], "count": 0, "grade": "正四品",
          "count_form": "P4", "count_evidence": "副使，(正四品)", "note": "无定员"},
         {"office": "佥事", "office_parts": [], "count": 0, "grade": "正五品",
          "count_form": "P4", "count_evidence": "佥事无定员。(正五品。详见诸道。)", "note": "无定员"},
         {"office": "经历", "office_parts": [], "count": 1, "grade": "正七品",
          "count_form": "P4", "count_evidence": "经历司，经历一人，(正七品)", "note": "未明"},
         {"office": "司狱", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "司狱司，司狱一人，(从九品)", "note": "未明"},
     ], "confidence": 0.92},

    # 行太仆寺
    {"slot": 14, "item_id": "04-043", "owner": "行太仆寺", "rank_type": "品级员额",
     "posts": [
         {"office": "卿", "office_parts": [], "count": 1, "grade": "从三品",
          "count_form": "P4", "count_evidence": "行太仆寺。卿一人，(从三品)", "note": "未明"},
         {"office": "少卿", "office_parts": [], "count": 1, "grade": "正四品",
          "count_form": "P4", "count_evidence": "少卿一人，(正四品)", "note": "未明"},
         {"office": "寺丞", "office_parts": [], "count": 0, "grade": "正六品",
          "count_form": "P4", "count_evidence": "寺丞无定员，(正六品)", "note": "无定员"},
         {"office": "主簿", "office_parts": [], "count": 1, "grade": "从七品",
          "count_form": "P4", "count_evidence": "主簿一人，(从七品)", "note": "未明"},
     ], "confidence": 0.9},

    # 苑马寺
    {"slot": 15, "item_id": "04-045", "owner": "苑马寺", "rank_type": "品级员额",
     "posts": [
         {"office": "卿", "office_parts": [], "count": 1, "grade": "从三品",
          "count_form": "P4", "count_evidence": "苑马寺。卿一人，(从三品)", "note": "未明"},
         {"office": "少卿", "office_parts": [], "count": 1, "grade": "正四品",
          "count_form": "P4", "count_evidence": "少卿一人，(正四品)", "note": "未明"},
         {"office": "寺丞", "office_parts": [], "count": 0, "grade": "正六品",
          "count_form": "P4", "count_evidence": "寺丞无定员，(正六品)", "note": "无定员"},
         {"office": "监正", "office_parts": [], "count": 1, "grade": "正九品",
          "count_form": "P4", "count_evidence": "各牧监，监正一人，(正九品)", "note": "各牧监各一人"},
     ], "confidence": 0.9},

    # 都转运盐使司
    {"slot": 16, "item_id": "04-047", "owner": "都转运盐使司", "rank_type": "品级员额",
     "posts": [
         {"office": "都转运使", "office_parts": [], "count": 1, "grade": "从三品",
          "count_form": "P4", "count_evidence": "都转运使一人，(从三品)", "note": "未明"},
         {"office": "同知", "office_parts": [], "count": 1, "grade": "从四品",
          "count_form": "P4", "count_evidence": "同知一人，(从四品)", "note": "未明"},
         {"office": "副使", "office_parts": [], "count": 1, "grade": "从五品",
          "count_form": "P4", "count_evidence": "副使一人，(从五品)", "note": "未明"},
         {"office": "判官", "office_parts": [], "count": 0, "grade": "从六品",
          "count_form": "P4", "count_evidence": "判官无定员。(从六品)", "note": "无定员"},
         {"office": "经历", "office_parts": [], "count": 1, "grade": "从七品",
          "count_form": "P4", "count_evidence": "经历司，经历一人，", "note": "未明"},
     ], "confidence": 0.9},

    # 盐课提举司
    {"slot": 17, "item_id": "04-049", "owner": "盐课提举司", "rank_type": "品级员额",
     "posts": [
         {"office": "提举", "office_parts": [], "count": 1, "grade": "从五品",
          "count_form": "P4", "count_evidence": "提举一人，(从五品)", "note": "未明"},
         {"office": "同提举", "office_parts": [], "count": 1, "grade": "从六品",
          "count_form": "P4", "count_evidence": "同提举一人，(从六品)", "note": "未明"},
         {"office": "副提举", "office_parts": [], "count": 0, "grade": "从七品",
          "count_form": "P4", "count_evidence": "副提举无定员。(从七品)", "note": "无定员"},
         {"office": "吏目", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "吏目一人，(从九品)", "note": "未明"},
     ], "confidence": 0.9},

    # 市舶提举司
    {"slot": 18, "item_id": "04-051", "owner": "市舶提举司", "rank_type": "品级员额",
     "posts": [
         {"office": "提举", "office_parts": [], "count": 1, "grade": "从五品",
          "count_form": "P4", "count_evidence": "提举一人，(从五品)", "note": "未明"},
         {"office": "副提举", "office_parts": [], "count": 2, "grade": "从六品",
          "count_form": "P4", "count_evidence": "副提举二人。(从六品)", "note": "未明"},
         {"office": "吏目", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "吏目一人。(从九品)", "note": "未明"},
     ], "confidence": 0.9},

    # 茶马司
    {"slot": 19, "item_id": "04-053", "owner": "茶马司", "rank_type": "品级员额",
     "posts": [
         {"office": "大使", "office_parts": [], "count": 1, "grade": "正九品",
          "count_form": "P4", "count_evidence": "大使一人，(正九品)", "note": "未明"},
         {"office": "副使", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "副使一人，(从九品)", "note": "未明"},
     ], "confidence": 0.9},
]

# ============ RANK 续：地方官机构品级员额（条37-75，v7 由 templates 转正）============
# v7（2026-10-14）：原 ORG_TEMPLATES 取消，其 posts 转入 ORG 节点后，
#   品级员额同步补入 RANK 层（RANK 是品级员额的规范归属层）。
RANK_LOCAL = [
    # 道
    {"slot": 101, "item_id": "04-037", "owner": "道", "rank_type": "品级员额",
     "posts": [
         {"office": "督粮道", "office_parts": ["督粮道"], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "督粮道，(十三布政司各一员，俱驻省城。)", "note": "十三布政司各一员，俱驻省城"},
         {"office": "分守道", "office_parts": ["分守道"], "count": 0, "grade": "未明",
          "count_form": "P4", "count_evidence": "分守道：浙江杭嘉湖道，宁绍台道，金衢严道，温处道。",
          "note": "各省不等，俱驻省或分驻"},
         {"office": "分巡道", "office_parts": ["分巡道"], "count": 0, "grade": "未明",
          "count_form": "P4", "count_evidence": "分巡道：浙江杭严道，宁绍道，嘉湖道，金衢道。", "note": "各省不等"},
         {"office": "整饬兵备道", "office_parts": ["整饬兵备道"], "count": 0, "grade": "未明",
          "count_form": "P4", "count_evidence": "整饬兵备道：浙江宁绍道，嘉兴道，温处道，台海道。", "note": "各省不等"},
     ], "confidence": 0.85},
    # 府
    {"slot": 102, "item_id": "04-054", "owner": "府", "rank_type": "品级员额",
     "posts": [
         {"office": "知府", "office_parts": [], "count": 1, "grade": "正四品",
          "count_form": "P4", "count_evidence": "知府一人，(正四品)同知，(正五品)通判无定员，(正六品)推官一人。(正七品)",
          "note": "上府从三品（洪武六年分三等：上府从三品、中府正四品、下府正四品）"},
         {"office": "同知", "office_parts": [], "count": 1, "grade": "正五品",
          "count_form": "P4", "count_evidence": "同知，(正五品)", "note": "未明"},
         {"office": "通判", "office_parts": [], "count": 0, "grade": "正六品",
          "count_form": "P4", "count_evidence": "通判无定员，(正六品)", "note": "无定员"},
         {"office": "推官", "office_parts": [], "count": 1, "grade": "正七品",
          "count_form": "P4", "count_evidence": "推官一人。(正七品)", "note": "未明"},
         {"office": "经历", "office_parts": [], "count": 1, "grade": "正八品",
          "count_form": "P4", "count_evidence": "其属，经历司经历一人，(正八品)知事一人。(正九品)", "note": "经历司"},
         {"office": "知事", "office_parts": [], "count": 1, "grade": "正九品",
          "count_form": "P4", "count_evidence": "知事一人。(正九品)", "note": "未明"},
         {"office": "照磨", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "照磨所，照磨一人，(从九品)检校一人。", "note": "照磨所"},
         {"office": "司狱", "office_parts": [], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "司狱司，司狱一人。", "note": "司狱司"},
     ], "confidence": 0.92},
    # 州
    {"slot": 103, "item_id": "04-057", "owner": "州", "rank_type": "品级员额",
     "posts": [
         {"office": "知州", "office_parts": [], "count": 1, "grade": "从五品",
          "count_form": "P4", "count_evidence": "知州一人，(从五品)", "note": "未明"},
         {"office": "同知", "office_parts": [], "count": 1, "grade": "从六品",
          "count_form": "P4", "count_evidence": "同知，(从六品)", "note": "里不及三十而无属县，裁同知、判官"},
         {"office": "判官", "office_parts": [], "count": 0, "grade": "从七品",
          "count_form": "P4", "count_evidence": "判官无定员，(从七品。", "note": "无定员；有属县，裁同知"},
         {"office": "吏目", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "其属，吏目一人，(从九品。", "note": "未明"},
     ], "confidence": 0.9},
    # 县
    {"slot": 104, "item_id": "04-059", "owner": "县", "rank_type": "品级员额",
     "posts": [
         {"office": "知县", "office_parts": [], "count": 1, "grade": "正七品",
          "count_form": "P4", "count_evidence": "知县一人，(正七品)",
          "note": "上县从六品、中县正七品、下县从七品（吴元年初定，后并为正七品）"},
         {"office": "县丞", "office_parts": [], "count": 1, "grade": "正八品",
          "count_form": "P4", "count_evidence": "县丞一人，(正八品)", "note": "未明"},
         {"office": "主簿", "office_parts": [], "count": 1, "grade": "正九品",
          "count_form": "P4", "count_evidence": "主簿一人，(正九品)", "note": "未明"},
         {"office": "典史", "office_parts": [], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "其属，典史一人。(所辖别见)", "note": "未明"},
     ], "confidence": 0.92},
    # 儒学
    {"slot": 105, "item_id": "04-062", "owner": "儒学", "rank_type": "品级员额",
     "posts": [
         {"office": "教授", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "儒学。府，教授一人，(从九品)训导四人。", "note": "府学"},
         {"office": "训导", "office_parts": [], "count": 4, "grade": "未明",
          "count_form": "P4", "count_evidence": "教授一人，(从九品)训导四人。", "note": "府学四人；州学三人；县学二人"},
         {"office": "学正", "office_parts": [], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "州，学正一人，训导三人。", "note": "州学"},
         {"office": "教谕", "office_parts": [], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "县，教谕一人，训导二人。", "note": "县学"},
     ], "confidence": 0.92},
    # 巡检司
    {"slot": 106, "item_id": "04-064", "owner": "巡检司", "rank_type": "品级员额",
     "posts": [
         {"office": "巡检", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "巡检司。巡检、副巡检，(俱从九品)", "note": "各府州县有无多寡不同"},
         {"office": "副巡检", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "巡检、副巡检，(俱从九品)", "note": "未明"},
     ], "confidence": 0.9},
    # 驿
    {"slot": 107, "item_id": "04-065", "owner": "驿", "rank_type": "品级员额",
     "posts": [
         {"office": "驿丞", "office_parts": [], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "驿。驿丞典邮传迎送之事。", "note": "各府州县有无多寡不同"},
     ], "confidence": 0.9},
    # 税课司
    {"slot": 108, "item_id": "04-066", "owner": "税课司", "rank_type": "品级员额",
     "posts": [
         {"office": "大使", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "大使一人，(从九品)典税事。", "note": "府曰司，县曰局"},
     ], "confidence": 0.9},
    # 仓
    {"slot": 109, "item_id": "04-067", "owner": "仓", "rank_type": "品级员额",
     "posts": [
         {"office": "大使", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "仓。大使一人，(府从九品，州县未入流)", "note": "府从九品，州县未入流"},
         {"office": "副使", "office_parts": [], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "副使一人，库大使一人。(州县设。)", "note": "州县设"},
     ], "confidence": 0.88},
    # 织染杂造局
    {"slot": 110, "item_id": "04-068", "owner": "织染杂造局", "rank_type": "品级员额",
     "posts": [
         {"office": "大使", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "织染杂造局。大使一人，(从九品，州织染局未入流。)", "note": "州织染局未入流"},
         {"office": "副使", "office_parts": [], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "副使一人。", "note": "未明"},
     ], "confidence": 0.88},
    # 河泊所闸坝官
    {"slot": 111, "item_id": "04-069", "owner": "河泊所闸坝官", "rank_type": "品级员额",
     "posts": [
         {"office": "河泊所官", "office_parts": ["河泊所官"], "count": 0, "grade": "未明",
          "count_form": "P4", "count_evidence": "河泊所官，掌收鱼税；",
          "note": "岁课粮五千石以上至万石者设官三人，千石以上者二人"},
         {"office": "闸官、坝官", "office_parts": ["闸官", "坝官"], "count": 0, "grade": "未明",
          "count_form": "P4", "count_evidence": "闸官、坝官，掌启闭蓄泄。", "note": "无定员"},
     ], "confidence": 0.88},
    # 批验所
    {"slot": 112, "item_id": "04-070", "owner": "批验所", "rank_type": "品级员额",
     "posts": [
         {"office": "大使", "office_parts": [], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "批验所。大使一人，副使一人，掌验茶盐引。", "note": "未明"},
         {"office": "副使", "office_parts": [], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "大使一人，副使一人，掌验茶盐引。", "note": "未明"},
     ], "confidence": 0.88},
    # 递运所
    {"slot": 113, "item_id": "04-071", "owner": "递运所", "rank_type": "品级员额",
     "posts": [
         {"office": "大使", "office_parts": [], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "递运所。大使一人，副使一人，掌运递粮物。", "note": "未明"},
         {"office": "副使", "office_parts": [], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "大使一人，副使一人，掌运递粮物。", "note": "未明"},
     ], "confidence": 0.88},
    # 铁冶所
    {"slot": 114, "item_id": "04-072", "owner": "铁冶所", "rank_type": "品级员额",
     "posts": [
         {"office": "大使", "office_parts": [], "count": 1, "grade": "未入流",
          "count_form": "P4", "count_evidence": "铁冶所。大使一人，副使一人。洪武七年初置。", "note": "初正八品，后为未入流"},
         {"office": "副使", "office_parts": [], "count": 1, "grade": "未入流",
          "count_form": "P4", "count_evidence": "每所置大使、副使各一人。", "note": "初正九品，后为未入流"},
     ], "confidence": 0.88},
    # 医学
    {"slot": 115, "item_id": "04-073", "owner": "医学", "rank_type": "品级员额",
     "posts": [
         {"office": "正科", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "医学。府，正科一人。(从九品)", "note": "府；州曰典科，县曰训科"},
     ], "confidence": 0.88},
    # 阴阳学
    {"slot": 116, "item_id": "04-074", "owner": "阴阳学", "rank_type": "品级员额",
     "posts": [
         {"office": "正术", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "阴阳学。府，正术一人。(从九品)", "note": "府；州曰典术，县曰训术"},
     ], "confidence": 0.88},
    # 僧纲司道纪司
    {"slot": 117, "item_id": "04-075", "owner": "僧纲司道纪司", "rank_type": "品级员额",
     "posts": [
         {"office": "都纲", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "府僧纲司，都纲一人，(从九品)副都纲一人。", "note": "府僧纲司"},
         {"office": "僧正", "office_parts": [], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "州僧正司，僧正一人。", "note": "州僧正司"},
         {"office": "僧会", "office_parts": [], "count": 1, "grade": "未明",
          "count_form": "P4", "count_evidence": "县僧会司，僧会一人。", "note": "县僧会司"},
         {"office": "都纪", "office_parts": [], "count": 1, "grade": "从九品",
          "count_form": "P4", "count_evidence": "府道纪司，都纪一人，(从九品)副都纪一人。", "note": "府道纪司"},
     ], "confidence": 0.88},
]

RANKS = RANKS + RANK_LOCAL
# v7（2026-10-14）：原 ORG_TEMPLATES 容器取消。用户裁定：府/州/县/道/儒学/杂职等
#   首先是正式机构，应在 ORG 树中占节点；「通用编制」只是其编制可复用的额外属性。
#   原 17 条模板全部转为 ORGS 正式节点，parent 依原文隶属关系：
#     道（条37-42）     → parent="天子"（布政司/按察司分司，跨司分职）
#     府/州/县（条54-61）→ 府 parent="天子"；州/县 parent="府"（地方行政三级树）
#     儒学/杂职（条62-75）→ parent="府"（各府州县属机构）
ORG_LOCAL = [
    # ---- 道制（条37-42）----
    {"slot": 101, "item_id": "04-037", "name": "道", "level": "道", "org_type": "地方",
     "parent": "天子", "core_officials": ["参政", "参议", "副使", "佥事"], "total_posts": 0,
     "note": "布政司参政参议分守道 + 按察司副使佥事分巡道/兵备道等。"
             "督粮道十三布政司各一员俱驻省城；分守道/分巡道/整饬兵备道各省不等",
     "children": [], "ent_ids": [], "confidence": 0.85,
     "instances": [
         "浙江杭嘉湖道", "浙江宁绍台道", "浙江金衢严道", "浙江温处道",
         "江西南瑞道", "江西湖东道", "江西湖西道", "江西饶南九江道", "江西赣南道",
         "山东济南道", "山东东兖道", "山东海右道",
         "山西冀宁道", "山西河东道", "山西冀北道", "山西冀南道",
         "陕西关内道", "陕西关西道", "陕西西宁道", "陕西关南道", "陕西河西道", "陕西陇右道",
         "河南大梁道", "河南河南道", "河南汝南道", "河南河北道",
         "湖广武昌道", "湖广下荆南道", "湖广上荆南道", "湖广荆西道", "湖广湖北道",
         "湖广上湖南道", "湖广下湖南道", "湖广沅靖道",
         "浙江杭严道", "浙江宁绍道", "浙江嘉湖道", "浙江金衢道",
         "山东兖州道", "山东济宁道", "山东青州海防道", "山东海道", "山东登莱道", "山东辽海道",
         "山西雁门道", "福建巡海道", "福建福宁道", "福建兴泉道", "福建建南道",
         "福建武平道", "福建漳南道", "福建建宁道",
         "浙江嘉兴道", "浙江台海道", "江西广建道", "山东临清道", "山东武德道", "山东曹濮道",
         "协堂道", "水利道", "屯田道", "管河道", "盐法道",
     ]},
    # ---- 府（条54-56）----
    {"slot": 102, "item_id": "04-054", "name": "府", "level": "府", "org_type": "地方",
     "parent": "天子", "core_officials": ["知府", "同知", "通判", "推官"], "total_posts": 0,
     "note": "各府通用编制。洪武六年分天下府三等：粮二十万石以上为上府（知府从三品），"
             "二十万石以下为中府（正四品），十万石以下为下府。所辖州县别见",
     "children": [
         # 州/县/儒学/杂职 12 项由本卷 v7 升为独立 ORG 节点（条57-75），
         # 此处按树内边列入 府.children（节点内容由各自 ORG 记录承载，此处作引用占位）。
         {"name": "州", "level": "州县", "parent": "府", "posts": [], "children": []},
         {"name": "县", "level": "州县", "parent": "府", "posts": [], "children": []},
         {"name": "儒学", "level": "杂职", "parent": "府", "posts": [], "children": []},
         {"name": "巡检司", "level": "杂职", "parent": "府", "posts": [], "children": []},
         {"name": "驿", "level": "杂职", "parent": "府", "posts": [], "children": []},
         {"name": "税课司", "level": "杂职", "parent": "府", "posts": [], "children": []},
         {"name": "仓", "level": "杂职", "parent": "府", "posts": [], "children": []},
         {"name": "织染杂造局", "level": "杂职", "parent": "府", "posts": [], "children": []},
         {"name": "河泊所闸坝官", "level": "杂职", "parent": "府", "posts": [], "children": []},
         {"name": "批验所", "level": "杂职", "parent": "府", "posts": [], "children": []},
         {"name": "递运所", "level": "杂职", "parent": "府", "posts": [], "children": []},
         {"name": "铁冶所", "level": "杂职", "parent": "府", "posts": [], "children": []},
         {"name": "医学", "level": "杂职", "parent": "府", "posts": [], "children": []},
         {"name": "阴阳学", "level": "杂职", "parent": "府", "posts": [], "children": []},
         {"name": "僧纲司道纪司", "level": "杂职", "parent": "府", "posts": [], "children": []},
     ], "ent_ids": [], "confidence": 0.92,
     "posts": [
         {"office": "知府", "count": 1, "grade": "正四品", "note": "上府从三品（洪武六年分三等）",
          "count_form": "P4", "count_evidence": "知府一人，(正四品)同知，(正五品)通判无定员，(正六品)推官一人。(正七品)"},
         {"office": "同知", "count": 1, "grade": "正五品", "note": "未明",
          "count_form": "P4", "count_evidence": "同知，(正五品)"},
         {"office": "通判", "count": 0, "grade": "正六品", "note": "无定员",
          "count_form": "P4", "count_evidence": "通判无定员，(正六品)"},
         {"office": "推官", "count": 1, "grade": "正七品", "note": "未明",
          "count_form": "P4", "count_evidence": "推官一人。(正七品)"},
         {"office": "经历", "count": 1, "grade": "正八品", "note": "经历司",
          "count_form": "P4", "count_evidence": "其属，经历司经历一人，(正八品)知事一人。(正九品)"},
         {"office": "知事", "count": 1, "grade": "正九品", "note": "未明",
          "count_form": "P4", "count_evidence": "知事一人。(正九品)"},
         {"office": "照磨", "count": 1, "grade": "从九品", "note": "照磨所",
          "count_form": "P4", "count_evidence": "照磨所，照磨一人，(从九品)检校一人。"},
         {"office": "司狱", "count": 1, "grade": "未明", "note": "司狱司",
          "count_form": "P4", "count_evidence": "司狱司，司狱一人。"},
     ]},
    # ---- 州（条57-58）----
    {"slot": 103, "item_id": "04-057", "name": "州", "level": "州县", "org_type": "地方",
     "parent": "府", "core_officials": ["知州", "同知", "判官", "吏目"], "total_posts": 0,
     "note": "各州通用编制。凡州二：有属州（视县），有直隶州（视府），而品秩则同。"
             "里不及三十而无属县，裁同知、判官",
     "children": [], "ent_ids": [], "confidence": 0.9,
     "posts": [
         {"office": "知州", "count": 1, "grade": "从五品", "note": "未明",
          "count_form": "P4", "count_evidence": "知州一人，(从五品)"},
         {"office": "同知", "count": 1, "grade": "从六品", "note": "里不及三十而无属县，裁同知、判官",
          "count_form": "P4", "count_evidence": "同知，(从六品)"},
         {"office": "判官", "count": 0, "grade": "从七品", "note": "无定员；有属县，裁同知",
          "count_form": "P4", "count_evidence": "判官无定员，(从七品。"},
         {"office": "吏目", "count": 1, "grade": "从九品", "note": "未明",
          "count_form": "P4", "count_evidence": "其属，吏目一人，(从九品。"},
     ]},
    # ---- 县（条59-61）----
    {"slot": 104, "item_id": "04-059", "name": "县", "level": "州县", "org_type": "地方",
     "parent": "府", "core_officials": ["知县", "县丞", "主簿", "典史"], "total_posts": 0,
     "note": "各县通用编制。吴元年定县三等：粮十万石以下为上县（从六品），六万石以下为中县"
             "（正七品），三万石以下为下县（从七品），后并为正七品",
     "children": [], "ent_ids": [], "confidence": 0.92,
     "posts": [
         {"office": "知县", "count": 1, "grade": "正七品",
          "note": "上县从六品、中县正七品、下县从七品（吴元年初定，后并为正七品）",
          "count_form": "P4", "count_evidence": "知县一人，(正七品)"},
         {"office": "县丞", "count": 1, "grade": "正八品", "note": "未明",
          "count_form": "P4", "count_evidence": "县丞一人，(正八品)"},
         {"office": "主簿", "count": 1, "grade": "正九品", "note": "未明",
          "count_form": "P4", "count_evidence": "主簿一人，(正九品)"},
         {"office": "典史", "count": 1, "grade": "未明", "note": "未明",
          "count_form": "P4", "count_evidence": "其属，典史一人。(所辖别见)"},
     ]},
    # ---- 儒学（条62-63）----
    {"slot": 105, "item_id": "04-062", "name": "儒学", "level": "杂职", "org_type": "地方",
     "parent": "府", "core_officials": ["教授", "学正", "教谕", "训导"], "total_posts": 0,
     "note": "府/州/县三级儒学。府曰教授，州曰学正，县曰教谕；洪武二年诏天下府州县皆立学",
     "children": [], "ent_ids": [], "confidence": 0.92,
     "posts": [
         {"office": "教授", "count": 1, "grade": "从九品", "note": "府学",
          "count_form": "P4", "count_evidence": "儒学。府，教授一人，(从九品)训导四人。"},
         {"office": "训导", "count": 4, "grade": "未明", "note": "府学四人；州学三人；县学二人",
          "count_form": "P4", "count_evidence": "教授一人，(从九品)训导四人。"},
         {"office": "学正", "count": 1, "grade": "未明", "note": "州学",
          "count_form": "P4", "count_evidence": "州，学正一人，训导三人。"},
         {"office": "教谕", "count": 1, "grade": "未明", "note": "县学",
          "count_form": "P4", "count_evidence": "县，教谕一人，训导二人。"},
     ]},
    # ---- 巡检司（条64）----
    {"slot": 106, "item_id": "04-064", "name": "巡检司", "level": "杂职", "org_type": "地方",
     "parent": "府", "core_officials": ["巡检", "副巡检"], "total_posts": 0,
     "note": "凡在外各府州县关津要害处俱设；洪武二年始于广西关隘冲要之处设，后遂增置各处",
     "children": [], "ent_ids": [], "confidence": 0.9,
     "posts": [
         {"office": "巡检", "count": 1, "grade": "从九品", "note": "各府州县有无多寡不同",
          "count_form": "P4", "count_evidence": "巡检司。巡检、副巡检，(俱从九品)"},
         {"office": "副巡检", "count": 1, "grade": "从九品", "note": "未明",
          "count_form": "P4", "count_evidence": "巡检、副巡检，(俱从九品)"},
     ]},
    # ---- 驿（条65）----
    {"slot": 107, "item_id": "04-065", "name": "驿", "level": "杂职", "org_type": "地方",
     "parent": "府", "core_officials": ["驿丞"], "total_posts": 0,
     "note": "驿丞典邮传迎送之事；各府州县有无多寡不同",
     "children": [], "ent_ids": [], "confidence": 0.9,
     "posts": [
         {"office": "驿丞", "count": 1, "grade": "未明", "note": "各府州县有无多寡不同",
          "count_form": "P4", "count_evidence": "驿。驿丞典邮传迎送之事。"},
     ]},
    # ---- 税课司（条66）----
    {"slot": 108, "item_id": "04-066", "name": "税课司", "level": "杂职", "org_type": "地方",
     "parent": "府", "core_officials": ["大使"], "total_posts": 0,
     "note": "府曰司，县曰局。典税事；明初改在京官店为宣课司，府州县官店为通课司，后改通课司为税课司、局",
     "children": [], "ent_ids": [], "confidence": 0.9,
     "posts": [
         {"office": "大使", "count": 1, "grade": "从九品", "note": "未明",
          "count_form": "P4", "count_evidence": "大使一人，(从九品)典税事。"},
     ]},
    # ---- 仓（条67）----
    {"slot": 109, "item_id": "04-067", "name": "仓", "level": "杂职", "org_type": "地方",
     "parent": "府", "core_officials": ["大使", "副使"], "total_posts": 0,
     "note": "府从九品，州县未入流",
     "children": [], "ent_ids": [], "confidence": 0.88,
     "posts": [
         {"office": "大使", "count": 1, "grade": "从九品", "note": "府从九品，州县未入流",
          "count_form": "P4", "count_evidence": "仓。大使一人，(府从九品，州县未入流)"},
         {"office": "副使", "count": 1, "grade": "未明", "note": "州县设",
          "count_form": "P4", "count_evidence": "副使一人，库大使一人。(州县设。)"},
     ]},
    # ---- 织染杂造局（条68）----
    {"slot": 110, "item_id": "04-068", "name": "织染杂造局", "level": "杂职", "org_type": "地方",
     "parent": "府", "core_officials": ["大使", "副使"], "total_posts": 0,
     "note": "府/州；州织染局未入流",
     "children": [], "ent_ids": [], "confidence": 0.88,
     "posts": [
         {"office": "大使", "count": 1, "grade": "从九品", "note": "州织染局未入流",
          "count_form": "P4", "count_evidence": "织染杂造局。大使一人，(从九品，州织染局未入流。)"},
         {"office": "副使", "count": 1, "grade": "未明", "note": "未明",
          "count_form": "P4", "count_evidence": "副使一人。"},
     ]},
    # ---- 河泊所 / 闸坝官（条69）----
    {"slot": 111, "item_id": "04-069", "name": "河泊所闸坝官", "level": "杂职", "org_type": "地方",
     "parent": "府", "core_officials": ["河泊所官", "闸官", "坝官"], "total_posts": 0,
     "note": "洪武十五年定天下河泊所凡二百五十二；闸官、坝官掌启闭蓄泄，无定员",
     "children": [], "ent_ids": [], "confidence": 0.88,
     "posts": [
         {"office": "河泊所官", "count": 0, "grade": "未明",
          "note": "岁课粮五千石以上至万石者设官三人，千石以上者二人",
          "count_form": "P4", "count_evidence": "河泊所官，掌收鱼税；"},
         {"office": "闸官、坝官", "office_parts": ["闸官", "坝官"], "count": 0, "grade": "未明",
          "note": "无定员",
          "count_form": "P4", "count_evidence": "闸官、坝官，掌启闭蓄泄。"},
     ]},
    # ---- 批验所（条70）----
    {"slot": 112, "item_id": "04-070", "name": "批验所", "level": "杂职", "org_type": "地方",
     "parent": "府", "core_officials": ["大使", "副使"], "total_posts": 2,
     "note": "掌验茶盐引",
     "children": [], "ent_ids": [], "confidence": 0.88,
     "posts": [
         {"office": "大使", "count": 1, "grade": "未明", "note": "未明",
          "count_form": "P4", "count_evidence": "批验所。大使一人，副使一人，掌验茶盐引。"},
         {"office": "副使", "count": 1, "grade": "未明", "note": "未明",
          "count_form": "P4", "count_evidence": "大使一人，副使一人，掌验茶盐引。"},
     ]},
    # ---- 递运所（条71）----
    {"slot": 113, "item_id": "04-071", "name": "递运所", "level": "杂职", "org_type": "地方",
     "parent": "府", "core_officials": ["大使", "副使"], "total_posts": 2,
     "note": "洪武九年始置；先是，在外多以卫所戍守军士传送军囚，太祖以其有妨练习守御，乃命兵部增置",
     "children": [], "ent_ids": [], "confidence": 0.88,
     "posts": [
         {"office": "大使", "count": 1, "grade": "未明", "note": "未明",
          "count_form": "P4", "count_evidence": "递运所。大使一人，副使一人，掌运递粮物。"},
         {"office": "副使", "count": 1, "grade": "未明", "note": "未明",
          "count_form": "P4", "count_evidence": "大使一人，副使一人，掌运递粮物。"},
     ]},
    # ---- 铁冶所（条72）----
    {"slot": 114, "item_id": "04-072", "name": "铁冶所", "level": "杂职", "org_type": "地方",
     "parent": "府", "core_officials": ["大使", "副使"], "total_posts": 0,
     "note": "洪武七年初置，凡十三所；初大使正八品、副使正九品，后俱为未入流",
     "children": [], "ent_ids": [], "confidence": 0.88,
     "posts": [
         {"office": "大使", "count": 1, "grade": "未入流", "note": "初正八品，后为未入流",
          "count_form": "P4", "count_evidence": "铁冶所。大使一人，副使一人。洪武七年初置。"},
         {"office": "副使", "count": 1, "grade": "未入流", "note": "初正九品，后为未入流",
          "count_form": "P4", "count_evidence": "每所置大使、副使各一人。"},
     ]},
    # ---- 医学（条73）----
    {"slot": 115, "item_id": "04-073", "name": "医学", "level": "杂职", "org_type": "地方",
     "parent": "府", "core_officials": ["正科"], "total_posts": 0,
     "note": "洪武十七年置，设官不给禄；府曰正科，州曰典科，县曰训科",
     "children": [], "ent_ids": [], "confidence": 0.88,
     "posts": [
         {"office": "正科", "count": 1, "grade": "从九品", "note": "府；州曰典科，县曰训科",
          "count_form": "P4", "count_evidence": "医学。府，正科一人。(从九品)"},
     ]},
    # ---- 阴阳学（条74）----
    {"slot": 116, "item_id": "04-074", "name": "阴阳学", "level": "杂职", "org_type": "地方",
     "parent": "府", "core_officials": ["正术"], "total_posts": 0,
     "note": "亦洪武十七年置，设官不给禄；府曰正术，州曰典术，县曰训术",
     "children": [], "ent_ids": [], "confidence": 0.88,
     "posts": [
         {"office": "正术", "count": 1, "grade": "从九品", "note": "府；州曰典术，县曰训术",
          "count_form": "P4", "count_evidence": "阴阳学。府，正术一人。(从九品)"},
     ]},
    # ---- 僧纲司 / 道纪司（条75）----
    {"slot": 117, "item_id": "04-075", "name": "僧纲司道纪司", "level": "杂职", "org_type": "地方",
     "parent": "府", "core_officials": ["都纲", "僧正", "僧会", "都纪"], "total_posts": 0,
     "note": "府僧纲司、州僧正司、县僧会司；府道纪司、州道正司、县道会司",
     "children": [], "ent_ids": [], "confidence": 0.88,
     "posts": [
         {"office": "都纲", "count": 1, "grade": "从九品", "note": "府僧纲司",
          "count_form": "P4", "count_evidence": "府僧纲司，都纲一人，(从九品)副都纲一人。"},
         {"office": "僧正", "count": 1, "grade": "未明", "note": "州僧正司",
          "count_form": "P4", "count_evidence": "州僧正司，僧正一人。"},
         {"office": "僧会", "count": 1, "grade": "未明", "note": "县僧会司",
          "count_form": "P4", "count_evidence": "县僧会司，僧会一人。"},
         {"office": "都纪", "count": 1, "grade": "从九品", "note": "府道纪司",
          "count_form": "P4", "count_evidence": "府道纪司，都纪一人，(从九品)副都纪一人。"},
     ]},
]

ORGS = ORGS + ORG_LOCAL

# ============ LINE 隶属统辖 ============
LINES = [
    # 南京官（跨树边：直隶天子）
    {"slot": 1, "item_id": "04-001", "subordinate": "南京宗人府", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京官品秩，俱同北京", "ent_ids": [], "confidence": 0.88},
    {"slot": 2, "item_id": "04-001", "subordinate": "经历司", "superior": "南京宗人府",
     "line_type": "统辖", "level_gap": 1, "note": "经历司", "ent_ids": [], "confidence": 0.92},
    {"slot": 3, "item_id": "04-002", "subordinate": "南京吏部", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京六部，品秩俱同北京", "ent_ids": [], "confidence": 0.88},
    {"slot": 4, "item_id": "04-002", "subordinate": "司务厅", "superior": "南京吏部",
     "line_type": "统辖", "level_gap": 1, "note": "其属，司务厅", "ent_ids": [], "confidence": 0.92},
    {"slot": 5, "item_id": "04-002", "subordinate": "四清吏司", "superior": "南京吏部",
     "line_type": "统辖", "level_gap": 1, "note": "文选、考功、验封、稽勋四清吏司", "ent_ids": [], "confidence": 0.92},
    {"slot": 6, "item_id": "04-003", "subordinate": "南京户部", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京六部，品秩俱同北京", "ent_ids": [], "confidence": 0.88},
    {"slot": 7, "item_id": "04-003", "subordinate": "十三司", "superior": "南京户部",
     "line_type": "统辖", "level_gap": 1, "note": "十三司", "ent_ids": [], "confidence": 0.92},
    {"slot": 8, "item_id": "04-005", "subordinate": "南京礼部", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京六部，品秩俱同北京", "ent_ids": [], "confidence": 0.88},
    {"slot": 9, "item_id": "04-005", "subordinate": "四司", "superior": "南京礼部",
     "line_type": "统辖", "level_gap": 1, "note": "仪制、祠祭、主客、精膳四司", "ent_ids": [], "confidence": 0.92},
    {"slot": 10, "item_id": "04-005", "subordinate": "铸印局", "superior": "南京礼部",
     "line_type": "统辖", "level_gap": 1, "note": "所辖，铸印局", "ent_ids": [], "confidence": 0.92},
    {"slot": 11, "item_id": "04-006", "subordinate": "南京兵部", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京六部，品秩俱同北京", "ent_ids": [], "confidence": 0.88},
    {"slot": 12, "item_id": "04-006", "subordinate": "四司", "superior": "南京兵部",
     "line_type": "统辖", "level_gap": 1, "note": "武选、职方、车驾、武库四司", "ent_ids": [], "confidence": 0.92},
    {"slot": 13, "item_id": "04-006", "subordinate": "典牧所", "superior": "南京兵部",
     "line_type": "统辖", "level_gap": 1, "note": "所辖，典牧所", "ent_ids": [], "confidence": 0.92},
    {"slot": 14, "item_id": "04-006", "subordinate": "会同馆", "superior": "南京兵部",
     "line_type": "统辖", "level_gap": 1, "note": "会同馆", "ent_ids": [], "confidence": 0.92},
    {"slot": 15, "item_id": "04-006", "subordinate": "大胜关", "superior": "南京兵部",
     "line_type": "统辖", "level_gap": 1, "note": "大胜关", "ent_ids": [], "confidence": 0.92},
    {"slot": 16, "item_id": "04-007", "subordinate": "南京刑部", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京六部，品秩俱同北京", "ent_ids": [], "confidence": 0.88},
    {"slot": 17, "item_id": "04-007", "subordinate": "十三司", "superior": "南京刑部",
     "line_type": "统辖", "level_gap": 1, "note": "十三司", "ent_ids": [], "confidence": 0.92},
    {"slot": 18, "item_id": "04-007", "subordinate": "司狱司", "superior": "南京刑部",
     "line_type": "统辖", "level_gap": 1, "note": "司狱司", "ent_ids": [], "confidence": 0.92},
    {"slot": 19, "item_id": "04-008", "subordinate": "南京工部", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京六部，品秩俱同北京", "ent_ids": [], "confidence": 0.88},
    {"slot": 20, "item_id": "04-008", "subordinate": "四司", "superior": "南京工部",
     "line_type": "统辖", "level_gap": 1, "note": "营缮、虞衡、都水、屯田四司", "ent_ids": [], "confidence": 0.92},
    {"slot": 21, "item_id": "04-009", "subordinate": "南京都察院", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京都察院", "ent_ids": [], "confidence": 0.88},
    {"slot": 22, "item_id": "04-011", "subordinate": "南京通政使司", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "掌收呈状，付刑部审理", "ent_ids": [], "confidence": 0.88},
    {"slot": 23, "item_id": "04-012", "subordinate": "南京大理寺", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京大理寺", "ent_ids": [], "confidence": 0.88},
    {"slot": 24, "item_id": "04-013", "subordinate": "南京詹事府", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京詹事府", "ent_ids": [], "confidence": 0.85},
    {"slot": 25, "item_id": "04-014", "subordinate": "南京翰林院", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京翰林院", "ent_ids": [], "confidence": 0.85},
    {"slot": 26, "item_id": "04-015", "subordinate": "南京国子监", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京国子监", "ent_ids": [], "confidence": 0.88},
    {"slot": 27, "item_id": "04-016", "subordinate": "南京太常寺", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京太常寺", "ent_ids": [], "confidence": 0.88},
    {"slot": 28, "item_id": "04-017", "subordinate": "南京光禄寺", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京光禄寺", "ent_ids": [], "confidence": 0.88},
    {"slot": 29, "item_id": "04-018", "subordinate": "南京太仆寺", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京太仆寺", "ent_ids": [], "confidence": 0.88},
    {"slot": 30, "item_id": "04-019", "subordinate": "南京鸿胪寺", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京鸿胪寺", "ent_ids": [], "confidence": 0.88},
    {"slot": 31, "item_id": "04-020", "subordinate": "南京尚宝司", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京尚宝司", "ent_ids": [], "confidence": 0.85},
    {"slot": 32, "item_id": "04-021", "subordinate": "南京六科", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京六科", "ent_ids": [], "confidence": 0.88},
    {"slot": 33, "item_id": "04-022", "subordinate": "南京行人司", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京行人司", "ent_ids": [], "confidence": 0.85},
    {"slot": 34, "item_id": "04-023", "subordinate": "南京钦天监", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京钦天监", "ent_ids": [], "confidence": 0.88},
    {"slot": 35, "item_id": "04-024", "subordinate": "南京太医院", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京太医院", "ent_ids": [], "confidence": 0.88},
    {"slot": 36, "item_id": "04-025", "subordinate": "南京五城兵马司", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京五城兵马司", "ent_ids": [], "confidence": 0.88},
    {"slot": 37, "item_id": "04-004", "subordinate": "南京总督粮储", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京特设，北京无对应", "ent_ids": [], "confidence": 0.85},
    {"slot": 38, "item_id": "04-010", "subordinate": "南京提督操江", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京特设，领上、下江防之事", "ent_ids": [], "confidence": 0.85},
    {"slot": 39, "item_id": "04-026", "subordinate": "应天府", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "南京京府；对应北京顺天府", "ent_ids": [], "confidence": 0.9},
    {"slot": 40, "item_id": "04-026", "subordinate": "宛平县", "superior": "应天府",
     "line_type": "统辖", "level_gap": 1, "note": "所辖，上元、江宁二县", "ent_ids": [], "confidence": 0.9},
    {"slot": 41, "item_id": "04-026", "subordinate": "江宁", "superior": "应天府",
     "line_type": "统辖", "level_gap": 1, "note": "所辖二县", "ent_ids": [], "confidence": 0.9},
    {"slot": 42, "item_id": "04-026", "subordinate": "司狱司", "superior": "应天府",
     "line_type": "统辖", "level_gap": 1, "note": "司狱司", "ent_ids": [], "confidence": 0.92},
    {"slot": 43, "item_id": "04-026", "subordinate": "织染局", "superior": "应天府",
     "line_type": "统辖", "level_gap": 1, "note": "织染局", "ent_ids": [], "confidence": 0.92},
    # 条27 虚拟锚点
    {"slot": 44, "item_id": "04-027", "subordinate": "南京官", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "虚拟锚点：南京官制整体沿革", "ent_ids": [], "confidence": 0.8},
    # 王府长史司
    {"slot": 45, "item_id": "04-028", "subordinate": "王府长史司", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "王府官属，隶宗人府/礼部", "ent_ids": [], "confidence": 0.85},
    {"slot": 46, "item_id": "04-028", "subordinate": "审理所", "superior": "王府长史司",
     "line_type": "统辖", "level_gap": 1, "note": "所辖，审理所", "ent_ids": [], "confidence": 0.92},
    {"slot": 47, "item_id": "04-028", "subordinate": "典膳所", "superior": "王府长史司",
     "line_type": "统辖", "level_gap": 1, "note": "典膳所", "ent_ids": [], "confidence": 0.92},
    {"slot": 48, "item_id": "04-028", "subordinate": "奉祠所", "superior": "王府长史司",
     "line_type": "统辖", "level_gap": 1, "note": "奉祠所", "ent_ids": [], "confidence": 0.92},
    {"slot": 49, "item_id": "04-028", "subordinate": "典宝所", "superior": "王府长史司",
     "line_type": "统辖", "level_gap": 1, "note": "典宝所", "ent_ids": [], "confidence": 0.92},
    {"slot": 50, "item_id": "04-028", "subordinate": "纪善所", "superior": "王府长史司",
     "line_type": "统辖", "level_gap": 1, "note": "纪善所", "ent_ids": [], "confidence": 0.92},
    {"slot": 51, "item_id": "04-028", "subordinate": "良医所", "superior": "王府长史司",
     "line_type": "统辖", "level_gap": 1, "note": "良医所", "ent_ids": [], "confidence": 0.92},
    {"slot": 52, "item_id": "04-028", "subordinate": "典仪所", "superior": "王府长史司",
     "line_type": "统辖", "level_gap": 1, "note": "典仪所", "ent_ids": [], "confidence": 0.92},
    {"slot": 53, "item_id": "04-028", "subordinate": "工正所", "superior": "王府长史司",
     "line_type": "统辖", "level_gap": 1, "note": "工正所", "ent_ids": [], "confidence": 0.92},
    {"slot": 54, "item_id": "04-028", "subordinate": "典簿", "superior": "王府长史司",
     "line_type": "统辖", "level_gap": 1, "note": "其属，典簿一人", "ent_ids": [], "confidence": 0.92},
    {"slot": 55, "item_id": "04-028", "subordinate": "郡王府", "superior": "王府长史司",
     "line_type": "统辖", "level_gap": 1, "note": "郡王府，教授一人，典膳一人", "ent_ids": [], "confidence": 0.9},
    {"slot": 56, "item_id": "04-028", "subordinate": "镇国将军府", "superior": "王府长史司",
     "line_type": "统辖", "level_gap": 1, "note": "镇国将军教授一人", "ent_ids": [], "confidence": 0.9},
    # 布政/按察
    {"slot": 57, "item_id": "04-031", "subordinate": "承宣布政使司", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "掌一省之政，承流宣播，以下于有司", "ent_ids": [], "confidence": 0.9},
    {"slot": 58, "item_id": "04-031", "subordinate": "经历司", "superior": "承宣布政使司",
     "line_type": "统辖", "level_gap": 1, "note": "经历司", "ent_ids": [], "confidence": 0.92},
    {"slot": 59, "item_id": "04-031", "subordinate": "照磨所", "superior": "承宣布政使司",
     "line_type": "统辖", "level_gap": 1, "note": "照磨所", "ent_ids": [], "confidence": 0.92},
    {"slot": 60, "item_id": "04-031", "subordinate": "理问所", "superior": "承宣布政使司",
     "line_type": "统辖", "level_gap": 1, "note": "理问所", "ent_ids": [], "confidence": 0.92},
    {"slot": 61, "item_id": "04-031", "subordinate": "司狱司", "superior": "承宣布政使司",
     "line_type": "统辖", "level_gap": 1, "note": "司狱司", "ent_ids": [], "confidence": 0.92},
    {"slot": 62, "item_id": "04-031", "subordinate": "杂造局", "superior": "承宣布政使司",
     "line_type": "统辖", "level_gap": 1, "note": "杂造局、军器局、宝泉局、织染局", "ent_ids": [], "confidence": 0.9},
    {"slot": 63, "item_id": "04-034", "subordinate": "提刑按察使司", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "掌一省刑名按劾之事，以振扬风纪", "ent_ids": [], "confidence": 0.9},
    {"slot": 64, "item_id": "04-034", "subordinate": "经历司", "superior": "提刑按察使司",
     "line_type": "统辖", "level_gap": 1, "note": "经历司", "ent_ids": [], "confidence": 0.92},
    {"slot": 65, "item_id": "04-034", "subordinate": "照磨所", "superior": "提刑按察使司",
     "line_type": "统辖", "level_gap": 1, "note": "照磨所", "ent_ids": [], "confidence": 0.92},
    {"slot": 66, "item_id": "04-034", "subordinate": "司狱司", "superior": "提刑按察使司",
     "line_type": "统辖", "level_gap": 1, "note": "司狱司", "ent_ids": [], "confidence": 0.92},
    # 行太仆寺/苑马寺
    {"slot": 67, "item_id": "04-043", "subordinate": "行太仆寺", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "掌各边卫所营堡之马政，以听于兵部", "ent_ids": [], "confidence": 0.88},
    {"slot": 68, "item_id": "04-043", "subordinate": "主簿", "superior": "行太仆寺",
     "line_type": "统辖", "level_gap": 1, "note": "其属，主簿一人", "ent_ids": [], "confidence": 0.92},
    {"slot": 69, "item_id": "04-045", "subordinate": "苑马寺", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "永乐四年置苑马寺凡四", "ent_ids": [], "confidence": 0.88},
    {"slot": 70, "item_id": "04-045", "subordinate": "主簿", "superior": "苑马寺",
     "line_type": "统辖", "level_gap": 1, "note": "其属，主簿一人", "ent_ids": [], "confidence": 0.92},
    {"slot": 71, "item_id": "04-045", "subordinate": "各牧监", "superior": "苑马寺",
     "line_type": "统辖", "level_gap": 1, "note": "各牧监", "ent_ids": [], "confidence": 0.92},
    {"slot": 72, "item_id": "04-045", "subordinate": "各苑", "superior": "苑马寺",
     "line_type": "统辖", "level_gap": 1, "note": "各苑", "ent_ids": [], "confidence": 0.92},
    # 盐运/盐课/市舶/茶马
    {"slot": 73, "item_id": "04-047", "subordinate": "都转运盐使司", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "掌盐监之事；凡六：两淮、两浙、长芦、河东、山东、福建", "ent_ids": [], "confidence": 0.88},
    {"slot": 74, "item_id": "04-047", "subordinate": "经历司", "superior": "都转运盐使司",
     "line_type": "统辖", "level_gap": 1, "note": "其属，经历司", "ent_ids": [], "confidence": 0.92},
    {"slot": 75, "item_id": "04-049", "subordinate": "盐课提举司", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "掌盐课", "ent_ids": [], "confidence": 0.88},
    {"slot": 76, "item_id": "04-051", "subordinate": "市舶提举司", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "掌海外诸蕃朝贡市易之事", "ent_ids": [], "confidence": 0.88},
    {"slot": 77, "item_id": "04-053", "subordinate": "茶马司", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "掌市马之事", "ent_ids": [], "confidence": 0.88},
]

# ============ LINE 续：地方官机构隶属（条37-75，v7 由 templates 转正）============
# v7：原 templates 无隶属边，转 ORG 节点后必须补边（树与边表须同源一致）。
#   道/府 parent="天子"（跨树边，不入 children[]）；
#   州/县/儒学/杂职 parent="府"（树内边，须入父节点 children[]）。
LINES_LOCAL = [
    # 道（跨树边：直隶天子，布政司/按察司分司）
    {"slot": 101, "item_id": "04-037", "subordinate": "道", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "布政司参政参议分守道、按察司副使佥事分巡道兵备道，分司诸道", "ent_ids": [], "confidence": 0.85},
    # 府（跨树边：直隶天子）
    {"slot": 102, "item_id": "04-054", "subordinate": "府", "superior": "天子",
     "line_type": "直属", "level_gap": 1, "note": "府领州县，直隶天子", "ent_ids": [], "confidence": 0.9},
    # 州（树内边：属州隶府）
    {"slot": 103, "item_id": "04-057", "subordinate": "州", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "有属州（视县）隶府，有直隶州（视府）隶天子；品秩则同", "ent_ids": [], "confidence": 0.88},
    # 县（树内边：隶府/州）
    {"slot": 104, "item_id": "04-059", "subordinate": "县", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "县隶府，府领州县", "ent_ids": [], "confidence": 0.9},
    # 儒学（树内边：隶府州县）
    {"slot": 105, "item_id": "04-062", "subordinate": "儒学", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "洪武二年诏天下府州县皆立学，府州县各设儒学", "ent_ids": [], "confidence": 0.9},
    # 杂职 12（树内边：隶府州县）
    {"slot": 106, "item_id": "04-064", "subordinate": "巡检司", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "凡在外各府州县关津要害处俱设", "ent_ids": [], "confidence": 0.88},
    {"slot": 107, "item_id": "04-065", "subordinate": "驿", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "驿丞典邮传迎送之事，各府州县有无多寡不同", "ent_ids": [], "confidence": 0.88},
    {"slot": 108, "item_id": "04-066", "subordinate": "税课司", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "府曰司，县曰局，典税事", "ent_ids": [], "confidence": 0.88},
    {"slot": 109, "item_id": "04-067", "subordinate": "仓", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "府从九品，州县未入流", "ent_ids": [], "confidence": 0.86},
    {"slot": 110, "item_id": "04-068", "subordinate": "织染杂造局", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "府织染杂造局，州织染局未入流", "ent_ids": [], "confidence": 0.86},
    {"slot": 111, "item_id": "04-069", "subordinate": "河泊所闸坝官", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "洪武十五年定天下河泊所凡二百五十二；闸官、坝官掌启闭蓄泄", "ent_ids": [], "confidence": 0.86},
    {"slot": 112, "item_id": "04-070", "subordinate": "批验所", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "掌验茶盐引", "ent_ids": [], "confidence": 0.86},
    {"slot": 113, "item_id": "04-071", "subordinate": "递运所", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "洪武九年始置，掌运递粮物", "ent_ids": [], "confidence": 0.86},
    {"slot": 114, "item_id": "04-072", "subordinate": "铁冶所", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "洪武七年初置，凡十三所", "ent_ids": [], "confidence": 0.86},
    {"slot": 115, "item_id": "04-073", "subordinate": "医学", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "洪武十七年置，设官不给禄；府曰正科，州曰典科，县曰训科", "ent_ids": [], "confidence": 0.86},
    {"slot": 116, "item_id": "04-074", "subordinate": "阴阳学", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "亦洪武十七年置，设官不给禄；府曰正术，州曰典术，县曰训术", "ent_ids": [], "confidence": 0.86},
    {"slot": 117, "item_id": "04-075", "subordinate": "僧纲司道纪司", "superior": "府",
     "line_type": "统辖", "level_gap": 1, "note": "府僧纲司、州僧正司、县僧会司；府道纪司、州道正司、县道会司", "ent_ids": [], "confidence": 0.86},
]

LINES = LINES + LINES_LOCAL

# ============ EVO 沿革阶段 ============
EVOS = [
    # 条27 南京官（虚拟锚点的沿革）
    {"slot": 1, "item_id": "04-027", "era": "永乐四年", "change_type": "初置",
     "content": "南京官，自永乐四年成祖往北京，置行部尚书，备行在九卿印以从。是时，皇太子监国，大小庶务悉以委之",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},
    {"slot": 2, "item_id": "04-027", "era": "永乐十八年", "change_type": "移驻",
     "content": "十八年，官属悉移而北，南京六部所存惟礼、刑、工三部，各一侍郎，在南之官加“南京”字于职衔上",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},
    {"slot": 3, "item_id": "04-027", "era": "仁宗时", "change_type": "复设",
     "content": "仁宗时补设官属，除“南京”字", "related_tme": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 4, "item_id": "04-027", "era": "正统六年", "change_type": "改置",
     "content": "正统六年，定制复如永乐时", "related_tme": [], "ent_ids": [], "confidence": 0.92},

    # 条29-30 王府沿革
    {"slot": 5, "item_id": "04-030", "era": "洪武三年", "change_type": "初置",
     "content": "洪武三年，置王相府，左、右相各一人，左、右傅各一人。参军府，参军一人，录事二人，纪善一人",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},
    {"slot": 6, "item_id": "04-030", "era": "洪武四年", "change_type": "改置",
     "content": "四年，更定官制（左、右相正二品，文武傅从二品，参军从五品，录事正七品，审理正正六品等）",
     "related_tme": [], "ent_ids": [], "confidence": 0.9},

    # 条33 布政司沿革
    {"slot": 7, "item_id": "04-033", "era": "戊戌", "change_type": "初置",
     "content": "初，太祖下集庆，自领江南行中书省。戊戌，置中书分省于婺州。后每略定地方，即置行省",
     "related_tme": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 8, "item_id": "04-033", "era": "洪武九年", "change_type": "改称",
     "content": "洪武九年，改行省为承宣布政使司",
     "related_tme": [], "ent_ids": [], "confidence": 0.9},

    # 条36 按察司沿革
    {"slot": 9, "item_id": "04-036", "era": "吴元年", "change_type": "初置",
     "content": "明初，置提刑按察司。吴元年，置各道按察司，设按察使，正三品，副使，正四品，佥事，正五品",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},
    {"slot": 10, "item_id": "04-036", "era": "洪武十三年", "change_type": "升秩",
     "content": "十三年，改使秩正四品，寻罢。十四年复置，并置各道按察分司",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},
    {"slot": 11, "item_id": "04-036", "era": "洪武十六年", "change_type": "改置",
     "content": "十六年，尽罢试佥事，改按察使为从三品，副使二人，从四品，佥事从五品，多寡从其分道之数",
     "related_tme": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 12, "item_id": "04-036", "era": "洪武二十二年", "change_type": "升秩",
     "content": "二十二年，复定按察使为正三品", "related_tme": [], "ent_ids": [], "confidence": 0.92},
    {"slot": 13, "item_id": "04-036", "era": "洪武二十九年", "change_type": "改置",
     "content": "二十九年，改置按察分司为四十一道", "related_tme": [], "ent_ids": [], "confidence": 0.92},

    # 条42 道制沿革
    {"slot": 14, "item_id": "04-042", "era": "明初", "change_type": "初置",
     "content": "按明初制，恐守令贪鄙不法，故于直隶府州县设巡按御史，各布政司所属设试佥事。已罢试佥事，改按察分司四十一道，此分巡之始也",
     "related_tme": [], "ent_ids": [], "confidence": 0.9},

    # 条44 行太仆寺
    {"slot": 15, "item_id": "04-044", "era": "洪武三十年", "change_type": "初置",
     "content": "洪武三十年，置行太仆寺于山西、北平、陕西、甘肃、辽东。山西、北平、陕西，每寺设少卿一人，丞三人；甘肃、辽东，每寺设少卿、丞各一人",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},

    # 条46 苑马寺
    {"slot": 16, "item_id": "04-046", "era": "永乐四年", "change_type": "初置",
     "content": "永乐四年，置苑马寺凡四：北直隶、辽东、平凉、甘肃",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},
    {"slot": 17, "item_id": "04-046", "era": "永乐五年", "change_type": "增置",
     "content": "五年，增设北直隶苑马寺六监二十四苑（顺义、长春、咸和、驯良四苑，隶清河监）",
     "related_tme": [], "ent_ids": [], "confidence": 0.9},

    # 条50 盐运司沿革
    {"slot": 18, "item_id": "04-050", "era": "吴元年", "change_type": "初置",
     "content": "明初，置都转运司于两淮。吴元年，置两浙都转运司于杭州，定都转运使秩正三品",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},

    # 条52 市舶司沿革
    {"slot": 19, "item_id": "04-052", "era": "吴元年", "change_type": "初置",
     "content": "吴元年，置市舶提举司", "related_tme": [], "ent_ids": [], "confidence": 0.92},
    {"slot": 20, "item_id": "04-052", "era": "洪武三年", "change_type": "革罢",
     "content": "洪武三年，罢太仓、黄渡市舶司", "related_tme": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 21, "item_id": "04-052", "era": "洪武七年", "change_type": "革罢",
     "content": "七年，罢福建之泉州、浙江之明州、广东之广州三市舶司",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},
    {"slot": 22, "item_id": "04-052", "era": "永乐元年", "change_type": "复设",
     "content": "永乐元年复置，设官如（旧制）", "related_tme": [], "ent_ids": [], "confidence": 0.92},

    # 条53 茶马司
    {"slot": 23, "item_id": "04-053", "era": "洪武中", "change_type": "初置",
     "content": "洪武中，置洮州、秦州、河州三茶马司，设司令、司丞。十五年改设大使",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},

    # 条54-56 府
    {"slot": 24, "item_id": "04-056", "era": "洪武六年", "change_type": "改置",
     "content": "明初，改诸路为府。洪武六年，分天下府三等：粮二十万石以上为上府，知府秩从三品；二十万石以下为中府，知府正四品；十万石以下为下府（知府从三品/正四品）",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},

    # 条59-61 县
    {"slot": 25, "item_id": "04-061", "era": "吴元年", "change_type": "改置",
     "content": "吴元年，定县三等：粮十万石以下为上县，知县从六品；六万石以下为中县，知县正七品；三万石以下为下县，知县从七品。已，并为正七品",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},

    # 条62-63 儒学
    {"slot": 26, "item_id": "04-063", "era": "洪武二年", "change_type": "初置",
     "content": "明初，置儒学提举司。洪武二年，诏天下府州县皆立学",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},
    {"slot": 27, "item_id": "04-063", "era": "洪武十三年", "change_type": "降秩",
     "content": "十三年，改各州学正为未入流（先是从九品）", "related_tme": [], "ent_ids": [], "confidence": 0.9},
    {"slot": 28, "item_id": "04-063", "era": "洪武二十四年", "change_type": "改置",
     "content": "二十四年，定儒学训导位杂职上", "related_tme": [], "ent_ids": [], "confidence": 0.9},

    # 条64 巡检司
    {"slot": 29, "item_id": "04-064", "era": "洪武二年", "change_type": "初置",
     "content": "初，洪武二年，以广西地接瑶、僮，始于关隘冲要之处设巡检司，以警奸盗，后遂增置各处",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},
    {"slot": 30, "item_id": "04-064", "era": "洪武十三年二月", "change_type": "改置",
     "content": "十三年二月，特赐敕谕之，寻改为杂职", "related_tme": [], "ent_ids": [], "confidence": 0.9},

    # 条66 税课司
    {"slot": 31, "item_id": "04-066", "era": "明初", "change_type": "改称",
     "content": "明初，改在京官店为宣课司，府州县官店为通课司，后改通课司为税课司、局",
     "related_tme": [], "ent_ids": [], "confidence": 0.9},

    # 条69 河泊所
    {"slot": 32, "item_id": "04-069", "era": "洪武十五年", "change_type": "改置",
     "content": "洪武十五年，定天下河泊所凡二百五十二", "related_tme": [], "ent_ids": [], "confidence": 0.92},

    # 条71 递运所
    {"slot": 33, "item_id": "04-071", "era": "洪武九年", "change_type": "初置",
     "content": "洪武九年始置。先是，在外多以卫所戍守军士传送军囚，太祖以其有妨练习守御，乃命兵部增置",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},

    # 条72 铁冶所
    {"slot": 34, "item_id": "04-072", "era": "洪武七年", "change_type": "初置",
     "content": "洪武七年初置。凡十三所，每所置大使、副使各一人（初，大使正八品，副使正九品，后俱为未入流）",
     "related_tme": [], "ent_ids": [], "confidence": 0.92},

    # 条73-74 医学/阴阳学
    {"slot": 35, "item_id": "04-073", "era": "洪武十七年", "change_type": "初置",
     "content": "洪武十七年置，设官不给禄", "related_tme": [], "ent_ids": [], "confidence": 0.92},
    {"slot": 36, "item_id": "04-074", "era": "洪武十七年", "change_type": "初置",
     "content": "亦洪武十七年置，设官不给禄", "related_tme": [], "ent_ids": [], "confidence": 0.92},

    # 条26 应天府
    {"slot": 37, "item_id": "04-026", "era": "洪武三年", "change_type": "升秩",
     "content": "洪武三年，改应天府知府为府尹，秩正三品，赐银印", "related_tme": [], "ent_ids": [], "confidence": 0.95},
    {"slot": 38, "item_id": "04-026", "era": "洪武十三年", "change_type": "初置",
     "content": "十三年，始立儒学", "related_tme": [], "ent_ids": [], "confidence": 0.9},
]
