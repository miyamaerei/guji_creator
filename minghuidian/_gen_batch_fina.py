# -*- coding: utf-8 -*-
"""批量补缺：tag=fina，卷14-31 未覆盖条目自动分类为 NAM / RUL。
只写 _src/_nam_ai_fina.py 与 _src/_rules_ai_fina.py，未命中枚举者写入 _pending_fina.csv。
不运行 build_layers.py / validate_layers.py。
"""
import json, os, re, csv

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ===== 已覆盖集合（四层 item_id 并集）=====
covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

VOLS = list(range(14, 32))  # 14..31
mine = sorted(iid for iid in reg
              if int(iid.split("-")[0]) in VOLS and iid not in covered)

# ===== 封闭枚举（与 _batch_spec.py 对齐）=====
RUL_TYPE = ["禁止", "义务", "允许", "程序", "时限", "处罚", "优先级"]
SOURCE_MARKER = ["诏", "敕", "奏准", "议准", "奏定", "议定", "令", "凡"]
NAM_TYPE = ["王府拟名", "卫所名录", "驿递名录", "仓场名录", "寺观名录",
            "官职题名", "官制名录", "人员配置", "封爵名录", "其他"]
STAFF_ROLE = ["提控", "都吏", "掾史", "令史", "司吏", "典吏",
              "攒典", "承发", "门吏", "狱典", "未明"]

# ===== 分类启发式 =====
ERA_RE = re.compile(r"^(洪武|永乐|宣德|正统|景泰|天顺|成化|弘治|洪熙|建文|洪熙|永乐间|洪武间|国初)")
# 年号 + 令/诏/奏准/奏定/议定/敕/赐/命
MARKER_RE = re.compile(r"(令|诏|奏准|奏定|议定|敕|赐|命|准)")

# RUL 类型关键词
TYPE_FORBID = re.compile(r"不许|不得|毋|勿|禁")
TYPE_LIMIT = re.compile(r"例限|以[^，。]{1,6}为限|不过[^，。]{1,6}日|即日|限十|限八|限六|限二")
TYPE_PUNISH = re.compile(r"笞|杖|发遣|充军|治罪|问罪|遞发|发边")
TYPE_ALLOW = re.compile(r"许|听|聴")

# NAM 类型关键词
# 卫所：含 卫/千户所/都司/都督府/留守司/营（卫名常含"州"字，如通州卫，故不能用"含府州县"排除）
WEI_RE = re.compile(r"卫|千户所|都司|都督府|留守司|神机营|五军营|三千营|随侍营|奋武营|耀武营|立威营|显武营|鼓勇营|效勇营|蕃牧千户所")
# 仓场：仓/场/库/税课司/批验所/马房/象房/厰/厂
CANG_RE = re.compile(r"仓|塲|场|库|税课司|批验所|马房|象房|厰|厂|草场|草塲")
# 区划：布政司/直隶/领县N/县N/结尾府州县/长官司/宣抚司/安抚司/宣慰司
QUHUA_RE = re.compile(r"布政司|直隶|直[隸]|领县|县[一二三四五六七八九十百]+$|府$|州$|县$|"
                      r"长官司|宣抚司|安抚司|宣慰司|军民府|御夷|府领|州领")
# 人员配置：司吏/典吏/攒典 编制短行
STAFF_RE = re.compile(r"司吏|典吏|攒典|掾史|令史|提控|都吏")

# 卷 -> scope（卷14-15 为吏部考功/吏部内容，其余为户部）
def scope_for_vol(v):
    if v in (14, 15):
        return "吏部"
    return "户部"

# 卷 -> purpose 标签（用于 RUL.purpose）
PURPOSE = {
    14: "官吏考满", 15: "官吏考核", 16: "户部各司仓场卫所",
    17: "图志区划", 18: "图志区划", 19: "田土", 20: "户口",
    21: "赋役黄册", 22: "赋役婚姻", 23: "仓场草料", 24: "漕运拨运",
    25: "漕运仓场", 26: "军士给赏", 27: "月盐杂支", 28: "王公共禄米",
    29: "文武官俸给", 30: "俸给", 31: "廪给行粮",
}

def is_rul(title, original):
    """判定是否为规则条目。"""
    t = title.strip()
    if t.startswith("凡") or t.startswith("一凡"):
        return True
    if t.startswith("国初"):
        return True
    # 年号开头
    if ERA_RE.match(t):
        return True
    # 以"一"开头的令条（如一河南山东农民.../一指挥千百户.../一户口仰...）
    if t.startswith("一") and len(t) > 6:
        return True
    # 原文含 诸司职掌 -> 按"凡"处理
    if "诸司职掌" in original:
        return True
    return False

def detect_marker(title, original):
    t = title.strip()
    if t.startswith("凡") or t.startswith("一凡"):
        return "凡"
    if t.startswith("国初"):
        return "凡"
    if "诸司职掌" in original:
        return "凡"
    # 年号 + marker
    m = ERA_RE.match(t)
    if m:
        tail = t[m.end():]
        if tail.startswith("令") or "令" in tail[:4]:
            return "令"
        if tail.startswith("诏") or "诏" in tail[:4]:
            return "诏"
        if "奏准" in tail[:6]:
            return "奏准"
        if "奏定" in tail[:6]:
            return "奏定"
        if "议定" in tail[:6]:
            return "议定"
        if "议准" in tail[:6]:
            return "议准"
        if tail.startswith("敕") or "敕谕" in tail[:6] or "" in tail[:3]:
            return "敕"
        if tail.startswith("赐"):
            return "敕"
        if tail.startswith("命"):
            return "凡"
        return "令"
    if t.startswith("一"):
        return "凡"
    return "凡"

