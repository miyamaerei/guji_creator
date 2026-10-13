# -*- coding: utf-8 -*-
"""
GEO 政区树打包器（地理志版）：树形政区节点 + 土司族节点 + 八到拆字段 + 编户口里。
用法：python build_geo.py [--volumes 01,03]
源数据：scripts/_geo_ai_NN.py  GEO_AI = [{slot,item_id,name,level,node_type,parent{text},bearing_distance[],quantity[],note}]
ID：DLZ-GEO-{卷×500+序号}。
树校验：深度 <=6、父级 level 序非递减（GEO_LEVEL_ORDER 兼容同级）。
parent 引用挂起机制：parent.text 无对应节点 -> warn + parent.geo_id=None（全量建齐后消除）。
同名政区（如太平府）：入同名异指待核清单.csv（V2），不自动合并。
"""

import argparse
import csv
import importlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C
import _kg_enums as E

VOLS = sorted(C.VOL_MAP.values())
HERE = os.path.dirname(os.path.abspath(__file__))


def collect(vols):
    out = []
    for v in vols:
        p = os.path.join(HERE, "_geo_ai_%s.py" % v)
        if not os.path.isfile(p):
            continue
        m = importlib.import_module("_geo_ai_%s" % v)
        for r in getattr(m, "GEO_AI", []):
            r["_vol"] = v
            out.append(r)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volumes", default=None)
    args = ap.parse_args()
    vols = C.iter_volumes(args.volumes)

    reg = C.load_registry()
    raw = collect(vols)

    errs, warns = [], []
    recs = []
    for r in raw:
        iid = r.get("item_id")
        if iid not in reg:
            errs.append("item_id 不存在: %s" % iid)
            continue
        if r.get("level") not in E.GEO_LEVELS:
            errs.append("%s level 越界: %s" % (iid, r.get("level")))
            continue
        if r.get("node_type") not in E.GEO_NODES:
            errs.append("%s node_type 越界: %s" % (iid, r.get("node_type")))
            continue
        if (
            r.get("tusi_type")
            and r.get("tusi_type") != "未明"
            and r.get("tusi_type") not in E.TUSI_TYPES
        ):
            errs.append("%s tusi_type 越界: %s" % (iid, r.get("tusi_type")))
        if r.get("govern") and r.get("govern") not in E.TUSI_GOVERN:
            errs.append("%s govern 越界: %s" % (iid, r.get("govern")))
        # 八到方位校验
        for bd in r.get("bearing_distance", []) or []:
            if bd.get("bearing") and bd["bearing"] not in E.GEOTOBEARINGS:
                errs.append("%s bearing 越界: %s" % (iid, bd.get("bearing")))
            if bd.get("raw") and reg.get(iid) and bd["raw"] not in reg[iid]["norm"]:
                warns.append("GAP %s bearing.raw 未命中原文: %s" % (iid, bd.get("raw")))
        # quantity 纪年校验
        for q in r.get("quantity", []) or []:
            if (
                q.get("reign")
                and q["reign"] != "未明"
                and q["reign"] not in E.REIGN_ORDER
            ):
                errs.append("%s quantity.reign 越界: %s" % (iid, q.get("reign")))
        recs.append(
            {
                "item_id": iid,
                "slot": r.get("slot", 0),
                "name": r["name"],
                "level": r["level"],
                "node_type": r.get("node_type", "政区"),
                "govern": r.get("govern", ""),
                "tusi_type": r.get("tusi_type", ""),
                "parent": r.get("parent", {}) or {},
                "children": [],
                "geo_id_parent": None,
                "to_anchor": r.get("to_anchor", ""),
                "bearing_distance": r.get("bearing_distance", []) or [],
                "quantity": r.get("quantity", []) or [],
                "note": r.get("note", ""),
                "is_virtual": r.get("is_virtual", False),
                "_vol": r["_vol"],
            }
        )

    # ---- ID 分配（按卷段位）----
    for v in vols:
        vrecs = sorted(
            [x for x in recs if x["_vol"] == v], key=lambda x: (x["item_id"], x["slot"])
        )
        C.assign_ids(vrecs, C.ID_PREFIX["geo"], v)

    # ---- 名称索引 + 同名冲突检测（V2）----
    by_name = {}
    for r in recs:
        by_name.setdefault(r["name"], []).append(r)
    pending = []
    for nm, lst in by_name.items():
        if len(lst) > 1:
            for r in lst:
                pending.append(
                    [
                        r["id"],
                        nm,
                        r["level"],
                        r["item_id"],
                        "同名政区",
                        "按层级/语境核后合并或维持分列（V2）",
                    ]
                )
            warns.append(
                "同名政区 %d 组: %s（入待核清单）"
                % (len([x for x in by_name.values() if len(x) > 1]), nm)
            )

    # ---- parent 回填 + children 构建 ----
    id_of = {r["id"]: r for r in recs}
    for r in recs:
        pt = (r.get("parent") or {}).get("text")
        if not pt:
            r["geo_id_parent"] = None
            continue
        cand = by_name.get(pt)
        if not cand:
            r["geo_id_parent"] = None
            warns.append("HANG %s parent 未建: %s（全量建齐后消除）" % (r["id"], pt))
            continue
        pid = cand[0]["id"]
        r["geo_id_parent"] = pid
        cand[0]["children"].append(r["id"])
    # 分解 parent dict 为 {text, geo_id} 规范形
    for r in recs:
        r["parent"] = {
            "text": (r.get("parent") or {}).get("text", ""),
            "geo_id": r["geo_id_parent"],
        }
        r.pop("geo_id_parent", None)

    # ---- 树校验：深度 <=6、level 非递减 ----
    def depth_of(rid, seen):
        if rid in seen:
            return -1  # 环
        seen.add(rid)
        r = id_of[rid]
        if not r.get("geo_id_parent") or not r["parent"].get("geo_id"):
            return 1
        return 1 + depth_of(r["parent"]["geo_id"], seen)

    for r in recs:
        seen = set()
        d = depth_of(r["id"], seen)
        if d < 0:
            errs.append("GEO 环引用: %s" % r["id"])
        elif d > 6:
            errs.append("GEO 深度越限(%d>6): %s" % (d, r["id"]))
        pid = r["parent"].get("geo_id")
        if pid:
            pr = id_of.get(pid)
            if pr:
                lc, lp = (
                    E.GEO_LEVEL_ORDER.get(r["level"], 99),
                    E.GEO_LEVEL_ORDER.get(pr["level"], 99),
                )
                if lc < lp:
                    errs.append(
                        "GEO 层级回退(%s<%s): %s/%s"
                        % (r["level"], pr["level"], r["id"], pid)
                    )

    # ---- 每卷写盘 ----
    for v in vols:
        C.save_layer(
            "geos",
            v,
            [{k: r[k] for k in r if k != "_vol"} for r in recs if r["_vol"] == v],
        )
    for r in recs:
        r.pop("_vol", None)

    # ---- 政区树视图 ----
    roots = [r for r in recs if not r["parent"].get("geo_id")]
    tree = [
        {
            "id": r["id"],
            "name": r["name"],
            "level": r["level"],
            "node_type": r["node_type"],
            "item_id": r["item_id"],
        }
        for r in roots
    ]
    C.atomic_write_json(
        os.path.join(C.ROOT, "_views", "geo_tree.json"),
        {"roots": tree, "count": len(recs)},
    )

    # ---- 汇总 ----
    C.atomic_write_json(
        os.path.join(C.ROOT, "_data", "geo", "归一_汇总.json"),
        {"records": sorted(recs, key=lambda x: x["id"])},
    )

    # ---- V2 同名异指待核清单 ----
    pending_path = os.path.join(C.ROOT, "_data", "同名异指待核清单.csv")
    with open(pending_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["层", "ID", "名称", "来源条目", "原因", "建议"])
        for p in pending:
            w.writerow(["geo"] + p)
    if not pending:
        with open(pending_path, "w", encoding="utf-8-sig", newline="") as f:
            f.write("层,ID,名称,来源条目,原因,建议\n")

    rep = [
        "=== GEO 政区树构建报告 ===",
        "卷: %s" % ",".join(vols),
        "节点: %d" % len(recs),
        "根节点: %d" % len(roots),
        "",
        "--- level 分布 ---",
    ]
    tc = {}
    for r in recs:
        tc[r["level"]] = tc.get(r["level"], 0) + 1
    for k, v in sorted(tc.items(), key=lambda x: -x[1]):
        rep.append("  %-10s %d" % (k, v))
    rep.append("")
    rep.append("--- node_type 分布 ---")
    nt = {}
    for r in recs:
        nt[r["node_type"]] = nt.get(r["node_type"], 0) + 1
    for k, v in sorted(nt.items(), key=lambda x: -x[1]):
        rep.append("  %-10s %d" % (k, v))
    rep.append("")
    rep.append("--- ERR (%d) ---" % len(errs))
    rep += ["  " + e for e in errs[:50]]
    rep.append("--- 挂起/冲突 HANG+WARN (%d) ---" % len(warns))
    rep += ["  " + w for w in warns[:50]]
    C.atomic_write_text(
        os.path.join(C.ROOT, "_data", "geo", "验证缺漏清单.txt"),
        "\n".join(["ERR %d / HANG %d" % (len(errs), len(warns))] + errs + warns) + "\n",
    )
    out = os.path.join(C.ROOT, "_geo_report.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")
    print(
        "OK geo=%d roots=%d ERR=%d HANG=%d -> %s"
        % (len(recs), len(roots), len(errs), len(warns), out)
    )


if __name__ == "__main__":
    main()
