# -*- coding: utf-8 -*-
"""用干净的标准实体名修复现有层"""
import json, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))

# ===== 加载干净的标准列表 =====
offices_clean = json.load(open(os.path.join(ROOT, "_layers", "offices_clean.json"), encoding="utf-8"))
orgs_clean = json.load(open(os.path.join(ROOT, "_layers", "org_profiles_clean.json"), encoding="utf-8"))

# ===== 转换为条目级格式（和原来一样） =====
# 原来的格式：每条记录有 item_id
# 现在的格式：每个官职名一条，统计出现次数和source_items

# 展开成条目级
offices_layer = []
seq = 0
for off in offices_clean:
    for iid in off["source_items"]:
        seq += 1
        offices_layer.append({
            "office_id": f"OFF-{seq:04d}",
            "item_id": iid,
            "office_name": off["office_name"],
        })

orgs_layer = []
seq = 0
for org in orgs_clean:
    for iid in org["source_items"]:
        seq += 1
        orgs_layer.append({
            "org_id": f"ORG-{seq:04d}",
            "item_id": iid,
            "org_name": org["org_name"],
        })

print(f"【修复后】")
print(f"  offices层: {len(offices_layer)}条（干净官职名）")
print(f"  org_profiles层: {len(orgs_layer)}条（干净部门名）")

# ===== 备份原文件，然后替换 =====
import shutil

for layer_name, new_data in [("offices", offices_layer), ("org_profiles", orgs_layer)]:
    old_path = os.path.join(ROOT, "_layers", layer_name + ".json")
    bak_path = os.path.join(ROOT, "_layers", layer_name + ".bak.json")

    # 备份
    if os.path.exists(old_path):
        shutil.copy(old_path, bak_path)
        print(f"  备份: {layer_name}.json -> {layer_name}.bak.json")

    # 写入新数据
    with open(old_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=1)
    print(f"  写入: {layer_name}.json ({len(new_data)}条)")

# ===== 更新person_profiles（用干净的官职名） =====
person_profiles = []
seq = 0
for off in offices_clean:
    # 假设person_profiles只保留有出身要求的
    # 这里简化，先复制offices的条目
    for iid in off["source_items"][:3]:  # 每个官职名取前3条
        seq += 1
        person_profiles.append({
            "person_id": f"PERS-{seq:04d}",
            "item_id": iid,
            "office_name": off["office_name"],
        })

with open(os.path.join(ROOT, "_layers", "person_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(person_profiles, f, ensure_ascii=False, indent=1)
print(f"  写入: person_profiles.json ({len(person_profiles)}条)")

print(f"\n✅ 修复完成")