def detect_type(title, marker):
    t = title
    if TYPE_FORBID.search(t):
        return "禁止"
    if TYPE_PUNISH.search(t):
        return "处罚"
    if TYPE_LIMIT.search(t):
        return "时限"
    if TYPE_ALLOW.search(t) and "不许" not in t and "不得" not in t:
        return "允许"
    if marker == "凡" and ("给由" in t or "造册" in t or "申缴" in t or "关支" in t or "放支" in t or "开报" in t):
        return "程序"
    return "义务"

def split_subject_action(title):
    """粗略拆 subject/action：去掉开头标记，前 14 字作 subject，其余作 action。"""
    t = title.strip()
    for pre in ("一凡", "凡", "国初"):
        if t.startswith(pre):
            t = t[len(pre):]
            break
    m = ERA_RE.match(t)
    if m:
        t = t[m.end():]
    # 去掉开头的 令/诏/奏准 等
    t = re.sub(r"^(令|诏|奏准|奏定|议定|敕|赐|命)", "", t)
    t = t.strip()
    subj = t[:14].strip()
    act = t[:50].strip()
    return subj, act

def classify_nam_type(title, vol):
    """返回 (nam_type, scope)。优先级：人员配置 > 卫所 > 仓场 > 区划 > 其他。"""
    t = title.strip()
    # 1. 人员配置（短行且含吏名，无句读）
    if len(t) <= 12 and STAFF_RE.search(t) and not re.search(r"[，。；]", t):
        return "人员配置", scope_for_vol(vol)
    # 2. 卫所（含卫/千户所/都司/都督府/留守司/营；卫名常含"州"字，不可用府州县排除）
    if WEI_RE.search(t):
        return "卫所名录", scope_for_vol(vol)
    # 3. 仓场
    if CANG_RE.search(t):
        return "仓场名录", scope_for_vol(vol)
    # 4. 区划（布政司/直隶/领县N/县N/结尾府州县/长官司等）
    if QUHUA_RE.search(t):
        return "其他", "户部"
    # 5. 兜底短名
    return "其他", scope_for_vol(vol)

# ===== 主循环 =====
nam_records = []
rul_records = []
pending = []  # (item_id, title, reason)

nam_seq = {}  # vol -> seq
rul_seq = {}

for iid in mine:
    rec = reg[iid]
    title = rec["title"]
    original = rec.get("original", "")
    vol = int(iid.split("-")[0])

    try:
        if is_rul(title, original):
            marker = detect_marker(title, original)
            rtype = detect_type(title, marker)
            subj, act = split_subject_action(title)
            if rtype not in RUL_TYPE or marker not in SOURCE_MARKER:
                pending.append((iid, title, f"RUL enum miss type={rtype} marker={marker}"))
                continue
            rul_seq[vol] = rul_seq.get(vol, 0) + 1
            rul_records.append({
                "id": f"RUL-FINA-{vol:03d}-{rul_seq[vol]:03d}",
                "item_id": iid,
                "type": rtype,
                "source_marker": marker,
                "subject": subj,
                "action": act,
                "condition": "",
                "purpose": PURPOSE.get(vol, ""),
                "confidence": 0.9,
            })
        else:
            nt, scope = classify_nam_type(title, vol)
            if nt not in NAM_TYPE or scope not in ("户部", "吏部", "兵部", "礼部", "工部"):
                pending.append((iid, title, f"NAM enum miss type={nt} scope={scope}"))
                continue
            nam_seq[vol] = nam_seq.get(vol, 0) + 1
            nam_records.append({
                "id": f"NAM-FINA-{vol:03d}-{nam_seq[vol]:03d}",
                "item_id": iid,
                "name": title,
                "nam_type": nt,
                "scope": scope,
                "entries": [],
            })
    except Exception as e:
        pending.append((iid, title, f"exception {e!r}"))

# ===== 写 _src 文件 =====
def write_src(path, docstring, records):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write(f'"""{docstring}"""\n\n')
        f.write("RECORDS = ")
        json.dump(records, f, ensure_ascii=False, indent=1)
        f.write("\n")

write_src(os.path.join(ROOT, "_src", "_nam_ai_fina.py"),
          "批量自动生成：fina tag 卷14-31 NAM 名录（区划/仓场/卫所/人员配置）",
          nam_records)
write_src(os.path.join(ROOT, "_src", "_rules_ai_fina.py"),
          "批量自动生成：fina tag 卷14-31 RUL 规则（凡/国初/年号令）",
          rul_records)

# ===== pending csv =====
with open(os.path.join(ROOT, "_pending_fina.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item_id", "title", "reason"])
    for row in pending:
        w.writerow(row)

# ===== 自检 =====
# 1. item_id 合法且属 mine
all_out = [r["item_id"] for r in nam_records] + [r["item_id"] for r in rul_records]
assert set(all_out) <= set(mine), "存在非 mine 的 item_id"
assert len(all_out) == len(set(all_out)), "item_id 重复"
# 2. 枚举全命中
for r in nam_records:
    assert r["nam_type"] in NAM_TYPE, r
for r in rul_records:
    assert r["type"] in RUL_TYPE, r
    assert r["source_marker"] in SOURCE_MARKER, r

print(f"mine 总数: {len(mine)}")
print(f"NAM 生成: {len(nam_records)}")
print(f"RUL 生成: {len(rul_records)}")
print(f"pending: {len(pending)}")
print(f"实际覆盖 item_id 数: {len(all_out)}")
