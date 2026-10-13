# -*- coding: utf-8 -*-
"""
L3 流程层 + APPT 任职层 + TME 时间沿革层 打包器（三小层合并，共用同一校验模式）。
源数据：_proc_ai_NN.py(PROCS) / _appt_ai_NN.py(APPTS) / _tme_ai_NN.py(TMES)
TME 另派生时间链 _views/timeline/<机构>.json（按 REIGN_ORDER 排序）。
"""
import argparse
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C
import _kg_enums as E


def collect(vols, mod, attr):
    """收集源数据；支持补充分片 `_<mod>_ai_NNb`。"""
    out = []
    for v in vols:
        for name in ("_%s_ai_%s" % (mod, v), "_%s_ai_%sb" % (mod, v)):
            if not os.path.isfile(os.path.join(C.SCRIPTS, name + ".py")):
                continue
            m = importlib.import_module(name)
            for r in getattr(m, attr, []):
                r["_vol"] = v
                out.append(r)
    return out


def load_ent_ids():
    import json
    p = os.path.join(C.ROOT, "_data", "ent", "实体_主键表.json")
    if not os.path.isfile(p):
        return set()
    with open(p, "r", encoding="utf-8") as f:
        return {e["ent_id"] for e in json.load(f)["entities"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volumes", default=None)
    args = ap.parse_args()
    vols = C.iter_volumes(args.volumes)
    reg = C.load_registry()
    ents = load_ent_ids()
    errs = []

    # ---------------- L3 流程 ----------------
    procs = collect(vols, "proc", "PROCS")
    for r in procs:
        iid = r.get("item_id", "")
        if iid and iid not in reg:
            errs.append("PROC item_id 不存在: %s" % iid)
        for s in r.get("steps", []) or []:
            ag = s.get("agent") or {}
            for eid in ag.get("agent_ent_ids", []) or []:
                if ents and eid not in ents:
                    errs.append("%s step%d agent_ent_ids 悬空: %s" % (iid, s.get("seq"), eid))
        # 步骤 seq 连续校验
        seqs = [s.get("seq") for s in r.get("steps", []) or []]
        if seqs != list(range(1, len(seqs) + 1)):
            errs.append("%s 步骤 seq 不连续: %s" % (iid, seqs))
    bv = {}
    for r in procs:
        r.setdefault("slot", 0)
        bv.setdefault(r["_vol"], []).append(r)
    for v, rs in bv.items():
        rs.sort(key=lambda x: (x["item_id"], x["slot"]))
        C.assign_ids(rs, E.ID_PREFIX["proc"], v, "process_id")
        # step_id 派生
        for r in rs:
            for i, s in enumerate(r["steps"], 1):
                s["step_id"] = "%s-%02d" % (r["process_id"].replace("ZG-P-", "P-"), i)
    for v in vols:
        rs = [r for r in procs if r["_vol"] == v]
        out = []
        for r in rs:
            x = dict(r)
            x["original"] = reg.get(r["item_id"], {}).get("original", "")
            x["id"] = x.pop("process_id")
            out.append(x)
        C.save_layer("procs", v, out)

    # ---------------- APPT ----------------
    appts = collect(vols, "appt", "APPTS")
    for r in appts:
        iid = r.get("item_id", "")
        if iid and iid not in reg:
            errs.append("APPT item_id 不存在: %s" % iid)
        if r.get("status") not in E.APPT_STATUS:
            errs.append("%s APPT status 越界: %s" % (iid, r.get("status")))
        for k in ("person", "office", "institution"):
            for eid in (r.get(k) or {}).get("ent_ids", []) or (r.get(k) or {}).get(k + "_ent_ids", []) or []:
                if ents and eid not in ents:
                    errs.append("%s %s ent_ids 悬空: %s" % (iid, k, eid))
    bv = {}
    for r in appts:
        r.setdefault("slot", 0)
        bv.setdefault(r["_vol"], []).append(r)
    for v, rs in bv.items():
        rs.sort(key=lambda x: (x["item_id"], x["slot"]))
        C.assign_ids(rs, E.ID_PREFIX["appt"], v, "appointment_id")
    for v in vols:
        rs = [r for r in appts if r["_vol"] == v]
        out = []
        for r in rs:
            x = dict(r)
            x["original"] = reg.get(r["item_id"], {}).get("original", "")
            x["id"] = x.pop("appointment_id")
            out.append(x)
        C.save_layer("appts", v, out)

    # ---------------- TME ----------------
    tmes = collect(vols, "tme", "TMES")
    for r in tmes:
        iid = r.get("item_id", "")
        if iid and iid not in reg:
            errs.append("TME item_id 不存在: %s" % iid)
        if r.get("category") not in E.TME_CATEGORIES:
            errs.append("%s TME category 越界: %s" % (iid, r.get("category")))
        era = r.get("era") or {}
        if era.get("reign") and era["reign"] not in E.REIGN_ORDER:
            errs.append("%s TME reign 越界: %s" % (iid, era["reign"]))
        if "order" not in era and era.get("reign"):
            era["order"] = E.reign_order(era["reign"])
    bv = {}
    for r in tmes:
        r.setdefault("slot", 0)
        bv.setdefault(r["_vol"], []).append(r)
    for v, rs in bv.items():
        rs.sort(key=lambda x: (x["item_id"], x["slot"]))
        C.assign_ids(rs, E.ID_PREFIX["tme"], v, "tme_id")
    for v in vols:
        rs = [r for r in tmes if r["_vol"] == v]
        out = []
        for r in rs:
            x = dict(r)
            x["original"] = reg.get(r["item_id"], {}).get("original", "")
            x["id"] = x.pop("tme_id")
            out.append(x)
        C.save_layer("tmes", v, out)

    # ---------------- 派生时间链 ----------------
    bytarget = {}
    for r in tmes:
        tname = (r.get("target") or {}).get("text", "未明")
        bytarget.setdefault(tname, []).append(r)
    tl_dir = os.path.join(C.VIEWS, "timeline")
    os.makedirs(tl_dir, exist_ok=True)
    tl_count = 0
    for tname, rs in bytarget.items():
        era = lambda x: x.get("era") or {}
        rs_sorted = sorted(rs, key=lambda x: E.time_key(era(x).get("reign", "未明"),
                                                        era(x).get("year", "未明")))
        chain = []
        for i, x in enumerate(rs_sorted, 1):
            e = era(x)
            chain.append({"seq": i,
                          "era": e.get("text", "未明"),
                          "reign": e.get("reign", "未明"),
                          "year": e.get("year", "未明"),
                          "category": x.get("category", "未明"),
                          "content": x.get("content", ""),
                          "tme_id": x.get("tme_id", ""),
                          "related_evo": x.get("related_evo", [])})
        obj = {"target": tname, "ent_ids": (rs_sorted[0].get("target") or {}).get("ent_ids", []),
               "chain": chain,
               "span": {"start": chain[0]["era"] if chain else "未明",
                        "end": chain[-1]["era"] if chain else "未明",
                        "count": len(chain)}}
        safe = "".join(ch if ch not in '\\/:*?"<>|' else "_" for ch in tname)
        C.atomic_write_json(os.path.join(tl_dir, "%s.json" % safe), obj)
        tl_count += 1

    rep = ["=== L3 流程 / APPT 任职 / TME 时间沿革 构建报告 ===", "卷: %s" % ",".join(vols),
           "流程记录: %d（步骤 %d）" % (len(procs), sum(len(r.get("steps", []) or []) for r in procs)),
           "任职记录: %d" % len(appts),
           "时间沿革记录: %d" % len(tmes),
           "派生时间链: %d 条（_views/timeline/）" % tl_count,
           "", "--- TME 分类分布 ---"]
    tc = {}
    for r in tmes:
        tc[r.get("category")] = tc.get(r.get("category"), 0) + 1
    for k, v in sorted(tc.items(), key=lambda x: -x[1]):
        rep.append("  %-10s %d" % (k, v))
    rep.append("")
    rep.append("--- APPT 状态分布 ---")
    ac = {}
    for r in appts:
        ac[r.get("status")] = ac.get(r.get("status"), 0) + 1
    for k, v in sorted(ac.items(), key=lambda x: -x[1]):
        rep.append("  %-8s %d" % (k, v))
    rep.append("")
    rep.append("--- ERR (%d) ---" % len(errs))
    rep += ["  " + e for e in errs[:80]]
    for c in ("proc", "appt", "tme"):
        C.atomic_write_text(os.path.join(C.ROOT, "_data", c, "验证缺漏清单.txt"),
                            "\n".join(["ERR %d" % len(errs)] + errs) + "\n")
    out = os.path.join(C.ROOT, "_proc_appt_tme_report.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")
    print("OK proc=%d appt=%d tme=%d chain=%d ERR=%d -> %s"
          % (len(procs), len(appts), len(tmes), tl_count, len(errs), out))


if __name__ == "__main__":
    main()
