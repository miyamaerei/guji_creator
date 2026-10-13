# -*- coding: utf-8 -*-
"""看G5刑部和G6工部的内容特征，找实体提取线索"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))

# G5 刑部（卷130-143）
print("=== G5 刑部 rules subject 分布 ===")
xingbu_subjects = Counter()
for r in rules:
    vol = int(r["item_id"].split("-")[0])
    if 130 <= vol <= 143:
        xingbu_subjects[r.get("subject", "未明")] += 1

for s, c in xingbu_subjects.most_common(15):
    print(f"  {s:20s}: {c}")

# G6 工部（卷144-163）
print("\n=== G6 工部 rules subject 分布 ===")
gongbu_subjects = Counter()
for r in rules:
    vol = int(r["item_id"].split("-")[0])
    if 144 <= vol <= 163:
        gongbu_subjects[r.get("subject", "未明")] += 1

for s, c in gongbu_subjects.most_common(15):
    print(f"  {s:20s}: {c}")

# 抽样看G5原文里有哪些机构名
print("\n=== G5 原文抽样（找机构名）===")
org_keywords = ["刑部", "都察院", "大理寺", "通政司", "按察司", "布政司", "府", "州", "县", "卫", "所"]
g5_items = [(iid, item) for iid, item in reg.items() if 130 <= int(iid.split("-")[0]) <= 143]
print(f"G5总条目: {len(g5_items)}")

# 统计原文里出现的机构名
org_count = Counter()
for iid, item in g5_items[:100]:
    text = item["original"]
    for kw in org_keywords:
        if kw in text:
            org_count[kw] += 1

print("G5原文中机构关键词出现频率（前100条）:")
for kw, c in org_count.most_common():
    print(f"  {kw}: {c}")
