# -*- coding: utf-8 -*-
"""批量校准：规则类型 + 文书标记"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 读取现有 rules
rules_path = os.path.join(ROOT, "_layers", "rules.json")
rules = json.load(open(rules_path, encoding="utf-8"))

# 校准规则
fixed_type = 0
fixed_marker = 0

for r in rules:
    iid = r["item_id"]
    if iid not in reg:
        continue
    original = reg[iid]["original"]

    # 1. 类型校准
    if r["type"] == "义务":
        if re.search(r"不许|毋得|毋|勿|禁止|不许|不得|不准", original):
            r["type"] = "禁止"
            fixed_type += 1
        elif re.search(r"限.*日|限.*月|三年|五年|十年", original):
            r["type"] = "时限"
            fixed_type += 1

    # 2. 文书标记校准
    if r["source_marker"] == "凡":
        if "奏准" in original:
            r["source_marker"] = "奏准"
            fixed_marker += 1
        elif "议准" in original:
            r["source_marker"] = "议准"
            fixed_marker += 1
        elif "奏定" in original:
            r["source_marker"] = "奏定"
            fixed_marker += 1
        elif "议定" in original:
            r["source_marker"] = "议定"
            fixed_marker += 1
        elif re.match(r"^洪武.*令|^永乐.*令|^宣德.*令", original):
            r["source_marker"] = "令"
            fixed_marker += 1
        elif "诏" in original[:10]:
            r["source_marker"] = "诏"
            fixed_marker += 1
        elif "敕" in original[:10]:
            r["source_marker"] = "敕"
            fixed_marker += 1

print(f"类型校准: {fixed_type} 条")
print(f"标记校准: {fixed_marker} 条")

# 写回
with open(rules_path, "w", encoding="utf-8") as f:
    json.dump(rules, f, ensure_ascii=False, indent=1)
print("已写回 rules.json")

# 统计新分布
from collections import Counter
type_dist = Counter(r["type"] for r in rules)
marker_dist = Counter(r["source_marker"] for r in rules)
print("\n新类型分布:")
for t, c in type_dist.most_common():
    print(f"  {t}: {c}")
print("\n新标记分布:")
for m, c in marker_dist.most_common():
    print(f"  {m}: {c}")
