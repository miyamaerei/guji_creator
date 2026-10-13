# -*- coding: utf-8 -*-
"""第二轮精细化：G3 朝贡国 + G6 物料补全"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

nams_records = []
nseq = 0

# G3 朝贡国/外国名录
for iid in sorted(reg):
    v = int(iid.split("-")[0])
    if not (42 <= v <= 105) or iid in covered:
        continue
    title = reg[iid]["title"]
    # 短行国名
    if len(title) <= 12 and not title.startswith(("洪武", "永乐", "国初", "凡", "一")):
        if any(k in title for k in ["国", "番", "夷", "蛮", "苗", "洞", "寨", "司"]):
            nseq += 1
            nams_records.append({
                "id": f"NAM-FRN2-{v:03d}-{nseq:03d}",
                "item_id": iid,
                "name": title,
                "nam_type": "官制名录",
                "scope": "礼部",
                "entries": [{"seq": 1, "office": title, "count": ""}],
            })

# G6 物料补全
MATERIAL_UNITS = ["斤", "两", "钱", "分", "疋", "匹", "根", "条", "张", "个", "只", "面", "座", "所", "间", "丈", "尺", "寸", "石", "斗", "升", "合", "勺", "撮", "圭", "粟", "两", "锭", "铤", "块", "片", "领", "袭", "副", "对", "双", "把", "枚", "颗", "粒", "株", "棵", "本", "株"]

for iid in sorted(reg):
    v = int(iid.split("-")[0])
    if not (144 <= v <= 163) or iid in covered:
        continue
    title = reg[iid]["title"]
    if len(title) <= 20 and any(title.endswith(u) for u in MATERIAL_UNITS):
        nseq += 1
        nams_records.append({
            "id": f"NAM-MAT2-{v:03d}-{nseq:03d}",
            "item_id": iid,
            "name": title,
            "nam_type": "官制名录",
            "scope": "工部",
            "entries": [{"seq": 1, "office": title, "count": ""}],
        })

print(f"第二轮生成名录: {len(nams_records)} 条")

with open(os.path.join(ROOT, "_src", "_nam_ai_refined2.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动生成：第二轮精细化名录"""\n\n')
    f.write("RECORDS = ")
    json.dump(nams_records, f, ensure_ascii=False, indent=1)

print("已写入")
