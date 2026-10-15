# -*- coding: utf-8 -*-
"""One-shot fix: registry titles + 05-002 + geo dangling refs."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# 1. Fix registry
reg = json.load(open('_item_registry.json', encoding='utf-8'))
fixes = {
    '32-001': '西安府',
    '34-001': '凤翔府',
    '34-002': '汉中府',
    '35-001': '平凉府',
    '35-002': '巩昌府',
    '36-001': '临洮府',
    '36-002': '庆阳府',
    '36-003': '延安府',
    '37-001': '宁夏卫',
    '37-002': '宁夏中卫',
    '37-003': '洮州卫军民指挥使司',
    '37-004': '岷州卫军民指挥使司',
    '37-005': '河州卫军民指挥使司',
    '37-006': '靖虏卫',
    '37-007': '陕西行都指挥使司',
    '38-001': '杭州府',
}
for iid, title in fixes.items():
    if iid in reg:
        reg[iid]['title'] = title
# Add 05-002 永宁县 if missing
if '05-002' not in reg:
    reg['05-002'] = {'title': '永宁县', 'volume': 5, 'region': '北直隶', 'type': 'county'}
json.dump(reg, open('_item_registry.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'registry: {len(reg)} entries')

# 2. Fix geo layer
geo_path = '_layers/geo/all.json'
geo_data = json.load(open(geo_path, encoding='utf-8'))
recs = geo_data['records']

# Fix 长垣县 parent
for g in recs:
    if g['geo_id'] == 'GEO-04003-c10':
        g['parent'] = 'GEO-04003'
        print('fixed 长垣县 parent -> GEO-04003')

# Add GEO-05002 if missing
if not any(g['geo_id'] == 'GEO-05002' for g in recs):
    recs.append({
        'geo_id': 'GEO-05002',
        'item_id': '05-002',
        'name': '永宁县',
        'type': 'county',
        'region': '北直隶',
        'parent': 'GEO-000',
        'children': ['GEO-05002-c01'],
        'volume_range': '卷5',
        'attributes': {}
    })
    print('added GEO-05002 永宁县')

geo_data['count'] = len(recs)
json.dump(geo_data, open(geo_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'geo: {len(recs)} nodes')
