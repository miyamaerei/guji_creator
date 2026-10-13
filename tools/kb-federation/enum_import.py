"""enum_import.py —— 稀疏表填充（一）：枚举基准库 → enum_registry / enum_values + 漂移检测

背景（见 docs/联邦库原表增量与稀疏诊断.md §2.2）：联邦库 enum_registry / enum_values /
enum_drift 三张表**从未被任何代码写入**，全为 0 行；但「枚举封闭、单点 _kg_enums.py」
是 guji 项目核心铁律。本模块把权威源 `Skills/00-…/references/enum-library.md`
（v6，18 个枚举组）解析进联邦库，并做漂移检测填 enum_drift。

解析策略（枚举库格式不统一，需同时处理多种形态）：
  - 代码块（```…```）逐行；支持「顶层 ─ 子类1 / 子类2」树、一行多值（用 " / " 分隔）、
    「值（别名：x）」别名提取；跳过 来源/使用说明/方向/归并 等元信息行。
  - 表格（EVENT_TYPES §1.3 用 markdown 表）：解析 | 规范值 | 使用说明 | 别名 | 来源 |
    与 | 子类型 | 父类 | 首建实例 | 两型；首列可能用 " / " 拼多个值；顶层 is_top=1，
    子类型带 parent。§1.3.3 归并映射表不是枚举值，截断排除。
  - §1.15 同节定义 CIT_TYPES（引用方式）+ CIT_CONTEXT（引用目的）两个组，拆开收录。

幂等：先 DELETE 再 INSERT OR REPLACE。枚举库升级（v7…）重跑本命令即可刷新。

用法：
  python federation.py enum-import          # 导入 + 漂移检测
  python federation.py enum-import --no-drift
零第三方依赖。
"""

import os
import re
import sqlite3
import json
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))
ENUM_LIB = os.path.join(
    REPO_ROOT, "Skills", "00-book-knowledge-factory", "references", "enum-library.md"
)

# 漂移检测：层 → {payload 字段名: 枚举组}。仅扫这些 (层,字段)，避免噪声。
# 字段名与枚举组均来自 enum-library.md（v6）各组与六书 records payload 实测普查。
LAYER_ENUM_FIELDS = {
    "ent":   {"type": "ENTITY_TYPES"},
    "event": {"type": "EVENT_TYPES"},
    "evt":   {"type": "EVENT_TYPES"},
    "appt":  {"status": "APPT_STATUS"},
    "opn":   {"stance": "OPN_STANCES"},
    "obj":   {"category": "OBJ_TYPES"},
    "reg":   {"type": "REG_TYPES"},
    "rule":  {"type": "RULE_TYPES"},
    "cus":   {"type": "CUS_TYPES"},
    "trl":   {"style": "TRL_STYLES"},
    "ming":  {"category": "MING_TYPES"},
    "chr":   {"category": "CHR_CATEGORIES"},
    "cit":   {"citation_type": "CIT_TYPES", "context": "CIT_CONTEXT"},
    "struct":{"dim": "STRUCT", "frd_type": "STRUCT", "lgr_type": "STRUCT",
              "act_type": "STRUCT", "tme_type": "STRUCT"},
    "nam":   {"category": "NAM_TYPES"},
    "rel":   {"relation_type": "REL_TYPES", "type": "REL_TYPES"},
    "proc":  {"event_type": "EVENT_TYPES"},
    "geo":   {"category": "GEO_TYPES"},
    "lit":   {"type": "LIT_TYPES"},
}


def _clean_val(s):
    """取规范值：去反引号/括号/后缀说明，取首 token。"""
    s = s.strip().strip("`").strip()
    s = re.split(r"[（(【\[]", s)[0].strip()
    toks = s.split()
    return toks[0] if toks else s


def _split_tokens(s):
    """把一行/一个单元格按枚举分隔符切成多个值 token。

    支持「值 / 值」「值＋值」（含行首/行尾分隔符、全角 ／＋）的多值写法；
    括号内（含中文 （）与英文 ()）的内容受「深度保护」，不被拆开——
    避免「民俗（别名：习俗 / 礼俗）」「山岳（别名：山/山岭）」里的 / 被误拆。
    """
    out = []
    cur = ""
    depth = 0
    for ch in s:
        if ch in "（(":
            depth += 1
            cur += ch
        elif ch in "）)":
            depth -= 1
            cur += ch
        elif ch in "/／+" and depth == 0:
            if cur.strip():
                out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return [p for p in out if p]


