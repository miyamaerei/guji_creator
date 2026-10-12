"""transform.py —— F3 T0–T3 去歧义变换（可重跑、幂等）

对应《跨书合并-ELT设计》§5：
  T0 层 key 归一   —— 已在 layer_catalog 归一，这里只读（未登记层报 WARN，反制 #27）
  T1 名字→uid      —— 建 nodes；rel/appt 的名字经 BookNameIndex 解析成 edges，悬空进 pending_refs
  T2 候选生成      —— name_resolver.cross_candidates → candidate_links（带类型封顶置信度）
  T3 关系消歧      —— 并查集 + 关系一致性传播 + 类型约束 → canonical / members（带置信度）

设计要点（用户细化）：
- 名字归一/装饰词全部配置驱动（name_rules.json），代码不写死变体类型。
- 同名异人 / 泛称角色（person/official/…）置信度封顶，避免误并；work/place/era 等
  跨书同名基本同一，置信度高。查询端按置信度呈现。
- 「宁可漏不可错」：并查集只并「同 type 且置信度 ≥ floor」的候选；低于关系佐证的
  只进 candidate_links 不并入 canonical，留待人工（status='pending'）。
"""

import json
import sqlite3
from collections import defaultdict

from name_resolver import (
    BookNameIndex,
    cross_candidates,
    collect_surfaces,
    load_rules,
    normalize,
    capped_confidence,
)

# edge 层与「谁指向谁」的字段映射（新增 edge 层只在此登记）
EDGE_SPEC = {
    "rel": {"subject": "person_a", "object": "person_b", "predicate": "relation_type"},
    "appt": {"subject": "person", "object": "institution", "predicate": "office"},
}


def _name_text(v):
    """REL/APPT 字段可能是 str 或 {text:..., *_ent_ids:[...]}，取其文本名。"""
    if isinstance(v, str):
        return v.strip() or None
    if isinstance(v, dict):
        t = v.get("text")
        return t.strip() if isinstance(t, str) and t.strip() else None
    return None


# ---------------------------------------------------------------------------
# T0 / T1：nodes
# ---------------------------------------------------------------------------
def build_nodes(con, rules=None, commit=True):
    """每个 ent 记录 → 一个 node（uid=book:local_id，label=normalized，type）。"""
    if rules is None:
        rules = load_rules()
    cur = con.cursor()
    cur.execute("DELETE FROM nodes")
    rows = []
    for book_id in [r[0] for r in cur.execute("SELECT book_id FROM books ORDER BY book_id")]:
        for uid, norm, typ, surfs, aliases in collect_surfaces(con, book_id, rules):
            payload = {
                "normalized": norm,
                "type": typ,
                "surfaces": sorted(surfs),
                "aliases": sorted(aliases) if aliases else [],
            }
            rows.append((uid, book_id, "ent", uid.split(":", 1)[1], norm, typ,
                         json.dumps(payload, ensure_ascii=False)))
    cur.executemany(
        "INSERT OR REPLACE INTO nodes(uid,book_id,layer_key,local_id,label,type,payload)"
        " VALUES (?,?,?,?,?,?,?)",
        rows,
    )
    if commit:
        con.commit()
    return len(rows)


# ---------------------------------------------------------------------------
# T1：edges + pending_refs
# ---------------------------------------------------------------------------
def build_edges(con, rules=None, commit=True):
    """rel/appt 的名字 → uid，解析成功建 edges，失败（悬空）记 pending_refs。"""
    if rules is None:
        rules = load_rules()
    cur = con.cursor()
    cur.execute("DELETE FROM edges")
    cur.execute("DELETE FROM pending_refs")

    indexes = {}
    edge_rows = []
    pending = []
    for book_id in [r[0] for r in cur.execute("SELECT book_id FROM books ORDER BY book_id")]:
        indexes[book_id] = BookNameIndex(con, book_id, rules)

    for book_id, idx in indexes.items():
        for layer, spec in EDGE_SPEC.items():
            q = con.execute(
                "SELECT local_id, item_id, payload FROM records"
                " WHERE book_id=? AND layer_key=?",
                (book_id, layer),
            )
            for local_id, item_id, pl in q.fetchall():
                rec = json.loads(pl)
                subj_name = _name_text(rec.get(spec["subject"]))
                obj_name = _name_text(rec.get(spec["object"]))
                pred = rec.get(spec["predicate"]) or rec.get("type") or ""
                pred = pred if isinstance(pred, str) else ""

                subj_uid = obj_uid = None
                if subj_name:
                    hits = idx.resolve(subj_name)
                    if hits:
                        subj_uid = hits[0][0]
                    else:
                        pending.append((book_id, layer, local_id, spec["subject"],
                                        subj_name, "no_ent_match"))
                if obj_name:
                    hits = idx.resolve(obj_name)
                    if hits:
                        obj_uid = hits[0][0]
                    else:
                        pending.append((book_id, layer, local_id, spec["object"],
                                        obj_name, "no_ent_match"))

                if subj_uid or obj_uid:
                    edge_uid = f"{book_id}:{layer}:{local_id}"
                    edge_rows.append((edge_uid, book_id, layer, local_id, pred,
                                      subj_uid, obj_uid,
                                      subj_name if not subj_uid else None,
                                      obj_name if not obj_uid else None,
                                      json.dumps(rec, ensure_ascii=False)))

    cur.executemany(
        "INSERT OR REPLACE INTO edges(uid,book_id,layer_key,local_id,predicate,"
        "subject_uid,object_uid,subject_pending,object_pending,payload)"
        " VALUES (?,?,?,?,?,?,?,?,?,?)",
        edge_rows,
    )
    cur.executemany(
        "INSERT INTO pending_refs(book_id,layer_key,local_id,field,raw_name,reason,created_at)"
        " VALUES (?,?,?,?,?,?,datetime('now'))",
        pending,
    )
    if commit:
        con.commit()
    return len(edge_rows), len(pending)


