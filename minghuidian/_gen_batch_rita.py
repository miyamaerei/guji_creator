# -*- coding: utf-8 -*-
"""tag=rita 批量补缺生成器：卷42-79。
读 registry + _layers 四层 covered；mine = 未覆盖。
按 _batch_spec.py 启发式逐条判定 NAM / RUL，写 _src/_nam_ai_rita.py 与 _src/_rules_ai_rita.py。
自检枚举；不命中者 append _pending_rita.csv 并跳过（枚举错误=0）。
"""
import json, os, re, csv

BASE = os.path.dirname(os.path.abspath(__file__))
VOLS = set(range(42, 80))

RUL_TYPE = ["禁止", "义务", "允许", "程序", "时限", "处罚", "优先级"]
SOURCE_MARKER = ["诏", "敕", "奏准", "议准", "奏定", "议定", "令", "凡"]
NAM_TYPE = ["王府拟名", "卫所名录", "驿递名录", "仓场名录", "寺观名录",
            "官职题名", "官制名录", "人员配置", "封爵名录", "其他"]
STAFF_ROLE = ["提控", "都吏", "掾史", "令史", "司吏", "典吏",
              "攒典", "承发", "门吏", "狱典", "未明"]

reg = json.load(open(os.path.join(BASE, "_item_registry.json"), "r", encoding="utf-8"))
covered = set()
for f in ["nams.json", "rules.json", "ents.json", "cits.json"]:
    d = json.load(open(os.path.join(BASE, "_layers", f), "r", encoding="utf-8"))
    for r in d:
        covered.add(r["item_id"])

mine = sorted(iid for iid in reg
              if int(iid.split("-")[0]) in VOLS and iid not in covered)

# ---------- 分类规则 ----------
# 乐舞曲名（NAM nam_type=官职题名）
TUNES = {
    "朝天子", "水仙子", "碧玉箫", "尧民歌", "沽美酒", "滚绣毬", "滚绣球",
    "庆太平", "武士欢", "阵阵赢", "得胜囘", "得胜回", "庆宣和", "窄砖儿",
    "太清歌", "上清歌", "水龙吟", "小将军", "殿前欢", "庆新年", "过门子",
    "泰阶平", "开天门", "万嵗乐", "清海宇", "千秋嵗", "共武间定", "天香鳯韶",
    "四边静", "刮地风", "豆叶黄", "庆丰年", "中宴", "常宴",
}
YUEWU_KW = ["乐章", "韶乐", "女乐", "宴乐", "侑食乐", "迎膳乐", "进膳乐",
            "导膳乐", "大乐", "清乐", "视学乐", "侑食"]

# 器物/仪仗/冠服/器皿/印信/图式（NAM nam_type=其他）
QIWU_KW = ["冠服", "巾服", "衮冕", "兖冕", "皮弁", "朝服", "公服", "礼服",
           "常服", "霞帔", "珠翟", "珠半开", "翠云", "圭长", "白鹇", "獬豸",
           "虎豹", "熊罴", "金器", "银器", "漆器", "器皿", "花银", "果四",
           "匙", "筯", "鞍马", "回门礼物", "杖鼓", "搏拊", "应钟",
           "", "与长子", "様", "乡饮酒礼图", "律案", "教民榜", "祝文式",
           "明集礼", "明祖训"]
# 精确短名才作为器物 NAM（避免长句/事目被子串误伤）
QIWU_EXACT = {"印信", "印信制度"}

def is_yuewu(title):
    if title.endswith("之曲"):
        return True
    if title in TUNES:
        return True
    for kw in YUEWU_KW:
        if kw in title:
            return True
    return False

def is_qiwu(title):
    if title == "乐器":
        return True
    for kw in QIWU_KW:
        if kw in title:
            return True
    return False

def source_marker_of(text):
    for m in ["奏定", "奏准", "议准", "议定", "诏", "敕"]:
        if m in text:
            return m
    return "凡"

def rul_type_of(text):
    if any(k in text for k in ["不许", "不得", "毋", "勿", "违者", "禁例", "不准", "并不许"]):
        return "禁止"
    if any(k in text for k in ["须", "务要", "须要", "照例", "当"]):
        return "义务"
    if any(k in text for k in ["许", "听"]):
        return "允许"
    return "程序"

def subject_of(section):
    s = section
    if "朝贺" in s or "常朝" in s: return "文武百官"
    if "册立" in s: return "皇帝宗藩"
    if "冠礼" in s: return "皇太子亲王"
    if any(k in s for k in ["纳后", "纳妃", "婚礼", "铺房", "见舅姑"]): return "皇室诸王"
    if "巡狩" in s or "亲征" in s: return "扈从官军"
    if "经筵" in s or "讲学" in s: return "讲读官"
    if "监国" in s: return "皇太子"
    if "祖训" in s: return "诸王皇帝"
    if "拜礼" in s: return "百官"
    if any(k in s for k in ["朝仪", "传制", "表笺"]): return "诸司百官"
    if "行移" in s or "礼部三十四" in s: return "各衙门"
    if any(k in s for k in ["举保", "学校", "乡试", "乡饮酒", "建言", "祭"]): return "礼部"
    if "宴" in s: return "宴享诸司"
    return "各衙门"

