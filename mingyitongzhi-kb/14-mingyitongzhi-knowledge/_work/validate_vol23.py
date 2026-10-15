import json, os, sys, glob

d = r'E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data\vol23'
files = sorted(glob.glob(os.path.join(d, '*.json')))

WHITELIST_GEO_TYPE = {'prefecture','subprefecture','county','weisuo','department','metro','tusi','foreign','other'}
WHITELIST_PER_TYPE = {'名宦','流寓','人物','列女','仙释','其他'}
WHITELIST_SITE_TYPE = {'寺观','祠庙','陵墓','古迹','宫室','学校','书院','坛庙','城池','苑囿','关梁','其他'}
WHITELIST_MTN_TYPE = {'山','岭','峰','冈','岩','洞','泉','溪','江','河','湖','潭','池','堰','关','桥','井','其他'}
WHITELIST_ACTION = {'置','废','改','并','复','因之','升','降','迁','未明','置郡'}
WHITELIST_DYNASTY = {'周','春秋','战国','秦','汉','东汉','晋','南北朝','隋','唐','五代','宋','金','元','明','未明','三国'}
WHITELIST_REGION = {'山东','北直隶','南直隶','山西','河南','陕西','浙江','江西','湖广','四川','福建','广东','广西','云南','贵州','外夷'}

all_geo_ids = {}
errors = []
file_summary = []

for fp in files:
    name = os.path.basename(fp)
    try:
        with open(fp, encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        errors.append(f'{name}: JSON parse error: {e}')
        continue
    layers = data.get('layers', {})
    # check 7 layers
    for L in ['ents','geos','evos','mtns','pers','sites','prods','cits']:
        if L not in layers:
            errors.append(f'{name}: missing layer {L}')
    geos = layers.get('geos', [])
    evos = layers.get('evos', [])
    mtns = layers.get('mtns', [])
    pers = layers.get('pers', [])
    sites = layers.get('sites', [])
    ents = layers.get('ents', [])
    cits = layers.get('cits', [])
    prods = layers.get('prods', [])
    # collect geo ids
    for g in geos:
        gid = g.get('geo_id')
        if gid in all_geo_ids:
            errors.append(f'{name}: duplicate geo_id {gid} (also in {all_geo_ids[gid]})')
        all_geo_ids[gid] = name
        # check type
        if g.get('type') not in WHITELIST_GEO_TYPE:
            errors.append(f'{name}: geo {gid} bad type {g.get("type")}')
        if g.get('region') not in WHITELIST_REGION:
            errors.append(f'{name}: geo {gid} bad region {g.get("region")}')
        # check parent is string
        p = g.get('parent')
        if p is not None and not isinstance(p, str):
            errors.append(f'{name}: geo {gid} parent not string: {p}')
        # check children list
        ch = g.get('children', [])
        if not isinstance(ch, list):
            errors.append(f'{name}: geo {gid} children not list')
    # check enums
    for e in evos:
        if e.get('dynasty') not in WHITELIST_DYNASTY:
            errors.append(f'{name}: evo {e.get("evo_id")} bad dynasty {e.get("dynasty")}')
        if e.get('action') not in WHITELIST_ACTION:
            errors.append(f'{name}: evo {e.get("evo_id")} bad action {e.get("action")}')
    for m in mtns:
        if m.get('type') not in WHITELIST_MTN_TYPE:
            errors.append(f'{name}: mtn {m.get("mtn_id")} bad type {m.get("type")}')
    for p in pers:
        if p.get('type') not in WHITELIST_PER_TYPE:
            errors.append(f'{name}: per {p.get("per_id")} bad type {p.get("type")}')
    for s in sites:
        if s.get('type') not in WHITELIST_SITE_TYPE:
            errors.append(f'{name}: site {s.get("site_id")} bad type {s.get("type")}')
    file_summary.append((name, len(ents), len(geos), len(evos), len(mtns), len(pers), len(sites), len(prods), len(cits)))

# Now check dangling children/parent
geo_set = set(all_geo_ids.keys())
for fp in files:
    name = os.path.basename(fp)
    with open(fp, encoding='utf-8') as f:
        data = json.load(f)
    for g in data.get('layers',{}).get('geos',[]):
        p = g.get('parent')
        if p is not None and p != 'GEO-000' and p not in geo_set:
            errors.append(f'{name}: geo {g["geo_id"]} parent {p} not found')
        for ch in g.get('children', []):
            if ch not in geo_set:
                errors.append(f'{name}: geo {g["geo_id"]} children {ch} not found')

# check prefecture has all expected children
print('=== File summary (name, ents, geos, evos, mtns, pers, sites, prods, cits) ===')
for row in file_summary:
    print('  ', row)

print()
print('=== Errors ===')
if not errors:
    print('  None. All checks pass.')
else:
    for e in errors:
        print('  ', e)

print()
print(f'Total files: {len(files)}')
print(f'Total unique geo_ids: {len(geo_set)}')
