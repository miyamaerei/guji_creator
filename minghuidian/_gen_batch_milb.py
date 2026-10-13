# -*- coding: utf-8 -*-
"""MILB 批量补缺生成器：卷120,121,123,124,125,126,127,128 未覆盖条目。
只读 registry + layers；写 _src/_nam_ai_milb.py 与 _src/_rules_ai_milb.py。
不运行 build/validate。
"""
import json, os, re, csv

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

VOLS = [120, 121, 123, 124, 125, 126, 127, 128]
mine = sorted(iid for iid in reg if int(iid.split("-")[0]) in VOLS and iid not in covered)

# ===== 封闭枚举（与 _batch_spec.py 一致，仅用于自检）=====
RUL_TYPE = ["禁止", "义务", "允许", "程序", "时限", "处罚", "优先级"]
SOURCE_MARKER = ["诏", "敕", "奏准", "议准", "奏定", "议定", "令", "凡"]
NAM_TYPE = ["王府拟名", "卫所名录", "驿递名录", "仓场名录", "寺观名录",
            "官职题名", "官制名录", "人员配置", "封爵名录", "其他"]
STAFF_ROLE = ["提控", "都吏", "掾史", "令史", "司吏", "典吏",
              "攒典", "承发", "门吏", "狱典", "未明"]

PROVINCES = {"北直隸", "南直隸", "北直隶", "南直隶", "浙江", "江西", "湖广",
             "福建", "广东", "广西", "四川", "河南", "陜西", "陕西", "山东",
             "山西", "云南", "贵州", "江南发", "江北发", "江南", "江北"}
ERAS = ("洪武", "永乐", "宣德", "正统", "景泰", "天顺", "成化", "弘治", "正德", "嘉靖", "国初")

PURPOSE = {120: "驿传", 121: "驿递马政", 123: "军器勾军", 124: "勾军",
           125: "俸给武学", 126: "卫所带管", 127: "名例律", 128: "刑律"}


def scope_for(vol):
    return "刑部" if vol in (127, 128) else "兵部"


def is_rul(t):
    if t.startswith("凡"):
        return True
    if t.startswith("国初"):
        return True
    if ("奏准" in t) or ("议准" in t) or ("奏定" in t) or ("议定" in t):
        return True
    # 年号 + 令/命
    if re.search(r"(洪武|永乐|宣德|正统|景泰|天顺|成化|弘治|正德|嘉靖).{0,10}(令|命)", t):
        return True
    # 年号起首的长规定句（洪武间/洪武中/洪武初置…）
    if re.match(r"^(" + "|".join(ERAS) + r")", t) and len(t) >= 11:
        return True
    # "一…" 枚举款目
    if t.startswith("一") and len(t) >= 11:
        return True
    # 计罪量刑行（贯→杖/斩/绞）
    if re.search(r"贯.*(杖|斩|绞|笞|徒|流)", t):
        return True
    return False


def rul_marker(t):
    if "奏准" in t:
        return "奏准"
    if "议准" in t:
        return "议准"
    if "奏定" in t:
        return "奏定"
    if "议定" in t:
        return "议定"
    if "诏" in t:
        return "诏"
    if "敕" in t:
        return "敕"
    if re.search(r"(洪武|永乐|宣德|正统|景泰|天顺|成化|弘治|正德|嘉靖).{0,10}(令|命)", t):
        return "令"
    return "凡"


def rul_type(t):
    if re.search(r"不许|不得|毋得|毋|勿|禁止", t):
        return "禁止"
    if re.search(r"杖|笞|斩|绞|发遣|治罪|充军", t):
        return "处罚"
    if re.search(r"昼夜|百刻|每三刻|限|即日|三日|十日|年月内", t):
        return "时限"
    if re.search(r"许|听", t):
        return "允许"
    if re.search(r"置|设|选充|差拨|计筭|关支|行取|编|造|磨勘|册封|递送|应付|给|拨|收买|折纳|销号", t):
        return "程序"
    return "义务"


