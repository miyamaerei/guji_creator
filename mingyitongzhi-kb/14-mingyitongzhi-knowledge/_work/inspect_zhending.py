import json, glob, os
for f in sorted(glob.glob('_data/vol03/*.json')):
    d = json.load(open(f, encoding='utf-8'))
    g = d['layers']['geos'][0]
    print(os.path.basename(f), ':', g['geo_id'], 'parent=', g.get('parent'), 'name=', g.get('name'))