# ---------------------------------------------------------------------------
# T2：candidate_links
# ---------------------------------------------------------------------------
def build_candidates(con, rules=None, commit=True):
    """跨书候选对 → candidate_links（置信度按类型封顶）。"""
    if rules is None:
        rules = load_rules()
    cur = con.cursor()
    cur.execute("DELETE FROM candidate_links")
    # 预取每个 uid 的 type（用于封顶）
    type_of = {r[0]: r[1] for r in cur.execute("SELECT uid, type FROM nodes")}
    rows = []
    seen = set()
    for a, b, method, conf in cross_candidates(con, rules):
        # 规范化顺序，避免 (a,b)/(b,a) 重复
        pair = (a, b) if a < b else (b, a)
        if pair in seen:
            continue
        seen.add(pair)
        ta = type_of.get(a)
        conf = capped_confidence(rules, ta, method, conf)
        rows.append((pair[0], pair[1], method, conf, 0))
    cur.executemany(
        "INSERT OR REPLACE INTO candidate_links(a_uid,b_uid,method,confidence,supporting_edges)"
        " VALUES (?,?,?,?,?)",
        rows,
    )
    if commit:
        con.commit()
    return len(rows)


# ---------------------------------------------------------------------------
# T3：并查集 + 关系传播 → canonical / members
# ---------------------------------------------------------------------------
class DSU:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra
        return ra


