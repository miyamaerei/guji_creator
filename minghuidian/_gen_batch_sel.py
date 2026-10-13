# -*- coding: utf-8 -*-
"""sel 卷组（吏部文选 卷1-13）批量补缺生成器。
读 registry -> 算开工时未覆盖且属于本卷组的条目 -> 按 _batch_spec 启发式判 NAM/RUL
-> 写 _src/_nam_ai_sel.py 与 _src/_rules_ai_sel.py -> 自检 -> 枚举不合法入 _pending_sel.csv。
"""
import json, os, re, csv, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(ROOT, "_item_registry.json")
SRC_DIR = os.path.join(ROOT, "_src")
PENDING = os.path.join(ROOT, "_pending_sel.csv")

VOLS = list(range(1, 14))
TAG = "sel"

# ===== 封闭枚举（与 _batch_spec.py 一致，禁止新增）=====
RUL_TYPE = ["禁止", "义务", "允许", "程序", "时限", "处罚", "优先级"]
SOURCE_MARKER = ["诏", "敕", "奏准", "议准", "奏定", "议定", "令", "凡"]
NAM_TYPE = ["王府拟名", "卫所名录", "驿递名录", "仓场名录", "寺观名录",
            "官职题名", "官制名录", "人员配置", "封爵名录", "其他"]
STAFF_ROLE = ["提控", "都吏", "掾史", "令史", "司吏", "典吏",
              "攒典", "承发", "门吏", "狱典", "未明"]

HAO = r"(洪武|永乐|宣德|洪熙|正统|景泰|天顺|成化|弘治|正德|嘉靖|隆庆|万历)"

# ---------- 读取 registry 与已覆盖 ----------
reg = json.load(open(REG, encoding="utf-8"))
covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

mine = sorted(iid for iid in reg
              if int(iid.split("-")[0]) in VOLS and iid not in covered)
MINE_SET = set(mine)


def add_pending(rows, iid, field, value, reason):
    rows.append({"tag": TAG, "item_id": iid, "field": field,
                 "value": value, "reason": reason})


def staff_role_in(text):
    """命中 STAFF_ROLE（不含未明）；返回 role 或 None。优先匹配较长角色词。"""
    for role in ["提控", "都吏", "掾史", "令史", "司吏", "典吏",
                 "攒典", "承发", "门吏", "狱典"]:
        if role in text:
            return role
    return None


def classify(iid, it):
    """返回 (rul_dict or None, nam_dict or None, pending_rows)。一次只产出一类。"""
    title = (it.get("title") or "").strip()
    orig = (it.get("original") or "").strip()
    sec = (it.get("section") or "").strip()
    vol = int(iid.split("-")[0])
    text = orig if orig else title
    flat = re.sub(r"\s+", "", text)
    pend = []

    # ---- 判定是否 RUL ----
    sm = None
    rt = None
    is_rul = False

    if "奏准" in flat:
        sm = "奏准"; is_rul = True
    elif "议准" in flat:
        sm = "议准"; is_rul = True
    elif "奏定" in flat:
        sm = "奏定"; is_rul = True
    elif "议定" in flat:
        sm = "议定"; is_rul = True

    if not is_rul:
        if orig.startswith("凡") or title.startswith("凡"):
            sm = "凡"; is_rul = True
        elif orig.startswith("国初") or title.startswith("国初"):
            sm = "凡"; rt = "程序"; is_rul = True
        elif orig.startswith("一") and len(flat) >= 15:
            # “一凡文官……”/“一两子……”枚举条款（验封/封赠/廕叙/诰敕用例）
            sm = "凡"; rt = rt or "程序"; is_rul = True
        elif re.search(HAO + r"[年间]?.{0,8}(诏|敕|令)", flat[:90]):
            m = re.search(HAO + r"[年间]?.{0,8}(诏|敕|令)", flat[:90])
            if m.group(2) == "诏":
                sm = "诏"
            elif m.group(2) == "敕":
                sm = "敕"
            else:
                sm = "令"
            is_rul = True

    if is_rul:
        if rt is None:
            if re.search(r"杖|笞|发遣|处斩|问罪|治罪|断罪|罚俸|充军|为民|送问|问发|追夺|的决", flat):
                rt = "处罚"
            elif re.search(r"不许|不得|毋得|勿|敢有|不许滥充", flat):
                rt = "禁止"
            elif re.search(r"违限|限[於以]?[^，。]{0,12}(日|月|年)", flat):
                rt = "时限"
            else:
                rt = "义务"
        if sm not in SOURCE_MARKER:
            add_pending(pend, iid, "source_marker", sm, "source_marker 未命中枚举"); is_rul = False
        if rt not in RUL_TYPE:
            add_pending(pend, iid, "type", rt, "RUL.type 未命中枚举"); is_rul = False

    if is_rul:
        subject = sec if sec else "吏部"
        rul = {
            "item_id": iid,
            "type": rt,
            "source_marker": sm,
            "subject": subject,
            "action": flat[:50],
            "condition": "",
            "purpose": sec,
            "confidence": 0.9,
        }
        return rul, None, pend

    # ---- 否则 NAM ----
    # 卷1 宗人府：含“王位下”字辈诗 -> 王府拟名
    if vol == 1 and "王位下" in flat:
        namtype = "王府拟名"
    # 卷11 到任须知：司吏/典吏/提控… 或 “计…名” 编制行 -> 人员配置
    elif vol == 11 and (staff_role_in(title) or re.search(r"^计.*名", title)):
        role = staff_role_in(title) or "未明"
        count = title
        if role != "未明":
            count = title.replace(role, "", 1).strip()
        if not count:
            count = orig
        if role not in STAFF_ROLE:
            add_pending(pend, iid, "staff_role", role, "staff role 未命中枚举")
            return None, None, pend
        nam = {
            "item_id": iid,
            "name": f"{title}·人员配置",
            "nam_type": "人员配置",
            "scope": "吏部",
            "staff_config": [{"role": role, "count": count}],
        }
        return None, nam, pend
    else:
        namtype = "官制名录"

    if namtype not in NAM_TYPE:
        add_pending(pend, iid, "nam_type", namtype, "nam_type 未命中枚举")
        return None, None, pend

    scope = "宗人府" if vol == 1 else "吏部"
    nam = {
        "item_id": iid,
        "name": title,
        "nam_type": namtype,
        "scope": scope,
        "entries": [],
    }
    return None, nam, pend


