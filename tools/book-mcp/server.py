# -*- coding: utf-8 -*-
"""新书格式契约服务（契约线 C0，只读：只回答「格式是什么」）。

两用入口：
    python server.py                        # MCP 模式：JSON-RPC 2.0 over stdio
    python server.py list                   # C1–C7 七条契约
    python server.py get --id C5            # 某条契约的完整规定
    python server.py layers                 # 层库：全部候选层
    python server.py layer --key appt       # 某一层的定义（key/code/前缀/名称均可）
    python server.py enums                  # 工厂基准枚举库：全部组
    python server.py enum --group EVENT     # 某组枚举的规范值
    python server.py selftest               # 自检

六个工具：contract_list / contract_get / layer_list / layer_get / enum_list / enum_get。

**它不做什么**（刻意不做，别加）：
    - 不扫描任何一本书的数据（那是存量线 tools/kb-mcp/ 的事）
    - 不生成脚手架、不做 book_check（C1/C2 阶段再说）
    - 不提供 add/update/delete——那是治理动作，属于存量线

**不抄值原则**：`contract.json` 只存「格式规则」。层定义与枚举规范值在运行时从
`Skills/00-…/references/` 下的权威源读（路径写在 contract.json 的 sources 里），
避免副本过期——`enum-induction-guide.md` 曾因抄了一份事件树而过期的教训。
枚举值解析复用存量线 `kb_mcp/adapters.py`（它踩过 8 个坑，不重复造轮子）；
复用失败时 enum_* 降级，其余工具不受影响。

零第三方依赖（与存量线同风格，手写 MCP 协议，协议版本 2024-11-05，日志走 stderr）。
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTRACT_PATH = os.path.join(HERE, "contract.json")

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "guji-book-contract"
SERVER_VERSION = "0.1.0-c0"

LAYER_FIELDS = ["定义", "适用信号", "schema 要点", "ID 前缀", "枚举",
                "执行流程", "执行注意", "产出", "schema", "配套",
                "配套字段（provenance 溯源）", "判定方法"]


# ------------------------------------------------------------------ 契约读取

def load_contract():
    with open(CONTRACT_PATH, encoding="utf-8") as f:
        return json.load(f)


def src_path(name):
    c = load_contract()
    return os.path.normpath(os.path.join(HERE, c["sources"][name]))


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


# ------------------------------------------------------------------ 层库解析

_HEAD_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
_CODE_RE = re.compile(r"^((?:L|C|V)\d+)\s+(.*)$")
_PREFIX_RE = re.compile(r"[（(]([A-Za-z]{2,8})[）)]\s*$")
_FIELD_RE = re.compile(r"^-\s+\*\*(.+?)\*\*[：:]\s*(.*)$")


def parse_layer_library(path=None):
    """解析 layer-library.md：按 ## / ### 标题切条，只保留带「定义」字段的条目。

    层库标题有两种形态：
        ## L1 实体层（术语/人物/机构/概念成体系时建）   → 无前缀括号
        ### C1 职官任职层（APPT）                      → 括号内是 ID 前缀
    引导性章节（「自定义层注册（v9…）」「版本记录」）下面没有「定义」字段，
    靠 filters 自然滤掉，不需要维护黑名单。
    """
    path = path or src_path("layer_library")
    if not os.path.exists(path):
        return [], "层库不存在: %s" % path

    by_code = load_contract().get("layer_key_by_code", {})
    items = []
    cur = None
    with open(path, encoding="utf-8") as f:
        for ln in f:
            ln = ln.rstrip("\n")
            m = _HEAD_RE.match(ln)
            if m:
                rest = m.group(2).strip()
                cm = _CODE_RE.match(rest)
                code = cm.group(1) if cm else ""
                name = cm.group(2).strip() if cm else rest
                name = re.split(r"[（(]", name)[0].strip()
                pm = _PREFIX_RE.search(rest)
                prefix = pm.group(1).upper() if pm else ""
                cur = {"code": code, "name": name, "prefix": prefix,
                       "fields": {}}
                items.append(cur)
                continue
            if cur is None:
                continue
            fm = _FIELD_RE.match(ln.strip())
            if fm:
                cur["fields"][fm.group(1).strip()] = fm.group(2).strip()

    out = []
    for it in items:
        if not it["fields"].get("定义"):
            continue  # 引导语/版本记录，不是层
        key = (it["prefix"].lower()
               or by_code.get(it["code"], "")
               or it["code"].lower())
        if not key and "跨层索引" in it["name"]:
            key = "kg_join"  # C2 里的保留名
        inferred = not it["prefix"]
        it["key"] = key
        it["prefix_inferred"] = inferred
        if inferred and key and key != "kg_join":
            it["prefix"] = key.upper()  # 按 layer_key 推导，只作建议
        it["kind"] = ("层" if it["code"].startswith(("L", "C"))
                      else "治理/索引组件")
        out.append(it)
    return out, None


def find_layer(key):
    layers, err = parse_layer_library()
    if err:
        return None, err
    k = (key or "").strip().lower()
    if not k:
        return None, "需要 key（layer_key / code / 前缀 / 名称均可，如 appt / C1 / TRL / 名物）"
    for L in layers:  # 精确
        if k in (L["key"].lower(), L["code"].lower(),
                 L["prefix"].lower(), L["name"].lower()):
            return L, None
    for L in layers:  # 子串
        if k in L["name"].lower() or k in L["key"].lower():
            return L, None
    return None, "层库里没有「%s」。用 layer_list 看全部（%s）" % (
        key, "、".join(L["key"] or L["code"] for L in layers))


def layer_list():
    layers, err = parse_layer_library()
    if err:
        return {"error": err}
    rows = [{"key": L["key"], "code": L["code"], "prefix": L["prefix"],
             "prefix_inferred": L["prefix_inferred"],
             "name": L["name"], "kind": L["kind"],
             "definition": L["fields"].get("定义", "")}
            for L in layers]
    return {
        "rows": rows,
        "summary": "层库共 %d 项（层 + 治理/索引组件）。这是**候选池不是强制清单**——"
                   "新书按适用信号选配后锁死，选中的层按 C4 注册 layer_key/目录/前缀/schema/枚举字段。"
                   % len(rows),
        "contract": "C4",
    }


def layer_get(key):
    L, err = find_layer(key)
    if err:
        return {"error": err}
    return {
        "key": L["key"], "code": L["code"], "prefix": L["prefix"],
        "name": L["name"], "kind": L["kind"],
        "fields": {k: v for k, v in L["fields"].items()},
        "summary": "[%s] %s（%s）—— %s" % (
            L["code"] or L["key"], L["name"], L["prefix"] or "无前缀",
            L["fields"].get("定义", "")),
        "contract_hint": "C4：layer_key 与目录名必须一致（snake_case 单数，无别名），"
                         "开工时登记 {layer_key, dir, prefix, schema_fields, enum_fields}；"
                         "ID 前缀全局唯一、禁止跨层占用（C2）。",
    }


# ------------------------------------------------------------------ 枚举库

_ENUM_CACHE = {"loaded": False, "data": None, "error": None}


def load_factory_enums():
    """复用存量线已验证的 enum-library.md 解析（它踩过 8 个坑，不重复实现）。

    失败时返回 (None, 说明)，enum_* 降级，其余工具不受影响。
    """
    if _ENUM_CACHE["loaded"]:
        return _ENUM_CACHE["data"], _ENUM_CACHE["error"]
    path = src_path("enum_library")
    try:
        kb = os.path.normpath(os.path.join(HERE, "..", "kb-mcp"))
        if kb not in sys.path:
            sys.path.insert(0, kb)
        from kb_mcp import adapters as A  # noqa: E402
        data, err = A.parse_factory_library(path)
        if err.get("error"):
            _ENUM_CACHE.update(loaded=True, data=None, error=err["error"])
        else:
            _ENUM_CACHE.update(loaded=True, data=data, error=None)
    except Exception as e:
        _ENUM_CACHE.update(loaded=True, data=None, error=(
            "枚举库解析不可用（%s: %s）。契约与层库查询不受影响。"
            % (type(e).__name__, e)))
    return _ENUM_CACHE["data"], _ENUM_CACHE["error"]


def _pick_group(data, group):
    g = (group or "").strip().upper()
    if not g:
        return None
    for k in sorted(data):
        if k.upper() == g:
            return k
    for k in sorted(data):          # 子串兜底
        if g in k.upper() or (data[k].get("name") and g in data[k]["name"].upper()):
            return k
    return None


def enum_list(group=None, limit=40):
    data, err = load_factory_enums()
    if err:
        return {"error": err}
    keys = sorted(data)
    if group:
        k = _pick_group(data, group)
        if not k:
            return {"error": "没有这组枚举：%s" % group, "available": keys}
        keys = [k]
    rows = []
    for k in keys:
        e = data[k]
        vals = [v["value"] for v in e.get("values", [])]
        rows.append({"enum": k, "name": e.get("name"), "section": e.get("section"),
                     "declared": e.get("declared"), "top_count": e.get("top_count"),
                     "parsed_count": len(vals),
                     "values": vals[:limit], "truncated": len(vals) > limit})
    return {
        "groups": rows,
        "summary": "工厂基准枚举库共 %d 组（列出 %d 组）。这是新书归纳枚举的**种子值**，"
                   "不是照抄清单——按本书文本归纳后落单点 _kg_enums.py（C5）。"
                   % (len(data), len(rows)),
        "contract": "C5",
    }


def enum_get(group, limit=200):
    data, err = load_factory_enums()
    if err:
        return {"error": err}
    k = _pick_group(data, group)
    if not k:
        return {"error": "没有这组枚举：%s" % group, "available": sorted(data)}
    e = data[k]
    vals = [v["value"] for v in e.get("values", [])]
    tops = [v["value"] for v in e.get("values", []) if v.get("depth", 0) == 0]
    subs = [v for v in vals if v not in tops]
    return {
        "enum": k, "name": e.get("name"), "section": e.get("section"),
        "var": e.get("var"), "declared": e.get("declared"),
        "top_count": e.get("top_count"), "parsed_count": len(vals),
        "top_values": tops, "sub_values": subs[:limit],
        "values": vals[:limit], "truncated": len(vals) > limit,
        "aliases": e.get("aliases", {}),
        "summary": "[%s] %s —— 声明 %s 个 / 解析 %d 个（顶层 %s 个），出处 %s。"
                   % (k, e.get("name"), e.get("declared"), len(vals),
                      e.get("top_count"), e.get("section")),
        "contract_hint": "C5：新书必须建单点 _kg_enums.py，值从它读、禁内嵌打包器；"
                         "封闭集 + 归类型必带兜底值；打包器对未注册值记 ERR；"
                         "改值 version+1 并双写 enum-changelog.md。",
    }


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
    {
        "name": "layer_list",
        "description": "列层库全部候选项（C1–C12 自定义层 / L0–L5 基础层 / V1–V3 治理与索引组件），"
                       "每项给 layer_key、code、ID 前缀与一句话定义。新书选层前先调这个。",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "layer_get",
        "description": "取某一层的完整定义：定义、适用信号、schema 要点、ID 前缀、枚举要求、"
                       "执行流程/注意、参考来源。key 可以是 layer_key（appt）、code（C1）、"
                       "ID 前缀（TRL）或名称片段（名物），大小写不限。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "key": {"type": "string",
                        "description": "层标识，如 appt / C1 / TRL / 名物 / evt"},
            },
            "required": ["key"],
        },
    },
    {
        "name": "enum_list",
        "description": "列工厂基准枚举库（enum-library.md v4）的全部组及其规范值。"
                       "这是新书归纳枚举的种子值，不是照抄清单。带 group 只看一组。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "group": {"type": "string",
                          "description": "枚举组名（可选），如 EVENT / ENTITY / GEO"},
                "limit": {"type": "integer", "default": 40,
                          "description": "每组最多列几个值"},
            },
            "required": [],
        },
    },
    {
        "name": "enum_get",
        "description": "取某一组枚举的规范值全量、别名映射与声明值数，并附 C5 的格式要求。"
                       "新书做枚举归纳时用来对照基准，避免重造已有值。",
        "inputSchema": {
            "type": "object",
            "properties": {
                "group": {"type": "string",
                          "description": "枚举组名，如 EVENT / ENTITY / OBJ（支持子串）"},
                "limit": {"type": "integer", "default": 200},
            },
            "required": ["group"],
        },
    },
]

DISPATCH = {
    "contract_list": lambda a: contract_list(),
    "contract_get": lambda a: contract_get(a["id"]),
    "layer_list": lambda a: layer_list(),
    "layer_get": lambda a: layer_get(a["key"]),
    "enum_list": lambda a: enum_list(group=a.get("group"),
                                     limit=int(a.get("limit", 40))),
    "enum_get": lambda a: enum_get(group=a["group"],
                                   limit=int(a.get("limit", 200))),
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


def _brief_layers(out):
    lines = [out.get("summary", "")]
    lines.append("")
    lines.append("  %-8s %-6s %-10s %-12s %s" % ("key", "code", "前缀", "名称", "定义"))
    for r in out.get("rows", []):
        pfx = r["prefix"] or "-"
        if r.get("prefix_inferred") and pfx != "-":
            pfx += "*"  # 由 layer_key 推导，非层库写死
        lines.append("  %-8s %-6s %-10s %-12s %s" % (
            r["key"] or "-", r["code"] or "-", pfx,
            r["name"], r["definition"][:44]))
    return "\n".join(lines)


def _brief_layer(out):
    lines = [out.get("summary", "")]
    lines.append("")
    for k, v in out.get("fields", {}).items():
        lines.append("  %s：%s" % (k, v))
    if out.get("contract_hint"):
        lines.append("")
        lines.append("  格式要求（%s）：%s" % (out.get("contract", "C4"),
                                              out["contract_hint"]))
    return "\n".join(lines)


def _brief_enums(out):
    lines = [out.get("summary", "")]
    lines.append("")
    for g in out.get("groups", []):
        lines.append("  [%-14s] %-10s %s 个值（顶层 %s，声明 %s）  %s" % (
            g["enum"], g.get("name") or "", g["parsed_count"],
            g.get("top_count"), g.get("declared"), g.get("section") or ""))
        lines.append("      " + "、".join(g["values"][:20])
                     + ("…" if g.get("truncated") else ""))
    return "\n".join(lines)


def _brief_enum(out):
    lines = [out.get("summary", "")]
    lines.append("")
    tops = out.get("top_values") or out["values"]
    lines.append("  顶层值（%d）：" % len(tops))
    lines.append("    " + "、".join(tops[:60])
                 + ("…" if len(tops) > 60 else ""))
    if out.get("sub_values"):
        lines.append("")
        lines.append("  子类值（%d）：" % len(out["sub_values"]))
        lines.append("    " + "、".join(out["sub_values"][:60])
                     + ("…" if len(out["sub_values"]) > 60 else ""))
    if out.get("aliases"):
        lines.append("")
        lines.append("  别名映射（%d）：" % len(out["aliases"]))
        for a, t in list(out["aliases"].items())[:20]:
            lines.append("    %s → %s" % (a, t))
    if out.get("contract_hint"):
        lines.append("")
        lines.append("  格式要求（C5）：%s" % out["contract_hint"])
    return "\n".join(lines)


def selftest():
    checks = [
        ("contract_list", lambda: contract_list()),
        ("layer_list", lambda: layer_list()),
        ("layer_get/appt", lambda: layer_get("appt")),
        ("layer_get/C1", lambda: layer_get("C1")),
        ("layer_get/TRL", lambda: layer_get("TRL")),
        ("layer_get/名物", lambda: layer_get("名物")),
        ("layer_get/evt", lambda: layer_get("evt")),
        ("enum_list", lambda: enum_list()),
        ("enum_get/EVENT", lambda: enum_get("EVENT")),
        ("enum_get/ENTITY", lambda: enum_get("ENTITY")),
    ] + [("contract_get/%s" % cid, lambda cid=cid: contract_get(cid))
         for cid in [x["id"] for x in load_contract().get("contracts", [])]] + [
        ("contract_get/未知 id", lambda: contract_get("C99")),
        ("layer_get/未知 key", lambda: layer_get("不存在的层")),
        ("enum_get/未知组", lambda: enum_get("NOPE")),
    ]
    print("自检 %d 项\n" % len(checks))
    ok = True
    for name, fn in checks:
        try:
            out = fn()
            if "未知" in name:
                good = isinstance(out, dict) and "error" in out
                print("  [%s] %-22s %s" % (" OK " if good else "FAIL", name,
                                           "正确报错" if good else "应当报错却通过了"))
                ok = ok and good
                continue
            if isinstance(out, dict) and out.get("error"):
                ok = False
                print("  [FAIL] %-22s %s" % (name, out["error"]))
            else:
                print("  [ OK ] %-22s %s" % (name, out.get("summary", "")[:62]))
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
    p.add_argument("cmd", choices=["list", "get", "layers", "layer",
                                   "enums", "enum", "selftest"])
    p.add_argument("--id", help="契约编号，如 C5")
    p.add_argument("--key", help="层标识：layer_key / code / 前缀 / 名称，如 appt")
    p.add_argument("--group", help="枚举组名，如 EVENT")
    p.add_argument("--limit", type=int)
    p.add_argument("--format", choices=["brief", "json"], default="brief")
    a = p.parse_args(argv)

    if a.cmd == "selftest":
        return selftest()

    if a.cmd == "list":
        out = contract_list()
        brief = _brief_list(out)
    elif a.cmd == "get":
        if not a.id:
            print("get 需要 --id", file=sys.stderr)
            return 2
        out = contract_get(a.id)
        brief = _brief_get(out)
    elif a.cmd == "layers":
        out = layer_list()
        brief = _brief_layers(out)
    elif a.cmd == "layer":
        if not a.key:
            print("layer 需要 --key", file=sys.stderr)
            return 2
        out = layer_get(a.key)
        brief = _brief_layer(out)
    elif a.cmd == "enums":
        out = enum_list(group=a.group, limit=a.limit or 40)
        brief = _brief_enums(out)
    else:
        if not a.group:
            print("enum 需要 --group", file=sys.stderr)
            return 2
        out = enum_get(a.group, limit=a.limit or 200)
        brief = _brief_enum(out)

    if a.format == "json" or (isinstance(out, dict) and out.get("error")):
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(brief)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # noqa: B018
        sys.stderr.reconfigure(encoding="utf-8")  # noqa: B018
    except Exception:
        pass
    sys.exit(main())
