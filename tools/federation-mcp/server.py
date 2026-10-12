"""server.py —— 联邦库 MCP 服务（第三条线：跨书查询 + 人工裁决）

与另两条 MCP 线同构（手写 JSON-RPC 2.0 over stdio，协议 2024-11-05，零第三方依赖）：
  tools/kb-mcp/    存量线 —— 只读体检已交付的 6 本（枚举漂移/同步）
  tools/book-mcp/  契约线 —— 只读查询格式契约（第 7 本起开工前用）
  tools/federation-mcp/ 本文件 —— 联邦线 —— 跨书关联查询 + conflict 人工裁决

定位：**查询与裁决入口**，不负责装载/变换（那是 `kb-federation/federation.py` 的职责）。
写操作仅限 member_overrides（人工裁决），且**不碰任何源书数据**——总库只读六书。

工具 13 个：
  跨书检索3：fed_search / fed_books / fed_entity
  关联查询10：fed_assoc_list + fed_assoc（统一入口，assoc 名 + 参数）
  人工裁决3：fed_conflicts / fed_lock / fed_unlock

用法：
  python server.py selftest                     # 自检（不启动服务）
  python server.py books
  python server.py search 王忠毅公
  python server.py assoc identity_bridge --arg name=苏轼
  python server.py conflicts --limit 5
  python server.py lock kzz:01:ENT-0136 --reason '确为同一人'
挂 MCP：stdio，命令 python，参数 server.py --db kb.sqlite
"""

import argparse
import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FED_DIR = os.path.normpath(os.path.join(HERE, "..", "kb-federation"))
if FED_DIR not in sys.path:
    sys.path.insert(0, FED_DIR)

from assoc import AssocQuery                      # noqa: E402
from curate import (                             # noqa: E402
    decide, list_conflicts, list_overrides, review_stats, undecide,
)
from query import FederationQuery                 # noqa: E402

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "guji-federation"
SERVER_VERSION = "1.0"
DEFAULT_DB = os.path.join(FED_DIR, "kb.sqlite")


def _connect(db):
    if not os.path.exists(db):
        raise FileNotFoundError(
            "找不到联邦库 %s；先跑 `python federation.py create && "
            "python federation.py load-all && python federation.py transform`" % db)
    con = sqlite3.connect(db)
    con.row_factory = None
    return con


# ----------------------------------------------------------------- 工具实现

def t_books(args):
    """各书的装载状态与层/记录数。"""
    con = _connect(args.get("db") or DEFAULT_DB)
    out = {"books": [], "totals": {}}
    for b in con.execute("SELECT book_id, name, status FROM books ORDER BY book_id"):
        layers = con.execute(
            "SELECT layer_key, kind, record_count FROM layer_catalog"
            " WHERE book_id=? ORDER BY layer_key", (b[0],)).fetchall()
        out["books"].append({
            "book_id": b[0], "name": b[1], "status": b[2],
            "layers": len(layers),
            "records": sum((x[2] or 0) for x in layers),
            "layer_detail": [{"layer": l, "kind": k, "records": n} for l, k, n in layers],
        })
    q = lambda s: con.execute(s).fetchone()[0]
    out["totals"] = {
        "items": q("SELECT COUNT(*) FROM items"),
        "records": q("SELECT COUNT(*) FROM records"),
        "nodes": q("SELECT COUNT(*) FROM nodes"),
        "edges": q("SELECT COUNT(*) FROM edges"),
        "record_refs": q("SELECT COUNT(*) FROM record_refs"),
        "canonicals": q("SELECT COUNT(*) FROM canonical"),
        "members": q("SELECT COUNT(*) FROM members"),
        "pending_names": q("SELECT COUNT(*) FROM pending_refs"),
    }
    con.close()
    return out


