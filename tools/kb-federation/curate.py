"""curate.py —— F4-2：conflict 成员的人工锁定与解除误并

**为什么裁决要单独存表**

T3 是「一切可重跑」的：重跑 `transform` 会 `DELETE FROM canonical/members`
再重建。若把人工裁决直接写进 `members.status`，一重跑就被抹掉——
这正是项目铁律「一切可重跑」与人工介入的冲突点。

解法（**裁决与派生分离**）：
    member_overrides  = 人工裁决（输入，只增不删，后写覆盖）
    canonical/members = 派生（transform 可随时重建）
每次 transform 之后调 `replay_overrides()` 重放裁决，保证重跑幂等且不丢人工成果。

**两个动作**
  lock   确认「确是同一人」→ 成员 status 置 'locked'，并**强制留在 canonical 内**
         （即便 T3 这次没并进来，如 low-conf 成员，人工说同就同）
  reject 确认「不是同一人」→ 成员**移出** canonical 成为独立节点，
         status 置 'rejected'，canonical.status 置 'split'（簇被拆过）

原则：**人工永远优先于算法**。T3 置信度只是建议，最终以 member_overrides 为准。
"""

import json
from datetime import datetime


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _audit(con, uid, action, canonical_id, reason, decided_by):
    con.execute(
        "INSERT INTO override_log(uid,action,canonical_id,reason,decided_by,decided_at)"
        " VALUES (?,?,?,?,?,?)",
        (uid, action, canonical_id, reason, decided_by, _now()),
    )


def decide(con, uid, action, *, canonical_id=None, reason=None, decided_by="human"):
    """记录一条人工裁决。action ∈ {'lock','reject'}。

    幂等：同一 uid 再裁决即覆盖（member_overrides 主键 = uid）。
    """
    if action not in ("lock", "reject"):
        raise ValueError("action 必须是 'lock' 或 'reject'")
    if not con.execute("SELECT 1 FROM nodes WHERE uid=?", (uid,)).fetchone():
        raise ValueError(f"未知 uid：{uid}")

    con.execute(
        "INSERT OR REPLACE INTO member_overrides"
        " (uid,action,canonical_id,reason,decided_by,decided_at,created_at)"
        " VALUES (?,?,?,?,?,?,?)",
        (uid, action, canonical_id, reason, decided_by, _now(), _now()),
    )
    _audit(con, uid, action, canonical_id, reason, decided_by)
    con.commit()
    return {"uid": uid, "action": action, "canonical_id": canonical_id}


def undecide(con, uid):
    """撤销一条裁决（回到 T3 自动判定）。无可撤销记录时报错，不静默成功。"""
    if not con.execute("SELECT 1 FROM member_overrides WHERE uid=?", (uid,)).fetchone():
        raise ValueError(f"该 uid 没有裁决记录可撤销：{uid}")
    con.execute("DELETE FROM member_overrides WHERE uid=?", (uid,))
    _audit(con, uid, "revoke", None, None, "human")
    con.commit()
    return {"uid": uid, "action": "revoke"}


def replay_overrides(con):
    """在 T3 之后重放人工裁决。返回统计。

    幂等：可在每次 transform 后重复调用。
    """
    ov = con.execute(
        "SELECT uid, action, canonical_id FROM member_overrides"
    ).fetchall()
    if not ov:
        return {"overrides": 0, "locked": 0, "rejected": 0, "split_canonicals": 0}

    label_of = {r[0]: r[1] for r in con.execute("SELECT uid, label FROM nodes")}
    canon_of = {r[0]: r[1] for r in con.execute(
        "SELECT uid, canonical_id FROM members")}
    repr_of = {r[0]: (r[1], r[2]) for r in con.execute(
        "SELECT canonical_id, repr_type, repr_label FROM canonical")}

    locked = rejected = 0
    touched = set()
    new_members = []
    for uid, action, cid in ov:
        cur_cid = canon_of.get(uid)
        touched.add(cur_cid or cid)
        if action == "lock":
            # 目标 canonical：优先人工指定，否则沿用 T3 结果
            target = cid or cur_cid
            if not target:
                # 人工锁定的「单节点」需新建 canonical
                target = _ensure_singleton_canonical(con, uid, label_of, repr_of)
            ev = con.execute(
                "SELECT COALESCE(MAX(evidence_count),0) FROM members"
                " WHERE canonical_id=? AND uid=?",
                (target, uid),
            ).fetchone()[0] + 1
            con.execute(
                "INSERT OR REPLACE INTO members"
                "(canonical_id,uid,method,confidence,status,evidence_count)"
                " VALUES (?,?,'manual_lock',1.0,'locked',?)",
                (target, uid, ev),
            )
            con.execute(
                "UPDATE canonical SET status='locked' WHERE canonical_id=?",
                (target,),
            )
            locked += 1
        else:  # reject
            if cur_cid:
                con.execute("DELETE FROM members WHERE uid=?", (uid,))
            # 簇里已无其他成员 → canonical 本身失去意义
            left = con.execute(
                "SELECT COUNT(*) FROM members WHERE canonical_id=?", (cur_cid,)
            ).fetchone()[0]
            if cur_cid and left < 2:
                con.execute("DELETE FROM canonical WHERE canonical_id=?", (cur_cid,))
            elif cur_cid:
                con.execute(
                    "UPDATE canonical SET status='split', note=? WHERE canonical_id=?",
                    (f"人工解除误并（{uid} {label_of.get(uid) or ''}）", cur_cid),
                )
            rejected += 1

    con.commit()
    return {
        "overrides": len(ov),
        "locked": locked,
        "rejected": rejected,
        "split_canonicals": con.execute(
            "SELECT COUNT(*) FROM canonical WHERE status='split'").fetchone()[0],
    }


