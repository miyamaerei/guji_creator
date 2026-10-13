# -*- coding: utf-8 -*-
"""Schema检查 + 树结构密度分析"""
import json, os
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

print("=" * 70)
print("Schema 完整性检查")
print("=" * 70)

# ===== 1. 各层schema字段检查 =====
expected_fields = {
    "ents": ["item_id", "text", "type"],
    "rules": ["item_id", "type", "subject", "source_marker"],
    "nams": ["item_id", "name", "nam_type"],
    "cits": ["item_id", "cited_work", "citation_type"],
}

for layer, expected in expected_fields.items():
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if not os.path.exists(p):
        print(f"\n❌ {layer}: 文件不存在")
        continue
    data = json.load(open(p, encoding="utf-8"))
    print(f"\n【{layer}】共 {len(data)} 条")

    # 检查每条记录的字段完整性
    missing_fields = Counter()
    for r in data:
        for f in expected:
            if f not in r:
                missing_fields[f] += 1

    if missing_fields:
        print(f"  ⚠️ 缺失字段:")
        for f, c in missing_fields.most_common():
            print(f"    {f}: {c} 条缺失")
    else:
        print(f"  ✅ 必填字段完整")

    # 列出所有出现过的字段
    all_fields = set()
    for r in data:
        all_fields.update(r.keys())
    print(f"  实际字段: {sorted(all_fields)}")

# ===== 2. 树结构密度分析 =====
print("\n" + "=" * 70)
print("树结构密度分析（书→大卷组→小卷→条目→各层）")
print("=" * 70)

reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))
ents = json.load(open(os.path.join(ROOT, "_layers", "ents.json"), encoding="utf-8"))
cits = json.load(open(os.path.join(ROOT, "_layers", "cits.json"), encoding="utf-8"))

# 按item_id分组
def by_vol(data):
    d = defaultdict(int)
    for r in data:
        vol = int(r["item_id"].split("-")[0])
        d[vol] += 1
    return d

rules_by_vol = by_vol(rules)
nams_by_vol = by_vol(nams)
ents_by_vol = by_vol([e for e in ents if not e.get("item_id", "").startswith("VIRT")])
cits_by_vol = by_vol(cits)

# 大卷组
GROUPS = [
    ("G0 宗人府", [1]),
    ("G1 吏部", list(range(2, 14))),
    ("G2 户部", list(range(14, 42))),
    ("G3 礼部", list(range(42, 106))),
    ("G4 兵部", list(range(106, 130))),
    ("G5 刑部", list(range(130, 144))),
    ("G6 工部", list(range(144, 164))),
    ("G7 诸文职", list(range(164, 179))),
    ("G8 诸武职", [179, 180]),
]

print(f"\n{'卷组':12s} {'总条目':>6s} {'规则':>5s} {'名录':>5s} {'实体':>5s} {'引用':>5s} {'密度':>6s}")
print("-" * 60)

for gname, vols in GROUPS:
    total = sum(1 for iid in reg if int(iid.split("-")[0]) in vols)
    r = sum(rules_by_vol[v] for v in vols)
    n = sum(nams_by_vol[v] for v in vols)
    e = sum(ents_by_vol[v] for v in vols)
    c = sum(cits_by_vol[v] for v in vols)
    density = (r + n + e + c) / total if total else 0
    print(f"{gname:12s} {total:6d} {r:5d} {n:5d} {e:5d} {c:5d} {density:6.2f}")

# ===== 3. 找出密度最小的卷 =====
print(f"\n{'='*70}")
print("密度最小的10卷（每层平均覆盖数）")
print(f"{'='*70}")

vol_stats = []
for vol in range(1, 181):
    total = sum(1 for iid in reg if int(iid.split("-")[0]) == vol)
    if total == 0:
        continue
    r = rules_by_vol.get(vol, 0)
    n = nams_by_vol.get(vol, 0)
    e = ents_by_vol.get(vol, 0)
    c = cits_by_vol.get(vol, 0)
    density = (r + n + e + c) / total
    vol_stats.append((vol, total, r, n, e, c, density))

vol_stats.sort(key=lambda x: x[6])

print(f"{'卷':>4s} {'总条目':>6s} {'规则':>5s} {'名录':>5s} {'实体':>5s} {'引用':>5s} {'密度':>6s}")
print("-" * 50)
for vol, total, r, n, e, c, d in vol_stats[:10]:
    print(f"卷{vol:3d} {total:6d} {r:5d} {n:5d} {e:5d} {c:5d} {d:6.2f}")
