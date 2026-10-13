# -*- coding: utf-8 -*-
"""
验证器：分层校验 + 跨层 ID 对齐审计 + 枚举口径。
区分结构性错误 ERR 与执行缺口 GAP（text 未逐字命中指纹库）。
验证结果写文件输出，不依赖 stdout（pitfalls #6）。
用法：python validate_layers.py [--volumes 01]
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C
import _kg_enums as E

LAYERS = [("ents", "id"), ("rules", "id"), ("procs", "id"),
          ("structs", "id"), ("appts", "id"), ("tmes", "id")]

ENT_FIELDS = {  # 各层内需校验的 ent 引用槽位
    "ents": [], "rules": ["subject_ent_ids"], "procs": ["agent_ent_ids"],
    "structs": ["ent_ids"], "appts": ["person_ent_ids", "official_ent_ids",
                                      "ent_ids"], "tmes": ["ent_ids"],
}


def deep_ent_ids(rec):
    """递归收集记录内所有 *_ent_ids / ent_ids 值"""
    out = []

    def walk(o, k=None):
        if isinstance(o, dict):
            for kk, vv in o.items():
                if kk.endswith("ent_ids") or kk == "ent_ids":
                    if isinstance(vv, list):
                        out.extend(vv)
                    elif vv:
                        out.append(vv)
                else:
                    walk(vv, kk)
        elif isinstance(o, list):
            for it in o:
                walk(it, k)
    walk(rec)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volumes", default=None)
    args = ap.parse_args()
    vols = C.iter_volumes(args.volumes)

    reg = C.load_registry()
    errs, gaps, stats = [], [], {}

    # ---- 实体主键表 ----
    ent_ids = set()
    p = os.path.join(C.ROOT, "_data", "ent", "实体_主键表.json")
    if os.path.isfile(p):
        with open(p, "r", encoding="utf-8") as f:
            ent_ids = {e["ent_id"] for e in json.load(f)["entities"]}

    seen_ids = {}     # 全局 ID 判重
    all_recs = {}     # layer -> [rec]

    for v in vols:
        for (d, idf) in LAYERS:
            fp = os.path.join(C.LAYERS, d, "%s_%s.json" % (d, v))
            if not os.path.isfile(fp):
                continue
            with open(fp, "r", encoding="utf-8") as f:
                obj = json.load(f)
            if "records" not in obj:
                errs.append("%s/%s_%s.json 顶层键不是 records" % (d, d, v))
            recs = obj.get("records", [])
            all_recs.setdefault(d, []).extend(recs)
            stats.setdefault(d, 0)
            stats[d] += len(recs)

            for r in recs:
                rid = r.get(idf) or r.get("id")
                # ID 唯一性：
                #   ents 层的 `id` 是**实体主键 ENT-xxxx**，同一实体多次出现共用同一
                #   id，属设计如此（实体主键 ≠ 记录主键），**不做撞号校验**；其余层
                #   的记录 id 必须全局唯一。
                if rid and d != "ents":
                    if rid in seen_ids:
                        errs.append("ID 撞号: %s（%s 与 %s）" % (rid, d, seen_ids[rid]))
                    seen_ids[rid] = d
                # item_id 存在
                iid = r.get("item_id")
                if not iid:
                    errs.append("%s %s 缺 item_id" % (d, rid))
                elif iid not in reg:
                    errs.append("%s %s item_id 不存在: %s" % (d, rid, iid))
                # 引用槽位
                for eid in deep_ent_ids(r):
                    if ent_ids and eid not in ent_ids:
                        errs.append("%s %s 引用悬空 ent_id: %s" % (d, rid, eid))
                # GAP：text 字段须逐字命中原文
                for tk in ("text",):
                    t = r.get(tk)
                    if isinstance(t, str) and t and iid in reg:
                        if t not in reg[iid]["original"]:
                            gaps.append("%s %s %s='%s' 未命中原文" % (d, rid, tk, t))

                # ---- 各层枚举硬校验 ----
                if d == "ents":
                    if r.get("type") not in E.ENTITY_TYPES:
                        errs.append("ENT %s type 越界: %s" % (rid, r.get("type")))
                elif d == "rules":
                    if r.get("type") not in E.RULE_TYPES:
                        errs.append("RULE %s type 越界: %s" % (rid, r.get("type")))
                    for m in r.get("modals", []) or []:
                        if m not in E.RULE_MODALS:
                            errs.append("RULE %s modal 越界: %s" % (rid, m))
                elif d == "structs":
                    # 四维混装于同一 records；按存在字段分派。
                    # 分派顺序不可颠倒：ORG 节点也可能带 posts[]（如 v7 升正的府/州/县），
                    # 若先判 "posts" in r 会把 ORG 误判为 RANK。ORG 的稳定标识是 children[]。
                    if "children" in r:   # ORG
                        if r.get("level") not in E.ORG_LEVELS:
                            errs.append("ORG %s level 越界: %s" % (rid, r.get("level")))
                    elif "change_type" in r:  # EVO
                        if r.get("change_type") not in E.EVO_TYPES:
                            errs.append("EVO %s change_type 越界: %s" % (rid, r.get("change_type")))
                    elif "line_type" in r:    # LINE
                        if r.get("line_type") not in E.LINE_TYPES:
                            errs.append("LINE %s line_type 越界: %s" % (rid, r.get("line_type")))
                    elif "posts" in r:        # RANK
                        if r.get("rank_type") not in E.RANK_TYPES:
                            errs.append("RANK %s rank_type 越界: %s" % (rid, r.get("rank_type")))
                        prev = -1
                        for pst in r.get("posts", []):
                            if pst.get("count_form") not in E.COUNT_FORMS:
                                errs.append("RANK %s count_form 越界: %s" % (rid, pst.get("count_form")))
                            go = pst.get("grade_order", 99)
                            if go < prev:
                                errs.append("RANK %s posts 未按品级降序（%s 在 %s 后）"
                                            % (rid, pst.get("office"), prev))
                            prev = go
                            if pst.get("vacancy_type") not in E.VACANCY_TYPES:
                                errs.append("RANK %s vacancy_type 越界: %s" % (rid, pst.get("vacancy_type")))
                            if pst.get("post_status") not in E.POST_STATUS:
                                errs.append("RANK %s post_status 越界: %s" % (rid, pst.get("post_status")))
                            if pst.get("selection_route") not in E.SELECTION_ROUTES:
                                errs.append("RANK %s selection_route 越界: %s" % (rid, pst.get("selection_route")))
                    else:
                        errs.append("structs %s 无法识别维度" % rid)
                elif d == "appts":
                    if r.get("status") not in E.APPT_STATUS:
                        errs.append("APPT %s status 越界: %s" % (rid, r.get("status")))
                elif d == "tmes":
                    if r.get("category") not in E.TME_CATEGORIES:
                        errs.append("TME %s category 越界: %s" % (rid, r.get("category")))

    # ---- 浮点容差：collect-set 语义若要求精确，此处仅告警 ----
    rep = []
    rep.append("=== 分层验证报告 ===")
    rep.append("卷: %s" % ",".join(vols))
    rep.append("指纹库条目: %d" % len(reg))
    rep.append("")
    rep.append("--- 各层记录数 ---")
    tot = 0
    for (d, _) in LAYERS:
        n = stats.get(d, 0)
        tot += n
        rep.append("  %-8s %d" % (d, n))
    rep.append("  合计     %d" % tot)
    rep.append("")
    rep.append("--- 全局 ID 唯一 ---")
    rep.append("  已分配 ID: %d / 唯一: %d" % (len(seen_ids), len(set(seen_ids))))
    rep.append("")
    rep.append("--- 结构性错误 ERR (%d) ---" % len(errs))
    rep += ["  " + e for e in errs[:120]]
    if len(errs) > 120:
        rep.append("  … 共 %d 条，见文件" % len(errs))
    rep.append("")
    rep.append("--- 执行缺口 GAP（text 未命中原文）(%d) ---" % len(gaps))
    rep += ["  " + g for g in gaps[:60]]
    rep.append("")
    rep.append("=== 结论: ERR=%d GAP=%d ===" % (len(errs), len(gaps)))

    out = os.path.join(C.ROOT, "验证缺漏清单.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")
    print("ERR=%d GAP=%d -> %s" % (len(errs), len(gaps), out))


if __name__ == "__main__":
    main()
