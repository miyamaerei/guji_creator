import json

path = '_data/vol02/02-002_河间府.json'
d = json.load(open(path, encoding='utf-8'))
geos = d['layers']['geos']

# 1. 修正河间府 children：直辖 c01-c10 + 属州 s01/s02
hejian = geos[0]
hejian['children'] = [
    'GEO-02002-c01','GEO-02002-c02','GEO-02002-c03','GEO-02002-c04','GEO-02002-c05',
    'GEO-02002-c06','GEO-02002-c07','GEO-02002-c08','GEO-02002-c09','GEO-02002-c10',
    'GEO-02002-s01','GEO-02002-s02'
]

# 2. 补景州 s01 / 沧州 s02 department 节点
dep_nodes = [
    {"geo_id":"GEO-02002-s01","item_id":"02-002","name":"景州","type":"department","region":"北直隶",
     "parent":"GEO-02002","children":["GEO-02002-s01-c11","GEO-02002-s01-c12","GEO-02002-s01-c13"]},
    {"geo_id":"GEO-02002-s02","item_id":"02-002","name":"沧州","type":"department","region":"北直隶",
     "parent":"GEO-02002","children":["GEO-02002-s02-c14","GEO-02002-s02-c15","GEO-02002-s02-c16"]},
]
geos.extend(dep_nodes)

json.dump(d, open(path,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
print(f"[OK] 河间府 geos: {len(geos)} nodes (added s01/s02)")
print("  children:", hejian['children'])