def clean_subj(t):
    s = re.sub(r"^(凡|一曰|一)", "", t)
    s = re.sub(r"^(" + "|".join(ERAS) + r")[^，。]{0,12}?(令|命|奏准|奏定|议准|议定|榜谕|榜例)?", "", s)
    return s


def nam_type_of(t, vol):
    # 勾军调配关系（X府调Y卫）→ 其他
    if "调" in t and re.search(r"府|州|卫", t) and vol == 124:
        return "其他"
    if ("驿" in t) or ("急递铺" in t):
        return "驿递名录"
    if re.search(r"卫|千戸所|千户所|都督府|都司|守卫", t):
        return "卫所名录"
    if t in PROVINCES:
        return "其他"
    return "官制名录"


nam_records = []
rul_records = []
pending = []
# 每卷独立序号计数器（NAM/RUL 共用，保证 vol+seq 唯一）
vol_counter = {}


def next_seq(vol):
    vol_counter[vol] = vol_counter.get(vol, 0) + 1
    return vol_counter[vol]


for iid in mine:
    vol = int(iid.split("-")[0])
    title = reg[iid]["title"]
    sc = scope_for(vol)
    try:
        if is_rul(title):
            rtype = rul_type(title)
            marker = rul_marker(title)
            if rtype not in RUL_TYPE or marker not in SOURCE_MARKER:
                raise ValueError("enum_rul")
            cs = clean_subj(title)
            seq = next_seq(vol)
            rul_records.append({
                "id": "RUL-MILB-{:03d}-{:03d}".format(vol, seq),
                "item_id": iid,
                "type": rtype,
                "source_marker": marker,
                "subject": cs[:10],
                "action": cs[:26],
                "condition": "",
                "purpose": PURPOSE.get(vol, "兵部"),
                "confidence": 0.9,
            })
        else:
            nt = nam_type_of(title, vol)
            if nt not in NAM_TYPE:
                raise ValueError("enum_nam")
            seq = next_seq(vol)
            nam_records.append({
                "id": "NAM-MILB-{:03d}-{:03d}".format(vol, seq),
                "item_id": iid,
                "name": title,
                "nam_type": nt,
                "scope": sc,
                "entries": [],
            })
    except ValueError:
        pending.append((iid, title))

# ===== 写 _src 文件 =====
def write_src(fname, header, records):
    with open(os.path.join(ROOT, "_src", fname), "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write(header + "\n\n")
        f.write("RECORDS = ")
        json.dump(records, f, ensure_ascii=False, indent=1)


write_src("_nam_ai_milb.py", '"""MILB 批量：卷120/121/123/124/125/126/127/128 名录"""', nam_records)
write_src("_rules_ai_milb.py", '"""MILB 批量：卷120/121/123/124/125/126/127/128 规则"""', rul_records)

# ===== pending csv =====
with open(os.path.join(ROOT, "_pending_milb.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item_id", "title"])
    for row in pending:
        w.writerow(row)

# ===== 自检：重新加载两个 RECORDS =====
import importlib.util
def load_mod(fname):
    spec = importlib.util.spec_from_file_location("m", os.path.join(ROOT, "_src", fname))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.RECORDS

nam2 = load_mod("_nam_ai_milb.py")
rul2 = load_mod("_rules_ai_milb.py")

mine_set = set(mine)
errs = 0
seen = set()
for rec in nam2:
    iid = rec["item_id"]
    assert iid in reg, "registry missing " + iid
    assert iid in mine_set, "not mine " + iid
    assert iid not in seen, "dup " + iid
    seen.add(iid)
    if rec["nam_type"] not in NAM_TYPE:
        errs += 1
for rec in rul2:
    iid = rec["item_id"]
    assert iid in reg, "registry missing " + iid
    assert iid in mine_set, "not mine " + iid
    assert iid not in seen, "dup " + iid
    seen.add(iid)
    if rec["type"] not in RUL_TYPE:
        errs += 1
    if rec["source_marker"] not in SOURCE_MARKER:
        errs += 1

print("MINE total:", len(mine))
print("NAM records:", len(nam2))
print("RUL records:", len(rul2))
print("pending:", len(pending))
print("covered item_ids:", len(seen))
print("enum errors:", errs)
