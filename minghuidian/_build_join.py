# -*- coding: utf-8 -*-
"""跨层整合：条目→各层ID一行全看"""
import json, os, csv
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))

# 加载底座
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 加载各层数据
layers = {}
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        layers[layer] = json.load(open(p, encoding="utf-8"))
    else:
        layers[layer] = []

# 建立 item_id → 各层记录映射
join = defaultdict(lambda: {
    "item_id": "",
    "volume": 0,
    "title": "",
    "rules": [],
    "nams": [],
    "ents": [],
    "cits": [],
    "layer_count": 0,
})

# 填充底座信息
for iid, item in reg.items():
    vol = int(iid.split("-")[0])
    join[iid]["item_id"] = iid
    join[iid]["volume"] = vol
    join[iid]["title"] = item["title"][:50]

# 填充 rules
for r in layers["rules"]:
    iid = r["item_id"]
    if iid in join:
        join[iid]["rules"].append({
            "rule_id": r.get("id", ""),
            "type": r["type"],
            "subject": r.get("subject", ""),
        })

# 填充 nams
for n in layers["nams"]:
    iid = n["item_id"]
    if iid in join:
        join[iid]["nams"].append({
            "nam_id": n.get("id", ""),
            "name": n["name"],
            "nam_type": n["nam_type"],
        })

# 填充 ents
for e in layers["ents"]:
    iid = e.get("item_id", "")
    if iid.startswith("VIRT"):
        continue
    if iid in join:
        join[iid]["ents"].append({
            "text": e["text"],
            "type": e["type"],
        })

# 填充 cits
for c in layers["cits"]:
    iid = c["item_id"]
    if iid in join:
        join[iid]["cits"].append({
            "cit_id": c.get("id", ""),
            "cited_work": c["cited_work"],
        })

# 计算 layer_count
for iid, j in join.items():
    count = 0
    if j["rules"]:
        count += 1
    if j["nams"]:
        count += 1
    if j["ents"]:
        count += 1
    if j["cits"]:
        count += 1
    j["layer_count"] = count

# 转成列表
join_list = sorted(join.values(), key=lambda x: x["item_id"])

# 写 JSON
out_json = os.path.join(ROOT, "_kg_join.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(join_list, f, ensure_ascii=False, indent=1)
print(f"✓ 已生成 {out_json} ({len(join_list)} 条)")

# 写 CSV（扁平）
out_csv = os.path.join(ROOT, "_kg_join_flat.csv")
with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["item_id", "volume", "title", "layer_count", "rules_count", "nams_count", "ents_count", "cits_count"])
    for j in join_list:
        writer.writerow([
            j["item_id"],
            j["volume"],
            j["title"],
            j["layer_count"],
            len(j["rules"]),
            len(j["nams"]),
            len(j["ents"]),
            len(j["cits"]),
        ])
print(f"✓ 已生成 {out_csv} ({len(join_list)} 条)")

# 统计
from collections import Counter
layer_counts = Counter(j["layer_count"] for j in join_list)
print(f"\n跨层分布统计:")
for k in sorted(layer_counts.keys()):
    print(f"  {k}层: {layer_counts[k]} 条")

multi_layer = sum(v for k, v in layer_counts.items() if k >= 2)
print(f"\n多层覆盖（≥2层）: {multi_layer} 条 ({multi_layer*100//len(join_list)}%)")
