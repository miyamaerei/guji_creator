# -*- coding: utf-8 -*-
"""遍历全部原文，提取所有部门的品级/上下级信息"""
import json, os, re
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ===== 标准部门列表 =====
STANDARD_ORGS = [
    "宗人府", "吏部", "户部", "礼部", "兵部", "刑部", "工部",
    "都察院", "通政司", "大理寺", "太常寺", "光禄寺", "鸿胪寺",
    "太仆寺", "国子监", "翰林院", "钦天监", "太医院", "上林苑监",
    "五军都督府", "中军都督府", "左军都督府", "右军都督府",
    "前军都督府", "后军都督府", "中书省",
    "文选司", "验封司", "稽勋司", "考功司",
    "仪制司", "祠祭司", "主客司", "精膳司",
    "武选司", "职方司", "车驾司", "武库司",
    "河南司", "山西司", "山东司", "湖广司", "陕西司",
    "广东司", "广西司", "四川司", "福建司", "浙江司",
    "江西司", "云南司", "贵州司",
]

# ===== 遍历所有条目，收集每个部门的信息 =====
org_info = defaultdict(lambda: {
    "rank": None,
    "parent_org": None,
    "child_orgs": None,
    "location": None,
    "history": None,
    "source_items": [],
})

for iid, item in reg.items():
    text = item["title"] + " " + item["original"]

    for org in STANDARD_ORGS:
        if org in text:
            org_info[org]["source_items"].append(iid)

            # 找品级
            if not org_info[org]["rank"]:
                rank_match = re.search(r"(正[一二三四五六七八九]品|从[一二三四五六七八九]品)衙门", text)
                if rank_match:
                    org_info[org]["rank"] = rank_match.group(1)

            # 找上下级
            if not org_info[org]["parent_org"]:
                if "属中书省" in text or "隶中书省" in text:
                    org_info[org]["parent_org"] = "中书省"

            # 找中央/地方
            if not org_info[org]["location"]:
                if "在京" in text:
                    org_info[org]["location"] = "中央"
                elif "在外" in text:
                    org_info[org]["location"] = "地方"

# ===== 生成新的org_profiles =====
org_profiles_new = []
seq = 0

for org in STANDARD_ORGS:
    if org not in org_info:
        continue

    info = org_info[org]
    seq += 1
    org_profiles_new.append({
        "org_id": f"ORGP-{seq:04d}",
        "item_id": info["source_items"][0] if info["source_items"] else None,
        "org_name": org,
        "rank": info["rank"],
        "parent_org": info["parent_org"],
        "location": info["location"],
        "history": info["history"],
        "source_count": len(info["source_items"]),
    })

print(f"【org_profiles层（遍历全部原文后）】{len(org_profiles_new)}条")
print(f"\n字段: {list(org_profiles_new[0].keys())}")

print(f"\n所有部门:")
print(f"{'部门名':15s} {'品级':8s} {'上级':10s} {'位置':6s} {'出现次数':>8s}")
print("-" * 60)
for o in org_profiles_new:
    print(f"{o['org_name']:15s} {o['rank'] or '?':8s} {o['parent_org'] or '?':10s} {o['location'] or '?':6s} {o['source_count']:8d}")

# 统计
with_rank = [o for o in org_profiles_new if o["rank"]]
print(f"\n有品级的部门: {len(with_rank)}/{len(org_profiles_new)}")

with_parent = [o for o in org_profiles_new if o["parent_org"]]
print(f"有上级的部门: {len(with_parent)}/{len(org_profiles_new)}")

with_location = [o for o in org_profiles_new if o["location"]]
print(f"有位置的部门: {len(with_location)}/{len(org_profiles_new)}")

# 保存
with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(org_profiles_new, f, ensure_ascii=False, indent=1)

print(f"\n已保存: _layers/org_profiles.json")
