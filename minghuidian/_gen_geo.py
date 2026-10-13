# -*- coding: utf-8 -*-
"""批量生成 NAM：从卷17-18切分结果里提取地理名录条目"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 已覆盖
covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

# 地理单元识别
def is_geo_unit(title):
    if len(title) > 15:
        return False
    if any(p in title for p in ["。", "，", "；", "界", "抵"]):
        return False
    if title.endswith(("承宣布政使司", "府", "州", "县", "卫", "所")):
        return True
    return False

records = []
seq = 0

for vol in [17, 18]:
    vol_items = sorted([iid for iid in reg if int(iid.split("-")[0]) == vol and iid not in covered])
    current = None
    current_entries = []

    for iid in vol_items:
        title = reg[iid]["title"]
        if is_geo_unit(title):
            if current:
                seq += 1
                records.append({
                    "id": f"NAM-GEO-{vol:03d}-{seq:03d}",
                    "item_id": f"{vol:03d}-{current[1]:03d}",
                    "name": current[0],
                    "nam_type": "官制名录",
                    "scope": "户部",
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
            "id": f"NAM-GEO-{vol:03d}-{seq:03d}",
            "item_id": f"{vol:03d}-{current[1]:03d}",
            "name": current[0],
            "nam_type": "官制名录",
            "scope": "户部",
            "entries": current_entries,
        })

print(f"生成 {len(records)} 条地理名录")
with open(os.path.join(ROOT, "_src", "_nam_ai_geo_17_18.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动生成：卷17-18 行政区划名录"""\n\n')
    f.write("RECORDS = ")
    json.dump(records, f, ensure_ascii=False, indent=1)
print("已写入")
