import json, glob, os

# Check which file for each item overwrites the registry title
for item_id, vol in [('32-001','32'),('34-001','34'),('37-007','37')]:
    files = sorted(glob.glob(f'_data/vol{vol}/{item_id}_*.json'))
    print(f'\n=== {item_id} ({len(files)} files) ===')
    for f in files:
        d = json.load(open(f, encoding='utf-8'))
        title = d.get('title', None)
        geos = d['layers'].get('geos', [])
        g0 = geos[0]['name'] if geos else 'EMPTY'
        fname = os.path.basename(f)
        print(f'  {fname}: title={title}, geos0={g0}')
