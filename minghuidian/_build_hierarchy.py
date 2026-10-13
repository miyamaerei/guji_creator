# -*- coding: utf-8 -*-
"""识别排版层级，建立父子关系，加军事分类"""
import json, os, re
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ===== 标准部门列表 + 分类 =====
# 中央文职 / 地方 / 军事
ORG_CATEGORIES = {
    # 中央文职
    "宗人府": "中央文职",
    "吏部": "中央文职", "户部": "中央文职", "礼部": "中央文职",
    "兵部": "中央文职", "刑部": "中央文职", "工部": "中央文职",
    "都察院": "中央文职", "通政司": "中央文职", "大理寺": "中央文职",
    "太常寺": "中央文职", "光禄寺": "中央文职", "鸿胪寺": "中央文职",
    "太仆寺": "中央文职", "国子监": "中央文职", "翰林院": "中央文职",
    "钦天监": "中央文职", "太医院": "中央文职", "上林苑监": "中央文职",
    "中书省": "中央文职",
    # 军事
    "五军都督府": "军事", "中军都督府": "军事", "左军都督府": "军事",
    "右军都督府": "军事", "前军都督府": "军事", "后军都督府": "军事",
    # 六部下属司（默认中央文职）
    "文选司": "中央文职", "验封司": "中央文职", "稽勋司": "中央文职", "考功司": "中央文职",
    "仪制司": "中央文职", "祠祭司": "中央文职", "主客司": "中央文职", "精膳司": "中央文职",
    "武选司": "中央文职", "职方司": "中央文职", "车驾司": "中央文职", "武库司": "中央文职",
    "河南司": "中央文职", "山西司": "中央文职", "山东司": "中央文职", "湖广司": "中央文职",
    "陕西司": "中央文职", "广东司": "中央文职", "广西司": "中央文职", "四川司": "中央文职",
    "福建司": "中央文职", "浙江司": "中央文职", "江西司": "中央文职", "云南司": "中央文职",
    "贵州司": "中央文职",
}

# ===== 部门上下级关系（根据互联网知识+原文排版推断） =====
ORG_HIERARCHY = {
    # 六部下属司
    "文选司": "吏部", "验封司": "吏部", "稽勋司": "吏部", "考功司": "吏部",
    "仪制司": "礼部", "祠祭司": "礼部", "主客司": "礼部", "精膳司": "礼部",
    "武选司": "兵部", "职方司": "兵部", "车驾司": "兵部", "武库司": "兵部",
    "河南司": "户部", "山西司": "户部", "山东司": "户部", "湖广司": "户部",
    "陕西司": "户部", "广东司": "户部", "广西司": "户部", "四川司": "户部",
    "福建司": "户部", "浙江司": "户部", "江西司": "户部", "云南司": "户部", "贵州司": "户部",
    # 五军都督府
    "中军都督府": "五军都督府", "左军都督府": "五军都督府",
    "右军都督府": "五军都督府", "前军都督府": "五军都督府",
    "后军都督府": "五军都督府",
}

# ===== 生成新的org_profiles =====
org_profiles_new = []
seq = 0

for org_name, category in ORG_CATEGORIES.items():
    seq += 1

    # 找这个部门出现在哪些条目
    source_items = []
    for iid, item in reg.items():
        if org_name in item["title"] or org_name in item["original"]:
            source_items.append(iid)

    org_profiles_new.append({
        "org_id": f"ORGP-{seq:04d}",
        "org_name": org_name,
        "category": category,  # 中央文职/地方/军事
        "parent_org": ORG_HIERARCHY.get(org_name),  # 上级部门
        "child_orgs": [k for k, v in ORG_HIERARCHY.items() if v == org_name],  # 下级部门
        "source_count": len(source_items),
        "first_source": source_items[0] if source_items else None,
    })

print(f"【org_profiles层（识别排版层级后）】{len(org_profiles_new)}条")
print(f"\n字段: {list(org_profiles_new[0].keys())}")

print(f"\n所有部门:")
print(f"{'部门名':15s} {'分类':8s} {'上级':12s} {'下级数':>6s} {'出现次数':>8s}")
print("-" * 65)
for o in org_profiles_new:
    child_count = len(o["child_orgs"])
    print(f"{o['org_name']:15s} {o['category']:8s} {o['parent_org'] or '-':12s} {child_count:6d} {o['source_count']:8d}")

# 统计
from collections import Counter
cat_dist = Counter(o["category"] for o in org_profiles_new)
print(f"\n分类分布:")
for cat, cnt in cat_dist.most_common():
    print(f"  {cat}: {cnt}个")

with_parent = [o for o in org_profiles_new if o["parent_org"]]
print(f"\n有上级的部门: {len(with_parent)}/{len(org_profiles_new)}")

with_child = [o for o in org_profiles_new if o["child_orgs"]]
print(f"有下级的部门: {len(with_child)}/{len(org_profiles_new)}")

# 保存
with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(org_profiles_new, f, ensure_ascii=False, indent=1)

print(f"\n已保存: _layers/org_profiles.json")
