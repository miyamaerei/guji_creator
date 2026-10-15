import json, os

ROOT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge"

# 看吉安府的 mtn 前 20 条
d = json.load(open(os.path.join(ROOT, "_data", "vol57", "57-001_吉安府.json"), encoding="utf-8"))
mtns = d["layers"]["mtns"]
print(f"吉安府 mtn 总数: {len(mtns)}")
print("前 20 条:")
for i, m in enumerate(mtns[:20]):
    print(f"  {i+1:2d}. {m.get('mtn_id','?'):15s} {m.get('name',''):10s} type={m.get('type','')}")

# 看饶州府 ent
print()
d2 = json.load(open(os.path.join(ROOT, "_data", "vol50", "50-001_饶州府.json"), encoding="utf-8"))
ents = d2["layers"]["ents"]
print(f"饶州府 ent 总数: {len(ents)}")
print("前 20 条:")
for i, e in enumerate(ents[:20]):
    print(f"  {i+1:2d}. {e.get('ent_id','?'):15s} {e.get('name',''):10s} type={e.get('type','')}")
