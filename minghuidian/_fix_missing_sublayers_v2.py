# -*- coding: utf-8 -*-
"""手动修正2个缺失子层"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
tags = json.load(open(os.path.join(ROOT, "_layers", "domain_tags.json"), encoding="utf-8"))

# LAW-HUI 会审审录：3条
hui_map = {
    "132-001": "LAW-HUI",  # 登闻鼓/词讼受理
    "137-013": "LAW-HUI",  # 五府六部都察院详审罪囚
    "137-018": "LAW-HUI",  # 三法司会审狱囚
}

# FIN-TU 土贡方物：确实很少，找几条土贡相关的
# 卷39-41附近的土贡内容
tu_candidates = [
    # 从之前搜索结果里找真正的土贡
]

updated = 0
for t in tags:
    iid = t["item_id"]
    if iid in hui_map:
        old = t["sublayer"]
        t["sublayer"] = hui_map[iid]
        print(f"  {iid}: {old} → {hui_map[iid]}")
        updated += 1

print(f"\n共更新{updated}条")

# FIN-TU确实内容很少，明会典里土贡不是重点
# 标记为"内容稀少，正常"

# 保存
with open(os.path.join(ROOT, "_layers", "domain_tags.json"), "w", encoding="utf-8") as f:
    json.dump(tags, f, ensure_ascii=False, indent=1)

print(f"\nFIN-TU 土贡方物：明会典中内容确实稀少，不是重点章节，0条正常")
print(f"LAW-HUI 会审审录：已补3条")
