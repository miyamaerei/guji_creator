# -*- coding: utf-8 -*-
"""
P4-B 跨层索引补强（打通与交付 · 第二件）

背景：P2-E 的 `_kg_join.json` 有 1306 条 layer_count=0（完全孤立），
      主因是 —— 只用"逐层已有记录"挂载，孤立条（职掌长文 / 名册行 / 事目）
      从未被任何抽取器覆盖。

本步做三件事：

  1) 内容法补齐（content-based fill）
     - 用 office_profiles / org_profiles / geo / objs / dress / num 的词表，
       对**每条 item 的 norm+original 正文**做最长匹配挂载；
     - 与旧法不同：旧法的 `orgs` 桶只匹配 ORG_NAMES 且硬截 20 条、且把
       "条目→衙门"当作单一来源；这里改为**多桶内容命中 + 去重**。

  2) 新增 `mentions` 桶（轻量实体提及索引）
     - 对孤立条（及所有条）登记 office/org/geo 的"提及"，
       让"某官职/某地牵涉哪些条目"可反查，而不必先在实体层建号。

  3) layer_count 重算 + 孤立条审计
     - 输出 `_p4_orphans.json`（仍孤立的条目及原因），供后续人工处置。

重跑幂等：读 _layers/*.json + _item_registry.json → 写 _kg_join.json / _kg_join_flat.csv。
"""
import json, os, csv, re
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")

reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

VOL2GROUP = {1: "G0 宗人府"}
for v in range(2, 16):    VOL2GROUP[v] = "G1 吏部"
for v in range(16, 42):   VOL2GROUP[v] = "G2 户部"
for v in range(42, 106):  VOL2GROUP[v] = "G3 礼部"
for v in range(106, 130): VOL2GROUP[v] = "G4 兵部"
for v in range(130, 144): VOL2GROUP[v] = "G5 刑部"
for v in range(144, 164): VOL2GROUP[v] = "G6 工部"
for v in range(164, 179): VOL2GROUP[v] = "G7 诸文职"
for v in range(179, 181): VOL2GROUP[v] = "G8 诸武职"

PUA = {0xE5AB: "隶", 0xEA1F: "寮", 0xF5F6: "灏", 0xEB08: "卷"}


def nz(t):
    return "".join(PUA.get(ord(c), c) for c in (t or ""))


