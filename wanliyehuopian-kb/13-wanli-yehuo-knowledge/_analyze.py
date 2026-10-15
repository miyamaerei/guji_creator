# -*- coding: utf-8 -*-
import json, re, os

vols = ['02', '03', '04', '05']
layers = ['ents', 'rules', 'events', 'appts', 'rels', 'cits', 'opns', 'mings', 'tmes', 'regs']

def idfield(rec):
    for k in rec.keys():
        if k.endswith('_id') and k != 'item_id':
            return k
    return None

def lastnum(idv):
    mm = re.findall(r'(\d+)', idv)
    return int(mm[-1]) if mm else 0

for v in vols:
    print('===== VOLUME', v, '=====')
    for L in layers:
        p = f'_layers/{L}/{L}_{v}.json'
        if not os.path.exists(p):
            print(L, 'MISSING'); continue
        d = json.load(open(p, encoding='utf-8'))
        recs = d['records'] if isinstance(d, dict) else d
        key = idfield(recs[0]) if recs else None
        maxn = max((lastnum(r.get(key, '')) for r in recs), default=0) if key else 0
        items = sorted(set(r.get('item_id') for r in recs))
        print(f'{L}: n={len(recs)} key={key} maxseq={maxn} items={items}')

# global ENT max
print('===== ENT IDs across all volumes =====')
allents = []
for f in sorted(os.listdir('_layers/ents')):
    if f.endswith('.json'):
        d = json.load(open('_layers/ents/'+f, encoding='utf-8'))
        recs = d['records'] if isinstance(d, dict) else d
        for r in recs:
            allents.append(r['ent_id'])
nums = sorted(int(re.findall(r'\d+', e)[-1]) for e in allents)
print('count', len(nums), 'min', nums[0], 'max', nums[-1])
print('any >=4000?', [n for n in nums if n >= 4000][:20])
