# -*- coding: utf-8 -*-
"""《水东日记》卷 30 —— REG 典章制度 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "30-001 | 祭社稷论", "30-002 | 文天祥像", "30-003 | 诛蚊赋",
    "30-004 | 均平徭役", "30-005 | 写像轶事",
]

# 字段键（打包器校验用）：reg_id, item_id, name, type, content, institutions, officials, confidence
DATA = [
    # ---- 30-001 州县祭社稷城隍祀典 ----
    {"reg_id": "REG-15001", "item_id": "30-001",
     "name": "州县祭社稷坛壝与城隍神祀典",
     "type": "礼仪",
     "content": "南轩张栻谓：今州县祭社稷是要典，祭时当筑一大坛于山下、望山而祭；并考城隍神之祀典所自始（城隍本为城池之神，历代渐加封爵）",
     "institutions": [], "officials": [],
     "confidence": 0.82},
    # ---- 30-004 广中均平徭役之法 ----
    {"reg_id": "REG-15002", "item_id": "30-004",
     "name": "广中均平徭役法（附朱熹答王子度论赋役书）",
     "type": "赋役",
     "content": "叶盛在广中均平一省徭役；晦庵（朱熹）答王子度二书，论赋役当使民力均平、不可偏重",
     "institutions": [], "officials": [],
     "confidence": 0.82},
]
