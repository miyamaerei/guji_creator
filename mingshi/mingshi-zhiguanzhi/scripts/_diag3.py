import io, json, os, collections
os.chdir(r"E:\git\ToolBox\guji\mingshi\mingshi-zhiguanzhi")
j = json.load(io.open("_views/dao_stations.json", encoding="utf-8"))
print("type:", type(j).__name__, "keys:" , list(j)[:6] if isinstance(j, dict) else len(j))
if isinstance(j, dict):
    for k in list(j)[:4]:
        print(" ", k, "->", json.dumps(j[k], ensure_ascii=False)[:200])
else:
    print(" sample:", json.dumps(j[:3], ensure_ascii=False)[:300])
    print(" total:", len(j))
