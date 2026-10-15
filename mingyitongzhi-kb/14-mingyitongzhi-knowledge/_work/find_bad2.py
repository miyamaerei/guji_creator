# -*- coding: utf-8 -*-
import json, glob, os

for f in sorted(glob.glob('_data/vol3[2-7]/*.json')):
    data = json.load(open(f, encoding='utf-8'))
    bn = os.path.basename(f)
    iid = data.get('item_id', '')
    for ev in data.get('layers', {}).get('evos', []):
        ev_iid = ev.get('item_id', '')
        if ev_iid and ev_iid != iid:
            print(f'{bn}: evo {ev.get("evo_id")} file_iid={iid} evo_iid={ev_iid!r}')
