# -*- coding: utf-8 -*-
"""确认org_events是否真的重复"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
org_events = json.load(open(os.path.join(ROOT, "_layers", "org_events.json"), encoding="utf-8"))

# 正确的去重key: item_id + org_name + event_type
keys = []
for r in org_events:
    iid = r.get("item_id", "")
    org_name = r.get("org_name", "")
    event_type = r.get("event_type", "")
    keys.append((iid, org_name, event_type))

key_count = Counter(keys)
duplicates = {k: c for k, c in key_count.items() if c > 1}

print(f"org_events共{len(org_events)}条")
print(f"正确key(item_id+org_name+event_type)的重复: {len(duplicates)}个")

if duplicates:
    for k, c in duplicates.items():
        print(f"  {k}: {c}次")
else:
    print("  ✅ 实际无重复")

# 看看校验脚本为什么说有7个重复
print(f"\n校验脚本bug原因:")
print(f"  校验脚本检测的是 text/name/office_name/material 字段")
print(f"  但org_events的字段是 org_name，校验脚本没找到")
print(f"  导致name=''，所有记录key都是 (iid, '')")
print(f"  同一item_id多条就被误判为重复")
