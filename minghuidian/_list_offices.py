# -*- coding: utf-8 -*-
"""查看现有官职列表"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
offices = json.load(open(os.path.join(ROOT, "_layers", "offices_clean.json"), encoding="utf-8"))

print(f"共 {len(offices)} 个官职")
print("=" * 60)
for i, o in enumerate(offices):
    print(f"{i+1:2d}. {o['office_name']:<15} 出现{o['count']}次")
