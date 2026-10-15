# -*- coding: utf-8 -*-
"""
gen_gap01.py —— 万历野获编 卷01 缺口补全（48 条：01-006 .. 01-053）

背景
----
卷一「列朝」共 53 条（01-001..01-053），其中 01-001..01-005 已在试点阶段完成，
剩余 48 条（01-006..01-053）无任何生成器，须新建。

本脚本与 gen_gap0205.py 同构，但针对卷01 的实际形态做了适配：
  1. 卷01 层文件形态与卷02 一致：ents/rules/events/appts/rels/cits/mings/tmes/regs
     为 {"records": [...]} 包裹形态；**opns 为裸数组**（卷内特例，见 SKILL.md §11.3）。
  2. 卷01 既有 ENT 为 4 位补零形态 ENT-0001..ENT-0050（卷01 槽位 0001-0049，
     但 ENT-0051 起已被卷02 占用）；故新增 ENT 一律使用**全库尾部自由池 ENT-5199 起**，
     与 gen_gap0205.py 一致，避免与任何卷槽位冲突。
  3. 卷01 既有 ID 前缀形态：RULE-01-nnn / EVT-01-nnn / APPT-01-nnn / REL-01-nnn /
     OPN-01-nnn / CIT-01-nnn / MING-01-nnn / **YHB-TME-01-nnn** / REG-01-nnn。

字段风格
--------
卷01 events 用 event_significance / political_impact / source_type / vs_official_history
（与卷02-05 同风格 A）。ents 用 start/end/confidence（风格 A）。

溯源硬校验
----------
所有 original / evidence / quoted_text / ent.text 必须是该条目源文段（去空白）的逐字子串。
任一失败则不写盘。

用法
----
    python -X utf8 gen_gap01.py
"""

import io
import json
import os
import re
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _kg_enums import (  # noqa: E402
    ENTITY_TYPES, ENTRY_ROLES, FACTIONS, CONFIDENCE,
    RULE_TYPES, RULE_ORIGINS, ACTUAL_PRACTICE,
    EVENT_TYPES, EVENT_SIGNIFICANCE, SOURCE_TYPES, VS_OFFICIAL_HISTORY,
    APPT_STATUS, CONTROVERSY,
    RELATION_TYPES, DIRECTION, EVIDENCE_STRENGTH,
    CITATION_TYPES, CITATION_PURPOSES,
    STANCES, COMMENTARY_TYPES, TONES, FIRSTHAND,
    MING_CATEGORIES, REIGN_FOCUS,
    TME_CATEGORIES, REIGN_ORDER,
    REG_CATEGORIES,
)

SRC = os.path.join(BASE, "assets", "sources", "万历野获编.txt")
VOLS = ["01"]

# ---------------------------------------------------------------- 源文分段
_flat = re.sub(r"[\s\u3000]", "", open(SRC, encoding="utf-8").read())
_fpos = [(m.group(1), m.start()) for m in re.finditer(r"【([^】]{1,40})】", _flat)]


def build_segments(vol):
    """{item_id: 去空白源文段}，按 registry 条目与源文【标题】锚点顺序对齐。

    段尾取「全局锚点序列中该锚点的下一个锚点位置」——**不是**本卷内的下一条。
    这是关键：卷内最后一条（01-053）若取本卷下一条会退化为 len(_flat)，
    以致整段吞掉全书（571K 字）。见踩坑记录。
    """
    reg = json.load(open(os.path.join(BASE, "_item_registry.json"), encoding="utf-8"))
    items = [r for r in reg["records"] if r["item_id"].startswith(vol + "-")]
    ordered, idx = [], 0
    for r in items:
        t = r["entry_title"]
        j = None
        for k in range(idx, len(_fpos)):
            if _fpos[k][0] == t:
                j = k
                break
        ordered.append((r["item_id"], t, j))
        if j is not None:
            idx = j + 1
    out = {}
    for (iid, ttl, j) in ordered:
        if j is None:
            continue
        st = _fpos[j][1]
        en = _fpos[j + 1][1] if j + 1 < len(_fpos) else len(_flat)
        out[iid] = _flat[st:en]
    return out, ordered


