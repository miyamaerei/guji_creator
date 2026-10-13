# -*- coding: utf-8 -*-
"""G2 缺口精确分析：每卷缺口数 + 未覆盖条目类型抽样"""
import json, os, re
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

# G2 卷14-41
vol_uncov = defaultdict(list)
for iid in reg:
    v = int(iid.split("-")[0])
    if 14 <= v <= 41 and iid not in covered:
        vol_uncov[v].append(iid)

print("G2 缺口按卷排序:")
print(f"{'卷':>4} {'缺口':>5}  未覆盖条目类型抽样")
total = 0
for v in sorted(vol_uncov, key=lambda x: -len(vol_uncov[x])):
    items = vol_uncov[v]
    total += len(items)
    # 抽样前3条判断类型
    samples = [reg[i]["title"][:25] for i in items[:3]]
    type_hint = ""
    if any(t.startswith("凡") for t in samples):
        type_hint = "规则(凡...)"
    elif any(re.search(r"(府|州|县|卫|所|司|局|仓|库)$", t) for t in samples):
        type_hint = "名录(衙门)"
    elif any(re.search(r"(名|名|名|几|几|几)", t) for t in samples):
        type_hint = "表格字段"
    else:
        type_hint = "其他"
    print(f"{v:>4} {len(items):>5}  {type_hint}  例: {samples[0]}")
print(f"\nG2 总缺口: {total} 条")
