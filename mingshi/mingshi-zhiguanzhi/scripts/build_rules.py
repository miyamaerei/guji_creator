# -*- coding: utf-8 -*-
"""
L2 规则层打包器。
源数据：scripts/_rules_ai_NN.py → RULES = [{"slot","item_id","type","modals","condition","subject{text,subject_ent_ids}","action","object","purpose","punishment","confidence"}]
打包器职责：ID 分配 / original 注入 / 枚举校验 / 引用槽位校验（ent_id 必须存在）。
"""
import argparse
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C
import _kg_enums as E


def collect(vols):
    """收集规则源数据；支持补充分片 `_rules_ai_NNb`。"""
    out = []
    for v in vols:
        for name in ("_rules_ai_%s" % v, "_rules_ai_%sb" % v):
            if not os.path.isfile(os.path.join(C.SCRIPTS, name + ".py")):
                continue
            m = importlib.import_module(name)
            for r in getattr(m, "RULES", []):
                r["_vol"] = v
                out.append(r)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volumes", default=None)
    args = ap.parse_args()
    vols = C.iter_volumes(args.volumes)
    reg = C.load_registry()

    # 实体主键全集（引用槽位校验用）
    ents = set()
    p = os.path.join(C.ROOT, "_data", "ent", "实体_主键表.json")
    if os.path.isfile(p):
        import json
        with open(p, "r", encoding="utf-8") as f:
            ents = {e["ent_id"] for e in json.load(f)["entities"]}

    raw = collect(vols)
    errs, recs = [], []
    for r in raw:
        iid = r.get("item_id", "")
        if iid and iid not in reg:
            errs.append("item_id 不存在: %s" % iid)
        if r.get("type") not in E.RULE_TYPES:
            errs.append("%s RULE type 越界: %s" % (iid, r.get("type")))
        for m in r.get("modals", []) or []:
            if m not in E.RULE_MODALS:
                errs.append("%s modal 越界: %s" % (iid, m))
        subj = r.get("subject") or {}
        for eid in subj.get("subject_ent_ids", []) or []:
            if ents and eid not in ents:
                errs.append("%s subject_ent_ids 悬空: %s" % (iid, eid))
        recs.append(r)

    by_vol = {}
    for r in recs:
        r.setdefault("slot", 0)
        by_vol.setdefault(r["_vol"], []).append(r)
    for v, rs in by_vol.items():
        rs.sort(key=lambda x: (x["item_id"], x["slot"]))   # 确定性顺序，ID 与顺序绑定
        C.assign_ids(rs, E.ID_PREFIX["rule"], v, "rule_id")

    for v in vols:
        rs = [r for r in recs if r["_vol"] == v]
        out = []
        for r in rs:
            x = dict(r)
            # target 用 ID 引用；original 由打包器注入（AI 不手抄）
            x["original"] = reg.get(r["item_id"], {}).get("original", "")
            x["id"] = x.pop("rule_id")
            out.append(x)
        C.save_layer("rules", v, out)

    rep = ["=== L2 规则层构建报告 ===", "卷: %s" % ",".join(vols),
           "规则记录: %d" % len(recs), "", "--- 类型分布 ---"]
    tc = {}
    for r in recs:
        tc[r.get("type")] = tc.get(r.get("type"), 0) + 1
    for k, v in sorted(tc.items(), key=lambda x: -x[1]):
        rep.append("  %-8s %d" % (k, v))
    rep.append("")
    rep.append("--- ERR (%d) ---" % len(errs))
    rep += ["  " + e for e in errs[:80]]
    C.atomic_write_text(os.path.join(C.ROOT, "_data", "rule", "验证缺漏清单.txt"),
                        "\n".join(["ERR %d" % len(errs)] + errs) + "\n")
    out = os.path.join(C.ROOT, "_rule_report.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")
    print("OK rules=%d ERR=%d -> %s" % (len(recs), len(errs), out))


if __name__ == "__main__":
    main()
