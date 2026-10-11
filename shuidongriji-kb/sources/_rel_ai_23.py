# -*- coding: utf-8 -*-
"""《水东日记》卷 23 —— REL 人物关系 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "23-001~008 文彦博庙记、许可用文、鱼袋考、对类、史论、文章精义、碑考、药方",
]

# 字段键（打包器校验用）：rel_id, item_id, person_a, person_b, relation_type, direction, evidence, confidence
DATA = [
    # 卷二十三通检：各条为碑记、文章、考论、巧对、史论、书目、碑考、药方，
    # 文本均无二人之间可直接取证的关系（寇准、李纲为王交山评论对象，非交游关系）。
    # REL 层本卷无可建模关系条目，如实登记缺口。
]
