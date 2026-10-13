# -*- coding: utf-8 -*-
"""开两个G3专门层：DRESS冠服器物 + FOREIGN朝贡外国"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ===== 1. DRESS 冠服器物层 =====
DRESS_KEYWORDS = ["冠服", "冕旒", "服色", "车舆", "袍", "衫", "裙", "带", "冠", "冕", "服", "舆", "辂", "辇"]

def is_dress(title, original):
    text = title + original
    for kw in DRESS_KEYWORDS:
        if kw in text:
            return True
    return False

# ===== 2. FOREIGN 朝贡外国层 =====
FOREIGN_KEYWORDS = ["朝贡", "外国", "夷", "番", "倭", "虏", "朝鲜", "日本", "安南", "琉球", "哈密", "吐鲁番"]

def is_foreign(title, original):
    text = title + original
    for kw in FOREIGN_KEYWORDS:
        if kw in text:
            return True
    return False

# 批量提取G3礼部（卷42-105）
dress_records = []
foreign_records = []
d_seq = f_seq = 0

for iid, item in reg.items():
    vol = int(iid.split("-")[0])
    if not (42 <= vol <= 105):
        continue

    title = item["title"]
    original = item["original"]

    if is_dress(title, original):
        d_seq += 1
        dress_records.append({
            "dress_id": f"DRESS-{d_seq:04d}",
            "item_id": iid,
            "category": "冠服",
            "name": title[:30],
        })

    if is_foreign(title, original):
        f_seq += 1
        foreign_records.append({
            "foreign_id": f"FOR-{f_seq:04d}",
            "item_id": iid,
            "type": "朝贡",
            "name": title[:30],
        })

print(f"【DRESS 冠服器物层】{len(dress_records)} 条")
print(f"【FOREIGN 朝贡外国层】{len(foreign_records)} 条")

# 按卷分布
print(f"\nDRESS按卷分布:")
d_by_vol = Counter(int(r["item_id"].split("-")[0]) for r in dress_records)
for vol in sorted(d_by_vol.keys())[:10]:
    print(f"  卷{vol}: {d_by_vol[vol]}条")

print(f"\nFOREIGN按卷分布:")
f_by_vol = Counter(int(r["item_id"].split("-")[0]) for r in foreign_records)
for vol in sorted(f_by_vol.keys())[:10]:
    print(f"  卷{vol}: {f_by_vol[vol]}条")

# 保存
for name, data in [("dress", dress_records), ("foreign", foreign_records)]:
    outpath = os.path.join(ROOT, "_layers", f"{name}.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"已保存: {outpath}")
