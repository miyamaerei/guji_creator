# -*- coding: utf-8 -*-
"""批量生成：卷108 卫所名录"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

def is_wei(title):
    if len(title) > 15:
        return False
    if any(p in title for p in ["。", "，", "；"]):
        return False
    if title.endswith(("卫", "所", "千户所")):
        return True
    return False

records = []
seq = 0

vol = 108
vol_items = sorted([iid for iid in reg if int(iid.split("-")[0]) == vol and iid not in covered])
current = None
current_entries = []

for iid in vol_items:
    title = reg[iid]["title"]
    if is_wei(title):
        if current:
            seq += 1
            records.append({
                "id": f"NAM-WEI-{vol:03d}-{seq:03d}",
                "item_id": f"{vol:03d}-{current[1]:03d}",
                "name": current[0],
                "nam_type": "卫所名录",
                "scope": "兵部",
                "entries": current_entries,
            })
        current = (title, int(iid.split("-")[1]))
        current_entries = []
    else:
        if current:
            current_entries.append({"seq": len(current_entries)+1, "office": title[:30], "count": ""})

if current:
    seq += 1
    records.append({
        "id": f"NAM-WEI-{vol:03d}-{seq:03d}",
        "item_id": f"{vol:03d}-{current[1]:03d}",
        "name": current[0],
        "nam_type": "卫所名录",
        "scope": "兵部",
        "entries": current_entries,
    })

print(f"卷108 生成 {len(records)} 条卫所名录")
with open(os.path.join(ROOT, "_src", "_nam_ai_108.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动生成：卷108 卫所名录"""\n\n')
    f.write("RECORDS = ")
    json.dump(records, f, ensure_ascii=False, indent=1)
print("已写入")
