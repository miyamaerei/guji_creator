import json
for f in ['02-002_c11_吴桥县.json','02-002_c14_南皮县.json','02-002_c01_河间县.json']:
    d = json.load(open(f'_data/vol02/{f}', encoding='utf-8'))
    g = d['layers']['geos'][0]
    print(f, ':', g['geo_id'], 'parent=', g.get('parent'), 'children=', g.get('children', []))
