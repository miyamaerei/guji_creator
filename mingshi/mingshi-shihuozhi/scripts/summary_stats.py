#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""汇总统计 —— 为使用报告生成准确数字。"""

import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

from _common import (
    BASE_DIR,
    ENT_LINKS_FILE,
    FROZEN_DIRS,
    KG_JOIN_FILE,
    KG_JOIN_FLAT_FILE,  # noqa: E402
    LEDGER_FLAT_FILE,
    LEDGER_TREE_FILE,  # noqa: E402
    REGISTRY_FILE,
    LAYER_SPECS,
    layer_dir,
)  # noqa: E402

reg = json.load(open(REGISTRY_FILE, encoding="utf-8"))
print("== 底座 ==")
print(f"registry 条目: {len(reg)}")
for vol in ["食货一", "食货二", "食货三", "食货四", "食货五", "食货六"]:
    items = [v for v in reg.values() if v["volume"] == vol]
    print(f"  {vol}: {len(items)} 条, {sum(v['chars'] for v in items):,} 字")

rows = list(csv.DictReader(open(LEDGER_FLAT_FILE, encoding="utf-8-sig")))
print("\n== C16 总账树 ==")
print(f"明细: {len(rows)} 条")
print(f"约数: {sum(1 for r in rows if r['约数'])} 条")
print(
    f"含未明: {sum(1 for r in rows if '未明' in (r['收入类别'], r['形态'], r['对象']))} 条"
)
print("银合计: %s 两" % f"{sum(int(r['数值']) for r in rows if r['单位'] == '两'):,}")
print("粮合计: %s 石" % f"{sum(int(r['数值']) for r in rows if r['单位'] == '石'):,}")
print("草合计: %s 束" % f"{sum(int(r['数值']) for r in rows if r['单位'] == '束'):,}")
print("盐合计: %s 引" % f"{sum(int(r['数值']) for r in rows if r['单位'] == '引'):,}")
print("按兵种:", dict(Counter(r["兵种"] for r in rows)))

print("\n== 各层构建状态 ==")
for k, spec in LAYER_SPECS.items():
    d = layer_dir(k)
    fs = (
        sorted(p for p in d.glob("*.json") if not p.name.startswith("_"))
        if d.exists()
        else []
    )
    n = 0
    for f in fs:
        try:
            data = json.load(open(f, encoding="utf-8"))
            if isinstance(data, list):
                n += len(data)
            elif isinstance(data, dict):
                n += sum(len(v) for v in data.values() if isinstance(v, list)) or len(
                    data
                )
        except Exception:
            pass
    print(f"  {k:<8} {spec['name']:<12} 文件{len(fs)} 记录{n}")

# 跨层索引（SKILL §13 正式产物）
print("\n== 跨层索引（kg_join）==")
for f in [KG_JOIN_FILE, KG_JOIN_FLAT_FILE]:
    q = f
    if q.exists():
        print(f"  {q.relative_to(BASE_DIR)}  {q.stat().st_size} B")

# 实体引用连通率（build_entity_links.py 产物）
print("\n== 实体引用连通率 ==")
if ENT_LINKS_FILE.exists():
    el = json.load(open(ENT_LINKS_FILE, encoding="utf-8"))
    n_total = len(el)
    n_linked = sum(1 for o in el if o.get("link_count"))
    total_refs = sum(o.get("link_count", 0) for o in el)
    print(
        f"  引用索引: {n_linked}/{n_total} 实体被引用 ({n_linked / n_total * 100:.1f}%)"
    )
    print(f"  总引用对: {total_refs}")
    per_layer: Counter = Counter()
    for o in el:
        for lay, ids in (o.get("links") or {}).items():
            per_layer[lay] += len(ids)
    print("  每层引用:", " ".join(f"{k}={v}" for k, v in sorted(per_layer.items())))
else:
    print("  _ent_links.json 未构建（运行 scripts/build_entity_links.py）")

# 遗留文件
print("\n== 遗留（已废弃）==")
for p in FROZEN_DIRS:
    if p.exists():
        for f in sorted(p.rglob("*")):
            if f.is_file():
                print(f"  {f.relative_to(BASE_DIR)}  {f.stat().st_size} B")
