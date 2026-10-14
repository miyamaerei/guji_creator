# -*- coding: utf-8 -*-
"""
卷二十二 十层数据生成器（Phase ⑤）
ents 偏移量从 _extract/22_卷二十二.txt 原文计算，其余层按行定义。
实体 ID 段：ENT-2100 起（卷 22 命名空间）
"""
import json
import re
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACT = os.path.join(BASE, "_extract", "22_卷二十二.txt")
LAYERS = os.path.join(BASE, "_layers")

# ---------------------------------------------------------------- 读取原文
bodies = {}
titles = {}
with open(EXTRACT, encoding="utf-8") as f:
    for line in f:
        m = re.match(r"^(\d+)-(\d+)\|(.*)$", line.rstrip("\n"))
        if not m:
            continue
        vol, num, rest = m.group(1), int(m.group(2)), m.group(3)
        item_id = f"{vol}-{num:03d}"
        tm = re.match(r"^【([^】]*)】(.*)$", rest)
        if tm:
            titles[item_id] = tm.group(1)
            bodies[item_id] = tm.group(2)
        else:
            titles[item_id] = ""
            bodies[item_id] = rest

# ---------------------------------------------------------------- L1 实体层
# (item_id, text, normalized, type, confidence, role, faction, exam_info, career_span)
ENT_DEFS = [
    ("22-001", "王骥", "王骥", "person", "high", ["主体"], "无", None, "永乐至景泰间"),
    ("22-002", "太祖", "朱元璋", "person", "high", ["主体"], "无", None, "洪武元年—洪武三十一年"),
    ("22-002", "皇太子", "朱标", "person", "high", ["主体"], "无", None, "洪武间"),
    ("22-002", "耿九畴", "耿九畴", "person", "high", ["主体"], "无", {"year": "天顺元年", "era": "明", "rank": "进士", "title": "天顺元年进士"}, "正统至天顺间"),
    ("22-003", "金濂", "金濂", "person", "high", ["主体"], "无", None, "正统至景泰间"),
    ("22-003", "宁阳侯陈懋", "陈懋", "person", "high", ["关联人物"], "无", None, "永乐至天顺间"),
    ("22-004", "金濂", "金濂（巡按山东御史，名疑传写之误）", "person", "medium", ["主体"], "无", None, "弘治间"),
    ("22-004", "张鼐", "张鼐", "person", "high", ["主体"], "无", None, "弘治间"),
    ("22-006", "张尚书（经）", "张经", "person", "high", ["主体"], "无", None, "正德至嘉靖间"),
    ("22-006", "赵甬江少保", "赵文华", "person", "high", ["评论对象"], "阉党", None, "嘉靖间"),
    ("22-007", "胡宗宪", "胡宗宪", "person", "high", ["主体"], "无", None, "嘉靖间"),
    ("22-007", "阮鹗", "阮鹗", "person", "high", ["主体"], "无", None, "嘉靖间"),
    ("22-007", "汪直", "汪直", "person", "high", ["评论对象"], "无", None, "嘉靖间"),
    ("22-007", "徐海", "徐海", "person", "high", ["关联人物"], "无", None, "嘉靖间"),
    ("22-008", "忠介", "海瑞", "person", "high", ["评论对象"], "无", None, "嘉靖至万历间"),
    ("22-008", "王弇州", "王世贞", "person", "high", ["关联人物"], "无", None, "嘉靖至万历间"),
    ("22-009", "刑科给事舒化", "舒化", "person", "high", ["主体"], "无", None, "万历间"),
    ("22-009", "戴凤翔", "戴凤翔", "person", "high", ["主体"], "无", None, "嘉靖至万历间"),
    ("22-009", "徐华亭", "徐阶", "person", "high", ["评论对象"], "无", None, "嘉靖至万历间"),
    ("22-010", "南兵部尚书李克斋（遂）", "李遂", "person", "high", ["主体"], "无", None, "嘉靖至隆庆间"),
    ("22-011", "李见罗名材", "李材", "person", "high", ["主体"], "无", None, "嘉靖至万历间"),
    ("22-011", "王公会泉讳俸", "王俸", "person", "high", ["主体"], "无", None, "嘉靖至万历间"),
    ("22-011", "米万钟", "米万钟", "person", "high", ["关联人物"], "无", None, "万历间"),
    ("22-013", "苕上许敬庵司马", "许国", "person", "high", ["主体"], "无", None, "嘉靖至万历间"),
    ("22-013", "佞人篆", "王篆", "person", "medium", ["关联人物"], "江陵党", None, "万历间"),
    ("22-014", "潞河李中丞修吾（三才）", "李三才", "person", "high", ["主体"], "无", None, "万历间"),
    ("22-014", "长垣李中丞霖寰（化龙）", "李化龙", "person", "high", ["主体"], "无", None, "万历间"),
    ("22-015", "李中丞名焘", "李焘", "person", "high", ["主体"], "无", {"year": "戊辰", "era": "隆庆二年", "rank": "进士", "title": "隆庆二年进士"}, "隆庆至万历间"),
    ("22-016", "秦舜峰（燿）", "秦燿", "person", "high", ["主体"], "无", {"year": "辛未", "era": "隆庆五年", "rank": "庶常", "title": "隆庆五年庶吉士"}, "隆庆至万历间"),
    ("22-016", "沈介庵（鈇）", "沈鈇", "person", "high", ["主体"], "无", None, "万历间"),
    ("22-017", "宋应昌", "宋应昌", "person", "high", ["主体"], "无", None, "万历间"),
    ("22-017", "顾养谦", "顾养谦", "person", "high", ["关联人物"], "无", None, "万历间"),
    ("22-017", "孙鑛", "孙鑛", "person", "high", ["关联人物"], "无", None, "万历间"),
    ("22-017", "邢玠", "邢玠", "person", "high", ["关联人物"], "无", None, "万历间"),
    ("22-018", "任邱李次溪（汶）", "李汶", "person", "high", ["主体"], "无", None, "嘉靖至万历间"),
    ("22-018", "田东洲（乐）", "田乐", "person", "high", ["主体"], "无", None, "嘉靖至万历间"),
    ("22-018", "徐理斋（三畏）", "徐三畏", "person", "high", ["关联人物"], "无", None, "万历间"),
    ("22-019", "陈毓台（用宾）", "陈用宾", "person", "high", ["主体"], "无", None, "嘉靖至万历间"),
    ("22-022", "朱与言", "朱与言", "person", "high", ["主体"], "无", None, "宣德间"),
    ("22-023", "郝敬", "郝敬", "person", "high", ["主体"], "无", None, "正统间"),
    ("22-024", "福建左布政方正", "方正", "person", "high", ["主体"], "无", None, "正统间"),
    ("22-024", "按察使谢庄", "谢庄", "person", "high", ["主体"], "无", None, "正统间"),
    ("22-024", "辽东苑马少卿黄琰", "黄琰", "person", "high", ["主体"], "无", None, "正统间"),
    ("22-025", "工部右侍郎霍瑄", "霍瑄", "person", "high", ["主体"], "无", None, "正统至天顺间"),
    ("22-025", "右少监韦力转", "韦力转", "person", "high", ["主体"], "宦官", None, "正统至天顺间"),
    ("22-026", "王吉", "王吉", "person", "high", ["主体"], "无", None, "天顺至成化间"),
    ("22-026", "门达", "门达", "person", "high", ["评论对象"], "无", None, "正统至成化间"),
    ("22-027", "湖广右布政司陶鲁", "陶鲁", "person", "high", ["主体"], "无", None, "成化至弘治间"),
    ("22-028", "马端肃（文升）", "马文升", "person", "high", ["主体"], "无", None, "正统至正德间"),
    ("22-028", "刘文靖（健）", "刘健", "person", "high", ["关联人物"], "无", None, "正统至正德间"),
    ("22-029", "尹纶", "尹纶", "person", "high", ["主体"], "无", {"year": "戊戌", "era": "嘉靖十七年", "rank": "进士", "title": "嘉靖十七年进士"}, "嘉靖间"),
    ("22-029", "秉衡", "尹秉衡", "person", "high", ["关联人物"], "无", None, "嘉靖至万历间"),
    ("22-030", "元江徐方伯", "徐樾", "person", "high", ["主体"], "无", None, "嘉靖间"),
    ("22-030", "贵溪夏相公", "夏言", "person", "high", ["引用人物"], "无", None, "正德至嘉靖间"),
    ("22-030", "那鉴", "那鉴", "person", "high", ["主体"], "无", None, "嘉靖间"),
    ("22-030", "知府那宪", "那宪", "person", "high", ["关联人物"], "无", None, "嘉靖间"),
    ("22-030", "总兵沐朝弼", "沐朝弼", "person", "high", ["关联人物"], "无", None, "嘉靖间"),
    ("22-030", "新抚臣石简", "石简", "person", "high", ["关联人物"], "无", None, "嘉靖间"),
    ("22-030", "姚安府土官高鹄", "高鹄", "person", "high", ["关联人物"], "无", None, "嘉靖间"),
    ("22-030", "王文成", "王守仁", "person", "high", ["引用人物"], "无", None, "成化至嘉靖间"),
    ("22-035", "宣城沈翰撰君典（懋学）", "沈懋学", "person", "high", ["主体"], "无", None, "隆庆至万历间"),
    ("22-035", "江陵", "张居正", "person", "high", ["评论对象"], "无", None, "嘉靖至万历间"),
    ("22-035", "编修（嗣修）", "沈嗣修", "person", "high", ["关联人物"], "无", None, "万历间"),
    ("22-036", "冯宗伯琢庵（琦）", "冯琦", "person", "high", ["关联人物"], "无", {"year": "辛未", "era": "隆庆五年", "rank": "进士", "title": "隆庆五年进士"}, "隆庆至万历间"),
    ("22-036", "仰芹（子履）", "冯子履", "person", "high", ["主体"], "无", None, "嘉靖至万历间"),
    ("22-036", "陈祖皋", "陈祖皋", "person", "high", ["关联人物"], "无", None, "万历间"),
    ("22-036", "项元池（德祯）", "项德祯", "person", "high", ["关联人物"], "无", None, "万历间"),
    ("22-037", "平凉知府何士英", "何士英", "person", "high", ["主体"], "无", None, "永乐间"),
    ("22-037", "耿清惠", "耿九畴", "person", "high", ["关联人物"], "无", None, "正统至天顺间"),
    ("22-037", "庞惺庵（尚鹏）", "庞尚鹏", "person", "high", ["关联人物"], "无", None, "嘉靖至万历间"),
    ("22-037", "鄢剑泉（懋卿）", "鄢懋卿", "person", "high", ["关联人物"], "阉党", None, "嘉靖间"),
    ("22-039", "苏州知府况钟", "况钟", "person", "high", ["主体"], "无", None, "宣德至正统间"),
    ("22-039", "蹇义", "蹇义", "person", "high", ["关联人物"], "无", None, "洪武至正统间"),
    ("22-039", "何文渊", "何文渊", "person", "high", ["关联人物"], "无", None, "宣德至成化间"),
    ("22-039", "吴县县丞赵浚", "赵浚", "person", "high", ["主体"], "无", None, "宣德间"),
    ("22-039", "周忱", "周忱", "person", "high", ["关联人物"], "无", None, "永乐至景泰间"),
    ("22-039", "苏州知府李从智", "李从智", "person", "high", ["关联人物"], "无", None, "正统间"),
    ("22-041", "江西吉安知府张锐", "张锐", "person", "high", ["主体"], "无", None, "成化间"),
    ("22-042", "雍正庵（泰）", "雍泰", "person", "high", ["主体"], "无", None, "成化至正德间"),
    ("22-042", "太原知府伊珍", "伊珍", "person", "high", ["主体"], "无", None, "弘治间"),
    ("22-042", "参将李杰", "李杰", "person", "high", ["关联人物"], "无", None, "弘治间"),
    ("22-043", "金元焕", "金元焕", "person", "high", ["主体"], "无", None, "万历间"),
    ("22-043", "石楚阳（昆玉）", "石昆玉", "person", "high", ["主体"], "无", None, "万历间"),
    ("22-044", "陈留人刘际明（芳誉）", "刘芳誉", "person", "high", ["主体"], "无", {"year": "癸未", "era": "万历十一年", "rank": "进士", "title": "万历十一年进士"}, "万历间"),
    ("22-044", "莱阳人高孩之（出）", "高出", "person", "high", ["主体"], "无", {"year": "戊戌", "era": "万历二十六年", "rank": "进士", "title": "万历二十六年进士"}, "万历间"),
    ("22-045", "邓云霄", "邓云霄", "person", "high", ["主体"], "无", None, "万历间"),
    ("22-046", "程篁墩", "程敏政", "person", "high", ["引用人物"], "无", None, "成化至正德间"),
    ("22-046", "罗一峰", "罗伦", "person", "high", ["引用人物"], "无", None, "成化间"),
    ("22-047", "裴松之", "裴松之", "person", "high", ["引用人物"], "无", None, "刘宋时期"),
    ("22-048", "戴春雨（凤翔）", "戴凤翔", "person", "high", ["主体"], "无", {"year": "己未", "era": "嘉靖三十八年", "rank": "甲榜", "title": "嘉靖三十八年进士"}, "嘉靖至万历间"),
]

