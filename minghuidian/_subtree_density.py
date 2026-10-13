# -*- coding: utf-8 -*-
"""二级树密度分析：大卷组内部各小卷的密度分布"""
import json, os
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))
ents = json.load(open(os.path.join(ROOT, "_layers", "ents.json"), encoding="utf-8"))
cits = json.load(open(os.path.join(ROOT, "_layers", "cits.json"), encoding="utf-8"))
laws = json.load(open(os.path.join(ROOT, "_layers", "laws.json"), encoding="utf-8"))
rituals = json.load(open(os.path.join(ROOT, "_layers", "rituals.json"), encoding="utf-8"))

ents_real = [e for e in ents if not e.get("item_id", "").startswith("VIRT")]

def build_index(data):
    d = defaultdict(list)
    for r in data:
        d[r["item_id"]].append(r)
    return d

idx = {
    "rules": build_index(rules),
    "nams": build_index(nams),
    "ents": build_index(ents_real),
    "cits": build_index(cits),
    "laws": build_index(laws),
    "rituals": build_index(rituals),
}

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

print("=" * 90)
print("二级树密度分析（大卷组内部各小卷）")
print("=" * 90)

for gname, vols in GROUPS:
    print(f"\n{'='*70}")
    print(f"【{gname}】卷 {vols[0]}-{vols[-1]}")
    print(f"{'='*70}")

    vol_data = []
    for vol in vols:
        v_items = [iid for iid in reg if int(iid.split("-")[0]) == vol]
        if not v_items:
            continue

        counts = {}
        for layer, id_map in idx.items():
            counts[layer] = sum(len(id_map[iid]) for iid in v_items)

        total_records = sum(counts.values())
        density = total_records / len(v_items)
        vol_data.append((vol, len(v_items), counts, density))

    # 按密度排序
    vol_data.sort(key=lambda x: x[3])

    # 组内密度统计
    densities = [v[3] for v in vol_data]
    avg = sum(densities) / len(densities) if densities else 0
    mn = min(densities) if densities else 0
    mx = max(densities) if densities else 0

    print(f"  组内密度: 平均{avg:.2f}, 最低{mn:.2f}, 最高{mx:.2f}")
    print(f"  卷数: {len(vol_data)}")
    print()

    # 打印每卷
    print(f"  {'卷':>4s} {'条目':>5s} {'规则':>5s} {'名录':>5s} {'实体':>5s} {'法律':>5s} {'礼仪':>5s} {'密度':>6s}")
    print("  " + "-" * 60)
    for vol, items, counts, d in vol_data:
        bar = "█" * int(d * 5)
        print(f"  卷{vol:3d} {items:5d} {counts['rules']:5d} {counts['nams']:5d} {counts['ents']:5d} {counts['laws']:5d} {counts['rituals']:5d} {d:6.2f} {bar}")

    # 找出异常低的卷（低于组内平均的50%）
    low_vols = [(v, i, c, d) for v, i, c, d in vol_data if d < avg * 0.6]
    if low_vols:
        print(f"\n  ⚠️ 密度异常低（低于组内平均60%）:")
        for vol, items, counts, d in low_vols:
            print(f"    卷{vol}: {items}条, 密度{d:.2f} (组均{avg:.2f})")
            print(f"      → rules={counts['rules']}, nams={counts['nams']}, ents={counts['ents']}")
