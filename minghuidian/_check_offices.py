# -*- coding: utf-8 -*-
"""抽查官职数据"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
offices = json.load(open(os.path.join(ROOT, "_layers", "office_profiles.json"), encoding="utf-8"))

# 抽查的官职
check_list = [
    "吏部文选清吏司郎中",
    "知府",
    "卫指挥使",
    "司礼监掌印太监",
    "特进光禄大夫",
    "总兵官",
    "监察御史",
    "知县",
    "翰林修撰",
    "大理寺评事",
]

print("=" * 80)
print("官职数据抽查报告")
print("=" * 80)

for name in check_list:
    org = next((o for o in offices if o["office_name"] == name), None)
    if org:
        print(f"\n【{name}】")
        print(f"  品级: {org.get('rank', '?')}")
        print(f"  类型: {org.get('type', '?')}")
        print(f"  系统: {org.get('system', '?')}")
        print(f"  编制: {org.get('headcount', '?')}")
        print(f"  职责: {org.get('duties', '?')[:50]}...")
        print(f"  上级: {org.get('parent_org', '?')}")
        print(f"  下级: {org.get('child_offices', [])}")
        print(f"  位置: {org.get('location', '?')}")
        sal = org.get('salary')
        if sal:
            print(f"  俸禄: 月{sal.get('monthly_shi', '?')}石 / 岁{sal.get('yearly_shi', '?')}石")
        else:
            print(f"  俸禄: {org.get('salary_note', '无')}")
    else:
        print(f"\n【{name}】❌ 未找到！")

print(f"\n{'=' * 80}")
print(f"总官职数: {len(offices)}")
print(f"找到的: {sum(1 for n in check_list if any(o['office_name'] == n for o in offices))}/{len(check_list)}")