ents = []
for i, (item, text, norm, typ, conf, roles, fac, exam, span) in enumerate(ENT_DEFS):
    ent_id = f"ENT-{2100 + i}"
    body = bodies[item]
    pos = body.find(text)
    rec = {
        "ent_id": ent_id, "item_id": item, "text": text, "type": typ,
        "normalized": norm, "start": pos, "end": pos + len(text) if pos >= 0 else pos,
        "confidence": conf, "source": item, "role_in_entry": roles, "faction": fac,
        "exam_info": exam, "career_span": span,
    }
    ents.append(rec)

# 校验未命中
miss = [e for e in ents if e["start"] < 0]
for e in miss:
    print("OFF-NOT-FOUND:", e["ent_id"], e["item_id"], repr(e["text"]))

ent_by_norm = {}
for e in ents:
    ent_by_norm.setdefault(e["normalized"], e["ent_id"])  # 首个（最早 item）优先

def ENT(norm, item=None):
    if item is not None:
        for e in ents:
            if e["normalized"] == norm and e["item_id"] == item:
                return e["ent_id"]
        raise AssertionError(f"missing entity {norm}@{item}")
    v = ent_by_norm.get(norm)
    assert v, f"missing entity for {norm}"
    return v

# ---------------------------------------------------------------- L2 规则层
rules = [
    {"rule_id": "RULE-22-001", "item_id": "22-002", "title": "督抚必兼都宪",
     "content": "尚书侍郎任总督巡抚者俱兼都御史（都宪）以便行事，以堂临官御史；景泰四年耿九畴改右副都御史镇守陕西，为专用宪臣之始。",
     "category": "官制", "scope": "在外督抚", "effective_date": "景泰四年", "status": "effective",
     "source_text": "其后凡尚书侍郎任督抚者，俱兼都宪，以便行事，盖欲以堂临官御史。", "confidence": "high"},
    {"rule_id": "RULE-22-002", "item_id": "22-002", "title": "文臣出镇不复称镇守",
     "content": "镇守既有总兵又有内监，故文臣出镇不复有镇守之称，但称巡抚；整饬边关、提督边关、抚治流民、总理河道等官皆因事特设而事权则一。",
     "category": "官制", "scope": "在外文臣", "effective_date": "正统以后", "status": "effective",
     "source_text": "以故文臣出镇，不复有镇守之称，但称巡抚。", "confidence": "high"},
    {"rule_id": "RULE-22-003", "item_id": "22-004", "title": "抚按公会坐次文移之制",
     "content": "抚按公会文移各遵旧制：都御史正坐，御史旁坐，都御史面付，御史具呈；弘治十七年山东抚按计奏经部议，上从之。",
     "category": "礼制", "scope": "在外抚按", "effective_date": "弘治十七年", "status": "effective",
     "source_text": "抚按公会文移，宜各遵旧制，都御史正坐，御史旁坐，都御史勔付，御史具呈。上从之。", "confidence": "high"},
    {"rule_id": "RULE-22-004", "item_id": "22-005", "title": "国初武事寄都司",
     "content": "国初武事俱寄之都指挥使司，其后渐设总兵，事权最重；今宇内文臣为巡抚者俱系添设，非国初旧制。",
     "category": "军事", "scope": "全国", "effective_date": "洪武定制", "status": "名存实亡",
     "source_text": "国初武事，俱寄之都指挥使司，其后渐设总兵，事权最重。", "confidence": "high"},
    {"rule_id": "RULE-22-005", "item_id": "22-009", "title": "田产分赎五年之限",
     "content": "祖宗时田产分赎定限五年，虑紊事端；海瑞抚江南不拘远年交易违例问断，戴凤翔疏以为滥。",
     "category": "财政", "scope": "全国", "effective_date": "洪武定制", "status": "变通",
     "source_text": "田产分赎，在祖宗时，亦虑紊事端，定限五年也。", "confidence": "high"},
    {"rule_id": "RULE-22-006", "item_id": "22-032", "title": "布按见朝序京官位次",
     "content": "天顺以前凡布政司按察司见朝，俱序京官二品三品之末；今明降本阶一级立。",
     "category": "礼制", "scope": "布按二司朝参官", "effective_date": "洪武至天顺", "status": "变通",
     "source_text": "天顺以前，凡布政司按察司见朝，俱序京官二品三品之末，今明降本阶一级立矣。", "confidence": "high"},
    {"rule_id": "RULE-22-007", "item_id": "22-032", "title": "知府缺保举部寺科道",
     "content": "祖宗朝最重布按二司官，知府凡有缺，必大臣保举部寺科道官有才望者居之。",
     "category": "官制", "scope": "全国府县", "effective_date": "洪武至天顺", "status": "名存实亡",
     "source_text": "祖宗朝最重布按二司官，知府凡有缺，必大臣保举部寺科道官有才望者居之。", "confidence": "high"},
    {"rule_id": "RULE-22-008", "item_id": "22-038", "title": "乡绅见监司礼仪等差",
     "content": "弇州谓乡大夫谒巡抚布政司官及府州县宜以部民礼，趋旁门走东阶；见巡按按察司官则入中门走甬道，以守土持宪有分别。然近年抚按事权不殊，藩臬互兼，其礼已不能行。",
     "category": "礼制", "scope": "乡绅见监司", "effective_date": "弘治至万历", "status": "名存实亡",
     "source_text": "乡大夫谒抚台布政司官及府州县，宜以部民礼，趋旁门，走东阶。", "confidence": "high"},
    {"rule_id": "RULE-22-009", "item_id": "22-041", "title": "府推官止设一员",
     "content": "本朝府佐同知通判无定员，而推官止一员，普天皆然；永平府带衔蓟辽诸镇理刑多设二三员，成化二十二年吉安府以健讼增一员，皆属创例。",
     "category": "官制", "scope": "天下诸府", "effective_date": "洪武定制", "status": "变通",
     "source_text": "本朝府佐同知、通判无定员，而推官止一员，盖普天皆然。", "confidence": "high"},
    {"rule_id": "RULE-22-010", "item_id": "22-046", "title": "御史九年称职升主事",
     "content": "国初极重郎署，凡御史九年称职者始升为主事；既而台省渐重，给事御史多从新进士除授，外官极轻。自考选法兴，非评博中行及外知推不得入台省，外吏骤重。",
     "category": "官制", "scope": "中央与地方迁转", "effective_date": "洪武至万历", "status": "变通",
     "source_text": "国初极重郎署，凡御史，九年称职者始升为主事。", "confidence": "high"},
]

