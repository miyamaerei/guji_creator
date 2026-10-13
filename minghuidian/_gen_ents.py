# -*- coding: utf-8 -*-
"""批量提取实体：从 rules 和 nams 中提取衙门名/官职名"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 读取现有实体
ents_path = os.path.join(ROOT, "_layers", "ents.json")
existing = json.load(open(ents_path, encoding="utf-8"))
existing_names = {e["text"] for e in existing}

# 读取 rules
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))

# 实体提取词典
ORG_SUFFIX = ["部", "院", "寺", "监", "司", "府", "卫", "所", "局", "仓", "库", "厂", "署", "厅", "学堂"]
OFF_SUFFIX = ["尚书", "侍郎", "郎中", "员外郎", "主事", "御史", "给事中", "都督", "总兵", "巡抚", "巡按", "知府", "知州", "知县"]

new_ents = []
seen = set()

# 从 NAM 中提取衙门名
for n in nams:
    name = n["name"]
    if name in existing_names or name in seen:
        continue
    # 判断类型
    if any(name.endswith(s) for s in ["卫", "所"]):
        etype = "institution"
    elif any(name.endswith(s) for s in ORG_SUFFIX):
        etype = "institution"
    else:
        continue
    seen.add(name)
    new_ents.append({
        "item_id": n["item_id"],
        "text": name,
        "type": etype,
        "rank_order": "未明",
        "confidence": "medium",
    })

# 从 rules 中提取 subject 中的衙门
for r in rules:
    subj = r.get("subject", "")
    if subj in existing_names or subj in seen:
        continue
    if any(subj.endswith(s) for s in ORG_SUFFIX):
        seen.add(subj)
        new_ents.append({
            "item_id": r["item_id"],
            "text": subj,
            "type": "institution",
            "rank_order": "未明",
            "confidence": "low",
        })

print(f"新提取实体: {len(new_ents)} 条")

# 合并
all_ents = existing + new_ents
with open(ents_path, "w", encoding="utf-8") as f:
    json.dump(all_ents, f, ensure_ascii=False, indent=1)
print(f"实体总数: {len(all_ents)} 条")

# 统计
from collections import Counter
type_dist = Counter(e["type"] for e in all_ents)
print("\n实体类型分布:")
for t, c in type_dist.most_common():
    print(f"  {t}: {c}")