SEG = {}
ORDERED = {}
for v in VOLS:
    SEG[v], ORDERED[v] = build_segments(v)

# ---------------------------------------------------------------- 校验
ERRORS = []


def q(item, s, field):
    """溯源校验：s 必须可回溯到该条目源文段。

    支持两种形态：
      1) 纯逐字子串 —— 直接 in 判定；
      2) 以省略号「…」连接的**多段连续子串** —— 逐段 in 判定，保证每段都逐字出自源文。
    这样长 original 可摘取首尾而不必抄全文，同时**绝不**放过任何编造文字。
    """
    if s is None:
        return
    seg = SEG.get(SEG_VOL, {}).get(item)
    if seg is None:
        ERRORS.append("%s %s: 无源文段" % (item, field))
        return
    if s in seg:
        return
    parts = [p for p in s.split("…") if p]
    if len(parts) > 1 and all(p in seg for p in parts):
        return
    bad = next((p for p in parts if p not in seg), s)
    ERRORS.append("%s %s: 非原文 %r" % (item, field, bad[:60]))


SEG_VOL = "01"


def chk(ok, msg):
    if not ok:
        ERRORS.append(msg)


# ---------------------------------------------------------------- 构造器
_ent_pool = 5199
ENT_START = 5199


def E(item, text, norm, typ="person", roles=("关联人物",), faction="无",
      exam=None, span=None, conf="high"):
    global _ent_pool
    eid = "ENT-%04d" % _ent_pool
    _ent_pool += 1
    q(item, text, "ent.text")
    chk(typ in ENTITY_TYPES, "ent type %s" % typ)
    for r in roles:
        chk(r in ENTRY_ROLES, "role %s" % r)
    chk(faction in FACTIONS, "faction %s" % faction)
    return {"_eid": eid, "item_id": item, "text": text, "type": typ,
            "normalized": norm, "confidence": conf, "role_in_entry": list(roles),
            "faction": faction, "exam_info": exam, "career_span": span}


def RULE(rid, item, typ, modals, condition, subject, action, original,
         origin, practice, tmark, subj_ents=(), obj=None, purpose=None,
         punishment=None, conf="high", viol=None):
    q(item, original, "rule.original")
    chk(typ in RULE_TYPES, "rule type %s" % typ)
    chk(origin in RULE_ORIGINS, "origin %s" % origin)
    chk(practice in ACTUAL_PRACTICE, "practice %s" % practice)
    return {"rule_id": rid, "item_id": item, "type": typ, "modals": list(modals),
            "condition": condition, "subject": subject,
            "subject_ent_ids": list(subj_ents), "action": action, "object": obj,
            "purpose": purpose, "punishment": punishment, "original": original,
            "confidence": conf, "rule_origin": origin,
            "actual_practice": practice, "violation_evidence": viol,
            "time_marker": tmark}


def EVT(eid, item, typ, who, action, what, when, where, original,
        sig, impact, stype, vs, who_ents=(), related=()):
    q(item, original, "evt.original")
    chk(typ in EVENT_TYPES, "evt type %s" % typ)
    chk(sig in EVENT_SIGNIFICANCE, "evt sig %s" % sig)
    chk(stype in SOURCE_TYPES, "evt stype %s" % stype)
    chk(vs in VS_OFFICIAL_HISTORY, "evt vs %s" % vs)
    return {"event_id": eid, "item_id": item, "type": typ, "who": who,
            "who_ent_ids": list(who_ents), "action": action, "what": what,
            "when": when, "where": where, "original": original,
            "event_significance": sig, "political_impact": impact,
            "source_type": stype, "vs_official_history": vs,
            "related_events": list(related)}


def APPT(aid, item, person, office, when, status, evidence, original,
         person_ents=(), office_ents=(), inst=None, inst_ents=(), ctx=None,
         contro="无争议", faction_impl=None, concurrent=()):
    q(item, original, "appt.original")
    q(item, evidence, "appt.evidence")
    chk(status in APPT_STATUS, "status %s" % status)
    chk(contro in CONTROVERSY, "contro %s" % contro)
    return {"appt_id": aid, "item_id": item, "person": person,
            "person_ent_ids": list(person_ents), "office": office,
            "office_ent_ids": list(office_ents), "institution": inst,
            "institution_ent_ids": list(inst_ents), "when": when, "status": status,
            "evidence": evidence, "original": original,
            "appointment_context": ctx, "controversy": contro,
            "faction_implication": faction_impl, "concurrent_posts": list(concurrent)}


