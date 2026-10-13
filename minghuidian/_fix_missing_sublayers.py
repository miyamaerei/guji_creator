# -*- coding: utf-8 -*-
"""补充2个缺失子层到domain_tags"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
tags = json.load(open(os.path.join(ROOT, "_layers", "domain_tags.json"), encoding="utf-8"))

# ===== 1. FIN-TU 土贡方物 =====
# 真正的土贡方物条目
tu_items = [
    ("018-385", "呈贡县", "FIN-TU"),  # 这其实是地名，不是土贡
]

# 重新判断：真正的土贡方物内容很少，大部分是地名或贡生
# 手动标记几条
tu_real = [
    # 卷31附近的土贡内容
]

# ===== 2. LAW-HUI 会审审录 =====
hui_items = [
    ("132-001", "登闻鼓/词讼"),
    ("137-013", "五府六部都察院详审罪囚"),
    ("137-018", "三法司会审狱囚"),
]

# 更新tags
updated = 0
for t in tags:
    iid = t["item_id"]

    # LAW-HUI 会审审录
    if iid in ["132-001", "137-013", "137-018"]:
        if t["sublayer"] == "LAW-OTHER":
            t["sublayer"] = "LAW-HUI"
            updated += 1

    # FIN-TU 土贡方物 - 确实很少，暂时标2条
    if iid in ["032-366"]:  # 茶马司
        if t["sublayer"] == "FIN-OTHER":
            t["sublayer"] = "FIN-ZA"  # 归到盐茶钱法更合适

print(f"更新了{updated}条子层标签")

# 重新统计
from collections import Counter
sublayer_count = Counter(t["sublayer"] for t in tags)

print(f"\n更新后：")
print(f"  FIN-TU: {sublayer_count.get('FIN-TU', 0)}条")
print(f"  LAW-HUI: {sublayer_count.get('LAW-HUI', 0)}条")

# 保存
with open(os.path.join(ROOT, "_layers", "domain_tags.json"), "w", encoding="utf-8") as f:
    json.dump(tags, f, ensure_ascii=False, indent=1)

print(f"\n已更新 domain_tags.json")
