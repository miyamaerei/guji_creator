import json

fixes = [
    ('_data/vol31/31-001_c10_固始县.json', 'evos', 'EVO-002', 'item_id', '31-001'),
    ('_data/vol31/31-002_汝州.json',       'evos', 'EVO-003', 'item_id', '31-002'),
    ('_data/vol33/33-001_汉中府.json',    'ents', 'ENT-002', 'ent_type', 'mtn'),
    ('_data/vol33/33-001_汉中府.json',    'ents', 'ENT-007', 'ent_type', 'mtn'),
]

for path, layer, rec_id, field, newval in fixes:
    d = json.load(open(path, encoding='utf-8'))
    found = False
    for rec in d['layers'][layer]:
        rid = rec.get('evo_id') or rec.get('ent_id')
        if rid == rec_id:
            old = rec.get(field)
            rec[field] = newval
            print(f"[OK] {path}: {rec_id} {field} {old!r} -> {newval!r}")
            found = True
    if not found:
        print(f"[MISS] {path}: {rec_id} not found")
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
