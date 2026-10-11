# -*- coding: utf-8 -*-
"""P0 只读工具集。

全部工具：只读、无副作用、不写任何文件。返回结构一律可 JSON 序列化，
并附一段 `summary` 人类可读摘要（CLI 与 MCP 客户端都直接展示这段）。

设计原则（来自 pitfalls #27 的教训）：
  * 拿不到基准就报「无基准」，**绝不猜一个基准去判漂移**；
  * 漂移只看比值与库外占比，不做任何自动修正；
  * 所有结论都给出证据（样例值、来源文件），便于人工复核。
"""

import os
import re

from . import registry as R
from . import adapters as A

# 组合标注分隔符：新官轨范规则层用「程序型+禁止型」表示一条规则兼属多类
_COMBO_SPLIT = re.compile(r"[+＋]")

DEFAULT_THRESHOLD = 1.5
DEFAULT_LIMIT = 200


def _values_of(entry):
    return [v["value"] for v in entry.get("values", [])]


def _aliases_resolve(entry, value):
    """值是否命中（含别名命中）。"""
    vals = set(_values_of(entry))
    if value in vals:
        return True
    canon = entry.get("aliases", {}).get(value)
    return canon in vals if canon else False


# ------------------------------------------------------------------ kb_books

def kb_books():
    """列出受管辖的书：枚举后端形态、层产物是否可扫、schemas 快照是否登记。"""
    fac, ferr = A.parse_factory_library()
    rows = []
    for book in R.list_books():
        cfg = R.BOOKS[book]
        _, meta = A.load_instance_enums(book)
        enums = A.load_instance_enums(book)[0]
        rows.append({
            "book": book,
            "title": cfg["title"],
            "enum_backend": cfg["enum_backend"],
            "enum_path": cfg.get("enum_path"),
            "enum_count": len(enums),
            "enum_error": meta.get("error") or meta.get("note"),
            "loaded_via": meta.get("loaded_via"),
            "schemas": cfg.get("schemas"),
        })
    return {
        "summary": "受管辖 %d 本书；工厂库解析出 %d 组枚举%s" % (
            len(rows), len(fac), ("；错误：" + ferr["error"]) if ferr.get("error") else ""),
        "factory_enum_count": len(fac),
        "books": rows,
    }


# ------------------------------------------------------------------ enum_list

def enum_list(scope="factory", book=None, enum=None, limit=DEFAULT_LIMIT):
    """列规范值。scope=factory（默认，全库）/ instance（某书）/ all。"""
    scope = (scope or "factory").lower()
    result = {"scope": scope, "groups": [], "summary": ""}

    def push(origin, src_label, data, meta):
        keys = sorted(data)
        if enum:
            k = R.canon_key(enum)
            keys = [x for x in keys if x == k or R.canon_key(x) == k]
            if not keys:
                result["groups"].append({
                    "origin": origin, "source": src_label, "enum": enum,
                    "error": "未找到该枚举（可用值见 enum_list 不带 enum 参数）",
                })
                return
        for k in keys:
            e = data[k]
            vals = _values_of(e)
            result["groups"].append({
                "origin": origin,
                "source": src_label,
                "enum": k,
                "var": e.get("var"),
                "section": e.get("section"),
                "name": e.get("name"),
                "declared": e.get("declared"),
                "parsed_count": len(vals),
                "values": vals[:limit],
                "truncated": len(vals) > limit,
                "aliases": e.get("aliases", {}),
                "merged_vars": e.get("merged_vars", []),
            })

    if scope in ("factory", "all"):
        fac, ferr = A.parse_factory_library()
        if ferr.get("error"):
            result["summary"] = ferr["error"]
            return result
        push("factory", os.path.relpath(R.FACTORY_ENUM_LIB, R.REPO_ROOT), fac, ferr)

    if scope in ("instance", "all"):
        if not book:
            result["summary"] = "scope=instance 必须指定 book"
            return result
        if book not in R.BOOKS:
            result["summary"] = "未知的书：%s（可用 kb_books 查看）" % book
            return result
        data, meta = A.load_instance_enums(book)
        if meta.get("error"):
            result["summary"] = meta["error"]
            return result
        if meta.get("note"):
            result["groups"].append({"origin": "instance", "book": book,
                                     "note": meta["note"]})
        push("instance", meta.get("path", book), data, meta)

    real = [g for g in result["groups"] if g.get("enum")]
    n = len(real)
    tot = sum(g.get("parsed_count", 0) for g in real)
    notes = len(result["groups"]) - n
    result["summary"] = "列出 %d 组枚举，共 %d 个规范值（scope=%s%s）%s" % (
        n, tot, scope, (", book=%s" % book) if book else "",
        "；另有 %d 条提示" % notes if notes else "")
    return result


