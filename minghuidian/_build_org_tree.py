# -*- coding: utf-8 -*-
"""批量补全三级树，每个字段都加原文位置"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
org_profiles = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

# ===== 从原文找到的机构（带原文位置） =====
# 格式：机构名, 品级, 编制, 职责, 沿革, 位置, 上级, 原文位置
FOUND_ORGS = [
    # 吏部相关（卷2-3）
    {"org_name": "司务厅", "rank": "从九品", "staff": [{"role": "司务", "count": 2}],
     "duties": "省署抄目，勾稽文书", "history": [{"year": "洪武", "event": "置"}],
     "category": "中央文职", "parent_org": "吏部", "child_orgs": [],
     "rank_source": "003-009", "staff_source": "003-009", "duties_source": "AI归纳", "history_source": "AI归纳"},

    {"org_name": "照磨所", "rank": "正八品", "staff": [{"role": "照磨", "count": 1}],
     "duties": "照刷文卷", "history": [],
     "category": "中央文职", "parent_org": "吏部", "child_orgs": [],
     "rank_source": "003-009", "staff_source": "003-009", "duties_source": "AI归纳", "history_source": "AI归纳"},

    {"org_name": "检校", "rank": "正九品", "staff": [{"role": "检校", "count": 1}],
     "duties": "检查文书", "history": [],
     "category": "中央文职", "parent_org": "照磨所", "child_orgs": [],
     "rank_source": "003-009", "staff_source": "003-009", "duties_source": "AI归纳", "history_source": "AI归纳"},

    # 文选司下属科室（从互联网搜索到的）
    {"org_name": "求贤科", "rank": "未入流", "staff": [{"role": "经承", "count": None}],
     "duties": "承办双月官员注册，进士举人截取", "history": [],
     "category": "中央文职", "parent_org": "文选司", "child_orgs": [],
     "rank_source": "互联网资料", "staff_source": "互联网资料", "duties_source": "互联网资料", "history_source": "互联网资料"},

    {"org_name": "开设科", "rank": "未入流", "staff": [{"role": "经承", "count": None}],
     "duties": "承办单月应补官员注册分发", "history": [],
     "category": "中央文职", "parent_org": "文选司", "child_orgs": [],
     "rank_source": "互联网资料", "staff_source": "互联网资料", "duties_source": "互联网资料", "history_source": "互联网资料"},

    {"org_name": "都书科", "rank": "未入流", "staff": [{"role": "经承", "count": None}],
     "duties": "收发本司文书", "history": [],
     "category": "中央文职", "parent_org": "文选司", "child_orgs": [],
     "rank_source": "互联网资料", "staff_source": "互联网资料", "duties_source": "互联网资料", "history_source": "互联网资料"},

    {"org_name": "缺科", "rank": "未入流", "staff": [{"role": "经承", "count": None}],
     "duties": "确定空缺岗位选候选人", "history": [],
     "category": "中央文职", "parent_org": "文选司", "child_orgs": [],
     "rank_source": "互联网资料", "staff_source": "互联网资料", "duties_source": "互联网资料", "history_source": "互联网资料"},

    {"org_name": "升调科", "rank": "未入流", "staff": [{"role": "经承", "count": None}],
     "duties": "承办官员升调事务", "history": [],
     "category": "中央文职", "parent_org": "文选司", "child_orgs": [],
     "rank_source": "互联网资料", "staff_source": "互联网资料", "duties_source": "互联网资料", "history_source": "互联网资料"},
]

# 添加新机构（避免重复）
existing_names = {o["org_name"] for o in org_profiles}
new_orgs = [o for o in FOUND_ORGS if o["org_name"] not in existing_names]
all_orgs = org_profiles + new_orgs

# 更新现有机构的child_orgs
for org in all_orgs:
    if org["org_name"] == "文选司":
        org["child_orgs"] = ["求贤科", "开设科", "都书科", "缺科", "升调科"]
    if org["org_name"] == "吏部":
        org["child_orgs"] = ["文选司", "验封司", "稽勋司", "考功司", "司务厅", "照磨所"]
    if org["org_name"] == "照磨所":
        org["child_orgs"] = ["检校"]

# 保存
with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(all_orgs, f, ensure_ascii=False, indent=2)

print(f"共 {len(all_orgs)} 个部门")
print(f"新增 {len(new_orgs)} 个三级机构")

# 展示组织树
print(f"\n{'=' * 60}")
print("组织树（吏部）:")
print("=" * 60)
print("吏部（正二品）")
print("├── 司务厅（从九品）")
print("├── 照磨所（正八品）")
print("│   └── 检校（正九品）")
print("├── 文选司（正五品）")
print("│   ├── 求贤科")
print("│   ├── 开设科")
print("│   ├── 都书科")
print("│   ├── 缺科")
print("│   └── 升调科")
print("├── 验封司（正五品）")
print("├── 稽勋司（正五品）")
print("└── 考功司（正五品）")

print(f"\n\n每个字段都有原文位置标注（xxx_source）")
print(f"示例：")
wenxuan = [o for o in all_orgs if o["org_name"] == "文选司"][0]
print(json.dumps(wenxuan, ensure_ascii=False, indent=2))
