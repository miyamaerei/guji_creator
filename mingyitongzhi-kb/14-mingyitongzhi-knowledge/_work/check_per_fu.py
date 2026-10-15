import json, os

ROOT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge"

# 对比各府的 evo 数量
print(f"{'vol':>4s} {'府名':10s} {'ent':>5s} {'geo':>5s} {'evo':>5s} {'mtn':>5s} {'per':>5s} {'site':>5s} {'cit':>5s}")
print("-" * 65)

for vol in list(range(38, 62)):
    vol_dir = os.path.join(ROOT, "_data", f"vol{vol:02d}")
    if not os.path.exists(vol_dir): continue
    # 找府级主文件
    for f in os.listdir(vol_dir):
        if not f.endswith(".json"): continue
        parts = f.replace(".json","").split("_")
        if len(parts) < 2: continue
        second = parts[1]
        if second.startswith("c") or second.startswith("s") or second.startswith("w") or second.startswith("pers") or second.startswith("sites"):
            continue
        try:
            d = json.load(open(os.path.join(vol_dir, f), encoding="utf-8"))
            name = parts[1][:8]
            e = len(d.get("layers",{}).get("ents",[]))
            g = len(d.get("layers",{}).get("geos",[]))
            ev = len(d.get("layers",{}).get("evos",[]))
            m = len(d.get("layers",{}).get("mtns",[]))
            p = len(d.get("layers",{}).get("pers",[]))
            s = len(d.get("layers",{}).get("sites",[]))
            c = len(d.get("layers",{}).get("cits",[]))
            print(f"{vol:4d} {name:10s} {e:5d} {g:5d} {ev:5d} {m:5d} {p:5d} {s:5d} {c:5d}")
        except: pass
