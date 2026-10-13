# -*- coding: utf-8 -*-
"""G1 卷6/7 吏典名录批量 AI 源数据"""

RECORDS = [
    # ===== 卷6 京官吏典 =====
    {"id": "NAM-006-001", "item_id": "006-001", "name": "国初吏典编制通则", "nam_type": "官制名录",
     "scope": "吏部",
     "entries": [
         {"seq": 1, "office": "司吏", "count": "视政事繁简为额"},
         {"seq": 2, "office": "典吏", "count": "视政事繁简为额"},
         {"seq": 3, "office": "提控", "count": "政事益繁添设"},
         {"seq": 4, "office": "都吏", "count": "政事益繁添设"},
         {"seq": 5, "office": "人吏/胥吏/狱典/攒典", "count": "事简者裁减"},
     ]},
    {"id": "NAM-006-002", "item_id": "006-002", "name": "宗人府吏典", "nam_type": "官制名录",
     "scope": "宗人府",
     "entries": [{"seq": 1, "office": "提控", "count": "一名"}, {"seq": 2, "office": "典吏", "count": "一名"}]},
    {"id": "NAM-006-003", "item_id": "006-003", "name": "中军都督府吏典", "nam_type": "官制名录",
     "scope": "五军都督府",
     "entries": [
         {"seq": 1, "office": "提控", "count": "二名"},
         {"seq": 2, "office": "掾史", "count": "六名"},
         {"seq": 3, "office": "典吏", "count": "一十九名"},
         {"seq": 4, "office": "门吏/承发/架阁库典吏/掌关防文簿典吏", "count": "后俱革"},
     ]},
    {"id": "NAM-006-004", "item_id": "006-004", "name": "左右前后军都督府吏典", "nam_type": "官制名录",
     "scope": "五军都督府",
     "entries": [
         {"seq": 1, "office": "提控", "count": "各二名"},
         {"seq": 2, "office": "掾史", "count": "各六名（后府添五名）"},
         {"seq": 3, "office": "典吏", "count": "左14/右18/前14/后25名"},
     ]},
    {"id": "NAM-006-005", "item_id": "006-006", "name": "六部吏典", "nam_type": "官制名录",
     "scope": "六部",
     "entries": [
         {"seq": 1, "office": "都吏", "count": "吏礼兵工各四名"},
         {"seq": 2, "office": "令史", "count": "吏礼各7/兵26/工16名"},
         {"seq": 3, "office": "典吏", "count": "吏34/礼35/兵134/工79名"},
         {"seq": 4, "office": "承发", "count": "吏4/礼2/兵3/工5名"},
     ]},
    {"id": "NAM-006-006", "item_id": "006-029", "name": "户部吏典", "nam_type": "官制名录",
     "scope": "户部",
     "entries": [
         {"seq": 1, "office": "都吏", "count": "十三名"},
         {"seq": 2, "office": "令史", "count": "四十一名"},
         {"seq": 3, "office": "典吏", "count": "一百四名"},
     ]},
    {"id": "NAM-006-007", "item_id": "006-030", "name": "户部照磨所吏典", "nam_type": "官制名录",
     "scope": "户部",
     "entries": [
         {"seq": 1, "office": "司吏", "count": "二名"},
         {"seq": 2, "office": "典吏", "count": "十二名"},
     ]},
    # ===== 卷7 外官宣吏典（抽样关键衙门） =====
    {"id": "NAM-007-001", "item_id": "007-001", "name": "千户所吏典", "nam_type": "官制名录",
     "scope": "卫所",
     "entries": [{"seq": 1, "office": "司吏", "count": "各卫所定额"}]},
    {"id": "NAM-007-002", "item_id": "007-002", "name": "羽林等十九卫吏典", "nam_type": "官制名录",
     "scope": "京卫",
     "entries": [
         {"seq": 1, "office": "令史", "count": "羽林左右府等十九卫各定额"},
         {"seq": 2, "office": "典吏", "count": "各卫定额"},
     ]},
]
