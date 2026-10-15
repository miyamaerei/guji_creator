import json, glob, os

print("=== pers/sites 分片记录数 ===")
for f in sorted(glob.glob('_data/vol38/38-001_pers*.json') + glob.glob('_data/vol38/38-001_sites*.json')):
    d = json.load(open(f, encoding='utf-8'))
    counts = {k: len(v) for k, v in d['layers'].items() if isinstance(v, list)}
    print(f"  {os.path.basename(f):35s} {counts}")

# 抽查 pers1
print("\n=== pers1_名宦 前5条 ===")
d = json.load(open('_data/vol38/38-001_pers1_名宦.json', encoding='utf-8'))
for p in d['layers']['pers'][:5]:
    print(f"  {p.get('per_id','?'):10s} name={p.get('name')}")

# 抽查 sites1
print("\n=== sites1 前5条 ===")
d = json.load(open('_data/vol38/38-001_sites1_寺观祠庙陵墓.json', encoding='utf-8'))
for s in d['layers']['sites'][:5]:
    print(f"  {s.get('site_id','?'):10s} name={s.get('name')}")