def _ensure_singleton_canonical(con, uid, label_of, repr_of):
    """为「人工锁定但 T3 未并入」的单节点建 canonical（复用 repr_of 保证 id 不冲突）。"""
    maxn = con.execute(
        "SELECT COALESCE(MAX(CAST(SUBSTR(canonical_id,7) AS INTEGER)),0) FROM canonical"
    ).fetchone()[0]
    new_cid = f"canon-{maxn + 1:05d}"
    row = con.execute("SELECT type, label FROM nodes WHERE uid=?", (uid,)).fetchone()
    con.execute(
        "INSERT INTO canonical(canonical_id,repr_type,repr_label,status,created_at,note)"
        " VALUES (?,?,?,'locked',?,?)",
        (new_cid, row[0] if row else None,
         row[1] if row else label_of.get(uid), _now(), "人工锁定单独成簇"),
    )
    return new_cid


def list_conflicts(con, limit=100, offset=0, book_id=None, type=None):
    """列出待人工复核的 conflict 成员（含理由线索：同簇各书的 label / 方法 / 置信）。"""
    sql = [
        "SELECT m.canonical_id, m.uid, n.label, n.book_id, n.type,",
        "       m.method, m.confidence, c.repr_label, c.repr_type",
        "FROM members m",
        "JOIN nodes n ON n.uid = m.uid",
        "LEFT JOIN canonical c ON c.canonical_id = m.canonical_id",
        "WHERE m.status='conflict'",
    ]
    args = []
    if book_id:
        sql.append("AND n.book_id=?")
        args.append(book_id)
    if type:
        sql.append("AND n.type=?")
        args.append(type)
    sql.append("ORDER BY m.confidence ASC, m.canonical_id LIMIT ? OFFSET ?")
    args += [limit, offset]
    rows = con.execute(" ".join(sql), args).fetchall()
    out = []
    for cid, uid, label, bid, typ, method, conf, rlabel, rtype in rows:
        # 同簇其他成员（同 type 且异书 = 最可能的误并）
        siblings = con.execute(
            "SELECT n.uid, n.book_id, n.label, m.confidence, m.status"
            "  FROM members m JOIN nodes n ON n.uid = m.uid"
            " WHERE m.canonical_id = ?",
            (cid,),
        ).fetchall()
        out.append({
            "canonical_id": cid,
            "uid": uid,
            "label": label,
            "book": bid,
            "type": typ,
            "method": method,
            "confidence": round(conf or 0.0, 3),
            "canonical_repr": rlabel,
            "canonical_type": rtype,
            "siblings": [
                {"uid": u, "book": b, "label": l,
                 "confidence": round(c or 0.0, 3), "status": s}
                for u, b, l, c, s in siblings if u != uid
            ],
            "suggestion": (
                "同 type 异书同名，若两书各写一人则为同名异人 → reject"
                if len({b for _u, b, _l, _c, _s in siblings}) == len(siblings)
                else "跨书多成员指向同一对象 → 多半同一人，可 lock"
            ),
        })
    return out


def list_overrides(con):
    """列出全部人工裁决（含已撤销的审计痕迹）。"""
    ovs = con.execute(
        "SELECT uid, action, canonical_id, reason, decided_by, decided_at"
        "  FROM member_overrides ORDER BY decided_at DESC"
    ).fetchall()
    labels = {r[0]: r[1] for r in con.execute("SELECT uid,label FROM nodes")}
    return [{
        "uid": u, "label": labels.get(u), "action": a, "canonical_id": c,
        "reason": r, "by": d, "at": t,
    } for u, a, c, r, d, t in ovs]


def review_stats(con):
    """裁决工作台概览。"""
    q = lambda s: con.execute(s).fetchone()[0]
    return {
        "members": q("SELECT COUNT(*) FROM members"),
        "auto": q("SELECT COUNT(*) FROM members WHERE status='auto'"),
        "conflict": q("SELECT COUNT(*) FROM members WHERE status='conflict'"),
        "locked": q("SELECT COUNT(*) FROM members WHERE status='locked'"),
        "rejected": q("SELECT COUNT(*) FROM override_log WHERE action='reject'"),
        "canonicals": q("SELECT COUNT(*) FROM canonical"),
        "split_canonicals": q("SELECT COUNT(*) FROM canonical WHERE status='split'"),
        "overrides": q("SELECT COUNT(*) FROM member_overrides"),
    }