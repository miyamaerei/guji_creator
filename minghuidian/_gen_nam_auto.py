# -*- coding: utf-8 -*-
"""批量生成 NAM：从切分结果自动识别衙门名录条目"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 已覆盖的 item_id
covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

# 卷6/7 未覆盖的条目，按连续短行分组
records = []
seq = 0
for vol in [6, 7]:
    vol_items = sorted([iid for iid in reg if int(iid.split("-")[0]) == vol and iid not in covered])
    current_yamen = None
    current_entries = []
    for iid in vol_items:
        title = reg[iid]["title"]
        # 衙门名：短行（<8字），不含"凡"/年号
        if len(title) <= 8 and not title.startswith(("凡", "国初")) and not re.match(r"^(洪武|永乐|宣德|正统|成化|弘治)", title):
            if current_yamen:
                # 保存上一条
                seq += 1
                records.append({
                    "id": f"NAM-AUTO-{vol:03d}-{seq:03d}",
                    "item_id": f"{vol:03d}-{current_yamen[1]:03d}",
                    "name": current_yamen[0],
                    "nam_type": "官制名录",
                    "scope": "吏部",
                    "entries": current_entries,
                })
            current_yamen = (title, int(iid.split("-")[1]))
            current_entries = []
        else:
            # 内容行
            if current_yamen:
                current_entries.append({"seq": len(current_entries)+1, "office": title[:30], "count": ""})
    # 最后一条
    if current_yamen:
        seq += 1
        records.append({
            "id": f"NAM-AUTO-{vol:03d}-{seq:03d}",
            "item_id": f"{vol:03d}-{current_yamen[1]:03d}",
            "name": current_yamen[0],
            "nam_type": "官制名录",
            "scope": "吏部",
            "entries": current_entries,
        })

print(f"自动生成 {len(records)} 条 NAM")
# 写入源数据文件
with open(os.path.join(ROOT, "_src", "_nam_ai_auto_06_07.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动生成：卷6/7 吏典名录批量条目"""\n\n')
    f.write("RECORDS = ")
    json.dump(records, f, ensure_ascii=False, indent=1)
print("已写入 _nam_ai_auto_06_07.py")
