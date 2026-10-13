# -*- coding: utf-8 -*-
"""试点源数据：卷07 HYD 水系（滇池/盘龙江/金沙江）。"""

HYD_AI = [
    {
        "slot": 1,
        "item_id": "07-003",
        "name": "滇池",
        "alt": "昆明池",
        "type": "池",
        "flow": "池在城南，周五百里，其西南为海口，至武定府北，注于金沙江",
        "anchor": {"anchor": "昆明县南", "context": "山下即滇池"},
        "events": [],
    },
    {
        "slot": 2,
        "item_id": "07-003",
        "name": "盘龙江",
        "alt": "",
        "type": "江",
        "flow": "又东有盘龙江，西注滇池",
        "anchor": {"anchor": "昆明县东", "context": "又东有盘龙江"},
        "events": [],
    },
    {
        "slot": 3,
        "item_id": "07-003",
        "name": "金沙江",
        "alt": "",
        "type": "江",
        "flow": "至武定府北，注于金沙江",
        "anchor": {"anchor": "武定府北", "context": "至武定府北，注于金沙江"},
        "events": [],
    },
]
