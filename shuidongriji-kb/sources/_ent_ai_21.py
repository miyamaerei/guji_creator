# -*- coding: utf-8 -*-
"""《水东日记》卷 21 —— L1 实体标注 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "21-001 | 丞相益国周公词科旧稿后刻益国亲书一防云绍兴丙子四月予任行在和",
    "21-002 | 王叔英字原采天台人洪武戊寅知汉阳县事多惠政有四月祷文三首其",
    "21-003 | 黄氏日抄凡十七卷宋干淳中慈溪黄震东发所着一之三十二读孝经论语",
    "21-004 | 余干吴正道深于六书之学草庐吴文正公甞过其家问六书名义",
    "21-005 | 世所传小说杂书往往多本伪作其尤可笑者则吕文穆鸱吻诗所谓",
    "21-006 | 李易安武陵春词云风住尘香花已尽日晚倦梳头物是人非事事休欲语",
]

# 字段键（打包器校验用）：text, type, normalized, confidence, source
DATA = [
    # ============ 21-001 周必大词科旧稿 乡饮酒礼 ============
    {"item_id": "21-001", "text": "周必大", "type": "person", "normalized": "周必大（丞相益国公）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "21-001", "text": "绍兴丙子", "type": "era", "normalized": "绍兴（南宋高宗年号）", "confidence": 0.85, "source": "原文片段"},
    {"item_id": "21-001", "text": "余熂", "type": "person", "normalized": "余熂（作乡饮酒礼序）", "confidence": 0.82, "source": "原文片段"},

    # ============ 21-002 王叔英祷雨文 ============
    {"item_id": "21-002", "text": "王叔英", "type": "person", "normalized": "王叔英（字原采，天台人，靖难死节）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "21-002", "text": "天台", "type": "place", "normalized": "天台", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "21-002", "text": "汉阳县", "type": "place", "normalized": "汉阳县", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "21-002", "text": "洪武戊寅", "type": "era", "normalized": "洪武（戊寅=洪武三十一年）", "confidence": 0.85, "source": "原文片段"},

    # ============ 21-003 黄氏日抄 ============
    {"item_id": "21-003", "text": "黄震", "type": "person", "normalized": "黄震（字东发，慈溪人）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "21-003", "text": "慈溪", "type": "place", "normalized": "慈溪", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "21-003", "text": "黄氏日抄", "type": "work", "normalized": "黄氏日抄（黄震著，十七卷）", "confidence": 0.88, "source": "原文片段"},

    # ============ 21-004 吴正道六书 ============
    {"item_id": "21-004", "text": "吴正道", "type": "person", "normalized": "吴正道（余干，深六书之学）", "confidence": 0.82, "source": "原文片段"},
    {"item_id": "21-004", "text": "吴澄", "type": "person", "normalized": "吴澄（号草庐，谥文正）", "confidence": 0.88, "source": "原文片段"},
    {"item_id": "21-004", "text": "余干", "type": "place", "normalized": "余干", "confidence": 0.85, "source": "原文片段"},

    # ============ 21-005 小说伪作 吕文穆 ============
    {"item_id": "21-005", "text": "吕文穆", "type": "person", "normalized": "吕蒙正（谥文穆）", "confidence": 0.82, "source": "原文片段"},

    # ============ 21-006 李易安武陵春 ============
    {"item_id": "21-006", "text": "李易安", "type": "person", "normalized": "李清照（号易安居士）", "confidence": 0.9, "source": "原文片段"},
    {"item_id": "21-006", "text": "武陵春", "type": "work", "normalized": "武陵春（李清照词牌）", "confidence": 0.85, "source": "原文片段"},
]
