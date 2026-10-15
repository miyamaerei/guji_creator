import json

# 1. 大名府补 s01 开州（长垣县 c10 属开州）
d = json.load(open('_data/vol04/04-003_大名府.json', encoding='utf-8'))
geos = d['layers']['geos']
daming = geos[0]
# 长垣 c10 从直辖挪到 s01
daming['children'] = [c for c in daming['children'] if c != 'GEO-04003-c10']
daming['children'].append('GEO-04003-s01')
geos.append({"geo_id":"GEO-04003-s01","item_id":"04-003","name":"开州","type":"department","region":"北直隶",
             "parent":"GEO-04003","children":["GEO-04003-c10"]})
json.dump(d, open('_data/vol04/04-003_大名府.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print("[OK] 大名府: +s01 开州 (长垣县)")

# 2. 创建延庆州主文件
yanqing = {
    "item_id": "05-002",
    "title": "延庆州",
    "region": "北直隶",
    "layers": {
        "geos": [
            {"geo_id":"GEO-05002","item_id":"05-002","name":"延庆州","type":"department","region":"北直隶",
             "parent":"GEO-000","children":["GEO-05002-c01"]}
        ]
    }
}
json.dump(yanqing, open('_data/vol05/05-002_延庆州.json','w',encoding='utf-8'), ensure_ascii=False, indent=2)
print("[OK] 创建 05-002_延庆州.json")
