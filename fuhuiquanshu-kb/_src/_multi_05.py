# -*- coding: utf-8 -*-
"""卷05 莅任部四·结构化四维 + 论说 + 角色关系。"""
STRUCT_RECORDS = [
    {"item_id": "05-001", "dim": "LGR", "lgr_type": "template_form",
     "target": "详文", "target_ent_ids": [], "content": "详文体式：源委清楚、词意明切、陈以可否之义仰候宪裁；刑名据实举矜恤/法无可宥，钱谷举侵吞逋抗/艰难穷困", "confidence": "high"},
    {"item_id": "05-002", "dim": "LGR", "lgr_type": "template_form",
     "target": "禀帖", "target_ent_ids": [], "content": "禀帖体式：词贵简净意贵诚实，商酌请示贵婉曲，申辩剖晰贵和平；通详文之不便言", "confidence": "high"},
]
OPN_RECORDS = [
    {"item_id": "05-001", "topic": "详文为有司要务", "stance": "肯定",
     "argument": "详文亦或有司之要务，且详之其行与否均关有司体面，故事非不得巳亦不可轻易动详；鸿在郯有关钱粮驿站数详俱蒙上台允行，岂敢云言堪动听亦上台虚怀悯吏为然", "evidence_refs": [], "confidence": "high"},
    {"item_id": "05-002", "topic": "禀帖通详文之不便言", "stance": "肯定",
     "argument": "禀帖者或详文有不便言与不必见之详文而乃以禀通之也；词贵简净毋冗意贵诚实无欺，商酌请示贵婉曲申辩剖晰贵和平，然后览者易于入目而亦易于见听，否则纷纭满纸徒废笔墨", "evidence_refs": [], "confidence": "high"},
]
REL_RECORDS = [
    {"item_id": "05-001", "person_a": "绅衿", "person_a_ent_ids": [], "person_b": "官",
     "person_b_ent_ids": [], "relation_type": "其他", "direction": "单向",
     "evidence": "阖县绅衿王士奇等乡民张宗颜等合词呈控请具详豁免赦前民欠", "confidence": "high"},
    {"item_id": "05-002", "person_a": "官", "person_a_ent_ids": [], "person_b": "宪台",
     "person_b_ent_ids": [], "relation_type": "上下级", "direction": "单向",
     "evidence": "禀帖通候：上扬提台/济东丹道台/东兖钱道台/东兖李道台/兖州府蔡太尊，词贵简净婉曲", "confidence": "high"},
    {"item_id": "05-002", "person_a": "官", "person_a_ent_ids": [], "person_b": "营官",
     "person_b_ent_ids": [], "relation_type": "上下级", "direction": "单向",
     "evidence": "扬提台禀陈在城把总躭安逸、红花埠把总骄矜纵兵殃民，请破例换防朱成名史应佩", "confidence": "high"},
]
