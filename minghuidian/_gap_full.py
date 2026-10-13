# -*- coding: utf-8 -*-
"""全书剩余缺口完整分析"""
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

# 按大卷组统计
groups = {
    "G0 宗人府": (1, 1),
    "G1 吏部": (2, 13),
    "G2 户部": (14, 41),
    "G3 礼部": (42, 105),
    "G4 兵部": (106, 129),
    "G5 刑部": (130, 143),
    "G6 工部": (144, 163),
    "G7 诸文职": (164, 178),
    "G8 诸武职": (179, 180),
}

print("=" * 60)
print("全书剩余缺口分析")
print("=" * 60)

for gname, (lo, hi) in groups.items():
    total = 0
    covered_cnt = 0
    vol_gaps = defaultdict(int)
    for iid in reg:
        v = int(iid.split("-")[0])
        if lo <= v <= hi:
            total += 1
            if iid in covered:
                covered_cnt += 1
            else:
                vol_gaps[v] += 1
    pct = covered_cnt * 100 // total
    gap = total - covered_cnt
    print(f"\n【{gname}】 {covered_cnt}/{total} = {pct}%  (缺口 {gap})")
    # 列出缺口>5的卷
    for v, cnt in sorted(vol_gaps.items(), key=lambda x: -x[1])[:8]:
        if cnt > 5:
            first_title = reg[f"{v:03d}-001"]["title"][:25]
            print(f"  卷{v}: {cnt}条  例: {first_title}")