def REL(rid, item, pa, pb, rtype, direction, evidence, original,
        pa_ents=(), pb_ents=(), evo=None, conseq=None, strength="直接表述", span=None):
    q(item, original, "rel.original")
    q(item, evidence, "rel.evidence")
    chk(rtype in RELATION_TYPES, "rt %s" % rtype)
    chk(direction in DIRECTION, "dir %s" % direction)
    chk(strength in EVIDENCE_STRENGTH, "strength %s" % strength)
    return {"rel_id": rid, "item_id": item, "person_a": pa,
            "person_a_ent_ids": list(pa_ents), "person_b": pb,
            "person_b_ent_ids": list(pb_ents), "relation_type": rtype,
            "direction": direction, "evidence": evidence, "original": original,
            "relationship_evolution": evo, "political_consequence": conseq,
            "evidence_strength": strength, "time_span": span}


def CIT(cid, item, work, ctype, context, original, purpose, work_ents=(),
        acc=None, quoted=None):
    q(item, original, "cit.original")
    if quoted:
        q(item, quoted, "cit.quoted_text")
    chk(ctype in CITATION_TYPES, "ctype %s" % ctype)
    chk(purpose in CITATION_PURPOSES, "purpose %s" % purpose)
    return {"cit_id": cid, "item_id": item, "cited_work": work,
            "cited_work_ent_ids": list(work_ents), "citation_type": ctype,
            "context": context, "original": original,
            "citation_purpose": purpose, "accuracy_note": acc,
            "quoted_text": quoted}


def OPN(oid, item, topic, stance, argument, original, ctype, tone, fw,
        targets=(), ev=None, parallel=None):
    q(item, original, "opn.original")
    chk(stance in STANCES, "stance %s" % stance)
    chk(ctype in COMMENTARY_TYPES, "ct %s" % ctype)
    chk(tone in TONES, "tone %s" % tone)
    chk(fw in FIRSTHAND, "fw %s" % fw)
    return {"opn_id": oid, "item_id": item, "topic": topic, "stance": stance,
            "argument": argument, "original": original, "commentary_type": ctype,
            "target_entities": list(targets), "evidence_cited": ev,
            "historical_parallel": parallel, "tone": tone,
            "firsthand_witness": fw}


def MING(mid, item, era, who, what, when, where, category, original,
         reign_focus, fw, who_ents=(), ref_evts=(), first_person=False, supp=None):
    q(item, original, "ming.original")
    chk(category in MING_CATEGORIES, "ming cat %s" % category)
    chk(reign_focus in REIGN_FOCUS, "reign %s" % reign_focus)
    chk(fw in FIRSTHAND, "fw %s" % fw)
    return {"ming_id": mid, "item_id": item, "era": era, "who": who,
            "who_ent_ids": list(who_ents), "what": what, "when": when,
            "where": where, "category": category, "first_person": first_person,
            "ref_events": list(ref_evts), "original": original,
            "reign_focus": reign_focus, "firsthand_witness": fw,
            "supplements_what": supp}


def ERA(reign, text, year=None, dynasty="明"):
    return {"dynasty": dynasty, "reign": reign, "year": year,
            "order": REIGN_ORDER.get(reign), "text": text}


def TME(tid, item, era, target, action, content, category, original,
        target_ents=(), rel_evo=None, rel_org=None, inst_target=None,
        cause=None, before=None, after=None):
    q(item, original, "tme.original")
    chk(category in TME_CATEGORIES, "tme cat %s" % category)
    return {"tme_id": tid, "item_id": item, "era": era, "target": target,
            "target_ent_ids": list(target_ents), "action": action,
            "content": content, "category": category, "related_evo": rel_evo,
            "related_org": rel_org, "ref_item": item, "original": original,
            "institution_target": inst_target, "cause": cause,
            "before_after": {"before": before, "after": after}}