def t_search(args):
    """跨书检索任意名字（含尊称/谥号/书名号等变体），返回所有成员+置信度。"""
    name = args.get("name") or args.get("query")
    if not name:
        return {"error": "缺少必填参数: name"}
    con = _connect(args.get("db") or DEFAULT_DB)
    fq = FederationQuery(con)
    groups = fq.cross_search(name, type=args.get("type"),
                             limit=int(args.get("limit", 20)))
    out = {"query": name, "groups": groups,
           "per_book": fq.resolve_across_books(name)}
    con.close()
    return out


def t_entity(args):
    """单个实体的详情：标签/类型/各书变体/被引用情况。"""
    uid = args.get("uid")
    if not uid:
        return {"error": "缺少必填参数: uid"}
    con = _connect(args.get("db") or DEFAULT_DB)
    row = con.execute(
        "SELECT uid, book_id, layer_key, local_id, label, type, payload"
        "  FROM nodes WHERE uid=?", (uid,)).fetchone()
    if not row:
        return {"error": "未知 uid: %s" % uid}
    try:
        payload = json.loads(row[6]) if row[6] else {}
    except (ValueError, TypeError):
        payload = {}
    refs = con.execute(
        "SELECT book_id, layer_key, field, role, count(*) FROM record_refs"
        " WHERE target_uid=? GROUP BY book_id, layer_key, field, role",
        (uid,)).fetchall()
    m = con.execute(
        "SELECT canonical_id, method, confidence, status FROM members WHERE uid=?",
        (uid,)).fetchone()
    out = {
        "uid": row[0], "book": row[1], "layer": row[2], "local_id": row[3],
        "label": row[4], "type": row[5],
        "surfaces": payload.get("surfaces", []),
        "aliases": payload.get("aliases", []),
        "canonical": ({"id": m[0], "method": m[1], "confidence": m[2], "status": m[3]}
                      if m else None),
        "referenced_by": [{"book": b, "layer": l, "field": f, "role": ro, "count": c}
                          for b, l, f, ro, c in refs],
    }
    con.close()
    return out


def t_assoc_list(args):
    """列出十个关联查询及其用法。"""
    con = _connect(args.get("db") or DEFAULT_DB)
    aq = AssocQuery(con)
    out = {"queries": aq.catalog(), "count": len(aq.catalog())}
    con.close()
    return out


# assoc 名 → 方法
ASSOC_METHODS = {
    "identity_bridge": "identity_bridge",
    "person_network": "person_network",
    "career_chain": "career_chain",
    "citation_network": "citation_network",
    "work_author": "work_author",
    "place_culture": "place_culture",
    "object_lineage": "object_lineage",
    "event_opinion": "event_opinion",
    "parallel_reading": "parallel_reading",
    "dangling_refs": "dangling_refs",
}


def t_assoc(args):
    """统一关联查询入口：assoc=<名> + 相应参数。"""
    which = args.get("assoc") or args.get("query")
    if not which:
        return {"error": "缺少必填参数: assoc（可用 fed_assoc_list 查看）"}
    if which not in ASSOC_METHODS:
        return {"error": "未知查询 %r；可用: %s" % (which, ", ".join(ASSOC_METHODS))}
    con = _connect(args.get("db") or DEFAULT_DB)
    aq = AssocQuery(con)
    kw = {}
    for k in ("name", "work", "author", "place", "keyword", "book_id"):
        if args.get(k):
            kw[k] = args[k]
    if args.get("predicates"):
        kw["predicates"] = args["predicates"] if isinstance(args["predicates"], list) \
            else [p.strip() for p in str(args["predicates"]).split(",")]
    kw["limit"] = int(args.get("limit", 20))
    try:
        out = getattr(aq, ASSOC_METHODS[which])(**kw)
    except TypeError as e:
        return {"error": "参数不匹配: %s" % e}
    con.close()
    return out


def t_conflicts(args):
    """列出待人工复核的 conflict 成员（同簇异书同名的可疑误并）。"""
    con = _connect(args.get("db") or DEFAULT_DB)
    out = {
        "stats": review_stats(con),
        "conflicts": list_conflicts(
            con, limit=int(args.get("limit", 20)), offset=int(args.get("offset", 0)),
            book_id=args.get("book_id"), type=args.get("type"),
        ),
        "overrides": list_overrides(con),
    }
    con.close()
    return out


