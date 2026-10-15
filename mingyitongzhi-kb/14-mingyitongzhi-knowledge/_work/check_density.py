import json, os

ROOT = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge"

regions = {
    "北直隶(1-5)": [1,2,3,4,5],
    "南直隶(6-18)": [6,7,8,9,10,11,12,13,14,15,16,17,18],
    "山西(19-21)": [19,20,21],
    "山东(22-25)": [22,23,24,25],
    "河南(26-31)": [26,27,28,29,30,31],
    "陕西(32-37)": [32,33,34,35,36,37],
    "浙江(38-48)": [38,39,40,41,42,43,44,45,46,47,48],
    "江西(49-61)": [49,50,51,52,53,54,55,56,57,58,59,60,61],
}

layers = ["ent","geo","evo","mtn","per","site","cit"]

print(f"{'region':16s} {'文件数':>5s} {'ent':>6s} {'geo':>6s} {'evo':>6s} {'mtn':>6s} {'per':>6s} {'site':>6s} {'cit':>6s} {'总计':>7s}")
print("-" * 85)

for region_name, vols in regions.items():
    counts = {l: 0 for l in layers}
    filecount = 0
    for vol in vols:
        vol_dir = os.path.join(ROOT, "_data", f"vol{vol:02d}")
        if not os.path.exists(vol_dir): continue
        for f in os.listdir(vol_dir):
            if not f.endswith(".json"): continue
            try:
                d = json.load(open(os.path.join(vol_dir, f), encoding="utf-8"))
                filecount += 1
                for k, out in [("ents","ent"),("geos","geo"),("evos","evo"),("mtns","mtn"),("pers","per"),("sites","site"),("cits","cit")]:
                    counts[out] += len(d.get("layers",{}).get(k,[]))
            except: pass
    total = sum(counts.values())
    print(f"{region_name:16s} {filecount:5d} {counts['ent']:6d} {counts['geo']:6d} {counts['evo']:6d} {counts['mtn']:6d} {counts['per']:6d} {counts['site']:6d} {counts['cit']:6d} {total:7d}")
