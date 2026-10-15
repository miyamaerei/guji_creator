import json

# 看南直隶单文件结构
d = json.load(open('_data/refined_south_zhili.json', encoding='utf-8'))
print("=== refined_south_zhili.json ===")
print("top keys:", list(d.keys())[:10] if isinstance(d, dict) else f"list of {len(d)}")
if isinstance(d, dict):
    for k in list(d.keys())[:3]:
        v = d[k]
        print(f"  {k}: type={type(v).__name__}", end="")
        if isinstance(v, list):
            print(f" len={len(v)}")
            if v: print(f"    sample keys: {list(v[0].keys())[:8]}")
        elif isinstance(v, dict):
            print(f" keys={list(v.keys())[:8]}")
        else:
            print()
elif isinstance(d, list):
    print(f"first item keys: {list(d[0].keys())[:10]}")
    print(f"first item sample: {json.dumps(d[0], ensure_ascii=False)[:300]}")