# ---------------------------------------------------------------- L5 事件层
events = [
    {"event_id": "EVT-22-001", "item_id": "22-001", "title": "王骥以总督军务入衔",
     "description": "正统初靖远伯兵部尚书王骥督师征麓川，始以总督军务入衔，为文帅第一重任，埒南宋之都督；景泰初王骥起为南兵部尚书，又以总督军务入衔。祖宗朝本无此衔。",
     "event_type": "制度变动", "date": "正统初", "reign": "正统", "location": "麓川",
     "participants": [ENT("王骥")], "outcome": "总督军务入衔之始",
     "source_text": "仅见于正统初，靖远伯王骥以兵部尚书督师征麓川，始以总督军务入衔。", "confidence": "high"},
    {"event_id": "EVT-22-002", "item_id": "22-006", "title": "张经督倭冤死西市",
     "description": "张经以南大司马兼北右都御史督兵征倭，所辖江南凡六省，事权最雄重，大功垂成，而为赵文华所诬，逮下狱死于西市，人至今冤之。",
     "event_type": "政治事件", "date": "嘉靖间", "reign": "嘉靖", "location": "江南",
     "participants": [ENT("张经"), ENT("赵文华")], "outcome": "逮下狱死西市，人冤之",
     "source_text": "而为赵甬江少保所诬，逮下狱死西市，人至今冤之。", "confidence": "high"},
    {"event_id": "EVT-22-003", "item_id": "22-007", "title": "胡宗宪抚倭讲好",
     "description": "嘉靖甲寅乙卯间倭寇东南，浙江按使胡宗宪以督军有功峻擢右都御史，总制浙直福汀四省军务；至丁巳年用蒋洲、陈可愿谋与倭酋汪直讲好，惟倭酋徐海未得要领。",
     "event_type": "军事", "date": "嘉靖二十六年至三十六年", "reign": "嘉靖", "location": "浙江",
     "participants": [ENT("胡宗宪"), ENT("汪直"), ENT("徐海")], "outcome": "与汪直成讲好",
     "source_text": "胡已用蒋洲、陈可愿等谋，与倭酋汪直讲好，倭酋徐海者未得要领。", "confidence": "high"},
    {"event_id": "EVT-22-004", "item_id": "22-008", "title": "海瑞抚江南刁讼之风起",
     "description": "海瑞巡抚江南，一意澄清而不识时务，裁抑缙绅仪从，属吏庭参不敢仰视；开府吴中后人人以告讦为事，王世贞为华亭画计草匿名词状讥之，海瑞悟而稍止。三吴小民刁顽甲于海内，实庚午辛未间启之。",
     "event_type": "社会", "date": "隆庆至万历初", "reign": "万历", "location": "苏州",
     "participants": [ENT("海瑞"), ENT("王世贞")], "outcome": "告讦成风，习为故常",
     "source_text": "海开府吴中，人人以告讦为事……至今三吴小民，刁顽甲于海内，则庚午、辛未间启之也。", "confidence": "high"},
    {"event_id": "EVT-22-005", "item_id": "22-009", "title": "言官合纠海瑞去位",
     "description": "海瑞巡抚江南立意挫抑豪强，刑科给事中舒化首论之其词尚缓，吏科给事中戴凤翔独疏力参，并及其在南京卿寺时妻妾相争二人同日自缢事；海瑞辨疏太激诋举朝无一人，都给事中光懋、御史成守节等合纠，海瑞始去。说者谓徐阶实嗾戴凤翔为此疏，后戴遂归女于徐氏。",
     "event_type": "政治事件", "date": "万历初", "reign": "万历", "location": "北京",
     "participants": [ENT("海瑞"), ENT("戴凤翔"), ENT("舒化"), ENT("徐阶")], "outcome": "海瑞被纠去位",
     "source_text": "各出公疏合纠，而海始去。说者谓徐实嗾戴为此疏，后戴遂归女于徐氏。", "confidence": "high"},
    {"event_id": "EVT-22-006", "item_id": "22-011", "title": "万历丁亥郧阳兵变",
     "description": "万历丁亥郧抚李材自负文武才、以讲学名天下，拆毁参将公署改建书院，为其将米万钟设谋鼓噪，变起，作者外大父王俸（湖广右参政分守下荆南驻郧阳）适抵家病作而郧变告。",
     "event_type": "兵变", "date": "1587", "reign": "万历", "location": "郧阳",
     "participants": [ENT("李材"), ENT("王俸"), ENT("米万钟")], "outcome": "师儒曲为诸弁卒解释",
     "source_text": "其疏甫发，而郧变告矣。见罗自负文武才，以讲学名天下，至拆毁参将公署，改建书院，为其将米万钟设谋鼓噪。", "confidence": "medium"},
    {"event_id": "EVT-22-007", "item_id": "22-013", "title": "许国抚闽军哗割耳定乱",
     "description": "许国以中丞开府福建，僻于讲学，会见罗李材戍闽，两人同时合并一方，有一省两巡抚之谣；壬辰年调兵往漳南防守，正申约束军中忽哗，许国次日访最桀者百余人馘其耳，尽赦诸伍，免其出戍，事始定。",
     "event_type": "兵变", "date": "1592", "reign": "万历", "location": "福建",
     "participants": [ENT("许国"), ENT("李材")], "outcome": "割其耳而乱定",
     "source_text": "军中忽哗……次日，访最桀者百余人，馘其耳，尽赦诸伍，免其出戍，事始定。", "confidence": "high"},
    {"event_id": "EVT-22-008", "item_id": "22-016", "title": "秦燿被追赃谪戍",
     "description": "秦燿巡抚湖广被论调用，濒行取库鍰羡余以归；其属吏衡州府同知沈鈇抗章胪列其状，上震怒，遣缇骑逮下诏狱，追赃谪戍。",
     "event_type": "司法", "date": "万历间", "reign": "万历", "location": "北京",
     "participants": [ENT("秦燿"), ENT("沈鈇")], "outcome": "逮诏狱追赃谪戍",
     "source_text": "濒行取读鍰羡余以归……上震怒，遣缇骑逮下诏狱，追赃谪戍。", "confidence": "high"},
    {"event_id": "EVT-22-009", "item_id": "22-017", "title": "宋应昌特加经略援朝鲜",
     "description": "万历间朝鲜告急，廷遣侍郎宋应昌往援，时以总督为不足重，特加经略之号；继之者顾养谦、孙鑛、邢玠诸臣遂皆因之。宋应昌素无威望，一旦特拔，议者蜂起，谓事权过隆。",
     "event_type": "边政", "date": "万历间", "reign": "万历", "location": "朝鲜",
     "participants": [ENT("宋应昌"), ENT("顾养谦"), ENT("孙鑛"), ENT("邢玠")], "outcome": "经略之名沿而不废",
     "source_text": "近年朝鲜告急，廷遣侍郎宋应昌往援，时以总督为不足重，特加经略之号。", "confidence": "high"},
    {"event_id": "EVT-22-010", "item_id": "22-018", "title": "任邱诸臣同镇甘肃恢松山",
     "description": "任邱李汶总陕西三边，同邑田乐巡抚甘肃在其节制之下；戊戌岁二公同以大兵恢复大小松山，李汶自兵部尚书太子太保进宫傅，田乐入正位本兵加太子太保；辛丑同为三孤，乙巳李汶加少师，徐三畏又以甘肃巡抚加兵部尚书代之。弹丸邑中一时大僚接武公孤，近代所少。",
     "event_type": "边政", "date": "万历二十六年至三十三年", "reign": "万历", "location": "甘肃",
     "participants": [ENT("李汶"), ENT("田乐"), ENT("徐三畏")], "outcome": "恢复大小松山，同邑三孤接武",
     "source_text": "戊戍岁，二公同以大兵忧复大小松山。", "confidence": "medium"},
    {"event_id": "EVT-22-011", "item_id": "22-028", "title": "弘治十二年始设九江兵备",
     "description": "兵备官之设始于弘治十二年，马文升为本兵建议创立，刘健在内阁力阴以为不可；马执奏愈坚，本年八月始设江西九江兵备官一员，以九江管江防又总辖鄱阳湖防，特以专敕令按察司官领之。正德间流寇起中原皆设，嘉靖末东南倭事日棘，江浙闽广分巡无不带整饬兵备之衔。",
     "event_type": "制度变动", "date": "1499", "reign": "弘治", "location": "九江",
     "participants": [ENT("马文升"), ENT("刘健")], "outcome": "兵备道渐遍天下",
     "source_text": "兵备官之设，始于弘治十二年。其时马端肃（文升）为本兵，建议创立此官，而刘文靖（健）在内阁，则力阴以为不可。", "confidence": "high"},
    {"event_id": "EVT-22-012", "item_id": "22-030", "title": "那鉴元江之乱徐樾死事",
     "description": "嘉靖庚戌，元江府土舍那鉴倡乱弑知府那宪夺印，抚按官及总兵沐朝弼不能御；新抚臣石简调土汉官兵分五哨进剿，那鉴佯为顺命伪降，云南右布政使徐樾督饷在军贪功请行，赴之遇象马伏兵俱发死焉，姚安土官高鹄力救亦战殁。会后那鉴死，诸酋悔过纳象赎罪，世宗厌久役遂罢兵。",
     "event_type": "军事", "date": "1550", "reign": "嘉靖", "location": "云南元江府",
     "participants": [ENT("徐樾"), ENT("那鉴"), ENT("那宪"), ENT("沐朝弼"), ENT("石简"), ENT("高鹄")], "outcome": "连岁交兵，那鉴死而罢兵",
     "source_text": "值元江府土舍那鉴倡乱，弑其主知府那宪，夺其印。", "confidence": "high"},
    {"event_id": "EVT-22-013", "item_id": "22-031", "title": "王俸空室夺刀斩殿后倭",
     "description": "嘉靖乙卯倭至嘉兴府劫漕卒，于王江泾弃舟易衣操刀焚劫，居民奔散死伤者弥望；作者外大父王俸时为大参，守舍独不去，匿隐处窥伺，乘一悍倭殿后入空室解刀置旁，跃出夺其刀刺之，倭丧元犹奋起再仆，所斩乃真魁贼。",
     "event_type": "军事", "date": "1555", "reign": "嘉靖", "location": "嘉兴府王江泾",
     "participants": [ENT("王俸")], "outcome": "手斩殿后魁倭",
     "source_text": "大参忽跃出，夺其刀刺之；倭丧元，犹奋起再仆，圆睛小口，肤如黝漆，真魁贼也。", "confidence": "high"},
    {"event_id": "EVT-22-014", "item_id": "22-039", "title": "况钟妄奏赵浚被记过",
     "description": "况钟抵苏州任之次年奏吴县县丞赵浚茸无能解送至京，其实民千八百余人诉于巡抚周忱称浚守法爱民；都察院请治况钟妄奏之罪，宣宗谓钟为经历所欺失于不察，姑记其过仍戒加慎。",
     "event_type": "司法", "date": "1429", "reign": "宣德", "location": "苏州",
     "participants": [ENT("况钟"), ENT("赵浚"), ENT("周忱"), ENT("蹇义")], "outcome": "姑记其过，赵浚复职",
     "source_text": "都察院请治钟妄奏之罪，上曰：“此钟为得所欺，但失之不察耳，姑记其过。”", "confidence": "high"},
    {"event_id": "EVT-22-015", "item_id": "22-043", "title": "金元焕人命冤案",
     "description": "松江青浦举人金元焕移居苏州，家人与徽州人争市相殴致伤，徽人归而病死被以人命告；知府石昆玉素以廉峭自矜，因廉金与己同举应天乡试，又闻浮言谓太守受同年金为之回护，遂立意坐以主使，县令承望意竟论金抵偿，谳词上郡、兵道俱如拟。",
     "event_type": "司法", "date": "万历间", "reign": "万历", "location": "苏州",
     "participants": [ENT("金元焕"), ENT("石昆玉")], "outcome": "坐以主使论抵偿",
     "source_text": "石素以廉峭自矜重，遂立意坐以主使。", "confidence": "high"},
]

