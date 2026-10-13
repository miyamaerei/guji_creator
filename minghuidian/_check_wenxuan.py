# -*- coding: utf-8 -*-
"""检查文选司的资料"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
org_profiles = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

print(f"共 {len(org_profiles)} 个部门")
print(f"\n部门列表:")
for o in org_profiles:
    print(f"  - {o['org_name']}")

# 找文选司
print(f"\n{'=' * 60}")
print("找文选司:")
print("=" * 60)

wenxuan = [o for o in org_profiles if "文选" in o["org_name"]]
if wenxuan:
    print(f"\n找到 {len(wenxuan)} 个:")
    for w in wenxuan:
        print(json.dumps(w, ensure_ascii=False, indent=2))
else:
    print(f"\n❌ 没有文选司的独立条目")
    print(f"现在文选司只作为吏部的child_orgs出现")

    # 看看吏部的child_orgs
    libu = [o for o in org_profiles if o["org_name"] == "吏部"][0]
    print(f"\n吏部的child_orgs: {libu['child_orgs']}")
    print(f"\n需要补全文选司、验封司、稽勋司、考功司这4个司的独立条目吗？")
