# -*- coding: utf-8 -*-
"""P1：细分NAM"其他"类"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))

# 抽样看"其他"类的内容
others = [n for n in nams if n["nam_type"] == "其他"]
print(f"'其他'类总数: {len(others)}")

# 按内容关键词分类
RULES = [
    ("行政区划", ["府", "州", "县", "布政司", "按察司"]),
    ("寺观名录", ["寺", "观", "庙", "祠", "坛"]),
    ("仓场名录", ["仓", "场", "库", "局", "厂"]),
    ("科举名录", ["进士", "举人", "状元", "榜眼", "探花", "会元"]),
    ("学校名录", ["学", "书院", "国子监", "社学"]),
]

fixed_counts = Counter()
for n in others:
    name = n["name"]
    for new_type, keywords in RULES:
        if any(k in name for k in keywords):
            n["nam_type"] = new_type
            fixed_counts[new_type] += 1
            break

print("\n细分结果:")
for t, c in fixed_counts.most_common():
    print(f"  {t}: {c} 条")

remaining = sum(1 for n in nams if n["nam_type"] == "其他")
print(f"\n剩余'其他': {remaining} 条")

with open(os.path.join(ROOT, "_layers", "nams.json"), "w", encoding="utf-8") as f:
    json.dump(nams, f, ensure_ascii=False, indent=1)
print("已写回")
