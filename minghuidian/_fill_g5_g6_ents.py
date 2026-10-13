# -*- coding: utf-8 -*-
"""补G5/G6提到的机构名"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
ents = json.load(open(os.path.join(ROOT, "_layers", "ents.json"), encoding="utf-8"))

existing = {e["text"] for e in ents if not e.get("item_id", "").startswith("VIRT")}

# 常见机构名清单
KNOWN_ORGS = [
    "刑部", "都察院", "大理寺", "通政司", "通政使司",
    "按察司", "按察使司", "布政司", "布政使司",
    "府", "州", "县", "卫", "千户所",
    "工部", "营缮司", "虞衡司", "都水司", "屯田司",
    "内府", "内官监", "司礼监", "御用监",
    "应天府", "顺天府", "大兴县", "宛平县",
]

new_ents = {}

# 扫描G5/G6原文
for iid, item in reg.items():
    vol = int(iid.split("-")[0])
    if not (130 <= vol <= 163):  # G5+G6
        continue
    text = item["original"]
    for org in KNOWN_ORGS:
        if org in text and org not in existing and org not in new_ents:
            # 过滤掉太短的（"府"、"州"、"县"太泛）
            if len(org) <= 2 and org in ["府", "州", "县", "卫"]:
                continue
            new_ents[org] = {
                "item_id": iid,
                "text": org,
                "type": "institution",
                "rank_order": "未明",
                "confidence": "low",
            }

print(f"G5/G6新提取实体: {len(new_ents)} 个")
for name in new_ents:
    print(f"  + {name}")

# 追加
all_ents = ents + list(new_ents.values())
print(f"\n实体总数: {len(all_ents)}")

with open(os.path.join(ROOT, "_layers", "ents.json"), "w", encoding="utf-8") as f:
    json.dump(all_ents, f, ensure_ascii=False, indent=1)
print("已写回")
