# -*- coding: utf-8 -*-
"""
跨层索引打包器：_kg_join.json（7 层槽位）+ _kg_join_flat.csv（查询用扁平视图）。
用法：python build_kg_join.py
读取 _layers/<容器>/<容器>_NN.json 全卷，输出：
  _kg_join.json     {每层: [记录]}（含 geo 父子链、ent 主键回填）
  _kg_join_flat.csv 每行一条记录：layer, id, item_id, name, kind, extra
"""

import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C

LAYERS = [
    ("ents", "ents", "id"),
    ("tmes", "tmes", "id"),
    ("geos", "geos", "id"),
    ("evos", "evos", "id"),
    ("hyds", "hyds", "id"),
    ("gars", "gars", "id"),
    ("ress", "ress", "id"),
]


def _kind(r, layer):
    if layer == "ents":
        return r.get("type", "")
    if layer == "geos":
        return r.get("level", "")
    if layer == "tmes":
        return r.get("category", "")
    if layer == "evos":
        return r.get("change_type", "")
    if layer == "hyds":
        return r.get("type", "")
    if layer == "gars":
        return r.get("type", "")
    if layer == "ress":
        return r.get("type", "")
    return ""


def _name(r, layer):
    for k in ("name", "normalized", "text"):
        if r.get(k):
            return r[k]
    return ""


def _read(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    join = {}
    rows = []
    for layer, key, idf in LAYERS:
        recs = []
        for p in C.layer_files(layer):
            obj = _read(p)
            recs.extend(obj.get("records", []))
        # 递归展平 geo 树 children（children 存 id 引用，不展开）
        join[layer] = recs
        for r in recs:
            rows.append(
                {
                    "layer": layer,
                    "id": r.get(idf, ""),
                    "item_id": r.get("item_id", ""),
                    "name": _name(r, layer),
                    "kind": _kind(r, layer),
                    "slot": r.get("slot", ""),
                }
            )

    with open(C.PATHS["join"], "w", encoding="utf-8") as f:
        json.dump(join, f, ensure_ascii=False, indent=1)

    flat = os.path.join(C.ROOT, "_kg_join_flat.csv")
    with open(flat, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["layer", "id", "item_id", "name", "kind", "slot"]
        )
        w.writeheader()
        for r in rows:
            w.writerow(r)

    counts = {k: len(v) for k, v in join.items()}
    print("OK kg_join %s -> %s / %s" % (counts, C.PATHS["join"], flat))


if __name__ == "__main__":
    main()
