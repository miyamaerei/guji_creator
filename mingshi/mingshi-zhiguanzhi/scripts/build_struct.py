# -*- coding: utf-8 -*-
"""
L4 结构化层打包器（四维 ORG/RANK/LINE/EVO）+ v3 员额置信度。
源数据：scripts/_struct_ai_NN.py
  ORGS  = [{"slot","item_id","name","level","org_type","parent","core_officials","total_posts","note","children":[...],"ent_ids","confidence"}]
  RANKS = [{"slot","item_id","owner","rank_type","posts":[{office,office_parts,count,grade,note,...}],"ent_ids","confidence"}]
  LINES = [{"slot","item_id","subordinate","superior","line_type","level_gap","note","ent_ids","confidence"}]
  EVOS  = [{"slot","item_id","era","change_type","content","related_tme","ent_ids","confidence"}]
打包器职责（AI 不写）：ID 分配 / original 注入 / RANK posts 排序 / 置信度派生 / 树与边一致性校验。
"""
import argparse
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C
import _kg_enums as E

LEVEL_RANK = {"中枢": 0, "部": 1, "院": 1, "寺": 1, "监": 1, "内府": 1, "京营": 1,
              "布政按察": 1, "王府": 1, "府": 1,      # 府=宗人府/顺天府等中央机构层
              "差遣": 1,                             # v4：总督/巡抚等差遣，直隶天子
              "司": 2, "卫": 2, "都司卫所": 2, "土司": 2, "州县": 2,
              "局": 3, "库": 3, "所": 3, "其他": 9}
# v8（卷05 实测）：锦衣卫「五所→十司」为合法下辖（原文：五所分銮舆…十司）。
# 所与司在本书中互为上下（都司→卫→所，卫所→司），层级不可单向排序，
# 故 level_ok 对 {所,司} 组合放行（见 level_ok_special）。


def level_ok(parent_level, child_level):
    """
    层级合法性：子层级须**不高于**父层级（非递减判定）。
    特例（卷03 实测）：`宦官(内府)` → `十二监(监)`、`太仆寺(寺)` → `各牧监(监)`
    属于「同级机构群」而非下辖机构，`监` 在此兼任"二级集合"角色。
    为兼顾，采用**非递减**判定：子层级 ≥ 父层级即合法（同层允许）。

    v8（卷05 实测）：`所` ↔ `司` 互为上下，不可单向排序 ——
      锦衣卫五所（所）→ 十司（司）：所 在上、司 在下；
      都指挥使司（司/都司卫所）→ 卫（卫）→ 千户所（所）：司 在上、所 在下。
    故二者组合一律放行。
    """
    if {parent_level, child_level} == {"所", "司"}:
        return True
    return LEVEL_RANK.get(child_level, 9) >= LEVEL_RANK.get(parent_level, 0)


def collect(vols, attr):
    """收集结构化源数据；支持补充分片 `_struct_ai_NNb`。"""
    out = []
    for v in vols:
        for name in ("_struct_ai_%s" % v, "_struct_ai_%sb" % v):
            if not os.path.isfile(os.path.join(C.SCRIPTS, name + ".py")):
                continue
            m = importlib.import_module(name)
            for r in getattr(m, attr, []):
                r["_vol"] = v
                out.append(r)
    return out


