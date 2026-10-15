# -*- coding: utf-8 -*-
"""Fix missing titles in Shaanxi main files."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_data")

fixes = {
    "vol32/32-001_西安府.json": "西安府",
    "vol34/34-001_凤翔府.json": "凤翔府",
    "vol37/37-007_陕西行都司.json": "陕西行都指挥使司",
}

for rel, title in fixes.items():
    p = os.path.join(DATA, rel)
    if not os.path.exists(p):
        print(f"SKIP {rel} (not found)")
        continue
    data = json.load(open(p, encoding="utf-8"))
    if not data.get("title"):
        data["title"] = title
        json.dump(data, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(f"Fixed title in {rel}: {title}")
    else:
        print(f"OK {rel}: {data['title']}")
