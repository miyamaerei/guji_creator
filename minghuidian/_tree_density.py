# -*- coding: utf-8 -*-
"""树结构密度：书→大卷组→小卷→条目，每一级都算密度"""
import json, os
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))
ents = json.load(open(os.path.join(ROOT, "_layers", "ents.json"), encoding="utf-8"))
cits = json.load(open(os.path.join(ROOT, "_layers", "cits.json"), encoding="utf-8"))

# 实体里去掉虚拟节点
ents_real = [e for e in ents if not e.get("item_id", "").startswith("VIRT")]

# 按item_id建立映射
def build_index(data):
    d = defaultdict(list)
    for r in data:
        d[r["item_id"]].append(r)
    return d

rules_idx = build_index(rules)
nams_idx = build_index(nams)
ents_idx = build_index(ents_real)
cits_idx = build_index(cits)

# ===== 树结构定义 =====
# L0: 全书
# L1: 大卷组（G0-G8）
# L2: 小卷（1-180）
# L3: 条目（11135）

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

print("=" * 80)
print("树结构密度分析（每一级）")
print("=" * 80)

# ===== L0: 全书 =====
print("\n【L0】全书密度")
total_items = len(reg)
total_rules = len(rules)
total_nams = len(nams)
total_ents = len(ents_real)
total_cits = len(cits)
total_records = total_rules + total_nams + total_ents + total_cits
density = total_records / total_items

print(f"  总条目: {total_items}")
print(f"  总记录: rules={total_rules} + nams={total_nams} + ents={total_ents} + cits={total_cits} = {total_records}")
print(f"  全书密度: {density:.2f} 条记录/条目")

# ===== L1: 大卷组 =====
print("\n【L1】大卷组密度")
print(f"  {'卷组':12s} {'条目数':>6s} {'规则':>5s} {'名录':>5s} {'实体':>5s} {'引用':>5s} {'总记录':>6s} {'密度':>6s}")
print("  " + "-" * 70)

group_stats = []
for gname, vols in GROUPS:
    g_items = [iid for iid in reg if int(iid.split("-")[0]) in vols]
    g_rules = sum(len(rules_idx[iid]) for iid in g_items)
    g_nams = sum(len(nams_idx[iid]) for iid in g_items)
    g_ents = sum(len(ents_idx[iid]) for iid in g_items)
    g_cits = sum(len(cits_idx[iid]) for iid in g_items)
    g_total = g_rules + g_nams + g_ents + g_cits
    g_density = g_total / len(g_items) if g_items else 0
    group_stats.append((gname, len(g_items), g_rules, g_nams, g_ents, g_cits, g_total, g_density))
    print(f"  {gname:12s} {len(g_items):6d} {g_rules:5d} {g_nams:5d} {g_ents:5d} {g_cits:5d} {g_total:6d} {g_density:6.2f}")

# ===== L2: 小卷 =====
print("\n【L2】小卷密度（按密度排序，最稀疏的10卷）")
print(f"  {'卷':>4s} {'条目':>5s} {'规则':>5s} {'名录':>5s} {'实体':>5s} {'引用':>5s} {'密度':>6s}")
print("  " + "-" * 55)

vol_stats = []
for vol in range(1, 181):
    v_items = [iid for iid in reg if int(iid.split("-")[0]) == vol]
    if not v_items:
        continue
    v_rules = sum(len(rules_idx[iid]) for iid in v_items)
    v_nams = sum(len(nams_idx[iid]) for iid in v_items)
    v_ents = sum(len(ents_idx[iid]) for iid in v_items)
    v_cits = sum(len(cits_idx[iid]) for iid in v_items)
    v_total = v_rules + v_nams + v_ents + v_cits
    v_density = v_total / len(v_items)
    vol_stats.append((vol, len(v_items), v_rules, v_nams, v_ents, v_cits, v_density))

vol_stats.sort(key=lambda x: x[6])
for vol, items, r, n, e, c, d in vol_stats[:10]:
    print(f"  卷{vol:3d} {items:5d} {r:5d} {n:5d} {e:5d} {c:5d} {d:6.2f}")

print("\n  --- 最密集的10卷 ---")
for vol, items, r, n, e, c, d in vol_stats[-10:]:
    print(f"  卷{vol:3d} {items:5d} {r:5d} {n:5d} {e:5d} {c:5d} {d:6.2f}")

# ===== L3: 条目级密度分布 =====
print("\n【L3】条目级密度分布（每条有几层覆盖）")
layer_count_dist = Counter()
for iid in reg:
    layers = 0
    if rules_idx[iid]: layers += 1
    if nams_idx[iid]: layers += 1
    if ents_idx[iid]: layers += 1
    if cits_idx[iid]: layers += 1
    layer_count_dist[layers] += 1

for k in sorted(layer_count_dist.keys()):
    cnt = layer_count_dist[k]
    pct = cnt * 100 // total_items
    bar = "█" * pct // 2
    print(f"  {k}层: {cnt:5d} 条 ({pct:3d}%) {bar}")

# ===== 找出密度异常低的节点 =====
print("\n" + "=" * 80)
print("密度异常低的节点清单")
print("=" * 80)

# 大卷组里密度低于1.1的
print("\n大卷组密度 < 1.1 的：")
for gname, items, r, n, e, c, total, d in group_stats:
    if d < 1.1:
        print(f"  ⚠️ {gname}: 密度 {d:.2f}（只有{r}规则+{n}名录，缺乏实体层）")

# 小卷里密度低于0.8的
print("\n小卷密度 < 0.8 的：")
low_vols = [(v, i, r, n, e, c, d) for v, i, r, n, e, c, d in vol_stats if d < 0.8]
print(f"  共 {len(low_vols)} 卷")
for vol, items, r, n, e, c, d in low_vols[:10]:
    print(f"    卷{vol}: {items}条, 密度{d:.2f} (rules={r}, nams={n})")
