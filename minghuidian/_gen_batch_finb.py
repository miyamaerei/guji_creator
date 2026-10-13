# -*- coding: utf-8 -*-
"""批量补缺：tag=finb，卷 32/34/35/36/37/38/39/40/41。
读 registry + _layers 四层 covered 并集，对未覆盖条目按 _batch_spec.py 启发式
生成 NAM / RUL 记录；枚举不命中者写入 _pending_finb.csv 并跳过。
不运行 build_layers.py / validate_layers.py。
"""
import json, os, re, csv

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---- 封闭枚举（与 _batch_spec.py 一致，禁止新增）----
RUL_TYPE = ["禁止", "义务", "允许", "程序", "时限", "处罚", "优先级"]
SOURCE_MARKER = ["诏", "敕", "奏准", "议准", "奏定", "议定", "令", "凡"]
NAM_TYPE = ["王府拟名", "卫所名录", "驿递名录", "仓场名录", "寺观名录",
            "官职题名", "官制名录", "人员配置", "封爵名录", "其他"]

VOLS = [32, 34, 35, 36, 37, 38, 39, 40, 41]
TAG = "FINB"

# ---- 加载 registry ----
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ---- covered = 四层 item_id 并集 ----
covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

mine = sorted(iid for iid in reg
              if int(iid.split("-")[0]) in VOLS and iid not in covered)
mine_set = set(mine)

# ---- purpose 映射（按 registry section）----
def purpose_for(section):
    s = section or ""
    if "课程" in s: return "税课征收"
    if "盐" in s: return "盐课征收"
    if "钞" in s or "钱法" in s: return "钞法钱法"
    if "户部二十三" in s or "征収" in s or "征收" in s: return "税粮征收"
    if "户部二十四" in s or "都司" in s: return "仓厫管理"
    if "清吏司" in s: return "南京户部"
    return "户部事务"

# ---- RUL / NAM 判定 ----
# OCR 异体字容忍：德/徳、宁/寜/甯、台/臺、于/於 等
REIGN = r"(洪武|永乐|宣[徳德]|正统|景泰|天顺|成化|弘治|正德|嘉靖|隆庆|万历|国初)"
reign_re = re.compile("^" + REIGN)

def is_rul_title(t):
    if t.startswith("凡"):
        return True
    if t.startswith("一") and len(t) > 8:
        return True
    if reign_re.match(t):
        return True
    if len(t) >= 18:
        return True
    return False

def rul_marker(t):
    if "奏准" in t: return "奏准"
    if "议准" in t: return "议准"
    if "奏定" in t: return "奏定"
    if "议定" in t: return "议定"
    if "诏" in t: return "诏"
    if "敕" in t: return "敕"
    # 年号...令（容忍 OCR 异体字）
    if re.search(REIGN + r".{0,10}令", t): return "令"
    return "凡"

def rul_type(t):
    if re.search(r"不许|不得|毋得|毋许|勿得|勿许|违禁|不许", t): return "禁止"
    if re.search(r"笞|杖|发遣|治罪|问罪|充军|拟罪|坐罪|处斩", t): return "处罚"
    if re.search(r"即日|限.{0,4}[日月年]|三日|五日|十日|月底|岁终|年终|次日|一季", t): return "时限"
    if re.search(r"^许|听其|许令|听从|许于", t): return "允许"
    return "义务"

# subject/action 粗提取
MARKER_STRIP = re.compile(
    r"^(凡|一|国初|" + REIGN + r"[二三四五六七八九十百千]*年?初?|"
    r"诏|令|奏准|议准|奏定|议定|置|设|差|照|依)")
BREAK_RE = re.compile(
    r"(遇|有|将|于|於|赴|照|依|令|许|听|须|要|当|设|置|差|造|解|纳|"
    r"查|核|给|与|出|入|收|放|支|起|征|科|办|卖|买|行|发|关|领|"
    r"开|报|奏|禁|勿|毋|不|各|凡|其|若|如)")

def extract_sa(t):
    s = MARKER_STRIP.sub("", t)
    m = BREAK_RE.search(s)
    if m and m.start() > 0:
        subject = s[:m.start()].strip()[:16]
        action = s[m.start():m.start()+26].strip()
    else:
        subject = s[:16].strip()
        action = s[16:40].strip()
    if not subject:
        subject = s[:12].strip() or "户部"
    if not action:
        action = "依例施行"
    return subject, action

# ---- NAM 分类 ----
# 仓场/盐课/库/场 短名后缀
CANGCHANG_SUF = ("河泊所", "税课司", "税课局", "盐课提举司", "盐课司",
                 "分司", "塲", "场", "仓", "库", "局", "所", "司")
INSTIT_KW = ("都督府", "清吏司", "卫", "衞", "官员", "事目", "衙门", "都督", "留守")
REGION_KW = ("布政使司", "布政司", "布政", "直隶", "直", "府", "州", "县")

