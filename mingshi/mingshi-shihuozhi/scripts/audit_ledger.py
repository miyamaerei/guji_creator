#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""总账解析审计 —— 逐镇对照原文，人工可核。"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

from _common import BASE_DIR, LEDGER_FLAT_FILE, load_json  # noqa: E402

rows = list(csv.DictReader(open(LEDGER_FLAT_FILE, encoding="utf-8-sig")))
reg = load_json(BASE_DIR / "_data" / "registry.json")

targets = sys.argv[1:] or ["宣府", "大同", "井陉", "蓟州"]
for t in targets:
    item_id = next(r["item_id"] for r in rows if r["镇"] == t)
    print(f"\n===== {t}  ({item_id}) =====")
    print("原文:")
    print("  " + reg[item_id]["original"])
    print("解析:")
    for r in rows:
        if r["镇"] == t:
            approx = "(约)" if r["约数"] else "    "
            print(f"  {r['兵种']:<4} {r['收入类别']:<6} {r['形态']:<4} "
                  f"{int(r['数值']):>10,} {r['单位']:<2} {approx} | {r['原短语']}")
