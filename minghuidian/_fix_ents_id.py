# -*- coding: utf-8 -*-
"""修复 ents.json：给无 item_id 的记录补上"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
ents = json.load(open(os.path.join(ROOT, "_layers", "ents.json"), encoding="utf-8"))

fixed = 0
for i, e in enumerate(ents):
    if "item_id" not in e:
        e["item_id"] = f"VIRT-{i+1:03d}"
        fixed += 1

print(f"修复 {fixed} 条无 item_id 的记录")

with open(os.path.join(ROOT, "_layers", "ents.json"), "w", encoding="utf-8") as f:
    json.dump(ents, f, ensure_ascii=False, indent=1)
print("已写回")
