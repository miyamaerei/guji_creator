import json

path = '_data/vol33/33-001_汉中府.json'
d = json.load(open(path, encoding='utf-8'))
for e in d['layers']['ents']:
    if e.get('ent_id') in ('ENT-002', 'ENT-007'):
        old = e.get('type')
        e['type'] = 'mtn'
        # 删掉我刚才误加的 ent_type
        e.pop('ent_type', None)
        print(f"{e['ent_id']}: type {old!r} -> mtn")
json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
