# -*- coding: utf-8 -*-
"""看原文格式，识别排版层级"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 看卷3（都察院所在卷）的原文，找排版层级
print("=" * 70)
print("【卷3 原文格式抽样】找排版层级标记")
print("=" * 70)

vol3_items = [(iid, item) for iid, item in reg.items() if iid.startswith("003-")]
for iid, item in vol3_items[:10]:
    print(f"\n{iid}: {item['title'][:60]}")
    print(f"  原文前150字:")
    print(f"    {item['original'][:150]}")

# 看看有没有特殊标记，比如【正官】【首领官】【属官】
print("\n\n" + "=" * 70)
print("【找子标题标记】【正官】【首领官】【属官】")
print("=" * 70)

count = 0
for iid, item in reg.items():
    text = item["original"]
    if "【正官】" in text or "【首领官】" in text or "【属官】" in text:
        count += 1
        if count <= 5:
            print(f"\n{iid}: {item['title'][:50]}")
            # 找子标题位置
            for mark in ["【正官】", "【首领官】", "【属官】"]:
                pos = text.find(mark)
                if pos >= 0:
                    context = text[max(0,pos-10):pos+30]
                    print(f"  {mark}: ...{context}...")

print(f"\n\n共 {count} 条条目包含【正官】/【首领官】/【属官】标记")
