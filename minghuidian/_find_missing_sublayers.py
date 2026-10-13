# -*- coding: utf-8 -*-
"""找FIN-TU土贡方物 + LAW-HUI会审审录的内容"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ===== 1. FIN-TU 土贡方物 =====
print("=" * 60)
print("【FIN-TU 土贡方物】搜索G2户部(卷14-41)")
print("=" * 60)

tu_keywords = ["土贡", "方物", "贡物", "贡品", "贡", "土宜", "任土", "供亿"]

tu_items = []
for iid, item in reg.items():
    vol = int(iid.split("-")[0])
    if not (14 <= vol <= 41):
        continue
    text = item["title"] + item["original"]
    for kw in tu_keywords:
        if kw in text:
            tu_items.append((iid, item, kw))
            break

print(f"找到{len(tu_items)}条候选:")
for iid, item, kw in tu_items[:15]:
    print(f"  {iid} [{kw}]: {item['title'][:40]}")

# ===== 2. LAW-HUI 会审审录 =====
print(f"\n{'='*60}")
print("【LAW-HUI 会审审录】搜索G5刑部(卷130-145)")
print("=" * 60)

hui_keywords = ["会审", "审录", "朝审", "大审", "秋审", "会问", "圆审", "三法司"]

hui_items = []
for iid, item in reg.items():
    vol = int(iid.split("-")[0])
    if not (130 <= vol <= 145):
        continue
    text = item["title"] + item["original"]
    for kw in hui_keywords:
        if kw in text:
            hui_items.append((iid, item, kw))
            break

print(f"找到{len(hui_items)}条候选:")
for iid, item, kw in hui_items[:15]:
    print(f"  {iid} [{kw}]: {item['title'][:40]}")
