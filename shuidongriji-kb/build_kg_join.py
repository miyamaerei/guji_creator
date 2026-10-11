# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— 跨层索引生成器（build_kg_join）
==========================================================
合并全部层产物 → 每条目一行：
  _kg_join.json + _kg_join_flat.csv（item_id/volume/source/ents/appts/
  events/regs/lits/rels/nams/trls/layer_count）

layer_count = 8 个贯通层非空计数（TRL 全量逐条，通常计入）。
"""
import argparse
import csv
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

LAYERS = ["ent", "appt", "event", "reg", "lit", "rel", "nam", "trl"]


def load_all_layer_records(layer):
    """汇总 data/<layer>/<layer>_NN.json 的全部记录（按 item_id 分组）。"""
    by_item = {}
    d = os.path.join(common.DATA_DIR, layer)
    if not os.path.isdir(d):
        return by_item
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".json") or fn.endswith("_summary.json"):
            continue
        data = common.load_json(os.path.join(d, fn))
        if not data:
            continue
        # ent 层产物结构为 annotations，其余层为 records
        recs = data.get("annotations", []) if layer == "ent" else data.get("records", [])
        for r in recs:
            by_item.setdefault(r["item_id"], []).append(r)
    return by_item


def build(volumes=None, verbose=True):
    out_dir = os.path.join(common.DATA_DIR, "join")
    os.makedirs(out_dir, exist_ok=True)
    reg = common.load_registry()
    all_items = sorted(reg.keys())

    layers_data = {layer: load_all_layer_records(layer) for layer in LAYERS}
    rows = []
    for item_id in all_items:
        if volumes and item_id[:2] not in volumes:
            continue
        row = {
            "item_id": item_id,
            "volume": item_id[:2],
            "source": "原文",
            "ents": [], "appts": [], "events": [], "regs": [],
            "lits": [], "rels": [], "nams": [], "trls": [],
        }
        for layer in LAYERS:
            key = "ents" if layer == "ent" else layer + "s"
            for r in layers_data[layer].get(item_id, []):
                if layer == "ent":
                    row[key].append(r.get("id") or r.get("ent_id"))
                else:
                    row[key].append(r.get({
                        "appt": "appointment_id", "event": "event_id",
                        "reg": "reg_id", "lit": "lit_id", "rel": "rel_id",
                        "nam": "nam_id", "trl": "trl_id",
                    }[layer]))
        row["layer_count"] = sum(1 for k in
                                 ["ents", "appts", "events", "regs", "lits",
                                  "rels", "nams", "trls"] if row[k])
        rows.append(row)

    common.write_json(os.path.join(out_dir, "_kg_join.json"), rows)
    with io.open(os.path.join(out_dir, "_kg_join_flat.csv"), "w",
                 encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        header = ["item_id", "volume", "source", "ents", "appts", "events",
                  "regs", "lits", "rels", "nams", "trls", "layer_count"]
        w.writerow(header)
        for r in rows:
            w.writerow([r["item_id"], r["volume"], r["source"]]
                       + [";".join(r[k]) for k in
                          ["ents", "appts", "events", "regs", "lits", "rels",
                           "nams", "trls"]] + [r["layer_count"]])
    if verbose:
        print(f"跨层索引：{len(rows)} 条目，覆盖 {len({r['volume'] for r in rows})} 卷")
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="跨层索引生成器")
    ap.add_argument("--volumes", nargs="*")
    args = ap.parse_args()
    build(volumes=args.volumes)
