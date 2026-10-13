# -*- coding: utf-8 -*-
"""精细化批量生成：G3 礼仪规则 + G6 物料/卫所名录"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

rules_records = []
nams_records = []
rseq = 0
nseq = 0

# 礼仪规则触发词
RITUAL_MARKERS = ["洪武", "永乐", "洪熙", "宣德", "正统", "景泰", "天顺", "成化", "弘治", "正德", "嘉靖"]

# 物料单位
MATERIAL_UNITS = ["斤", "两", "钱", "分", "疋", "匹", "根", "条", "张", "个", "只", "面", "座", "所", "间", "丈", "尺", "寸", "石", "斗", "升", "合", "勺", "撮", "圭", "粟"]

for iid in sorted(reg):
    v = int(iid.split("-")[0])
    if iid in covered:
        continue
    title = reg[iid]["title"]

    # G3 礼部 (42-105)：礼仪规则
    if 42 <= v <= 105:
        # 礼仪规则：洪武X年定/永乐X年定/国初...
        if any(title.startswith(m) for m in RITUAL_MARKERS) or title.startswith("国初"):
            rseq += 1
            rules_records.append({
                "id": f"RUL-RIT-{v:03d}-{rseq:03d}",
                "item_id": iid,
                "type": "程序",
                "source_marker": "凡",
                "subject": "礼部",
                "action": title[:25],
                "confidence": 0.75,
            })
        # 朝贡国/外国名录
        elif len(title) <= 15 and any(k in title for k in ["国", "番", "夷", "朝贡"]):
            nseq += 1
            nams_records.append({
                "id": f"NAM-FRN-{v:03d}-{nseq:03d}",
                "item_id": iid,
                "name": title,
                "nam_type": "官制名录",
                "scope": "礼部",
                "entries": [{"seq": 1, "office": title, "count": ""}],
            })

    # G6 工部 (144-163)：物料明细
    elif 144 <= v <= 163:
        # 物料：X斤/X根/X疋...
        if any(title.endswith(u) for u in MATERIAL_UNITS) and len(title) <= 15:
            nseq += 1
            nams_records.append({
                "id": f"NAM-MAT-{v:03d}-{nseq:03d}",
                "item_id": iid,
                "name": title,
                "nam_type": "官制名录",
                "scope": "工部",
                "entries": [{"seq": 1, "office": title, "count": ""}],
            })
        # 卫所/衙门名录
        elif len(title) <= 10 and title.endswith(("卫", "所", "司", "局", "厂", "库", "仓")):
            nseq += 1
            nams_records.append({
                "id": f"NAM-WEI-{v:03d}-{nseq:03d}",
                "item_id": iid,
                "name": title,
                "nam_type": "卫所名录",
                "scope": "工部",
                "entries": [{"seq": 1, "office": title, "count": ""}],
            })

print(f"礼仪规则: {len(rules_records)} 条")
print(f"物料/卫所名录: {len(nams_records)} 条")

with open(os.path.join(ROOT, "_src", "_rules_ai_ritual.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动生成：G3 礼仪规则"""\n\n')
    f.write("RECORDS = ")
    json.dump(rules_records, f, ensure_ascii=False, indent=1)

with open(os.path.join(ROOT, "_src", "_nam_ai_material.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动生成：G6 物料/卫所名录"""\n\n')
    f.write("RECORDS = ")
    json.dump(nams_records, f, ensure_ascii=False, indent=1)

print("已写入")
