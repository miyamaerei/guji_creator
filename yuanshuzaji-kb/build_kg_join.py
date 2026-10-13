# -*- coding: utf-8 -*-
"""跨层整合（必建）：9 层按 item_id 组装 → _kg_join.json + _kg_join_flat.csv（Excel 直开）。
用法：python build_kg_join.py（缺省=全部已打包卷，扫描 _layers/ent）"""
import csv
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (ROOT, LAYER_DIR, read_json, write_json)

VOLUME_SOURCE = {
    "01": "卷一（宣谕）", "02": "卷二（县始/分土/署廨/古墨斋）",
    "03": "卷三（职官）", "04": "卷四（山川/古迹）",
    "05": "卷五（铺舍/街道）", "06": "卷六（地亩/人丁/繇赋/力役）",
    "07": "卷七（黄垡仓/廊头）", "08": "卷八（宫庄子粒）",
    "09": "卷九（马政）", "10": "卷十（奶口/三婆/土工）",
    "11": "卷十一（驾相/养济院/孤老）", "12": "卷十二（契税）",
    "13": "卷十三（铺行）", "14": "卷十四（经费上）",
    "15": "卷十五（经费下）", "16": "卷十六（人物）",
    "17": "卷十七（民风/土俗/方言）", "18": "卷十八（恩泽/坟墓）",
    "19": "卷十九（僧道/寺庵宫观庙堂祠）", "20": "卷二十（志遗）",
}

# 9 层槽位（与 LAYER_SCHEMA 对齐）
LAYERS = [("ent", "ent_id"), ("appt", "appointment_id"), ("evt", "event_id"),
          ("lit", "lit_id"), ("reg", "reg_id"), ("nam", "nam_id"),
          ("opn", "opn_id"), ("cus", "cus_id"), ("geo", "geo_id")]


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
        layer_recs = {layer: load_layer(vol, layer, id_key) for layer, id_key in LAYERS}
        items = {}
        # 先按 registry 铺全部 item_id（空条目也回填，layer_count=0）
        for item_id in registry:
            if item_id.startswith(vol + "-"):
                items.setdefault(item_id, {layer: [] for layer, _ in LAYERS})
        for layer, _ in LAYERS:
            for item_id, lid in layer_recs[layer]:
                items.setdefault(item_id, {l: [] for l, _ in LAYERS})[layer].append(lid)
        for item_id, layers in sorted(items.items()):
            join["records"].append({
                "item_id": item_id,
                "volume": vol,
                "source": VOLUME_SOURCE.get(vol, vol),
                **{l: layers[l] for l, _ in LAYERS},
                "layer_count": sum(1 for l, _ in LAYERS if layers[l]),
            })
            seen.add(item_id)
    write_json(os.path.join(ROOT, "_kg_join.json"), join)

    # CSV（utf-8-sig，Excel 直开）
    with io.open(os.path.join(ROOT, "_kg_join_flat.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "volume", "source"] + [l for l, _ in LAYERS] + ["layer_count"])
        for r in join["records"]:
            w.writerow([r["item_id"], r["volume"], r["source"]] +
                       [";".join(r[l]) for l, _ in LAYERS] + [r["layer_count"]])
    print("跨层索引：%d 条（覆盖 item_id %d 个）" % (len(join["records"]), len(seen)))


if __name__ == "__main__":
    main()
