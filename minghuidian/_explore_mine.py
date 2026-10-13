# -*- coding: utf-8 -*-
import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])
VOLS = [120, 121, 123, 124, 125, 126, 127, 128]
mine = sorted(iid for iid in reg if int(iid.split("-")[0]) in VOLS and iid not in covered)
out = []
for iid in mine:
    t = reg[iid]["title"]
    sec = reg[iid].get("section", "")
    out.append("{}\t[{}]\t{}字\t{}".format(iid, sec, len(t), t))
open(os.path.join(ROOT, "_mine_dump.txt"), "w", encoding="utf-8").write("\n".join(out))
print("written", len(out))
