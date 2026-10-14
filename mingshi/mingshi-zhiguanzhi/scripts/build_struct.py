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
#
# v12（缺口2 内阁归翰林院）：`中枢` 虽在 LEVEL_RANK 中为 0（最高），但内阁
# 由翰林官入直而生、隶翰林院，故 `翰林院(院=1) -> 内阁(中枢=0)` 会触发严格排序告警。
# 这与 v5「监/内府 兼任同级机构群」、v8「所/司 互为上下」同源：
# LEVEL_RANK 是**机构地位的粗略序**，不是**树深的严格约束**。
# 处置同 v8 —— 在 level_ok 中对 {院,中枢} 组合放行（内阁是本书记载中唯一的此类特例）。


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

    v12（缺口2）：`院` ↔ `中枢` 组合放行 —— 内阁（中枢）隶翰林院（院），
    内阁由翰林官入直而生（01-018「永乐初，选翰林官入直内阁」），是本书唯一特例。
    """
    if {parent_level, child_level} == {"所", "司"}:
        return True
    if {parent_level, child_level} == {"院", "中枢"}:
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

    # ---------- v10：ORG 子节点分配 id ----------
    # 关键缺陷（v10 前）：assign_ids 只作用于**顶层记录**，`children[]` 内的子机构
    # 从未拿到 id —— 子机构在结构上「无名」，导致
    #   ① 官职层无法把子机构所属的职官挂上去（org_id 为空）
    #   ② 跨树引用（如南京官 link_to_bj 指北京子机构）只能靠名字匹配，同名即歧义
    # 修法：按「父 id + 子序号」派生稳定 id（`ORG-505#3`），保证幂等且可读。
    # 选择 `#` 分隔而非新序号段的原因：子机构数量与卷序无关（同一条目内动态），
    # 独立编号会因条目增删而全段漂移；父派生编号则稳定。
    def _assign_child_ids(node):
        for i, c in enumerate(node.get("children") or [], 1):
            if not c.get("id"):
                pid = node.get("id") or ""
                c["id"] = "%s#%d" % (pid, i) if pid else ""
            _assign_child_ids(c)
    for r in org_recs:
        if not r.get("id"):
            r["id"] = r.get("org_id") or ""
        _assign_child_ids(r)

    # ---------- v10：posts 回填 org_id ----------
    # 官职层（C15）需要「这条职官属于哪个机构」的直接指针。
    # ORG 节点的 posts[] 与节点同属一个机构，但 posts 元素本身没有机构字段，
    # 导致官职层只能靠 (org_name, office) 二级匹配、且无法区分同名机构
    # （如 右侍郎@兵部 / 右侍郎@南京兵部）。
    # 此处按节点递归展开，把**节点自身 id**写进每个 post 的 org_id。
    # 子节点在同一次递归中各自覆盖，叶子节点不会继承父节点的 org_id。
    def _fill_org_id(node, node_id):
        for p in (node.get("posts") or []):
            p["org_id"] = node_id or ""
        for c in (node.get("children") or []):
            _fill_org_id(c, c.get("id") or "")
    for r in org_recs:
        _fill_org_id(r, r.get("org_id") or r.get("id") or "")

    # ---------- v11 第 4 项：ORG 节点回填印信（seal）----------
    # 原文第 3 行「礼部……凡诸司之印信，领其制度」后接一段**全书性印信表**：
    # 按品级列各衙门所用印/关防/条记的材质·钮式·尺寸·篆文。
    # 该表与单条机构无关，属「全书性专表」，在此按机构名归一后回填到 ORG 节点。
    # 差遣官（总督/巡抚等）用「铜关防」，随 tie 未列于表内者留空——不臆造。
    import _seal_backfill as SB
    n_seal, n_map, (n_q, n_j) = SB.backfill(org_recs, reg, errs)
    # 递归下探子节点：子机构（如 六部各司 / 各卫千户所）同样在表内出现
    _SEAL_MAP = SB.collect_seal_map("\n".join(t for _, t in C.read_source_lines()))

    def _fill_seal(node):
        for c in (node.get("children") or []):
            if not c.get("seal"):
                s = _SEAL_MAP.get(c.get("name"))
                if s:
                    cs = dict(s)
                    cs["confidence"] = 0.8
                    c["seal"] = cs
            _fill_seal(c)
    for r in org_recs:
        _fill_seal(r)

    # ---------- v11 第 1/3/5/6/7 项：ORG 节点回填权力/考核/文书/管辖/驻地 ----------
    # 逐条依据见 scripts/_attr_backfill.py 模块头（每字段注明原文出处）。
    # 无原文依据者留空 —— 不按品级推演、不臆造。
    import _attr_backfill as AB
    _attr_cnt = AB.backfill(org_recs, errs)

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

    # ---------- v10：RANK 记录回填 owner_org_id ----------
    # RANK 的 owner 是机构名（可能与 ORG 节点同名多义），需要显式指向 ORG 节点 id。
    # 匹配优先级：① 同 item_id 的 ORG 节点 ② 同名 ORG 节点 ③ 留空。
    _by_item = {}
    _by_name = {}
    def _idx_org(node):
        if node.get("id"):
            if node.get("item_id"):
                _by_item.setdefault(node["item_id"], []).append(node)
            if node.get("name"):
                _by_name.setdefault(node["name"], []).append(node)
        for c in (node.get("children") or []):
            _idx_org(c)
    for r in org_recs:
        _idx_org(r)
    for r in rank_recs:
        if r.get("rank_type") != "品级员额":
            continue
        _iid = r.get("item_id") or ""
        _own = r.get("owner") or ""
        pick = None
        if _iid and not _iid.startswith("00-"):
            cs = _by_item.get(_iid) or []
            pick = next((c for c in cs if c.get("name") == _own), cs[0] if cs else None)
        if pick is None and _own:
            cs = _by_name.get(_own) or []
            pick = next((c for c in cs if c.get("item_id") == _iid), cs[0] if cs else None)
        r["owner_org_id"] = pick.get("id") if pick else ""
        r["owner_org_name"] = pick.get("name") if pick else _own
        # posts[].org_id 回填：RANK 的职官同属 owner 机构。
        # ⚠ 必须与 ORG 节点 posts 用同一套 ID，否则官职层两侧对不上
        #   （实测漏填致「侍郎」全部无机构归属，「尚书→侍郎」边全丢）。
        for _p in (r.get("posts") or []):
            if not _p.get("org_id"):
                _p["org_id"] = r["owner_org_id"] or ""

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

    # ---------- v12：道制子节点展开（卷04 条37–41）----------
    # 原 ORG-2031「道」节点 仅有 instances[] 字符串占位（59 项）；
    # v12 用 `_dao_builder` 解析出 206 条（165 唯一名）带驻点的道记录，
    # 展开为正式 children[] 子节点，并同步补 LINE 边（注入 lines_ 后走统一 ID 分配）。
    dao_stations = []
    try:
        import _dao_builder as DB
        dao = DB.build(vols, errs)
        dao_parent = dao["dao_parent"]
        dao_nodes = dao["dao_nodes"]
        dao_stations = dao["dao_stations"]
        if dao_parent and dao_nodes:
            hit = None
            for r in org_recs:
                if r.get("org_id") == dao_parent or r.get("id") == dao_parent:
                    hit = r
                    break
            if hit is None:
                errs.append("道制：找不到汇总节点 %s" % dao_parent)
            else:
                hit["children"] = dao_nodes
                hit["instances"] = [x["name"] for x in dao_nodes]
                hit["note"] = ("布政司参政参议分守道 + 按察司副使佥事分巡道/兵备道等；"
                               "v12 展开 %d 个道节点（含驻点 %d）"
                               % (len(dao_nodes), len(dao_stations)))
                for e in dao["dao_lines"]:
                    e["_vol"] = "04"
                    lines_.append(e)
        # 驻点视图
        C.atomic_write_json(
            os.path.join(C.ROOT, "_views", "dao_stations.json"),
            {"count": len(dao_stations), "stations": dao_stations})
    except Exception as ex:
        errs.append("道制展开失败：%s" % ex)

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
    # v12：道制子节点（挂汇总节点「道」）的 LINE 边记 superior="天子" + cross_tree=True，
    #      故其树内边 (道名, 道) 不参与比对，改记入 cross_edges。
    line_edges = set()
    cross_edges = set()
    for r in line_recs:
        e = (r.get("subordinate"), r.get("superior"))
        if r.get("superior") == "天子" or r.get("cross_tree"):
            cross_edges.add(e)
        else:
            line_edges.add(e)
    # 道制子节点的树内边豁免（其 LINE 边已按跨树处理）
    dao_child_names = set()
    for r in org_recs:
        for c in (r.get("children") or []):
            if c.get("level") == "道" and c.get("parent") == "道":
                dao_child_names.add(c.get("name"))
    only_tree = {e for e in (tree_edges - line_edges) if e[0] not in dao_child_names}
    only_line = line_edges - tree_edges
    for e in sorted(only_tree):
        errs.append("树内边仅 ORG 有: %s->%s" % e)
    for e in sorted(only_line):
        errs.append("树内边仅 LINE 有: %s->%s" % e)

    # ---------- EVO ----------
    # v12 缺口3：EVO 沿革无法归属到具体机构。
    # 旧状：273 条 EVO 仅 101 条能按 item_id 关联到机构；六部共用的 01-016 一条里
    # 5 条 EVO 同时属于六部，EVO 记录**没有 owner 字段**，无法回答「吏部的沿革是什么」。
    # 修法：加 `owner_orgs[]`（**可多值**，共用的记为六部全体）+ `owner_org_ids[]`。
    #
    # 归属判定四级（宁缺毋滥，判不出即空数组）：
    #   ① 该 item_id 下只有一个 ORG 节点 → 极明确，直接归它；
    #   ② 该 item_id 下多个 ORG 节点 → 看**沿革文本是否显式点名**其中某机构
    #      （如「升六部秩」点名六部）；点名的进 owner_orgs，未点名的留空；
    #   ③ **集体机构名展开**（关键：本书特有问题）——「吏、户、礼、兵、刑、工六部」
    #      的沿革共处于**独立总述条 01-016**，而六部各自的 ORG 节点挂在各自的
    #      编制条（吏部=01-009、户部=01-019…）下，故 01-016 自身**没有 ORG 节点**。
    #      若沿革文本含集体名（六部/六科/五军都督府/都察院…的并列式），须展开为
    #      该集体的全部成员机构。展开表见 `EVO_COLLECTIVES`。
    #   ④ 全库同名索引按文本点名匹配（长名优先，避免「部」这类泛词命中）。
    #
    # 去重纪律：按 **name** 去重而非按 id —— 同名机构在全库有 74 组多 ID 实例
    #   （如「经历司」12 个、「司务厅」8 个、「四司」4 个），按 id 去重会得到
    #   `['四司','四司','四司','四司']` 这种同义重复（v12 首跑实测）。
    #   同名多 ID 时保留**作用域最贴近该 item_id** 者（同 item 优先，其次首个）。
    def _dedupe_by_name(picks, iid):
        by = {}
        for c in picks:
            n = c.get("name")
            if not n or not c.get("id"):
                continue
            prev = by.get(n)
            if prev is None:
                by[n] = c
            elif c.get("item_id") == iid and prev.get("item_id") != iid:
                by[n] = c          # 同条目者优先
        return list(by.values())

    evo_owner_n = evo_multi = 0
    evo_recs = []
    for r in evos:
        _iid = r.get("item_id") or ""
        cands = list(_by_item.get(_iid) or [])
        txt = r.get("content") or ""
        picks = []
        if len(cands) == 1:
            picks = [cands[0]]
        elif cands:
            named = [c for c in cands if c.get("name") and c["name"] in txt]
            named.sort(key=lambda c: -len(c["name"]))
            if named:
                picks = [named[0]]
        # ③ 集体机构名展开（六部共用沿革的关键修补）
        # ⚠ 纪律（v12 首跑踩坑）：**个体名优先于集体名**。
        #   「初，洪武元年置户部」虽属六部总述条 01-016，但只点名了户部 ——
        #   若先判集体，会把这条单独沿革错误地挂到六部全体（实测 8 条全被吞）。
        #   故顺序必须是：个体名点名 → 集体名展开。
        #   而集体侧须用**显式触发形态**（「吏、户、礼、兵、刑、工」「六部」
        #   「六卿」），因原文用并列单字，成员全名「吏部」一次也不出现。
        if not picks and not cands:
            indiv = [(n, c) for n, cs in _by_name.items()
                     for c in cs if n and len(n) >= 2 and n in txt]
            if indiv:
                indiv.sort(key=lambda t: -len(t[0]))
                top = indiv[0][0]
                if top in [cn for cn, _m, _f in E.EVO_COLLECTIVES]:
                    indiv = []
                else:
                    picks = [c for (n, c) in indiv if n == top]
            if not picks:
                for _cn, members, forms in E.EVO_COLLECTIVES:
                    if any(f in txt for f in forms):
                        picks = [c for n, cs in _by_name.items() if n in members
                                 for c in cs]
                        break
        if not picks:
            # ④ 全库同名兜底（仅文本显式点名时；长名优先）
            all_named = [(n, c) for n, cs in _by_name.items()
                         for c in cs if n and len(n) >= 2 and n in txt]
            if all_named:
                all_named.sort(key=lambda t: -len(t[0]))
                top = all_named[0][0]
                picks = [c for (n, c) in all_named if n == top]
        uniq = _dedupe_by_name(picks, _iid)
        r["owner_orgs"] = [{"id": c["id"], "name": c.get("name")} for c in uniq]
        r["owner_org_ids"] = [c["id"] for c in uniq]
        if uniq:
            evo_owner_n += 1
            if len(uniq) > 1:
                evo_multi += 1
    _stats_evo = {"evo_owner": evo_owner_n, "evo_multi": evo_multi}

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
           "EVO 记录: %d（有 owner %d，含多 owner %d）" % (
               len(evo_recs), _stats_evo["evo_owner"], _stats_evo["evo_multi"]),
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
