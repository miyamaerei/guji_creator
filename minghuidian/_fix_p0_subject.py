# -*- coding: utf-8 -*-
"""P0修复：把 subject="各衙门" 的规则按卷组替换成精准部门"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))

# 卷组→部门映射
VOL_GROUP_DEPT = {
    range(2, 14): "吏部",
    range(14, 42): "户部",
    range(42, 106): "礼部",
    range(106, 130): "兵部",
    range(130, 144): "刑部",
    range(144, 164): "工部",
}

def get_dept(volume):
    for vols, dept in VOL_GROUP_DEPT.items():
        if volume in vols:
            return dept
    return None

fixed = 0
for r in rules:
    if r.get("subject") in ["各衙门", "各处", "有司"]:
        vol = int(r["item_id"].split("-")[0])
        dept = get_dept(vol)
        if dept:
            r["subject"] = dept
            fixed += 1

print(f"修复泛化主体: {fixed} 条")

# 统计修复后分布
from collections import Counter
subjects = Counter(r.get("subject", "未明") for r in rules)
print("\n修复后 subject TOP10:")
for s, c in subjects.most_common(10):
    print(f"  {s:15s}: {c:4d}")

# 写回
with open(os.path.join(ROOT, "_layers", "rules.json"), "w", encoding="utf-8") as f:
    json.dump(rules, f, ensure_ascii=False, indent=1)
print("\n已写回 rules.json")
