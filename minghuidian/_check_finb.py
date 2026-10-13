# -*- coding: utf-8 -*-
import json, os, collections
ROOT = os.path.dirname(os.path.abspath(__file__))
ns={}
exec(open(os.path.join(ROOT,"_src","_nam_ai_finb.py"),encoding="utf-8").read(), ns)
nam=ns["RECORDS"]
ns={}
exec(open(os.path.join(ROOT,"_src","_rules_ai_finb.py"),encoding="utf-8").read(), ns)
rul=ns["RECORDS"]

print("=== NAM type distribution ===")
print(collections.Counter(r["nam_type"] for r in nam))
print("\n=== NAM by volume ===")
print(collections.Counter(int(r["item_id"].split("-")[0]) for r in nam))
print("\n=== NAM samples ===")
for r in nam[:6]: print(" ", json.dumps(r,ensure_ascii=False))
print("  ...")
for r in nam[-6:]: print(" ", json.dumps(r,ensure_ascii=False))

print("\n=== RUL type distribution ===")
print(collections.Counter(r["type"] for r in rul))
print("=== RUL marker distribution ===")
print(collections.Counter(r["source_marker"] for r in rul))
print("\n=== RUL samples ===")
for r in rul[:10]: print(" ", json.dumps(r,ensure_ascii=False))
