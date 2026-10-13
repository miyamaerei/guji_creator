# -*- coding: utf-8 -*-
"""
EVO 沿革阶段打包器（地理志版）：政区视角的阶段切片（与 TME 分工：EVO=阶段线，TME=事件点）。
用法：python build_evo.py [--volumes 01,03]
源数据：scripts/_evo_ai_NN.py  EVO_AI = [{slot,item_id,phase,era_raw,reign,year,change_type,change,owner}]
ID：DLZ-EVO-{卷×500+序号}。
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
        p = os.path.join(HERE, "_evo_ai_%s.py" % v)
        if not os.path.isfile(p):
            continue
        m = importlib.import_module("_evo_ai_%s" % v)
        for r in getattr(m, "EVO_AI", []):
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
        if r.get("change_type") not in E.EVO_TYPES:
            errs.append("%s change_type 越界: %s" % (iid, r.get("change_type")))
            continue
        if (
            r.get("reign")
            and r.get("reign") != "未明"
            and r.get("reign") not in E.REIGN_ORDER
        ):
            errs.append("%s reign 越界: %s" % (iid, r.get("reign")))
        if r.get("change") and reg.get(iid) and r["change"] not in reg[iid]["norm"]:
            warns.append("GAP %s change 未命中原文: %s" % (iid, r["change"][:20]))
        recs.append(
            {
                "item_id": iid,
                "slot": r.get("slot", 0),
                "phase": r.get("phase", 1),
                "era_raw": r.get("era_raw", "未明"),
                "reign": r.get("reign", "未明"),
                "year": r.get("year", 0),
                "change_type": r["change_type"],
                "change": r.get("change", ""),
                "owner": r.get("owner", ""),
                "_vol": r["_vol"],
            }
        )

    for v in vols:
        vrecs = sorted(
            [x for x in recs if x["_vol"] == v],
            key=lambda x: (x["item_id"], x["phase"]),
        )
        C.assign_ids(vrecs, C.ID_PREFIX["evo"], v)
        C.save_layer("evos", v, [{k: x[k] for k in x if k != "_vol"} for x in vrecs])
    for r in recs:
        r.pop("_vol", None)

    C.atomic_write_json(
        os.path.join(C.ROOT, "_data", "evo", "归一_汇总.json"),
        {"records": sorted(recs, key=lambda x: x["id"])},
    )

    rep = [
        "=== EVO 沿革阶段层构建报告 ===",
        "卷: %s" % ",".join(vols),
        "记录: %d" % len(recs),
        "",
        "--- change_type 分布 ---",
    ]
    tc = {}
    for r in recs:
        tc[r["change_type"]] = tc.get(r["change_type"], 0) + 1
    for k, v in sorted(tc.items(), key=lambda x: -x[1]):
        rep.append("  %-8s %d" % (k, v))
    rep.append("")
    rep.append("--- ERR (%d) ---" % len(errs))
    rep += ["  " + e for e in errs[:50]]
    rep.append("--- GAP (%d) ---" % len(warns))
    rep += ["  " + w for w in warns[:50]]
    C.atomic_write_text(
        os.path.join(C.ROOT, "_data", "evo", "验证缺漏清单.txt"),
        "\n".join(["ERR %d / GAP %d" % (len(errs), len(warns))] + errs + warns) + "\n",
    )
    out = os.path.join(C.ROOT, "_evo_report.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")
    print("OK evo=%d ERR=%d GAP=%d -> %s" % (len(recs), len(errs), len(warns), out))


if __name__ == "__main__":
    main()
