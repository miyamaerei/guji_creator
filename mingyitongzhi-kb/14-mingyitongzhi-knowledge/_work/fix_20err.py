# -*- coding: utf-8 -*-
"""一次性修复：① registry 补 05-002 永宁县；② evo 脏 item_id 改正。"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 1. registry 补 05-002
reg_path = os.path.join(ROOT, "_item_registry.json")
reg = json.load(open(reg_path, encoding="utf-8"))
if "05-002" not in reg:
    reg["05-002"] = {"title": "永宁县", "volume": 5, "region": "北直隶", "type": "county"}
    print("+registry 05-002 永宁县")

# 2. evo 脏 item_id
evo_path = os.path.join(ROOT, "_layers/evo/all.json")
evo = json.load(open(evo_path, encoding="utf-8"))
fix_map = {"EVO-002": "31-001", "EVO-003": "31-002"}
for r in evo["records"]:
    if r.get("item_id") in fix_map:
        old = r["item_id"]
        r["item_id"] = fix_map[old]
        print(f"~evo {old} -> {fix_map[old]} ({r.get('institution_name','')[:20]})")

# 写回
json.dump(reg, open(reg_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump(evo, open(evo_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("done.")