def t_lock(args):
    """人工锁定：确认两个 uid 是同一人（写 member_overrides，可撤销）。"""
    uid = args.get("uid")
    action = args.get("action", "lock")
    if not uid:
        return {"error": "缺少必填参数: uid"}
    con = _connect(args.get("db") or DEFAULT_DB)
    try:
        out = decide(con, uid, action,
                     canonical_id=args.get("canonical_id"),
                     reason=args.get("reason"),
                     decided_by=args.get("decided_by", "mcp"))
        out["stats"] = review_stats(con)
        out["hint"] = "裁决已记录；重跑 transform 后由 replay_overrides 自动重放"
    except ValueError as e:
        return {"error": str(e)}
    con.close()
    return out


def t_unlock(args):
    """撤销人工裁决（回到 T3 自动判定）。"""
    uid = args.get("uid")
    if not uid:
        return {"error": "缺少必填参数: uid"}
    con = _connect(args.get("db") or DEFAULT_DB)
    try:
        out = undecide(con, uid)
        out["stats"] = review_stats(con)
    except ValueError as e:
        return {"error": str(e)}
    con.close()
    return out


# ----------------------------------------------------------------- MCP 协议

def _s(desc, props=None, required=None):
    return {
        "name": desc[0],
        "description": desc[1],
        "inputSchema": {
            "type": "object",
            "properties": props or {},
            "required": required or [],
        },
    }


_DB = {"db": {"type": "string", "description": "联邦库路径（默认 kb.sqlite）"}}

TOOLS = [
    _s(("fed_books", "各书装载状态 + 全库统计（items/records/nodes/edges/refs/canonicals）"),
       dict(_DB)),
    _s(("fed_search", "跨书检索任意名字（支持尊称/谥号/书名号等变体），"
                      "返回所有成员 + 匹配方法 + 置信度"),
       dict(_DB, name={"type": "string", "description": "人名/地名/书名等"},
            type={"type": "string", "description": "限定实体类型 person/place/work…"},
            limit={"type": "integer", "description": "返回条数，默认 20"}),
       ["name"]),
    _s(("fed_entity", "单个实体详情：各书变体、所属canonical、被哪些层的哪些字段引用"),
       dict(_DB, uid={"type": "string", "description": "如 kzz:01:ENT-0136"}), ["uid"]),
    _s(("fed_assoc_list", "列出十个跨书关联查询及其参数"), dict(_DB)),
    _s(("fed_assoc", "执行关联查询：identity_bridge/person_network/career_chain/"
                     "citation_network/work_author/place_culture/object_lineage/"
                     "event_opinion/parallel_reading/dangling_refs"),
       dict(_DB, assoc={"type": "string", "description": "查询名"},
            name={"type": "string"}, work={"type": "string"},
            author={"type": "string"}, place={"type": "string"},
            keyword={"type": "string"}, book_id={"type": "string"},
            predicates={"type": "string", "description": "关系类型过滤，逗号分隔"},
            limit={"type": "integer"}),
       ["assoc"]),
    _s(("fed_conflicts", "待人工复核的 conflict 成员（含同簇异书兄弟成员与处理建议）"),
       dict(_DB, limit={"type": "integer"}, book_id={"type": "string"},
            type={"type": "string"})),
    _s(("fed_lock", "人工裁决：action=lock 确认同人（锁定）/action=reject 解除误并（拆出）。"
                    "写member_overrides，可撤销，且重跑 transform 不丢"),
       dict(_DB, uid={"type": "string"},
            action={"type": "string", "enum": ["lock", "reject"]},
            canonical_id={"type": "string"},
            reason={"type": "string", "description": "裁决理由（供后续审计）"}),
       ["uid"]),
    _s(("fed_unlock", "撤销人工裁决，回到 T3 自动判定"),
       dict(_DB, uid={"type": "string"}), ["uid"]),
]

