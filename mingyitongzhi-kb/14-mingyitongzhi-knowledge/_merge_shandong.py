# -*- coding: utf-8 -*-
"""增量合并：把 _data/volNN/*.json 追加进现有 _layers/（不覆盖老数据）。"""
import json, os, glob, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")
DATA = os.path.join(ROOT, "_data")

LAYER_MAP = {"ents":"ent","geos":"geo","evos":"evo","mtns":"mtn",
             "pers":"per","sites":"site","cits":"cit"}

# 加载现有
reg_path = os.path.join(ROOT,"_item_registry.json")
registry = json.load(open(reg_path,encoding="utf-8"))

layers_now = {}
for out in ["ent","geo","evo","mtn","per","site","cit"]:
    p = os.path.join(LAYERS,out,"all.json")
    layers_now[out] = json.load(open(p,encoding="utf-8"))["records"]

# 扫 vol22-25
added_reg = 0
added_layer = {k:0 for k in LAYER_MAP.values()}
for vol in ["vol22","vol23","vol24","vol25"]:
    for f in sorted(glob.glob(os.path.join(DATA,vol,"*.json"))):
        d = json.load(open(f,encoding="utf-8"))
        iid = d["item_id"]
        # 县文件 item_id 是父府号 (22-001)，不重复加 registry
        # 只有府级文件（文件名不含 _cXX_/_sXX_）才进 registry
        base = os.path.basename(f)
        is_county = "_c" in base.split("_",1)[1][:4] or "_s" in base.split("_",1)[1][:4]
        if not is_county and iid not in registry:
            geo0 = d["layers"]["geos"][0] if d.get("layers",{}).get("geos") else {}
            registry[iid] = {
                "title": geo0.get("name", base.split("_",1)[1].replace(".json","")),
                "volume": int(vol.replace("vol","")),
                "region": d.get("region","山东"),
                "type": d.get("type", geo0.get("type","?")),
            }
            added_reg += 1
        # 各层追加
        for k, out in LAYER_MAP.items():
            for rec in d.get("layers",{}).get(k,[]):
                if not rec.get("item_id"): rec["item_id"] = iid
                layers_now[out].append(rec)
                added_layer[out] += 1

# 写回
json.dump(registry, open(reg_path,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
for out, recs in layers_now.items():
    d = os.path.join(LAYERS,out)
    json.dump({"records":recs,"count":len(recs)},
              open(os.path.join(d,"all.json"),"w",encoding="utf-8"),
              ensure_ascii=False, indent=2)

print(f"+registry {added_reg}, total {len(registry)}")
print(f"+layers: {added_layer}")
print(f"total layers: { {k:len(v) for k,v in layers_now.items()} }")
