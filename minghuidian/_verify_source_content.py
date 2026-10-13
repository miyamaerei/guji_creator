# -*- coding: utf-8 -*-
"""抽样看原书，验证用户要的信息在不在原文里"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 抽样看几卷的原文内容
sample_vols = [2, 3, 14, 15, 106, 107, 146, 147]

print("=" * 80)
print("抽样验证：用户要的信息在原书里吗？")
print("=" * 80)

for vol in sample_vols:
    items = [(iid, item) for iid, item in reg.items() if int(iid.split("-")[0]) == vol]
    if not items:
        continue

    print(f"\n【卷{vol}】{len(items)}条")
    print(f"  首条: {items[0][1]['title'][:50]}")
    print(f"  原文: {items[0][1]['original'][:100]}...")
    print()

# 专门找几个典型问题，看原文有没有答案
print("=" * 80)
print("典型问题验证")
print("=" * 80)

# 问题1：吏部的编制人数是多少？
print("\n【问题1】吏部编制人数？")
for iid, item in reg.items():
    if "吏部" in item["title"] and ("额数" in item["original"] or "设官" in item["original"] or "一员" in item["original"]):
        print(f"  {iid}: {item['title'][:40]}")
        print(f"    {item['original'][:80]}...")
        break

# 问题2：某部门的品级？
print("\n【问题2】某部门品级？")
for iid, item in reg.items():
    if "正一品" in item["original"] or "从一品" in item["original"]:
        print(f"  {iid}: {item['title'][:40]}")
        print(f"    {item['original'][:80]}...")
        break

# 问题3：上下级关系？
print("\n【问题3】上下级关系？")
for iid, item in reg.items():
    if "属" in item["title"] and ("部" in item["title"] or "司" in item["title"]):
        print(f"  {iid}: {item['title'][:40]}")
        print(f"    {item['original'][:80]}...")
        break

# 问题4：薪酬？
print("\n【问题4】薪酬？")
for iid, item in reg.items():
    if "俸" in item["title"] or "俸给" in item["original"]:
        print(f"  {iid}: {item['title'][:40]}")
        print(f"    {item['original'][:80]}...")
        break
