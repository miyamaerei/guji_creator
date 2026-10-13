# -*- coding: utf-8 -*-
"""开INSPECT风宪事务层：承接都察院事务"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 事务类型关键词
INSPECT_TYPES = {
    "巡按": ["巡按", "分巡", "巡行"],
    "刷卷": ["刷卷", "磨勘", "文卷"],
    "清军": ["清军", "清理军伍"],
    "审录": ["审录", "审録", "重囚", "罪囚"],
    "考察": ["考察", "考察风宪", "考察百司"],
    "考满": ["考满", "给由"],
    "选任": ["选", "除授", "除", "差御史", "差官"],
    "弹劾": ["弹劾", "纠劾", "举劾"],
    "巡抚": ["巡抚", "抚按"],
}

def classify_inspect(title, original):
    """判断事务类型"""
    text = title + original
    for affair, keywords in INSPECT_TYPES.items():
        for kw in keywords:
            if kw in text:
                return affair
    return "其他"

# 批量提取G7（卷164-178）
insp_records = []
insp_seq = 0

for iid, item in reg.items():
    vol = int(iid.split("-")[0])
    if 164 <= vol <= 178:
        affair = classify_inspect(item["title"], item["original"])
        # 只提取事务类（不是名录类）
        if affair != "其他" or len(item["title"]) < 10:
            insp_seq += 1
            insp_records.append({
                "insp_id": f"INSP-{insp_seq:04d}",
                "item_id": iid,
                "affair_type": affair,
                "name": item["title"][:30],
            })

print(f"【INSPECT 风宪事务层】{len(insp_records)} 条")
print()

# 事务类型分布
type_dist = Counter(r["affair_type"] for r in insp_records)
print("事务类型分布:")
for t, c in type_dist.most_common():
    print(f"  {t:8s}: {c:4d}条")

# 按卷分布
by_vol = Counter()
for r in insp_records:
    vol = int(r["item_id"].split("-")[0])
    by_vol[vol] += 1

print(f"\n按卷分布:")
for vol in sorted(by_vol.keys()):
    print(f"  卷{vol}: {by_vol[vol]}条")

# 保存
outpath = os.path.join(ROOT, "_layers", "inspect.json")
with open(outpath, "w", encoding="utf-8") as f:
    json.dump(insp_records, f, ensure_ascii=False, indent=1)
print(f"\n已保存: {outpath}")
