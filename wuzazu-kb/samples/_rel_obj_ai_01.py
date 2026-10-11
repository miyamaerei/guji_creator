"""关系层（REL）/ 名物层（OBJ）源数据样例

关系层形状约定：
  person_a / person_b  必填，双方词形（字符串或列表，打包器升格为 {text, ent_ids}）
  relation_type        必填，枚举 relation_type：
      师友 / 师生 / 上下级 / 亲属 / 同僚 / 姻亲 / 举荐 / 敌对 / 同乡 / 婚姻 / 门生 / 其他
      旧写法「主从」自动归一为「上下级」
  direction            单向 / 双向 / 未明
  evidence             原文依据摘句（尽量贴原文）

名物层形状约定：
  name       必填，名物词形
  category   必填，枚举 obj_category：器物/动物/植物/饮食/珍宝/材料/建筑/服饰/其他
  attributes 自由键字典（形制、用途、产地、价格……名字随材料自定，不设枚举）
  lore       典故、起源、谢肇淛的评断

下列两段分别可复制为 _src/_rel_ai_01.py 与 _src/_obj_ai_01.py
"""

# ---- _src/_rel_ai_01.py ----
REL_RECORDS = [
    {
        "item_id": "01-006",
        "person_a": "舜",
        "person_b": "洛下闳",
        "relation_type": "主从",          # 别名写法：打包器归一为「上下级」
        "direction": "单向",
        "evidence": "舜作璇玑玉衡以齐七政；后世如洛下闳、僧一行、王朴之辈，冥思精数，亦能范围天地",
    },
]

# ---- _src/_obj_ai_01.py ----
OBJ_RECORDS = [
    {
        "item_id": "01-006",
        "name": "璇玑玉衡",
        "category": "器物",
        "attributes": {
            "形制": "浑仪倚盖，旋转不差",
            "用途": "以齐七政",
            "关联人物": "舜",
        },
        "lore": "舜以耕稼陶渔之夫，一旦践帝位便作璇玑玉衡，故谢肇淛谓造化之理尽在圣人橐龠中",
    },
]
