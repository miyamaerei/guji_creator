# -*- coding: utf-8 -*-
"""Fix Shaanxi data: bad ent types + duplicate geos in small files."""
import json, glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_data")

# 1. Fix bad ent types in main files
TYPE_FIX = {"river": "mtn", "fief": "geo", "weisuo": "geo"}
fixed_ents = 0
for f in sorted(glob.glob(os.path.join(DATA, "vol3[2-7]", "*.json"))):
    data = json.load(open(f, encoding="utf-8"))
    changed = False
    for e in data.get("layers", {}).get("ents", []):
        t = e.get("type", "")
        if t in TYPE_FIX:
            e["type"] = TYPE_FIX[t]
            fixed_ents += 1
            changed = True
    if changed:
        json.dump(data, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"Fixed ent types in {os.path.basename(f)}")

print(f"Total ents fixed: {fixed_ents}")

# 2. Empty geos in small files (c##/s##/w## pattern) to avoid duplicates
#    Main files already contain all geo nodes.
emptied = 0
for f in sorted(glob.glob(os.path.join(DATA, "vol3[2-7]", "*_[csw][0-9][0-9]_*.json"))):
    data = json.load(open(f, encoding="utf-8"))
    geos = data.get("layers", {}).get("geos", [])
    if geos:
        data["layers"]["geos"] = []
        json.dump(data, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        emptied += 1
        print(f"Emptied geos in {os.path.basename(f)} ({len(geos)} nodes)")

print(f"Total small files emptied: {emptied}")