# ---------------------------------------------------------------- C1 任职层
appts = [
    {"appt_id": "APPT-22-001", "item_id": "22-001", "person": ENT("王骥"), "person_text": "王骥",
     "position": "总督军务（兵部尚书督师征麓川）", "reign": "正统", "date": "正统初", "type": "特设", "source": "22-001", "confidence": "high"},
    {"appt_id": "APPT-22-002", "item_id": "22-002", "person": ENT("朱标"), "person_text": "皇太子",
     "position": "巡抚陕西", "reign": "洪武", "date": "洪武二十四年", "type": "初设", "source": "22-002", "confidence": "high"},
    {"appt_id": "APPT-22-003", "item_id": "22-002", "person": ENT("耿九畴"), "person_text": "耿九畴",
     "position": "右副都御史镇守陕西", "reign": "景泰", "date": "景泰四年", "type": "改授", "source": "22-002", "confidence": "high"},
    {"appt_id": "APPT-22-004", "item_id": "22-006", "person": ENT("张经"), "person_text": "张经",
     "position": "以南大司马兼北右都御史总督军务征倭", "reign": "嘉靖", "date": "嘉靖间", "type": "特设", "source": "22-006", "confidence": "high"},
    {"appt_id": "APPT-22-005", "item_id": "22-007", "person": ENT("胡宗宪"), "person_text": "胡宗宪",
     "position": "右都御史总制浙直福汀四省军务", "reign": "嘉靖", "date": "嘉靖三十六年前后", "type": "升迁", "source": "22-007", "confidence": "high"},
    {"appt_id": "APPT-22-006", "item_id": "22-007", "person": ENT("阮鹗"), "person_text": "阮鹗",
     "position": "佥都御史（代胡宗宪巡按浙江任）", "reign": "嘉靖", "date": "嘉靖间", "type": "升迁", "source": "22-007", "confidence": "high"},
    {"appt_id": "APPT-22-007", "item_id": "22-014", "person": ENT("李三才"), "person_text": "李三才",
     "position": "都察院左佥都御史巡抚凤阳（督漕）", "reign": "万历", "date": "万历间", "type": "实授", "source": "22-014", "confidence": "high"},
    {"appt_id": "APPT-22-008", "item_id": "22-014", "person": ENT("李化龙"), "person_text": "李化龙",
     "position": "巡抚（总河）驻济宁", "reign": "万历", "date": "万历间", "type": "实授", "source": "22-014", "confidence": "high"},
    {"appt_id": "APPT-22-009", "item_id": "22-017", "person": ENT("宋应昌"), "person_text": "宋应昌",
     "position": "兵部侍郎经略（援朝鲜）", "reign": "万历", "date": "万历间", "type": "特设", "source": "22-017", "confidence": "high"},
    {"appt_id": "APPT-22-010", "item_id": "22-018", "person": ENT("田乐"), "person_text": "田乐",
     "position": "兵部尚书（入正位本兵，前巡抚甘肃）", "reign": "万历", "date": "万历二十六年", "type": "升迁", "source": "22-018", "confidence": "high"},
    {"appt_id": "APPT-22-011", "item_id": "22-027", "person": ENT("陶鲁"), "person_text": "陶鲁",
     "position": "湖广左布政使兼广东按察司副使（带管岭东道）", "reign": "弘治", "date": "弘治九年", "type": "兼任", "source": "22-027", "confidence": "high"},
    {"appt_id": "APPT-22-012", "item_id": "22-039", "person": ENT("况钟"), "person_text": "况钟",
     "position": "苏州府知府（赐敕便宜行事）", "reign": "宣德", "date": "宣德三年", "type": "超迁", "source": "22-039", "confidence": "high"},
    {"appt_id": "APPT-22-013", "item_id": "22-039", "person": ENT("何文渊"), "person_text": "何文渊",
     "position": "温州府知府（九人中后大用为名卿）", "reign": "宣德", "date": "宣德三年", "type": "超迁", "source": "22-039", "confidence": "high"},
    {"appt_id": "APPT-22-014", "item_id": "22-048", "person": ENT("戴凤翔"), "person_text": "戴凤翔",
     "position": "凤翔府知府（由行人降补郿县丞渐历至此）", "reign": "万历", "date": "万历初元以后", "type": "除授", "source": "22-048", "confidence": "high"},
]

