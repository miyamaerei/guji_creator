# -*- coding: utf-8 -*-
"""《水东日记》卷 21 —— APPT 职官任职 源数据（AI 判定逐条填写）"""

ITEM_LIST = [
    "21-001 | 丞相益国周公词科旧稿后刻益国亲书一防云绍兴丙子四月予任行在和",
    "21-002 | 王叔英字原采天台人洪武戊寅知汉阳县事多惠政有四月祷文三首其",
    "21-003 | 黄氏日抄凡十七卷宋干淳中慈溪黄震东发所着一之三十二读孝经论语",
    "21-004 | 余干吴正道深于六书之学草庐吴文正公甞过其家问六书名义",
    "21-005 | 世所传小说杂书往往多本伪作其尤可笑者则吕文穆鸱吻诗所谓",
    "21-006 | 李易安武陵春词云风住尘香花已尽日晚倦梳头物是人非事事休欲语",
]

# 字段键（打包器校验用）：appointment_id, item_id, person, office, institution, when, status, evidence, confidence
DATA = [
    # ---- 21-002 王叔英知汉阳县 ----
    {"appointment_id": "APPT-10501", "item_id": "21-002",
     "person": {"text": "王叔英", "person_ent_ids": []},
     "office": {"text": "汉阳县知县", "official_ent_ids": []},
     "institution": {"text": "汉阳县", "ent_ids": []},
     "when": "洪武戊寅", "status": "现任",
     "evidence": "洪武戊寅知汉阳县事多惠政",
     "confidence": 0.88},
]