def norm_posts(posts, item_id, errs):
    """规范化 posts[]：补字段 + 派生置信度 + 排序（品高→低）

    v6：若元素含 `link_to_bj.grade_ref`，则 `grade_order` 取自该北京实际品级
        （用户 2026-10-14 决定：南京官 grade 记"同北京"，grade_order 取北京实际值）。
    """
    out = []
    for p in posts:
        office = p.get("office", "")
        grade = p.get("grade", "未明")
        cnt = p.get("count", 0)
        if not isinstance(cnt, int):
            try:
                cnt = int(cnt)
            except Exception:
                errs.append("%s count 非整数: %r" % (item_id, cnt))
                cnt = 0
        form = p.get("count_form", "未明")
        if form not in E.COUNT_FORMS:
            errs.append("%s count_form 越界: %s" % (item_id, form))
            form = "未明"
        conf = p.get("count_confidence")
        if conf is None:
            conf = E.count_confidence(form)
        if not (0.0 <= float(conf) <= 1.0):
            errs.append("%s count_confidence 越界: %r" % (item_id, conf))
            conf = 0.0
        vneed = E.need_verify(form, float(conf))
        parts = p.get("office_parts", []) or []
        if not isinstance(parts, list):
            parts = [parts]

        # ---- v6：grade_order 派生（南京官取北京实际品级值）----
        link = p.get("link_to_bj") or {}
        grade_ref = link.get("grade_ref")
        if grade_ref and grade_ref in E.GRADE_ORDER:
            g_order = E.grade_order(grade_ref)
        else:
            g_order = E.grade_order(grade)

        out.append({
            "office": office,
            "office_parts": parts,
            "count": cnt,
            "grade": grade,
            "grade_order": g_order,
            "count_form": form,
            "count_confidence": float(conf),
            "verify_needed": vneed,
            "verify_reason": p.get("verify_reason", "未明"),
            "count_evidence": p.get("count_evidence", "未明"),
            "note": p.get("note", "未明"),
            # v6：南京官→北京节点关联（其他条目为空 dict）
            "link_to_bj": link,
            # v3 扩展 12 项
            "vacancy_type": p.get("vacancy_type", "未明"),
            "is_concurrent": bool(p.get("is_concurrent", False)),
            "post_status": p.get("post_status", "未明"),
            "grade_note": p.get("grade_note", "未明"),
            "selection_route": p.get("selection_route", "未明"),
            "succession": bool(p.get("succession", False)),
            "era_validity": p.get("era_validity", {"from": "未明", "to": "未明"}),
            "original_span": p.get("original_span", None),
            "rank_grade_raw": p.get("rank_grade_raw", grade),
            "salary_ref": p.get("salary_ref", "未明"),
        })
        # 枚举硬校验（缺省"未明"不报）
        if out[-1]["vacancy_type"] not in E.VACANCY_TYPES:
            errs.append("%s vacancy_type 越界: %s" % (item_id, out[-1]["vacancy_type"]))
        if out[-1]["post_status"] not in E.POST_STATUS:
            errs.append("%s post_status 越界: %s" % (item_id, out[-1]["post_status"]))
        if out[-1]["selection_route"] not in E.SELECTION_ROUTES:
            errs.append("%s selection_route 越界: %s" % (item_id, out[-1]["selection_route"]))
    out.sort(key=lambda p: (p["grade_order"], -p["count"], p["office"]))
    return out


