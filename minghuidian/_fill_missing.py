# -*- coding: utf-8 -*-
"""补全所有缺失字段"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ===== 完整的标准知识（补全所有缺失） =====
FULL_KNOWLEDGE = {
    "吏部": {
        "rank": "正二品",
        "history": "洪武元年始置，正三品，十三年革中书省后升正二品",
    },
    "户部": {
        "rank": "正二品",
        "history": "洪武元年始置，正三品，十三年革中书省后升正二品",
    },
    "兵部": {
        "rank": "正二品",
        "history": "洪武元年始置，正三品，十三年革中书省后升正二品",
    },
    "刑部": {
        "rank": "正二品",
    },
    "工部": {
        "rank": "正二品",
        "history": "洪武元年始置，正三品，十三年革中书省后升正二品",
    },
    "通政司": {
        "rank": "正三品",
        "staff": "通政使1人，左右通政各1人，左右参议各1人",
        "history": "洪武十年置，初为正三品衙门",
    },
    "太常寺": {
        "rank": "正三品",
        "history": "洪武三十年改太常司为太常寺",
    },
    "鸿胪寺": {
        "staff": "卿1人，左右少卿各1人，左右寺丞各1人",
    },
    "太仆寺": {
        "history": "洪武六年置",
    },
    "国子监": {
        "staff": "祭酒1人，司业1人，监丞1人，博士5人，助教15人",
    },
    "钦天监": {
        "staff": "监正1人，监副2人",
    },
    "上林苑监": {
        "history": "洪武十四年置",
    },
    "中军都督府": {
        "staff": "左/右都督各1人，都督同知，都督佥事",
    },
    "左军都督府": {
        "rank": "正一品",
        "staff": "左/右都督各1人，都督同知，都督佥事",
        "duties": "掌军旅之事，分领都司卫所",
        "history": "洪武十三年改大都督府为五军都督府",
    },
    "右军都督府": {
        "rank": "正一品",
        "staff": "左/右都督各1人，都督同知，都督佥事",
        "duties": "掌军旅之事，分领都司卫所",
        "history": "洪武十三年改大都督府为五军都督府",
    },
    "前军都督府": {
        "rank": "正一品",
        "staff": "左/右都督各1人，都督同知，都督佥事",
        "duties": "掌军旅之事，分领都司卫所",
        "history": "洪武十三年改大都督府为五军都督府",
    },
    "后军都督府": {
        "rank": "正一品",
        "staff": "左/右都督各1人，都督同知，都督佥事",
        "history": "洪武十三年改大都督府为五军都督府",
    },
}

# ===== 加载并补全 =====
org_profiles = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

fixed_count = 0
for org in org_profiles:
    name = org["org_name"]
    if name in FULL_KNOWLEDGE:
        for field, value in FULL_KNOWLEDGE[name].items():
            if not org.get(field):
                org[field] = value
                org[f"{field}_source"] = "AI补全（标准明代官制）"
                fixed_count += 1

print(f"共补全 {fixed_count} 个字段")

# ===== 最终验证 =====
print(f"\n{'=' * 70}")
print("最终验证报告")
print("=" * 70)

fields = ["rank", "staff", "duties", "history", "category"]
field_names = {
    "rank": "品级",
    "staff": "编制",
    "duties": "职责",
    "history": "沿革",
    "category": "位置",
}

print(f"\n{'部门':12s}", end="")
for f in fields:
    print(f" {field_names[f]:6s}", end="")
print()
print("-" * 50)

complete_count = 0
low_density = []
for org in org_profiles:
    name = org["org_name"]
    print(f"{name:12s}", end="")
    missing = []
    for f in fields:
        if org.get(f):
            print(f" ✅    ", end="")
        else:
            print(f" ❌    ", end="")
            missing.append(field_names[f])
    if not missing:
        complete_count += 1
    else:
        low_density.append((name, missing))
    print()

print(f"\n\n完整度统计:")
print(f"  全部字段完整: {complete_count}/{len(org_profiles)}")
print(f"  有缺失字段: {len(low_density)}/{len(org_profiles)}")

if low_density:
    print(f"\n密度不够的部门:")
    for name, missing in low_density:
        print(f"  - {name}: 缺 {', '.join(missing)}")

# 保存
with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(org_profiles, f, ensure_ascii=False, indent=1)

print(f"\n已保存最终版org_profiles.json")
