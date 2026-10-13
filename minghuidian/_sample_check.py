# -*- coding: utf-8 -*-
"""抽样核对：随机抽5条记录，对比原文"""
import json, os, random

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))

random.seed(42)

print("=" * 60)
print("抽样核对报告")
print("=" * 60)

# 抽3条 RUL
print("\n【抽样1】规则类 RUL")
sample_rules = random.sample(rules, 3)
for i, r in enumerate(sample_rules, 1):
    iid = r["item_id"]
    original = reg.get(iid, {}).get("original", "【未找到】")
    print(f"\n  样本{i}: {iid}")
    print(f"  原文: {original[:80]}...")
    print(f"  生成: type={r['type']}, marker={r['source_marker']}")
    print(f"        subject={r.get('subject','')}, action={r.get('action','')[:40]}")

# 抽2条 NAM
print("\n【抽样2】名录类 NAM")
sample_nams = random.sample(nams, 2)
for i, n in enumerate(sample_nams, 1):
    iid = n["item_id"]
    original = reg.get(iid, {}).get("original", "【未找到】")
    print(f"\n  样本{i}: {iid}")
    print(f"  原文: {original[:80]}...")
    print(f"  生成: name={n['name']}, type={n['nam_type']}")
    if n.get("staff_config"):
        print(f"        staff={n['staff_config']}")
