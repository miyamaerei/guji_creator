# -*- coding: utf-8 -*-
"""新书格式契约服务（契约线 C0，最小实现：只回答「格式是什么」）。

两用入口：
    python server.py                  # MCP 模式：JSON-RPC 2.0 over stdio
    python server.py list             # CLI：列出 C1–C7 全部契约项
    python server.py get --id C5      # CLI：取某条契约的完整规定
    python server.py selftest         # 自检

**它不做什么**（刻意不做，别加）：
    - 不扫描任何一本书的数据（那是存量线 tools/kb-mcp/ 的事）
    - 不生成脚手架、不做 book_check（C1/C2 阶段再说）
    - 不提供 add/update/delete——那是治理动作，属于存量线

契约本体在 `contract.json`，是唯一真源；本文件只是读取 + 回答。
改格式请改 contract.json，不要改这里。

零第三方依赖（与存量线同风格，手写 MCP 协议，协议版本 2024-11-05，
日志走 stderr）。
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTRACT_PATH = os.path.join(HERE, "contract.json")

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "guji-book-contract"
SERVER_VERSION = "0.1.0-c0"


# ------------------------------------------------------------------ 契约读取

def load_contract():
    with open(CONTRACT_PATH, encoding="utf-8") as f:
        return json.load(f)


def contract_list():
    c = load_contract()
    return {
        "format_version": c.get("format_version"),
        "applies_to": c.get("applies_to"),
        "principle": c.get("principle", []),
        "contracts": [{"id": x["id"], "title": x["title"],
                       "statement": x.get("statement", "")}
                      for x in c.get("contracts", [])],
        "summary": "格式契约 v%s，共 %d 条（%s）。带 id 调 contract_get 看完整规定。"
                   % (c.get("format_version"),
                      len(c.get("contracts", [])),
                      "、".join(x["id"] for x in c.get("contracts", []))),
    }


def contract_get(cid):
    c = load_contract()
    key = (cid or "").strip().upper()
    for x in c.get("contracts", []):
        if x["id"].upper() == key:
            out = dict(x)
            out["format_version"] = c.get("format_version")
            out["summary"] = "[%s] %s —— %s" % (
                x["id"], x.get("title", ""), x.get("statement", ""))
            return out
    return {"error": "没有这条契约：%s。可用：%s"
                     % (cid, "、".join(x["id"] for x in c.get("contracts", [])))}


# ------------------------------------------------------------------ 工具声明

TOOLS = [
    {
        "name": "contract_list",
        "description": "列出新书格式契约的全部条目（C1–C7）与格式版本号。"
                       "开工一本新书前先调这个，确认要遵守哪些格式。",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "contract_get",
        "description": "取某一条格式契约的完整规定：规定内容、为什么这么定（现状乱在哪）、"
                       "可校验点、正例反例、条文出处。如 id=C5 是「枚举单点必建」。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {"type": "string",
                       "description": "契约编号，如 C1 / C2 / C5（大小写不限）"},
            },
            "required": ["id"],
        },
    },
]

DISPATCH = {
    "contract_list": lambda a: contract_list(),
    "contract_get": lambda a: contract_get(a["id"]),
}


def call_tool(name, arguments):
    if name not in DISPATCH:
        return {"error": "未知工具: %s" % name}
    try:
        return DISPATCH[name](arguments or {})
    except KeyError as e:
        return {"error": "缺少必填参数: %s" % e}
    except Exception as e:
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
        out = call_tool(params.get("name"), params.get("arguments") or {})
        is_err = isinstance(out, dict) and "error" in out and len(out) <= 2
        return _result(rid, {"content": [{"type": "text",
                                          "text": json.dumps(out, ensure_ascii=False, indent=2)}],
                             "isError": bool(is_err)})
    if method and method.startswith("notifications/"):
        return None
    return _error(rid, -32601, "Method not found: %s" % method)


def serve():
    log("server started (C0 read-only)")
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

def _brief_list(out):
    lines = [out.get("summary", "")]
    lines.append("")
    for p in out.get("principle", []):
        lines.append("  · %s" % p)
    lines.append("")
    for x in out.get("contracts", []):
        lines.append("  [%s] %-8s %s" % (x["id"], x["title"], x["statement"]))
    return "\n".join(lines)


def _brief_get(out):
    lines = [out.get("summary", "")]
    lines.append("")
    if out.get("why"):
        lines.append("为什么这么定：%s" % out["why"])
    lines.append("")
    lines.append("可校验点：")
    for r in out.get("rules", []):
        args = r.get("args", {})
        desc = args.get("desc") or args.get("name") or args.get("pattern") or ""
        lines.append("  - %-26s %s" % (r.get("check"), desc))
    if out.get("reference_layer_keys"):
        lines.append("")
        lines.append("参考层 key：" + "、".join(out["reference_layer_keys"]))
    lines.append("")
    lines.append("  正例：%s" % out.get("ok", "-"))
    lines.append("  反例：%s" % out.get("bad", "-"))
    if out.get("source"):
        lines.append("  出处：%s" % out["source"])
    return "\n".join(lines)


def selftest():
    checks = [
        ("contract_list", lambda: contract_list()),
    ] + [("contract_get/%s" % cid, lambda cid=cid: contract_get(cid))
         for cid in ["C1", "C2", "C3", "C4", "C5", "C6", "C7"]] + [
        ("contract_get/未知 id", lambda: contract_get("C9")),
    ]
    print("自检 %d 项\n" % len(checks))
    ok = True
    for name, fn in checks:
        try:
            out = fn()
            if name.endswith("未知 id"):
                good = isinstance(out, dict) and "error" in out
                print("  [%s] %-22s %s" % (" OK " if good else "FAIL", name,
                                           "正确报错" if good else "应当报错却通过了"))
                ok = ok and good
                continue
            if isinstance(out, dict) and out.get("error"):
                ok = False
                print("  [FAIL] %-22s %s" % (name, out["error"]))
            else:
                print("  [ OK ] %-22s %s" % (name, out.get("summary", "")[:60]))
        except Exception as e:
            ok = False
            print("  [FAIL] %-22s %s: %s" % (name, type(e).__name__, e))
    print("\n结果：%s" % ("全部通过" if ok else "存在失败项"))
    return 0 if ok else 1


def main(argv=None):
    import argparse
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        serve()
        return 0

    p = argparse.ArgumentParser(prog="server.py",
                                description="新书格式契约服务（C0 只读）CLI")
    p.add_argument("cmd", choices=["list", "get", "selftest"])
    p.add_argument("--id", help="契约编号，如 C5")
    p.add_argument("--format", choices=["brief", "json"], default="brief")
    a = p.parse_args(argv)

    if a.cmd == "selftest":
        return selftest()

    if a.cmd == "list":
        out = contract_list()
        print(_brief_list(out) if a.format == "brief"
              else json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    if not a.id:
        print("get 需要 --id", file=sys.stderr)
        return 2
    out = contract_get(a.id)
    if a.format == "json" or out.get("error"):
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(_brief_get(out))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # noqa: B018
        sys.stderr.reconfigure(encoding="utf-8")  # noqa: B018
    except Exception:
        pass
    sys.exit(main())
