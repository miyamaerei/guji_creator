import json
files = [
  r'E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol01\01-001_京师.json',
  r'E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol01\01-002_顺天府.json',
  r'E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol02\02-001_保定府.json',
  r'E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol05\05-001_永平府.json',
]
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    L = d['layers']
    g = L['geos'][0]
    print('{} {} type={} region={}'.format(d['item_id'], d['source'], g['type'], g['region']))
    print('  ents={:3d} geos={} evos={:2d} mtns={:2d} pers={:3d} sites={:3d} cits={:2d} prods={}'.format(
        len(L['ents']), len(L['geos']), len(L['evos']), len(L['mtns']),
        len(L['pers']), len(L['sites']), len(L['cits']), len(L['prods'])))
    print('  evo dynasties:', [e['dynasty'] for e in L['evos']])
