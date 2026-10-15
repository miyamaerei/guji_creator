import json, os

# 修 vol19 太原府
f = '_data/vol19/19-001_太原府.json'
d = json.load(open(f, encoding='utf-8'))
for g in d['layers']['geos']:
    if g['geo_id'] == 'GEO-001':
        g['geo_id'] = 'GEO-19001'
    # children 指向 GEO-002/003 不存在，清空
    g['children'] = []
with open(f, 'w', encoding='utf-8') as fp:
    json.dump(d, fp, ensure_ascii=False, indent=2)
print("vol19 太原府: GEO-001 -> GEO-19001, children cleared")

# 修 vol20 平阳府
f = '_data/vol20/20-001_平阳府.json'
d = json.load(open(f, encoding='utf-8'))
for g in d['layers']['geos']:
    if g['geo_id'] == 'GEO-001':
        g['geo_id'] = 'GEO-20001'
    g['children'] = []
with open(f, 'w', encoding='utf-8') as fp:
    json.dump(d, fp, ensure_ascii=False, indent=2)
print("vol20 平阳府: GEO-001 -> GEO-20001, children cleared")

# 修 vol21 各府：清空悬空 children
for f in ['_data/vol21/21-001_大同府.json',
          '_data/vol21/21-002_潞安府.json',
          '_data/vol21/21-003_21-003.json',
          '_data/vol21/21-004_21-004.json',
          '_data/vol21/21-005_21-005.json',
          '_data/vol21/21-006_21-006.json']:
    d = json.load(open(f, encoding='utf-8'))
    for g in d['layers']['geos']:
        g['children'] = []
    with open(f, 'w', encoding='utf-8') as fp:
        json.dump(d, fp, ensure_ascii=False, indent=2)
    print(f"{os.path.basename(f)}: children cleared")
