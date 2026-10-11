# -*- coding: utf-8 -*-
"""《水东日记》卷 13 —— REL 人物关系 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "13-001 | 邹奕字道苏州人有文行元季尝守贑国初谪关西与一时知名士若江右",
    "13-002 | 谢员友规者鄞人洪武初以户役起充浙江宪司吏非其志也告指疾求退得",
    "13-003 | 洪武己巳之秋予兵籍都城艮维之姚坊门乃九月八日与其侪输作于公",
    "13-004 | 袭阳武侯家因凿池得唐故幽州衙前【缺】　使乐安郡府君孙公墓志铭",
]

# 字段键（打包器校验用）：rel_id, item_id, person_a, person_b, relation_type, direction, evidence, confidence
DATA = [
    # ---- 13-001 邹奕与沈诚庄倡和交游 ----
    {"rel_id": "REL-6501", "item_id": "13-001",
     "person_a": {"text": "邹奕", "person_a_ent_ids": []},
     "person_b": {"text": "沈诚庄（成章）", "person_b_ent_ids": []},
     "relation_type": "其他", "direction": "双向",
     "evidence": "邹奕谪关西与沈诚庄为倡和友；诚庄出郊远迓、握袂联镳，邹奕为作杏林小隐记",
     "confidence": 0.85},
    # ---- 13-002 谢员与斯隆玛交游 ----
    {"rel_id": "REL-6502", "item_id": "13-002",
     "person_a": {"text": "谢员", "person_a_ent_ids": []},
     "person_b": {"text": "斯隆玛", "person_b_ent_ids": []},
     "relation_type": "其他", "direction": "双向",
     "evidence": "生从予至临洮……从予八年盖未始朝夕离也；临别白予嘱勿交沽衒之徒",
     "confidence": 0.85},
    # ---- 13-004 孙绪与孙伏伽五世祖孙 ----
    {"rel_id": "REL-6503", "item_id": "13-004",
     "person_a": {"text": "孙绪（宗绪）", "person_a_ent_ids": []},
     "person_b": {"text": "孙伏伽", "person_b_ent_ids": []},
     "relation_type": "父子亲属", "direction": "未明",
     "evidence": "公讳绪字宗绪五世祖伏伽大理卿",
     "confidence": 0.85},
]
