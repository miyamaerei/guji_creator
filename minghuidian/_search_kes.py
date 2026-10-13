# -*- coding: utf-8 -*-
"""从原文搜索科室记载"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# 加载item_registry
registry = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 搜索关键词：科、司务厅、照磨所等
keywords = ["科", "司务厅", "照磨所", "检校", "经历司"]

print("=" * 60)
print("搜索原文中的科室记载:")
print("=" * 60)

# 搜索卷1-13（吏部相关）
found = []
for item_id, item in registry.items():
    vol = int(item_id.split("-")[0])
    if vol > 13:
        continue

    original = item.get("original", "")
    for kw in keywords:
        if kw in original:
            # 提取上下文
            idx = original.find(kw)
            context = original[max(0, idx-10):idx+20]
            found.append((item_id, kw, context))
            break

print(f"\n找到 {len(found)} 条相关条目:")
for item_id, kw, context in found[:20]:
    print(f"  {item_id}: [{kw}] ...{context}...")
