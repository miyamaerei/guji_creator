import json
d = json.load(open('_data/vol49/49-001_南昌府.json', encoding='utf-8'))
for g in d['layers']['geos']:
    print(f"{g['geo_id']:20s} {g['name']:8s} type={g.get('type',''):12s} children={g.get('children',[])}")
