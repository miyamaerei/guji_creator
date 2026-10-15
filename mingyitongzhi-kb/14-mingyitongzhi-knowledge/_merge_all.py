# -*- coding: utf-8 -*-
"""通用增量合并：扫 _data/volNN/*.json，追加进现有 _layers/。"""
import json, os, glob, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")
DATA = os.path.join(ROOT, "_data")
LAYER_MAP = {"ents":"ent","geos":"geo","evos":"evo","mtns":"mtn","pers":"per","sites":"site","cits":"cit"}

reg_path = os.path.join(ROOT,"_item_registry.json")
registry = json.load(open(reg_path,encoding="utf-8"))
layers_now = {out: json.load(open(os.path.join(LAYERS,out,"all.json"),encoding="utf-8"))["records"]
              for out in ["ent","geo","evo","mtn","per","site","cit"]}
existing_geo = {r["geo_id"] for r in layers_now["geo"]}

added_reg = 0; added_layer = {k:0 for k in LAYER_MAP.values()}
for vol_dir in sorted(glob.glob(os.path.join(DATA,"vol*/"))):
    for f in sorted(glob.glob(os.path.join(vol_dir,"*.json"))):
        base = os.path.basename(f)
        try: d = json.load(open(f,encoding="utf-8"))
        except: continue
        iid = d["item_id"]
        # 府级文件（不 cXX/sXX）才进 registry
        parts = base.split("_")
        is_sub = len(parts) >= 3 and (parts[1].startswith("c") or parts[1].startswith("s"))
        if not is_sub and iid not in registry:
            geo0 = d.get("layers",{}).get("geos",[{}])[0] if d.get("layers",{}).get("geos") else {}
            volnum = os.path.basename(vol_dir.rstrip("\\/")).replace("vol","")
            try: volnum = int(volnum)
            except: volnum = 0
            registry[iid] = {"title":geo0.get("name",base.split("_",1)[1].replace(".json","")[:8]),
                             "volume":volnum,
                             "region":d.get("region","?"),"type":geo0.get("type","?")}
            added_reg += 1
        for k,out in LAYER_MAP.items():
            for rec in d.get("layers",{}).get(k,[]):
                if not rec.get("item_id"): rec["item_id"] = iid
                # geo 层去重
                if out == "geo":
                    gid = rec.get("geo_id")
                    if gid in existing_geo: continue
                    existing_geo.add(gid)
                layers_now[out].append(rec); added_layer[out] += 1

# 修 GEO-SHANDONG
for r in layers_now["geo"]:
    if r.get("parent") == "GEO-SHANDONG": r["parent"] = "GEO-000"

json.dump(registry, open(reg_path,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
for out,recs in layers_now.items():
    json.dump({"records":recs,"count":len(recs)}, open(os.path.join(LAYERS,out,"all.json"),"w",encoding="utf-8"),
              ensure_ascii=False, indent=2)
print(f"+registry {added_reg}, total {len(registry)}")
print(f"+layers: {added_layer}")
print(f"total: { {k:len(v) for k,v in layers_now.items()} }")

# 源文件完整性警告：registry 有条目但 _data/volNN/ 下无源文件
scanned_iids = set()
for vol_dir in sorted(glob.glob(os.path.join(DATA,"vol*/"))):
    for f in sorted(glob.glob(os.path.join(vol_dir,"*.json"))):
        base = os.path.basename(f)
        parts = base.split("_")
        if len(parts) >= 2:
            scanned_iids.add(parts[0])
missing = [iid for iid in registry if iid not in scanned_iids]
if missing:
    print(f"⚠️  WARNING: {len(missing)} 条 registry 条目无 _data/volNN/ 源文件: {missing}")
    print(f"   这些条目重建后会变成 0 层占位，必须拆分源文件入 volNN/ 目录")
