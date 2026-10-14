#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""总账字段覆盖率核查 —— 统计 未明 残留与来源类别分布。"""
import csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

from _common import LEDGER_FLAT_FILE  # noqa: E402

rows = list(csv.DictReader(open(LEDGER_FLAT_FILE, encoding="utf-8-sig")))
print(f"明细总条数: {len(rows)}")

und = [r for r in rows if "未明" in (r["收入类别"], r["形态"], r["对象"])]
print(f"含未明字段条数: {len(und)}")
seen = set()
for r in und:
    k = (r["收入类别"], r["形态"], r["对象"], r["原短语"])
    if k in seen:
        continue
    seen.add(k)
    print(f"  {r['镇']:<4} origin={r['收入类别']:<4} form={r['形态']:<4} "
          f"obj={r['对象']:<5} | {r['原短语']}")

print("\n=== 收入类别分布 ===")
for k, v in Counter(r["收入类别"] for r in rows).most_common():
    amt = sum(int(r["数值"]) for r in rows if r["收入类别"] == k)
    print(f"  {k:<6} {v:>3} 条")
print("\n=== 形态分布 ===")
for k, v in Counter(r["形态"] for r in rows).most_common():
    print(f"  {k:<6} {v:>3} 条")
print("\n=== 量纲分布 ===")
for k, v in Counter(r["量纲"] for r in rows).most_common():
    print(f"  {k:<6} {v:>3} 条")
print(f"\n约数条数: {sum(1 for r in rows if r['约数'])} / {len(rows)}")
