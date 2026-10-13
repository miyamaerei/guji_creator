# -*- coding: utf-8 -*-
"""提取4个视角层：部门主档/地理主档/人物主档/流程主档"""
import json, os, re
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ===== 1. ORG_PROFILE 部门主档层 =====
# 从原文提取部门信息
# 模式："XX衙门"、"正X品衙门"、"设尚书侍郎"

RANK_PATTERN = re.compile(r"(正[一二三四五六七八九]品|从[一二三四五六七八九]品)衙门")
ORG_NAME_PATTERN = re.compile(r"([一-龥]{2,10}(部|院|寺|监|司|府|卫|所|局|厂|库|仓))")

def extract_org_profile(title, original):
    """从条目提取部门主档信息"""
    text = title + " " + original
    profiles = []

    # 找品级
    rank_match = RANK_PATTERN.search(text)
    rank = rank_match.group(1) if rank_match else None

    # 找部门名
    org_matches = ORG_NAME_PATTERN.findall(text)
    org_names = set(name for name, suffix in org_matches)

    # 找上下级关系
    parent = None
    child_count = None

    if "属中书省" in text or "隶中书省" in text:
        parent = "中书省"
    if "其属有" in text:
        child_match = re.search(r"其属有([^，。；]+)", text)
        if child_match:
            child_count = child_match.group(1)[:30]

    # 找编制人数
    staff = None
    if "设" in text and ("尚书" in text or "侍郎" in text or "都御史" in text):
        staff = "有尚书侍郎等官"

    for name in org_names:
        if len(name) >= 2 and len(name) <= 8:
            profiles.append({
                "org_name": name,
                "rank": rank,
                "parent_org": parent,
                "child_orgs": child_count,
                "staff": staff,
            })

    return profiles

# ===== 2. GEO_PROFILE 地理主档层 =====
# 从geo层扩展，加上层级关系

# ===== 3. PERSON_PROFILE 人物主档层 =====
# 提取官职的出身要求
ENTRY_ROUTES = ["进士", "举人", "监生", "教官", "吏员", "特旨", "推举"]

def extract_person_profile(title, original):
    """从条目提取人物/官职要求"""
    text = title + " " + original
    profiles = []

    # 找出身要求
    entry_route = None
    for route in ENTRY_ROUTES:
        if route in text:
            entry_route = route
            break

    # 找官职名
    office_matches = re.findall(r"([一-龥]{2,8}(尚书|侍郎|郎中|员外郎|主事|御史|知府|知州|知县))", text)
    offices = set(name for name, suffix in office_matches)

    for off in offices:
        if len(off) <= 8:
            profiles.append({
                "office_name": off,
                "entry_route": entry_route,
            })

    return profiles

# ===== 4. PROCESS_PROFILE 流程主档层 =====
# 提取流程步骤
def extract_process_profile(title, original):
    """从条目提取流程信息"""
    text = title + " " + original

    # 找流程关键词
    process_keywords = ["先", "然后", "次", "复", "乃", "遂"]
    has_process = any(kw in text for kw in process_keywords)

    if has_process and len(text) > 50:
        return {
            "process_name": title[:30],
            "has_steps": True,
            "length": len(text),
        }
    return None

# ===== 批量提取 =====
org_profiles = []
geo_profiles = []
person_profiles = []
process_profiles = []

org_seq = geo_seq = person_seq = process_seq = 0

for iid, item in reg.items():
    title = item["title"]
    original = item["original"]

    # 1. 部门主档
    orgs = extract_org_profile(title, original)
    for o in orgs:
        org_seq += 1
        org_profiles.append({
            "org_id": f"ORGP-{org_seq:04d}",
            "item_id": iid,
            **o,
        })

    # 2. 人物主档
    persons = extract_person_profile(title, original)
    for p in persons:
        person_seq += 1
        person_profiles.append({
            "person_id": f"PERS-{person_seq:04d}",
            "item_id": iid,
            **p,
        })

    # 3. 流程主档
    proc = extract_process_profile(title, original)
    if proc:
        process_seq += 1
        process_profiles.append({
            "process_id": f"PROC-{process_seq:04d}",
            "item_id": iid,
            **proc,
        })

print("=" * 60)
print("4个视角层提取结果")
print("=" * 60)

print(f"\n【1. ORG_PROFILE 部门主档层】{len(org_profiles)} 条")
# 有品级的
with_rank = [o for o in org_profiles if o.get("rank")]
print(f"  有品级信息: {len(with_rank)} 条")
if with_rank:
    rank_dist = Counter(o["rank"] for o in with_rank)
    for r, c in rank_dist.most_common():
        print(f"    {r}: {c}条")

print(f"\n【2. PERSON_PROFILE 人物主档层】{len(person_profiles)} 条")
with_route = [p for p in person_profiles if p.get("entry_route")]
print(f"  有出身要求: {len(with_route)} 条")
if with_route:
    route_dist = Counter(p["entry_route"] for p in with_route)
    for r, c in route_dist.most_common():
        print(f"    {r}: {c}条")

print(f"\n【3. PROCESS_PROFILE 流程主档层】{len(process_profiles)} 条")

print(f"\n【4. GEO_PROFILE 地理主档层】待扩展（基于现有geo层）")

# 保存
for name, data in [("org_profiles", org_profiles), ("person_profiles", person_profiles), ("process_profiles", process_profiles)]:
    outpath = os.path.join(ROOT, "_layers", f"{name}.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"已保存: {outpath}")
