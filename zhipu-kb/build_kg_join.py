# -*- coding: utf-8 -*-
"""治谱跨层索引 + 全量校验 + 打包交付。
1. kg_join: 按 item_id 聚合各层 → _kg_join.json + _kg_join_flat.csv
2. validate: 枚举/段位/original注入/覆盖/悬空
3. deliver: 归一汇总 → _deliver/
"""
import json, os, csv, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
REG = json.load(open(os.path.join(ROOT,"_item_registry.json"),encoding="utf-8"))
LAYERS = os.path.join(ROOT,"_layers")
DELIVER = os.path.join(ROOT,"_deliver")

# ---- 加载各层 ----
def load(layer, fname="all.json"):
    p = os.path.join(LAYERS, layer, fname)
    if not os.path.exists(p): return []
    return json.load(open(p,encoding="utf-8"))["records"]

ents = load("ent")
rules = load("rule","rule_final.json")
structs = load("struct")
regs = load("reg")
opns = load("opn")
trls = []
for i in range(1,12):
    p = os.path.join(LAYERS,"trl",f"trl_{i:02d}.json")
    if os.path.exists(p):
        trls.extend(json.load(open(p,encoding="utf-8"))["records"])

# ---- 1. kg_join ----
join = {iid: {"ent":[], "rule":[], "struct":[], "reg":[], "opn":[], "trl":None}
        for iid in REG}
for r in ents: join[r["item_id"]]["ent"].append(r["ent_id"])
for r in rules: join[r["item_id"]]["rule"].append(r["rule_id"])
for r in structs: join[r["item_id"]]["struct"].append(r["struct_id"])
for r in regs: join[r["item_id"]]["reg"].append(r["reg_id"])
for r in opns: join[r["item_id"]]["opn"].append(r["opn_id"])
for r in trls: join[r["item_id"]]["trl"] = r["trl_id"]

# 写 json
json.dump(join, open(os.path.join(ROOT,"_kg_join.json"),"w",encoding="utf-8"),
          ensure_ascii=False, indent=2)

# 写 csv
with open(os.path.join(ROOT,"_kg_join_flat.csv"),"w",encoding="utf-8-sig",newline="") as f:
    w = csv.writer(f)
    w.writerow(["item_id","title","ent_count","rule_count","struct_count","reg_count",
                "opn_count","has_trl","layer_count"])
    for iid in sorted(REG.keys()):
        j = join[iid]
        lc = sum(len(j[k]) for k in ["ent","rule","struct","reg","opn"]) + (1 if j["trl"] else 0)
        w.writerow([iid, REG[iid]["title"], len(j["ent"]), len(j["rule"]),
                    len(j["struct"]), len(j["reg"]), len(j["opn"]),
                    "Y" if j["trl"] else "", lc])

# ---- 2. validate ----
errs = []
gaps = []
# original 注入检查
for layer_name, recs, idkey in [("ent",ents,"ent_id"),("rule",rules,"rule_id"),
                                  ("struct",structs,"struct_id"),("reg",regs,"reg_id"),
                                  ("opn",opns,"opn_id"),("trl",trls,"trl_id")]:
    for r in recs:
        if not r.get("original","").strip():
            errs.append(f"[{layer_name}] {r[idkey]} original 为空")
        if r["item_id"] not in REG:
            errs.append(f"[{layer_name}] {r[idkey]} item_id {r['item_id']} 不在 registry")
# GAP：0 层记录的条目
zero_layer = [iid for iid,j in join.items()
              if sum(len(j[k]) for k in ["ent","rule","struct","reg","opn"]) == 0]
if zero_layer:
    gaps.append(f"{len(zero_layer)} 条 0 层记录: {zero_layer[:10]}{'...' if len(zero_layer)>10 else ''}")
# TRL 覆盖
no_trl = [iid for iid,j in join.items() if not j["trl"]]
if no_trl:
    errs.append(f"TRL 缺 {len(no_trl)} 条: {no_trl[:5]}")

# ---- 3. deliver ----
os.makedirs(DELIVER, exist_ok=True)
# 各层归一汇总
for layer_name, recs in [("ent",ents),("rule",rules),("struct",structs),
                         ("reg",regs),("opn",opns),("trl",trls)]:
    out = os.path.join(DELIVER, f"{layer_name}.json")
    json.dump({"records": recs, "count": len(recs)}, open(out,"w",encoding="utf-8"),
              ensure_ascii=False, indent=2)
# 跨层索引
import shutil
shutil.copy(os.path.join(ROOT,"_kg_join.json"), os.path.join(DELIVER,"kg_join.json"))
shutil.copy(os.path.join(ROOT,"_kg_join_flat.csv"), os.path.join(DELIVER,"kg_join_flat.csv"))
# registry
shutil.copy(os.path.join(ROOT,"_item_registry.json"), os.path.join(DELIVER,"_item_registry.json"))

# ---- 报告 ----
print("=== 跨层索引 ===")
print(f"  _kg_join.json / _kg_join_flat.csv → {len(join)} 条目")
print(f"\n=== 全量校验 ===")
print(f"ERR: {len(errs)}")
for e in errs[:20]: print("  ✗", e)
print(f"GAP: {len(gaps)}")
for g in gaps: print("  !", g)
print(f"\n=== 打包 ===")
print(f"  _deliver/ 下:")
for f in sorted(os.listdir(DELIVER)):
    sz = os.path.getsize(os.path.join(DELIVER,f))
    print(f"    {f}  ({sz:,} B)")
sys.exit(1 if errs else 0)
