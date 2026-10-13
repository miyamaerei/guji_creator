# -*- coding: utf-8 -*-
"""
TME 时间沿革层打包器（地理志版）。
用法：python build_tme.py [--volumes 01,03]
源数据：scripts/_tme_ai_NN.py  TME_AI = [{"slot","item_id","reign","year","era_raw","category","event","place"}]
ID：DLZ-TME-{卷×500+序号}（C.assign_ids 卷段位）。
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
        p = os.path.join(HERE, "_tme_ai_%s.py" % v)
        if not os.path.isfile(p):
            continue
        m = importlib.import_module("_tme_ai_%s" % v)
        for r in getattr(m, "TME_AI", []):
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
        if r.get("category") not in E.TME_CATEGORIES:
            errs.append("%s category 越界: %s" % (iid, r.get("category")))
            continue
        if (
            r.get("reign")
            and r.get("reign") != "未明"
            and r.get("reign") not in E.REIGN_ORDER
        ):
            errs.append("%s reign 越界: %s" % (iid, r.get("reign")))
            continue
        if not r.get("era_raw"):
            errs.append("%s 缺 era_raw" % iid)
            continue
        if r["era_raw"] != "未明" and r["era_raw"] not in reg[iid]["norm"]:
            warns.append("GAP %s era_raw 未命中原文: %s" % (iid, r["era_raw"]))
        recs.append(
            {
                "item_id": iid,
                "slot": r.get("slot", 0),
                "reign": r.get("reign", "未明"),
                "year": r.get("year", 0),
                "era_raw": r["era_raw"],
                "category": r["category"],
                "event": r.get("event", ""),
                "place": r.get("place", ""),
                "ent_ids": r.get("ent_ids", []),
                "related_evo": r.get("related_evo", ""),
                "_vol": r["_vol"],
            }
        )

    # ID 分配：按卷段位
    for v in vols:
        vrecs = sorted(
            [x for x in recs if x["_vol"] == v], key=lambda x: (x["item_id"], x["slot"])
        )
        C.assign_ids(vrecs, C.ID_PREFIX["tme"], v)
        C.save_layer("tmes", v, [{k: x[k] for k in x if k != "_vol"} for x in vrecs])
    for r in recs:
        r.pop("_vol", None)

    # 汇总（时间视角全量）
    C.atomic_write_json(
        os.path.join(C.ROOT, "_data", "tme", "归一_汇总.json"),
        {
            "records": sorted(
                recs, key=lambda x: E.time_key(x["reign"], x.get("year", 0))
            )
        },
    )

    rep = [
        "=== TME 时间沿革层构建报告 ===",
        "卷: %s" % ",".join(vols),
        "记录: %d" % len(recs),
        "",
        "--- 分类分布 ---",
    ]
    tc = {}
    for r in recs:
        tc[r["category"]] = tc.get(r["category"], 0) + 1
    for k, v in sorted(tc.items(), key=lambda x: -x[1]):
        rep.append("  %-8s %d" % (k, v))
    rep.append("")
    rep.append("--- ERR (%d) ---" % len(errs))
    rep += ["  " + e for e in errs[:50]]
    rep.append("--- GAP era_raw 未命中原文 (%d) ---" % len(warns))
    rep += ["  " + w for w in warns[:50]]
    C.atomic_write_text(
        os.path.join(C.ROOT, "_data", "tme", "验证缺漏清单.txt"),
        "\n".join(["ERR %d / GAP %d" % (len(errs), len(warns))] + errs + warns) + "\n",
    )
    out = os.path.join(C.ROOT, "_tme_report.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")
    print("OK tme=%d ERR=%d GAP=%d -> %s" % (len(recs), len(errs), len(warns), out))


if __name__ == "__main__":
    main()