# ---------- 逐条分类 ----------
nam_records, rul_records = [], []
pending_all = []
nam_seq = {}
rul_seq = {}
for iid in mine:
    vol = int(iid.split("-")[0])
    rul, nam, pend = classify(iid, reg[iid])
    pending_all.extend(pend)
    if rul is not None:
        rul_seq[vol] = rul_seq.get(vol, 0) + 1
        rul["id"] = f"RUL-SEL-{vol:03d}-{rul_seq[vol]:03d}"
        rul_records.append(rul)
    elif nam is not None:
        nam_seq[vol] = nam_seq.get(vol, 0) + 1
        nam["id"] = f"NAM-SEL-{vol:03d}-{nam_seq[vol]:03d}"
        nam_records.append(nam)

# ---------- 写 _src ----------
def dump(path, header, records):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write(header)
        f.write("RECORDS = ")
        json.dump(records, f, ensure_ascii=False, indent=1)
        f.write("\n")

nam_path = os.path.join(SRC_DIR, "_nam_ai_sel.py")
rul_path = os.path.join(SRC_DIR, "_rules_ai_sel.py")
dump(nam_path, '"""sel 卷组（文选 卷1-13）宗人府/六科/布政司/到任须知 名录与人员配置批量条目"""\n\n', nam_records)
dump(rul_path, '"""sel 卷组（文选 卷1-13）铨选/考满/封赠/廕叙/告假规则批量条目"""\n\n', rul_records)

# ---------- pending CSV ----------
if pending_all:
    with open(PENDING, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["tag", "item_id", "field", "value", "reason"])
        w.writeheader()
        w.writerows(pending_all)

# ---------- 自检：importlib 重载 ----------
def load_records(path, var):
    spec = importlib.util.spec_from_file_location(os.path.basename(path), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, var)

errs = []
nam_loaded = load_records(nam_path, "RECORDS")
rul_loaded = load_records(rul_path, "RECORDS")

for r in nam_loaded:
    if r["item_id"] not in reg:
        errs.append((r["id"], "item_id 不在 registry"))
    if r["item_id"] not in MINE_SET:
        errs.append((r["id"], "item_id 不属于开工未覆盖集合"))
    if r["nam_type"] not in NAM_TYPE:
        errs.append((r["id"], "nam_type 越枚举"))
    if "staff_config" in r:
        for sc in r["staff_config"]:
            if sc["role"] not in STAFF_ROLE:
                errs.append((r["id"], "staff role 越枚举"))
for r in rul_loaded:
    if r["item_id"] not in reg:
        errs.append((r["id"], "item_id 不在 registry"))
    if r["item_id"] not in MINE_SET:
        errs.append((r["id"], "item_id 不属于开工未覆盖集合"))
    if r["type"] not in RUL_TYPE:
        errs.append((r["id"], "RUL.type 越枚举"))
    if r["source_marker"] not in SOURCE_MARKER:
        errs.append((r["id"], "source_marker 越枚举"))

covered_identifiers = len({r["item_id"] for r in nam_loaded} | {r["item_id"] for r in rul_loaded})
print("mine_total", len(mine))
print("NAM", len(nam_loaded))
print("RUL", len(rul_loaded))
print("pending", len(pending_all))
print("distinct_item_ids", covered_identifiers)
print("selfcheck_errors", len(errs))
for e in errs[:20]:
    print("  ERR", e)
print("NAM_PATH", nam_path)
print("RUL_PATH", rul_path)