# ------------------------------------------------------------------- enum_get

def enum_get(enum, value, scope="all", book=None):
    """单值详情：在哪一组、是否有别名、是否被层产物实际使用。"""
    out = {"enum": enum, "value": value, "found_in": [], "summary": ""}
    key = R.canon_key(enum)

    fac, _ = A.parse_factory_library()
    if key in fac:
        e = fac[key]
        vals = _values_of(e)
        hit = value in vals
        out["found_in"].append({
            "origin": "factory", "enum": key, "var": e.get("var"),
            "section": e.get("section"),
            "exact_hit": hit,
            "as_alias": e.get("aliases", {}).get(value),
            "doc": next((v["doc"] for v in e["values"] if v["value"] == value), ""),
        })

    for b in ([book] if book else R.list_books()):
        data, meta = A.load_instance_enums(b)
        if key in data:
            e = data[key]
            vals = _values_of(e)
            out["found_in"].append({
                "origin": "instance", "book": b, "var": e.get("var"),
                "exact_hit": value in vals,
                "as_alias": e.get("aliases", {}).get(value),
            })

    # 层产物里实际用到没有
    usage = []
    for b in ([book] if book else R.list_books()):
        try:
            layers = A.scan_layers(b)
        except Exception:
            continue
        for layer, info in layers.items():
            c = info["counts"].get(value)
            if c:
                usage.append({"book": b, "layer": layer, "count": c})
    out["usage"] = usage
    out["usage_total"] = sum(u["count"] for u in usage)

    hits = [f for f in out["found_in"] if f.get("exact_hit")]
    out["summary"] = ("%s 在 %s 中%s；层产物实际使用 %d 次" % (
        value, key,
        ("已定义（%d 处命中）" % len(hits)) if hits else "**未定义**（库外值，命中即漂移）",
        out["usage_total"]))
    return out


# ----------------------------------------------------------------- enum_drift

def enum_drift(book, layer=None, threshold=DEFAULT_THRESHOLD):
    """漂移报告：层产物实际取值种数 vs 枚举定义数。

    比值 > threshold（默认 1.5）判漂移；同时给出库外值占比——客座赘语 #27 事故
    （EVT 111 种 vs 定义 23）就是靠这两个数当场暴露的。
    """
    if book not in R.BOOKS:
        return {"summary": "未知的书：%s" % book, "layers": []}
    fac, _ = A.parse_factory_library()
    inst, _ = A.load_instance_enums(book)
    layers = A.scan_layers(book, only_layer=layer)

    rows = []
    for lname in sorted(layers):
        info = layers[lname]
        counts = info["counts"]
        distinct = len(counts)
        key = R.enum_key_for_layer(lname)

        defined, dsrc, dvars = None, None, []
        if key in inst:
            defined = set(_values_of(inst[key]))
            dsrc = "instance"
            dvars = [inst[key].get("var")]
        elif key in fac:
            defined = set(_values_of(fac[key]))
            dsrc = "factory"
            dvars = [fac[key].get("var")]
        if defined:
            aliases = {}
            src_entry = inst.get(key) or fac.get(key) or {}
            aliases = src_entry.get("aliases", {})
            def known(x):
                x = x.strip()
                return x in defined or aliases.get(x) in defined

            outside, combo = {}, 0
            for v, c in counts.items():
                if known(v):
                    continue
                # 组合标注（程序型+禁止型）：拆开后每部分都合法 → 不是造值，
                # 只是「一条记录兼属多类」。单独计数，不计入库外。
                parts = [p for p in _COMBO_SPLIT.split(v) if p.strip()]
                if len(parts) > 1 and all(known(p) for p in parts):
                    combo += c
                    continue
                outside[v] = c
        else:
            outside, combo = dict(counts), 0

        outside_n = sum(outside.values())
        total = info["total"] or 1
        # 比值用「组合展开后」的种数：新官规则层 38 个原始值其实只由 7 个基本值
        # 组合而成，用 38 去比会把合法的组合标注误判成漂移
        expanded = set()
        for v in counts:
            parts = [p.strip() for p in _COMBO_SPLIT.split(v) if p.strip()]
            expanded.update(parts if len(parts) > 1 else [v])
        eff_distinct = len(expanded)
        ratio = (eff_distinct / len(defined)) if defined else None
        if defined is None:
            verdict = "无基准"
        elif ratio is not None and ratio > threshold:
            verdict = "漂移"
        elif outside_n:
            verdict = "有库外值"
        else:
            verdict = "正常"

        # 组合标注不算漂移，但它是「口径事实」，要在结论里说清楚
        if combo:
            verdict_note = "含组合标注 %d 条" % combo
        else:
            verdict_note = ""

        rows.append({
            "layer": lname,
            "enum_key": key,
            "field": info["field"],
            "combo_records": combo,
            "note": verdict_note,
            "files": info["files"],
            "records": info["total"],
            "distinct": distinct,
            "effective_distinct": eff_distinct,
            "defined": len(defined) if defined else None,
            "defined_source": dsrc,
            "defined_var": dvars,
            "ratio": round(ratio, 2) if ratio is not None else None,
            "outside_count": len(outside),
            "outside_records": outside_n,
            "outside_pct": round(outside_n / total * 100, 1),
            "verdict": verdict,
            "top_outside": sorted(outside.items(), key=lambda x: -x[1])[:12],
            "top_values": sorted(counts.items(), key=lambda x: -x[1])[:8],
        })

    rows.sort(key=lambda r: (-(r["outside_records"]), r["layer"]))
    drift = [r for r in rows if r["verdict"] == "漂移"]
    nbase = [r for r in rows if r["verdict"] == "无基准"]
    nout = sum(r["outside_records"] for r in rows)
    out = {
        "book": book,
        "title": R.BOOKS[book]["title"],
        "threshold": threshold,
        "layers": rows,
        "summary": "%s：扫描 %d 层 / %d 条记录；漂移 %d 层、无基准 %d 层、库外记录共 %d 条"
                   % (R.BOOKS[book]["title"], len(rows),
                      sum(r["records"] for r in rows), len(drift), len(nbase), nout),
    }
    return out


