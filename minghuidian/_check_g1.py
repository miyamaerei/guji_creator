# -*- coding: utf-8 -*-
import json, os
from collections import defaultdict

reg = json.load(open('_item_registry.json', encoding='utf-8'))
covered = set()
for layer in ['ents', 'rules', 'nams', 'cits']:
    p = f'_layers/{layer}.json'
    if os.path.exists(p):
        for r in json.load(open(p, encoding='utf-8')):
            covered.add(r['item_id'])

vol_items = defaultdict(list)
for iid in reg:
    v = int(iid.split('-')[0])
    if 2 <= v <= 13:
        vol_items[v].append(iid)

print('G1 吏部各卷密度:')
print('  卷  总条数  已覆盖  覆盖率   内容类型(首条)')
total_items = 0
total_cov = 0
for v in sorted(vol_items.keys()):
    items = vol_items[v]
    cov = len([i for i in items if i in covered])
    pct = cov * 100 // len(items) if items else 0
    first = reg[items[0]]['title'][:25]
    print(f'  {v:2d}   {len(items):4d}    {cov:3d}    {pct:3d}%   {first}')
    total_items += len(items)
    total_cov += cov
print(f'\n  合计 {total_items:4d}    {total_cov:3d}    {total_cov*100//total_items:3d}%')