# ---------- 逐条分类 ----------
nam_records = []
rul_records = []
pending = []

# 每卷序号计数器
seq_nam = {}
seq_rul = {}

for iid in mine:
    it = reg[iid]
    title = it["title"].strip()
    section = it["section"]
    vol = int(iid.split("-")[0])

    # 决定 NAM / RUL：长句或“一”起首的条列规定一律 RUL；
    # 仅短名（<=14字、非“一”起首）才进入 NAM 关键词判定。
    short = (not title.startswith("一")) and len(title) <= 14
    if short and (title in QIWU_EXACT or is_yuewu(title)):
        nam_type = "官职题名" if is_yuewu(title) else "其他"
        kind = "NAM"
    elif short and is_qiwu(title):
        nam_type = "其他"
        kind = "NAM"
    else:
        kind = "RUL"

    if kind == "NAM":
        seq_nam[vol] = seq_nam.get(vol, 0) + 1
        rid = "NAM-RITA-%03d-%03d" % (vol, seq_nam[vol])
        rec = {
            "id": rid,
            "item_id": iid,
            "name": title,
            "nam_type": nam_type,
            "scope": "礼部",
            "entries": [],
        }
        # 自检枚举
        ok = (nam_type in NAM_TYPE)
        if ok:
            nam_records.append(rec)
        else:
            pending.append([rid, iid, title, "nam_type=" + nam_type])
    else:
        seq_rul[vol] = seq_rul.get(vol, 0) + 1
        rid = "RUL-RITA-%03d-%03d" % (vol, seq_rul[vol])
        sm = source_marker_of(title)
        ty = rul_type_of(title)
        action = re.sub(r"^[一]", "", title)
        action = action[:30]
        rec = {
            "id": rid,
            "item_id": iid,
            "type": ty,
            "source_marker": sm,
            "subject": subject_of(section),
            "action": action,
            "condition": "",
            "purpose": section,
            "confidence": 0.9,
        }
        ok = (ty in RUL_TYPE) and (sm in SOURCE_MARKER)
        if ok:
            rul_records.append(rec)
        else:
            pending.append([rid, iid, title, "type=%s marker=%s" % (ty, sm)])

# ---------- 写 _src 文件 ----------
def write_records(fname, records, header_doc):
    p = os.path.join(BASE, "_src", fname)
    with open(p, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write('"""%s"""\n\n' % header_doc)
        f.write("RECORDS = [\n")
        for r in records:
            f.write("    " + json.dumps(r, ensure_ascii=False) + ",\n")
        f.write("]\n")
    return p

p_nam = write_records("_nam_ai_rita.py", nam_records, "tag=rita 卷42-79 名录补缺（乐舞/器物冠服）")
p_rul = write_records("_rules_ai_rita.py", rul_records, "tag=rita 卷42-79 规则补缺（朝仪/册立/冠婚/行移/经筵/宴乐）")

# ---------- 自检：重新 load 生成的 RECORDS ----------
import importlib.util
def load_records(path):
    spec = importlib.util.spec_from_file_location("mod", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.RECORDS

chk_nam = load_records(p_nam)
chk_rul = load_records(p_rul)

mine_set = set(mine)
errs = []
for r in chk_nam:
    assert r["item_id"] in reg, ("NAM not in registry", r["item_id"])
    assert r["item_id"] in mine_set, ("NAM not in mine", r["item_id"])
    if r["nam_type"] not in NAM_TYPE:
        errs.append(r)
for r in chk_rul:
    assert r["item_id"] in reg, ("RUL not in registry", r["item_id"])
    assert r["item_id"] in mine_set, ("RUL not in mine", r["item_id"])
    if r["type"] not in RUL_TYPE:
        errs.append(r)
    if r["source_marker"] not in SOURCE_MARKER:
        errs.append(r)

covered_by_us = set(r["item_id"] for r in chk_nam) | set(r["item_id"] for r in chk_rul)

# pending csv
p_pend = os.path.join(BASE, "_pending_rita.csv")
with open(p_pend, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "item_id", "title", "reason"])
    for row in pending:
        w.writerow(row)

print("NAM records:", len(chk_nam))
print("RUL records:", len(chk_rul))
print("Pending:", len(pending))
print("Enum errors:", len(errs))
print("Covered item_ids by this batch:", len(covered_by_us))
print("mine total:", len(mine))
print("NAM file:", p_nam)
print("RUL file:", p_rul)
print("Pending file:", p_pend)
