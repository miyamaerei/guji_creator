# -*- coding: utf-8 -*-
"""抽样看只有1层覆盖的条目"""
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

# 统计每层只有1层覆盖的条目
single_layer_items = []
for iid, item in reg.items():
    covered_layers = [layer for layer in layers if idx[layer][iid]]
    if len(covered_layers) == 1:
        single_layer_items.append((iid, item, covered_layers[0]))

print(f"全书只有1层覆盖的条目: {len(single_layer_items)}条 ({len(single_layer_items)*100//len(reg)}%)")
print()

# 按层统计
layer_dist = Counter(l for _, _, l in single_layer_items)
print("按层分布:")
for layer, cnt in layer_dist.most_common():
    print(f"  {layer:12s}: {cnt:5d}条")

print(f"\n{'='*80}")
print("抽样看这些薄覆盖条目是什么内容:")
print("=" * 80)

# 每层抽5条
for layer, _ in layer_dist.most_common():
    print(f"\n【{layer}层】抽样:")
    items = [(iid, item) for iid, item, l in single_layer_items if l == layer]
    sample = items[:5]
    for iid, item in sample:
        print(f"  {iid}: {item['title'][:50]}")
