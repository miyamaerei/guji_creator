# -*- coding: utf-8 -*-
"""查看卷72内容"""
import json
reg = json.load(open('_item_registry.json', encoding='utf-8'))
covered = set()
import os
for layer in ['ents', 'rules', 'nams', 'cits']:
    p = f'_layers/{layer}.json'
    if os.path.exists(p):
        for r in json.load(open(p, encoding='utf-8')):
            covered.add(r['item_id'])
uncov = [iid for iid in sorted(reg) if int(iid.split('-')[0]) == 72 and iid not in covered]
print(f'卷72 未覆盖 {len(uncov)} 条:')
for iid in uncov[:15]:
    print(f'  {iid}: [{reg[iid]["title"][:40]}]')
