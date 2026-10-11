# -*- coding: utf-8 -*-
"""《水东日记》卷 29 —— L1 实体标注（S4 片填写）

名录优先卷：表中 102 人姓名以 NAM entries.person 承载，本层只标注自序（29-002）与
六科分科标题所涉的机构/职官/年号/作者实体；表列人名不逐一建独立 ENT（同卷 17 口径）。
"""

DATA = [
    # ===== 题名与自序（29-001 / 29-002）=====
    {"item_id": "29-001", "text": "六科", "type": "institution", "normalized": "六科", "confidence": 0.95, "source": "六科旧僚题名"},
    {"item_id": "29-002", "text": "叶盛", "type": "person", "normalized": "叶盛（《水东日记》作者）", "confidence": 0.95, "source": "昆山叶盛识"},
    {"item_id": "29-002", "text": "昆山", "type": "place", "normalized": "昆山（叶盛里籍）", "confidence": 0.9, "source": "昆山叶盛识"},
    {"item_id": "29-002", "text": "成化", "type": "era", "normalized": "成化（明宪宗年号）", "confidence": 0.95, "source": "成化丙戌春三月"},
    {"item_id": "29-002", "text": "都察院", "type": "institution", "normalized": "都察院", "confidence": 0.95, "source": "都察院左佥都御史"},
    {"item_id": "29-002", "text": "左佥都御史", "type": "official", "normalized": "左佥都御史", "confidence": 0.95, "source": "都察院左佥都御史"},
    {"item_id": "29-002", "text": "兵科都给事中", "type": "official", "normalized": "兵科都给事中", "confidence": 0.95, "source": "前承事郎兵科都给事中"},
    {"item_id": "29-002", "text": "中议大夫", "type": "official", "normalized": "中议大夫（散阶）", "confidence": 0.85, "source": "中议大夫赞治尹"},
    {"item_id": "29-002", "text": "赞治尹", "type": "official", "normalized": "赞治尹（勋级）", "confidence": 0.85, "source": "赞治尹"},

    # ===== 六科分科标题（机构）=====
    {"item_id": "29-003", "text": "兵科", "type": "institution", "normalized": "兵科（六科之一）", "confidence": 0.95, "source": "兵科"},
    {"item_id": "29-044", "text": "吏科", "type": "institution", "normalized": "吏科（六科之一）", "confidence": 0.95, "source": "吏科"},
    {"item_id": "29-070", "text": "户科", "type": "institution", "normalized": "户科（六科之一）", "confidence": 0.95, "source": "户科"},
    {"item_id": "29-103", "text": "礼科", "type": "institution", "normalized": "礼科（六科之一）", "confidence": 0.95, "source": "礼科"},
    {"item_id": "29-134", "text": "刑科", "type": "institution", "normalized": "刑科（六科之一）", "confidence": 0.95, "source": "刑科"},
    {"item_id": "29-170", "text": "工科", "type": "institution", "normalized": "工科（六科之一）", "confidence": 0.95, "source": "工科"},

    # ===== 科内职衔（人名行末左/右/都）=====
    {"item_id": "29-013", "text": "都", "type": "official", "normalized": "都给事中（六科掌印）", "confidence": 0.85, "source": "姚铣孟声…都"},
    {"item_id": "29-006", "text": "左", "type": "official", "normalized": "左给事中", "confidence": 0.85, "source": "蒋性中…左"},
    {"item_id": "29-009", "text": "右", "type": "official", "normalized": "右给事中", "confidence": 0.85, "source": "黄仕儁…右"},
]
# 缺口说明：题名表 102 人（李春以下）的姓名/字/邑里以 NAM-14501 entries 承载，
# 本表未逐一建 person 实体（无文中传记者表列人名，实体化价值低；人物图谱化阶段再批量建）。
