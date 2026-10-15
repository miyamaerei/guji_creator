# -*- coding: utf-8 -*-
"""明一统志收口：把 pilot/_data 里的试点数据归到标准 _item_registry.json + _layers/ + _deliver/。
范围：卷1-18（北直隶4条 + 真定府1条 + 南直隶15条 = 20 条）。
"""
import json, os, shutil
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")
DELIVER = os.path.join(ROOT, "_deliver")

registry = {}
layer_buckets = defaultdict(list)  # ents/geos/evos/mtns/pers/sites/cits

# ---- 1. 真定府 03-001 ----
zd = json.load(open(os.path.join(ROOT, "pilot/03_zhendingfu.json"), encoding="utf-8"))
registry["03-001"] = {
    "title": "真定府",
    "original": zd["original"],
    "volume": 3,
    "region": "北直隶",
    "type": "prefecture",
}
for k in ["ents","geos","evos","mtns","pers","sites","cits"]:
    layer_buckets[k].extend(zd["layers"].get(k, []))

# ---- 2. 南直隶 15 条 ----
sn = json.load(open(os.path.join(ROOT, "_data/refined_south_zhili.json"), encoding="utf-8"))
for e in sn:
    iid = e["item_id"]
    # 取 name：geos[0].name 或 type
    name = e["layers"]["geos"][0]["name"] if e.get("layers",{}).get("geos") else e.get("type","?")
    registry[iid] = {
        "title": name,
        "original": e.get("source",""),  # 精化版没有 original 全文，用 source
        "volume": int(e["volume"]),
        "region": "南直隶",
        "type": e["type"],
    }
    for k in ["ents","geos","evos","mtns","pers","sites","cits"]:
        layer_buckets[k].extend(e["layers"].get(k, []))

# ---- 3. 北直隶 4 条（早期格式，只进 registry，layers 待补）----
bz = json.load(open(os.path.join(ROOT, "pilot/beizhili_vols1-5.json"), encoding="utf-8"))
for e in bz["entries"]:
    iid = e["item_id"]
    name = e["geo"]["name"] if e.get("geo") else e.get("source","?")
    registry[iid] = {
        "title": name,
        "original": "",  # 早期切片无原文
        "volume": int(e["volume"]),
        "region": "北直隶",
        "type": e["type"],
        "note": "早期格式，layers 待拆分回填",
    }

# ---- 4. 写 registry ----
json.dump(registry, open(os.path.join(ROOT, "_item_registry.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

# ---- 5. 写 _layers/ ----
os.makedirs(LAYERS, exist_ok=True)
layer_files = {
    "ents": "ent", "geos": "geo", "evos": "evo",
    "mtns": "mtn", "pers": "per", "sites": "site", "cits": "cit",
}
for src_key, out_name in layer_files.items():
    recs = layer_buckets[src_key]
    out = os.path.join(LAYERS, f"{out_name}", "all.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({"records": recs, "count": len(recs)}, open(out, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

# ---- 6. 写 _deliver/ ----
os.makedirs(DELIVER, exist_ok=True)
shutil.copy(os.path.join(ROOT, "_item_registry.json"), os.path.join(DELIVER, "_item_registry.json"))
for src_key, out_name in layer_files.items():
    recs = layer_buckets[src_key]
    json.dump({"records": recs, "count": len(recs)},
              open(os.path.join(DELIVER, f"{out_name}.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

# ---- 报告 ----
print("=== 收口结果 ===")
print(f"  registry: {len(registry)} 条")
for iid in sorted(registry.keys()):
    r = registry[iid]
    print(f"    {iid} {r['title']} ({r['region']} 卷{r['volume']})")
print(f"\n  _layers/ 各层:")
for src_key, out_name in layer_files.items():
    print(f"    {out_name}.json: {len(layer_buckets[src_key])} 条")
print(f"\n  _deliver/: {len(os.listdir(DELIVER))} 文件")
