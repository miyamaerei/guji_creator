import json, glob, os, re

# 山西文件的 geo_id 重命名：
# vol19 太原府: GEO-001 -> GEO-19001, GEO-002 -> GEO-19001-c01, GEO-003 -> GEO-19001-c02
# vol20 平阳府: GEO-001 -> GEO-20001
# vol21 各府: 保留 GEO-21xxx 但需要补全子节点

# 先看所有山西文件的 geo_id 现状
print("=== 山西 geo_id 现状 ===")
for f in sorted(glob.glob('_data/vol1[9]/vol*.json') + glob.glob('_data/vol2[01]/*.json')):
    d = json.load(open(f, encoding='utf-8'))
    if 'layers' not in d: continue
    print(f"\n{os.path.basename(f)}:")
    for g in d['layers'].get('geos', []):
        print(f"  {g['geo_id']:15s} {g['name']:8s} type={g.get('type',''):12s} parent={g.get('parent',''):15s} children={g.get('children',[])}")
