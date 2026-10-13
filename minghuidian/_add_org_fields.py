# -*- coding: utf-8 -*-
"""给org_profiles层加字段，然后从原文提取填充"""
import json, os, re
from collections import defaultdict, Counter

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

# ===== 从原文提取部门信息 =====
def extract_org_info(org_name, title, original):
    """从原文提取某个部门的信息"""
    text = title + " " + original
    info = {
        "org_name": org_name,
        "rank": None,
        "parent_org": None,
        "staff": None,
        "history": None,
        "location": None,
    }

    # 找品级
    rank_match = re.search(r"(正[一二三四五六七八九]品|从[一二三四五六七八九]品)衙门", text)
    if rank_match:
        info["rank"] = rank_match.group(1)

    # 找上下级
    if "属中书省" in text or "隶中书省" in text:
        info["parent_org"] = "中书省"
    if "其属有" in text:
        child_match = re.search(r"其属有([^，。；]{2,20})", text)
        if child_match:
            info["staff"] = child_match.group(1)[:30]

    # 找中央/地方
    if "在京" in text and "部" in org_name:
        info["location"] = "中央"
    if "在外" in text:
        info["location"] = "地方"

    # 找沿革
    if "国初置" in text or "洪武" in text:
        hist_match = re.search(r"(国初置[^，。；]{5,30})", text)
        if hist_match:
            info["history"] = hist_match.group(1)[:50]

    return info

# ===== 批量提取 =====
org_profiles_new = []
org_items = defaultdict(list)

# 先找出每个部门出现在哪些条目
for iid, item in reg.items():
    text = item["title"] + " " + item["original"]
    for org in STANDARD_ORGS:
        if org in text:
            org_items[org].append((iid, item))

# 然后提取每个部门的信息
seq = 0
for org in STANDARD_ORGS:
    if org not in org_items:
        continue

    # 取第一条有信息的条目
    for iid, item in org_items[org][:5]:
        info = extract_org_info(org, item["title"], item["original"])
        # 如果提取到了信息，就用这条
        if info["rank"] or info["history"] or info["parent_org"]:
            seq += 1
            org_profiles_new.append({
                "org_id": f"ORGP-{seq:04d}",
                "item_id": iid,
                **info,
            })
            break
    else:
        # 没提取到特殊信息，就建个基础记录
        seq += 1
        org_profiles_new.append({
            "org_id": f"ORGP-{seq:04d}",
            "item_id": org_items[org][0][0],
            "org_name": org,
            "rank": None,
            "parent_org": None,
            "staff": None,
            "history": None,
            "location": None,
        })

print(f"【org_profiles层（加字段后）】{len(org_profiles_new)}条")
print(f"\n字段: {list(org_profiles_new[0].keys())}")

print(f"\n抽样:")
for o in org_profiles_new[:15]:
    print(f"  - {o['org_name']:12s} rank={o['rank'] or '?':8s} parent={o['parent_org'] or '?'}")

# 统计有品级的
with_rank = [o for o in org_profiles_new if o["rank"]]
print(f"\n有品级的部门: {len(with_rank)}条")
for o in with_rank:
    print(f"  - {o['org_name']:12s} {o['rank']}")

# 保存
with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(org_profiles_new, f, ensure_ascii=False, indent=1)

print(f"\n已保存: _layers/org_profiles.json")
