# -*- coding: utf-8 -*-
"""跨层索引 + 全量打包输出。"""
import json, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")
DELIVER = os.path.join(ROOT, "_deliver")
os.makedirs(DELIVER, exist_ok=True)

# 加载所有层
layers = {}
for name in ["ent", "geo", "evo", "mtn", "per", "site", "cit"]:
    p = os.path.join(LAYERS, name, "all.json")
    d = json.load(open(p, encoding="utf-8"))
    layers[name] = d["records"]
    print(f"{name}: {len(layers[name])} 条")

# === 1. 建 GEO 索引 ===
geo_by_id = {g["geo_id"]: g for g in layers["geo"]}
print(f"\nGEO 节点: {len(geo_by_id)}")

# === 2. 建 GEO 树（parent -> children）===
children_map = defaultdict(list)
roots = []
for g in layers["geo"]:
    pid = g.get("parent")
    if pid and pid in geo_by_id:
        children_map[pid].append(g["geo_id"])
    else:
        roots.append(g["geo_id"])

# 给每个 geo 节点补上 children 列表
for g in layers["geo"]:
    g["children"] = children_map.get(g["geo_id"], [])

print(f"GEO 根节点: {len(roots)}")

# === 3. 计算每个 geo 节点的跨层计数 ===
geo_counts = defaultdict(lambda: {"mtn": 0, "per": 0, "site": 0, "evo": 0, "ent": 0, "cit": 0})
for m in layers["mtn"]:
    gid = m.get("geo_id")
    if gid:
        geo_counts[gid]["mtn"] += 1
for p in layers["per"]:
    gid = p.get("geo_id")
    if gid:
        geo_counts[gid]["per"] += 1
for s in layers["site"]:
    gid = s.get("geo_id")
    if gid:
        geo_counts[gid]["site"] += 1
for e in layers["evo"]:
    gid = e.get("geo_id")
    if gid:
        geo_counts[gid]["evo"] += 1
for c in layers["cit"]:
    gid = c.get("geo_id")
    if gid:
        geo_counts[gid]["cit"] += 1

# 给 geo 节点加上 counts 字段
for g in layers["geo"]:
    g["counts"] = geo_counts.get(g["geo_id"], {})

# === 4. 输出 GEO 树（按 region 分组）===
by_region = defaultdict(list)
for g in layers["geo"]:
    region = g.get("region", "未知")
    by_region[region].append(g)

geo_tree_out = {
    "meta": {"total_nodes": len(layers["geo"]), "regions": list(by_region.keys())},
    "regions": {}
}
for region, nodes in by_region.items():
    geo_tree_out["regions"][region] = {
        "count": len(nodes),
        "nodes": nodes
    }

json.dump(geo_tree_out, open(os.path.join(DELIVER, "geo_tree.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print(f"\ngeo_tree.json 已输出: {len(layers['geo'])} 节点, {len(by_region)} 区域")

# === 5. 输出全量合并包 ===
full_pack = {
    "meta": {
        "book": "大明一统志",
        "layers": {k: len(v) for k, v in layers.items()},
        "geo_regions": len(by_region)
    },
    "layers": layers
}
json.dump(full_pack, open(os.path.join(DELIVER, "full_kb.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print(f"full_kb.json 已输出")

# === 6. 输出统计摘要 ===
summary = {
    "总条目数": {k: len(v) for k, v in layers.items()},
    "GEO 节点数": len(layers["geo"]),
    "布政司/区域数": len(by_region),
    "各区域 GEO 数": {r: len(n) for r, n in by_region.items()},
    "各类型 GEO 数": dict(Counter = defaultdict(int))
}
type_count = defaultdict(int)
for g in layers["geo"]:
    type_count[g["type"]] += 1
summary["各类型 GEO 数"] = dict(type_count)

json.dump(summary, open(os.path.join(DELIVER, "summary.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print(f"summary.json 已输出")
print("\n=== 完成 ===")
