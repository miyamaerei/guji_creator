# -*- coding: utf-8 -*-
"""
L1 实体层打包器（地理志版）：源数据 slot/解读 -> GAP 校验 + ID 分配 + 归一 + 主键表。
用法：python build_ent.py [--volumes 01,03]
源数据：scripts/_ents_ai_NN.py  形如 ENTITIES = [{"slot":1,"item_id":"01-001","text":..,"type":..}]
ID：ENT- 全局顺序（ENT-0001 起，不分卷段——SKILL.md §2.7）。
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
        p = os.path.join(HERE, "_ents_ai_%s.py" % v)
        if not os.path.isfile(p):
            continue
        m = importlib.import_module("_ents_ai_%s" % v)
        for r in getattr(m, "ENTITIES", []):
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
    ann = []
    for r in raw:
        iid = r.get("item_id")
        if iid not in reg:
            errs.append("item_id 不存在: %s" % iid)
            continue
        t = r.get("type")
        if t not in E.ENTITY_TYPES:
            errs.append("%s type 越界: %s" % (iid, t))
            continue
        if r.get("text") not in reg[iid]["norm"]:
            warns.append("GAP %s text 未命中原文(norm): %s" % (iid, r.get("text")))
        ann.append(
            {
                "item_id": iid,
                "text": r["text"],
                "type": t,
                "volume": r["_vol"],
                "slot": r.get("slot", 0),
                "count": r.get("count", 1),
                "provenance": r.get("provenance", ""),
            }
        )

    # ---- 全局归一：同名同类型合并（词形 -> 归一实体）----
    inv = {}
    for a in ann:
        k = (a["text"], a["type"])
        if k not in inv:
            inv[k] = {
                "normalized": a["text"],
                "type": a["type"],
                "count": 0,
                "first_source": a["item_id"],
                "surfaces": set(),
            }
        inv[k]["count"] += a.get("count", 1)
        inv[k]["surfaces"].add(a["text"])

    # ---- 主键表：ENT 全局顺序 ----
    ents = []
    ent_id = {}
    for i, (k, v) in enumerate(
        sorted(inv.items(), key=lambda x: (-x[1]["count"], x[1]["normalized"])), 1
    ):
        eid = "ENT-%04d" % i
        ent_id[k] = eid
        ents.append(
            {
                "ent_id": eid,
                "normalized": v["normalized"],
                "type": v["type"],
                "count": v["count"],
                "first_source": v["first_source"],
                "surfaces": sorted(v["surfaces"]),
            }
        )

    alias = {}
    for a in ann:
        alias[a["text"]] = ent_id[(a["text"], a["type"])]

    for a in ann:
        a["id"] = ent_id[(a["text"], a["type"])]

    # ---- 每卷写盘（增量合并语义）----
    for v in vols:
        recs = [a for a in ann if a["volume"] == v]
        recs.sort(key=lambda x: (x["item_id"], x["slot"]))
        C.save_layer("ents", v, recs)

    # ---- 汇总写盘 ----
    C.atomic_write_json(
        os.path.join(C.ROOT, "_data", "ent", "归一_汇总.json"),
        {
            "normalized_inventory": [
                {**vv, "surfaces": sorted(vv["surfaces"])}
                for _, vv in sorted(inv.items(), key=lambda x: -x[1]["count"])
            ]
        },
    )
    C.atomic_write_json(
        os.path.join(C.ROOT, "_data", "ent", "实体_主键表.json"),
        {"entities": ents, "alias_index": alias},
    )

    rep = [
        "=== L1 实体层构建报告 ===",
        "卷: %s" % ",".join(vols),
        "标注记录: %d" % len(ann),
        "归一实体: %d" % len(ents),
        "主键范围: %s ~ %s" % (ents[0]["ent_id"], ents[-1]["ent_id"])
        if ents
        else "主键范围: 无",
        "",
        "--- 类型分布 ---",
    ]
    tc = {}
    for e in ents:
        tc[e["type"]] = tc.get(e["type"], 0) + 1
    for k, v in sorted(tc.items(), key=lambda x: -x[1]):
        rep.append("  %-14s %d" % (k, v))
    rep.append("")
    rep.append("--- ERR (%d) ---" % len(errs))
    rep += ["  " + e for e in errs[:50]]
    rep.append("--- GAP text 未命中原文 (%d) ---" % len(warns))
    rep += ["  " + w for w in warns[:50]]

    C.atomic_write_text(
        os.path.join(C.ROOT, "_data", "ent", "验证缺漏清单.txt"),
        "\n".join(["ERR %d / GAP %d" % (len(errs), len(warns))] + errs + warns) + "\n",
    )
    out = os.path.join(C.ROOT, "_ent_report.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")
    print(
        "OK ent ann=%d uniq=%d ERR=%d GAP=%d -> %s"
        % (len(ann), len(ents), len(errs), len(warns), out)
    )


if __name__ == "__main__":
    main()
