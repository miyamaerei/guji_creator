# -*- coding: utf-8 -*-
"""Validate vol22 output."""
import json, os, glob

OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol22"

files = sorted(glob.glob(os.path.join(OUT, "*.json")))
print(f"Total files: {len(files)}")

# Whitelists
GEO_TYPES = {"metro","prefecture","department","subprefecture","county","tusi","weisuo","foreign","other"}
PER_TYPES = {"名宦","流寓","人物","列女","仙释","其他"}
MTN_TYPES = {"山","岭","峰","冈","岩","洞","泉","溪","江","河","湖","潭","池","堰","关","桥","井","其他"}
SITE_TYPES = {"寺观","祠庙","陵墓","古迹","宫室","学校","书院","坛庙","城池","苑囿","关梁","其他"}
EVO_ACTIONS = {"置","废","改","并","复","因之","升","降","迁","未明","置郡","复置","迁治"}
CIT_CONTEXTS = {"立论","证俗","考源","补遗","其他"}
DYNASTIES = {"秦","汉","三国","晋","南北朝","隋","唐","五代","宋","金","元","明","未明","春秋战国","周"}

all_geo_ids = set()
all_errors = []
all_warnings = []
layer_counts = {}

for fp in files:
    with open(fp, encoding="utf-8") as f:
        data = json.load(f)
    layers = data.get("layers", {})
    fname = os.path.basename(fp)

    # Check geos
    for g in layers.get("geos", []):
        gid = g["geo_id"]
        if gid in all_geo_ids:
            all_errors.append(f"DUPLICATE geo_id: {gid} in {fname}")
        all_geo_ids.add(gid)
        if g["type"] not in GEO_TYPES:
            all_errors.append(f"BAD geo type '{g['type']}' for {gid} in {fname}")
        # parent must be a geo_id string
        par = g.get("parent", "")
        if par and not par.startswith("GEO-"):
            all_errors.append(f"BAD parent '{par}' (not geo_id) for {gid} in {fname}")
        # check children later

    # Check evos
    for e in layers.get("evos", []):
        if e.get("dynasty") and e["dynasty"] not in DYNASTIES:
            all_warnings.append(f"EV0 dynasty '{e['dynasty']}' not in whitelist ({e.get('institution_name')})")
        if e.get("action") and e["action"] not in EVO_ACTIONS:
            all_warnings.append(f"EV0 action '{e['action']}' not in whitelist ({e.get('institution_name')})")

    # Check mtns
    for m in layers.get("mtns", []):
        if m["type"] not in MTN_TYPES:
            all_warnings.append(f"MTN type '{m['type']}' not in whitelist ({m['name']})")

    # Check pers
    for p in layers.get("pers", []):
        if p["type"] not in PER_TYPES:
            all_errors.append(f"PER type '{p['type']}' not in whitelist ({p['name']})")

    # Check sites
    for s in layers.get("sites", []):
        if s["type"] not in SITE_TYPES:
            all_warnings.append(f"SITE type '{s['type']}' not in whitelist ({s['name']})")

    # Check cits
    for c in layers.get("cits", []):
        if c.get("context") and c["context"] not in CIT_CONTEXTS:
            all_warnings.append(f"CIT context '{c['context']}' not in whitelist ({c['cited_work']})")

    layer_counts[fname] = {
        "ents": len(layers.get("ents",[])),
        "geos": len(layers.get("geos",[])),
        "evos": len(layers.get("evos",[])),
        "mtns": len(layers.get("mtns",[])),
        "pers": len(layers.get("pers",[])),
        "sites": len(layers.get("sites",[])),
        "prods": len(layers.get("prods",[])),
        "cits": len(layers.get("cits",[])),
    }

# Second pass: check children/parent references
for fp in files:
    with open(fp, encoding="utf-8") as f:
        data = json.load(f)
    layers = data.get("layers", {})
    fname = os.path.basename(fp)
    for g in layers.get("geos", []):
        for ch in g.get("children", []):
            if ch not in all_geo_ids:
                all_errors.append(f"DANGLING child ref: {ch} (child of {g['geo_id']}) not in any geos array, in {fname}")
        par = g.get("parent","")
        if par and par != "GEO-000" and par not in all_geo_ids:
            all_errors.append(f"DANGLING parent ref: {par} (parent of {g['geo_id']}) not found, in {fname}")

print(f"\n=== ERRORS ({len(all_errors)}) ===")
for e in all_errors:
    print(f"  ERR: {e}")
print(f"\n=== WARNINGS ({len(all_warnings)}) ===")
for w in all_warnings[:30]:
    print(f"  WARN: {w}")
if len(all_warnings) > 30:
    print(f"  ... and {len(all_warnings)-30} more")

print(f"\n=== GEO nodes: {len(all_geo_ids)} ===")
print(f"=== File layer counts ===")
for fn, lc in sorted(layer_counts.items()):
    print(f"  {fn}: ents={lc['ents']} geos={lc['geos']} evos={lc['evos']} mtns={lc['mtns']} pers={lc['pers']} sites={lc['sites']} cits={lc['cits']}")
