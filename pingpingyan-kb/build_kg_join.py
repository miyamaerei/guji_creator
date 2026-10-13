# -*- coding: utf-8 -*-
"""跨层整合（必建）：各层按 item_id 组装 → _kg_join.json + _kg_join_flat.csv（Excel 直开）。
用法：python build_kg_join.py [--volumes 01,02]（缺省=全部已打包卷）"""
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (ROOT, LAYER_DIR, parse_volumes, read_json, write_json)

VOLUME_SOURCE = {"01": "卷一", "02": "卷二", "03": "卷三", "04": "卷四"}
# (目录名, 槽位, id_key)——单数目录名（C4 layer_key），规避复数映射坑
LAYERS = [("ent", "ents", "ent_id"), ("rule", "rules", "rule_id"),
          ("struct", "structs", "struct_id"), ("reg", "regs", "reg_id"),
          ("opn", "opns", "opn_id")]
SLOTS = [slot for _, slot, _ in LAYERS]


def load_layer(vol, layer, id_key):
    p = os.path.join(LAYER_DIR, layer, "%s_%s.json" % (layer, vol))
    data = read_json(p, {"records": []})
    return [(r["item_id"], r[id_key]) for r in data["records"] if id_key in r]


def main():
    vols = parse_volumes() or ["%02d" % i for i in range(1, 5)]
    registry = read_json(os.path.join(ROOT, "_item_registry.json"), {})
    join = {"records": []}
    seen = set()
    for vol in vols:
        layer_data = {slot: load_layer(vol, layer, id_key)
                      for layer, slot, id_key in LAYERS}
        items = {}
        # 先按 registry 铺全部 item_id（空条目也回填，layer_count=0）
        for item_id in registry:
            if item_id.startswith(vol + "-"):
                items.setdefault(item_id, {slot: [] for slot in SLOTS})
        for slot, pairs in layer_data.items():
            for item_id, lid in pairs:
                # 每次新建独立列表（dict 浅拷贝会共享同一列表引用，酿成跨条目串数据）
                items.setdefault(item_id, {slot: [] for slot in SLOTS})[slot].append(lid)
        for item_id, layers in sorted(items.items()):
            join["records"].append({
                "item_id": item_id,
                "volume": vol,
                "source": VOLUME_SOURCE.get(vol, vol),
                "rules": layers["rules"],
                "regs": layers["regs"],
                "opns": layers["opns"],
                "structs": layers["structs"],
                "ents": layers["ents"],
                "layer_count": sum(1 for s in SLOTS if layers[s]),
            })
            seen.add(item_id)
    write_json(os.path.join(ROOT, "_kg_join.json"), join)

    # CSV（utf-8-sig，Excel 直开）
    with io.open(os.path.join(ROOT, "_kg_join_flat.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "volume", "source"] + SLOTS + ["layer_count"])
        for r in join["records"]:
            w.writerow([r["item_id"], r["volume"], r["source"]] +
                       [";".join(r[s]) for s in SLOTS] + [r["layer_count"]])
    print("跨层索引：%d 条（覆盖 item_id %d 个）" % (len(join["records"]), len(seen)))


if __name__ == "__main__":
    main()
