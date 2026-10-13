# -*- coding: utf-8 -*-
"""
跨层索引打包器：_kg_join.json + _kg_join_flat.csv
关键纪律（pitfalls #28）：目录名 + 文件名前缀 + join 槽位名三处统一复数；
LAYERS 用 (dir, key, id_key) 三元组显式映射。
收尾用缺省模式跑（PowerShell 下 --volumes 01,02 会被拆参致 0 回填）。
"""
import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C

# (目录名, 槽位键, 记录内 ID 字段名)
LAYERS = [
    ("ents",   "ents",   "id"),
    ("rules",  "rules",  "id"),
    ("procs",  "procs",  "id"),
    ("structs","structs","id"),   # ORG/RANK/LINE/EVO 同置 structs 目录
    ("appts",  "appts",  "id"),
    ("tmes",   "tmes",   "id"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volumes", default=None)
    args = ap.parse_args()
    vols = C.iter_volumes(args.volumes)
    reg = C.load_registry()

    join = {}
    for iid in reg:
        v = iid.split("-")[0]
        join[iid] = {"item_id": iid, "volume": v, "source": "原文",
                     "ents": [], "rules": [], "procs": [],
                     "structs": [], "appts": [], "tmes": [],
                     "layer_count": 0}
    if args.volumes is None:
        target = reg
    else:
        target = {k: v for k, v in reg.items() if k.split("-")[0] in vols}

    filled = 0
    for v in vols:
        for (d, key, idf) in LAYERS:
            p = os.path.join(C.LAYERS, d, "%s_%s.json" % (d, v))
            if not os.path.isfile(p):
                continue
            with open(p, "r", encoding="utf-8") as f:
                obj = json.load(f)
            for r in obj.get("records", []):
                iid = r.get("item_id")
                if iid not in join:
                    continue
                rid = r.get(idf) or r.get("id")
                if rid and rid not in join[iid][key]:
                    join[iid][key].append(rid)
                    filled += 1

    for iid, j in join.items():
        j["layer_count"] = sum(1 for (_, key, _) in LAYERS if j[key])

    out = [join[k] for k in sorted(join.keys())] if args.volumes is None else \
          [join[k] for k in sorted(target.keys())]

    C.atomic_write_json(os.path.join(C.ROOT, "_kg_join.json"), {"records": out})

    # 扁平 CSV（不逐条列 ID，只列计数 + 全文，便于 Excel 直开）
    flat = os.path.join(C.ROOT, "_kg_join_flat.csv")
    with open(flat, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item_id", "volume", "ents", "rules", "procs", "structs",
                    "appts", "tmes", "layer_count"])
        for j in out:
            w.writerow([j["item_id"], j["volume"],
                        ";".join(j["ents"]), ";".join(j["rules"]),
                        ";".join(j["procs"]), ";".join(j["structs"]),
                        ";".join(j["appts"]), ";".join(j["tmes"]),
                        j["layer_count"]])

    # 分布统计（pitfalls #28：交付前必查 layer_count 分布与 0 空条目率）
    dist = {}
    for j in out:
        dist[j["layer_count"]] = dist.get(j["layer_count"], 0) + 1
    empty = dist.get(0, 0)

    rep = ["=== 跨层索引构建报告 ===", "模式: %s" % ("全量" if args.volumes is None else ",".join(vols)),
           "条目数: %d" % len(out),
           "槽位回填: %d 处" % filled,
           "", "--- layer_count 分布 ---"]
    for k in sorted(dist):
        rep.append("  %d 层: %d 条" % (k, dist[k]))
    rep.append("")
    rep.append("0 空条目率: %.1f%%（%d 条）" % (100.0 * empty / len(out) if out else 0, empty))
    rep.append("槽位命中: " + " ".join(
        "%s=%d" % (key, sum(1 for j in out if j[key])) for (_, key, _) in LAYERS))
    rep.append("")
    rep.append("--- ERR ---")
    errs = []
    if dist and max(dist.keys()) < 2 and len(out) > 1:
        errs.append("最大 layer_count < 2：疑似目录名/键名映射错（pitfalls #28）")
    rep += ["  " + e for e in errs] if errs else ["  无"]
    C.atomic_write_text(os.path.join(C.ROOT, "_kg_join_report.txt"), "\n".join(rep) + "\n")
    print("OK join=%d filled=%d dist=%s empty=%d -> _kg_join.json"
          % (len(out), filled, dist, empty))


if __name__ == "__main__":
    main()
