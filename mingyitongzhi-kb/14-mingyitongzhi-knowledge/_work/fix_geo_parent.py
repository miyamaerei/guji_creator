import json, glob, os

# 批量修：把所有 parent 不是 GEO-000 但指向 region 名的 geo 节点改成 GEO-000
fixed = 0
for f in sorted(glob.glob('_data/vol*/*.json')):
    d = json.load(open(f, encoding='utf-8'))
    if 'layers' not in d:
        continue
    changed = False
    for g in d['layers'].get('geos', []):
        p = g.get('parent', '')
        # parent 是中文 region 名而非 GEO-xxx
        if p and not p.startswith('GEO-'):
            print(f"  {os.path.basename(f)}: {g['geo_id']} {g['name']} parent={p} -> GEO-000")
            g['parent'] = 'GEO-000'
            changed = True
            fixed += 1
    if changed:
        with open(f, 'w', encoding='utf-8') as fp:
            json.dump(d, fp, ensure_ascii=False, indent=2)
print(f"\n共修 {fixed} 个 geo parent")