HANDLERS = {
    "fed_books": t_books,
    "fed_search": t_search,
    "fed_entity": t_entity,
    "fed_assoc_list": t_assoc_list,
    "fed_assoc": t_assoc,
    "fed_conflicts": t_conflicts,
    "fed_lock": t_lock,
    "fed_unlock": t_unlock,
}


def call_tool(name, arguments):
    fn = HANDLERS.get(name)
    if not fn:
        return {"error": "未知工具: %s" % name}
    try:
        return fn(arguments or {})
    except FileNotFoundError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "%s: %s" % (type(e).__name__, e)}


def _result(rid, result):
    return {"jsonrpc": "2.0", "id": rid, "result": result}


def _error(rid, code, message):
    return {"jsonrpc": "2.0", "id": rid,
            "error": {"code": code, "message": message}}


def handle(msg):
    rid = msg.get("id")
    method = msg.get("method")
    params = msg.get("params") or {}
    if method == "initialize":
        return _result(rid, {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
        })
    if method == "ping":
        return _result(rid, {})
    if method == "tools/list":
        return _result(rid, {"tools": TOOLS})
    if method == "tools/call":
        out = call_tool(params.get("name"), params.get("arguments") or {})
        is_err = isinstance(out, dict) and "error" in out and len(out) <= 2
        return _result(rid, {"content": [{"type": "text",
                                          "text": json.dumps(out, ensure_ascii=False, indent=2)}],
                             "isError": bool(is_err)})
    if method and method.startswith("notifications/"):
        return None
    return _error(rid, -32601, "Method not found: %s" % method)


def serve():
    log("server started（联邦线：跨书查询 + 人工裁决）")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception as e:
            log("bad json: %s" % e)
            continue
        resp = handle(msg)
        if resp is None:
            continue
        sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
        sys.stdout.flush()


def log(s):
    sys.stderr.write("[%s] %s\n" % (SERVER_NAME, s))
    sys.stderr.flush()


# ------------------------------------------------------------------- CLI 模式

def selftest(db):
    """自检：库在不在、每个工具能不能跑、十个查询是否都通。"""
    print("selftest：联邦库 = %s" % db)
    if not os.path.exists(db):
        print("✗ 库不存在，先跑 federation.py create / load-all / transform")
        return 1
    ok = fail = 0
    checks = [
        ("fed_books", {}, "fed_books"),
        ("fed_assoc_list", {}, "fed_assoc_list"),
        ("fed_search(精确名)", {"name": "宋濂", "limit": 3}, "fed_search"),
        ("fed_search(谥号变体)", {"name": "王忠毅公", "limit": 3}, "fed_search"),
        ("fed_search(书名号变体)", {"name": "礼记", "limit": 3}, "fed_search"),
    ]
    for label, a, tool in checks:
        out = call_tool(tool, a)
        bad = isinstance(out, dict) and "error" in out
        print("  %s %s%s" % ("✗" if bad else "✓", label,
                              ("  " + str(out["error"])) if bad else ""))
        fail += bad
        ok += (not bad)
    # fed_entity 取一个真实 uid
    con = _connect(db)
    r = con.execute("SELECT uid FROM nodes LIMIT 1").fetchone()
    con.close()
    if r:
        out = call_tool("fed_entity", {"uid": r[0]})
        bad = isinstance(out, dict) and "error" in out
        print("  %s fed_entity(%s)%s" % ("✗" if bad else "✓", r[0],
                                         ("  " + str(out["error"])) if bad else ""))
        fail += bad
        ok += (not bad)
    else:
        print("  ✗ fed_entity（nodes 为空）")
        fail += 1
    # 十个关联查询各跑一次（每个用各自的参数名）
    sample = {
        "identity_bridge": {"name": "苏轼"},
        "person_network": {"name": "苏轼"},
        "career_chain": {"name": "杨溥"},
        "citation_network": {"work": "礼记"},
        "work_author": {"author": "陈沂"},
        "place_culture": {"place": "南京"},
        "object_lineage": {"name": "鲥鱼"},
        "event_opinion": {"keyword": "科举"},
        "parallel_reading": {"keyword": "科举"},
        "dangling_refs": {},
    }
    for q in ASSOC_METHODS:
        out = call_tool("fed_assoc", dict(sample[q], assoc=q, limit=3))
        bad = isinstance(out, dict) and "error" in out
        print("  %s fed_assoc/%s%s" % ("✗" if bad else "✓", q,
                                        ("  " + str(out["error"])) if bad else ""))
        fail += bad
        ok += (not bad)
    for label, tool, a, expect_err in [
        ("fed_conflicts", "fed_conflicts", {"limit": 3}, False),
        ("fed_unlock(未知uid 应报错)", "fed_unlock", {"uid": "nonexistent"}, True),
    ]:
        out = call_tool(tool, a)
        bad = isinstance(out, dict) and "error" in out
        bad = (not bad) if expect_err else bad
        print("  %s %s%s" % ("✗" if bad else "✓", label,
                              ("  " + str(out.get("error")) if isinstance(out, dict) and "error" in out else "")))
        fail += bad
        ok += (not bad)
    print("\n通过 %d / 失败 %d" % (ok, fail))
    return 0 if fail == 0 else 1


