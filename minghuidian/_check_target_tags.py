# -*- coding: utf-8 -*-
"""检查特定条目的sublayer"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
tags = json.load(open(os.path.join(ROOT, "_layers", "domain_tags.json"), encoding="utf-8"))

targets = ["132-001", "137-013", "137-018", "032-366"]
for t in tags:
    if t["item_id"] in targets:
        print(f"  {t['item_id']}: {t['sublayer']} - {t['title'][:30]}")
