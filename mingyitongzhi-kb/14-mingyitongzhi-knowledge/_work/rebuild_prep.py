import json, os, shutil

# 1. 清空 _layers
if os.path.exists('_layers'):
    shutil.rmtree('_layers')

# 2. 建空 all.json
for layer in ["ent","geo","evo","mtn","per","site","cit"]:
    os.makedirs(os.path.join('_layers', layer), exist_ok=True)
    json.dump({"records": [], "count": 0},
              open(os.path.join('_layers', layer, 'all.json'), 'w', encoding='utf-8'),
              ensure_ascii=False)

# 3. 修 registry 里 03-001 title（之前错写成"衡水县"）
reg = json.load(open('_item_registry.json', encoding='utf-8'))
if '03-001' in reg:
    old = reg['03-001']['title']
    reg['03-001']['title'] = '真定府'
    reg['03-001']['type'] = 'prefecture'
    print(f"registry[03-001]: title {old!r} -> 真定府, type -> prefecture")
json.dump(reg, open('_item_registry.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print("layers emptied, registry fixed. ready for _merge_all.py")
