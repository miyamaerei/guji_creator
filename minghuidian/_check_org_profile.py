# -*- coding: utf-8 -*-
"""看看现在的org_profiles层到底有什么"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
org_profiles = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

print(f"【org_profiles层现状】{len(org_profiles)}条")
print(f"\n字段: {list(org_profiles[0].keys())}")
print(f"\n抽样:")
for o in org_profiles[:10]:
    print(f"  - {o}")

print(f"\n\n问题：")
print(f"  ✅ 有部门名（org_name）")
print(f"  ❌ 没有品级（rank）")
print(f"  ❌ 没有上下级关系（parent_org）")
print(f"  ❌ 没有编制人数（staff_count）")
print(f"  ❌ 没有沿革（history）")
print(f"  ❌ 没有薪酬（salary）")
print(f"  ❌ 没有职责（duties）")
print(f"  ❌ 没有中央/地方（location）")
