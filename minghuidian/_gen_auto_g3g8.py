# -*- coding: utf-8 -*-
"""通用批量生成器：G3-G8 所有卷自动生成 RUL + NAM"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

# G3-G8: 卷42-180
rules_records = []
nams_records = []
rseq = 0
nseq = 0

ERA_RE = re.compile(r"^(洪武|永乐|洪熙|宣德|正统|景泰|天顺|成化|弘治|正德|嘉靖|隆庆|万历)")

for iid in sorted(reg):
    v = int(iid.split("-")[0])
    if v < 42 or iid in covered:
        continue
    item = reg[iid]
    title = item["title"]
    body = item["original"]

    # 规则类：凡...开头
    if title.startswith("凡") or title.startswith("一凡"):
        rseq += 1
        # 简单提取 subject/action
        subject = "各衙门"
        action = title[:20]
        if "军官" in title or "军职" in title:
            subject = "武官"
        elif "文官" in title or "官员" in title:
            subject = "文官"
        rules_records.append({
            "id": f"RUL-AUTO-{v:03d}-{rseq:03d}",
            "item_id": iid,
            "type": "义务",
            "source_marker": "凡",
            "subject": subject,
            "action": action,
            "confidence": 0.7,
        })
    # 名录类：短行衙门/地名
    elif len(title) <= 10 and not title.startswith(("国初", "南京")):
        # 识别是否是衙门/地名
        if title.endswith(("司", "府", "州", "县", "卫", "所", "寺", "监", "局", "仓", "库", "厂", "署", "院")):
            nseq += 1
            nams_records.append({
                "id": f"NAM-AUTO-{v:03d}-{nseq:03d}",
                "item_id": iid,
                "name": title,
                "nam_type": "官制名录",
                "scope": "户部",
                "entries": [{"seq": 1, "office": title, "count": ""}],
            })

print(f"自动生成规则: {len(rules_records)} 条")
print(f"自动生成名录: {len(nams_records)} 条")

# 写入
with open(os.path.join(ROOT, "_src", "_rules_ai_auto_g3g8.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动生成：G3-G8 规则批量"""\n\n')
    f.write("RECORDS = ")
    json.dump(rules_records, f, ensure_ascii=False, indent=1)

with open(os.path.join(ROOT, "_src", "_nam_ai_auto_g3g8.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动生成：G3-G8 名录批量"""\n\n')
    f.write("RECORDS = ")
    json.dump(nams_records, f, ensure_ascii=False, indent=1)

print("已写入")
