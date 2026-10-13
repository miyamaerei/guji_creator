# -*- coding: utf-8 -*-
"""统一后处理脚本：打包后自动运行所有修复"""
import os, sys, json, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

print("=" * 60)
print("统一后处理（打包后自动修复）")
print("=" * 60)

# ===== 1. 修复 rules：subject 泛化 + type 重新分类 =====
print("\n【1】修复 rules...")
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
rules_path = os.path.join(ROOT, "_layers", "rules.json")
rules = json.load(open(rules_path, encoding="utf-8"))

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

fixed_subject = 0
fixed_type = 0
for r in rules:
    iid = r["item_id"]
    vol = int(iid.split("-")[0])
    original = reg.get(iid, {}).get("original", "")

    # subject 修复
    if r.get("subject") in ["各衙门", "各处", "有司"]:
        dept = get_dept(vol)
        if dept:
            r["subject"] = dept
            fixed_subject += 1

    # type 重新分类
    if r["type"] == "义务" and original:
        if re.search(r"不许|毋得|毋|勿|不得|不准", original):
            r["type"] = "禁止"
            fixed_type += 1
        elif re.search(r"笞|杖|徒|流|充军|罢职", original):
            r["type"] = "处罚"
            fixed_type += 1

print(f"  subject 修复: {fixed_subject} 条")
print(f"  type 修复: {fixed_type} 条")

with open(rules_path, "w", encoding="utf-8") as f:
    json.dump(rules, f, ensure_ascii=False, indent=1)

# ===== 2. 修复 nams：乐章误判 + 其他细分 =====
print("\n【2】修复 nams...")
nams_path = os.path.join(ROOT, "_layers", "nams.json")
nams = json.load(open(nams_path, encoding="utf-8"))

MUSIC_KEYWORDS = ["乐章", "之曲", "迎神", "送神", "初献", "亚献", "终献"]
fixed_music = 0
fixed_other = 0

for n in nams:
    name = n["name"]
    # 乐章修复
    if n["nam_type"] == "官职题名" and any(k in name for k in MUSIC_KEYWORDS):
        n["nam_type"] = "乐章名录"
        fixed_music += 1
    # 其他细分
    elif n["nam_type"] == "其他":
        if any(k in name for k in ["府", "州", "县", "布政司"]):
            n["nam_type"] = "行政区划"
            fixed_other += 1
        elif any(k in name for k in ["仓", "场", "库"]):
            n["nam_type"] = "仓场名录"
            fixed_other += 1

print(f"  乐章修复: {fixed_music} 条")
print(f"  其他细分: {fixed_other} 条")

with open(nams_path, "w", encoding="utf-8") as f:
    json.dump(nams, f, ensure_ascii=False, indent=1)

# ===== 3. 修复 ents：父子关系 =====
print("\n【3】修复 ents 父子关系...")
ents_path = os.path.join(ROOT, "_layers", "ents.json")
ents = json.load(open(ents_path, encoding="utf-8"))

BUBU = ["吏部", "户部", "礼部", "兵部", "刑部", "工部"]
fixed_parent = 0

for e in ents:
    name = e["text"]
    if e.get("parent_id"):
        continue
    if name.endswith("司") and len(name) > 3:
        for bu in BUBU:
            if bu in name and bu != name:
                e["parent_id"] = bu
                e["node_type"] = "子部门"
                fixed_parent += 1
                break

print(f"  父子关系: {fixed_parent} 条")

with open(ents_path, "w", encoding="utf-8") as f:
    json.dump(ents, f, ensure_ascii=False, indent=1)

print("\n✓ 后处理完成")
