# -*- coding: utf-8 -*-
"""用AI识别修复PROCESS_PROFILE层"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ===== 流程关键词（AI判断） =====
# 真正的流程条目，通常有这些特征
PROCESS_KEYWORDS = [
    "凡", "先", "然后", "次", "复", "乃", "遂",
    "程序", "流程", "步骤", "仪式", "典礼",
    "考试", "考核", "选官", "升迁",
    "祭祀", "朝会", "典礼",
]

# ===== 流程类型（AI分类） =====
def classify_process(title, original):
    """AI判断这条是不是流程，以及是什么类型的流程"""
    text = title + " " + original

    # 流程类型关键词
    if any(kw in text for kw in ["祭祀", "郊庙", "宗庙", "社稷"]):
        return "祭祀礼仪"
    if any(kw in text for kw in ["朝会", "朝仪", "班序", "上朝"]):
        return "朝会礼仪"
    if any(kw in text for kw in ["科举", "考试", "会试", "殿试"]):
        return "科举考试"
    if any(kw in text for kw in ["选官", "铨选", "除授", "升迁"]):
        return "选官流程"
    if any(kw in text for kw in ["考核", "考满", "考察"]):
        return "考核流程"
    if any(kw in text for kw in ["审判", "案件", "会审"]):
        return "司法流程"
    if any(kw in text for kw in ["工部", "营造", "修建"]):
        return "工程流程"

    return None

# ===== 重新提取流程层 =====
process_profiles = []
seq = 0

for iid, item in reg.items():
    title = item["title"]
    original = item["original"]

    ptype = classify_process(title, original)
    if ptype:
        seq += 1
        # 用条目标题作为流程名，而不是原文片段
        process_name = title[:30] if len(title) > 30 else title
        process_profiles.append({
            "process_id": f"PROC-{seq:04d}",
            "item_id": iid,
            "process_name": process_name,
            "process_type": ptype,
            "length": len(original),
        })

print(f"【PROCESS_PROFILE 修复后】{len(process_profiles)}条")
print(f"\n流程类型分布:")
type_dist = Counter(p["process_type"] for p in process_profiles)
for t, c in type_dist.most_common():
    print(f"  {t}: {c}条")

print(f"\n抽样:")
for p in process_profiles[:15]:
    print(f"  - [{p['process_type']}] {p['process_name']}")

with open(os.path.join(ROOT, "_layers", "process_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(process_profiles, f, ensure_ascii=False, indent=1)

print(f"\n已保存: _layers/process_profiles.json")
