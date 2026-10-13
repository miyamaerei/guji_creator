# -*- coding: utf-8 -*-
"""G2 户部剩余缺口分析"""
import json, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

vol_items = defaultdict(list)
for iid in reg:
    v = int(iid.split("-")[0])
    if 14 <= v <= 41:
        vol_items[v].append(iid)

print("G2 户部各卷缺口:")
print(f"{'卷':>4} {'总数':>5} {'已覆盖':>5} {'缺口':>5} {'覆盖率':>7}  内容类型")
total_uncov = 0
for v in sorted(vol_items):
    items = vol_items[v]
    cov = len([i for i in items if i in covered])
    unc = len(items) - cov
    total_uncov += unc
    pct = cov * 100 // len(items)
    first = reg[items[0]]["title"][:20]
    flag = "🔥" if unc > 100 else ("⚠️" if unc > 20 else "✅")
    print(f"{v:>4} {len(items):>5} {cov:>5} {unc:>5} {pct:>6}%  {flag} {first}")
print(f"\n总缺口: {total_uncov} 条")
