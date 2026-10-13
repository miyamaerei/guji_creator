# -*- coding: utf-8 -*-
"""改进提取方法：提取编制/职责/薪酬/沿革，每个属性加原文位置"""
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
    "前军都督府", "后军都督府",
]

# ===== 从原文提取每个部门的信息 =====
def extract_org_detail(org_name, items):
    """从相关条目中提取部门详细信息"""
    info = {
        "rank": None, "rank_source": None,
        "staff": None, "staff_source": None,
        "duties": None, "duties_source": None,
        "history": None, "history_source": None,
        "salary": None, "salary_source": None,
        "category": None, "category_source": None,
    }

    for iid, item in items:
        text = item["title"] + " " + item["original"]

        # 1. 品级
        if not info["rank"]:
            rank_match = re.search(r"(正[一二三四五六七八九]品|从[一二三四五六七八九]品)衙门", text)
            if rank_match:
                info["rank"] = rank_match.group(1)
                info["rank_source"] = iid

        # 2. 编制人数（从【正官】【属官】提取）
        if not info["staff"]:
            if "【正官】" in text:
                # 提取正官部分
                staff_match = re.search(r"【正官】([^【]{5,50})", text)
                if staff_match:
                    info["staff"] = staff_match.group(1)[:50]
                    info["staff_source"] = iid

        # 3. 职责（找"掌"字开头的描述）
        if not info["duties"]:
            duty_match = re.search(r"掌([^，。；]{5,40})", text)
            if duty_match:
                info["duties"] = duty_match.group(1)[:40]
                info["duties_source"] = iid

        # 4. 沿革（找"国初置"、"洪武"等）
        if not info["history"]:
            hist_match = re.search(r"(国初置[^，。；]{5,40})", text)
            if hist_match:
                info["history"] = hist_match.group(1)[:40]
                info["history_source"] = iid

        # 5. 位置（中央/地方/军事）
        if not info["category"]:
            if "在京" in text:
                info["category"] = "中央"
                info["category_source"] = iid
            elif "在外" in text:
                info["category"] = "地方"
                info["category_source"] = iid

    return info

# ===== 批量处理 =====
org_profiles_new = []

for org in STANDARD_ORGS:
    # 找这个部门出现在哪些条目
    items = []
    for iid, item in reg.items():
        if org in item["title"] or org in item["original"]:
            items.append((iid, item))

    if not items:
        continue

    detail = extract_org_detail(org, items)

    org_profiles_new.append({
        "org_name": org,
        "source_count": len(items),
        **detail,
    })

print(f"【改进后的org_profiles层】{len(org_profiles_new)}个部门")
print(f"\n字段: {list(org_profiles_new[0].keys())}")

print(f"\n所有部门详情:")
for o in org_profiles_new:
    print(f"\n--- {o['org_name']} ---")
    print(f"  品级: {o['rank'] or '?'} ({o['rank_source'] or '-'})")
    print(f"  编制: {o['staff'] or '?'} ({o['staff_source'] or '-'})")
    print(f"  职责: {o['duties'] or '?'} ({o['duties_source'] or '-'})")
    print(f"  沿革: {o['history'] or '?'} ({o['history_source'] or '-'})")
    print(f"  位置: {o['category'] or '?'} ({o['category_source'] or '-'})")

# 统计
print(f"\n\n【统计】")
with_rank = [o for o in org_profiles_new if o["rank"]]
print(f"有品级: {len(with_rank)}/{len(org_profiles_new)}")

with_staff = [o for o in org_profiles_new if o["staff"]]
print(f"有编制: {len(with_staff)}/{len(org_profiles_new)}")

with_duty = [o for o in org_profiles_new if o["duties"]]
print(f"有职责: {len(with_duty)}/{len(org_profiles_new)}")

with_history = [o for o in org_profiles_new if o["history"]]
print(f"有沿革: {len(with_history)}/{len(org_profiles_new)}")

with_category = [o for o in org_profiles_new if o["category"]]
print(f"有位置: {len(with_category)}/{len(org_profiles_new)}")

# 保存
with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(org_profiles_new, f, ensure_ascii=False, indent=1)

print(f"\n已保存: _layers/org_profiles.json")
