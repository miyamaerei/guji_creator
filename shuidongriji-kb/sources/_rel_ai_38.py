# -*- coding: utf-8 -*-
"""《水东日记》卷 38 —— REL 人物关系 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "38-001~003 任事十臣、预备仓、范梈钦廉记",
]

# 字段键（打包器校验用）：rel_id, item_id, person_a, person_b, relation_type, direction, evidence, confidence
DATA = [
    # 卷三十八通检：3 条为君臣论对、仓储之议、远方记文，
    # 文本无二人之间可直接取证的交游关系（十臣为品第对象，非交游）。
    # REL 层本卷无可建模关系条目，如实登记缺口。
]
