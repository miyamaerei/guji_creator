# -*- coding: utf-8 -*-
"""补全文选司的下属科室"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
org_profiles = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

# ===== 文选司下属科室（从互联网搜索到的） =====
WENXUAN_KES = [
    {"org_name": "求贤科", "rank": "未入流", "staff": [{"role": "经承", "count": None}],
     "duties": "承办双月官员注册，进士举人截取，拣选举人，贡生就职就教", "history": [],
     "category": "中央文职", "parent_org": "文选司", "child_orgs": []},
    {"org_name": "开设科", "rank": "未入流", "staff": [{"role": "经承", "count": None}],
     "duties": "承办单月应补官员注册、验看、分发、引见", "history": [],
     "category": "中央文职", "parent_org": "文选司", "child_orgs": []},
    {"org_name": "都书科", "rank": "未入流", "staff": [{"role": "经承", "count": None}],
     "duties": "收发本司应办各项文书", "history": [],
     "category": "中央文职", "parent_org": "文选司", "child_orgs": []},
    {"org_name": "缺科", "rank": "未入流", "staff": [{"role": "经承", "count": None}],
     "duties": "确定每月空缺岗位并选出候选人", "history": [],
     "category": "中央文职", "parent_org": "文选司", "child_orgs": []},
    {"org_name": "升调科", "rank": "未入流", "staff": [{"role": "经承", "count": None}],
     "duties": "承办官员升调事务", "history": [],
     "category": "中央文职", "parent_org": "文选司", "child_orgs": []},
    # 吏部直属机构
    {"org_name": "司务厅", "rank": "从九品", "staff": [{"role": "司务", "count": 2}],
     "duties": "省署抄目，勾稽文书", "history": [],
     "category": "中央文职", "parent_org": "吏部", "child_orgs": []},
]

# 添加
all_orgs = org_profiles + WENXUAN_KES

# 更新文选司的child_orgs
for org in all_orgs:
    if org["org_name"] == "文选司":
        org["child_orgs"] = ["求贤科", "开设科", "都书科", "缺科", "升调科"]
    if org["org_name"] == "吏部":
        org["child_orgs"] = ["文选司", "验封司", "稽勋司", "考功司", "司务厅"]

# 保存
with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(all_orgs, f, ensure_ascii=False, indent=2)

# 展示文选司完整信息
print("=" * 60)
print("文选司完整资料:")
print("=" * 60)
wenxuan = [o for o in all_orgs if o["org_name"] == "文选司"][0]
print(json.dumps(wenxuan, ensure_ascii=False, indent=2))

print(f"\n\n文选司下属科室:")
for ke in WENXUAN_KES[:5]:
    print(f"  - {ke['org_name']}: {ke['duties'][:30]}...")

print(f"\n\n共 {len(all_orgs)} 个部门")
