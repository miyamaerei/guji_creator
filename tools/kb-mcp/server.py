# -*- coding: utf-8 -*-
"""古籍知识工程 MCP server（P0：只读）。

两用入口：
    python server.py                    # MCP 模式：JSON-RPC 2.0 over stdio
    python server.py drift --book X     # CLI 自检模式：不挂客户端也能验证

**零第三方依赖**：只用标准库手写 MCP 协议（initialize / tools/list / tools/call）。
这是刻意的——六本书的管线是「纯标准库零依赖」（见根 README §6），
MCP server 作为外围工具若引入 mcp/fastmcp，虽然装在独立 venv 不污染管线，
但会让仓库多出一份需要 pip install 的东西。P0 只读场景用不上那些高级能力。
若后续 P2 需要通知/资源订阅等，再评估引入官方 SDK。

协议版本 2024-11-05。日志一律走 stderr（stdout 只能有 JSON-RPC 消息）。
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kb_mcp import tools as T  # noqa: E402
from kb_mcp import registry as R  # noqa: E402

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "guji-kb-enum"
SERVER_VERSION = "0.1.0-p0"

# ------------------------------------------------------------------ 工具声明

TOOLS = [
    {
        "name": "kb_books",
        "description": "列出受管辖的书：枚举后端形态、枚举组数、schemas 快照是否登记。"
                       "不确定有哪些书、某本书能不能被 MCP 读到时先调这个。",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "enum_list",
        "description": "列枚举规范值。scope=factory 看工厂基准库（默认，跨全部书）；"
                       "scope=instance 看某本书自己的 _kg_enums.py；scope=all 两边都看。"
                       "带 enum 参数可只看一组（如 ENTITY / EVENT / GEO）。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "scope": {"type": "string", "enum": ["factory", "instance", "all"],
                          "default": "factory", "description": "作用域"},
                "book": {"type": "string", "description": "scope=instance 时必填，"
                                                          "如 wuzazu-kb / kezuozhuiyu-kb"},
                "enum": {"type": "string", "description": "枚举名（ENTITY/EVT/GEO…），"
                                                          "不填列全部"},
                "limit": {"type": "integer", "default": 200, "description": "每组最多列几个值"},
            },
            "required": [],
        },
    },
    {
        "name": "enum_get",
        "description": "查单个值：是否被定义（工厂/实例）、是不是别名、"
                       "在层产物里实际被用了多少次。用来判断一个值该不该新增。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "enum": {"type": "string", "description": "枚举名，如 ENTITY / EVENT"},
                "value": {"type": "string", "description": "要查的值，如 星象 / 靖难"},
                "scope": {"type": "string", "enum": ["factory", "instance", "all"],
                          "default": "all"},
                "book": {"type": "string", "description": "限定某本书（可选）"},
            },
            "required": ["enum", "value"],
        },
    },
    {
        "name": "enum_drift",
        "description": "漂移报告：扫某本书的层产物，统计每层实际取值种数，"
                       "与枚举定义数比对。比值>threshold 判漂移，并给出库外值占比。"
                       "这是最该定期跑的工具——客座赘语 EVT 跑到 111 种（定义 23）"
                       "就是这类事故。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "book": {"type": "string", "description": "书目录名，如 kezuozhuiyu-kb"},
                "layer": {"type": "string", "description": "限定某一层（可选），如 ent / evt"},
                "threshold": {"type": "number", "default": 1.5,
                              "description": "漂移阈值（实际种数/定义数）"},
            },
            "required": ["book"],
        },
    },
    {
        "name": "enum_sync",
        "description": "三处一致性：工厂库 enum-library.md / 实例 _kg_enums.py / "
                       "实例 schemas.md 快照。factory_only=实例落后；"
                       "instance_only=实例有未回库的本地扩展（#27 的温床）。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "book": {"type": "string", "description": "书目录名"},
                "enum": {"type": "string", "description": "限定某一组枚举（可选）"},
            },
            "required": ["book"],
        },
    },
    {
        "name": "enum_checklist",
        "description": "健康度体检：缺兜底值、树深度>3、声明值与解析值不符、"
                       "层无对应枚举定义（无护栏区）、实体表 pending 未决数。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "book": {"type": "string", "description": "限定某本书（可选），不填查全部"},
            },
            "required": [],
        },
    },
]

DISPATCH = {
    "kb_books": lambda a: T.kb_books(),
    "enum_list": lambda a: T.enum_list(
        scope=a.get("scope", "factory"), book=a.get("book"),
        enum=a.get("enum"), limit=int(a.get("limit", 200))),
    "enum_get": lambda a: T.enum_get(
        enum=a["enum"], value=a["value"],
        scope=a.get("scope", "all"), book=a.get("book")),
    "enum_drift": lambda a: T.enum_drift(
        book=a["book"], layer=a.get("layer"),
        threshold=float(a.get("threshold", 1.5))),
    "enum_sync": lambda a: T.enum_sync(book=a["book"], enum=a.get("enum")),
    "enum_checklist": lambda a: T.enum_checklist(book=a.get("book")),
}


def call_tool(name, arguments):
    if name not in DISPATCH:
        return {"error": "未知工具: %s" % name}
    try:
        return DISPATCH[name](arguments or {})
    except KeyError as e:
        return {"error": "缺少必填参数: %s" % e}
    except Exception as e:  # 只读工具，异常不应中断 server
        return {"error": "%s: %s" % (type(e).__name__, e)}


# ------------------------------------------------------------------ MCP 协议

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
        name = params.get("name")
        out = call_tool(name, params.get("arguments") or {})
        is_err = isinstance(out, dict) and "error" in out and len(out) <= 2
        text = json.dumps(out, ensure_ascii=False, indent=2)
        return _result(rid, {"content": [{"type": "text", "text": text}],
                             "isError": bool(is_err)})
    if method and method.startswith("notifications/"):
        return None
    return _error(rid, -32601, "Method not found: %s" % method)


def serve():
    log("server started (P0 read-only)")
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

def _brief(kind, out):
    """人类可读简报：不做全量 JSON dump，只打结论 + 关键行。"""
    lines = []
    if isinstance(out, dict) and out.get("error"):
        return "错误：" + out["error"]

    if kind == "books":
        lines.append(out.get("summary", ""))
        lines.append("%-22s %-14s %-8s %-6s %s" % ("书", "后端", "枚举组", "via", "备注"))
        for b in out.get("books", []):
            note = b.get("enum_error") or ""
            lines.append("%-22s %-14s %-8s %-6s %s"
                         % (b["book"], b["enum_backend"], b["enum_count"],
                            b.get("loaded_via") or "-", note[:40]))
    elif kind == "list":
        lines.append(out.get("summary", ""))
        for g in out.get("groups", []):
            if g.get("error"):
                lines.append("  ! %s" % g["error"]); continue
            vs = g.get("values", [])
            head = "  [%s] %s (%s%s)  %d 值" % (
                g["origin"], g["enum"], g.get("var") or "",
                " §%s" % g["section"] if g.get("section") else "",
                g["parsed_count"])
            lines.append(head)
            lines.append("      " + "、".join(vs[:40]) + ("…" if g.get("truncated") else ""))
    elif kind == "get":
        lines.append(out.get("summary", ""))
        for f in out.get("found_in", []):
            lines.append("  - %s%s: 精确命中=%s 别名=%s" % (
                f["origin"], "(" + f["book"] + ")" if f.get("book") else "",
                f.get("exact_hit"), f.get("as_alias") or "-"))
        for u in out.get("usage", [])[:10]:
            lines.append("  使用: %s / %s × %d" % (u["book"], u["layer"], u["count"]))
    elif kind == "drift":
        lines.append(out.get("summary", ""))
        lines.append("%-8s %-8s %-6s %-7s %-7s %-7s %-7s %s" % (
            "层", "枚举", "字段", "记录", "实际种", "定义数", "比值", "判定(库外%)"))
        for r in out.get("layers", []):
            lines.append("%-8s %-8s %-6s %-7d %-7d %-7s %-7s %s(%s%%)" % (
                r["layer"], r["enum_key"] or "-", r["field"], r["records"],
                r["distinct"], r["defined"] if r["defined"] is not None else "无",
                r["ratio"] if r["ratio"] is not None else "-",
                r["verdict"], r["outside_pct"]))
            if r["top_outside"]:
                lines.append("      库外: " + "、".join(
                    "%s(%d)" % (v, c) for v, c in r["top_outside"][:8]))
    elif kind == "sync":
        lines.append(out.get("summary", ""))
        if out.get("enum_meta", {}).get("error"):
            lines.append("  ! " + out["enum_meta"]["error"])
        if out.get("schemas_meta", {}).get("note"):
            lines.append("  · " + out["schemas_meta"]["note"])
        for r in out.get("rows", []):
            if not r["factory_only_n"] and not r["instance_only_n"] \
                    and not r.get("missing_in_schemas_n"):
                continue
            lines.append("  [%s] 工厂%d / 实例%d" % (
                r["enum"], r["factory_count"], r["instance_count"]))
            if r["factory_only"]:
                lines.append("      工厂有实例无: " + "、".join(r["factory_only"][:15]))
            if r["instance_only"]:
                lines.append("      实例有工厂无: " + "、".join(r["instance_only"][:15]))
            if r.get("missing_in_schemas_n"):
                lines.append("      schemas 未提及 %d 个: %s" % (
                    r["missing_in_schemas_n"], "、".join(r["missing_in_schemas"][:10])))
    elif kind == "checklist":
        lines.append(out.get("summary", ""))
        for i in out.get("issues", []):
            lines.append("  [%-5s] %s / %s : %s" % (
                i["level"], i["origin"], i["enum"], i["issue"]))
            if i.get("detail"):
                lines.append("            %s" % i["detail"])
    else:
        lines.append(json.dumps(out, ensure_ascii=False, indent=2))
    return "\n".join(lines)


def main(argv=None):
    import argparse
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        serve()
        return 0

    p = argparse.ArgumentParser(prog="server.py",
                                description="古籍知识工程 MCP（P0 只读）CLI 自检")
    p.add_argument("cmd", choices=["books", "list", "get", "drift", "sync",
                                   "checklist", "selftest"])
    p.add_argument("--book", help="书目录名，如 kezuozhuiyu-kb")
    p.add_argument("--enum")
    p.add_argument("--value")
    p.add_argument("--scope", default="factory")
    p.add_argument("--layer")
    p.add_argument("--threshold", type=float, default=1.5)
    p.add_argument("--limit", type=int, default=200)
    p.add_argument("--format", choices=["brief", "json"], default="brief")
    a = p.parse_args(argv)

    if a.cmd == "selftest":
        return selftest()

    args = {}
    if a.cmd == "books":
        out = T.kb_books()
    elif a.cmd == "list":
        out = T.enum_list(scope=a.scope, book=a.book, enum=a.enum, limit=a.limit)
    elif a.cmd == "get":
        if not (a.enum and a.value):
            print("get 需要 --enum 与 --value", file=sys.stderr); return 2
        out = T.enum_get(enum=a.enum, value=a.value, scope=a.scope, book=a.book)
    elif a.cmd == "drift":
        if not a.book:
            print("drift 需要 --book", file=sys.stderr); return 2
        out = T.enum_drift(book=a.book, layer=a.layer, threshold=a.threshold)
    elif a.cmd == "sync":
        if not a.book:
            print("sync 需要 --book", file=sys.stderr); return 2
        out = T.enum_sync(book=a.book, enum=a.enum)
    else:
        out = T.enum_checklist(book=a.book)

    print(_brief(a.cmd, out) if a.format == "brief"
          else json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def selftest():
    """不挂 MCP 客户端也能验证：跑一遍全部工具，确认都能返回且无异常。"""
    ok = True
    checks = [
        ("kb_books", lambda: T.kb_books()),
        ("enum_list/factory", lambda: T.enum_list(scope="factory", enum="ENTITY")),
        ("enum_get", lambda: T.enum_get(enum="ENTITY", value="star")),
        ("enum_checklist", lambda: T.enum_checklist()),
    ]
    for b in R.list_books():
        checks.append(("enum_drift/%s" % b, lambda b=b: T.enum_drift(book=b)))
        checks.append(("enum_sync/%s" % b, lambda b=b: T.enum_sync(book=b)))
        checks.append(("enum_list/instance/%s" % b,
                       lambda b=b: T.enum_list(scope="instance", book=b)))

    print("自检 %d 项\n" % len(checks))
    for name, fn in checks:
        try:
            out = fn()
            err = out.get("error") if isinstance(out, dict) else None
            if err:
                ok = False
                print("  [FAIL] %-34s %s" % (name, err))
            else:
                s = (out.get("summary", "") if isinstance(out, dict) else "")[:88]
                print("  [ OK ] %-34s %s" % (name, s))
        except Exception as e:
            ok = False
            print("  [FAIL] %-34s %s: %s" % (name, type(e).__name__, e))
    print("\n结果：%s" % ("全部通过" if ok else "存在失败项"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # noqa: B018
        sys.stderr.reconfigure(encoding="utf-8")  # noqa: B018
    except Exception:
        pass
    sys.exit(main())