# ---------------------------------------------------------------- C3 关系层
rels = [
    {"rel_id": "REL-22-001", "item_id": "22-006", "source": ENT("赵文华"), "source_text": "赵甬江少保",
     "target": ENT("张经"), "target_text": "张经", "relation": "弹劾构陷",
     "detail": "赵文华诬构总督张经，致其逮下狱死西市，人至今冤之", "source_text": "而为赵甬江少保所诬，逮下狱死西市", "confidence": "high"},
    {"rel_id": "REL-22-002", "item_id": "22-007", "source": ENT("胡宗宪"), "source_text": "胡宗宪",
     "target": ENT("阮鹗"), "target_text": "阮鹗", "relation": "恩怨",
     "detail": "阮鹗代胡宗宪巡按浙江任，好大言不甚知兵，胡轻之颇成隙", "source_text": "阮好大言，然不甚知兵，胡轻之颇成隙", "confidence": "high"},
    {"rel_id": "REL-22-003", "item_id": "22-010", "source": ENT("李遂"), "source_text": "李克斋（遂）",
     "target": ENT("李材"), "target_text": "李材", "relation": "父子亲属",
     "detail": "丰城李遂以南兵部尚书抚淮扬，其子李材亦以中丞知名，条目题为父子", "source_text": "适倭寇入犯，围淮安甚危急，乃子中丞见罗（材）", "confidence": "medium"},
    {"rel_id": "REL-22-004", "item_id": "22-011", "source": ENT("李材"), "source_text": "李见罗",
     "target": ENT("王俸"), "target_text": "王会泉", "relation": "同科",
     "detail": "李材与王俸为同榜进士又同为郎署，最称知契，抚郧阳时书促王俸兼程赴任", "source_text": "时郧抚为李见罗名材，故同榜进士，又同为郎署，最称知契", "confidence": "high"},
    {"rel_id": "REL-22-005", "item_id": "22-011", "source": ENT("米万钟"), "source_text": "米万钟",
     "target": ENT("李材"), "target_text": "李材", "relation": "恩怨",
     "detail": "李材拆毁参将公署改建书院，其将米万钟设谋鼓噪，致有郧变", "source_text": "为其将米万钟设谋鼓噪，禁李于署不得出", "confidence": "high"},
    {"rel_id": "REL-22-006", "item_id": "22-013", "source": ENT("许国"), "source_text": "许敬庵",
     "target": ENT("李材"), "target_text": "李见罗", "relation": "同僚",
     "detail": "许国特疏救李见罗，后李材戍闽与许国同省开府，有一省两巡抚之谣", "source_text": "又特疏救李见罗……两人同时龙象，合并一方，于是有一省两巡抚之谣", "confidence": "high"},
    {"rel_id": "REL-22-007", "item_id": "22-013", "source": ENT("王篆"), "source_text": "佞人篆",
     "target": ENT("许国"), "target_text": "许敬庵", "relation": "排挤构陷",
     "detail": "许国在吏部为佞人王篆所排，外转佥事", "source_text": "其在吏部为佞人篆所排，外转佥事", "confidence": "medium"},
    {"rel_id": "REL-22-008", "item_id": "22-016", "source": ENT("沈鈇"), "source_text": "沈介庵（鈇）",
     "target": ENT("秦燿"), "target_text": "秦舜峰（燿）", "relation": "弹劾",
     "detail": "衡州府同知沈鈇抗章胪列抚臣秦燿濒行取羡余之状，致秦燿被逮诏狱追赃谪戍", "source_text": "抗章胪列其状，上震怒，遣缇骑逮下诏狱", "confidence": "high"},
    {"rel_id": "REL-22-009", "item_id": "22-018", "source": ENT("田乐"), "source_text": "田东洲（乐）",
     "target": ENT("李汶"), "target_text": "李次溪（汶）", "relation": "同僚",
     "detail": "田乐巡抚甘肃在李汶三边节制之下，二人同籍任邱、同加大都御史，戊戌同年进宫保，辛丑同为三孤", "source_text": "同邑田东洲（乐）抚甘肃，在其节制之下", "confidence": "high"},
    {"rel_id": "REL-22-010", "item_id": "22-025", "source": ENT("韦力转"), "source_text": "右少监韦力转",
     "target": ENT("霍瑄"), "target_text": "霍瑄", "relation": "恩怨",
     "detail": "中官韦力转恨霍瑄，送之都御史年富家众杖十余；瑄拜亚卿后奏力转不法，天顺初上命逮治，后力转蒙宥而瑄亦不问", "source_text": "右少监韦力转恨瑄，送都御史年富家，众杖十余", "confidence": "high"},
    {"rel_id": "REL-22-011", "item_id": "22-026", "source": ENT("王吉", "22-026"), "source_text": "王吉",
     "target": ENT("门达"), "target_text": "门达", "relation": "敌对",
     "detail": "门达怙宪宗宠兼领镇抚司势张甚，刑部主事王吉每事裁抑之，缇骑作奸者讯治加等", "source_text": "吉每事裁抑之，遇其缇骑作奸者，讯治加等", "confidence": "high"},
    {"rel_id": "REL-22-012", "item_id": "22-029", "source": ENT("尹纶"), "source_text": "尹纶",
     "target": ENT("尹秉衡"), "target_text": "秉衡", "relation": "父子亲属",
     "detail": "尹秉衡从戎历官总兵当得貤恩，尹纶辄受其封诰，改服犀带狮补出谒宾客", "source_text": "其子秉衡从戎，历官总兵，当得貤恩，尹辄受其封诰", "confidence": "high"},
    {"rel_id": "REL-22-013", "item_id": "22-009", "source": ENT("戴凤翔"), "source_text": "戴凤翔",
     "target": ENT("徐阶"), "target_text": "徐华亭", "relation": "姻亲",
     "detail": "说者谓徐阶实嗾戴凤翔参海瑞之疏，后戴凤翔遂归女于徐氏", "source_text": "说者谓徐实嗾戴为此疏，后戴遂归女于徐氏", "confidence": "medium"},
    {"rel_id": "REL-22-014", "item_id": "22-030", "source": ENT("徐樾"), "source_text": "徐波石",
     "target": ENT("王守仁"), "target_text": "王文成", "relation": "师生",
     "detail": "徐樾自名王文成（王守仁）高足弟子，兼文武才，至今有称之者", "source_text": "徐号波石，自名王文成高足，兼文武才", "confidence": "high"},
    {"rel_id": "REL-22-015", "item_id": "22-009", "source": ENT("戴凤翔"), "source_text": "戴凤翔",
     "target": ENT("海瑞"), "target_text": "海忠介", "relation": "弹劾",
     "detail": "吏科给事中戴凤翔独疏参海瑞至发其南京妻妾自缢事；戴旋归女于徐氏，后以行人降补凤翔郿县丞，说者疑由劾瑞之报", "source_text": "至吏科给事中戴凤翔独疏参之", "confidence": "high"},
]

