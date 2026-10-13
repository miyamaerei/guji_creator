# -*- coding: utf-8 -*-
"""试点源数据：卷01 HYD 水系（大通河/玉河/桑乾河/卫河）。"""

HYD_AI = [
    {
        "slot": 1,
        "item_id": "01-008",
        "name": "大通河",
        "alt": "通惠河",
        "type": "河",
        "flow": "水自玉河出，绕都城东南，下流至高丽庄，入白河，即元运河也",
        "anchor": {"anchor": "大兴县东南", "context": "东南有大通河"},
        "events": [],
    },
    {
        "slot": 2,
        "item_id": "01-008",
        "name": "玉河",
        "alt": "",
        "type": "河",
        "flow": "源自玉泉山，流经大内，出都城东南，注大通河",
        "anchor": {"anchor": "大兴县", "context": "又有玉河"},
        "events": [],
    },
    {
        "slot": 3,
        "item_id": "01-009",
        "name": "桑乾河",
        "alt": "",
        "type": "河",
        "flow": "出山西马邑县，流千里入京师宛平县境。出卢沟桥下，又东南分为二：一至通州，入白河；一至武清小直沽，合卫河，入于海",
        "anchor": {"anchor": "宛平县境", "context": "有桑乾河出山西马邑县"},
        "events": [],
    },
    {
        "slot": 4,
        "item_id": "01-009",
        "name": "卫河",
        "alt": "",
        "type": "河",
        "flow": "至武清小直沽，合卫河，入于海",
        "anchor": {"anchor": "武清小直沽", "context": "合卫河，入于海"},
        "events": [],
    },
]
