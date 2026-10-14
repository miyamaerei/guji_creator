# -*- coding: utf-8 -*-
"""
C15 官职层打包器（v10）。

产出：
  _layers/structs/officials.json      官职节点（含 salary / peers / relations）
  _views/officials_flat.csv           官职 × 机构 × 品级 × 俸禄 扁平表
  _views/official_tree.json           官职按机构成树
  _views/official_by_grade.json       品级倒排
  _data/struct/official_report.txt    构建报告

运行：python scripts/build_officials.py
"""
import argparse
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C
import _kg_enums as E
import _build_officials as BO


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volumes", default=None)
    args = ap.parse_args()
    vols = C.iter_volumes(None)          # 官职层全量构建（跨卷去重）

    officials, relations_raw, stats, errs = BO.build_officials(vols)

    org_nodes = []
    for v in vols:
        for rec in BO.load_vol_json("structs", v):
            if BO.is_org(rec):
                BO.walk_org(rec, org_nodes)
    org_by_id = {n["id"]: n for n in org_nodes if n["id"]}

    rel_edges, unmatched = BO.build_official_relations(
        officials, relations_raw, org_by_id, stats.get("org_items"))

    # ---------- 写层 ----------
    C.atomic_write_json(os.path.join(C.LAYERS, "structs", "officials.json"),
                        {"volume": "all", "records": officials})

    # ---------- 视图 1：扁平 CSV ----------
    vdir = os.path.join(C.VIEWS)
    os.makedirs(vdir, exist_ok=True)
    flat = os.path.join(vdir, "officials_flat.csv")
    with open(flat, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["official_id", "org_id", "org_name", "org_path", "office",
                    "grade", "grade_order", "count",
                    "salary_base_item", "salary_base_amount", "salary_base_unit",
                    "salary_base_form",
                    "salary_actual_item", "salary_actual_amount", "salary_actual_unit",
                    "salary_actual_form", "salary_actual_duty",
                    "relations", "peers", "item_ids", "sources"])
        for n in officials:
            gb = n["salary"]["grade_based"] or {}
            ac = n["salary"]["actual"] or {}
            w.writerow([
                n["official_id"], n["org_id"], n["org_name"], "/".join(n["org_path"]),
                n["office"], n["grade"], n["grade_order"], n["count"],
                gb.get("item", ""), gb.get("amount", ""), gb.get("unit", ""),
                gb.get("form", ""),
                ac.get("item", ""), ac.get("amount", ""), ac.get("unit", ""),
                ac.get("form", ""), ac.get("duty", ""),
                ";".join("%s>%s" % (r["type"], r["target_office"]) for r in n["relations"]),
                ";".join(n["peers"]),
                ";".join(n["item_ids"]), ";".join(n["sources"]),
            ])

    # ---------- 视图 2：官职树（按机构归属）----------
    tree = {}
    for n in officials:
        oid = n["org_id"] or "_UNASSIGNED"
        tree.setdefault(oid, {
            "org_id": oid,
            "org_name": n["org_name"] or "（无机构归属）",
            "org_path": n["org_path"],
            "officials": [],
        })
        tree[oid]["officials"].append({
            "official_id": n["official_id"],
            "office": n["office"],
            "grade": n["grade"],
            "grade_order": n["grade_order"],
            "count": n["count"],
            "peers": n["peers"],
            "relations": n["relations"],
        })
    for oid in tree:
        tree[oid]["officials"].sort(key=lambda x: (x["grade_order"], x["office"]))
    C.atomic_write_json(os.path.join(vdir, "official_tree.json"),
                        {"records": [tree[k] for k in sorted(tree.keys())]})

    # ---------- 视图 3：品级倒排 ----------
    byg = {}
    for n in officials:
        byg.setdefault(n["grade"], []).append({
            "official_id": n["official_id"], "office": n["office"],
            "org_name": n["org_name"], "count": n["count"],
        })
    C.atomic_write_json(os.path.join(vdir, "official_by_grade.json"), {
        "records": [{"grade": g, "grade_order": E.grade_order(g), "officials": v}
                    for g, v in sorted(byg.items(), key=lambda kv: E.grade_order(kv[0]))]
    })

    # ---------- 校验 ----------
    ids = [n["official_id"] for n in officials]
    if len(ids) != len(set(ids)):
        errs.append("OFFICIALS ID 撞号")
    by_id = {n["official_id"]: n for n in officials}
    for n in officials:
        if n["org_id"] and n["org_id"] not in org_by_id:
            errs.append("%s org_id 不存在: %s" % (n["official_id"], n["org_id"]))
        for r in n["relations"]:
            if r["target"] not in by_id:
                errs.append("%s relation target 不存在: %s" % (n["official_id"], r["target"]))
            if r["type"] not in E.OFFICIAL_RELATIONS:
                errs.append("%s relation type 越界: %s" % (n["official_id"], r["type"]))
        # peers 必须同机构同品级（用户定义）
        for pid in n["peers"]:
            m = by_id.get(pid)
            if m is None:
                errs.append("%s peer 不存在: %s" % (n["official_id"], pid))
            elif m["org_id"] != n["org_id"] or m["grade_order"] != n["grade_order"]:
                errs.append("%s peer 非法（非平级）: %s" % (n["official_id"], pid))
        if n["peers"] and pid_strict(n, by_id, errs):
            pass

    # ---------- 报告 ----------
    with_actual = [n for n in officials if n["salary"]["actual"]]
    with_peers = [n for n in officials if n["peers"]]
    with_rel = [n for n in officials if n["relations"]]
    rep = [
        "=== C15 官职层构建报告 ===",
        "源：ORG 节点 %d / RANK 记录 %d（仅品级员额）/ ENT official 标注 %d"
        % (stats["org_nodes"], stats["rank_recs"], stats["ent_official"]),
        "官职节点: %d" % len(officials),
        "  有机构归属: %d" % len([n for n in officials if n["org_id"]]),
        "  无机构归属: %d" % len([n for n in officials if not n["org_id"]]),
        "  有平级(peers): %d 条 / 平级边 %d"
        % (len(with_peers), sum(len(n["peers"]) for n in officials) // 2),
        "  有关系边: %d 条 / 边数 %d" % (len(with_rel), len(rel_edges)),
        "  有实俸(actual): %d 条" % len(with_actual),
        "  有保底俸禄: %d 条" % len([n for n in officials if n["salary"]["grade_based"]]),
        "",
        "--- 来源分布 ---",
    ]
    src_d = {}
    for n in officials:
        for s in n["sources"]:
            src_d[s] = src_d.get(s, 0) + 1
    for k in sorted(src_d):
        rep.append("  %-6s %d" % (k, src_d[k]))
    rep += ["", "--- 实俸形态分布 ---"]
    fd = {}
    for n in with_actual:
        k = n["salary"]["actual"]["form"]
        fd[k] = fd.get(k, 0) + 1
    for k in sorted(fd):
        rep.append("  %-10s %d" % (k, fd[k]))
    rep += ["", "--- 关系类型分布 ---"]
    rd = {}
    for e in rel_edges:
        rd[e["type"]] = rd.get(e["type"], 0) + 1
    for k in sorted(rd):
        rep.append("  %-6s %d" % (k, rd[k]))
    rep += ["", "--- 关系边明细（%d 条）---" % len(rel_edges)]
    for e in sorted(rel_edges, key=lambda x: (x["type"], x["org_id"], x["official_id"])):
        rep.append("  %-5s %-10s(%s) 副贰于 -> %s"
                   % (e["type"], e["target_office"], e["org_id"] or "—",
                      e["official_id"]))
    rep += ["", "--- 未配对的关系表述（%d 条，留档待人工判）---" % len(unmatched)]
    for u in unmatched[:40]:
        rep.append("  %-8s %-5s %s" % (u["item_id"], u["type"], u["reason"]))
        rep.append("            原文：%s" % u["window"].strip()[:70])
    rep += ["", "--- ERR (%d) ---" % len(errs)]
    rep += ["  " + e for e in errs[:60]]
    out = os.path.join(C.ROOT, "_data", "struct", "official_report.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")

    print("OK officials=%d peers=%d rel=%d actual_salary=%d ERR=%d -> %s"
          % (len(officials), len(with_peers), len(rel_edges), len(with_actual),
             len(errs), out))


def pid_strict(n, by_id, errs):
    """占位（保留扩展点）"""
    return False


if __name__ == "__main__":
    main()
