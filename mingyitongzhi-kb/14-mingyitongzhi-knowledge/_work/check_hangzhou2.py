import json
d = json.load(open('_data/vol38/38-001_杭州府.json', encoding='utf-8'))
print("=== 杭州府主文件各层记录数 ===")
for k, v in sorted(d['layers'].items()):
    if isinstance(v, list):
        print(f"  {k:8s}: {len(v):4d}")

# 抽查 ents
print("\n=== ents 抽查（前5条）===")
for e in d['layers']['ents'][:5]:
    print(f"  {e.get('ent_id'):10s} type={e.get('type'):8s} name={e.get('name')}")

# 抽查 evos
print("\n=== evos 抽查（前3条）===")
for e in d['layers']['evos'][:3]:
    print(f"  {json.dumps(e, ensure_ascii=False)[:150]}")

# 抽查 mtns
print("\n=== mtns 抽查（前5条）===")
for e in d['layers']['mtns'][:5]:
    print(f"  {e.get('mtn_id','?'):10s} name={e.get('name')}")

# 抽查 sites
print("\n=== sites 抽查（前5条）===")
for e in d['layers']['sites'][:5]:
    print(f"  {e.get('site_id','?'):10s} name={e.get('name')}")

# 抽查 pers
print("\n=== pers 抽查（前5条）===")
for e in d['layers']['pers'][:5]:
    print(f"  {e.get('per_id','?'):10s} name={e.get('name')}")

# cits
print("\n=== cits ===")
for e in d['layers']['cits']:
    print(f"  {json.dumps(e, ensure_ascii=False)[:150]}")
