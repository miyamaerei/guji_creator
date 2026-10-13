# -*- coding: utf-8 -*-
"""抽样看G3礼部内容，找可提取的层"""
import json, os
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

g3_items = [(iid, item) for iid, item in reg.items() if 42 <= int(iid.split("-")[0]) <= 105]
print(f"G3总条目: {len(g3_items)}")
print()

# 按卷分组统计
by_vol = defaultdict(list)
for iid, item in g3_items:
    vol = int(iid.split("-")[0])
    by_vol[vol].append((iid, item))

print("=== 各卷条目数和首条内容 ===")
for vol in sorted(by_vol.keys())[:20]:
    items = by_vol[vol]
    print(f"卷{vol:3d}: {len(items):3d}条 | {items[0][1]['title'][:40]}")

print(f"\n... 共{len(by_vol)}卷")

# 统计关键词
print("\n=== 关键词统计 ===")
keywords = [
    "乐章", "乐器", "曲", "歌",
    "祭祀", "祭", "郊", "庙", "社稷",
    "冠服", "车舆", "冕旒", "服色",
    "朝贡", "外国", "夷",
    "僧", "道",
    "皇后", "皇妃", "皇太子", "亲王",
    "谥", "册封",
]
for kw in keywords:
    cnt = sum(1 for iid, item in g3_items if kw in item["title"] + item["original"])
    print(f"  {kw:8s}: {cnt:4d}条")
