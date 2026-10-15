# -*- coding: utf-8 -*-
"""Assemble vol22 JSON files."""
import json, os, sys, pickle

WORK = os.path.dirname(os.path.abspath(__file__))
OUT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol22"
sys.path.insert(0, WORK)

from vol22_mtns import MTNS
from vol22_sites import SITES
from vol22_pers import PERS

with open(os.path.join(OUT, "_skeleton.pkl"), "rb") as f:
    skel = pickle.load(f)

geos = skel["geos"]
evos = skel["evos"]
cits = skel["cits"]
ents = skel["ents"]
counties = skel["counties"]
subprefectures = skel["subprefectures"]

ITEM = "22-001"
VOL = "卷22"
REGION = "山东"

# Build county name -> geo_id map
county_geo_map = {}
county_name_map = {}
for suf, name, parent, loc, hc, hn in counties:
    cid = "GEO-22001-" + suf
    county_geo_map[name] = cid
    county_name_map[cid] = name

# Subprefecture geo map
sp_geo_map = {}
for suf, name, parent, loc, hc, hn, kids in subprefectures:
    sp_geo_map[name] = "GEO-22001-" + suf

# ========== Split MTNS by geo_id ==========
# geo_id -> list of mtn records
mtn_by_geo = {}
mtn_all_pref = []  # prefecture + subprefecture level
for i, (name, mtype, gid, loc, desc, lore) in enumerate(MTNS):
    rec = {
        "mtn_id": f"MTN-{i+1:03d}",
        "item_id": ITEM,
        "geo_id": gid,
        "name": name,
        "type": mtype,
        "location_text": loc,
        "description": desc,
        "lore": lore,
    }
    mtn_by_geo.setdefault(gid, []).append(rec)
    # prefecture file includes mtns at GEO-22001, s01-s04 (subprefectures have no own file)
    if gid.startswith("GEO-22001-s") or gid == "GEO-22001":
        mtn_all_pref.append(rec)

# ========== Split SITES by geo_id ==========
site_by_geo = {}
site_all_pref = []
for i, (name, stype, gid, loc, lore) in enumerate(SITES):
    rec = {
        "site_id": f"SITE-{i+1:03d}",
        "item_id": ITEM,
        "geo_id": gid,
        "name": name,
        "type": stype,
        "location_text": loc,
        "history_lore": lore,
    }
    site_by_geo.setdefault(gid, []).append(rec)
    if gid.startswith("GEO-22001-s") or gid == "GEO-22001":
        site_all_pref.append(rec)

# ========== PER: all stay in prefecture file ==========
pers_all = []
for i, (name, ptype, dyn, np, off, summ) in enumerate(PERS):
    pers_all.append({
        "per_id": f"PER-{i+1:03d}",
        "item_id": ITEM,
        "geo_id": "GEO-22001",
        "name": name,
        "type": ptype,
        "dynasty": dyn,
        "native_place": np,
        "office": off,
        "summary": summ,
    })

# ========== Build prefecture file (skeleton: ents/geos/evos/mtns/cits; sites & pers split out) ==========
pref = {
    "item_id": ITEM,
    "volume": "22",
    "source": "济南府",
    "region": REGION,
    "layers": {
        "ents": ents,
        "geos": geos,
        "evos": evos,
        "mtns": mtn_all_pref,
        "pers": [],
        "sites": [],
        "prods": [],
        "cits": cits,
    },
    "layer_count": 7,
    "validation": {
        "errs": [],
        "gap": 0,
        "notes": "sites 层拆至 22-001_济南府_sites.json；pers 层拆至 22-001_济南府_pers1_名宦.json 与 22-001_济南府_pers2_人物列女仙释.json；prods 空数组"
    }
}

pref_path = os.path.join(OUT, "22-001_济南府.json")
with open(pref_path, "w", encoding="utf-8") as f:
    json.dump(pref, f, ensure_ascii=False, indent=1)
pref_size = os.path.getsize(pref_path)
print(f"prefecture file: {pref_size/1024:.1f}KB")

# sites split file
sites_file = {
    "item_id": ITEM,
    "volume": "22",
    "source": "济南府-古迹建筑层",
    "region": REGION,
    "layers": {
        "ents": [], "geos": [], "evos": [], "mtns": [],
        "pers": [], "sites": site_all_pref, "prods": [], "cits": [],
    },
    "layer_count": 1,
}
sites_path = os.path.join(OUT, "22-001_济南府_sites.json")
with open(sites_path, "w", encoding="utf-8") as f:
    json.dump(sites_file, f, ensure_ascii=False, indent=1)
print(f"sites split file: {os.path.getsize(sites_path)/1024:.1f}KB")

# pers split: 名宦 / 人物 / 列女仙释
pers_groups = [
    ([p for p in pers_all if p["type"] == "名宦"], "22-001_济南府_pers1_名宦.json"),
    ([p for p in pers_all if p["type"] == "人物"], "22-001_济南府_pers2_人物.json"),
    ([p for p in pers_all if p["type"] in ("流寓","列女","仙释")], "22-001_济南府_pers3_流寓列女仙释.json"),
]
for plist, fname in pers_groups:
    pf = {
        "item_id": ITEM,
        "volume": "22",
        "source": f"济南府-人物层",
        "region": REGION,
        "layers": {
            "ents": [], "geos": [], "evos": [], "mtns": [],
            "pers": plist, "sites": [], "prods": [], "cits": [],
        },
        "layer_count": 1,
    }
    pp = os.path.join(OUT, fname)
    with open(pp, "w", encoding="utf-8") as f:
        json.dump(pf, f, ensure_ascii=False, indent=1)
    print(f"pers split {fname}: {os.path.getsize(pp)/1024:.1f}KB ({len(plist)} records)")

# ========== Build county files ==========
county_files = []
for suf, name, parent, loc, hc, hn in counties:
    cid = "GEO-22001-" + suf
    # find the geo node for this county
    cgeo = [g for g in geos if g["geo_id"] == cid][0]
    cm = mtn_by_geo.get(cid, [])
    cs = site_by_geo.get(cid, [])
    cfile = {
        "item_id": ITEM,
        "volume": "22",
        "source": name,
        "region": REGION,
        "layers": {
            "ents": [{"ent_id": f"ENT-{suf}", "name": name, "type": "geo", "norm": name, "first_source": ITEM}],
            "geos": [cgeo],
            "evos": [],
            "mtns": cm,
            "pers": [],
            "sites": cs,
            "prods": [],
            "cits": [],
        },
        "layer_count": 7,
    }
    fname = f"22-001_{suf}_{name}.json"
    fpath = os.path.join(OUT, fname)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(cfile, f, ensure_ascii=False, indent=1)
    sz = os.path.getsize(fpath)
    county_files.append((fname, sz, len(cm), len(cs)))
    print(f"  {fname}: {sz/1024:.1f}KB, mtns={len(cm)}, sites={len(cs)}")

# cleanup pkl
os.remove(os.path.join(OUT, "_skeleton.pkl"))

print("\n=== Summary ===")
print(f"Prefecture: {len(geos)} geos, {len(evos)} evos, {len(mtn_all_pref)} mtns, {len(pers_all)} pers, {len(site_all_pref)} sites, {len(cits)} cits, {len(ents)} ents")
print(f"County files: {len(county_files)}")
