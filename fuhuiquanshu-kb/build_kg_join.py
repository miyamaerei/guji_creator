# -*- coding: utf-8 -*-
"""跨层整合（必建）：8 层按 item_id 组装 → _kg_join.json + _kg_join_flat.csv（Excel 直开）。
用法：python build_kg_join.py（缺省=全部已打包卷，扫描 _layers/ent）"""
import csv
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (ROOT, LAYER_DIR, read_json, write_json)

VOLUME_SOURCE = {
    "01": "卷一（筮仕部）", "02": "卷二（莅任部一）", "03": "卷三（莅任部二）",
    "04": "卷四（莅任部三）", "05": "卷五（莅任部四）",
    "06": "卷六（钱谷部一）", "07": "卷七（钱谷部二）", "08": "卷八（钱谷部三/杂课部）",
    "09": "卷九（编审部）", "10": "卷十（清丈部）",
    "11": "卷十一（刑名部一）", "12": "卷十二（刑名部二）", "13": "卷十三（刑名部三）",
    "14": "卷十四（刑名部四）", "15": "卷十五（刑名部五）", "16": "卷十六（刑名部六）",
    "17": "卷十七（刑名部七）", "18": "卷十八（刑名部八）", "19": "卷十九（刑名部九）",
    "20": "卷二十（刑名部十）",
    "21": "卷二十一（保甲部一）", "22": "卷二十二（保甲部二）", "23": "卷二十三（保甲部三）",
    "24": "卷二十四（典礼部）",
    "25": "卷二十五（教养部一）", "26": "卷二十六（教养部二）",
    "27": "卷二十七（荒政部）",
    "28": "卷二十八（邮政部一）", "29": "卷二十九（邮政部二）",
    "30": "卷三十（庶政部一）", "31": "卷三十一（庶政部二）",
    "32": "卷三十二（升迁部）", "33": "卷三十三（禀启附）",
}

# 8 层槽位（dir 为产物实际目录名：复数；key 为 join 槽位名；id_key 为层 ID 字段）
LAYERS = [("ent", "ent", "ent_id"), ("rules", "rule", "rule_id"),
          ("structs", "struct", "struct_id"), ("regs", "reg", "reg_id"),
          ("opns", "opn", "opn_id"), ("procs", "proc", "process_id"),
          ("docs", "doc", "doc_id"), ("rels", "rel", "rel_id")]


def load_layer(vol, layer_dir, id_key):
    p = os.path.join(LAYER_DIR, layer_dir, "%s_%s.json" % (layer_dir, vol))
    data = read_json(p, {"records": []})
    return [(r["item_id"], r[id_key]) for r in data["records"] if id_key in r]


def available_vols():
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
        layer_recs = {key: load_layer(vol, layer_dir, id_key) for layer_dir, key, id_key in LAYERS}
        items = {}
        for item_id in registry:
            if item_id.startswith(vol + "-"):
                items.setdefault(item_id, {key: [] for _, key, _ in LAYERS})
        for layer_dir, key, id_key in LAYERS:
            for item_id, lid in layer_recs[key]:
                items.setdefault(item_id, {k: [] for _, k, _ in LAYERS})[key].append(lid)
        for item_id, layers in sorted(items.items()):
            join["records"].append({
                "item_id": item_id,
                "volume": vol,
                "source": VOLUME_SOURCE.get(vol, vol),
                **{k: layers[k] for _, k, _ in LAYERS},
                "layer_count": sum(1 for _, k, _ in LAYERS if layers[k]),
            })
            seen.add(item_id)
    write_json(os.path.join(ROOT, "_kg_join.json"), join)

    with io.open(os.path.join(ROOT, "_kg_join_flat.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "volume", "source"] + [k for _, k, _ in LAYERS] + ["layer_count"])
        for r in join["records"]:
            w.writerow([r["item_id"], r["volume"], r["source"]] +
                       [";".join(r[k]) for _, k, _ in LAYERS] + [r["layer_count"]])
    print("跨层索引：%d 条（覆盖 item_id %d 个）" % (len(join["records"]), len(seen)))


if __name__ == "__main__":
    main()