# ------------------------------------------------------------------ enum_sync

def enum_sync(book, enum=None):
    """三处一致性：工厂库 / 实例 _kg_enums.py / 实例 schemas.md 快照。

    - factory_only：工厂有、实例没有 → 实例快照落后（如 v4 新增的 star/event 没同步）
    - instance_only：实例有、工厂没有 → **未回库的本地扩展**，正是 #27 的温床
    - missing_in_schemas：工厂值在 schemas.md 里查不到（文本命中判断，仅作线索）
    """
    if book not in R.BOOKS:
        return {"summary": "未知的书：%s" % book, "rows": []}
    fac, _ = A.parse_factory_library()
    inst, meta = A.load_instance_enums(book)
    snap, snap_meta = A.parse_schemas_snapshot(book)

    # 只比对「实例实际启用」的组。工厂库是全量基准（17 组），而一本书通常只启用
    # 其中几组——把没启用的也算成「实例落后」会让报告变成纯噪音（曾报出 334 个
    # 假差异）。未启用的组单独列为 not_enabled，供人工判断是否该启用。
    inst_keys, fac_keys = set(inst), set(fac)
    keys = sorted((fac_keys & inst_keys) | inst_keys)
    not_enabled = sorted(fac_keys - inst_keys)
    if enum:
        k = R.canon_key(enum)
        keys = [x for x in keys if x == k]

    rows = []
    for k in keys:
        f = set(_values_of(fac[k])) if k in fac else set()
        i = set(_values_of(inst[k])) if k in inst else set()
        row = {
            "enum": k,
            "in_factory": k in fac,
            "in_instance": k in inst,
            "factory_count": len(f),
            "instance_count": len(i),
            "factory_only": sorted(f - i)[:40],
            "instance_only": sorted(i - f)[:40],
            "factory_only_n": len(f - i),
            "instance_only_n": len(i - f),
        }
        if snap:
            miss = [v for v in sorted(f) if not A.value_hits(snap["text"], v)]
            row["schemas_path"] = snap["path"]
            row["missing_in_schemas"] = miss[:40]
            row["missing_in_schemas_n"] = len(miss)
        rows.append(row)

    rows.sort(key=lambda r: -(r["factory_only_n"] + r["instance_only_n"]))
    tot_fo = sum(r["factory_only_n"] for r in rows)
    tot_io = sum(r["instance_only_n"] for r in rows)
    backend = R.BOOKS[book]["enum_backend"]
    summary = "%s：比对 %d 组（实例启用）" % (R.BOOKS[book]["title"], len(rows))
    if backend == "none":
        summary += "；本书无单点枚举文件，无法与工厂库比对（这是 P1.5 要补的前置）"
    else:
        summary += "；工厂有实例无 %d 个值、实例有工厂无 %d 个值" % (tot_fo, tot_io)
        if not_enabled:
            summary += "；工厂另有 %d 组本书未启用" % len(not_enabled)
    out = {
        "book": book,
        "title": R.BOOKS[book]["title"],
        "enum_backend": backend,
        "enum_meta": {k: v for k, v in meta.items() if k in ("error", "note", "path")},
        "schemas_meta": snap_meta,
        "not_enabled": not_enabled,
        "rows": rows,
        "summary": summary,
    }
    return out


