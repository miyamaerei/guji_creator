import json, glob, os

# 找 GEO-04003 和 GEO-05002 是哪个府
for f in sorted(glob.glob('_data/vol*/*.json')):
    try:
        d = json.load(open(f, encoding='utf-8'))
    except: continue
    for g in d.get('layers', {}).get('geos', []):
        gid = g.get('geo_id', '')
        if gid in ('GEO-04003', 'GEO-05002', 'GEO-04003-s01', 'GEO-04003-c10'):
            print(os.path.basename(f), ':', gid, g.get('name'), 'type=', g.get('type'), 'parent=', g.get('parent'))

# 找长垣县
print("\n--- 长垣县 ---")
for f in sorted(glob.glob('_data/vol*/*长垣*')):
    print(f)
# 找永宁县
print("\n--- 永宁县 ---")
for f in sorted(glob.glob('_data/vol*/*永宁*')):
    print(f)
