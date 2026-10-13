# -*- coding: utf-8 -*-
"""批量生成：卷18 "X府领县X" 行转成 NAM"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

records = []
seq = 0

# 卷18 所有未覆盖条目，按"X府领县X"识别
vol = 18
vol_items = sorted([iid for iid in reg if int(iid.split("-")[0]) == vol and iid not in covered])
for iid in vol_items:
    title = reg[iid]["title"]
    # 匹配 "X府领县X" 或 "X府" 短行
    if re.match(r"^.+府领县[一二三四五六七八九十]+$", title) or re.match(r"^.+府$", title):
        seq += 1
        records.append({
            "id": f"NAM-GEO-{vol:03d}-{seq:03d}",
            "item_id": iid,
            "name": title,
            "nam_type": "官制名录",
            "scope": "户部",
            "entries": [{"seq": 1, "office": "领县", "count": title.split("领县")[-1] if "领县" in title else ""}],
        })

print(f"卷18 生成 {len(records)} 条府级名录")
with open(os.path.join(ROOT, "_src", "_nam_ai_v18_ext.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动生成：卷18 府级名录"""\n\n')
    f.write("RECORDS = ")
    json.dump(records, f, ensure_ascii=False, indent=1)
print("已写入")
