# -*- coding: utf-8 -*-
"""树结构密度 v3：加入laws + rituals两层"""
import json, os
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))
ents = json.load(open(os.path.join(ROOT, "_layers", "ents.json"), encoding="utf-8"))
cits = json.load(open(os.path.join(ROOT, "_layers", "cits.json"), encoding="utf-8"))
laws = json.load(open(os.path.join(ROOT, "_layers", "laws.json"), encoding="utf-8"))
rituals = json.load(open(os.path.join(ROOT, "_layers", "rituals.json"), encoding="utf-8"))

ents_real = [e for e in ents if not e.get("item_id", "").startswith("VIRT")]

def build_index(data):
    d = defaultdict(list)
    for r in data:
        d[r["item_id"]].append(r)
    return d

idx = {
    "rules": build_index(rules),
    "nams": build_index(nams),
    "ents": build_index(ents_real),
    "cits": build_index(cits),
    "laws": build_index(laws),
    "rituals": build_index(rituals),
}

GROUPS = [
    ("G0 宗人府", [1]),
    ("G1 吏部", list(range(2, 14))),
    ("G2 户部", list(range(14, 42))),
    ("G3 礼部", list(range(42, 106))),
    ("G4 兵部", list(range(106, 130))),
    ("G5 刑部", list(range(130, 144))),
    ("G6 工部", list(range(144, 164))),
    ("G7 诸文职", list(range(164, 179))),
    ("G8 诸武职", [179, 180]),
]

print("=" * 90)
print("树结构密度（7层：rules/nams/ents/cits/laws/rituals）")
print("=" * 90)

total_items = len(reg)
total_records = sum(len(v) for v in [rules, nams, ents_real, cits, laws, rituals])
print(f"\n【L0】全书: {total_items}条目, {total_records}条记录, 密度 {total_records/total_items:.2f}")

print(f"\n【L1】大卷组密度")
print(f"  {'卷组':12s} {'条目':>5s} {'规则':>5s} {'名录':>5s} {'实体':>5s} {'引用':>5s} {'法律':>5s} {'礼仪':>5s} {'密度':>6s}")
print("  " + "-" * 75)

for gname, vols in GROUPS:
    g_items = [iid for iid in reg if int(iid.split("-")[0]) in vols]
    counts = {}
    for layer, id_map in idx.items():
        counts[layer] = sum(len(id_map[iid]) for iid in g_items)
    total = sum(counts.values())
    d = total / len(g_items) if g_items else 0
    print(f"  {gname:12s} {len(g_items):5d} {counts['rules']:5d} {counts['nams']:5d} {counts['ents']:5d} {counts['cits']:5d} {counts['laws']:5d} {counts['rituals']:5d} {d:6.2f}")

# 条目级密度分布
print(f"\n【L3】条目级层数分布")
layer_count_dist = Counter()
for iid in reg:
    layers = sum(1 for id_map in idx.values() if id_map[iid])
    layer_count_dist[layers] += 1

for k in sorted(layer_count_dist.keys()):
    cnt = layer_count_dist[k]
    pct = cnt * 100 // total_items
    print(f"  {k}层: {cnt:5d} 条 ({pct:3d}%)")
