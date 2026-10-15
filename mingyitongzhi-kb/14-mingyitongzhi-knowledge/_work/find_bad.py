# -*- coding: utf-8 -*-
import json, glob, os

ENT_TYPES = {'geo','person','mtn','site','prod','book','era','dynasty','待定'}

for f in sorted(glob.glob('_data/vol3[2-7]/*.json')):
    data = json.load(open(f, encoding='utf-8'))
    bn = os.path.basename(f)
    for e in data.get('layers', {}).get('ents', []):
        t = e.get('type', '')
        if t not in ENT_TYPES:
            print(f'{bn}: ent {e.get("ent_id")} type={t!r} name={e.get("name")}')
    for ev in data.get('layers', {}).get('evos', []):
        iid = ev.get('item_id', '')
        if iid and not iid[:2] in ('32','33','34','35','36','37'):
            print(f'{bn}: evo {ev.get("evo_id")} item_id={iid!r}')
