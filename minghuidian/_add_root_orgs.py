# -*- coding: utf-8 -*-
"""补根衙门到实体列表"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
ents = json.load(open(os.path.join(ROOT, "_layers", "ents.json"), encoding="utf-8"))

# 需要补的根衙门
ROOT_ORGS = ["五军都督府", "前军都督府", "后军都督府", "左军都督府", "右军都督府"]

existing = {e["text"] for e in ents}
added = 0
for org in ROOT_ORGS:
    if org not in existing:
        ents.append({
            "item_id": "VIRT-ROOT",
            "text": org,
            "type": "institution",
            "node_type": "根节点",
            "parent_id": "全书",
            "rank_order": "正一品",
            "confidence": "high",
        })
        added += 1

print(f"补充根衙门: {added} 个")

with open(os.path.join(ROOT, "_layers", "ents.json"), "w", encoding="utf-8") as f:
    json.dump(ents, f, ensure_ascii=False, indent=1)
print("已写回")