def main(argv=None):
    p = argparse.ArgumentParser(prog="federation-mcp",
                                description="古籍联邦库 MCP 服务")
    p.add_argument("--db", default=DEFAULT_DB)
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("selftest", help="自检")
    sub.add_parser("serve", help="启动 MCP 服务（stdio）")
    ps = sub.add_parser("search", help="跨书检索名字")
    ps.add_argument("name")
    ps.add_argument("--type")
    ps.add_argument("--limit", type=int, default=10)
    pb = sub.add_parser("books", help="各书状态 + 全库统计")
    pa = sub.add_parser("assoc", help="执行关联查询")
    pa.add_argument("query")
    pa.add_argument("--arg", action="append", default=[], help="name=值，可多次")
    pa.add_argument("--limit", type=int, default=20)
    pc = sub.add_parser("conflicts", help="待复核 conflict 成员")
    pc.add_argument("--limit", type=int, default=10)
    pl = sub.add_parser("lock", help="人工锁定（action=lock|reject）")
    pl.add_argument("uid")
    pl.add_argument("--action", default="lock")
    pl.add_argument("--reason")
    pu = sub.add_parser("unlock", help="撤销裁决")
    pu.add_argument("uid")

    args = p.parse_args(argv)
    db = args.db
    if args.cmd in (None, "serve"):
        serve()
        return 0
    if args.cmd == "selftest":
        return selftest(db)

    if args.cmd == "books":
        print(json.dumps(call_tool("fed_books", {"db": db}), ensure_ascii=False, indent=2))
    elif args.cmd == "search":
        print(json.dumps(call_tool("fed_search",
                                   {"db": db, "name": args.name, "type": args.type,
                                    "limit": args.limit}), ensure_ascii=False, indent=2))
    elif args.cmd == "assoc":
        kw = {}
        for kv in args.arg:
            if "=" in kv:
                k, v = kv.split("=", 1)
                kw[k.strip()] = v
        kw["limit"] = args.limit
        print(json.dumps(call_tool("fed_assoc", dict(kw, assoc=args.query, db=db)),
                         ensure_ascii=False, indent=2))
    elif args.cmd == "conflicts":
        print(json.dumps(call_tool("fed_conflicts", {"db": db, "limit": args.limit}),
                         ensure_ascii=False, indent=2))
    elif args.cmd == "lock":
        print(json.dumps(call_tool("fed_lock",
                                   {"db": db, "uid": args.uid, "action": args.action,
                                    "reason": args.reason}), ensure_ascii=False, indent=2))
    elif args.cmd == "unlock":
        print(json.dumps(call_tool("fed_unlock", {"db": db, "uid": args.uid}),
                         ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())