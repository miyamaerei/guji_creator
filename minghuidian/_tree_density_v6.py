# -*- coding: utf-8 -*-
"""树结构密度 v6：加入 inspect 风宪事务层（11层）"""
import json, os
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

layers = {}
for layer in ["rules", "nams", "ents", "cits", "laws", "rituals", "geo", "org_events", "offices", "materials", "inspect"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        layers[layer] = json.load(open(p, encoding="utf-8"))
    else:
        layers[layer] = []

layers["ents"] = [e for e in layers["ents"] if not e.get("item_id", "").startswith("VIRT")]

def build_index(data):
    d = defaultdict(list)
    for r in data:
        d[r["item_id"]].append(r)
    return d

idx = {layer: build_index(data) for layer, data in layers.items()}

GROUPS = [
    ("G0 宗人府", [1]),
    ("G1 吏部", list(range(2, 14))),
    ("G2 户部", list(range(14, 42))),
    ("G3 礼部", list(range(42, 106))),
    ("G4 兵部", list(range(106, 130))),
    ("G5 刑部", list(range(130, 146))),
    ("G6 工部", list(range(146, 164))),
    ("G7 诸文职", list(range(164, 179))),
    ("G8 诸武职", [179, 180]),
]

print("=" * 120)
print(f"树结构密度 v6（{len(layers)}层）")
print("=" * 120)

total_items = len(reg)
total_records = sum(len(data) for data in layers.values())
print(f"\n【L0】全书: {total_items}条目, {total_records}条记录, 密度 {total_records/total_items:.2f}")

print(f"\n【L1】大卷组密度")
header = f"  {'卷组':12s} {'条目':>5s}"
for layer in layers.keys():
    header += f" {layer[:5]:>6s}"
header += f" {'密度':>6s}"
print(header)
print("  " + "-" * 120)

for gname, vols in GROUPS:
    g_items = [iid for iid in reg if int(iid.split("-")[0]) in vols]
    counts = {layer: sum(len(idx[layer][iid]) for iid in g_items) for layer in layers}
    total = sum(counts.values())
    d = total / len(g_items) if g_items else 0

    line = f"  {gname:12s} {len(g_items):5d}"
    for layer in layers.keys():
        line += f" {counts[layer]:6d}"
    line += f" {d:6.2f}"
    print(line)

print(f"\n【L3】条目级层数分布")
layer_count_dist = Counter()
for iid in reg:
    layers_count = sum(1 for layer in layers if idx[layer][iid])
    layer_count_dist[layers_count] += 1

for k in sorted(layer_count_dist.keys()):
    cnt = layer_count_dist[k]
    pct = cnt * 100 // total_items
    print(f"  {k}层: {cnt:5d} 条 ({pct:3d}%)")
