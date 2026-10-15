# -*- coding: utf-8 -*-
"""明一统志收口 v2：修 item_id 注入。"""
import json, os, shutil
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")
DELIVER = os.path.join(ROOT, "_deliver")

registry = {}
layer_buckets = defaultdict(list)

# ---- 1. 真定府 03-001 ----
zd = json.load(open(os.path.join(ROOT, "pilot/03_zhendingfu.json"), encoding="utf-8"))
registry["03-001"] = {"title":"真定府","original":zd["original"],"volume":3,"region":"北直隶","type":"prefecture"}
for k in ["ents","geos","evos","mtns","pers","sites","cits"]:
    for rec in zd["layers"].get(k, []):
        rec.setdefault("item_id", "03-001")  # 补 item_id
        layer_buckets[k].append(rec)

# ---- 2. 南直隶 15 条（mtn/site 英文枚举→中文）----
MTN_EN2CN = {"mountain":"山","ridge":"岭","peak":"峰","hill":"冈","cliff":"岩","cave":"洞",
             "spring":"泉","stream":"溪","river":"河","water":"水","lake":"湖","pool":"潭",
             "pond":"池","weir":"堰","pass":"关","bridge":"桥","well":"井"}
SITE_EN2CN = {"palace":"宫室","temple":"寺观","shrine":"祠庙","tomb":"陵墓","ruins":"古迹",
              "school":"学校","academy":"书院","altar":"坛庙","city_wall":"城池","garden":"苑囿",
              "bridge":"关梁"}
sn = json.load(open(os.path.join(ROOT, "_data/refined_south_zhili.json"), encoding="utf-8"))
for e in sn:
    iid = e["item_id"]
    name = e["layers"]["geos"][0]["name"] if e.get("layers",{}).get("geos") else e.get("type","?")
    registry[iid] = {"title":name,"original":e.get("source",""),"volume":int(e["volume"]),"region":"南直隶","type":e["type"]}
    for k in ["ents","geos","evos","mtns","pers","sites","cits"]:
        for rec in e["layers"].get(k, []):
            if not rec.get("item_id"):
                rec["item_id"] = iid
            # 英文枚举→中文
            if k == "mtns" and rec.get("type") in MTN_EN2CN:
                rec["type"] = MTN_EN2CN[rec["type"]]
            if k == "sites" and rec.get("type") in SITE_EN2CN:
                rec["type"] = SITE_EN2CN[rec["type"]]
            layer_buckets[k].append(rec)

# ---- 2.5 山西 8 条 ----
sx = json.load(open(os.path.join(ROOT, "_data/shanxi_vols19-21.json"), encoding="utf-8"))
for e in sx:
    iid = e["item_id"]
    name = e["layers"]["geos"][0]["name"] if e.get("layers",{}).get("geos") else "?"
    registry[iid] = {"title":name,"original":e.get("source",""),"volume":int(e["volume"]),"region":"山西","type":e["type"]}
    for k in ["ents","geos","evos","mtns","pers","sites","cits"]:
        for rec in e["layers"].get(k, []):
            if not rec.get("item_id"):
                rec["item_id"] = iid
            layer_buckets[k].append(rec)

# ---- 3. 北直隶 4 条（只进 registry）----
bz = json.load(open(os.path.join(ROOT, "pilot/beizhili_vols1-5.json"), encoding="utf-8"))
for e in bz["entries"]:
    iid = e["item_id"]
    name = e["geo"]["name"] if e.get("geo") else e.get("source","?")
    registry[iid] = {"title":name,"original":"","volume":int(e["volume"]),"region":"北直隶","type":e["type"],"note":"早期格式，layers 待拆分回填"}

# ---- 写盘 ----
json.dump(registry, open(os.path.join(ROOT,"_item_registry.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=2)
os.makedirs(LAYERS, exist_ok=True)
os.makedirs(DELIVER, exist_ok=True)
mapping = {"ents":"ent","geos":"geo","evos":"evo","mtns":"mtn","pers":"per","sites":"site","cits":"cit"}
for src, out in mapping.items():
    recs = layer_buckets[src]
    for d in [os.path.join(LAYERS,out), DELIVER]:
        os.makedirs(d, exist_ok=True)
        fname = f"{out}.json" if d==DELIVER else "all.json"
        json.dump({"records":recs,"count":len(recs)},
                  open(os.path.join(d,fname),"w",encoding="utf-8"),
                  ensure_ascii=False, indent=2)
shutil.copy(os.path.join(ROOT,"_item_registry.json"), os.path.join(DELIVER,"_item_registry.json"))

print(f"registry: {len(registry)} 条")
for src, out in mapping.items():
    print(f"  {out}: {len(layer_buckets[src])} 条")
