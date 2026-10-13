# -*- coding: utf-8 -*-
"""白名单过滤：只保留标准明代衙门/官职名"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

# ===== 标准明代中央衙门白名单 =====
STANDARD_ORGS = {
    # 宗人府
    "宗人府",
    # 六部
    "吏部", "户部", "礼部", "兵部", "刑部", "工部",
    # 六部下属司
    "文选司", "验封司", "稽勋司", "考功司",
    "十三清吏司", "仪制司", "祠祭司", "主客司", "精膳司",
    "武选司", "职方司", "车驾司", "武库司",
    "河南司", "山西司", "山东司", "湖广司", "陕西司", "广东司", "广西司", "四川司", "福建司", "浙江司", "江西司", "云南司", "贵州司",
    # 都察院
    "都察院",
    # 通政司
    "通政司",
    # 大理寺
    "大理寺",
    # 太常寺
    "太常寺",
    # 光禄寺
    "光禄寺",
    # 鸿胪寺
    "鸿胪寺",
    # 太仆寺
    "太仆寺",
    # 国子监
    "国子监",
    # 翰林院
    "翰林院",
    # 钦天监
    "钦天监",
    # 太医院
    "太医院",
    # 上林苑监
    "上林苑监",
    # 五军都督府
    "五军都督府", "中军都督府", "左军都督府", "右军都督府", "前军都督府", "后军都督府",
    # 其他
    "中书省", "军机处", "内务府",
}

# ===== 标准明代官职白名单 =====
STANDARD_OFFICES = {
    # 六部
    "尚书", "侍郎", "郎中", "员外郎", "主事",
    # 都察院
    "都御史", "左都御史", "右都御史", "副都御史", "佥都御史", "御史",
    # 大理寺
    "大理寺卿", "大理寺少卿", "寺丞",
    # 通政司
    "通政使", "通政副使",
    # 太常寺
    "太常寺卿", "太常寺少卿",
    # 光禄寺
    "光禄寺卿", "光禄寺少卿",
    # 鸿胪寺
    "鸿胪寺卿", "鸿胪寺少卿",
    # 太仆寺
    "太仆寺卿", "太仆寺少卿",
    # 国子监
    "祭酒", "司业",
    # 翰林院
    "学士", "侍读学士", "侍讲学士", "修撰", "编修", "检讨",
    # 地方
    "布政使", "按察使", "知府", "知州", "知县",
    # 宗人府
    "宗人令", "左宗正", "右宗正", "左宗人", "右宗人",
}

def is_standard_org(name):
    """判断是否是标准部门名"""
    name = name.strip()
    # 精确匹配
    if name in STANDARD_ORGS:
        return True
    # 包含匹配（如"吏部文选司"应该算）
    for std in STANDARD_ORGS:
        if std in name and len(name) <= 10:
            return True
    return False

def is_standard_office(name):
    """判断是否是标准官职名"""
    name = name.strip()
    if name in STANDARD_OFFICES:
        return True
    for std in STANDARD_OFFICES:
        if std in name and len(name) <= 10:
            return True
    return False

# ===== 过滤org_profiles =====
org_profiles = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

before = len(org_profiles)
clean_orgs = [o for o in org_profiles if is_standard_org(o.get("org_name", ""))]

# 去重
seen = set()
unique_orgs = []
for o in clean_orgs:
    key = o["org_name"]
    if key not in seen:
        seen.add(key)
        unique_orgs.append(o)

print(f"【org_profiles】")
print(f"  过滤前: {before}条")
print(f"  过滤后: {len(unique_orgs)}条")
print(f"\n  标准部门名列表:")
for o in sorted(unique_orgs, key=lambda x: x["org_name"]):
    rank = o.get("rank", "无品级")
    print(f"    - {o['org_name']:12s} ({rank})")

with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(unique_orgs, f, ensure_ascii=False, indent=1)

# ===== 过滤offices =====
offices = json.load(open(os.path.join(ROOT, "_layers", "offices.json"), encoding="utf-8"))

before = len(offices)
clean_offices = [o for o in offices if is_standard_office(o.get("office_name", ""))]

# 去重
seen = set()
unique_offices = []
for o in clean_offices:
    key = o["office_name"]
    if key not in seen:
        seen.add(key)
        unique_offices.append(o)

print(f"\n【offices】")
print(f"  过滤前: {before}条")
print(f"  过滤后: {len(unique_offices)}条")
print(f"\n  标准官职名列表:")
for o in sorted(unique_offices, key=lambda x: x["office_name"]):
    print(f"    - {o['office_name']}")

with open(os.path.join(ROOT, "_layers", "offices.json"), "w", encoding="utf-8") as f:
    json.dump(unique_offices, f, ensure_ascii=False, indent=1)

# ===== 过滤person_profiles =====
person_profiles = json.load(open(os.path.join(ROOT, "_layers", "person_profiles.json"), encoding="utf-8"))

before = len(person_profiles)
clean_persons = [p for p in person_profiles if is_standard_office(p.get("office_name", ""))]

print(f"\n【person_profiles】")
print(f"  过滤前: {before}条")
print(f"  过滤后: {len(clean_persons)}条")

with open(os.path.join(ROOT, "_layers", "person_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(clean_persons, f, ensure_ascii=False, indent=1)

print(f"\n✅ 白名单过滤完成")
