import json, os, glob

d = r'E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol23'
files = sorted(glob.glob(os.path.join(d, '*.json')))

# Fix 1: action "复置" -> "复"
# Fix 2: action "封" -> "置"
# Fix 3: action "属" -> "因之" (only the prefecture EVO-003)
# Fix 4: site type "列女" -> move to pers (or just relabel)
# Fix 5: per type "陵墓"/"祠庙" -> "人物" or move to sites

for fp in files:
    with open(fp, encoding='utf-8') as f:
        data = json.load(f)
    changed = False
    for e in data.get('layers',{}).get('evos',[]):
        if e.get('action') == '复置':
            e['action'] = '复'; changed = True
        if e.get('action') == '封':
            e['action'] = '置'; changed = True
    # Fix site type 列女 -> 其他 (these are actually female biographies misplaced)
    new_sites = []
    extra_pers = []
    for s in data.get('layers',{}).get('sites',[]):
        if s.get('type') == '列女':
            # convert to a PER entry
            extra_pers.append({
                'per_id': s.get('site_id','PER-X').replace('SITE','PER'),
                'item_id': s.get('item_id','23-001'),
                'geo_id': s.get('geo_id'),
                'name': s.get('name',''),
                'type': '列女',
                'dynasty': '',
                'native_place': '',
                'office': '',
                'summary': s.get('history_lore',''),
                'original': s.get('original','')
            })
            changed = True
        else:
            new_sites.append(s)
    if extra_pers:
        data['layers']['sites'] = new_sites
        data['layers']['pers'].extend(extra_pers)
    # Fix per type 陵墓/祠庙 -> 人物 (these are tomb entries misplaced)
    new_pers = []
    extra_sites = []
    for p in data.get('layers',{}).get('pers',[]):
        if p.get('type') in ('陵墓','祠庙'):
            extra_sites.append({
                'site_id': p.get('per_id','SITE-X').replace('PER','SITE'),
                'item_id': p.get('item_id','23-001'),
                'geo_id': p.get('geo_id'),
                'name': p.get('name',''),
                'type': '陵墓' if p.get('type')=='陵墓' else '祠庙',
                'location_text': '',
                'history_lore': p.get('summary',''),
                'original': p.get('original','')
            })
            changed = True
        else:
            new_pers.append(p)
    if extra_sites:
        data['layers']['pers'] = new_pers
        data['layers']['sites'].extend(extra_sites)
    if changed:
        with open(fp, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'Fixed: {os.path.basename(fp)}')
print('Done.')
