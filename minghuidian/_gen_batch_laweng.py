# -*- coding: utf-8 -*-
"""laweng 卷组（130-163）批量补缺生成器。
刑部（131-145）刑名规则 -> RUL；工部（146-163）卫所/河渠/海运/竹木/物料/器物清单 -> NAM，
长条文（令/奏准/议定/诏/勑/凡/国初）仍 -> RUL。
读 registry -> 算开工时未覆盖且属本卷组条目 -> 分类 -> 写 _src 两个文件 -> 自检 -> 枚举不合法入 pending。
"""
import json, os, re, csv, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(ROOT, "_item_registry.json")
SRC_DIR = os.path.join(ROOT, "_src")
PENDING = os.path.join(ROOT, "_pending_laweng.csv")

VOLS = list(range(130, 164))
TAG = "laweng"
XINGBU = set(range(131, 146))   # 刑部卷：一律 RUL

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


def detect_marker(orig, title, flat):
    """返回 source_marker 或 None。优先显式奏议类，再诏/勑/令/凡/国初。"""
    head = flat[:90]
    if "奏准" in flat:
        return "奏准"
    if "议准" in flat:
        return "议准"
    if "奏定" in flat:
        return "奏定"
    if "议定" in flat:
        return "议定"
    if "诏" in flat:
        return "诏"
    if ("勑" in flat) or ("敕" in flat) or ("勑谕" in flat):
        return "敕"
    if ("圣旨" in flat) or ("榜例" in flat):
        return "令"
    if re.search(HAO + r".{0,18}(令|定)", head):
        return "令"
    if orig.startswith("凡") or title.startswith("凡"):
        return "凡"
    if orig.startswith("国初") or title.startswith("国初"):
        return "凡"
    return None


def detect_type(flat):
    """RUL.type 速查：处罚 > 禁止 > 时限 > 义务。"""
    if re.search(r"笞|杖|徒|流|斩|绞|凌迟|问罪|治罪|充军|发遣|处死|处斩|罚俸|的决|发边|发附近|极边|永远充军|重罪", flat):
        return "处罚"
    if re.search(r"不许|不得|毋得|毋|勿|敢有|禁", flat):
        return "禁止"
    if re.search(r"限[於以]?[^。]{0,6}(日|月|年)", flat):
        return "时限"
    return "义务"


def classify(iid, it):
    """返回 (rul_dict or None, nam_dict or None, pending_rows)。"""
    title = (it.get("title") or "").strip()
    orig = (it.get("original") or "").strip()
    sec = (it.get("section") or "").strip()
    vol = int(iid.split("-")[0])
    text = orig if orig else title
    flat = re.sub(r"\s+", "", text)
    pend = []

    sm = detect_marker(orig, title, flat)

    # 刑部卷：一律 RUL，短名事目兜底 sm=凡
    if vol in XINGBU:
        if sm is None:
            sm = "凡"
        if sm not in SOURCE_MARKER:
            add_pending(pend, iid, "source_marker", sm, "source_marker 未命中枚举")
            return None, None, pend
        rt = detect_type(flat)
        if rt not in RUL_TYPE:
            add_pending(pend, iid, "type", rt, "RUL.type 未命中枚举")
            return None, None, pend
        rul = {
            "item_id": iid,
            "type": rt,
            "source_marker": sm,
            "subject": sec or "刑部",
            "action": flat[:60],
            "condition": "",
            "purpose": sec,
            "confidence": 0.9,
        }
        return rul, None, pend

    # 工部卷：有显式标记 -> RUL；否则 -> NAM 清单
    if sm is not None:
        rt = detect_type(flat)
        if sm not in SOURCE_MARKER:
            add_pending(pend, iid, "source_marker", sm, "source_marker 未命中枚举")
            return None, None, pend
        if rt not in RUL_TYPE:
            add_pending(pend, iid, "type", rt, "RUL.type 未命中枚举")
            return None, None, pend
        rul = {
            "item_id": iid,
            "type": rt,
            "source_marker": sm,
            "subject": sec or "工部",
            "action": flat[:60],
            "condition": "",
            "purpose": sec,
            "confidence": 0.9,
        }
        return rul, None, pend

    # 工部 NAM
    if vol == 146:
        namtype = "卫所名录"          # 江西清吏司分管卫所短名
    else:
        namtype = "其他"              # 河渠/海运/竹木/物料/器物/给价/坟茔/段疋 清单
    if namtype not in NAM_TYPE:
        add_pending(pend, iid, "nam_type", namtype, "nam_type 未命中枚举")
        return None, None, pend
    nam = {
        "item_id": iid,
        "name": title,
        "nam_type": namtype,
        "scope": "工部",
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
        rul["id"] = f"RUL-LAWENG-{vol:03d}-{rul_seq[vol]:03d}"
        rul_records.append(rul)
    elif nam is not None:
        nam_seq[vol] = nam_seq.get(vol, 0) + 1
        nam["id"] = f"NAM-LAWENG-{vol:03d}-{nam_seq[vol]:03d}"
        nam_records.append(nam)


# ---------- 写 _src ----------
def dump(path, header, records):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write(header)
        f.write("RECORDS = ")
        json.dump(records, f, ensure_ascii=False, indent=1)
        f.write("\n")


nam_path = os.path.join(SRC_DIR, "_nam_ai_laweng.py")
rul_path = os.path.join(SRC_DIR, "_rules_ai_laweng.py")
dump(nam_path, '"""laweng 卷组（130-163）工部卫所/河渠/海运/竹木/物料/器物名录批量条目"""\n\n', nam_records)
dump(rul_path, '"""laweng 卷组（130-163）刑部刑名规则 + 工部成造/河渠/抽分规则批量条目"""\n\n', rul_records)

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

# id 全局唯一
all_ids = [r["id"] for r in nam_loaded] + [r["id"] for r in rul_loaded]
if len(all_ids) != len(set(all_ids)):
    errs.append(("*", "id 有重复"))

covered_identifiers = len({r["item_id"] for r in nam_loaded} | {r["item_id"] for r in rul_loaded})
print("mine_total", len(mine))
print("NAM", len(nam_loaded))
print("RUL", len(rul_loaded))
print("pending", len(pending_all))
print("distinct_item_ids", covered_identifiers)
print("selfcheck_errors", len(errs))
for e in errs[:30]:
    print("  ERR", e)
print("NAM_PATH", nam_path)
print("RUL_PATH", rul_path)
