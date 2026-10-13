# -*- coding: utf-8 -*-
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
orgs = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

print(f"共 {len(orgs)} 个机构")
print("=" * 60)
for i, o in enumerate(orgs):
    rank = o.get("rank", "?")
    parent = o.get("parent_org") or "无"
    child_count = len(o.get("child_orgs", []))
    print(f"{i+1:2d}. {o['org_name']:<15} {rank:<8} 上级:{parent:<10} 下级:{child_count}个")