def disambiguate(con, rules=None, commit=True):
    """T3：关系消歧。返回统计 dict。

    流程：
      1. 先并「高置信」候选（conf ≥ secure_threshold，如 0.85）作为锚；
      2. 关系传播：对低置信候选，若其两端各有一条同 predicate 的关系边指向
         已对齐的一对节点，则提升置信（method→relation_propagated）；
      3. 提升后若 ≥ floor，再并入；
      4. 剩余低于 floor 的候选保留在 candidate_links（status pending，不并）。
    """
    if rules is None:
        rules = load_rules()
    conf_map = rules.get("match_confidence", {})
    floor = rules.get("confidence_floor", 0.35)
    secure = conf_map.get("exact_normalized", 0.98) * 0.85  # 约 0.83 作为锚阈值
    per = rules.get("relation_boost_per_edge", 0.08)
    cap_boost = rules.get("relation_boost_cap", 0.20)
    rel_conf = conf_map.get("relation_propagated", 0.55)

    cur = con.cursor()
    type_of = {r[0]: r[1] for r in cur.execute("SELECT uid, type FROM nodes")}

    # 读候选
    cands = cur.execute(
        "SELECT a_uid,b_uid,method,confidence FROM candidate_links"
    ).fetchall()

    # 关系邻接：uid → set[(other_uid, predicate)]
    adj = defaultdict(list)
    for subj, obj, pred in cur.execute(
        "SELECT subject_uid, object_uid, predicate FROM edges"
        " WHERE subject_uid IS NOT NULL AND object_uid IS NOT NULL"
    ):
        adj[subj].append((obj, pred))
        adj[obj].append((subj, pred))

    # 1) 高置信锚 union
    dsu = DSU()
    cand_conf = {}
    cand_method = {}
    for a, b, method, conf in cands:
        cand_conf[(a, b)] = conf
        cand_method[(a, b)] = method
        if conf >= secure:
            dsu.union(a, b)

    # 2) 关系传播提升
    def aligned(x, y):
        return dsu.find(x) == dsu.find(y)

    boosted = 0
    changed = True
    rounds = 0
    while changed and rounds < 3:
        changed = False
        rounds += 1
        for (a, b), conf in list(cand_conf.items()):
            if conf >= secure:
                continue
            # 找 a、b 各自的关系邻居，若存在 (na,nb) 已对齐且 predicate 同 → 佐证
            na_list = adj.get(a, [])
            nb_list = adj.get(b, [])
            if not na_list or not nb_list:
                continue
            nb_set = {}
            for nb, p in nb_list:
                nb_set.setdefault(nb, set()).add(p)
            support = 0
            for na, p in na_list:
                for nb, preds in nb_set.items():
                    if p in preds and aligned(na, nb):
                        support += 1
            if support > 0:
                new_conf = min(conf + per * min(support, cap_boost / per), rel_conf + cap_boost)
                new_conf = max(new_conf, rel_conf)
                if new_conf > conf + 1e-9:
                    cand_conf[(a, b)] = new_conf
                    cand_method[(a, b)] = "relation_propagated"
                    boosted += 1
                    changed = True

    # 3) 提升后并入（≥ floor 且同 type 由构造保证）
    for (a, b), conf in cand_conf.items():
        if conf >= floor:
            dsu.union(a, b)

    # 4) 物化 canonical / members
    cur.execute("DELETE FROM canonical")
    cur.execute("DELETE FROM members")
    groups = defaultdict(list)
    for uid in list(dsu.p.keys()):
        groups[dsu.find(uid)].append(uid)
    # 单节点组（无跨书对齐）不必建 canonical；但 present 的先建，便于查询
    canon_rows = []
    member_rows = []
    cid = 0
    for root, members_uids in sorted(groups.items(), key=lambda kv: kv[0]):
        if len(members_uids) < 2:
            continue  # 只建跨书 canonical
        cid += 1
        canonical_id = f"canon-{cid:05d}"
        types = {type_of.get(u) for u in members_uids}
        repr_type = next(iter(types)) if len(types) == 1 else "mixed"
        # repr = 置信最高者的 label
        best_uid, best_conf = None, -1
        for u in members_uids:
            c = 0.0
            for (a, b), mc in cand_conf.items():
                if a == u or b == u:
                    c = max(c, mc)
            if c > best_conf:
                best_uid, best_conf = u, c
        repr_label = _label_of(con, best_uid) if best_uid else None
        canon_rows.append((canonical_id, repr_type, repr_label, "open"))

        for u in members_uids:
            # 该成员的方法/置信/证据数
            best_m, best_c, ev = "exact", 0.0, 0
            for (a, b), mc in cand_conf.items():
                if a == u or b == u:
                    ev += 1
                    if mc > best_c:
                        best_c = mc
                        best_m = cand_method[(a, b)]
            status = "auto" if best_c >= secure else "conflict"
            member_rows.append((canonical_id, u, best_m, best_c, status, ev))

    cur.executemany(
        "INSERT INTO canonical(canonical_id,repr_type,repr_label,status,created_at)"
        " VALUES (?,?,?,?,datetime('now'))",
        canon_rows,
    )
    cur.executemany(
        "INSERT OR REPLACE INTO members(canonical_id,uid,method,confidence,status,evidence_count)"
        " VALUES (?,?,?,?,?,?)",
        member_rows,
    )
    if commit:
        con.commit()
    return {
        "candidates": len(cands),
        "canonicals": cid,
        "members": len(member_rows),
        "relation_boosted": boosted,
        "rounds": rounds,
        "floor": floor,
        "secure": round(secure, 3),
    }


def _label_of(con, uid):
    r = con.execute("SELECT label FROM nodes WHERE uid=?", (uid,)).fetchone()
    return r[0] if r else None


# ---------------------------------------------------------------------------
# 编排
# ---------------------------------------------------------------------------
def run_transform(con, rules=None, commit=True):
    """T0–T3 全跑 + 物化引用 + 重放人工裁决。

    顺序理由：refs 依赖 nodes（要先有 uid），裁决重放必须在 T3 之后
    （T3 会重建 canonical/members，把人工裁决冲掉）。
    """
    from refs import materialize_refs  # 局部导入避免环
    from curate import replay_overrides

    rules = rules or load_rules()
    out = {}
    out["nodes"] = build_nodes(con, rules)
    out["edges"], out["pending"] = build_edges(con, rules)
    out["refs"] = materialize_refs(con)
    out["candidates"] = build_candidates(con, rules)
    out["t3"] = disambiguate(con, rules, commit=commit)
    # 人工裁决重放：让「一切可重跑」与人工介入共存
    out["overrides"] = replay_overrides(con)
    return out