def _extract_alias(tok):
    """从单个值 token 抽出 (规范值, 别名)。兼容「值（别名：x）」与「值 中文标签」。"""
    alias = None
    am = re.search(r"别名[：:]\s*([^）)】\]]+)", tok)
    if am:
        alias = am.group(1).strip()
    val = re.split(r"[（(【\[]", tok)[0].strip()
    val = val.strip("`").strip()
    val = val.split()[0] if val.split() else val   # 「person 人物」取英文键
    return val, alias


def _parse_body(body, group_name):
    """解析一个枚举组的正文，返回 [(value, alias, is_top, parent), ...]。"""
    # EVENT_TYPES 的 §1.3.3 归并表不是枚举值，截断排除
    if group_name == "EVENT_TYPES":
        idx = body.find("#### 1.3.3")
        if idx != -1:
            body = body[:idx]

    lines = body.splitlines()

    # —— 形态 A：markdown 表格（EVENT_TYPES §1.3）——
    table_rows = [l for l in lines if l.strip().startswith("|")]
    if len(table_rows) >= 2:
        return _parse_table(table_rows, body)

    # —— 形态 B：代码块逐行 / 或 §1.15 无围栏的「引用方式：…」列表 ——
    infence = False
    fenced_seen = False
    content_lines = []
    for l in lines:
        if l.strip().startswith("```"):
            fenced_seen = True
            infence = not infence
            continue
        if fenced_seen and not infence:
            continue                      # 围栏外、且已见过围栏 → 跳过
        content_lines.append(l)
    values = []
    for l in content_lines:
        l = re.sub(r"^(引用方式|引用目的)[：:]\s*", "", l.strip()).strip("`").strip()
        if not l or l.startswith(">") or l.startswith("#"):
            continue
        if any(k in l for k in ("来源：", "使用说明：", "方向", "归并说明",
                                 "实测分布", "命名对齐", "归并映射", "使用说明")):
            continue
        # 树：顶层 ─ 子类1 / 子类2
        if "─" in l or "——" in l:
            parts = re.split(r"[─—]", l)
            top, top_a = _extract_alias(parts[0])
            if top:
                values.append((top, top_a, 1, None))
            if len(parts) > 1:
                for tok in _split_tokens(parts[1]):
                    v, a = _extract_alias(tok)
                    if v:
                        values.append((v, a, 0, top))
            continue
        for tok in _split_tokens(l):
            v, a = _extract_alias(tok)
            if v and not v.startswith("*") and "分支" not in v and "·" not in v:
                values.append((v, a, 1, None))
    return values


def _parse_table(rows, body):
    """解析 EVENT_TYPES 的 markdown 表（顶层 §1.3.1 与子类型 §1.3.2 两型）。"""
    is_sub = ("子类型" in body[:400]) or ("父类" in body[:600])
    header = None
    data = []
    for r in rows:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        # 跳过 markdown 分隔行（|---|---|）
        if cells and all(re.fullmatch(r"-+", c) for c in cells if c):
            continue
        zn = {"规范值", "使用说明", "别名", "来源", "子类", "子类型", "父类", "首建实例", ""}
        if set(cells) <= zn and any(c for c in cells):
            header = cells
            continue
        if cells and cells[0] and not all(c == "" for c in cells):
            data.append(cells)
    values = []
    skip = {"子类", "子类型", "规范值", "客座原值", "归并到", "说明", "---"}
    for cells in data:
        # 首列可能用 " / " 拼了多个值（§1.3.2 一行多子类型）
        toks = _split_tokens(cells[0])
        alias_col = ""
        if header and "别名" in header:
            ai = header.index("别名")
            if ai < len(cells):
                alias_col = cells[ai]
        for t in toks:
            v, a = _extract_alias(t)
            if not v or v in skip or v.startswith("*"):
                continue
            combined = a
            if alias_col:
                ac, _ = _extract_alias(alias_col)
                if ac and ac != v:
                    combined = (combined + "/" + ac) if combined else ac
            parent = None
            if header:
                for ci, c in enumerate(header):
                    if ci < len(cells) and c == "父类" and cells[ci]:
                        parent = _clean_val(cells[ci])
            if is_sub and parent:
                values.append((v, combined, 0, parent))
            else:
                values.append((v, combined, 1, None))
    return values


