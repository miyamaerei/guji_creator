# -*- coding: utf-8 -*-
"""三级树密度：按卷统计"""
import json, os
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

layers = {}
for layer in ["rules", "nams", "ents", "cits", "laws", "rituals", "geo", "org_events", "offices", "materials", "inspect", "dress", "foreign"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        layers[layer] = json.load(open(p, encoding="utf-8"))
    else:
        layers[layer] = []

layers["ents"] = [e for e in layers["ents"] if not e.get("item_id", "").startswith("VIRT")]

def build_index(data):
    d = defaultdict(list)
    for r in data:
        d[r["item_id"]].append(r)
    return d

idx = {layer: build_index(data) for layer, data in layers.items()}

# 按卷统计
vol_stats = defaultdict(lambda: {"items": 0, "records": 0, "layers": Counter()})

for iid in reg:
    vol = int(iid.split("-")[0])
    vol_stats[vol]["items"] += 1

    for layer in layers:
        cnt = len(idx[layer][iid])
        vol_stats[vol]["records"] += cnt
        if cnt > 0:
            vol_stats[vol]["layers"][layer] += 1

# 按大卷组分组显示
GROUPS = [
    ("G0 宗人府", [1]),
    ("G1 吏部", list(range(2, 14))),
    ("G2 户部", list(range(14, 42))),
    ("G3 礼部", list(range(42, 106))),
    ("G4 兵部", list(range(106, 130))),
    ("G5 刑部", list(range(130, 146))),
    ("G6 工部", list(range(146, 164))),
    ("G7 诸文职", list(range(164, 179))),
    ("G8 诸武职", [179, 180]),
]

print("=" * 80)
print("三级树密度（卷级）")
print("=" * 80)

for gname, vols in GROUPS:
    g_items = sum(vol_stats[v]["items"] for v in vols if v in vol_stats)
    g_records = sum(vol_stats[v]["records"] for v in vols if v in vol_stats)
    g_density = g_records / g_items if g_items else 0

    print(f"\n【{gname}】 组均密度 {g_density:.2f}")
    print(f"  {'卷':>4s} {'条目':>5s} {'记录':>6s} {'密度':>6s} {'主要层'}")
    print("  " + "-" * 70)

    for vol in vols:
        if vol not in vol_stats:
            continue
        s = vol_stats[vol]
        d = s["records"] / s["items"] if s["items"] else 0

        # 主要层（top3）
        top_layers = s["layers"].most_common(3)
        main = ", ".join(f"{l[:5]}({c})" for l, c in top_layers)

        # 标记低密度
        mark = ""
        if d < 1.0:
            mark = " ❌"
        elif d < 1.2:
            mark = " ⚠️"
        elif d > 2.0:
            mark = " ⭐"

        print(f"  卷{vol:3d}: {s['items']:5d} {s['records']:6d} {d:6.2f}  {main}{mark}")
