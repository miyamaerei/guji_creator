# -*- coding: utf-8 -*-
"""更新树结构密度：加入laws层"""
import json, os
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))
ents = json.load(open(os.path.join(ROOT, "_layers", "ents.json"), encoding="utf-8"))
cits = json.load(open(os.path.join(ROOT, "_layers", "cits.json"), encoding="utf-8"))
laws = json.load(open(os.path.join(ROOT, "_layers", "laws.json"), encoding="utf-8"))

ents_real = [e for e in ents if not e.get("item_id", "").startswith("VIRT")]

def build_index(data):
    d = defaultdict(list)
    for r in data:
        d[r["item_id"]].append(r)
    return d

rules_idx = build_index(rules)
nams_idx = build_index(nams)
ents_idx = build_index(ents_real)
cits_idx = build_index(cits)
laws_idx = build_index(laws)

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

print("=" * 80)
print("树结构密度（含法律条文层 LAW）")
print("=" * 80)

total_items = len(reg)
total_records = len(rules) + len(nams) + len(ents_real) + len(cits) + len(laws)
print(f"\n【L0】全书: {total_items}条目, {total_records}条记录, 密度 {total_records/total_items:.2f}")

print(f"\n【L1】大卷组密度（含laws层）")
print(f"  {'卷组':12s} {'条目':>5s} {'规则':>5s} {'名录':>5s} {'实体':>5s} {'引用':>5s} {'法律':>5s} {'密度':>6s}")
print("  " + "-" * 65)

for gname, vols in GROUPS:
    g_items = [iid for iid in reg if int(iid.split("-")[0]) in vols]
    r = sum(len(rules_idx[iid]) for iid in g_items)
    n = sum(len(nams_idx[iid]) for iid in g_items)
    e = sum(len(ents_idx[iid]) for iid in g_items)
    c = sum(len(cits_idx[iid]) for iid in g_items)
    l = sum(len(laws_idx[iid]) for iid in g_items)
    total = r + n + e + c + l
    d = total / len(g_items) if g_items else 0
    print(f"  {gname:12s} {len(g_items):5d} {r:5d} {n:5d} {e:5d} {c:5d} {l:5d} {d:6.2f}")

# 条目级密度分布
print(f"\n【L3】条目级层数分布（含laws）")
layer_count_dist = Counter()
for iid in reg:
    layers = 0
    if rules_idx[iid]: layers += 1
    if nams_idx[iid]: layers += 1
    if ents_idx[iid]: layers += 1
    if cits_idx[iid]: layers += 1
    if laws_idx[iid]: layers += 1
    layer_count_dist[layers] += 1

for k in sorted(layer_count_dist.keys()):
    cnt = layer_count_dist[k]
    pct = cnt * 100 // total_items
    print(f"  {k}层: {cnt:5d} 条 ({pct:3d}%)")
