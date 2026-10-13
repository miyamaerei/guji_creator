# -*- coding: utf-8 -*-
"""查看org_events重复情况"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
org_events = json.load(open(os.path.join(ROOT, "_layers", "org_events.json"), encoding="utf-8"))

print(f"org_events共{len(org_events)}条")
print()

# 看第一条结构
print("第一条结构:")
print(json.dumps(org_events[0], ensure_ascii=False, indent=2))
print()

# 找重复
keys = []
for r in org_events:
    iid = r.get("item_id", "")
    # 所有可能的名称字段
    name = r.get("org_name", "") or r.get("name", "") or r.get("text", "")
    keys.append((iid, name))

key_count = Counter(keys)
duplicates = {k: c for k, c in key_count.items() if c > 1}

print(f"重复的(item_id + name)组合:")
for (iid, name), cnt in duplicates.items():
    print(f"  {iid} / {name}: {cnt}次")
