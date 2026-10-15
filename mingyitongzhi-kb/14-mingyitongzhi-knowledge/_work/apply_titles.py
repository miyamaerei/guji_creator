import json, glob, os

titles = {
    '32-001': '西安府',
    '34-001': '凤翔府',
    '34-002': '汉中府',
    '35-001': '平凉府',
    '35-002': '巩昌府',
    '36-001': '临洮府',
    '36-002': '庆阳府',
    '36-003': '延安府',
    '37-001': '宁夏卫',
    '37-002': '宁夏中卫',
    '37-003': '洮州卫军民指挥使司',
    '37-004': '岷州卫军民指挥使司',
    '37-005': '河州卫军民指挥使司',
    '37-006': '靖虏卫',
    '37-007': '陕西行都指挥使司',
}

fixed = 0
for item_id, title in titles.items():
    vol = item_id.split('-')[0]
    for f in glob.glob(f'_data/vol{vol}/{item_id}_*.json'):
        d = json.load(open(f, encoding='utf-8'))
        if not d.get('title'):
            d['title'] = title
            json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            fixed += 1

print(f'Fixed title in {fixed} files')
