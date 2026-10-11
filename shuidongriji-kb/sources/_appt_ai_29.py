# -*- coding: utf-8 -*-
"""《水东日记》卷 29 —— APPT 职官任职（S4 片填写）

名录优先卷：题名表 102 人的"初升官位"已由 NAM-14501 entries.office 整体承载
（共享证据不重复抽取）；本层只从自序（29-002）提取叶盛本人有明确任职句的记录。
"""

DATA = [
    {"appointment_id": "APPT-14501", "item_id": "29-002",
     "person": {"text": "叶盛", "person_ent_ids": ["ENT-036"]},
     "office": {"text": "兵科都给事中", "official_ent_ids": []},
     "institution": {"text": "兵科（六科）", "ent_ids": []},
     "when": "正统末至景泰（壬申前六载）", "status": "现任",
     "evidence": "前承事郎兵科都给事中昆山叶盛识（余忝科名承乏侍近者几六载）", "confidence": 0.9},
    {"appointment_id": "APPT-14502", "item_id": "29-002",
     "person": {"text": "叶盛", "person_ent_ids": ["ENT-036"]},
     "office": {"text": "都察院左佥都御史", "official_ent_ids": []},
     "institution": {"text": "都察院", "ent_ids": []},
     "when": "成化丙戌", "status": "升迁",
     "evidence": "中议大夫赞治尹都察院左佥都御史（壬申之夏始有出参藩政之行，又十四五年）", "confidence": 0.9},
]
# 缺口：题名表 102 人初升官位已数组化于 NAM-14501，不逐条重复建 APPT（避免与 NAM 重复抽取）。