# ---------------------------------------------------------------- C9 论说层
opns = [
    {"opn_id": "OPN-22-001", "item_id": "22-002", "author": "沈德符", "author_text": "沈德符",
     "opinion_type": "制度考辨", "target": "抚按礼制之变",
     "content": "论督抚兼都宪本以堂临御史，初犹以属礼待之，既而改称晚生，今彼此俱称侍生，文移毫无轩轾，相与若寮采，抚臣反伺巡方嚬笑逢迎其意旨，慨叹体制之日亵。",
     "source_text": "今则彼此俱称侍生，文移毫无轩轾，相与若寮采，抚臣反伺巡方嚬笑，逢迎其意旨矣。",
     "confidence": "high", "reign": "万历", "faction": "无"},
    {"opn_id": "OPN-22-002", "item_id": "22-006", "author": "沈德符", "author_text": "沈德符",
     "opinion_type": "品评", "target": "张经冤狱",
     "content": "张经督师征倭事权最雄重大功垂成，为赵文华所诬逮死西市，人至今冤之；然亦微讽其在事时不为无衅。",
     "source_text": "大功垂成。而为赵甬江少保所诬，逮下狱死西市，人至今冤之。然在事时，亦有",
     "confidence": "medium", "reign": "万历", "faction": "无"},
    {"opn_id": "OPN-22-003", "item_id": "22-008", "author": "沈德符", "author_text": "沈德符",
     "opinion_type": "人物论", "target": "海瑞抚江南",
     "content": "海瑞在江南一意澄清而不识时务，好为不近人情之事，特荐绩溪令不问治状资望，盖矫枉过正，亦贤者之一蔽。",
     "source_text": "忠介在江南，一意澄清，而不识时务，好为不近人情之事。盖矫枉过正，亦贤者之一蔽云。",
     "confidence": "high", "reign": "万历", "faction": "无"},
    {"opn_id": "OPN-22-004", "item_id": "22-011", "author": "沈德符", "author_text": "沈德符",
     "opinion_type": "人物论", "target": "李材讲学致变",
     "content": "李材自负文武才，以讲学名天下，至拆毁参将公署改建书院，卒启其将米万钟鼓噪之郧变，讲学绖生之弊可鉴。",
     "source_text": "见罗自负文武才，以讲学名天下，至拆毁参将公署，改建书院，为其将米万钟设谋鼓噪。",
     "confidence": "high", "reign": "万历", "faction": "无"},
    {"opn_id": "OPN-22-005", "item_id": "22-024", "author": "沈德符", "author_text": "沈德符",
     "opinion_type": "刑名考辨", "target": "方面官淫纵处分",
     "content": "方正、谢庄遣戍大同，黄琰仅降主簿，同一淫纵同一年内而处分迥异；且方面大吏即于所治宣淫，亦未有之事也。",
     "source_text": "同一淫纵，同在一年内，而处分之异如此。且方面大吏，即于所治宣淫，亦未有之事也。",
     "confidence": "high", "reign": "万历", "faction": "无"},
    {"opn_id": "OPN-22-006", "item_id": "22-025", "author": "沈德符", "author_text": "沈德符",
     "opinion_type": "品评", "target": "霍瑄不能抑韦力转",
     "content": "中官敢笞方面大员为抑更异事；霍瑄守大同时从水窦匍匐叩马进膳奉太上皇，复辟见知，独不能稍抑韦力转以一伸其忿耶。",
     "source_text": "独不能稍抑力转，以一伸其忿耶？",
     "confidence": "high", "reign": "万历", "faction": "无"},
    {"opn_id": "OPN-22-007", "item_id": "22-030", "author": "沈德符", "author_text": "沈德符",
     "opinion_type": "借事讽世", "target": "徐樾贪功偾事",
     "content": "徐樾素讲道学负时誉，乃贪功喜事与夏言同科，一则茅土热中，一则节钺在望，或狼籍都市，或荠粉行间，足为后来庸人妄想之戒。",
     "source_text": "乃其贪功喜事，与夏同科……又在一邑一时，足为后来庸人妄想之戒。",
     "confidence": "high", "reign": "万历", "faction": "无"},
    {"opn_id": "OPN-22-008", "item_id": "22-038", "author": "沈德符", "author_text": "沈德符",
     "opinion_type": "风俗议论", "target": "部堂妄自尊大之态",
     "content": "漕储道暂过里中勒令府县行属礼，通判长跪、县丞叩头犹怏怏不悦，此量小易盈妄自尊大，无足怪者；事有古行之而今必不可行者也。",
     "source_text": "于是本府管粮通判长跪，各县管粮丞叩头，余官以半属庭参，犹怏怏不悦。此量小易盈，妄自尊大，无足怪者。",
     "confidence": "high", "reign": "万历", "faction": "无"},
    {"opn_id": "OPN-22-009", "item_id": "22-042", "author": "沈德符", "author_text": "沈德符",
     "opinion_type": "品评", "target": "雍泰廉而刚暴",
     "content": "雍泰身为按察使笞太原知府伊珍，后又以大杖杖参将李杰为言官劾罢；知府阶已尊无可挞辱之理，想雍之为人廉洁而刚暴无疑矣。",
     "source_text": "想雍之为人廉洁而刚暴无疑矣。",
     "confidence": "high", "reign": "万历", "faction": "无"},
    {"opn_id": "OPN-22-010", "item_id": "22-047", "author": "沈德符", "author_text": "沈德符",
     "opinion_type": "风俗议论", "target": "去思碑之滥",
     "content": "今世立碑之滥极矣而去思尤甚，不出乡绅不情之誉、霸儒强醵之钱；南史裴松之请以禁私碑之议奏闻朝议然后听之，宋武帝从之由是普断。以今一统全盛岂反逊义熙之年，所当首为禁者。",
     "source_text": "今世立碑之滥极矣，而“去思”尤甚。以今一统全盛，岂反逊义熙之年，所当首为禁者。",
     "confidence": "high", "reign": "万历", "faction": "无"},
]

