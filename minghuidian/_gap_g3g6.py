# -*- coding: utf-8 -*-
"""G3/G6 缺口精确分析"""
import json, os, re
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

def gap_stats(lo, hi, label):
    vol_uncov = defaultdict(list)
    for iid in reg:
        v = int(iid.split("-")[0])
        if lo <= v <= hi and iid not in covered:
            vol_uncov[v].append(iid)
    print(f"\n=== {label} 缺口按卷排序 ===")
    print(f"{'卷':>4} {'缺口':>5}  抽样")
    total = 0
    for v in sorted(vol_uncov, key=lambda x: -len(vol_uncov[x])):
        items = vol_uncov[v]
        total += len(items)
        samples = [reg[i]["title"][:30] for i in items[:2]]
        print(f"{v:>4} {len(items):>5}  {samples[0]}")
    print(f"总缺口: {total}")

gap_stats(42, 105, "G3 礼部")
gap_stats(144, 163, "G6 工部")
