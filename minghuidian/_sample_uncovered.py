# -*- coding: utf-8 -*-
"""随机抽样检查未覆盖内容"""
import json, os, random
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

layers = {}
for layer in ["rules", "nams", "ents", "cits", "laws", "rituals", "geo", "org_events", "offices", "materials", "inspect", "dress", "foreign"]:
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

# 随机选10卷
all_vols = list(set(int(iid.split("-")[0]) for iid in reg.keys()))
random.seed(42)
sample_vols = sorted(random.sample(all_vols, 10))

print("=" * 80)
print(f"随机抽样 {len(sample_vols)} 卷，检查未覆盖内容")
print("=" * 80)

uncovered_total = 0
covered_total = 0

for vol in sample_vols:
    vol_items = [(iid, item) for iid, item in reg.items() if int(iid.split("-")[0]) == vol]

    uncovered = []
    covered = []

    for iid, item in vol_items:
        layers_count = sum(1 for layer in layers if idx[layer][iid])
        if layers_count == 0:
            uncovered.append((iid, item))
        else:
            covered.append((iid, item))

    uncovered_total += len(uncovered)
    covered_total += len(covered)

    print(f"\n【卷{vol}】{len(vol_items)}条 | 覆盖{len(covered)} | 未覆盖{len(uncovered)}")
    print(f"  {'条目':10s} {'标题':40s}")
    print("  " + "-" * 60)

    # 抽样显示未覆盖的前5条
    for iid, item in uncovered[:5]:
        print(f"  {iid:10s} {item['title'][:38]}")

    if len(uncovered) > 5:
        print(f"  ... 还有{len(uncovered)-5}条未覆盖")

print(f"\n{'='*80}")
print(f"抽样总结:")
print(f"  总条目: {covered_total + uncovered_total}")
print(f"  已覆盖: {covered_total} ({covered_total*100//(covered_total+uncovered_total)}%)")
print(f"  未覆盖: {uncovered_total} ({uncovered_total*100//(covered_total+uncovered_total)}%)")
