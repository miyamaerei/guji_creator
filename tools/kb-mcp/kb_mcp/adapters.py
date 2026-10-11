# -*- coding: utf-8 -*-
"""适配器层：把五种互不兼容的枚举载体，读成同一种结构。

产出统一形状（P0 只读，所有函数均无副作用、不写盘）：

    {
      "<CANON_KEY>": {
        "name":      显示名（工厂库标题里的中文名，实例侧则为空）
        "section":   工厂库小节号（如 "1.3"），实例侧为 None
        "var":       原始变量名（ENTITY_TYPES / BASE_ENUMS / ENUM_REGISTRY …）
        "declared":  文档或标题里声明的值个数（int 或 None）
        "values":    [{"value": str, "doc": str, "depth": int, "src": "block"|"table"}]
        "aliases":   {别名: 规范值}
        "source":    来源文件路径
      }
    }

设计取向：**宁可少解析，不可误解析。** 解析不出来就报「无基准 / 需人工确认」，
绝不用猜的值去支撑 drift 结论——那会重演 pitfalls #27（拿错误基准判漂移）。
"""

import ast
import glob as _glob
import importlib.util
import json
import os
import re
import sys

from . import registry as R

# ---------------------------------------------------------------- 通用工具

# 非值的元键（spec 形态下出现在 dict 里，不代表枚举值）
_SPEC_META_KEYS = {
    "version", "doc", "desc", "description", "note", "notes", "source",
    "sources", "deprecated", "since", "owner", "updated", "comment",
}
# 这些键的值是「别名映射」而非枚举值
_SPEC_ALIAS_KEYS = {"alias", "aliases", "alias_map", "synonyms"}
# 这些键的值是「值集合」
_SPEC_LIST_KEYS = {"values", "value", "items", "canonical", "canonicals", "tree"}


def _strip_paren(s):
    """剥离中英文括号注记：`器物（别名：artifact）——说明` → `器物`"""
    s = re.sub(r"[（(].*?[)）]", "", s)
    s = re.split(r"——|--", s)[0]
    return s.strip()


def _first_token(s):
    """取第一个空白前的 token；无空白则整串。中文值天然无空格，兼容。"""
    s = s.strip()
    if not s:
        return ""
    if " " in s or "\t" in s:
        s = re.split(r"\s+", s, 1)[0]
    return _strip_paren(s).strip()


def _split_slash(s):
    """`器物 / 动物 / 植物` → ['器物','动物','植物']。中文值里不含空格，靠斜杠分隔。"""
    if "/" in s:
        return [x.strip() for x in s.split("/")]
    return [s.strip()]


def _clean_value(s):
    """洗掉 markdown 与括号残留：`**异闻**` → 异闻；`仙道交游）` → 仙道交游。"""
    s = str(s).strip()
    s = s.replace("**", "").replace("`", "").strip("* ")
    # 只有右括号没有左括号 → 是被切开的残留，剥掉
    if s and s[-1] in "）)" and "（" not in s and "(" not in s:
        s = s[:-1]
    return _strip_paren(s).strip()


_BAD_CHARS = "；;，,、：:。.！!？?（）()[]【】"


def _is_valid_value(v):
    """排除说明性文字与切分残渣。真值都是短名词，不含标点。"""
    if not v or v in _TABLE_SKIP:
        return False
    if set(v) <= set("-: |*/"):
        return False
    if len(v) > 12:
        return False
    if any(c in v for c in _BAD_CHARS):
        return False
    if v in ("和", "或", "与", "等", "含", "注"):
        return False
    return True


# ---------------------------------------------------------------- 工厂库（Markdown）

_SECTION_RE = re.compile(r"^###\s+(1\.\d+)\s+(.+?)\s*$")
_VAR_RE = re.compile(r"\b([A-Z][A-Z0-9_]{2,})\b")
_DECLARED_RE = re.compile(r"[（(](\d+)\s*(?:值|顶层|个)")
_TABLE_SKIP = {"规范值", "父类型", "子类型", "顶层", "判定", "来源", "说明",
               "别名", "类型", "值", "字段名", "客座原值", "合并后"}
