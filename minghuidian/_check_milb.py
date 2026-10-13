# -*- coding: utf-8 -*-
import json, os, importlib.util, collections
ROOT = os.path.dirname(os.path.abspath(__file__))
def load(f):
    spec = importlib.util.spec_from_file_location("m", os.path.join(ROOT, "_src", f))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m.RECORDS
nam = load("_nam_ai_milb.py"); rul = load("_rules_ai_milb.py")
print("== NAM by type ==")
print(collections.Counter(r["nam_type"] for r in nam))
print("== NAM by vol ==")
print(collections.Counter(int(r["item_id"].split("-")[0]) for r in nam))
print("== RUL by type ==")
print(collections.Counter(r["type"] for r in rul))
print("== RUL by marker ==")
print(collections.Counter(r["source_marker"] for r in rul))
print("== RUL sample ==")
for r in rul:
    print(r["item_id"], r["source_marker"], r["type"], "|", r["subject"], "->", r["action"])