def load(name):
    p = os.path.join(LAYERS, name + ".json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


OLD = ["ents", "rules", "nams", "cits", "laws", "inspect", "rituals", "dress",
       "foreign", "materials", "eng_tags", "person_profiles", "process_profiles"]
NEW = ["rank", "njc", "xref", "geo", "num", "reports", "objs", "rank_sequence"]
L = {n: load(n) for n in OLD + NEW}
org_profiles = load("org_profiles")
office_profiles = load("office_profiles")
RANK_SEQ = L["rank_sequence"]

ORG_BLACK = {"群", "司务厅", "照磨所", "经历司", "检校", "巡检司", "牧监", "税课司局",
             "河泊所", "批验所", "都指挥使司", "卫指挥使司", "千户所", "百户所",
             "提刑按察使司", "各祠祭署", "五官正", "太医院十三科"}

# ---------- 官名词表扩展（P4-B）----------
# office_profiles 只收了 566 个"有档案"的官（主要是京官）。
# 但卷12 品级名录里的地方/土司/杂职官（宣慰司同知、盐运司副使、𨔛运所大使…）
# 未进档案，导致名录行全成孤立条。
# 这里从 rank_sequence 的段落**抽取官名，建成"补充官名词表"**，
# 只用于 join 的 mentions/offices 挂载，不改写 office_profiles（保持档案层纯净）。
import re as _re

SUPP_OFFICE = set()
# 官名尾缀（可作为切分右边界）
OFF_TAIL = ("使", "丞", "郎", "卿", "正", "副", "判", "簿", "事", "史", "目", "监",
            "令", "守", "抚", "讨", "长", "官", "校", "库", "局", "仓", "所", "卫",
            "知州", "知县", "知府", "同知", "通判", "推官", "典史", "教谕", "训导",
            "大使", "副使", "提举", "吏目", "检校", "照磨", "都事", "经历")


def harvest_offices(seg):
    """从品级名录段落里切出候选官名。段内常无标点，用衙门前缀 + 尾缀切分。"""
    out = []
    # 先按常见衙门/机构前缀切
    parts = _re.split(r"(?<=[监寺司院府卫局库所仓州学])", seg)
    for p in parts:
        p = p.strip()
        if not p or len(p) < 3 or len(p) > 14:
            continue
        if p in JUNK_SEG:
            continue
        if p.endswith(OFF_TAIL) or p.startswith(("各", "左右", "王府", "中都")):
            out.append(p)
    return out


JUNK_SEG = {"左右", "各", "王府", "旧制", "凡", "已上增"}

for r in RANK_SEQ:
    for seg in r["segments"]:
        for name in harvest_offices(seg):
            SUPP_OFFICE.add(name)

# 过滤：与已知官名重复的丢掉；长度过短的非官名丢掉
SUPP_OFFICE = {x for x in SUPP_OFFICE if x not in {p["office_name"] for p in office_profiles}
               and len(x) >= 3}

ORG_NAMES = sorted({p["org_name"] for p in org_profiles if p["org_name"] not in ORG_BLACK},
                   key=len, reverse=True)
OFF_NAMES = sorted({p["office_name"] for p in office_profiles}, key=len, reverse=True)
SUPP_OFFICE_SORTED = sorted(SUPP_OFFICE, key=len, reverse=True)
GEO_NAMES = sorted({g["name"] for g in L["geo"] if g.get("name") and len(g["name"]) >= 2},
                   key=len, reverse=True)

# ---------- 1) 构建 join 骨架 ----------
BUCKETS = ["rules", "ents", "nams", "cits", "laws", "inspect", "rituals", "dress",
           "foreign", "materials", "eng", "offices", "process", "orgs",
           "rank", "rank_seq", "njc", "xref", "geo", "num", "reports", "objs", "mentions"]

join = {}
for iid, it in reg.items():
    vol = it.get("volume") or int(iid.split("-")[0])
    j = {"item_id": iid, "volume": vol, "group": VOL2GROUP.get(vol, ""),
         "node_kind": it.get("node_kind", ""), "section": it.get("section", ""),
         "title": (it.get("title") or "")[:60], "layer_count": 0}
    for b in BUCKETS:
        j[b] = []
    join[iid] = j


def add(key, iid, rec):
    if iid and iid in join:
        join[iid][key].append(rec)


# ---------- 2) 逐层挂载（沿用 P2-E 口径）----------
for r in L["rules"]:
    add("rules", r.get("item_id"), {"rule_id": r.get("id") or r.get("rule_id", ""),
                                    "type": r.get("type", ""), "subject": r.get("subject", ""),
                                    "era": r.get("era", ""), "event_types": r.get("event_types", [])})
for e in L["ents"]:
    add("ents", e.get("item_id"), {"text": e.get("text", ""), "type": e.get("type", "")})
for n in L["nams"]:
    add("nams", n.get("item_id"), {"nam_type": n.get("nam_type", ""), "name": n.get("name", "")})
for c in L["cits"]:
    add("cits", c.get("item_id"), {"cited_work": c.get("cited_work", "")})
for x in L["laws"]:
    add("laws", x.get("item_id"), {"crime": x.get("crime", ""), "punishment_type": x.get("punishment_type", "")})
for x in L["inspect"]:
    add("inspect", x.get("item_id"), {"affair_type": x.get("affair_type", ""), "name": x.get("name", "")})
for x in L["rituals"]:
    add("rituals", x.get("item_id"), {"ritual_type": x.get("ritual_type", ""), "ritual_name": x.get("ritual_name", "")})
for x in L["dress"]:
    add("dress", x.get("item_id"), {"category": x.get("category", ""), "name": x.get("name", "")})
for x in L["foreign"]:
    add("foreign", x.get("item_id"), {"type": x.get("type", ""), "name": x.get("name", "")})
for x in L["materials"]:
    add("materials", x.get("item_id"), {"material": x.get("material", ""), "quantity": x.get("quantity", ""),
                                        "unit": x.get("unit", "")})
for x in L["eng_tags"]:
    add("eng", x.get("item_id"), {"sublayer": x.get("sublayer", ""), "title": x.get("title", "")})
for x in L["person_profiles"]:
    add("offices", x.get("item_id"), {"office_name": x.get("office_name", "")})
for x in L["process_profiles"]:
    add("process", x.get("item_id"), {"process_name": x.get("process_name", ""),
                                      "process_type": x.get("process_type", "")})
for r in L["rank"]:
    for cat, iid in (r.get("sources") or {}).items():
        add("rank", iid, {"rank_id": r.get("rank_id"), "level": r.get("level"),
                          "category": r.get("category"), "cat": cat})
for x in L["njc"]:
    for key, role in (("beijing_item", "北京"), ("nanjing_item", "南京"), ("source_item", "凡例")):
        add("njc", x.get(key), {"njc_id": x.get("njc_id"), "type": x.get("type"),
                                "topic": x.get("topic"), "role": role})
for x in L["xref"]:
    add("xref", x.get("from_item"), {"xref_id": x.get("xref_id"), "ref_type": x.get("ref_type"),
                                     "target": x.get("target"), "target_org": x.get("target_org", "")})
for x in L["geo"]:
    if len(join.get(x.get("item_id"), {}).get("geo", [])) < 60:
        add("geo", x.get("item_id"), {"geo_id": x.get("geo_id"), "name": x.get("name"),
                                      "type": x.get("type"), "level": x.get("level")})
for x in L["num"]:
    add("num", x.get("item_id"), {"num_id": x.get("num_id"), "subject": x.get("subject"),
                                  "quantity": x.get("quantity"), "unit": x.get("unit"),
                                  "category": x.get("category")})
for x in L["reports"]:
    add("reports", x.get("item_id"), {"rep_id": x.get("rep_id"), "doc_name": x.get("doc_name"),
                                      "doc_category": x.get("doc_category")})
for x in L["objs"]:
    add("objs", x.get("item_id"), {"obj_id": x.get("obj_id"), "obj_name": x.get("obj_name"),
                                   "obj_category": x.get("obj_category")})

# rank_sequence（P4-C 新增）：卷12 文职品级名录 → 每个品级段挂到它所属的 item
PIN_ORDER = ["正一品", "从一品", "正二品", "从二品", "正三品", "从三品",
             "正四品", "从四品", "正五品", "从五品", "正六品", "从六品",
             "正七品", "从七品", "正八品", "从八品", "正九品", "从九品", "未入流"]
RANK_LEVEL_BY_ITEM = defaultdict(set)
for r in RANK_SEQ:
    for iid in r.get("item_ids") or []:
        RANK_LEVEL_BY_ITEM[iid].add(r["level"])
for iid, lvs in RANK_LEVEL_BY_ITEM.items():
    ordered = [x for x in PIN_ORDER if x in lvs]
    add("rank_seq", iid, {
        "levels": ordered,
        "top_level": ordered[0] if ordered else "",
        "segments": sum(r["segment_count"] for r in RANK_SEQ if r["level"] in lvs),
    })

# ---------- 3) 内容法补强（P4 新增）----------
# 3.1 orgs 桶：放宽上限、按正文最长命中（替 P2-E 的"标题+原文 in blob"）
for iid, it in reg.items():
    blob = nz((it.get("title") or "") + (it.get("original") or ""))
    hit = [o for o in ORG_NAMES if o in blob]
    # 去包含：若 A 是 B 的子串且都命中，只留最长
    hit = [h for h in hit if not any(h != k and h in k for k in hit)]
    join[iid]["orgs"] = hit[:30]

# 3.2 mentions 桶：实体提及（office / org / geo），供"某官/某地→条目"反查
GEO_STOP = {"京师", "南京", "北京", "中都", "中国", "天下", "本府", "本县", "本州"}


def mentions_of(blob):
    off = [o for o in OFF_NAMES if o in blob and len(o) >= 3]
    off = [h for h in off if not any(h != k and h in k for k in off)]
    sup = [o for o in SUPP_OFFICE_SORTED if o in blob]
    sup = [h for h in sup if not any(h != k and h in k for k in sup)]
    org = [o for o in ORG_NAMES if o in blob]
    org = [h for h in org if not any(h != k and h in k for k in org)]
    geo = [g for g in GEO_NAMES if g in blob and g not in GEO_STOP]
    geo = [h for h in geo if not any(h != k and h in k for k in geo)]
    return (off[:25], sup[:25], org[:25], geo[:25])


for iid, it in reg.items():
    blob = nz((it.get("title") or "") + (it.get("original") or ""))
    off, sup, org, geo = mentions_of(blob)
    join[iid]["mentions"] = ([{"kind": "office", "name": x} for x in off]
                             + [{"kind": "office_sup", "name": x} for x in sup]
                             + [{"kind": "org", "name": x} for x in org]
                             + [{"kind": "geo", "name": x} for x in geo])

# 3.3 用 mentions 回填 offices / geo 桶（补孤立条）
off_by_name = {x["office_name"]: x for x in office_profiles}
geo_by_name = defaultdict(list)
for g in L["geo"]:
    geo_by_name[g["name"]].append(g)

for iid, j in join.items():
    if not j["offices"]:
        for m in j["mentions"]:
            if m["kind"] == "office" and m["name"] in off_by_name:
                o = off_by_name[m["name"]]
                j["offices"].append({"office_name": o["office_name"], "rank": o.get("rank", ""),
                                     "system": o.get("system", "")})
            elif m["kind"] == "office_sup":
                j["offices"].append({"office_name": m["name"], "rank": "",
                                     "system": "", "supp": True})
    if not j["geo"]:
        for m in j["mentions"]:
            if m["kind"] == "geo" and m["name"] in geo_by_name:
                for g in geo_by_name[m["name"]][:3]:
                    j["geo"].append({"geo_id": g["geo_id"], "name": g["name"],
                                     "type": g["type"], "level": g.get("level", "")})

# 3.4 职掌长文 → 挂其所属衙门（用 orgs 桶已有结果，这里补 note 型记录）
for iid, j in join.items():
    if j["node_kind"] == "长文" and j["orgs"] and not j["offices"]:
        j["offices"] = [{"office_name": "(职掌文)", "rank": "", "system": "",
                         "note": "该条为 " + j["orgs"][0] + " 职掌长文"}]

# ---------- 4) 去重 + layer_count ----------
for j in join.values():
    for b in BUCKETS:
        if b == "mentions":
            continue
        if isinstance(j[b], list) and j[b] and isinstance(j[b][0], dict):
            seen, uniq = set(), []
            for x in j[b]:
                k = tuple(sorted((kk, str(vv)) for kk, vv in x.items() if kk != "note"))
                if k in seen:
                    continue
                seen.add(k)
                uniq.append(x)
            j[b] = uniq
    j["layer_count"] = sum(1 for b in BUCKETS if b != "mentions" and j[b])

join_list = sorted(join.values(), key=lambda x: x["item_id"])
json.dump(join_list, open(os.path.join(ROOT, "_kg_join.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

with open(os.path.join(ROOT, "_kg_join_flat.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item_id", "volume", "group", "node_kind", "section", "title", "layer_count"]
               + [b for b in BUCKETS if b != "mentions"] + ["mentions"])
    for j in join_list:
        w.writerow([j["item_id"], j["volume"], j["group"], j["node_kind"], j["section"],
                    j["title"], j["layer_count"]]
                   + [len(j[b]) for b in BUCKETS if b != "mentions"] + [len(j["mentions"])])

# ---------- 5) 孤立条审计 ----------
orph = [j for j in join_list if j["layer_count"] == 0]
orph_audit = []
for j in orph:
    it = reg[j["item_id"]]
    orph_audit.append({
        "item_id": j["item_id"], "volume": j["volume"], "group": j["group"],
        "node_kind": j["node_kind"], "section": j["section"], "title": j["title"],
        "mentions": len(j["mentions"]),
        "text_len": len(it.get("original") or ""),
        "reason": ("无任何词表命中" if not j["mentions"]
                   else "仅命中提及、未构成层记录"),
    })
json.dump(orph_audit, open(os.path.join(ROOT, "_p4_orphans.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ---------- 6) 校验输出 ----------
lc = Counter(j["layer_count"] for j in join_list)
print("=" * 68)
print("P4-B 跨层索引补强")
print("=" * 68)
print(f"\njoin 条目 {len(join_list)} ｜ 子层 {len(BUCKETS)}（含 mentions）")
print("\n[各桶挂载条目数]")
for b in BUCKETS:
    n = sum(1 for j in join_list if j[b])
    print(f"  {b:12s} {n:6d}")
print("\n[layer_count 分布]")
for k in sorted(lc):
    print(f"  {k:2d} 层: {lc[k]:6d}")
multi = sum(v for k, v in lc.items() if k >= 2)
print(f"  多层覆盖(≥2层): {multi} 条 ({multi * 100 // len(join_list)}%)")
print(f"\n孤立条(layer_count=0): {len(orph)}")
print(f"  其中「仅命中提及」: {sum(1 for x in orph_audit if x['mentions'])}")
print(f"  其中「无任何词表命中」: {sum(1 for x in orph_audit if not x['mentions'])}")
print(f"  孤立条 node_kind: {dict(Counter(x['node_kind'] for x in orph_audit))}")
print(f"  孤立条 volume top: {dict(Counter(x['volume'] for x in orph_audit).most_common(8))}")
print(f"\n写出: _kg_join.json / _kg_join_flat.csv / _p4_orphans.json")