def REG2(rid, item, name, category, establishment, summary, practice, original,
         vs, tme_ids=(), abuses=(), figures=()):
    q(item, original, "reg.original")
    chk(category in REG_CATEGORIES, "reg cat %s" % category)
    chk(practice in ACTUAL_PRACTICE, "practice %s" % practice)
    chk(vs in VS_OFFICIAL_HISTORY, "vs %s" % vs)
    return {"reg_id": rid, "item_id": item, "name": name, "category": category,
            "establishment": establishment, "tme_ids": list(tme_ids),
            "content_summary": summary, "actual_practice": practice,
            "abuses_reform": list(abuses), "key_figures": list(figures),
            "original": original, "vs_official_history": vs}


# ---------------------------------------------------------------- ID 计数器
class Seq:
    def __init__(self, n):
        self.n = n

    def nid(self):
        self.n += 1
        return self.n


# 卷01 现有各层最大序号（实测）：rules 3, events 5, appts 3, rels 2, opns 5,
# cits 2, mings 6, tmes 12, regs 4
NEXT = {
    "01": {"rules": 3, "events": 5, "appts": 3, "rels": 2, "opns": 5,
           "cits": 2, "mings": 6, "tmes": 12, "regs": 4},
}
SEQ = {v: {L: Seq(n) for L, n in d.items()} for v, d in NEXT.items()}
NEW = {v: {} for v in VOLS}


def add(layer, vol, recs):
    NEW[vol].setdefault(layer, []).extend(recs)


def rid(layer, vol, prefix):
    return "%s-%s-%03d" % (prefix, vol, SEQ[vol][layer].nid())


def tid(vol):
    return "YHB-TME-%s-%03d" % (vol, SEQ[vol]["tmes"].nid())


# ================================================================ 卷 01 补全
V = "01"


# 占位：条目构造在 gen_gap01_part2.py 中导入
def main():
    from gen_gap01_part2 import build  # noqa
    build(globals())
    if ERRORS:
        print("!!! 校验失败 %d 项：" % len(ERRORS))
        for e in ERRORS:
            print("   ", e)
        print("未写盘。")
        return 1
    used = _ent_pool - ENT_START
    print("ENT 池用量: ENT-%d .. ENT-%04d (新分配 %d 个)" % (ENT_START, _ent_pool - 1, used))
    report = write_back()
    for vol in sorted(report):
        print(vol, json.dumps(report[vol], ensure_ascii=False))
    print("TOTAL new records:", sum(sum(v.values()) for v in report.values()))
    return 0


def load_item_originals():
    out = {}
    for v in VOLS:
        out.update(SEG[v])
    return out


def write_back():
    originals = load_item_originals()
    report = {}
    for vol, layers in NEW.items():
        report[vol] = {}
        for layer, new_recs in layers.items():
            path = os.path.join(BASE, "_layers", layer, "%s_%s.json" % (layer, vol))
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            is_dict = isinstance(data, dict)
            old_recs = data["records"] if is_dict else data
            if layer == "ents":
                aligned = []
                for r in new_recs:
                    seg = originals.get(r["item_id"]) or ""
                    idx = seg.find(r["text"])
                    aligned.append({
                        "ent_id": r.pop("_eid"), "item_id": r["item_id"],
                        "text": r["text"], "type": r["type"],
                        "normalized": r["normalized"],
                        "start": idx if idx >= 0 else None,
                        "end": idx + len(r["text"]) if idx >= 0 else None,
                        "confidence": r["confidence"],
                        "role_in_entry": r["role_in_entry"],
                        "faction": r["faction"], "exam_info": r["exam_info"],
                        "career_span": r["career_span"],
                    })
                new_recs = aligned
            else:
                for r in new_recs:
                    r.pop("_eid", None)
            merged = old_recs + new_recs
            with open(path, "w", encoding="utf-8") as f:
                if is_dict:
                    json.dump({"records": merged}, f, ensure_ascii=False, indent=2)
                else:
                    json.dump(merged, f, ensure_ascii=False, indent=2)
                f.write("\n")
            report[vol][layer] = len(new_recs)
    return report


if __name__ == "__main__":
    raise SystemExit(main())
