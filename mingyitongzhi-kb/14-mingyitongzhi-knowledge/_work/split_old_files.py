import json, os, glob

os.makedirs('_work', exist_ok=True)

def split_old_file(filepath, target_dir_prefix='_data'):
    """把旧单文件按 item_id 拆成 volNN/ 独立文件"""
    d = json.load(open(filepath, encoding='utf-8'))
    if not isinstance(d, list):
        print(f"  skip {filepath}: not a list")
        return 0
    count = 0
    for item in d:
        item_id = item['item_id']
        vol = item['volume']
        # vol 可能是 int 或 str
        vol = int(vol) if isinstance(vol, str) else vol
        vol_dir = f'{target_dir_prefix}/vol{vol:02d}'
        os.makedirs(vol_dir, exist_ok=True)
        title = item.get('type', '')
        # 找一个名字做文件名
        name = ''
        for g in item['layers'].get('geos', []):
            if g.get('type') in ('prefecture', 'metro', 'department', 'tusi'):
                name = g['name']
                break
        if not name:
            name = item_id
        outfile = f'{vol_dir}/{item_id}_{name}.json'
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(item, f, ensure_ascii=False, indent=2)
        count += 1
        print(f"  -> {outfile}")
    return count

print("=== 拆分南直隶 ===")
n = split_old_file('_data/refined_south_zhili.json')
print(f"  共 {n} 个文件")

print("\n=== 拆分山西 ===")
n = split_old_file('_data/shanxi_vols19-21.json')
print(f"  共 {n} 个文件")

print("\n=== 拆分贵州 ===")
n = split_old_file('_data/guizhou_vol88.json')
print(f"  共 {n} 个文件")
