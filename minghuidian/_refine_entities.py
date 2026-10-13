# -*- coding: utf-8 -*-
"""精修：只保留干净的实体名"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

# ===== 干净的部门名模式 =====
# 规则：2-6个字，结尾是标准衙门后缀
ORG_SUFFIXES = [
    "部", "院", "寺", "监", "司", "府", "卫", "所", "局", "厂", "库", "仓",
    "清吏司", "都督府", "留守司", "宣慰司", "宣抚司",
]

# 干净的官职名模式
# 规则：2-8个字，结尾是标准官职后缀
OFFICE_SUFFIXES = [
    "尚书", "侍郎", "郎中", "员外郎", "主事", "都御史", "副都御史", "佥都御史",
    "御史", "大理寺卿", "少卿", "寺丞", "知府", "知州", "知县",
    "都督", "都指挥", "总兵", "副总兵", "参将",
    "宗人令", "宗正", "宗人",
]

def is_clean_org(name):
    """判断是否是干净的部门名"""
    if not name or len(name) < 2 or len(name) > 8:
        return False
    # 结尾必须是标准后缀
    for suffix in ORG_SUFFIXES:
        if name.endswith(suffix):
            # 不能包含动词/副词
            if any(kw in name for kw in ["设", "改", "置", "革", "为", "以", "于", "后", "又", "复"]):
                return False
            return True
    return False

def is_clean_office(name):
    """判断是否是干净的官职名"""
    if not name or len(name) < 2 or len(name) > 10:
        return False
    # 结尾必须是标准后缀
    for suffix in OFFICE_SUFFIXES:
        if name.endswith(suffix):
            # 不能包含动词/副词
            if any(kw in name for kw in ["设", "改", "置", "革", "为", "以", "于", "后", "又", "复", "衙门", "一员"]):
                return False
            return True
    return False

# ===== 精修org_profiles =====
org_profiles = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

before = len(org_profiles)
clean_orgs = []
for o in org_profiles:
    name = o.get("org_name", "")
    if is_clean_org(name):
        clean_orgs.append(o)

after = len(clean_orgs)
print(f"【org_profiles】")
print(f"  精修前: {before}条")
print(f"  精修后: {after}条")
print(f"  过滤掉: {before - after}条句子片段")

# 去重
seen = set()
unique_orgs = []
for o in clean_orgs:
    key = (o["org_name"], o.get("rank", ""))
    if key not in seen:
        seen.add(key)
        unique_orgs.append(o)

print(f"  去重后: {len(unique_orgs)}条")

# 按品级统计
rank_dist = Counter(o.get("rank", "无品级") for o in unique_orgs if o.get("rank"))
print(f"\n  有品级的部门:")
for r, c in rank_dist.most_common():
    samples = [o["org_name"] for o in unique_orgs if o.get("rank") == r][:5]
    print(f"    {r}: {c}条 - {', '.join(samples)}")

with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(unique_orgs, f, ensure_ascii=False, indent=1)

# ===== 精修offices =====
offices = json.load(open(os.path.join(ROOT, "_layers", "offices.json"), encoding="utf-8"))

before = len(offices)
clean_offices = []
for o in offices:
    name = o.get("office_name", "")
    if is_clean_office(name):
        clean_offices.append(o)

after = len(clean_offices)
print(f"\n【offices】")
print(f"  精修前: {before}条")
print(f"  精修后: {after}条")
print(f"  过滤掉: {before - after}条句子片段")

# 去重
seen = set()
unique_offices = []
for o in clean_offices:
    if o["office_name"] not in seen:
        seen.add(o["office_name"])
        unique_offices.append(o)

print(f"  去重后: {len(unique_offices)}条")

print(f"\n  干净官职名抽样:")
for o in unique_offices[:15]:
    print(f"    - {o['office_name']}")

with open(os.path.join(ROOT, "_layers", "offices.json"), "w", encoding="utf-8") as f:
    json.dump(unique_offices, f, ensure_ascii=False, indent=1)

# ===== 精修person_profiles =====
person_profiles = json.load(open(os.path.join(ROOT, "_layers", "person_profiles.json"), encoding="utf-8"))

before = len(person_profiles)
clean_persons = []
for p in person_profiles:
    name = p.get("office_name", "")
    if is_clean_office(name):
        clean_persons.append(p)

after = len(clean_persons)
print(f"\n【person_profiles】")
print(f"  精修前: {before}条")
print(f"  精修后: {after}条")
print(f"  过滤掉: {before - after}条句子片段")

with open(os.path.join(ROOT, "_layers", "person_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(clean_persons, f, ensure_ascii=False, indent=1)

print(f"\n✅ 精修完成")
