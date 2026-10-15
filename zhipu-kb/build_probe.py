# -*- coding: utf-8 -*-
"""治谱探针打包器：把 _src/_probe_pilot.py 的 AI 解读打包成 _layers/<layer>/<vol>.json。
- 从 _item_registry.json 注入 original（C3：AI 源数据不手抄原文）
- 枚举硬校验（C5：未注册值记 ERR）
- ID 段位分配：RULE-0501 = 卷01×500+1
- ent 主键：探针阶段用 ENT-P001 起（全局主键表后续批量建）
"""
import json, os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _kg_enums as enu
import _src._probe_pilot as pilot

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")
REG = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

errs = []
gaps = []

def check_enum(group, value, where):
    if value not in enu.ENUM_GROUPS[group]:
        errs.append(f"[ENUM-{group}] {where}: 未注册值 '{value}'")

# ---- ent ----
ent_records = []
ent_seq = {}
for i, (iid, text, etype, s, e, norm, conf) in enumerate(pilot.ENTS, 1):
    check_enum("ENTITY", etype, f"ent#{i}")
    if iid not in REG:
        errs.append(f"[ENT] {iid} 不在指纹库")
        continue
    ent_id = f"ENT-P{i:03d}"
    ent_records.append({
        "ent_id": ent_id, "item_id": iid, "text": text, "type": etype,
        "start": s, "end": e, "normalized": norm, "confidence": conf,
        "original": REG[iid]["original"], "source": "probe_ai",
    })

# ---- rule ----
rule_records = []
for i, (iid, rtype, modals, cond, subj, action, obj, purpose, punish) in enumerate(pilot.RULES, 1):
    check_enum("RULE", rtype, f"rule#{i}")
    for m in modals:
        if m not in enu.RULE_MODALS:
            errs.append(f"[RULE_MODALS] rule#{i}: 未注册模态 '{m}'")
    if iid not in REG:
        errs.append(f"[RULE] {iid} 不在指纹库"); continue
    vol = int(iid.split("-")[0])
    rid = f"RULE-{vol*500+i:04d}"
    rule_records.append({
        "rule_id": rid, "item_id": iid, "type": rtype, "modals": modals,
        "condition": cond, "subject": subj, "action": action, "object": obj,
        "purpose": purpose, "punishment": punish,
        "original": REG[iid]["original"], "confidence": 0.9,
    })

# ---- struct ----
struct_records = []
sidx = {"ACT":1,"FRD":1,"LGR":1,"TME":1}
for i, (iid, dim, dtype, target, content) in enumerate(pilot.STRUCTS, 1):
    if dim not in enu.STRUCT_DIMS:
        errs.append(f"[STRUCT_DIMS] struct#{i}: 未注册维度 '{dim}'")
    check_enum(dim, dtype, f"struct#{i}")
    if iid not in REG:
        errs.append(f"[STRUCT] {iid} 不在指纹库"); continue
    vol = int(iid.split("-")[0])
    sid = f"{dim}-{vol*500+sidx[dim]:04d}"
    sidx[dim] += 1
    rec = {"struct_id": sid, "item_id": iid, "dim": dim, "target": target,
           "content": content, "original": REG[iid]["original"], "confidence": 0.9}
    rec[f"{dim.lower()}_type"] = dtype
    struct_records.append(rec)

# ---- reg ----
reg_records = []
for i, (iid, name, rtype, content, evo, target) in enumerate(pilot.REGS, 1):
    check_enum("REG", rtype, f"reg#{i}")
    if iid not in REG:
        errs.append(f"[REG] {iid} 不在指纹库"); continue
    vol = int(iid.split("-")[0])
    rid = f"REG-{vol*500+i:04d}"
    reg_records.append({
        "reg_id": rid, "item_id": iid, "name": name, "type": rtype,
        "content": content, "evolution": evo, "target": target,
        "original": REG[iid]["original"], "confidence": 0.9,
    })

# ---- opn ----
opn_records = []
for i, (iid, topic, stance, arg, refs) in enumerate(pilot.OPNS, 1):
    check_enum("OPN", stance, f"opn#{i}")
    if iid not in REG:
        errs.append(f"[OPN] {iid} 不在指纹库"); continue
    vol = int(iid.split("-")[0])
    oid = f"OPN-{vol*500+i:04d}"
    opn_records.append({
        "opn_id": oid, "item_id": iid, "topic": topic, "stance": stance,
        "argument": arg, "evidence_refs": refs,
        "original": REG[iid]["original"], "confidence": 0.9,
    })

# ---- 写盘 ----
os.makedirs(LAYERS, exist_ok=True)
for layer, recs in [("ent",ent_records),("rule",rule_records),("struct",struct_records),
                    ("reg",reg_records),("opn",opn_records)]:
    d = os.path.join(LAYERS, layer); os.makedirs(d, exist_ok=True)
    out = os.path.join(d, "pilot.json")
    json.dump({"records": recs}, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"  {layer}: {len(recs)} 条 → {out}")

# ---- 探针覆盖：4 条探针每条至少有 1 层记录 ----
pilot_ids = {"04-001","05-030","09-001","11-001"}
covered = set()
for recs in [ent_records,rule_records,struct_records,reg_records,opn_records]:
    for r in recs: covered.add(r["item_id"])
for p in pilot_ids:
    if p not in covered:
        gaps.append(f"[GAP] 探针 {p} 没有任何层记录")

print(f"\n=== 探针打包完成 ===")
print(f"ERR: {len(errs)}")
for e in errs: print("  ✗", e)
print(f"GAP: {len(gaps)}")
for g in gaps: print("  !", g)
print(f"\n探针覆盖: {sorted(covered)}")
sys.exit(1 if errs else 0)
