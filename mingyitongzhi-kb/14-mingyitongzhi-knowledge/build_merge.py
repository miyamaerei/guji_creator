# -*- coding: utf-8 -*-
"""标准合并器：扫 _data/volNN/*.json，按层聚合到 _layers/。
用法: python build_merge.py            # 全量
      python build_merge.py --vol 19   # 只合卷19
"""
import json, os, glob, sys, shutil
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "_data")
LAYERS = os.path.join(ROOT, "_layers")
DELIVER = os.path.join(ROOT, "_deliver")

LAYER_MAP = {"ents":"ent","geos":"geo","evos":"evo","mtns":"mtn",
             "pers":"per","sites":"site","cits":"cit"}

def main():
    only_vol = None
    if "--vol" in sys.argv:
        only_vol = sys.argv[sys.argv.index("--vol")+1].zfill(2)

    registry = {}
    buckets = defaultdict(list)

    vol_dirs = sorted(glob.glob(os.path.join(DATA, "vol*/")))
    for vd in vol_dirs:
        vol = os.path.basename(vd.rstrip("\\/")).replace("vol","")
        if only_vol and vol != only_vol: continue
        for f in sorted(glob.glob(os.path.join(vd, "*.json"))):
            data = json.load(open(f, encoding="utf-8"))
            iid = data["item_id"]
            registry[iid] = {
                "title": data.get("title") or (data["layers"]["geos"][0]["name"] if data.get("layers",{}).get("geos") else "?"),
                "volume": int(vol),
                "region": data.get("region","?"),
                "type": data.get("type","?"),
            }
            for k, out in LAYER_MAP.items():
                for rec in data.get("layers",{}).get(k, []):
                    if not rec.get("item_id"): rec["item_id"] = iid
                    buckets[out].append(rec)

    # 写 registry
    json.dump(registry, open(os.path.join(ROOT,"_item_registry.json"),"w",encoding="utf-8"),
              ensure_ascii=False, indent=2)
    # 写 layers
    for out, recs in buckets.items():
        d = os.path.join(LAYERS, out)
        os.makedirs(d, exist_ok=True)
        json.dump({"records":recs,"count":len(recs)},
                  open(os.path.join(d,"all.json"),"w",encoding="utf-8"),
                  ensure_ascii=False, indent=2)
    print(f"merged: registry={len(registry)}, layers={ {k:len(v) for k,v in buckets.items()} }")

if __name__ == "__main__":
    main()
