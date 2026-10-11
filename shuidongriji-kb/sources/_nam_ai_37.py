# -*- coding: utf-8 -*-
"""《水东日记》卷 37 —— NAM 名录谱牒（结构分类） 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "37-001~006 瀛国公诗、刘江杀倭、王恽纪梦、志石昭穆、试马、药方",
]

# 字段键（打包器校验用）：nam_id, item_id, name, category, scope, entries, ent_ids, confidence
DATA = [
    # 卷三十七通检：6 条无表格式人名名录或谱牒（37-003 提及叶氏族谱考，仅考订话题，无完整谱表）。
    {"nam_id": "NAM-18501", "item_id": "37-003",
     "name": "叶氏族谱考（话题登记，无完整谱表）",
     "category": "谱牒",
     "scope": "叶氏谱（仅考订源流，未列世系人名）",
     "entries": [],
     "ent_ids": [],
     "evidence": "37-003 王恽纪梦条附带考叶氏族谱源流、杨荣所藏图书，仅作源流考订，未列完整世系人名，无可数组化 entries；登记为谱牒话题",
     "confidence": 0.8},
]