# ---------------------------------------------------------------- C6 引书层
cits = [
    {"cit_id": "CIT-22-001", "item_id": "22-004", "cited_work": "弇山堂别集", "author": "王世贞",
     "cite_context": "弇州纪抚按重轻，自正统至弘治凡四事，而遗却一事最有关系者，作者据弘治十七年山东抚按会议补之。",
     "source_text": "弇州纪抚按重轻，自正统至弘治凡四事，而遗却一事，最有关系者", "confidence": "medium", "reign": "万历"},
    {"cit_id": "CIT-22-002", "item_id": "22-038", "cited_work": "弇山堂别集", "author": "王世贞",
     "cite_context": "弇州谓乡大夫谒抚台布政司官宜以部民礼，见巡按按察司官则入中门走甬道，作者以近事辨其今必不可行。",
     "source_text": "弇州谓乡大夫谒抚台布政司官及府州县，宜以部民礼", "confidence": "medium", "reign": "万历"},
    {"cit_id": "CIT-22-003", "item_id": "22-042", "cited_work": "雍泰墓志（吕楠撰）", "author": "吕楠",
     "cite_context": "雍泰笞太原知府伊珍及杖参将李杰事，皆出其同乡吕仲木所撰墓志，作者据以辨非臆说。",
     "source_text": "而事在雍墓志中，又出其同乡吕仲木（楠）笔，非臆说也。", "confidence": "high", "reign": "弘治"},
    {"cit_id": "CIT-22-004", "item_id": "22-047", "cited_work": "《宋书》（南史所记裴松之事）", "author": "沈约",
     "cite_context": "南史裴松之曰世立私碑有乖事实，请诸立碑者悉令言上为朝议所许然后听之，宋武帝从之由是普断。",
     "source_text": "南史裴松之曰：“世立私碑，有乖事实。”", "confidence": "high", "reign": "刘宋"},
]

# ---------------------------------------------------------------- C10 纪事层
mings = [
    {"ming_id": "MING-22-001", "item_id": "22-002", "person": "耿九畴", "person_text": "耿九畴",
     "event": "景泰四年镇守陕西刑部右侍郎改右副都御史，为督抚专用宪臣之始", "reign": "景泰", "date": "景泰四年",
     "source_text": "景泰四年镇守陕西刑部右侍郎耿九畴改右副都御史，仍旧镇守，此专用宪臣之始", "confidence": "high"},
    {"ming_id": "MING-22-002", "item_id": "22-004", "person": "金濂", "person_text": "巡按山东御史金濂",
     "event": "弘治十七年十月与巡抚辽东都御史张鼐计奏抚按公会之礼，下部会议，都御史正坐御史旁坐", "reign": "弘治", "date": "弘治十七年十月",
     "source_text": "巡按山东御史金濂，与巡抚辽东都御史张鼐计奏……都御史正坐，御史旁坐", "confidence": "medium"},
    {"ming_id": "MING-22-003", "item_id": "22-022", "person": "朱与言", "person_text": "朱与言",
     "event": "宣德十年英宗初政，先任四川按察副使朱与言以捕盗至郫县怒知县孙祥，杖之", "reign": "宣德", "date": "宣德十年",
     "source_text": "宣德十年英宗初御极，有先任四川按察副使朱与言者，以捕盗至郫县，怒知县孙祥不设策缉捕，杖之", "confidence": "high"},
    {"ming_id": "MING-22-004", "item_id": "22-023", "person": "郝敬", "person_text": "郝敬",
     "event": "正统五年陕西参政郝敬以驿丞不至杖之至死，按问当赎徒还职，上命编戍大同", "reign": "正统", "date": "正统五年",
     "source_text": "陕西参政郝敬，以公务至华池驿，呼驿丞张耕野不至，杖之至死……命编戍大同。", "confidence": "high"},
    {"ming_id": "MING-22-005", "item_id": "22-024", "person": "方正", "person_text": "方正",
     "event": "正统十年福建左布政使方正、按察使谢庄以淫纵事发遣戍大同", "reign": "正统", "date": "正统十年",
     "source_text": "福建左布政方正，诱取福州中卫指挥单刚妻马氏为妾……事发，下巡按御史问，得实，遣戍大同。", "confidence": "high"},
    {"ming_id": "MING-22-006", "item_id": "22-028", "person": "马文升", "person_text": "马文升",
     "event": "弘治十二年为本兵建议创立兵备官，八月始设江西九江兵备一员", "reign": "弘治", "date": "弘治十二年八月",
     "source_text": "兵备官之设，始于弘治十二年……本年八月始设江西九江兵备官一员", "confidence": "high"},
    {"ming_id": "MING-22-007", "item_id": "22-030", "person": "徐樾", "person_text": "徐樾",
     "event": "嘉靖庚戌督饷请行，赴元江伪降之约，遇伏死事", "reign": "嘉靖", "date": "嘉靖二十九年",
     "source_text": "比至元江府南门外，鉴不出，方呵责间，象马伏兵齐发，樾及左右皆死。", "confidence": "high"},
    {"ming_id": "MING-22-008", "item_id": "22-034", "person": "周观政", "person_text": "周观政",
     "event": "永乐间江西按察使周观政有罪谪为河间府驿夫，宪臣之辱未有至是", "reign": "永乐", "date": "永乐间",
     "source_text": "永乐间，江西按察使周观政有罪，谪为河间府驿夫", "confidence": "high"},
    {"ming_id": "MING-22-009", "item_id": "22-037", "person": "何士英", "person_text": "何士英",
     "event": "永乐间平凉知府何士英以循良第一特升两淮盐运使，先朝极重此官", "reign": "永乐", "date": "永乐间",
     "source_text": "永乐间，平凉知府何士英以循良第一，特升两淮运使，重可知矣。", "confidence": "high"},
    {"ming_id": "MING-22-010", "item_id": "22-041", "person": "张锐", "person_text": "张锐",
     "event": "成化二十二年吉安知府张锐奏以健讼增设推官一员，上从之，为府推官设一员外之创例", "reign": "成化", "date": "成化二十二年",
     "source_text": "惟成化二十二年江西吉安知府张锐奏请……宜增设推官一员，上从之。", "confidence": "high"},
    {"ming_id": "MING-22-011", "item_id": "22-042", "person": "雍泰", "person_text": "雍泰",
     "event": "弘治元年山西按察使雍泰怒太原知府伊珍避道稍迟执而笞之，讦诉仅降湖广参政", "reign": "弘治", "date": "弘治元年",
     "source_text": "至弘治元年为山西按察使，怒太原知府伊珍避道稍迟，执而笞之。", "confidence": "high"},
]

