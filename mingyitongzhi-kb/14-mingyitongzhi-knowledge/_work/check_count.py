import json, glob, os
total_ent = 0
total_mtn = 0
for f in glob.glob('_data/vol*/*.json'):
    try:
        d = json.load(open(f, encoding='utf-8'))
        total_ent += len(d.get('layers',{}).get('ents',[]))
        total_mtn += len(d.get('layers',{}).get('mtns',[]))
    except: pass
print(f'source files: ent={total_ent}, mtn={total_mtn}')
merged = json.load(open('_layers/ent/all.json', encoding='utf-8'))
print(f'merged ent count: {len(merged["records"])}')
