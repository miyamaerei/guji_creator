# -*- coding: utf-8 -*-
"""治谱层打包器（通用）：加载 _src/ 下所有 _volNN_ai.py + _probe_pilot.py，
枚举硬校验 + 从指纹库注入 original + ID 段位分配。
用法: python build_layers.py [--vol 01]
"""
import json, os, sys, importlib, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _kg_enums as enu

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")
REG = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 加载所有 _src/_*_ai.py 和 _probe_pilot.py
def load_src():
    ents, structs, regs, opns = [], [], [], []
    src_dir = os.path.join(ROOT, "_src")
    for f in sorted(glob.glob(os.path.join(src_dir, "_*_ai.py"))) + \
             [os.path.join(src_dir, "_probe_pilot.py")]:
        modname = os.path.splitext(os.path.basename(f))[0]
        mod = importlib.import_module(f"_src.{modname}")
        importlib.reload(mod)
        ents.extend(getattr(mod, "ENTS", []))
        structs.extend(getattr(mod, "STRUCTS", []))
        regs.extend(getattr(mod, "REGS", []))
        opns.extend(getattr(mod, "OPNS", []))
    return ents, structs, regs, opns

errs = []
ents, structs, regs, opns = load_src()

# ---- ent ----
ent_records = []
for i, (iid, text, etype, s, e, norm, conf) in enumerate(ents, 1):
    if etype not in enu.ENTITY_TYPES:
        errs.append(f"[ENT] {iid} '{text}': 未注册类型 '{etype}'")
        continue
    if iid not in REG:
        errs.append(f"[ENT] {iid} 不在指纹库"); continue
    ent_records.append({
        "ent_id": f"ENT-{i:04d}", "item_id": iid, "text": text, "type": etype,
        "start": s, "end": e, "normalized": norm, "confidence": conf,
        "original": REG[iid]["original"], "source": "ai",
    })

# ---- struct ----
struct_records = []
sidx = {"ACT":1,"FRD":1,"LGR":1,"TME":1}
for i, (iid, dim, dtype, target, content) in enumerate(structs, 1):
    if dim not in enu.STRUCT_DIMS:
        errs.append(f"[STRUCT] {iid}: 未注册维度 '{dim}'"); continue
    if dtype not in getattr(enu, f"{dim}_TYPES"):
        errs.append(f"[STRUCT] {iid} dim={dim}: 未注册类型 '{dtype}'"); continue
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
for i, (iid, name, rtype, content, evo, target) in enumerate(regs, 1):
    if rtype not in enu.REG_TYPES:
        errs.append(f"[REG] {iid} '{name}': 未注册类型 '{rtype}'"); continue
    if iid not in REG:
        errs.append(f"[REG] {iid} 不在指纹库"); continue
    vol = int(iid.split("-")[0])
    reg_records.append({
        "reg_id": f"REG-{vol*500+i:04d}", "item_id": iid, "name": name,
        "type": rtype, "content": content, "evolution": evo, "target": target,
        "original": REG[iid]["original"], "confidence": 0.9,
    })

# ---- opn ----
opn_records = []
for i, (iid, topic, stance, arg, refs) in enumerate(opns, 1):
    if stance not in enu.OPN_STANCES:
        errs.append(f"[OPN] {iid}: 未注册立场 '{stance}'"); continue
    if iid not in REG:
        errs.append(f"[OPN] {iid} 不在指纹库"); continue
    vol = int(iid.split("-")[0])
    opn_records.append({
        "opn_id": f"OPN-{vol*500+i:04d}", "item_id": iid, "topic": topic,
        "stance": stance, "argument": arg, "evidence_refs": refs,
        "original": REG[iid]["original"], "confidence": 0.9,
    })

# ---- 写盘 ----
for layer, recs in [("ent",ent_records),("struct",struct_records),
                    ("reg",reg_records),("opn",opn_records)]:
    d = os.path.join(LAYERS, layer); os.makedirs(d, exist_ok=True)
    out = os.path.join(d, "all.json")
    json.dump({"records": recs}, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"  {layer}: {len(recs)} 条")

print(f"\nERR: {len(errs)}")
for e in errs: print("  ✗", e)
sys.exit(1 if errs else 0)