# ---------------------------------------------------------------- C14 时间沿革层
tmes = [
    {"tme_id": "YHB-TME-22-001", "item_id": "22-001", "date": "1436-1449", "reign": "正统", "era": "正统初",
     "event": "王骥以兵部尚书督师征麓川，始以总督军务入衔", "source_text": "仅见于正统初，靖远伯王骥以兵部尚书督师征麓川，始以总督军务入衔", "confidence": "high"},
    {"tme_id": "YHB-TME-22-002", "item_id": "22-002", "date": "1391", "reign": "洪武", "era": "洪武二十四年辛未",
     "event": "太祖命皇太子巡抚陕西，巡抚之名始见于此", "source_text": "洪武二十四年辛未，太祖命皇太子巡抚陕西地方，巡抚之名，始见于此", "confidence": "high"},
    {"tme_id": "YHB-TME-22-003", "item_id": "22-002", "date": "1453", "reign": "景泰", "era": "景泰四年",
     "event": "耿九畴改右副都御史镇守陕西，为督抚专用宪臣之始", "source_text": "景泰四年镇守陕西刑部右侍郎耿九畴改右副都御史，此专用宪臣之始", "confidence": "high"},
    {"tme_id": "YHB-TME-22-004", "item_id": "22-004", "date": "1504", "reign": "弘治", "era": "弘治十七年十月",
     "event": "抚按公会文移之制重定，都御史正坐御史旁坐", "source_text": "弘治十七年十月，巡按山东御史金濂，与巡抚辽东都御史张鼐计奏", "confidence": "high"},
    {"tme_id": "YHB-TME-22-005", "item_id": "22-011", "date": "1587", "reign": "万历", "era": "万历丁亥",
     "event": "郧阳兵变，巡抚李材为所属鼓噪所困", "source_text": "万历丁亥……其疏甫发，而郧变告矣", "confidence": "high"},
    {"tme_id": "YHB-TME-22-006", "item_id": "22-013", "date": "1592", "reign": "万历", "era": "壬辰",
     "event": "福建巡抚许国军门兵哗，割桀者之耳而定", "source_text": "其事在壬辰年，许同里张御史（天德）按闽，亲为余言", "confidence": "high"},
    {"tme_id": "YHB-TME-22-007", "item_id": "22-018", "date": "1598", "reign": "万历", "era": "戊戍",
     "event": "李汶、田乐同以大兵恢复大小松山", "source_text": "戊戍岁，二公同以大兵忧复大小松山", "confidence": "medium"},
    {"tme_id": "YHB-TME-22-008", "item_id": "22-019", "date": "1593-1608", "reign": "万历", "era": "自癸巳讫戊申",
     "event": "陈用宾巡抚云南首尾十六年，为抚台久任之最", "source_text": "无如陈毓台（用宾）之抚云南，自癸巳讫戊申凡十六年", "confidence": "high"},
    {"tme_id": "YHB-TME-22-009", "item_id": "22-021", "date": "1382", "reign": "洪武", "era": "洪武十五年",
     "event": "增云南布政司，天下府州县及分巡四十二道俱授方印，事权特重", "source_text": "分十二布政司，十五年增云南以至按察都指挥司，下及府州县授方印", "confidence": "high"},
    {"tme_id": "YHB-TME-22-010", "item_id": "22-028", "date": "1499", "reign": "弘治", "era": "弘治十二年",
     "event": "始设江西九江兵备官一员，为兵备道之始", "source_text": "兵备官之设，始于弘治十二年……本年八月始设江西九江兵备官一员", "confidence": "high"},
    {"tme_id": "YHB-TME-22-011", "item_id": "22-030", "date": "1550", "reign": "嘉靖", "era": "嘉靖庚戌",
     "event": "徐樾赴元江伪降之约遇伏死事", "source_text": "次年庚戌，则其同里又有一事，为元江徐方伯也", "confidence": "medium"},
    {"tme_id": "YHB-TME-22-012", "item_id": "22-039", "date": "1428", "reign": "宣德", "era": "宣德三年",
     "event": "吏部缺守九员，举京官廉能者升知府并赐敕，况钟其一", "source_text": "盖宣德三年，上闻郡守悉由资格，多不称任，适吏部阙守九员", "confidence": "high"},
    {"tme_id": "YHB-TME-22-013", "item_id": "22-041", "date": "1486", "reign": "成化", "era": "成化二十二年",
     "event": "吉安府增设推官一员", "source_text": "惟成化二十二年江西吉安知府张锐奏请", "confidence": "high"},
    {"tme_id": "YHB-TME-22-014", "item_id": "22-013", "date": "1594", "reign": "万历", "era": "甲午",
     "event": "许国推南京大理卿，以中丞得南冷局", "source_text": "至甲午许推南大理卿", "confidence": "medium"},
]

# ---------------------------------------------------------------- REG 制度层
regs = [
    {"reg_id": "REG-22-001", "item_id": "22-001", "name": "总督军务", "type": "官制",
     "description": "文帅第一重任，埒南宋之都督。祖宗朝无之，正统初王骥征麓川始以总督军务入衔，宜德以后大臣总督止施于工程钱谷等项。",
     "reign": "正统至万历", "source_text": "继乃有总督军务，为文帅第一重任，埒南宋之都督", "confidence": "high"},
    {"reg_id": "REG-22-002", "item_id": "22-002", "name": "巡抚制度", "type": "官制",
     "description": "巡抚之名始于洪武二十四年命皇太子巡抚陕西；后渐遣尚书侍郎都御史等巡抚边腹，事毕报命即停不遣；文臣出镇但称巡抚，因事特设整饬边关总理河道等官而事权则一。",
     "reign": "洪武至万历", "source_text": "巡抚之名，始见于此。", "confidence": "high"},
    {"reg_id": "REG-22-003", "item_id": "22-003", "name": "参赞军务", "type": "官制",
     "description": "今天下称赞理军务者惟巡抚一官俱在边方，以挂印总兵既称总镇，故稍逊其称以亚之；正统间金濂以刑部尚书同宁阳侯陈懋征闽寇尚称参赞军务。",
     "reign": "正统以来", "source_text": "如正统间，金濂以刑部尚书，同宁阳侯陈懋寺征闽寇，尚称参赞军务是也。", "confidence": "high"},
    {"reg_id": "REG-22-004", "item_id": "22-005", "name": "都指挥使司", "type": "军事",
     "description": "国初武事俱寄之都指挥使司，其后渐设总兵，事权最重；文臣巡抚系添设，非国初旧制。",
     "reign": "洪武", "source_text": "国初武事，俱寄之都指挥使司，其后渐设总兵。", "confidence": "high"},
    {"reg_id": "REG-22-005", "item_id": "22-017", "name": "经略大臣", "type": "军事",
     "description": "朝鲜告急以总督为不足重，特加经略之号，宋应昌为首任，顾养谦、孙鑛、邢玠继之，遂为定制。",
     "reign": "万历", "source_text": "时以总督为不足重，特加经略之号。继之者为顾养谦、孙鑛、邢玠诸臣，遂皆因之矣。", "confidence": "high"},
    {"reg_id": "REG-22-006", "item_id": "22-021", "name": "方印分司之制", "type": "官制",
     "description": "太祖分十二布政司，十五年增云南，下及府州县按察都指挥司俱授方印；每省分巡四十二道亦以方印治事，俱列衔按察使；分守道则无钦降方印。",
     "reign": "洪武", "source_text": "下及府州县授方印，此外则每省列分巡为四十二道，亦以方印治事。", "confidence": "high"},
    {"reg_id": "REG-22-007", "item_id": "22-028", "name": "整饬兵备道", "type": "官制",
     "description": "始于弘治十二年马文升建议，首设九江兵备以专敕令按察司官领之；正德流寇起中原皆设，嘉靖末东南倭棘江浙闽广分巡无不带整饬兵备之衔；本欲隆柄钤制武臣，承平日久仍如守土之吏。",
     "reign": "弘治至万历", "source_text": "兵备官之设，始于弘治十二年。", "confidence": "high"},
    {"reg_id": "REG-22-008", "item_id": "22-037", "name": "盐运使", "type": "财政",
     "description": "天下六转运使理鹾政，两淮盐课居五运司之大半，事权最繁钜，先朝极重此官；永乐何士英以循良特升，后耿清惠以故都运转侍郎出理盐法，嘉靖间俱用中丞莅任。",
     "reign": "永乐至嘉靖", "source_text": "天下六转运使理鹾政，而两淮盐课，居五运司之大半，其事权最繁钜，先朝极重此官。", "confidence": "high"},
    {"reg_id": "REG-22-009", "item_id": "22-039", "name": "知府赐敕", "type": "官制",
     "description": "宣德三年选京官廉能者九人升知府俱赐敕，许公差人违法害民即具实奏闻、所属官作奸害民即提解来京；正统八年苏州知府李从智亦赐敕。今人传况钟异典非尽实。",
     "reign": "宣德至正统", "source_text": "是时，九人皆赐敕……非如今所传，凡其同僚皆得拿问也。", "confidence": "high"},
    {"reg_id": "REG-22-010", "item_id": "22-048", "name": "嫌名之避", "type": "其他",
     "description": "前代仕宦每避嫌名如宗如周、韩皋、元绛之属；本朝此禁稍弛，然未有居官之地直犯其名者，戴凤翔竟履任凤翔府郿县丞后且守凤翔，在郡三年。",
     "reign": "历代至万历", "source_text": "前代仕宦，每避嫌名……本朝此禁稍弛，然未有居官之地，直犯其名者。", "confidence": "high"},
]

# ---------------------------------------------------------------- 写盘
def dump(layer, key, data):
    path = os.path.join(LAYERS, layer, f"{layer}_22.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{layer}_22.json: {len(data)} records -> {path}")

dump("ents", "ent_id", ents)
dump("rules", "rule_id", rules)
dump("events", "event_id", events)
dump("appts", "appt_id", appts)
dump("rels", "rel_id", rels)
dump("opns", "opn_id", opns)
dump("cits", "cit_id", cits)
dump("mings", "ming_id", mings)
dump("tmes", "tme_id", tmes)
dump("regs", "reg_id", regs)

# ID 越界自检
assert len(ents) <= 100, f"ents overflow: {len(ents)} (ENT-2100..ENT-2199)"
print("OK: entity id range ENT-2100..ENT-%d" % (2100 + len(ents) - 1))
