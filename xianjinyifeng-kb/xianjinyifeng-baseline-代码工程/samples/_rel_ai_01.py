# -*- coding: utf-8 -*-
"""《先进遗风》REL 人物关系层源数据样例（_rel_ai_01.py）

说明：
  * 顶层键固定为 relations（列表）；只建原文有直接证据的关系
  * 单条字段：
      item_id      必填，指纹库条号
      person_a     甲方（规范化主名）
      person_b     乙方
      relation_type 关系类型，封闭集 13 值（_kg_enums.REL_TYPES）
      direction    方向，封闭集 3 值（单向/双向/未明）
      evidence     原文证据词
"""

relations = [
    {
        "item_id": "01-008",
        "person_a": "杨溥",
        "person_b": "杨溥之子",
        "relation_type": "父子亲属",
        "direction": "单向",
        "evidence": "其子自乡来省",
    },
]
