import json
reg = json.load(open('_item_registry.json', encoding='utf-8'))
gap = ['06-001','06-002','07-003','08-004','09-005','10-006','11-007','13-008','14-009','14-010','15-011','15-012','16-013','16-014','17-015','19-001','20-001','21-001','21-002','21-003','21-004','21-005','21-006','88-001','88-002','88-003','88-004','88-005','88-006','88-007','88-008','88-010','88-011','88-012','88-013','88-014','88-015','88-016','88-017','88-018','88-019','88-020','88-021']
print(f'共 {len(gap)} 条占位\n')
by_region = {}
for item_id in gap:
    if item_id in reg:
        r = reg[item_id]
        by_region.setdefault(r['region'], []).append((item_id, r['volume'], r['type'], r['title']))
for region, items in by_region.items():
    print(f'=== {region} ({len(items)}条) ===')
    for item_id, vol, typ, title in items:
        print(f'  {item_id}  vol{vol}  {typ:12s}  {title}')
    print()
