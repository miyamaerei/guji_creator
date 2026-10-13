# -*- coding: utf-8 -*-
"""跨层整合（必建）：各层按 item_id 组装 → _kg_join.json + _kg_join_flat.csv（Excel 直开）。
用法：python build_kg_join.py [--volumes 01,02]（缺省=全部已打包卷）"""
import csv
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (ROOT, LAYER_DIR, parse_volumes, read_json, write_json)

VOLUME_SOURCE = {
    "01": "明职·新吾吕先生实政录序", "02": "明职·明职引", "03": "明职·卷一",
    "04": "民务·卷之二", "05": "民务·卷之三", "06": "民务·卷之四",
    "07": "乡甲约·卷之一", "08": "乡甲约·卷之二", "09": "乡甲约·卷之三",
    "10": "乡甲约·卷之四", "11": "乡甲约·卷之五", "12": "乡甲约·卷之六",
    "13": "风宪约·重刊风宪约序", "14": "风宪约·卷之一", "15": "风宪约·卷之二",
}


def load_layer(vol, layer, id_key):
    p = os.path.join(LAYER_DIR, layer, "%s_%s.json" % (layer, vol))
    data = read_json(p, {"records": []})
    return [(r["item_id"], r[id_key]) for r in data["records"] if id_key in r]


def main():
    vols = parse_volumes() or ["%02d" % i for i in range(1, 16)]
    registry = read_json(os.path.join(ROOT, "_item_registry.json"), {})
    join = {"records": []}
    seen = set()
    for vol in vols:
        ents = load_layer(vol, "ent", "ent_id")
        rules = load_layer(vol, "rule", "rule_id")
        structs = load_layer(vol, "struct", "struct_id")
        items = {}
        # 先按 registry 铺全部 item_id（空条目也回填，layer_count=0）
        for item_id in registry:
            if item_id.startswith(vol + "-"):
                items.setdefault(item_id, {"rules": [], "structs": [], "ents": []})
        for item_id, eid in ents + rules + structs:
            items.setdefault(item_id, {"rules": [], "structs": [], "ents": []})
        for item_id, eid in ents:
            items[item_id]["ents"].append(eid)
        for item_id, eid in rules:
            items[item_id]["rules"].append(eid)
        for item_id, eid in structs:
            items[item_id]["structs"].append(eid)
        for item_id, layers in sorted(items.items()):
            join["records"].append({
                "item_id": item_id,
                "volume": vol,
                "source": VOLUME_SOURCE.get(vol, vol),
                "rules": layers["rules"],
                "structs": layers["structs"],
                "ents": layers["ents"],
                "layer_count": sum(1 for x in (layers["rules"], layers["structs"], layers["ents"]) if x),
            })
            seen.add(item_id)
    write_json(os.path.join(ROOT, "_kg_join.json"), join)

    # CSV（utf-8-sig，Excel 直开）
    with io.open(os.path.join(ROOT, "_kg_join_flat.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "volume", "source", "rules", "structs", "ents", "layer_count"])
        for r in join["records"]:
            w.writerow([r["item_id"], r["volume"], r["source"],
                        ";".join(r["rules"]), ";".join(r["structs"]), ";".join(r["ents"]),
                        r["layer_count"]])
    print("跨层索引：%d 条（覆盖 item_id %d 个）" % (len(join["records"]), len(seen)))


if __name__ == "__main__":
    main()
