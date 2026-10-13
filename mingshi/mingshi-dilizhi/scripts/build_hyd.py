# -*- coding: utf-8 -*-
"""
HYD 水系河患打包器（地理志版）：水体条目 + 河患事件（决/淤/徙/塞/泛滥/改道/涸）。
用法：python build_hyd.py [--volumes 01,03]
源数据：scripts/_hyd_ai_NN.py  HYD_AI = [{slot,item_id,name,alt,type,flow,anchor,events[]}]
ID：DLZ-HYD-{卷×500+序号}。
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
        p = os.path.join(HERE, "_hyd_ai_%s.py" % v)
        if not os.path.isfile(p):
            continue
        m = importlib.import_module("_hyd_ai_%s" % v)
        for r in getattr(m, "HYD_AI", []):
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
        if r.get("type") not in E.HYD_TYPES:
            errs.append("%s type 越界: %s" % (iid, r.get("type")))
            continue
        if r.get("name") and reg.get(iid) and r["name"] not in reg[iid]["norm"]:
            warns.append("GAP %s name 未命中原文: %s" % (iid, r["name"]))
        if r.get("flow") and reg.get(iid) and r["flow"] not in reg[iid]["norm"]:
            warns.append("GAP %s flow 未命中原文: %s" % (iid, r["flow"][:20]))
        for ev in r.get("events", []) or []:
            if ev.get("kind") not in E.HYD_EVENTS:
                errs.append("%s events.kind 越界: %s" % (iid, ev.get("kind")))
            if (
                ev.get("era_raw")
                and ev["era_raw"] != "未明"
                and reg.get(iid)
                and ev["era_raw"] not in reg[iid]["norm"]
            ):
                warns.append(
                    "GAP %s events.era_raw 未命中原文: %s" % (iid, ev["era_raw"])
                )
        recs.append(
            {
                "item_id": iid,
                "slot": r.get("slot", 0),
                "name": r["name"],
                "alt": r.get("alt", ""),
                "type": r["type"],
                "flow": r.get("flow", ""),
                "anchor": r.get("anchor", {}),
                "events": r.get("events", []) or [],
                "_vol": r["_vol"],
            }
        )

    for v in vols:
        vrecs = sorted(
            [x for x in recs if x["_vol"] == v], key=lambda x: (x["item_id"], x["slot"])
        )
        C.assign_ids(vrecs, C.ID_PREFIX["hyd"], v)
        C.save_layer("hyds", v, [{k: x[k] for k in x if k != "_vol"} for x in vrecs])
    for r in recs:
        r.pop("_vol", None)

    C.atomic_write_json(
        os.path.join(C.ROOT, "_data", "hyd", "归一_汇总.json"),
        {"records": sorted(recs, key=lambda x: x["id"])},
    )

    rep = [
        "=== HYD 水系河患层构建报告 ===",
        "卷: %s" % ",".join(vols),
        "记录: %d" % len(recs),
        "含河患事件记录: %d" % sum(1 for r in recs if r.get("events")),
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
    rep.append("--- GAP (%d) ---" % len(warns))
    rep += ["  " + w for w in warns[:50]]
    C.atomic_write_text(
        os.path.join(C.ROOT, "_data", "hyd", "验证缺漏清单.txt"),
        "\n".join(["ERR %d / GAP %d" % (len(errs), len(warns))] + errs + warns) + "\n",
    )
    out = os.path.join(C.ROOT, "_hyd_report.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")
    print("OK hyd=%d errs=%d gaps=%d -> %s" % (len(recs), len(errs), len(warns), out))


if __name__ == "__main__":
    main()
