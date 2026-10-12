"""name_resolver.py —— F3 名字解析（两级接入 + 配置驱动归一化）

职责（对应 ELT设计 §3 / 用户细化要求）：
- 两级接入：
    * 标准接入：若某书在 name_rules.json 的 ent_keys_paths 里登记了标准
      ent_keys.json 且结构标准，则读其 alias 列表（最高价值，method=alias）。
    * 特殊接入：否则（或标准源无 alias 数据）从 records 的 ent 负载抽取
      normalized + text 作为 surface（所有书都有，兜底）。
  两路都归一到同一套 (uid, normalized, type, surfaces) 结构。
- 配置驱动归一化：装饰词（尊称后缀 / 官称前缀 / 地名后缀 / 谥号标记…）
  全部在 name_rules.json 里，匹配逻辑只泛化处理这份配置——
  新增一种称呼/变体，只改配置、不动代码。
- 解析：resolve_in_book（T1 名字→uid，带置信度）；
  cross_candidates（T2 跨书候选生成，带置信度）。

不依赖任何第三方库；只读联邦库与（可选的）源工程目录。
"""

import json
import os
import sqlite3
from collections import defaultdict

RULES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "name_rules.json")


# ---------------------------------------------------------------------------
# 规则加载
# ---------------------------------------------------------------------------
def load_rules():
    with open(RULES_PATH, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# 配置驱动归一化：泛化剥离装饰词，得 base 形式
# ---------------------------------------------------------------------------
def normalize(raw, rules=None):
    """把任意称呼形式归一到 base 形式。

    逻辑只认配置，不认具体变体类型——按 `strip_order` 依次处理各装饰组：
      wrapping_marks    包裹标记（书名号《》/引号『』）—— 成对剥除
      title_prefix      官称前缀（太师/尚书/…）—— 从头删
      posthumous_marker 谥号标记（谥/追赠）—— 全文删
      honorific_suffix  尊称后缀（公/先生/山人/…）—— 从尾删
      place_suffix      地名后缀 —— 从尾删
      work_tail_suffix  尾缀（注本标识：正义/集说/注疏）—— 从尾删
    新增一种称呼只往配置加 token，不动本函数。
    """
    if rules is None:
        rules = load_rules()
    if not raw:
        return raw
    s = raw.strip()
    groups = rules.get("decoration_groups", {})
    order = rules.get("strip_order") or [
        "title_prefix", "posthumous_marker", "honorific_suffix", "place_suffix"]

    # 逐组按配置顺序处理；未在 strip_order 列出的组不生效
    for g in order:
        if g == "wrapping_marks":
            # 成对标记（《…〉）：按配置的「起始符→终止符」配对反复剥除。
            # 单侧符号（singles）直接删。
            spec = groups.get("wrapping_marks", {})
            pairs = spec.get("pairs", []) if isinstance(spec, dict) else spec
            singles = spec.get("singles", []) if isinstance(spec, dict) else []
            changed = True
            while changed and s:
                changed = False
                for pair in pairs:
                    if not (isinstance(pair, (list, tuple)) and len(pair) == 2):
                        continue
                    open_m, close_m = pair
                    # 起止符相同时按单侧处理
                    if open_m == close_m:
                        if s.startswith(open_m) or s.endswith(close_m):
                            s = s.replace(open_m, "", 1)
                            changed = True
                            break
                    elif (len(s) > len(open_m) + len(close_m)
                          and s.startswith(open_m) and s.endswith(close_m)):
                        s = s[len(open_m):-len(close_m)].strip()
                        changed = True
                        break
                if changed:
                    continue
                for m in singles:
                    if m and m in s:
                        s = s.replace(m, "")
                        changed = True
                        break
        elif g == "posthumous_marker":
            for m in groups.get("posthumous_marker", []):
                if m:
                    s = s.replace(m, "")
        elif g == "title_prefix":
            # 从头删（长优先）
            for t in sorted(groups.get("title_prefix", []), key=len, reverse=True):
                if t and s.startswith(t):
                    s = s[len(t):]
        elif g in ("honorific_suffix", "place_suffix", "work_tail_suffix"):
            # 从尾删；work_tail_suffix 同样带「剩余≥2字」保护。
            # 注意分组值可能是 list 或 {_comment, tokens:[...]} 两种形态，统一取 token 列表。
            spec = groups.get(g, [])
            if isinstance(spec, dict):
                spec = spec.get("tokens", [])
            for t in sorted(spec, key=len, reverse=True):
                if not t:
                    continue
                if s.endswith(t):
                    remaining = len(s) - len(t)
                    if len(t) == 1 and remaining < 2:
                        continue
                    if remaining >= 1:
                        s = s[:remaining]

    return s.strip() or raw.strip()


# ---------------------------------------------------------------------------
# 两级接入：收集每书每个 ent 的 surface 集合
# ---------------------------------------------------------------------------
def _ent_primary_name(payload):
    for k in ("normalized", "norm", "text", "name", "label"):
        v = payload.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return None


def _collect_from_records(con, book_id, rules):
    """特殊接入：从 records(layer_key='ent') 抽取。所有书都支持。"""
    cur = con.cursor()
    icur = con.cursor()
    out = []  # (uid, normalized, type, surfaces:set, aliases:set)
    rows = icur.execute(
        "SELECT local_id, payload FROM records WHERE book_id=? AND layer_key='ent'",
        (book_id,),
    )
    for local_id, pl in rows:
        try:
            d = json.loads(pl)
        except (ValueError, TypeError):
            continue
        uid = f"{book_id}:{local_id}"
        normalized = _ent_primary_name(d)
        if not normalized:
            continue
        typ = d.get("type") or "unknown"
        surfaces = {normalized}
        for k in ("norm", "text", "name", "label"):
            v = d.get(k)
            if isinstance(v, str) and v.strip():
                surfaces.add(v.strip())
        # 派生 base 形式（剥离装饰词后的形态，作为候选匹配键）
        for s in list(surfaces):
            b = normalize(s, rules)
            if b and b != s:
                surfaces.add(b)
        out.append((uid, normalized, typ, surfaces, set()))
    return out


def _collect_from_ent_keys(con, book_id, rules):
    """标准接入：读 name_rules 登记的 ent_keys.json（若有且结构标准）。

    返回 (entities, source) —— entities 为 (uid, normalized, type, surfaces, aliases)。
    若路径未登记 / 文件缺失 / 无 alias 数据，返回空列表（交给特殊接入）。
    """
    paths = rules.get("ent_keys_paths", {})
    schema_map = rules.get("ent_keys_schema", {})
    rel = paths.get(book_id)
    if not rel:
        return []
    cur = con.cursor()
    row = cur.execute(
        "SELECT source_root FROM books WHERE book_id=?", (book_id,)
    ).fetchone()
    if not row or not row[0]:
        return []
    abspath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", row[0], rel)
    abspath = os.path.normpath(abspath)
    if not os.path.exists(abspath):
        return []
    try:
        with open(abspath, encoding="utf-8") as f:
            data = json.load(f)
    except (ValueError, OSError):
        return []

    sch = schema_map.get(book_id, {})
    ent_key = sch.get("entities")
    norm_key = sch.get("normalized", "normalized")
    alias_key = sch.get("aliases")  # 可能为 None（该书未在 ent_keys 存 alias）
    if not ent_key or ent_key not in data:
        return []

    out = []
    for e in data.get(ent_key, []):
        normalized = e.get(norm_key)
        if not isinstance(normalized, str) or not normalized.strip():
            continue
        typ = e.get(sch.get("type", "type")) or "unknown"
        surfaces = {normalized}
        aliases = set()
        if alias_key and isinstance(e.get(alias_key), list):
            for a in e[alias_key]:
                if isinstance(a, str) and a.strip():
                    aliases.add(a.strip())
                    surfaces.add(a.strip())
        for s in list(surfaces):
            b = normalize(s, rules)
            if b and b != s:
                surfaces.add(b)
        # uid 暂时用 normalized 占位；真正 uid 由 records 接入补齐，
        # 这里仅作为「标准源是否提供 alias」的探针——若 alias 为空则视为无价值。
        out.append((None, normalized, typ, surfaces, aliases))
    return out


def collect_surfaces(con, book_id, rules=None):
    """两级合并：标准源若有真实 alias 数据则采用；否则纯 records 接入。

    返回 list[(uid, normalized, type, surfaces:set, aliases:set)]。
    surfaces 含 primary + text + 派生 base；aliases 仅为标准源显式列出的变体。
    """
    if rules is None:
        rules = load_rules()
    # 先拿 records 接入（保证每个 ent 都有真实 uid）
    recs = _collect_from_records(con, book_id, rules)
    rec_by_norm = defaultdict(list)
    for uid, norm, typ, surfs, _ in recs:
        rec_by_norm[(norm, typ)].append((uid, surfs))

    # 标准源：若提供 alias，回填到对应 (normalized,type) 的 records 条目
    std = _collect_from_ent_keys(con, book_id, rules)
    for _uid, norm, typ, surfs, aliases in std:
        if aliases:
            for uid, surfs2 in rec_by_norm.get((norm, typ), []):
                surfs2 |= surfs
                surfs2 |= aliases
    return recs


# ---------------------------------------------------------------------------
# 索引与解析
# ---------------------------------------------------------------------------
def build_global_index(con, rules=None):
    """构建 type → surface_base → list[(uid, kind)] 的全局索引。

    uid 自带 book 前缀（book:local_id），所以同一 type 下的 base 可直接跨书比对。
    kind ∈ {'normalized', 'surface'}：
      - normalized：该 surface 是 ent 的 canonical 名（s == 该 ent 的 normalized）
      - surface   ：canonical 之外的其它出现形式（text / alias / 派生 base）
    跨书候选据此生成（见 cross_candidates）。
    """
    if rules is None:
        rules = load_rules()
    index = defaultdict(lambda: defaultdict(list))  # type -> base -> [(uid,kind)]
    for book_id in _book_ids(con):
        norm_of = {}
        for uid, norm, typ, surfs, _aliases in collect_surfaces(con, book_id, rules):
            norm_of[uid] = norm
            for s in surfs:
                base = normalize(s, rules)
                kind = "normalized" if s == norm else "surface"
                index[typ][base].append((uid, kind))
    return index


def resolve_in_book(con, book_id, raw, rules=None):
    """T1：把一段原始名字解析成本书 ent uid（带方法+置信度）。

    返回 list[(uid, method, confidence)]，按置信降序；空列表表示悬空（进 pending）。
    """
    if rules is None:
        rules = load_rules()
    conf_map = rules.get("match_confidence", {})
    n_raw = normalize(raw, rules)
    hits = []
    seen = set()
    for uid, norm, typ, surfs, _a in collect_surfaces(con, book_id, rules):
        if raw == norm:
            m, c = "exact_normalized", 1.0
        elif raw in surfs:
            m, c = "surface_alias", conf_map.get("surface_alias", 0.90)
        elif n_raw and n_raw == normalize(norm, rules) and n_raw != norm:
            m, c = "normalized_stripped", conf_map.get("normalized_stripped", 0.65)
        elif n_raw and any(n_raw == normalize(s, rules) for s in surfs):
            m, c = "normalized_stripped", conf_map.get("normalized_stripped", 0.65)
        else:
            continue
        if uid in seen:
            continue
        seen.add(uid)
        hits.append((uid, m, c))
    hits.sort(key=lambda x: x[2], reverse=True)
    return hits


def cross_candidates(con, rules=None):
    """T2：跨书候选对生成（同 type、不同书、共享 surface_base）。

    返回 list[(a_uid, b_uid, method, confidence)]。方法取两 uid 在共享键上的
    最优 kind：normalized×normalized → exact_normalized；否则 surface_alias；
    否则 normalized_stripped。
    """
    if rules is None:
        rules = load_rules()
    conf_map = rules.get("match_confidence", {})
    index = build_global_index(con, rules)
    candidates = []
    for typ, keymap in index.items():
        for base, members in keymap.items():
            # 按 book 分组（uid 自带 book 前缀）
            by_book = defaultdict(list)
            for uid, kind in members:
                by_book[uid.split(":", 1)[0]].append((uid, kind))
            books_here = list(by_book.keys())
            if len(books_here) < 2:
                continue
            for i in range(len(books_here)):
                for j in range(i + 1, len(books_here)):
                    ba, bb = books_here[i], books_here[j]
                    for ua, ka in by_book[ba]:
                        for ub, kb in by_book[bb]:
                            # 方法 = 两端 kind 的最优
                            if ka == "normalized" and kb == "normalized":
                                m = "exact_normalized"
                                c = conf_map.get("exact_normalized", 0.98)
                            elif "normalized" in (ka, kb):
                                m = "surface_alias"
                                c = conf_map.get("surface_alias", 0.90)
                            else:
                                m = "normalized_stripped"
                                c = conf_map.get("normalized_stripped", 0.65)
                            candidates.append((ua, ub, m, c))
    return candidates


# ---------------------------------------------------------------------------
# 辅助
# ---------------------------------------------------------------------------
def _book_ids(con):
    return [r[0] for r in con.execute("SELECT book_id FROM books ORDER BY book_id")]


def capped_confidence(rules, typ, method, conf):
    """按实体类型对置信度封顶（同名异人 / 泛称角色保护）。"""
    cap = (rules.get("type_confidence_cap", {}) or {}).get(typ)
    if cap is not None and conf > cap:
        return float(cap)
    return conf


class BookNameIndex:
    """单书名字索引（transform 批量解析用，避免逐条全表扫）。

    norm_map : normalized → [(uid, type)]
    surf_map : 任意 surface（含派生 base）→ [(uid, type)]
    """

    def __init__(self, con, book_id, rules=None):
        if rules is None:
            rules = load_rules()
        self.rules = rules
        self.book_id = book_id
        self.norm_map = defaultdict(list)
        self.surf_map = defaultdict(list)
        self.norm_of = {}
        self.type_of = {}
        for uid, norm, typ, surfs, _a in collect_surfaces(con, book_id, rules):
            self.norm_map[norm].append((uid, typ))
            self.surf_map[norm].append((uid, typ))
            self.norm_of[uid] = norm
            self.type_of[uid] = typ
            for s in surfs:
                self.surf_map[s].append((uid, typ))
                b = normalize(s, rules)
                self.surf_map[b].append((uid, typ))

    def resolve(self, raw):
        """解析一个原始名字 → [(uid, method, confidence)]（含类型封顶）。"""
        rules = self.rules
        conf_map = rules.get("match_confidence", {})
        n_raw = normalize(raw, rules)
        hits = {}
        # 1) 精确 canonical
        for uid, typ in self.norm_map.get(raw, []):
            hits[uid] = (uid, "exact_normalized",
                         capped_confidence(rules, typ, "exact_normalized", 1.0))
        # 2) 任意 surface（含 text / alias / base）
        for uid, typ in self.surf_map.get(raw, []):
            if uid not in hits:
                hits[uid] = (uid, "surface_alias",
                             capped_confidence(rules, typ, "surface_alias",
                                                conf_map.get("surface_alias", 0.90)))
        # 3) 归一后 base 相等
        if n_raw != raw:
            for uid, typ in self.surf_map.get(n_raw, []):
                if uid not in hits:
                    hits[uid] = (uid, "normalized_stripped",
                                 capped_confidence(rules, typ, "normalized_stripped",
                                                    conf_map.get("normalized_stripped", 0.65)))
        out = list(hits.values())
        out.sort(key=lambda x: x[2], reverse=True)
        return out


def all_ent_surfaces(con, book_id, rules=None):
    """调试/审计：返回本书 ent 的 (uid, normalized, type, surfaces) 列表。"""
    return [(uid, norm, typ, surfs) for uid, norm, typ, surfs, _a in collect_surfaces(con, book_id, rules)]
