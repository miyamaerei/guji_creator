# -*- coding: utf-8 -*-
"""
GAR 卫所关隘层打包器（地理志版）：卫/所/关/隘/巡检司，含实土属性（实土/无实土/未明——原文未载一律未明，不臆断）+ 建制沿革（established）。
用法：python build_gar.py [--volumes 01,03]
源数据：scripts/_gar_ai_NN.py  GAR_AI = [{slot,item_id,name,type,territorial,established{reign,year,era_raw},place,dusi,note}]
ID：DLZ-GAR-{卷×500+序号}。
"""

import argparse
import importlib
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
        p = os.path.join(HERE, "_gar_ai_%s.py" % v)
        if not os.path.isfile(p):
            continue
        m = importlib.import_module("_gar_ai_%s" % v)
        for r in getattr(m, "GAR_AI", []):
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
        if r.get("type") not in E.GAR_TYPES:
            errs.append("%s type 越界: %s" % (iid, r.get("type")))
            continue
        if r.get("territorial", "未明") not in E.GAR_TERRITORIAL:
            errs.append("%s territorial 越界: %s" % (iid, r.get("territorial")))
            continue
        if r.get("dusi", "未明") not in E.GAR_DUSI:
            errs.append("%s dusi 越界: %s" % (iid, r.get("dusi")))
        if r.get("name") and reg.get(iid) and r["name"] not in reg[iid]["norm"]:
            warns.append("GAP %s name 未命中原文: %s" % (iid, r["name"]))
        est = r.get("established") or {}
        if (
            est.get("reign")
            and est["reign"] != "未明"
            and est["reign"] not in E.REIGN_ORDER
        ):
            errs.append("%s established.reign 越界: %s" % (iid, est.get("reign")))
        if (
            est.get("era_raw")
            and est["era_raw"] != "未明"
            and reg.get(iid)
            and est["era_raw"] not in reg[iid]["norm"]
        ):
            warns.append(
                "GAP %s established.era_raw 未命中原文: %s" % (iid, est["era_raw"])
            )
        recs.append(
            {
                "item_id": iid,
                "slot": r.get("slot", 0),
                "name": r["name"],
                "type": r["type"],
                "territorial": r.get("territorial", "未明"),
                "established": {
                    "reign": est.get("reign", "未明"),
                    "year": est.get("year", 0),
                    "era_raw": est.get("era_raw", "未明"),
                },
                "place": r.get("place", ""),
                "dusi": r.get("dusi", "未明"),
                "note": r.get("note", ""),
                "_vol": r["_vol"],
            }
        )

    for v in vols:
        vrecs = sorted(
            [x for x in recs if x["_vol"] == v], key=lambda x: (x["item_id"], x["slot"])
        )
        C.assign_ids(vrecs, C.ID_PREFIX["gar"], v)
        C.save_layer("gars", v, [{k: x[k] for k in x if k != "_vol"} for x in vrecs])
    for r in recs:
        r.pop("_vol", None)

    C.atomic_write_json(
        os.path.join(C.ROOT, "_data", "gar", "归一_汇总.json"),
        {"records": sorted(recs, key=lambda x: x["id"])},
    )

    rep = [
        "=== GAR 卫所关隘层构建报告 ===",
        "卷: %s" % ",".join(vols),
        "记录: %d" % len(recs),
        "",
        "--- type 分布 ---",
    ]
    tc = {}
    for r in recs:
        tc[r["type"]] = tc.get(r["type"], 0) + 1
    for k, v in sorted(tc.items(), key=lambda x: -x[1]):
        rep.append("  %-12s %d" % (k, v))
    rep.append("--- territorial 分布 ---")
    tc2 = {}
    for r in recs:
        tc2[r["territorial"]] = tc2.get(r["territorial"], 0) + 1
    for k, v in sorted(tc2.items(), key=lambda x: -x[1]):
        rep.append("  %-8s %d" % (k, v))
    rep.append("")
    rep.append("--- ERR (%d) ---" % len(errs))
    rep += ["  " + e for e in errs[:50]]
    rep.append("--- GAP (%d) ---" % len(warns))
    rep += ["  " + w for w in warns[:50]]
    C.atomic_write_text(
        os.path.join(C.ROOT, "_data", "gar", "验证缺漏清单.txt"),
        "\n".join(["ERR %d / GAP %d" % (len(errs), len(warns))] + errs + warns) + "\n",
    )
    out = os.path.join(C.ROOT, "_gar_report.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")
    print("OK gar=%d ERR=%d GAP=%d -> %s" % (len(recs), len(errs), len(warns), out))


if __name__ == "__main__":
    main()
