# -*- coding: utf-8 -*-
"""跨层整合（必建）：各层按 item_id 组装 → _kg_join.json + _kg_join_flat.csv（Excel 直开）。
用法：python build_kg_join.py [--volumes 01,02]（缺省=全部已打包卷）"""
import csv
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (ROOT, LAYER_DIR, read_json, write_json)

VOLUME_SOURCE = {
    "01": "卷一（内阁/六部/科道+六部则例）", "02": "卷二（直省事例）",
    "03": "卷三（官箴+钱粮技术·上）", "04": "卷四（吕叔简救命会+十家牌法）",
    "05": "卷五（状式+刑戒+狱政）",
}


def load_layer(vol, layer, id_key):
    p = os.path.join(LAYER_DIR, layer, "%s_%s.json" % (layer, vol))
    data = read_json(p, {"records": []})
    return [(r["item_id"], r[id_key]) for r in data["records"] if id_key in r]


def available_vols():
    """扫描 _layers/ent 已打包卷（全量重建依据，不受 --volumes 影响）。"""
    import re
    p = os.path.join(LAYER_DIR, "ent")
    vols = []
    if os.path.isdir(p):
        for fn in os.listdir(p):
            m = re.match(r"ent_(\d+)\.json$", fn)
            if m:
                vols.append(m.group(1))
    return sorted(vols)


def main():
    vols = available_vols()
    registry = read_json(os.path.join(ROOT, "_item_registry.json"), {})
    join = {"records": []}
    seen = set()
    for vol in vols:
        ents = load_layer(vol, "ent", "ent_id")
        rules = load_layer(vol, "rule", "rule_id")
        structs = load_layer(vol, "struct", "struct_id")
        regs = load_layer(vol, "reg", "reg_id")
        events = load_layer(vol, "evt", "event_id")
        items = {}
        # 先按 registry 铺全部 item_id（空条目也回填，layer_count=0）
        for item_id in registry:
            if item_id.startswith(vol + "-"):
                items.setdefault(item_id, {"rules": [], "structs": [], "ents": [],
                                           "regs": [], "events": []})
        for item_id, eid in ents + rules + structs + regs + events:
            items.setdefault(item_id, {"rules": [], "structs": [], "ents": [],
                                       "regs": [], "events": []})
        for item_id, eid in ents:
            items[item_id]["ents"].append(eid)
        for item_id, eid in rules:
            items[item_id]["rules"].append(eid)
        for item_id, eid in structs:
            items[item_id]["structs"].append(eid)
        for item_id, eid in regs:
            items[item_id]["regs"].append(eid)
        for item_id, eid in events:
            items[item_id]["events"].append(eid)
        for item_id, layers in sorted(items.items()):
            join["records"].append({
                "item_id": item_id,
                "volume": vol,
                "source": VOLUME_SOURCE.get(vol, vol),
                "rules": layers["rules"],
                "regs": layers["regs"],
                "events": layers["events"],
                "structs": layers["structs"],
                "ents": layers["ents"],
                "layer_count": sum(1 for x in (layers["rules"], layers["regs"],
                                               layers["events"], layers["structs"],
                                               layers["ents"]) if x),
            })
            seen.add(item_id)
    write_json(os.path.join(ROOT, "_kg_join.json"), join)

    # CSV（utf-8-sig，Excel 直开）
    with io.open(os.path.join(ROOT, "_kg_join_flat.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "volume", "source", "rules", "regs", "events",
                    "structs", "ents", "layer_count"])
        for r in join["records"]:
            w.writerow([r["item_id"], r["volume"], r["source"],
                        ";".join(r["rules"]), ";".join(r["regs"]), ";".join(r["events"]),
                        ";".join(r["structs"]), ";".join(r["ents"]),
                        r["layer_count"]])
    print("跨层索引：%d 条（覆盖 item_id %d 个）" % (len(join["records"]), len(seen)))


if __name__ == "__main__":
    main()