# -------------------------------------------------------------- enum_checklist

def enum_checklist(book=None):
    """健康度体检（P0）。

    检查项：
      1. 兜底值（其他 / unknown）是否存在 —— 没有则执行期必然自造值
      2. 树深度 ≤3
      3. 声明值数 vs 解析值数是否一致（不一致多为树状段/多枚举段，需人工确认）
      4. 层产物是否有对应枚举定义（无定义 = 无护栏，自由造值区）
      5. 实体主键表 pending 未决数
    """
    fac, ferr = A.parse_factory_library()
    issues, checked = [], 0

    def check_set(label, data, origin):
        nonlocal checked
        for k in sorted(data):
            e = data[k]
            checked += 1
            vals = e.get("values", [])
            names = [v["value"] for v in vals]
            low = {v.lower() for v in names}
            if k in R.NEEDS_FALLBACK and not (R.FALLBACK_VALUES & low):
                issues.append({
                    "level": "warn", "origin": origin, "enum": k,
                    "issue": "缺兜底值（其他/unknown）——归类型枚举没有出口值",
                    "detail": "执行期遇到无法归类的条目就会自造值（#27 成因）；"
                              "封闭分类型枚举不检查此项",
                })
            depth = max((v.get("depth", 0) for v in vals), default=0)
            if depth > 3:
                issues.append({
                    "level": "warn", "origin": origin, "enum": k,
                    "issue": "树深度 %d > 3" % depth,
                    "detail": "层级过深，回归父类成本高",
                })
            declared = e.get("declared")
            top = e.get("top_count")
            if origin == "factory" and declared and top is not None and declared != top:
                issues.append({
                    "level": "info", "origin": origin, "enum": k,
                    "issue": "声明 %d 个顶层 / 解析出 %d 个顶层（解析值总数 %d，含子类型）"
                             % (declared, top, len(vals)),
                    "detail": "树状段按「顶层+子类型」全封闭集解析，总数大于顶层数属预期；"
                              "顶层数对不上则需人工核对解析口径",
                })
            dup = len(names) - len(set(names))
            if dup:
                issues.append({
                    "level": "error", "origin": origin, "enum": k,
                    "issue": "重复值 %d 个" % dup, "detail": "规范值重复会导致 ID 分配歧义",
                })
            if e.get("merged_vars"):
                issues.append({
                    "level": "info", "origin": origin, "enum": k,
                    "issue": "该段含多个枚举变量 %s" % e["merged_vars"],
                    "detail": "值已并入首变量，比对时口径可能偏松",
                })

    check_set("factory", fac, "factory")
    books = [book] if book else R.list_books()
    for b in books:
        inst, _ = A.load_instance_enums(b)
        check_set(b, inst, b)

        # 层 → 枚举定义覆盖
        try:
            layers = A.scan_layers(b)
        except Exception:
            layers = {}
        has_inst = bool(inst)
        for lname in sorted(layers):
            key = R.enum_key_for_layer(lname)
            if key not in fac and (not has_inst or key not in inst):
                issues.append({
                    "level": "warn", "origin": b, "enum": key,
                    "issue": "层「%s」无对应枚举定义" % lname,
                    "detail": "该层处于无护栏状态，取值不受封闭集约束（%d 条记录）"
                              % layers[lname]["total"],
                })

        # 实体主键表 pending
        ek, ekp = A.load_ent_keys(b)
        if isinstance(ek, dict):
            pend = ek.get("pending")
            n = len(pend) if isinstance(pend, (list, dict)) else 0
            if n:
                issues.append({
                    "level": "info", "origin": b, "enum": "ent_keys",
                    "issue": "实体表有 %d 条 pending 未决" % n,
                    "detail": os.path.relpath(ekp, R.REPO_ROOT) if ekp else "",
                })

    errs = [i for i in issues if i["level"] == "error"]
    warns = [i for i in issues if i["level"] == "warn"]
    out = {
        "checked_groups": checked,
        "errors": len(errs), "warnings": len(warns),
        "issues": issues,
        "summary": "体检 %d 组枚举：%d 项错误 / %d 项警告 / %d 项提示"
                   % (checked, len(errs), len(warns),
                      len(issues) - len(errs) - len(warns)),
    }
    if ferr.get("error"):
        out["summary"] += "；" + ferr["error"]
    return out
