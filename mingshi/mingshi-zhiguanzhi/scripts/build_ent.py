# -*- coding: utf-8 -*-
"""
L1 实体层打包器：源数据 slot/解读 → original 注入 + ID 分配 + 归一 + 主键表。
用法：python build_ent.py [--volumes 01,02]
源数据：scripts/_ents_ai_NN.py  形如 ENTITIES = [{"slot":1,"item_id":"01-001","text":..,"type":..,"start":..,"end":..,"normalized":..,"confidence":..}]
"""
import argparse
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C
import _kg_enums as E

VOLS = ["01", "02", "03", "04", "05"]


def collect(vols):
    """
    收集指定卷的源数据：按卷动态 import `_ents_ai_NN`。
    另支持**补充分片** `_ents_ai_NNb`（如 `_ents_ai_01b.py`）—— 同一卷的续做部分，
    用于分批推进大卷（卷01 条21–53 即以此为补充片），归属卷号仍取 NN。
    """
    out = []
    for v in vols:
        names = ["_ents_ai_%s" % v, "_ents_ai_%sb" % v]
        for name in names:
            p = os.path.join(C.SCRIPTS, name + ".py")
            if not os.path.isfile(p):
                continue
            m = importlib.import_module(name)
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
    ann = []          # 标注记录
    for r in raw:
        iid = r.get("item_id")
        if iid not in reg:
            errs.append("item_id 不存在: %s" % iid)
            continue
        t = r.get("type")
        if t not in E.ENTITY_TYPES:
            errs.append("%s type 越界: %s" % (iid, t))
            continue
        # text 必须逐字命中原文（GAP 检查）
        if r["text"] not in reg[iid]["original"]:
            warns.append("GAP %s text 未命中原文: %s" % (iid, r["text"]))
        ann.append({
            "item_id": iid, "text": r["text"], "type": t,
            "start": r.get("start", -1), "end": r.get("end", -1),
            "normalized": r.get("normalized", r["text"]),
            "confidence": r.get("confidence", 0.9),
            "volume": r["_vol"],
        })

    # ---- 全局归一 ----
    inv = {}
    for a in ann:
        k = (a["normalized"], a["type"])
        if k not in inv:
            inv[k] = {"normalized": a["normalized"], "type": a["type"],
                      "count": 0, "first_source": a["item_id"], "surfaces": set()}
        inv[k]["count"] += 1
        inv[k]["surfaces"].add(a["text"])

    # ---- 主键表：全局顺序 ENT-0001 起（同 lgs/xzl/ppy 先例）----
    ent_id = {}
    ents = []
    for i, (k, v) in enumerate(sorted(inv.items(), key=lambda x: (-x[1]["count"], x[1]["normalized"])), 1):
        eid = "ENT-%04d" % i
        ent_id[k] = eid
        ents.append({"ent_id": eid, "normalized": v["normalized"], "type": v["type"],
                     "count": v["count"], "first_source": v["first_source"],
                     "surfaces": sorted(v["surfaces"])})

    alias = {}
    for a in ann:
        alias[a["text"]] = ent_id[(a["normalized"], a["type"])]
        alias.setdefault(a["normalized"], ent_id[(a["normalized"], a["type"])])

    # ---- 回填 ent_id 到标注 ----
    for a in ann:
        a["ent_id"] = ent_id[(a["normalized"], a["type"])]

    # ---- 每卷写盘（增量合并语义）----
    for v in vols:
        recs = [a for a in ann if a["volume"] == v]
        recs.sort(key=lambda x: (x["item_id"], x["start"]))
        for r in recs:
            # ENT- id 是**实体主键**（同一实体多次出现共用同一 id，属设计如此）；
            # 标注记录自身的唯一定位靠 (item_id, start, end)。
            r["id"] = r.pop("ent_id")

        C.save_layer("ents", v, recs)

    # ---- 汇总写盘 ----
    C.atomic_write_json(os.path.join(C.ROOT, "_data", "ent", "归一_汇总.json"),
                        {"normalized_inventory": [
                            {**v, "surfaces": sorted(v["surfaces"])}
                            for _, v in sorted(inv.items(), key=lambda x: -x[1]["count"])]})
    C.atomic_write_json(os.path.join(C.ROOT, "_data", "ent", "实体_主键表.json"),
                        {"entities": ents, "alias_index": alias})

    rep = ["=== L1 实体层构建报告 ===",
           "卷: %s" % ",".join(vols),
           "标注记录: %d" % len(ann),
           "归一实体: %d" % len(ents),
           "主键范围: %s ~ %s" % (ents[0]["ent_id"], ents[-1]["ent_id"]) if ents else "主键范围: 无",
           "ENT 总数 == 产物唯一 ent_id: %s" % ("是" if len(ents) == len(set(a["id"] for a in ann)) or not ann else "否"),
           "",
           "--- 类型分布 ---"]
    tc = {}
    for e in ents:
        tc[e["type"]] = tc.get(e["type"], 0) + 1
    for k, v in sorted(tc.items(), key=lambda x: -x[1]):
        rep.append("  %-14s %d" % (k, v))
    rep.append("")
    rep.append("--- 高频实体 Top20 ---")
    for e in ents[:20]:
        rep.append("  %-10s %-12s %-10s count=%d" % (e["ent_id"], e["normalized"][:12], e["type"], e["count"]))
    rep.append("")
    rep.append("--- ERR (%d) ---" % len(errs))
    rep += ["  " + e for e in errs[:50]]
    rep.append("--- GAP text未命中原文 (%d，不计为错误但须复核) ---" % len(warns))
    rep += ["  " + w for w in warns[:50]]

    C.atomic_write_text(os.path.join(C.ROOT, "_data", "ent", "验证缺漏清单.txt"),
                        "\n".join(["ERR %d / GAP %d" % (len(errs), len(warns))] + errs + warns) + "\n")
    out = os.path.join(C.ROOT, "_ent_report.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")
    print("OK ent ann=%d uniq=%d ERR=%d GAP=%d -> %s" % (len(ann), len(ents), len(errs), len(warns), out))


if __name__ == "__main__":
    main()
