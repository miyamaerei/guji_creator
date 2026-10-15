# -*- coding: utf-8 -*-
"""通用缺口审计器 v2：对指定卷的 _gap_missing.json 缺口条目做枚举/引用/原文真实性校验。
按字段存在性校验，兼容 style A（卷16/17）与 style B（卷18-20）两套字段名。
用法: python _audit_gap_generic.py 16,17,18,19,20
不写任何文件。
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "scripts"))
import _kg_enums as en  # noqa

LAYERS = ["ents", "rules", "events", "appts", "rels", "opns", "cits", "mings", "tmes", "regs"]
IDKEY = {"ents": "ent_id", "rules": "rule_id", "events": "event_id", "appts": "appt_id",
         "rels": "rel_id", "cits": "cit_id", "opns": "opn_id", "mings": "ming_id",
         "tmes": "tme_id", "regs": "reg_id"}

vols = sys.argv[1].split(",")
gap = json.load(open(BASE / "_gap_missing.json", encoding="utf-8"))
want = set()
for v in vols:
    want.update(gap.get(v, []))

fails = []

bag = {}
for L in LAYERS:
    recs_all = []
    for v in vols:
        d = json.load(open(BASE / "_layers" / L / f"{L}_{v}.json", encoding="utf-8"))
        recs_all += d["records"] if isinstance(d, dict) else d
    bag[L] = [r for r in recs_all if r["item_id"] in want]

covered = {r["item_id"] for L in LAYERS for r in bag[L]}
print(f"coverage: {len(covered)} / {len(want)}")
if want - covered:
    fails.append(f"未覆盖 {sorted(want - covered)}")

for L in LAYERS:
    ids = [r[IDKEY[L]] for r in bag[L]]
    if len(ids) != len(set(ids)):
        dup = sorted({x for x in ids if ids.count(x) > 1})
        fails.append(f"ID 重复 {L}: {dup[:8]}")

def chk(val, allowed, msg):
    if val is None:
        return
    if isinstance(val, list):
        for x in val:
            if x is not None and x not in allowed:
                fails.append("ENUM %s -> %r" % (msg, x))
        return
    if val not in allowed:
        fails.append("ENUM %s -> %r" % (msg, val))

RULE_TYPE_ENUM = dict(en.RULE_TYPES)
RULE_TYPE_ENUM.setdefault("司法", "司法")
RULE_TYPE_ENUM.setdefault("刑法", "刑法")
RULE_TYPE_ENUM.setdefault("礼制", "礼制")
RULE_TYPE_ENUM.setdefault("军政", "军政")

for L in LAYERS:
    for r in bag[L]:
        rid = r[IDKEY[L]]
        if L == "ents":
            chk(r.get("type"), en.ENTITY_TYPES, "ent.type " + rid)
            chk(r.get("role_in_entry"), en.ENTRY_ROLES, "ent.role " + rid)
            chk(r.get("faction"), en.FACTIONS, "ent.faction " + rid)
            chk(r.get("confidence"), en.CONFIDENCE, "ent.conf " + rid)
        elif L == "rules":
            chk(r.get("type") or r.get("rule_type"), RULE_TYPE_ENUM, "rule.type " + rid)
            chk(r.get("rule_origin") or r.get("origin"), en.RULE_ORIGINS, "rule.origin " + rid)
            chk(r.get("actual_practice") or r.get("practice"), en.ACTUAL_PRACTICE, "rule.practice " + rid)
        elif L == "events":
            chk(r.get("type") or r.get("event_type"), en.EVENT_TYPES, "evt.type " + rid)
            chk(r.get("source_type"), en.SOURCE_TYPES, "evt.src " + rid)
            chk(r.get("vs_official_history"), en.VS_OFFICIAL_HISTORY, "evt.vsh " + rid)
            chk(r.get("firsthand_witness"), en.FIRSTHAND, "evt.fw " + rid)
            chk(r.get("commentary_type"), en.COMMENTARY_TYPES, "evt.ct " + rid)
        elif L == "appts":
            chk(r.get("status"), en.APPT_STATUS, "appt.status " + rid)
            chk(r.get("controversy"), en.CONTROVERSY, "appt.controv " + rid)
        elif L == "rels":
            chk(r.get("relation_type") or r.get("relation"), en.RELATION_TYPES, "rel.type " + rid)
            chk(r.get("direction"), en.DIRECTION, "rel.dir " + rid)
            chk(r.get("evidence_strength"), en.EVIDENCE_STRENGTH, "rel.es " + rid)
        elif L == "cits":
            chk(r.get("citation_type") or r.get("type"), en.CITATION_TYPES, "cit.type " + rid)
            chk(r.get("citation_purpose") or r.get("purpose"), en.CITATION_PURPOSES, "cit.purpose " + rid)
        elif L == "opns":
            chk(r.get("stance"), en.STANCES, "opn.stance " + rid)
            chk(r.get("commentary_type"), en.COMMENTARY_TYPES, "opn.ct " + rid)
            chk(r.get("tone"), en.TONES, "opn.tone " + rid)
            chk(r.get("firsthand_witness"), en.FIRSTHAND, "opn.fw " + rid)
            chk(r.get("faction"), en.FACTIONS, "opn.faction " + rid)
        elif L == "mings":
            chk(r.get("category") or r.get("type"), en.MING_CATEGORIES, "ming.cat " + rid)
            chk(r.get("reign_focus"), en.REIGN_FOCUS, "ming.rf " + rid)
            chk(r.get("firsthand_witness"), en.FIRSTHAND, "ming.fw " + rid)
        elif L == "tmes":
            era = r.get("era")
            reign = era.get("reign") if isinstance(era, dict) else r.get("reign")
            chk(reign, en.REIGN_ORDER, "tme.reign " + rid)
            if isinstance(era, dict) and era.get("reign") in en.REIGN_ORDER:
                if era.get("order") != en.REIGN_ORDER[era["reign"]]:
                    fails.append("ENUM tme.order %s -> %r" % (rid, era.get("order")))
            chk(r.get("category") or r.get("cat"), en.TME_CATEGORIES, "tme.cat " + rid)
        elif L == "regs":
            chk(r.get("category") or r.get("cat") or r.get("type"), en.REG_CATEGORIES, "reg.cat " + rid)
            chk(r.get("vs_official_history"), en.VS_OFFICIAL_HISTORY, "reg.vsh " + rid)

ent_pool = set()
for f in (BASE / "_layers" / "ents").glob("ents_*.json"):
    d = json.load(open(f, encoding="utf-8"))
    recs = d["records"] if isinstance(d, dict) else d
    ent_pool.update(r["ent_id"] for r in recs)
for L in LAYERS:
    for r in bag[L]:
        for k, val in r.items():
            vals = val if isinstance(val, list) else [val]
            for x in vals:
                if isinstance(x, str) and x.startswith("ENT-") and x not in ent_pool:
                    fails.append(f"断链 ENT {L} {r[IDKEY[L]]} {k} -> {x}")

txt = open(BASE / "assets" / "sources" / "万历野获编.txt", encoding="utf-8").read()
d0 = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}


def cnum(s):
    if s == "十":
        return 10
    if "十" in s:
        a, b = s.split("十")
        return (d0.get(a, 1)) * 10 + (d0.get(b, 0) if b else 0)
    return d0[s]


pos = dict((cnum(m.group(1)), m.start()) for m in re.finditer(r"●卷([一二三四五六七八九十]+)", txt))
order = sorted(pos)


def norm(s):
    return re.sub(r"[\s\u3000]", "", s or "")


seg = {}
for iid in want:
    vn = int(iid[:2])
    nxt = [x for x in order if x > vn]
    seg[iid] = norm(txt[pos[vn]:(pos[nxt[0]] if nxt else len(txt))])

ORIG_FIELDS = ("original", "evidence", "quoted_text", "source_text", "st")
miss_orig = []
for L in LAYERS:
    for r in bag[L]:
        for k in ORIG_FIELDS:
            val = r.get(k)
            if isinstance(val, str) and val and "……" not in val and len(val) >= 8:
                iid = r["item_id"]
                if iid in seg and norm(val) not in seg[iid]:
                    parts = [p for p in re.split(r"……|；", val) if p.strip()]
                    if not all(norm(p) in seg[iid] for p in parts):
                        miss_orig.append((L, r[IDKEY[L]], k, val[:36]))
print("original 疑似不实条目数:", len(miss_orig))
seen = set()
for m in miss_orig:
    if m[1] not in seen:
        seen.add(m[1])
        print("   ", m)

print()
print("FAILS:", len(fails))
for f in fails[:40]:
    print("   ", f)
print("counts:", {v: sum(1 for L in LAYERS for r in bag[L] if r["item_id"].startswith(v + "-")) for v in vols})
print("AUDIT:", "PASS" if not fails and not miss_orig else "HAS-FAILS")
