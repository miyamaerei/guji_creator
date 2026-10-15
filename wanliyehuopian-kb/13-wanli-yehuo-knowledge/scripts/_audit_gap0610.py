# -*- coding: utf-8 -*-
"""gen_gap0610 预检：覆盖/ID/ENT引用/枚举（不写文件）"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "scripts"))
import gen_gap0610 as G  # noqa
import _kg_enums as en  # noqa

layers = ["ents", "rules", "events", "appts", "rels", "cits", "opns", "mings", "tmes", "regs"]
idkeys = {"ents": "ent_id", "rules": "rule_id", "events": "event_id", "appts": "appt_id",
          "rels": "rel_id", "cits": "cit_id", "opns": "opn_id", "mings": "ming_id",
          "tmes": "tme_id", "regs": "reg_id"}
miss = json.load(open(BASE / "_gap_missing.json", encoding="utf-8"))
want = set()
for v in ["06", "07", "08", "09", "10"]:
    want.update(miss[v])

fails = []

cov = set()
for v, Ls in G.NEW.items():
    for L, rs in Ls.items():
        for r in rs:
            cov.add(r["item_id"])
if cov - want:
    fails.append(f"新记录引用了非缺失条目: {sorted(cov - want)}")
if want - cov:
    fails.append(f"未覆盖: {sorted(want - cov)}")
print("coverage:", len(cov & want), "/", len(want))

def num(i):
    if i.startswith("ENT-"):
        return int(i[4:])
    return int(re.findall(r"\d+", i)[-1])

allents = {}
for v in ["06", "07", "08", "09", "10"]:
    d = json.load(open(BASE / "_layers" / "ents" / f"ents_{v}.json", encoding="utf-8"))
    old = d["records"] if isinstance(d, dict) else d
    for r in old:
        allents[r["ent_id"]] = r["item_id"]
for v in G.NEW:
    for r in G.NEW[v].get("ents", []):
        allents[r["ent_id"]] = r["item_id"]
new_ents = [x for x in allents if int(x[4:]) >= 4200]
if not all(4200 <= int(x[4:]) <= 4399 for x in new_ents):
    fails.append("ENT 池越界")

for v in ["06", "07", "08", "09", "10"]:
    for L in layers:
        d = json.load(open(BASE / "_layers" / L / f"{L}_{v}.json", encoding="utf-8"))
        old = d["records"] if isinstance(d, dict) else d
        oldids = [r[idkeys[L]] for r in old]
        new = G.NEW[v].get(L, [])
        newids = [r[idkeys[L]] for r in new]
        if len(newids) != len(set(newids)):
            fails.append(f"新记录内部重复 {L}_{v}")
        if set(newids) & set(oldids):
            fails.append(f"新旧 ID 冲突 {L}_{v}: {sorted(set(newids) & set(oldids))}")
        if not all(x.startswith({"ents": "ENT-", "rules": "RULE-", "events": "EVT-",
                                 "appts": "APPT-", "rels": "REL-", "cits": "CIT-",
                                 "opns": "OPN-", "mings": "MING-", "tmes": "YHB-TME-",
                                 "regs": "REG-"}[L]) for x in newids):
            fails.append(f"前缀错误 {L}_{v}")
        if oldids and any(num(x) <= max(num(y) for y in oldids) for x in newids):
            fails.append(f"序号未顺延 {L}_{v}: {newids} oldmax={max(num(y) for y in oldids)}")

for v in G.NEW:
    for L, rs in G.NEW[v].items():
        for r in rs:
            for k, val in r.items():
                vals = val if isinstance(val, list) else [val]
                for x in vals:
                    if isinstance(x, str) and x.startswith("ENT-") and x not in allents:
                        fails.append(f"断链 ENT 引用 {v}/{L} {r[idkeys[L]]} {k} -> {x}")

def chk(cond, msg):
    if not cond:
        fails.append("ENUM " + msg)

for v in G.NEW:
    for r in G.NEW[v].get("ents", []):
        chk(r["type"] in en.ENTITY_TYPES, f"ent type {r['ent_id']} {r['type']}")
        chk(all(x in en.ENTRY_ROLES for x in r["role_in_entry"]), f"role {r['ent_id']}")
        chk(r["faction"] in en.FACTIONS, f"faction {r['ent_id']} {r['faction']}")
        chk(r["confidence"] in en.CONFIDENCE, f"conf {r['ent_id']} {r['confidence']}")
    for r in G.NEW[v].get("rules", []):
        chk(r["type"] in en.RULE_TYPES, f"rule type {r['rule_id']} {r['type']}")
        chk(r["rule_origin"] in en.RULE_ORIGINS, f"origin {r['rule_id']} {r['rule_origin']}")
        chk(r["actual_practice"] in en.ACTUAL_PRACTICE, f"practice {r['rule_id']} {r['actual_practice']}")
    for r in G.NEW[v].get("events", []):
        chk(r["type"] in en.EVENT_TYPES, f"evt type {r['event_id']} {r['type']}")
        chk(r["event_significance"] in en.EVENT_SIGNIFICANCE, f"sig {r['event_id']} {r['event_significance']}")
        chk(r["source_type"] in en.SOURCE_TYPES, f"src {r['event_id']} {r['source_type']}")
        chk(r["vs_official_history"] in en.VS_OFFICIAL_HISTORY, f"vsh {r['event_id']} {r['vs_official_history']}")
    for r in G.NEW[v].get("appts", []):
        chk(r["status"] in en.APPT_STATUS, f"status {r['appt_id']} {r['status']}")
        chk(r["controversy"] in en.CONTROVERSY, f"controv {r['appt_id']} {r['controversy']}")
    for r in G.NEW[v].get("rels", []):
        chk(r["relation_type"] in en.RELATION_TYPES, f"reltype {r['rel_id']} {r['relation_type']}")
        chk(r["direction"] in en.DIRECTION, f"dir {r['rel_id']} {r['direction']}")
        chk(r["evidence_strength"] in en.EVIDENCE_STRENGTH, f"es {r['rel_id']} {r['evidence_strength']}")
    for r in G.NEW[v].get("cits", []):
        chk(r["citation_type"] in en.CITATION_TYPES, f"cittype {r['cit_id']} {r['citation_type']}")
        chk(r["citation_purpose"] in en.CITATION_PURPOSES, f"cp {r['cit_id']} {r['citation_purpose']}")
    for r in G.NEW[v].get("opns", []):
        chk(r["stance"] in en.STANCES, f"stance {r['opn_id']} {r['stance']}")
        chk(r["commentary_type"] in en.COMMENTARY_TYPES, f"ct {r['opn_id']} {r['commentary_type']}")
        chk(r["tone"] in en.TONES, f"tone {r['opn_id']} {r['tone']}")
        chk(r["firsthand_witness"] in en.FIRSTHAND, f"fw {r['opn_id']} {r['firsthand_witness']}")
    for r in G.NEW[v].get("mings", []):
        chk(r["category"] in en.MING_CATEGORIES, f"mc {r['ming_id']} {r['category']}")
        chk(r["reign_focus"] in en.REIGN_FOCUS, f"rf {r['ming_id']} {r['reign_focus']}")
        chk(r["firsthand_witness"] in en.FIRSTHAND, f"fw {r['ming_id']} {r['firsthand_witness']}")
    for r in G.NEW[v].get("tmes", []):
        chk(r["era"]["reign"] in en.REIGN_ORDER, f"reign {r['tme_id']} {r['era']['reign']}")
        chk(r["era"]["order"] == en.REIGN_ORDER[r["era"]["reign"]], f"order {r['tme_id']}")
        chk(r["category"] in en.TME_CATEGORIES, f"tc {r['tme_id']} {r['category']}")
    for r in G.NEW[v].get("regs", []):
        chk(r["category"] in en.REG_CATEGORIES, f"rc {r['reg_id']} {r['category']}")
        chk(r["vs_official_history"] in en.VS_OFFICIAL_HISTORY, f"vsh {r['reg_id']} {r['vs_official_history']}")

# EVT/TME 跨层引用闭合（ref_events / tme_ids / related_events 允许指向本卷旧记录或新记录）
for v in G.NEW:
    vt = set()
    for L, rs in G.NEW[v].items():
        for r in rs:
            vt.add(r[idkeys[L]])
    old_ids = set()
    for L in layers:
        d = json.load(open(BASE / "_layers" / L / f"{L}_{v}.json", encoding="utf-8"))
        old = d["records"] if isinstance(d, dict) else d
        oldids = {r[idkeys[L]] for r in old}
    for r in G.NEW[v].get("mings", []):
        for x in r["ref_events"]:
            if x not in vt and x not in oldids:
                fails.append(f"ref_events 断链 {r['ming_id']} -> {x}")
    for r in G.NEW[v].get("regs", []):
        for x in r["tme_ids"]:
            if x not in vt and x not in oldids:
                fails.append(f"tme_ids 断链 {r['reg_id']} -> {x}")
    for r in G.NEW[v].get("events", []):
        for x in r["related_events"]:
            if x not in vt and x not in oldids:
                fails.append(f"related_events 断链 {r['event_id']} -> {x}")

# original 真实性：新记录中所有非空 original 应为该条目源文（去空白）子串
txt = open(BASE / "assets" / "sources" / "万历野获编.txt", encoding="utf-8").read()
d0 = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def cnum(s):
    if s == "十":
        return 10
    if "十" in s:
        a, b = s.split("十")
        return (d0.get(a, 1)) * 10 + (d0.get(b, 0) if b else 0)
    return d0[s]


marks = [(cnum(m.group(1)), m.start()) for m in re.finditer(r"●卷([一二三四五六七八九十]+)", txt)]
pos = dict(marks)
order = sorted(pos)


def norm(s):
    return re.sub(r"[\s\u3000]", "", s or "")


seg = {}
regs = json.load(open(BASE / "_item_registry.json", encoding="utf-8"))["records"]
regbyid = {r["item_id"]: r for r in regs}
for iid in want:
    vn = int(iid[:2])
    nxt = [x for x in order if x > vn]
    st, en_ = pos[vn], (pos[nxt[0]] if nxt else len(txt))
    seg[iid] = norm(txt[st:en_])

miss_orig = []
for v in G.NEW:
    for L, rs in G.NEW[v].items():
        for r in rs:
            for k in ("original", "evidence", "quoted_text", "content"):
                val = r.get(k)
                if k == "content":
                    continue
                if isinstance(val, str) and val and "……" not in val and "，" not in val[:2]:
                    iid = r["item_id"]
                    if iid in seg and norm(val) not in seg[iid]:
                        # 允许引文以……或；分隔的多段：拆段逐段检查
                        parts = [p for p in re.split(r"……|；", val) if p.strip()]
                        if not all(norm(p) in seg[iid] for p in parts):
                            miss_orig.append((L, r[idkeys[L]], k, val[:30]))
print("original 疑似不实条目数:", len(miss_orig))
for m in miss_orig:
    print("  ", m)

print()
print("FAILS:", len(fails))
for f in fails:
    print("  ", f)
print("counts:", {v: {L: len(rs) for L, rs in G.NEW[v].items()} for v in ["06", "07", "08", "09", "10"]})
print("AUDIT:", "PASS" if not fails else "HAS-FAILS")