def nam_type_for(t):
    # 南京机构 / 官制事目
    if any(k in t for k in ("都督府", "清吏司", "留守", "都督")):
        return "官制名录"
    if t.endswith("科"):
        return "官制名录"
    if t.endswith(("官员", "事目", "印", "铜版", "官员")) or t in ("权量", "时估", "钱法", "盐课衙门", "茶盐引印", "斛斗秤尺"):
        return "官制名录"
    # 仓+卫 组合（南新仓八衞）
    if "仓" in t and (t.endswith("衞") or t.endswith("卫")):
        return "仓场名录"
    # 仓场后缀
    if t.endswith(CANGCHANG_SUF):
        return "仓场名录"
    # 卫所
    if t.endswith(("卫", "衞")) and "仓" not in t:
        return "卫所名录"
    # 纯区划
    if any(t.endswith(k) for k in REGION_KW) or len(t) <= 6:
        return "其他"
    return "其他"

# ---- 逐条分类 ----
nam_records = []
rul_records = []
pending = []

nam_seq = {}  # vol -> next seq
rul_seq = {}

for iid in mine:
    vol = int(iid.split("-")[0])
    title = reg[iid]["title"].strip()
    section = reg[iid].get("section", "")

    # 空 title -> pending
    if not title:
        pending.append((iid, "", "empty_title"))
        continue

    try:
        if is_rul_title(title):
            marker = rul_marker(title)
            typ = rul_type(title)
            if marker not in SOURCE_MARKER:
                pending.append((iid, title, "bad_marker:"+marker)); continue
            if typ not in RUL_TYPE:
                pending.append((iid, title, "bad_type:"+typ)); continue
            subj, act = extract_sa(title)
            rul_seq[vol] = rul_seq.get(vol, 0) + 1
            rid = f"RUL-{TAG}-{vol:03d}-{rul_seq[vol]:03d}"
            rul_records.append({
                "id": rid,
                "item_id": iid,
                "type": typ,
                "source_marker": marker,
                "subject": subj,
                "action": act,
                "condition": "",
                "purpose": purpose_for(section),
                "confidence": 0.9,
            })
        else:
            nt = nam_type_for(title)
            if nt not in NAM_TYPE:
                pending.append((iid, title, "bad_nam_type:"+nt)); continue
            nam_seq[vol] = nam_seq.get(vol, 0) + 1
            nid = f"NAM-{TAG}-{vol:03d}-{nam_seq[vol]:03d}"
            nam_records.append({
                "id": nid,
                "item_id": iid,
                "name": title,
                "nam_type": nt,
                "scope": "户部",
                "entries": [],
            })
    except Exception as e:
        pending.append((iid, title, "exc:"+str(e)[:40]))

# ---- 写 _src 文件 ----
def write_records(path, docstring, records):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write(docstring + "\n\n")
        f.write("RECORDS = ")
        json.dump(records, f, ensure_ascii=False, indent=1)
        f.write("\n")

nam_path = os.path.join(ROOT, "_src", "_nam_ai_finb.py")
rul_path = os.path.join(ROOT, "_src", "_rules_ai_finb.py")
write_records(nam_path, f'"""自动生成：{TAG} 卷{VOLS} 仓场/官制名录"""', nam_records)
write_records(rul_path, f'"""自动生成：{TAG} 卷{VOLS} 规则"""', rul_records)

# ---- pending csv ----
pend_path = os.path.join(ROOT, "_pending_finb.csv")
with open(pend_path, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item_id", "title", "reason"])
    for row in pending:
        w.writerow(row)

# ---- 自检 ----
def check(path, kind):
    ns = {}
    with open(path, encoding="utf-8") as f:
        exec(f.read(), ns)
    recs = ns["RECORDS"]
    err = 0
    used_iid = set()
    for r in recs:
        iid = r["item_id"]
        assert iid in reg, f"{iid} not in registry"
        assert iid in mine_set, f"{iid} not in mine"
        assert iid not in used_iid, f"{iid} duplicated"
        used_iid.add(iid)
        if kind == "RUL":
            assert r["type"] in RUL_TYPE, f"bad type {r['type']}"
            assert r["source_marker"] in SOURCE_MARKER, f"bad marker {r['source_marker']}"
        else:
            assert r["nam_type"] in NAM_TYPE, f"bad nam_type {r['nam_type']}"
    return recs, used_iid

nam_recs, nam_iids = check(nam_path, "NAM")
rul_recs, rul_iids = check(rul_path, "RUL")

covered_now = nam_iids | rul_iids
print(f"NAM records: {len(nam_recs)}")
print(f"RUL records: {len(rul_recs)}")
print(f"pending:     {len(pending)}")
print(f"实际覆盖 item_id 数: {len(covered_now)} / mine {len(mine)}")
assert len(covered_now) + len(pending) == len(mine), \
    f"coverage mismatch: {len(covered_now)}+{len(pending)} != {len(mine)}"
print("自检通过：枚举错误=0，所有 item_id 合法且属 mine。")
print("NAM path:", nam_path)
print("RUL path:", rul_path)
print("pending path:", pend_path)