def parse_enum_library(path=ENUM_LIB):
    """返回 [(group_name, zh_name, sec_no, [(value, alias, is_top, parent), ...]), ...]。"""
    text = open(path, encoding="utf-8").read()
    hdr = re.compile(r"^###\s+1\.(\d+)\s+([^\n]+)$", re.M)
    matches = list(hdr.finditer(text))
    groups = []
    for i, m in enumerate(matches):
        sec_no = m.group(1)
        header_line = m.group(2).strip()
        gm = re.search(r"([A-Z][A-Z_]{2,})", header_line)
        group_name = gm.group(1) if gm else header_line
        zh_name = header_line[: gm.start()].strip() if gm else header_line
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.end():end]
        vals = _parse_body(body, group_name)

        # §1.15 同节定义两个组：引用方式 CIT_TYPES / 引用目的 CIT_CONTEXT
        if group_name == "CIT_TYPES" and "引用目的" in body:
            pre, _, post = body.partition("引用目的：")
            v1 = _parse_body(pre, "CIT_TYPES")
            v2 = _parse_body(post, "CIT_CONTEXT")
            groups.append(("CIT_TYPES", "引用方式", sec_no, v1))
            groups.append(("CIT_CONTEXT", "引用目的", sec_no, v2))
            continue

        groups.append((group_name, zh_name, sec_no, vals))
    return groups


def import_enums(con):
    """解析枚举库并写入 enum_registry / enum_values（先删后插，幂等）。"""
    groups = parse_enum_library()
    con.execute("DELETE FROM enum_registry")
    con.execute("DELETE FROM enum_values")
    reg_rows = []
    val_rows = []
    for gname, zh, sec, vals in groups:
        if not vals:
            continue
        reg_rows.append((gname, zh, "v6", "1." + sec))
        seen = set()
        for v, alias, is_top, parent in vals:
            key = (gname, v)
            if key in seen:
                continue
            seen.add(key)
            val_rows.append((gname, v, 1 if is_top else 0, parent, alias))
    con.executemany(
        "INSERT OR REPLACE INTO enum_registry(enum_group,name,version,section) VALUES(?,?,?,?)",
        reg_rows,
    )
    con.executemany(
        "INSERT OR REPLACE INTO enum_values(enum_group,value,is_top,parent,alias) VALUES(?,?,?,?,?)",
        val_rows,
    )
    con.commit()
    return {
        "groups": len(reg_rows),
        "values": len(val_rows),
        "tops": sum(1 for _, _, t, _p, _a in val_rows if t),
    }


def _parts_allowed(val, allowed):
    """组合值（用 + 连接，如 义务型+程序型）逐段判定。"""
    parts = re.split(r"[+＋]", val)
    if len(parts) <= 1:
        return val in allowed
    return all(p.strip() in allowed for p in parts)


def compute_drift(con):
    """漂移检测：扫 records payload，命中 LAYER_ENUM_FIELDS 的 (层,字段) 取值，
    不在 enum_values[组]（含别名）即记 enum_drift。组合值逐段判定。"""
    group_vals = {}
    for g, v, _t, _p, a in con.execute(
        "SELECT enum_group,value,is_top,parent,alias FROM enum_values"
    ):
        group_vals.setdefault(g, set()).add(v)
        if a:
            for part in re.split(r"[/／]", a):
                part = part.strip()
                if part:
                    group_vals[g].add(part)
    drift = {}  # (book,layer,field,group,value) -> count
    for book, layer, payload in con.execute(
        "SELECT book_id,layer_key,payload FROM records"
    ):
        fmap = LAYER_ENUM_FIELDS.get(layer)
        if not fmap:
            continue
        try:
            rec = json.loads(payload)
        except Exception:
            continue
        if not isinstance(rec, dict):
            continue
        for field, group in fmap.items():
            if field not in rec:
                continue
            raw = rec[field]
            cands = raw if isinstance(raw, list) else [raw]
            for val in cands:
                val = (val or "").strip()
                if not val:
                    continue
                allowed = group_vals.get(group, set())
                if _parts_allowed(val, allowed):
                    continue
                key = (book, layer, field, group, val)
                drift[key] = drift.get(key, 0) + 1
    con.execute("DELETE FROM enum_drift")
    rows = [
        (b, l, f, g, v, 0, c) for (b, l, f, g, v), c in drift.items()
    ]
    con.executemany(
        "INSERT OR REPLACE INTO enum_drift"
        "(book_id,layer_key,field,enum_group,value,in_library,count) VALUES(?,?,?,?,?,?,?)",
        rows,
    )
    con.commit()
    return {"drift_rows": len(rows), "distinct_values": len(drift)}


if __name__ == "__main__":
    con = sqlite3.connect(os.path.join(HERE, "kb.sqlite"))
    con.execute("PRAGMA foreign_keys=OFF")
    imp = import_enums(con)
    print("枚举导入：groups=%d values=%d (顶层 %d)" % (imp["groups"], imp["values"], imp["tops"]))
    dr = compute_drift(con)
    print("漂移检测：distinct=%d rows=%d" % (dr["distinct_values"], dr["drift_rows"]))
    con.close()
