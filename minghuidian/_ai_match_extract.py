# -*- coding: utf-8 -*-
"""AI判断版：从原文匹配标准官职名列表"""
import json, os
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ===== 标准明代官职名列表（AI整理） =====
STANDARD_OFFICES = [
    # ===== 六部正官 =====
    "尚书", "左侍郎", "右侍郎", "侍郎",
    # ===== 六部司官 =====
    "郎中", "员外郎", "主事",
    # ===== 都察院 =====
    "左都御史", "右都御史", "都御史",
    "左副都御史", "右副都御史", "副都御史",
    "左佥都御史", "右佥都御史", "佥都御史",
    "监察御史", "御史",
    # ===== 大理寺 =====
    "大理寺卿", "大理寺少卿", "寺丞",
    # ===== 通政司 =====
    "通政使", "通政副使",
    # ===== 太常寺 =====
    "太常寺卿", "太常寺少卿",
    # ===== 光禄寺 =====
    "光禄寺卿", "光禄寺少卿",
    # ===== 鸿胪寺 =====
    "鸿胪寺卿", "鸿胪寺少卿",
    # ===== 太仆寺 =====
    "太仆寺卿", "太仆寺少卿",
    # ===== 国子监 =====
    "祭酒", "司业",
    # ===== 翰林院 =====
    "学士", "侍读学士", "侍讲学士",
    "侍读", "侍讲", "修撰", "编修", "检讨",
    # ===== 内阁大学士 =====
    "华盖殿大学士", "谨身殿大学士", "武英殿大学士",
    "文华殿大学士", "文渊阁大学士", "东阁大学士",
    # ===== 宗人府 =====
    "宗人令", "左宗正", "右宗正", "左宗人", "右宗人",
    # ===== 地方官 =====
    "布政使", "按察使", "知府", "知州", "知县",
    "同知", "通判", "推官",
    # ===== 军事 =====
    "五军都督", "都督", "都指挥",
    "总兵官", "副总兵", "参将",
    # ===== 其他 =====
    "行人", "尚宝司丞", "六科给事中",
]

# ===== 标准部门名列表 =====
STANDARD_ORGS = [
    # ===== 中央衙门 =====
    "宗人府",
    "吏部", "户部", "礼部", "兵部", "刑部", "工部",
    "都察院", "通政司", "大理寺",
    "太常寺", "光禄寺", "鸿胪寺", "太仆寺",
    "国子监", "翰林院", "钦天监", "太医院", "上林苑监",
    "五军都督府", "中军都督府", "左军都督府", "右军都督府",
    "前军都督府", "后军都督府",
    "中书省", "内阁",
    # ===== 六部下属司 =====
    "文选司", "验封司", "稽勋司", "考功司",
    "仪制司", "祠祭司", "主客司", "精膳司",
    "武选司", "职方司", "车驾司", "武库司",
    "河南司", "山西司", "山东司", "湖广司", "陕西司",
    "广东司", "广西司", "四川司", "福建司", "浙江司",
    "江西司", "云南司", "贵州司",
    # ===== 其他 =====
    "行人司", "尚宝司", "六科", "十三道",
]

# ===== 从原文匹配提取 =====
def match_in_text(text, candidates):
    """在文本中匹配候选词"""
    found = []
    for c in candidates:
        if c in text:
            found.append(c)
    return found

# ===== 批量处理 =====
office_counter = Counter()
office_items = defaultdict(list)
org_counter = Counter()
org_items = defaultdict(list)

for iid, item in reg.items():
    text = item["title"] + " " + item["original"]

    # 匹配官职名
    offices = match_in_text(text, STANDARD_OFFICES)
    for off in offices:
        office_counter[off] += 1
        office_items[off].append(iid)

    # 匹配部门名
    orgs = match_in_text(text, STANDARD_ORGS)
    for org in orgs:
        org_counter[org] += 1
        org_items[org].append(iid)

print("=" * 70)
print("AI匹配提取结果（标准列表）")
print("=" * 70)

print(f"\n【标准官职名】共 {len(office_counter)} 个出现")
print(f"{'官职名':20s} {'出现次数':>8s} {'涉及条目':>8s}")
print("-" * 50)
for off, cnt in office_counter.most_common():
    print(f"{off:20s} {cnt:8d} {len(office_items[off]):8d}")

print(f"\n【标准部门名】共 {len(org_counter)} 个出现")
print(f"{'部门名':20s} {'出现次数':>8s} {'涉及条目':>8s}")
print("-" * 50)
for org, cnt in org_counter.most_common():
    print(f"{org:20s} {cnt:8d} {len(org_items[org]):8d}")

# 保存
offices_data = []
for off, cnt in office_counter.most_common():
    offices_data.append({
        "office_name": off,
        "count": cnt,
        "source_items": office_items[off],
    })

with open(os.path.join(ROOT, "_layers", "offices_clean.json"), "w", encoding="utf-8") as f:
    json.dump(offices_data, f, ensure_ascii=False, indent=1)

orgs_data = []
for org, cnt in org_counter.most_common():
    orgs_data.append({
        "org_name": org,
        "count": cnt,
        "source_items": org_items[org],
    })

with open(os.path.join(ROOT, "_layers", "org_profiles_clean.json"), "w", encoding="utf-8") as f:
    json.dump(orgs_data, f, ensure_ascii=False, indent=1)

print(f"\n已保存:")
print(f"  _layers/offices_clean.json ({len(offices_data)}个官职名)")
print(f"  _layers/org_profiles_clean.json ({len(orgs_data)}个部门名)")
