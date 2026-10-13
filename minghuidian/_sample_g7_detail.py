# -*- coding: utf-8 -*-
"""抽样看G7都察院内容，设计风宪事务层"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

g7_items = [(iid, item) for iid, item in reg.items() if 164 <= int(iid.split("-")[0]) <= 178]
print(f"G7总条目: {len(g7_items)}")
print()

# 看条目标题，找事务类型
titles = [item["title"] for iid, item in g7_items]
print("=== 条目标题抽样 ===")
for iid, item in g7_items[:30]:
    print(f"  {iid}: {item['title'][:40]}")

# 统计关键词
keywords = ["巡按", "刷卷", "清军", "审录", "考察", "考满", "选", "除授", "弹劾", "风宪", "御史"]
print("\n=== 关键词统计 ===")
for kw in keywords:
    cnt = sum(1 for iid, item in g7_items if kw in item["title"] + item["original"])
    print(f"  {kw}: {cnt}条")
