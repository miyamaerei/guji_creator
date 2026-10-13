# -*- coding: utf-8 -*-
"""密度分析：每卷条目数 + 各层覆盖数"""
import json, os
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 各层数据
layers = {}
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        layers[layer] = json.load(open(p, encoding="utf-8"))
    else:
        layers[layer] = []

# 按卷统计
vol_stats = defaultdict(lambda: {"total": 0, "rules": 0, "nams": 0, "ents": 0, "cits": 0})

for iid in reg:
    vol = int(iid.split("-")[0])
    vol_stats[vol]["total"] += 1

for r in layers["rules"]:
    vol = int(r["item_id"].split("-")[0])
    vol_stats[vol]["rules"] += 1

for n in layers["nams"]:
    vol = int(n["item_id"].split("-")[0])
    vol_stats[vol]["nams"] += 1

for e in layers["ents"]:
    iid = e.get("item_id", "")
    if iid.startswith("VIRT"):
        continue
    vol = int(iid.split("-")[0])
    vol_stats[vol]["ents"] += 1

# 按密度排序（每条平均有几层覆盖）
print("=" * 70)
print("卷密度分析（按每卷平均覆盖层数排序）")
print("=" * 70)
print(f"{'卷':>4s} {'总条目':>6s} {'规则':>5s} {'名录':>5s} {'实体':>5s} {'引用':>5s} {'平均层数':>8s}")
print("-" * 70)

vol_density = []
for vol in sorted(vol_stats.keys()):
    s = vol_stats[vol]
    avg = (s["rules"] + s["nams"] + s["ents"] + s["cits"]) / s["total"] if s["total"] else 0
    vol_density.append((vol, s["total"], s["rules"], s["nams"], s["ents"], s["cits"], avg))

# 按平均层数升序（最稀疏的在前）
vol_density.sort(key=lambda x: x[6])

print("\n【最稀疏的10卷】")
for vol, total, rules, nams, ents, cits, avg in vol_density[:10]:
    bar = "█" * int(avg * 5)
    print(f"卷{vol:3d} {total:6d} {rules:5d} {nams:5d} {ents:5d} {cits:5d} {avg:6.2f} {bar}")

print("\n【最密集的10卷】")
for vol, total, rules, nams, ents, cits, avg in vol_density[-10:]:
    bar = "█" * int(avg * 5)
    print(f"卷{vol:3d} {total:6d} {rules:5d} {nams:5d} {ents:5d} {cits:5d} {avg:6.2f} {bar}")

# 找问题卷：只有一层覆盖的
print("\n【只有1层覆盖的卷（疑似问题）】")
thin_vols = [(v, t, r, n, e, c, a) for v, t, r, n, e, c, a in vol_density if a < 1.5]
print(f"共 {len(thin_vols)} 卷密度低于1.5层")
for vol, total, rules, nams, ents, cits, avg in thin_vols[:15]:
    print(f"  卷{vol:3d}: {total}条, rules={rules}, nams={nams}, ents={ents}, cits={cits}")
