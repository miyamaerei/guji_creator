import json, os
d = r"E:\git\ToolBox\guji\mingyitongzhi-kb\14-mingyitongzhi-knowledge\_data"
for vol, mainname in [("vol122", "122-001_澂江府.json"), ("vol123", "123-001_蒙化府.json")]:
    files = sorted(os.listdir(os.path.join(d, vol)))
    main = json.load(open(os.path.join(d, vol, mainname), encoding="utf-8"))
    L = main["layers"]
    print(vol, "files=", len(files))
    for f in files:
        print("   ", f)
    print("   GEO nodes:", len(L["geos"]), "->", [g["geo_id"] for g in L["geos"]])
    print("   evos:", len(L["evos"]), "mtns:", len(L["mtns"]), "prods:", len(L["prods"]), "cits:", len(L["cits"]))
    for f in files:
        if "pers" in f or "sites" in f:
            o = json.load(open(os.path.join(d, vol, f), encoding="utf-8"))
            for k in ("pers", "sites"):
                if o["layers"].get(k):
                    print("   ", f, "->", len(o["layers"][k]), k)
