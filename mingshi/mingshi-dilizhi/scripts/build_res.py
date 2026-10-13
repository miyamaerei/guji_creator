# -*- coding: utf-8 -*-
"""
RES 经济资源层打包器（地理志版）：盐井/铁/银/铜/金/煤/硝/矾等矿冶资源与盐课，raw 必逐字命中原文。
用法：python build_res.py [--volumes 01,03]
源数据：scripts/_res_ai_NN.py  RES_AI = [{slot,item_id,name,type,place,site,importance,raw}]
ID：DLZ-RES-{卷×500+序号}。
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
        p = os.path.join(HERE, "_res_ai_%s.py" % v)
        if not os.path.isfile(p):
            continue
        m = importlib.import_module("_res_ai_%s" % v)
        for r in getattr(m, "RES_AI", []):
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
        if r.get("type") not in E.RES_TYPES:
            errs.append("%s type 越界: %s" % (iid, r.get("type")))
            continue
        if not r.get("raw"):
            errs.append("%s 缺 raw" % iid)
        elif r["raw"] not in reg[iid]["norm"]:
            warns.append("GAP %s raw 未命中原文: %s" % (iid, r["raw"]))
        recs.append(
            {
                "item_id": iid,
                "slot": r.get("slot", 0),
                "name": r.get("name", r.get("type")),
                "type": r["type"],
                "place": r.get("place", ""),
                "site": r.get("site", ""),
                "importance": r.get("importance", ""),
                "raw": r.get("raw", ""),
                "_vol": r["_vol"],
            }
        )

    for v in vols:
        vrecs = sorted(
            [x for x in recs if x["_vol"] == v], key=lambda x: (x["item_id"], x["slot"])
        )
        C.assign_ids(vrecs, C.ID_PREFIX["res"], v)
        C.save_layer("ress", v, [{k: x[k] for k in x if k != "_vol"} for x in vrecs])
    for r in recs:
        r.pop("_vol", None)

    C.atomic_write_json(
        os.path.join(C.ROOT, "_data", "res", "归一_汇总.json"),
        {"records": sorted(recs, key=lambda x: x["id"])},
    )

    rep = [
        "=== RES 资源层构建报告 ===",
        "卷: %s" % ",".join(vols),
        "记录: %d" % len(recs),
        "",
        "--- type 分布 ---",
    ]
    tc = {}
    for r in recs:
        tc[r["type"]] = tc.get(r["type"], 0) + 1
    for k, v in sorted(tc.items(), key=lambda x: -x[1]):
        rep.append("  %-8s %d" % (k, v))
    rep.append("")
    rep.append("--- ERR (%d) ---" % len(errs))
    rep += ["  " + e for e in errs[:50]]
    rep.append("--- GAP raw 未命中原文 (%d) ---" % len(warns))
    rep += ["  " + w for w in warns[:50]]
    C.atomic_write_text(
        os.path.join(C.ROOT, "_data", "res", "验证缺漏清单.txt"),
        "\n".join(["ERR %d / GAP %d" % (len(errs), len(warns))] + errs + warns) + "\n",
    )
    out = os.path.join(C.ROOT, "_res_report.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")
    print("OK res=%d ERR=%d GAP=%d -> %s" % (len(recs), len(errs), len(warns), out))


if __name__ == "__main__":
    main()
