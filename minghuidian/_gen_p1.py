# -*- coding: utf-8 -*-
"""批量生成 NAM：补全卷18/35/40/41 剩余缺口"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

def is_unit(title, suffixes):
    if len(title) > 12:
        return False
    if any(p in title for p in ["。", "，", "；", "界", "抵"]):
        return False
    if title.endswith(suffixes):
        return True
    return False

records = []
seq = 0

# 卷18 行政区划（补全）
vol = 18
vol_items = sorted([iid for iid in reg if int(iid.split("-")[0]) == vol and iid not in covered])
current = None
current_entries = []
for iid in vol_items:
    title = reg[iid]["title"]
    if is_unit(title, ("府", "州", "县", "卫", "所")):
        if current:
            seq += 1
            records.append({"id": f"NAM-GEO-{vol:03d}-{seq:03d}", "item_id": f"{vol:03d}-{current[1]:03d}",
                           "name": current[0], "nam_type": "官制名录", "scope": "户部", "entries": current_entries})
        current = (title, int(iid.split("-")[1]))
        current_entries = []
    else:
        if current:
            current_entries.append({"seq": len(current_entries)+1, "office": title[:30], "count": ""})
if current:
    seq += 1
    records.append({"id": f"NAM-GEO-{vol:03d}-{seq:03d}", "item_id": f"{vol:03d}-{current[1]:03d}",
                   "name": current[0], "nam_type": "官制名录", "scope": "户部", "entries": current_entries})

# 卷35 盐课
vol = 35
vol_items = sorted([iid for iid in reg if int(iid.split("-")[0]) == vol and iid not in covered])
current = None
current_entries = []
for iid in vol_items:
    title = reg[iid]["title"]
    if is_unit(title, ("运司", "盐课司", "盐场", "盐局")):
        if current:
            seq += 1
            records.append({"id": f"NAM-SALT-{vol:03d}-{seq:03d}", "item_id": f"{vol:03d}-{current[1]:03d}",
                           "name": current[0], "nam_type": "仓场名录", "scope": "户部", "entries": current_entries})
        current = (title, int(iid.split("-")[1]))
        current_entries = []
    else:
        if current:
            current_entries.append({"seq": len(current_entries)+1, "office": title[:30], "count": ""})
if current:
    seq += 1
    records.append({"id": f"NAM-SALT-{vol:03d}-{seq:03d}", "item_id": f"{vol:03d}-{current[1]:03d}",
                   "name": current[0], "nam_type": "仓场名录", "scope": "户部", "entries": current_entries})

# 卷40/41 边卫南京
for vol in [40, 41]:
    vol_items = sorted([iid for iid in reg if int(iid.split("-")[0]) == vol and iid not in covered])
    current = None
    current_entries = []
    for iid in vol_items:
        title = reg[iid]["title"]
        if is_unit(title, ("卫", "所", "千户所")):
            if current:
                seq += 1
                records.append({"id": f"NAM-WEI-{vol:03d}-{seq:03d}", "item_id": f"{vol:03d}-{current[1]:03d}",
                               "name": current[0], "nam_type": "卫所名录", "scope": "户部", "entries": current_entries})
            current = (title, int(iid.split("-")[1]))
            current_entries = []
        else:
            if current:
                current_entries.append({"seq": len(current_entries)+1, "office": title[:30], "count": ""})
    if current:
        seq += 1
        records.append({"id": f"NAM-WEI-{vol:03d}-{seq:03d}", "item_id": f"{vol:03d}-{current[1]:03d}",
                       "name": current[0], "nam_type": "卫所名录", "scope": "户部", "entries": current_entries})

print(f"补全生成 {len(records)} 条")
with open(os.path.join(ROOT, "_src", "_nam_ai_p1_ext.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动生成：卷18/35/40/41 补全"""\n\n')
    f.write("RECORDS = ")
    json.dump(records, f, ensure_ascii=False, indent=1)
print("已写入")
