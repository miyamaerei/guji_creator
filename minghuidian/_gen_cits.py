# -*- coding: utf-8 -*-
"""批量提取引用：识别典籍直引段"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 典籍词典
CIT_BOOKS = ["诸司职掌", "明集礼", "皇明祖训", "大诰", "大明令", "洪武礼制", "大明律", "礼记", "周礼", "仪礼"]

cits_path = os.path.join(ROOT, "_layers", "cits.json")
existing = json.load(open(cits_path, encoding="utf-8"))
covered_items = {c["item_id"] for c in existing}

new_cits = []
seq = len(existing)

for iid, item in reg.items():
    if iid in covered_items:
        continue
    original = item["original"]
    for book in CIT_BOOKS:
        if book in original:
            seq += 1
            new_cits.append({
                "id": f"CIT-AUTO-{seq:03d}",
                "item_id": iid,
                "cited_work": book,
                "citation_type": "直引",
                "context": "典籍直引",
                "confidence": "medium",
            })
            break

print(f"新提取引用: {len(new_cits)} 条")

# 合并
all_cits = existing + new_cits
with open(cits_path, "w", encoding="utf-8") as f:
    json.dump(all_cits, f, ensure_ascii=False, indent=1)
print(f"引用总数: {len(all_cits)} 条")

# 统计
from collections import Counter
book_dist = Counter(c["cited_work"] for c in all_cits)
print("\n引用典籍分布:")
for b, c in book_dist.most_common():
    print(f"  {b}: {c}")
