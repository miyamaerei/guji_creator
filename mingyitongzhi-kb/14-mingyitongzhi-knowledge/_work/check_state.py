# -*- coding: utf-8 -*-
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

for layer in ['ent','geo','evo','mtn','per','site','cit']:
    d = json.load(open(f'_layers/{layer}/all.json', encoding='utf-8'))
    print(f'{layer}: {len(d["records"])} records')

ent = json.load(open('_layers/ent/all.json', encoding='utf-8'))['records']
for iid in ['06-002', '20-001', '88-001', '38-001', '32-001']:
    n = sum(1 for r in ent if r.get('item_id') == iid)
    print(f'ent item_id={iid}: {n}')

geo = json.load(open('_layers/geo/all.json', encoding='utf-8'))['records']
for gid in ['GEO-04003-c10', 'GEO-05002', 'GEO-05002-c01']:
    found = [g for g in geo if g['geo_id'] == gid]
    print(f'geo {gid}: {"FOUND parent="+found[0].get("parent","?") if found else "MISSING"}')
