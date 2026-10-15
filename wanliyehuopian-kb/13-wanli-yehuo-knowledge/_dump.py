# -*- coding: utf-8 -*-
import json

reg = json.load(open('_item_registry.json', encoding='utf-8'))
# reg could be dict keyed by item_id or list, or {records:[...]}
if isinstance(reg, dict) and 'records' in reg:
    items = {r['item_id']: r for r in reg['records']}
elif isinstance(reg, dict):
    items = reg
else:
    items = {r['item_id']: r for r in reg}

missing = {
 '02': ["02-014","02-020","02-023","02-025","02-027","02-030","02-035","02-039","02-042","02-043","02-046","02-049","02-050","02-051","02-053","02-054"],
 '03': ["03-007","03-011","03-023","03-026","03-029","03-034","03-035","03-036","03-037","03-041"],
 '04': ["04-008","04-010","04-020","04-021","04-031","04-034","04-038"],
 '05': ["05-004","05-010","05-016","05-025","05-028","05-029","05-031","05-034"],
}
for v in ['02','03','04','05']:
    for iid in missing[v]:
        r = items.get(iid)
        if not r:
            print(iid, 'NOT FOUND'); continue
        print(f"### {iid} | {r.get('volume_name')} | {r.get('subcategory')} | {r.get('entry_title')}")
        print(r.get('original'))
        print()
