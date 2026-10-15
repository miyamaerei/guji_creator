import json

# 1. 杭州府主文件 GEO 树
print("=== 杭州府 GEO 树 ===")
d = json.load(open('_data/vol38/38-001_杭州府.json', encoding='utf-8'))
for g in d['layers']['geos']:
    print(f"  {g['geo_id']} {g['name']} type={g['type']} parent={g.get('parent')} children={len(g.get('children',[]))}")

# 2. 县文件 parent 是否正确
print("\n=== 县/卫 parent 抽查 ===")
import glob, os
for f in sorted(glob.glob('_data/vol38/38-001_c*.json')) + sorted(glob.glob('_data/vol38/38-001_w*.json')):
    cd = json.load(open(f, encoding='utf-8'))
    g = cd['layers']['geos'][0]
    print(f"  {g['geo_id']} {g['name']:8s} parent={g.get('parent')}")

# 3. 各层记录数
print("\n=== 各层记录数（主文件）===")
for k, v in d['layers'].items():
    if isinstance(v, list):
        print(f"  {k}: {len(v)}")

# 4. 县文件层记录数
print("\n=== 县文件层记录数 ===")
for f in sorted(glob.glob('_data/vol38/38-001_c*.json')):
    cd = json.load(open(f, encoding='utf-8'))
    counts = {k: len(v) for k, v in cd['layers'].items() if isinstance(v, list)}
    print(f"  {os.path.basename(f):30s} {counts}")
