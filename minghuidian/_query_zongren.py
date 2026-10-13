# -*- coding: utf-8 -*-
"""查宗人府相关规则"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 找宗人府相关的规则
zongren = [r for r in rules if "宗人府" in r.get("subject", "") or "宗人" in r.get("action", "")]
print(f"宗人府相关规则: {len(zongren)} 条")

for r in zongren[:5]:
    iid = r["item_id"]
    print(f"\n--- {iid} ---")
    print(f"type: {r['type']}")
    print(f"subject: {r['subject']}")
    print(f"action: {r.get('action', '')[:80]}")
    print(f"原文: {reg[iid]['original'][:100]}...")
