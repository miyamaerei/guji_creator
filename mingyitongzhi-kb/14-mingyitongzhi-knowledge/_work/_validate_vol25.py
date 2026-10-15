import json, os, glob
d = r'E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol25'
all_geos = {}
errors = []
counts = {}
for f in sorted(glob.glob(os.path.join(d, '*.json'))):
    j = json.load(open(f, encoding='utf-8'))
    iid = j['item_id']
    counts.setdefault(iid, {'ents': 0, 'geos': 0, 'evos': 0, 'mtns': 0, 'pers': 0, 'sites': 0, 'cits': 0})
    L = j['layers']
    counts[iid]['ents'] += len(L.get('ents', []))
    counts[iid]['geos'] += len(L.get('geos', []))
    counts[iid]['evos'] += len(L.get('evos', []))
    counts[iid]['mtns'] += len(L.get('mtns', []))
    counts[iid]['pers'] += len(L.get('pers', []))
    counts[iid]['sites'] += len(L.get('sites', []))
    counts[iid]['cits'] += len(L.get('cits', []))
    for g in L.get('geos', []):
        gid = g['geo_id']
        if gid in all_geos:
            errors.append('DUP geo_id %s in %s and %s' % (gid, os.path.basename(f), os.path.basename(all_geos[gid])))
        all_geos[gid] = f
known = set(all_geos.keys())
known.add('GEO-SHANDONG')
for f in sorted(glob.glob(os.path.join(d, '*.json'))):
    j = json.load(open(f, encoding='utf-8'))
    for g in j['layers'].get('geos', []):
        if g['parent'] not in known:
            errors.append('ORPHAN parent: %s -> %s in %s' % (g['geo_id'], g['parent'], os.path.basename(f)))
        for c in g.get('children', []):
            if c not in known:
                errors.append('ORPHAN child: %s -> %s in %s' % (g['geo_id'], c, os.path.basename(f)))
print('=== counts (aggregated by item_id) ===')
for k, v in sorted(counts.items()):
    print(k, v)
print('=== errors ===')
print('NONE' if not errors else '\n'.join(errors))