# 归并映射表的表头特征词：命中即整表跳过（详见 parse_factory_library 注释）
_MAPPING_TABLE_HEAD = ("原值", "合并", "归并", "判定", "旧值")
# 子类型表：首列就是子类型（父类型在第二列）
_SUBTYPE_HEAD = {"子类型", "子类", "子值", "下层"}
# 代码块里的「字段定义行」前缀，不是枚举值
_FIELD_DEF_PREFIX = ("方向", "使用说明", "说明：", "说明", "来源", "注：", "注",
                     "判据", "取值", "字段")


def parse_factory_library(path=None):
    """解析 enum-library.md：表格首列 + 代码块行，两者并集。

    表格与代码块都收，是因为 v4 重构后各段写法不一（1.3 顶层在表、子类型在代码块；
    1.6 树状在代码块）。宁可并集后由 checklist 提示「解析数与声明数不符」，
    也不 silently 漏掉一半值。
    """
    path = path or R.FACTORY_ENUM_LIB
    if not os.path.exists(path):
        return {}, {"error": "工厂枚举库不存在: %s" % path}

    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()

    # 先切段
    sections = []
    cur = None
    in_block = False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_block = not in_block
            if cur is not None:
                cur["block"].append(ln) if in_block else None
            continue
        m = _SECTION_RE.match(ln)
        if m and not in_block:
            cur = {"section": m.group(1), "title": m.group(2),
                   "lines": [], "block": []}
            sections.append(cur)
            continue
        if cur is not None:
            if in_block:
                cur["block"].append(ln)
            else:
                cur["lines"].append(ln)

    out = {}
    for sec in sections:
        title = sec["title"]
        vars_found = [v for v in _VAR_RE.findall(title)
                      if not v.endswith(("TYPES", "TYPES")) or True]
        # 标题里的大写 token，排除纯中文标题里误命中
        vars_found = list(dict.fromkeys(_VAR_RE.findall(title)))
        if not vars_found:
            continue
        main_var = vars_found[0]

        dm = _DECLARED_RE.search(title)
        declared = int(dm.group(1)) if dm else None

        values, aliases = [], {}
        seen = set()

        def add(value, doc, depth, src):
            # 依次做三件事：按斜杠拆 → 取空格前的首词（值后面常跟中文说明）
            # → 洗净 markdown 与括号残留
            # 少了「取首词」这步，`person 人物` 会整串变成值，定义集全脏
            for piece in _split_slash(value):
                v = _clean_value(_first_token(piece))
                if not v or v in seen or not _is_valid_value(v):
                    continue
                seen.add(v)
                values.append({"value": v, "doc": doc.strip(),
                               "depth": depth, "src": src})

        # 代码块行。一个段里可能同时存在两种写法，必须分路：
        #   A. `禁止型(prohibit) / 义务型(obligation)`  —— 括号紧跟值，先拆 / 再剥括号
        #   B. `民俗（别名：习俗 / 地方风俗 / 礼俗）`   —— 括号里含 /，先切括号再取别名
        # 顺序搞反都会坏事：A 会被切成未闭合的 `禁止型(prohibit` 而整条丢弃；
        # B 会把别名当值收进定义集。
        merged = []
        for raw in sec["block"]:
            s = raw.rstrip()
            if not s.strip() or s.strip().startswith("```"):
                continue
            if s.strip().startswith("#"):
                continue
            # 续行：行首是 `/` 说明是上一行的延续（1.2 段就是这么断行的）
            if s.strip().startswith("/") and merged:
                merged[-1] = merged[-1].rstrip() + " " + s.strip()
            else:
                merged.append(s)

        for raw in merged:
            indent = len(raw) - len(raw.lstrip(" "))
            depth = 0 if indent == 0 else max(1, indent // 2)
            body = raw.strip().lstrip("-*+").strip()
            if not body:
                continue
            # 字段定义行（`方向 direction：单向 / 双向`）不是枚举值，整行跳过。
            # 用**行首关键词**判定，不用「冒号位置」——值行也可能带冒号
            # （`event 事件名——事件专名实体：靖难、土木之难等`，曾因此误杀）。
            if any(body.startswith(p) for p in _FIELD_DEF_PREFIX):
                continue

            m = re.match(r"^([^（(]*)[（(](.*)$", body)
            # 括号出现在第一个 `/` 之前 且 是别名注记 → 整行模式（B）
            #   例：`民俗（别名：习俗 / 地方风俗 / 礼俗）`，括号里的 / 是别名分隔
            # 否则 → 逐片模式：括号属于某个值自己
            #   例：`同僚 / 师生 / … / 上下级（别名：主从）/ 父子亲属 / …`
            #   早期版本对后者也走整行模式，结果只取到首词「同僚」，REL 13 值丢了 11 个
            whole_line = bool(m and "别名" in body and "/" not in m.group(1))

            def emit(piece, dep, note=""):
                v = _clean_value(_first_token(piece))
                if not v or not _is_valid_value(v):
                    return None
                if v not in seen:
                    seen.add(v)
                    values.append({"value": v, "doc": "", "depth": dep,
                                   "src": "block"})
                am = re.search(r"别名[:：]\s*(.+)", note)
                if am:
                    for a in _split_slash(am.group(1)):
                        a = _clean_value(a)
                        if a and _is_valid_value(a):
                            aliases[a] = v
                return v

            if whole_line:
                emit(m.group(1), depth, note=m.group(2))
                continue

            # 树状行：`器物 ─ 文书 / 文房 / 乐器` —— 破折号左侧顶层，右侧子类
            if "─" in body:
                left, right = body.split("─", 1)
                for piece in _split_slash(left):
                    emit(piece, depth or 0)
                for piece in _split_slash(right):
                    emit(piece, (depth or 0) + 1)
                continue

            for piece in _split_slash(body):
                pm = re.match(r"^([^（(]*)(.*)$", piece)
                emit(pm.group(1) if pm else piece, depth,
                     note=(pm.group(2) if pm else ""))

        # 表格：一段里可能串着多个表（顶层表 / 子类型表 / 归并映射表），
        # 必须认出**每个表自己的表头**——表头的下一行是 |---| 分隔行。
        # 只在首表认一次表头的话，后面几个表的数据行会被当成前一个表的续行收进来
        # （曾把归并映射表的 28 个旧值收进 EVENT 定义集）。
        tbl = []
        for raw in sec["lines"]:
            s = raw.strip()
            if s.startswith("|"):
                tbl.append([c.strip() for c in s.strip("|").split("|")])
        is_sep = [bool(cells) and set("".join(cells)) <= set("-: ") for cells in tbl]
        is_head = [False] * len(tbl)
        for i, sep in enumerate(is_sep):
            if sep and i > 0:
                is_head[i - 1] = True

        header, skip = None, False
        for i, cells in enumerate(tbl):
            if is_sep[i]:
                continue
            if is_head[i]:
                header = [_clean_value(c) for c in cells]
                # 归并映射表（`| 客座原值 | 归并到 |`）不是规范值定义，整表跳过
                skip = any(k in h for h in header for k in _MAPPING_TABLE_HEAD)
                continue
            if header is None or skip or not cells:
                continue
            subtype_table = bool(header) and header[0] in _SUBTYPE_HEAD
            doc = cells[1] if len(cells) > 1 else ""
            canon_v = _clean_value(cells[0])
            add(cells[0], doc, 1 if subtype_table else 0, "table")
            # 顶层表的「别名（各书旧值）」列 → 抽别名，drift 判定时按别名命中
            alias_col = next((j for j, h in enumerate(header) if "别名" in h), None)
            if alias_col is not None and not subtype_table and len(cells) > alias_col:
                for piece in _split_slash(cells[alias_col]):
                    a = _clean_value(piece)
                    if a and _is_valid_value(a):
                        aliases[a] = canon_v

        key = R.canon_key(main_var)
        top_n = sum(1 for v in values if v.get("depth", 0) == 0)
        out[key] = {
            "name": re.split(r"[（(]", title)[0].strip(),
            "section": sec["section"],
            "var": main_var,
            "declared": declared,
            "top_count": top_n,
            "values": values,
            "aliases": aliases,
            "source": path,
            "merged_vars": vars_found[1:] or [],
        }
    return out, {}


# ---------------------------------------------------------------- 实例（Python）

def _static_module_vars(path):
    """ast 静态解析模块级赋值，只保留能 literal_eval 的。零副作用。"""
    try:
        tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    except Exception:
        return {}
    out = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        if node.value is None:
            continue
        try:
            val = ast.literal_eval(node.value)
        except Exception:
            continue
        for t in targets:
            if isinstance(t, ast.Name):
                out[t.id] = val
    return out


def _import_module(path, mod_name="_kb_enum_probe"):
    """兜底：真的执行模块（仅对静态解析拿不到的动态构造，如五杂俎 BASE_ENUMS）。

    风险已被限定：只在目标变量静态缺失时调用，且整段包在 try 里。
    """
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception:
        return None
    return mod


def _collect_from_spec(spec):
    """从 spec 字典里收集规范值、别名与分组。

    两种真实形态（都见过，别再靠猜）：

      A. 五杂俎   {version, tree:{中文值:[英文canonical, 别名…]}, canonical:[英文…],
                   alias:{别名: canonical}}
         → **规范值取 canonical（英文）**，因为层产物实际标注用的是英文
           （ent_01.json 里 type=place/person/object…）。中文 tree 键只是分组，
           若也当值会与英文双算，drift 定义数直接翻倍。
      B. 先进遗风 {values: set, aliases: dict, doc: str}
         → 规范值取 values。

    兜底：两者都没有时，退回 tree 的键（递归，带层级）。
    """
    values, aliases, groups = [], {}, []
    seen = set()

    def add(v, doc="", depth=0):
        v = str(v).strip()
        if not v or v in seen:
            return
        seen.add(v)
        values.append({"value": v, "doc": doc, "depth": depth, "src": "runtime"})

    # ① 规范值：canonical / values 优先
    for key in ("canonical", "canonicals", "values", "items", "value"):
        v = spec.get(key)
        if isinstance(v, (list, tuple, set)):
            for x in sorted(v, key=str):
                if isinstance(x, str):
                    add(x)
            break
        if isinstance(v, dict):
            for x in v:
                add(str(x).strip())
            break

    # ② 别名映射
    for key in ("alias", "aliases", "alias_map", "synonyms"):
        v = spec.get(key)
        if isinstance(v, dict):
            for a, canon in v.items():
                aliases[str(a).strip()] = str(canon).strip()

    # ③ tree：有 canonical 时只作分组，无 canonical 时退为值
    tree = spec.get("tree")
    if isinstance(tree, dict):
        if values:
            for k in tree:
                groups.append(str(k).strip())
        else:
            def walk_t(node, depth):
                for k, v in node.items():
                    ks = str(k).strip()
                    add(ks, depth=depth)
                    if isinstance(v, dict):
                        walk_t(v, depth + 1)
                    elif isinstance(v, (list, tuple, set)):
                        for x in v:
                            if isinstance(x, str) and x != ks:
                                aliases[x] = ks
            walk_t(tree, 0)

    return values, aliases, groups


def load_instance_enums(book):
    """读某本书的枚举定义。返回 (dict, meta)。"""
    cfg = R.BOOKS[book]
    backend = cfg["enum_backend"]
    meta = {"backend": backend, "book": book}
    if backend == "none" or not cfg.get("enum_path"):
        meta["note"] = "无单点枚举文件（值内嵌在打包器里），drift 只能报「无基准」"
        return {}, meta

    path = os.path.join(R.book_dir(book), cfg["enum_path"])
    if not os.path.exists(path):
        meta["error"] = "枚举文件不存在: %s" % path
        return {}, meta

    meta["path"] = os.path.relpath(path, R.REPO_ROOT)
    static = _static_module_vars(path)
    out = {}

    if backend == "spec":
        var = cfg.get("enum_var") or "ENUM_REGISTRY"
        spec = static.get(var)
        src = "static"
        if spec is None:
            mod = _import_module(path, "_kb_enum_%s" % re.sub(r"\W", "", book))
            if mod is not None:
                spec = getattr(mod, var, None)
                src = "import"
        if spec is None:
            meta["error"] = "未找到注册表变量 %s" % var
            return {}, meta
        meta["loaded_via"] = src
        if isinstance(spec, dict) and all(
                isinstance(v, dict) and (
                    "tree" in v or "canonical" in v or "alias" in v or "values" in v)
                for v in spec.values() if v):
            for name, one in spec.items():
                vals, als, grp = _collect_from_spec(one)
                out[R.canon_key(name)] = {
                    "name": "", "section": None, "var": "%s[%s]" % (var, name),
                    "declared": len(vals) or None,
                    "values": vals, "aliases": als, "groups": grp,
                    "source": meta["path"], "merged_vars": [],
                }
        else:
            vals, als, grp = _collect_from_spec(spec)
            out[R.canon_key(var)] = {
                "name": "", "section": None, "var": var,
                "declared": len(vals) or None,
                "values": vals, "aliases": als, "groups": grp,
                "source": meta["path"], "merged_vars": [],
            }
        return out, meta

    # flat：抓所有 *_TYPES / *_STYLES 等大写常量
    names = cfg.get("enum_names")
    if not names:
        names = [n for n in static
                 if n.isupper()
                 and n.endswith(R.ENUM_VAR_PATTERNS)
                 and not n.endswith(R.NON_ENUM_VAR_SUFFIX)]
    for n in names:
        val = static.get(n)
        if val is None:
            continue
        vals, als = [], {}
        if isinstance(val, dict):
            for k, v in val.items():
                doc = v if isinstance(v, str) else ""
                vals.append({"value": str(k), "doc": doc, "depth": 0, "src": "static"})
        elif isinstance(val, (list, tuple, set)):
            for x in val:
                if isinstance(x, str):
                    vals.append({"value": x, "doc": "", "depth": 0, "src": "static"})
        if vals:
            out[R.canon_key(n)] = {
                "name": "", "section": None, "var": n,
                "declared": len(vals), "values": vals, "aliases": als,
                "source": meta["path"], "merged_vars": [],
            }
    return out, meta


# ------------------------------------------------------- 实例 schemas.md 快照

def parse_schemas_snapshot(book):
    """第三处（schemas.md）不做结构解析，只做**文本命中**检查。

    理由：各书 schemas.md 排版差异极大（表格/代码块/行内枚举混排），结构解析误报率
    高于收益。改为检查「工厂库的每个值是否作为独立 token 出现在 schemas 里」——
    足以发现"实例快照没跟上工厂库"这件事，且不产生假的结构性结论。
    """
    cfg = R.BOOKS[book]
    rel = cfg.get("schemas")
    if not rel:
        return None, {"note": "未登记 schemas.md 路径"}
    path = os.path.join(R.REPO_ROOT, rel)
    if not os.path.exists(path):
        return None, {"note": "schemas.md 不存在: %s" % rel}
    text = open(path, encoding="utf-8").read()
    return {"path": rel, "text": text}, {}


def value_hits(text, value):
    """值是否作为大致独立的 token 出现在文本中。"""
    if not text:
        return False
    if value in text:
        return True
    return False


# ---------------------------------------------------------------- 层产物扫描

# 类型字段候选，按优先级取记录里**第一个存在**的。
# 之所以列这么长：新官轨范各层字段名不统一（流程层 event_type、结构层 role_type /
# mechanism_type / doc_type），只认 `type` 会漏掉整层。
_TYPE_FIELDS = ("type", "event_type", "category", "role_type", "mechanism_type",
                "doc_type", "subtype", "sub_type", "kind", "class")
_SKIP_FILE_TOKENS = ("join", "index", "keys", "inventory", "alias_index",
                     "report", "summary")
# 顶层里是 list[dict] 但不是「记录」的键（日志/错误清单之类），扫描时排除
_NON_RECORD_KEYS = {"errors", "warnings", "notes", "logs", "issues",
                    "changelog", "history"}


def _layer_name_from_file(fp, dir_layer_map):
    base = os.path.basename(fp)
    stem = base[:-5] if base.endswith(".json") else base
    parent = os.path.basename(os.path.dirname(fp))
    if parent in dir_layer_map:
        return dir_layer_map[parent]
    # ent_01 / appt_00 / _kg_01 → 去掉尾部编号
    m = re.match(r"^(.*?)[_-]?\d{1,4}$", stem)
    name = m.group(1) if m else stem
    name = name.strip("_")
    return name or stem


def scan_layers(book, only_layer=None):
    """扫层产物，统计各层每个候选类型字段的取值分布。

    返回 {layer: {"field": str, "total": int, "counts": {值: 次数}, "files": int}}
    """
    cfg = R.BOOKS[book]
    spec = cfg["layers"]
    root = R.book_dir(book)
    dir_layer_map = spec.get("dir_layer_map", {})
    acc = {}

    for pattern in spec["globs"]:
        for fp in sorted(_glob.glob(os.path.join(root, pattern))):
            low = os.path.basename(fp).lower()
            if any(t in low for t in _SKIP_FILE_TOKENS):
                continue
            try:
                data = json.load(open(fp, encoding="utf-8"))
            except Exception:
                continue
            if not isinstance(data, dict):
                continue

            if spec.get("nested") == "dict_of_layers":
                container = None
                for k in spec["container"]:
                    if isinstance(data.get(k), dict):
                        container = data[k]
                        break
                if container is None:
                    continue
                for layer, recs in container.items():
                    if only_layer and layer != only_layer:
                        continue
                    _accumulate(acc, layer, recs, fp, key=layer)
            else:
                layer = _layer_name_from_file(fp, dir_layer_map)
                if only_layer and layer != only_layer:
                    continue
                # 遍历**所有**候选容器，而不是取第一个匹配：
                # 新官结构层一个文件里有 ledgers/times/docs/actors/frauds 多个容器，
                # 只取第一个（ledgers 恰好无类型字段）会整层漏扫。
                hit = False
                for k, v in data.items():
                    if k in _NON_RECORD_KEYS:
                        continue
                    if isinstance(v, list) and v and isinstance(v[0], dict):
                        if _accumulate(acc, layer, v, fp, key=k):
                            hit = True
                if not hit:
                    continue

    # 折叠：每层取记录数最多的字段为主字段，其余只在 other_fields 里报个数
    out = {}
    for layer, slot in acc.items():
        by_field = slot["by_field"]
        if not by_field:
            continue
        main = max(by_field.items(), key=lambda kv: kv[1]["total"])
        others = {f: len(b["counts"]) for f, b in by_field.items() if f != main[0]}
        out[layer] = {
            "field": main[0],
            "total": main[1]["total"],
            "counts": main[1]["counts"],
            "files": len(slot["files"]),
            "containers": sorted(slot["containers"]),
            "other_fields": others,
        }
    return out


def _accumulate(acc, layer, recs, fp, key=None):
    """把一个容器里的记录累加到该层。返回是否真的采到了类型字段。"""
    if not isinstance(recs, list) or not recs:
        return False
    sample = recs[0]
    field = None
    for f in _TYPE_FIELDS:
        if f in sample:
            field = f
            break
    if field is None:
        return False
    # 按 field 分桶：一个层若同时有 role_type / mechanism_type 等多个类型字段，
    # 混在一个 Counter 里会让 drift 比值失真。取记录数最多的字段为主字段。
    slot = acc.setdefault(layer, {"by_field": {}, "files": set(),
                                  "sample_file": fp, "containers": set()})
    slot["files"].add(fp)
    if key:
        slot["containers"].add(key)
    bucket = slot["by_field"].setdefault(field, {"total": 0, "counts": {}})
    for r in recs:
        if not isinstance(r, dict):
            continue
        v = r.get(field)
        if v is None or not isinstance(v, str):
            continue
        bucket["total"] += 1
        bucket["counts"][v] = bucket["counts"].get(v, 0) + 1
    return True


def load_ent_keys(book):
    """读实体主键表（P0 只读，供 checklist 报未决数）。找不到返回 None。"""
    root = R.book_dir(book)
    cands = [
        os.path.join(root, "data", "ent", "ent_keys.json"),
        os.path.join(root, "_layers", "ent_keys.json"),
        os.path.join(root, "data", "_layers", "ent_keys.json"),
        os.path.join(root, "ent_keys.json"),
    ]
    for p in cands:
        if os.path.exists(p):
            try:
                return json.load(open(p, encoding="utf-8")), p
            except Exception:
                return None, p
    return None, None
