# -*- coding: utf-8 -*-
"""g7g8 卷组（164-180）批量补缺生成器。
读 registry -> 算开工时未覆盖且属于本卷组的条目 -> 按 _batch_spec 启发式判 NAM/RUL
-> 写 _src/_nam_ai_g7g8.py 与 _src/_rules_ai_g7g8.py -> 自检 -> 枚举不合法入 _pending_g7g8.csv。

本卷组为文职衙门：都察院/通政使司/大理寺/太常寺/六科/五军都督府/锦衣卫等。
  - 卫所/都督府/千户所 短名        -> NAM 卫所名录, scope=武职
  - 职官/道分/事目短标题            -> NAM 官制名录, scope=诸文职
  - 物料/仪仗/经费清单（拿不准）    -> NAM 其他,     scope=诸文职
  - 国初/洪武初置…沿革、年号令诏敕、凡、一…条款 -> RUL
"""
import json, os, re, csv, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(ROOT, "_item_registry.json")
SRC_DIR = os.path.join(ROOT, "_src")
PENDING = os.path.join(ROOT, "_pending_g7g8.csv")

VOLS = list(range(164, 181))   # 164-180
TAG = "g7g8"

# ===== 封闭枚举（与 _batch_spec.py 一致，禁止新增）=====
RUL_TYPE = ["禁止", "义务", "允许", "程序", "时限", "处罚", "优先级"]
SOURCE_MARKER = ["诏", "敕", "奏准", "议准", "奏定", "议定", "令", "凡"]
NAM_TYPE = ["王府拟名", "卫所名录", "驿递名录", "仓场名录", "寺观名录",
            "官职题名", "官制名录", "人员配置", "封爵名录", "其他"]
STAFF_ROLE = ["提控", "都吏", "掾史", "令史", "司吏", "典吏",
              "攒典", "承发", "门吏", "狱典", "未明"]

HAO = r"(洪武|永乐|洪熙|宣徳|宣德|洪熙|正统|景泰|天顺|成化|弘治|正德|嘉靖|隆庆|万历)"

# 卫所名录命中：卫 / 千户所 / 都督府 / 都司 / 护卫
WEI_RE = re.compile(r"(卫|千户所|都督府|都督|都司|护卫)")
# 纯物料/仪仗/经费清单结尾字（拿不准 -> 其他）
WULIAO_RE = re.compile(r"(只|口|石|斤|疋|匹|把|对|座|文|贯|两|个|条|两)$")


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


def classify(iid, it):
    """返回 (rul_dict or None, nam_dict or None, pending_rows)。一次只产出一类。"""
    title = (it.get("title") or "").strip()
    orig = (it.get("original") or "").strip()
    sec = (it.get("section") or "").strip()
    text = orig if orig else title
    flat = re.sub(r"\s+", "", text)
    pend = []

    sm = None
    rt = None
    is_rul = False

    # ---- RUL 判定（先于 NAM）----
    # 原则：一条原文常含多条款，取 flat 中【最早出现】的标记作为 source_marker。
    cands = []           # (position, marker)
    for mk in ["奏准", "议准", "奏定", "议定"]:
        i = flat.find(mk)
        if i >= 0:
            cands.append((i, mk))
    if orig.startswith("凡") or title.startswith("凡"):
        cands.append((0, "凡"))
    for mkr, mk in [(HAO + r".{0,14}诏", "诏"),
                    (HAO + r".{0,14}勑", "敕"),
                    (HAO + r".{0,14}敕", "敕"),
                    (HAO + r".{0,24}令", "令")]:
        mm = re.search(mkr, flat[:90])
        if mm:
            cands.append((mm.start(), mk))

    is_yange = (orig.startswith("国初") or title.startswith("国初")
                or bool(re.match(HAO + r".{0,4}初?置", flat[:24]) and len(flat) >= 24))
    is_yi = ((orig.startswith("一") or title.startswith("一")) and len(flat) >= 15)

    if is_yange:
        sm = "凡"; rt = "程序"; is_rul = True
    elif cands:
        cands.sort()
        sm = cands[0][1]
        is_rul = True
        if is_yi:
            rt = "程序"
    elif is_yi:
        # “一……”枚举条款（出巡宪纲/照刷式条目），无年代标记亦属规则
        sm = "凡"; rt = "程序"; is_rul = True

    if is_rul:
        if rt is None:
            if re.search(r"杖|笞|流|发遣|处斩|问罪|治罪|罚俸|的决|重罪|极刑|充军|论", flat):
                rt = "处罚"
            elif re.search(r"不许|不得|毋得|毋致|勿|敢有|禁约|禁止", flat):
                rt = "禁止"
            elif re.search(r"限[於以]?.*?(日|月|年)", flat):
                rt = "时限"
            else:
                rt = "义务"
        if sm not in SOURCE_MARKER:
            add_pending(pend, iid, "source_marker", sm, "source_marker 未命中枚举")
            is_rul = False
        if rt not in RUL_TYPE:
            add_pending(pend, iid, "type", rt, "RUL.type 未命中枚举")
            is_rul = False

    if is_rul:
        subject = sec if sec else "文职衙门"
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

    # ---- NAM 判定 ----
    if WEI_RE.search(flat):
        namtype = "卫所名录"; scope = "武职"
    else:
        # 其余短名：职官/道分/事目 -> 官制名录；纯物料仪仗 -> 其他
        if WULIAO_RE.search(flat) and not re.search(r"(寺|司|科|道|观|厂|局|府|院)", flat):
            namtype = "其他"
        else:
            namtype = "官制名录"
        scope = "诸文职"

    if namtype not in NAM_TYPE:
        add_pending(pend, iid, "nam_type", namtype, "nam_type 未命中枚举")
        return None, None, pend

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
        rul["id"] = f"RUL-G7G8-{vol:03d}-{rul_seq[vol]:03d}"
        rul_records.append(rul)
    elif nam is not None:
        nam_seq[vol] = nam_seq.get(vol, 0) + 1
        nam["id"] = f"NAM-G7G8-{vol:03d}-{nam_seq[vol]:03d}"
        nam_records.append(nam)


# ---------- 写 _src ----------
def dump(path, header, records):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write(header)
        f.write("RECORDS = ")
        json.dump(records, f, ensure_ascii=False, indent=1)
        f.write("\n")


nam_path = os.path.join(SRC_DIR, "_nam_ai_g7g8.py")
rul_path = os.path.join(SRC_DIR, "_rules_ai_g7g8.py")
dump(nam_path, '"""g7g8 卷组（164-180）院寺职官/道分/卫所属衙名录批量条目"""\n\n', nam_records)
dump(rul_path, '"""g7g8 卷组（164-180）建置沿革/选用风宪/职掌事例规则批量条目"""\n\n', rul_records)

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
# 分类分布概览
from collections import Counter
print("NAM_by_type", dict(Counter(r["nam_type"] for r in nam_loaded)))
print("RUL_by_marker", dict(Counter(r["source_marker"] for r in rul_loaded)))
print("RUL_by_type", dict(Counter(r["type"] for r in rul_loaded)))
print("NAM_PATH", nam_path)
print("RUL_PATH", rul_path)