def walk_tree(node, fn, parent_name=None):
    fn(node, parent_name)
    for c in node.get("children", []) or []:
        walk_tree(c, fn, node.get("name"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volumes", default=None)
    args = ap.parse_args()
    vols = C.iter_volumes(args.volumes)
    reg = C.load_registry()
    errs = []

    orgs = collect(vols, "ORGS")
    ranks = collect(vols, "RANKS")
    lines_ = collect(vols, "LINES")
    evos = collect(vols, "EVOS")

    # ---------- v9：全书性专表（卷00）----------
    # 散阶/勋级/俸禄三类品级专表，源数据在 _struct_ai_00.py（不属任何正文条目）。
    _ex = []
    if os.path.isfile(os.path.join(C.SCRIPTS, "_struct_ai_00.py")):
        _m0 = importlib.import_module("_struct_ai_00")
        for r in getattr(_m0, "RANKS_EX", []):
            r["_vol"] = "00"
            _ex.append(r)
    ranks = _ex + ranks

    # ---------- ORG ----------
    org_recs, tree_edges = [], set()
    for r in orgs:
        iid = r.get("item_id", "")
        if iid and iid not in reg:
            errs.append("ORG item_id 不存在: %s" % iid)
        lvl = r.get("level")
        if lvl not in E.ORG_LEVELS:
            errs.append("%s ORG level 越界: %s" % (iid, lvl))
        def check(node, parent_name):
            nm, lv, par = node.get("name"), node.get("level"), node.get("parent")
            if lv not in E.ORG_LEVELS:
                errs.append("%s ORG 子节点 level 越界: %s" % (iid, lv))
            if parent_name is not None and par != parent_name:
                errs.append("%s ORG 父子不一致: %s.parent=%s 应为 %s" % (iid, nm, par, parent_name))
            if parent_name is not None:
                tree_edges.add((nm, parent_name))
            for c in node.get("children", []) or []:
                # 子层级须不低于父层级（非递减；同层允许——宦官→十二监 属同级机构群）
                if not level_ok(lv, c.get("level")):
                    errs.append("%s ORG 层级非法: %s(%s) -> %s(%s)" % (iid, nm, lv, c.get("name"), c.get("level")))
                check(c, nm)
        check(r, None)
        org_recs.append(r)

    by_vol = {}
    for r in org_recs:
        r.setdefault("slot", 0)
        by_vol.setdefault(r["_vol"], []).append(r)
    for v, rs in by_vol.items():
        rs.sort(key=lambda x: (x["item_id"], x["slot"]))
        C.assign_ids(rs, E.ID_PREFIX["org"], v, "org_id")

    # ---------- RANK ----------
    rank_recs = []
    for r in ranks:
        iid = r.get("item_id", "")
        # "00-" 前缀为全书性专表（虚设 item_id），不属任何正文条目
        if iid and not iid.startswith("00-") and iid not in reg:
            errs.append("RANK item_id 不存在: %s" % iid)
        r["posts"] = norm_posts(r.get("posts", []), iid, errs)
        r["total"] = sum(p["count"] for p in r["posts"])
        if r.get("rank_type") not in E.RANK_TYPES:
            errs.append("%s RANK rank_type 越界: %s" % (iid, r.get("rank_type")))
        rank_recs.append(r)
    by_vol = {}
    for r in rank_recs:
        r.setdefault("slot", 0)
        by_vol.setdefault(r["_vol"], []).append(r)
    for v, rs in by_vol.items():
        rs.sort(key=lambda x: (x["item_id"], x["slot"]))
        C.assign_ids(rs, E.ID_PREFIX["rank"], v, "rank_id")

    # ---------- v9 第 3 项：posts 逐条回填 ----------
    # 规则化回填（世官九等 / 流官八等 / 寄禄 / 岁禄表），命中即填、不命中留未明。
    # 每条回填附 *_evidence，便于溯源与推翻。详见 scripts/_post_backfill.py。
    import _post_backfill as BF
    n_route = n_salary = 0
    for r in rank_recs:
        if r.get("rank_type") != "品级员额":
            continue
        _iid = r.get("item_id", "")
        # scope_text：条目原文首段，供 _post_backfill 判定「世官九等/流官八等」语域
        _scope = ""
        if _iid in reg:
            _scope = (reg[_iid].get("original") or "")[:400]
        a, b = BF.backfill(r["posts"], owner=r.get("owner", ""),
                           item_id=_iid, scope_text=_scope)
        n_route += a
        n_salary += b

    # ---------- LINE ----------
    line_recs = []
    for r in lines_:
        iid = r.get("item_id", "")
        if iid and iid not in reg:
            errs.append("LINE item_id 不存在: %s" % iid)
        if r.get("line_type") not in E.LINE_TYPES:
            errs.append("%s LINE line_type 越界: %s" % (iid, r.get("line_type")))
        line_recs.append(r)
    by_vol = {}
    for r in line_recs:
        r.setdefault("slot", 0)
        by_vol.setdefault(r["_vol"], []).append(r)
    for v, rs in by_vol.items():
        rs.sort(key=lambda x: (x["item_id"], x["slot"]))
        C.assign_ids(rs, E.ID_PREFIX["line"], v, "line_id")

    # ---------- LINE ↔ ORG 树内边一致性（排除跨树边 superior=="天子"）----------
    line_edges = set()
    cross_edges = set()
    for r in line_recs:
        e = (r.get("subordinate"), r.get("superior"))
        if r.get("superior") == "天子":
            cross_edges.add(e)
        else:
            line_edges.add(e)
    only_tree = tree_edges - line_edges
    only_line = line_edges - tree_edges
    for e in sorted(only_tree):
        errs.append("树内边仅 ORG 有: %s->%s" % e)
    for e in sorted(only_line):
        errs.append("树内边仅 LINE 有: %s->%s" % e)

    # ---------- EVO ----------
    evo_recs = []
    for r in evos:
        iid = r.get("item_id", "")
        if iid and iid not in reg:
            errs.append("EVO item_id 不存在: %s" % iid)
        if r.get("change_type") not in E.EVO_TYPES:
            errs.append("%s EVO change_type 越界: %s" % (iid, r.get("change_type")))
        evo_recs.append(r)
    by_vol = {}
    for r in evo_recs:
        r.setdefault("slot", 0)
        by_vol.setdefault(r["_vol"], []).append(r)
    for v, rs in by_vol.items():
        rs.sort(key=lambda x: (x["item_id"], x["slot"]))
        C.assign_ids(rs, E.ID_PREFIX["evo"], v, "evo_id")

    # ---------- 逐卷写盘 ----------
    # v9：写盘卷序须含 "00"（全书性专表），否则卷00 的散阶/勋级/俸禄记录只在内存中
    #     参与计数却永不落盘（首跑实测：RANK=104 但 _layers/structs 仅 01–05）。
    n_post = 0
    for v in sorted(set(vols) | {"00"}):
        o = [r for r in org_recs if r["_vol"] == v]
        k = [r for r in rank_recs if r["_vol"] == v]
        n_post += sum(len(r["posts"]) for r in k)
        l = [r for r in line_recs if r["_vol"] == v]
        e = [r for r in evo_recs if r["_vol"] == v]
        recs = []
        for r in o:
            x = dict(r); x["id"] = x.pop("org_id"); recs.append(x)
        for r in k:
            x = dict(r); x["id"] = x.pop("rank_id"); recs.append(x)
        for r in l:
            x = dict(r); x["id"] = x.pop("line_id"); recs.append(x)
        for r in e:
            x = dict(r); x["id"] = x.pop("evo_id"); recs.append(x)
        C.save_layer("structs", v, recs)

    # ---------- v7：机构模板容器已取消 ----------
    # 原 v6 的 ORG_TEMPLATES / TPL- 命名空间 / templates 层于 2026-10-14 删除。
    # 用户裁定：府/州/县/道/儒学/杂职等首先是正式机构，应在 ORG 树中占节点；
    # 「通用编制」只是其编制可复用的额外属性。原 17 条模板已全部转为 ORGS 正式节点，
    # 其 posts 转入 ORG 节点、品级员额补入 RANKS、隶属边补入 LINES。
    # 若仍有源文件导出 ORG_TEMPLATES，直接报错以免静默丢弃数据。
    _stray = collect(vols, "ORG_TEMPLATES")
    if _stray:
        errs.append("ORG_TEMPLATES 已废弃（v7 取消模板容器），但源文件仍导出 %d 条——请转为 ORGS 节点" % len(_stray))

    # ---------- 待核清单（V2 治理组件）----------
    need = [(r.get("owner", ""), p) for r in rank_recs for p in r["posts"] if p["verify_needed"]]
    csv = ["owner,office,count,grade,count_form,count_confidence,verify_reason,item_id"]
    for owner, p in need:
        csv.append("%s,%s,%d,%s,%s,%.2f,%s,%s" % (
            owner, p["office"], p["count"], p["grade"], p["count_form"],
            p["count_confidence"], str(p["verify_reason"]).replace(",", "；"), ""))
    C.atomic_write_text(os.path.join(C.ROOT, "_data", "struct", "verify_needs_review.csv"),
                        "\n".join(csv) + "\n")

    rep = ["=== L4 结构化层构建报告 ===", "卷: %s" % ",".join(vols),
           "ORG 记录: %d" % len(org_recs), "RANK 记录: %d（posts 元素 %d）" % (len(rank_recs), n_post),
           "LINE 记录: %d（树内边 %d / 跨树边 %d）" % (len(line_recs), len(line_edges), len(cross_edges)),
           "EVO 记录: %d" % len(evo_recs),
           "树内边一致: %s" % ("是" if not only_tree and not only_line else "否"),
           "待核 posts: %d" % len(need),
           "v9 回填: selection_route %d / salary_ref %d" % (n_route, n_salary), "",
           "--- count_form 分布 ---"]
    fd = {}
    for r in rank_recs:
        for p in r["posts"]:
            fd[p["count_form"]] = fd.get(p["count_form"], 0) + 1
    for k, v2 in sorted(fd.items()):
        rep.append("  %-4s %d" % (k, v2))
    rep.append("")
    rep.append("--- ERR (%d) ---" % len(errs))
    rep += ["  " + e for e in errs[:80]]
    C.atomic_write_text(os.path.join(C.ROOT, "_data", "struct", "验证缺漏清单.txt"),
                        "\n".join(["ERR %d" % len(errs)] + errs) + "\n")
    out = os.path.join(C.ROOT, "_struct_report.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")
    print("OK ORG=%d RANK=%d posts=%d LINE=%d EVO=%d ERR=%d -> %s"
          % (len(org_recs), len(rank_recs), n_post, len(line_recs), len(evo_recs), len(errs), out))


if __name__ == "__main__":
    main()
