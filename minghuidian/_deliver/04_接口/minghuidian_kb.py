# -*- coding: utf-8 -*-
"""
明会典知识库 · 统一查询接口  (P4-E)
====================================
一部书 = 一个可检索的知识库。《明会典》13,364 条底座 + 30 个专题层 + 三层树，
全部通过本脚本对外提供**只读查询**。

设计原则
--------
1. **一入口**：只暴露 `MingHuidianKB` 一个类；调用方不必知道 30 个 json 的分布。
2. **可溯源**：每条结果都带 `item_id` / `volume` / `source`，可回查原文。
3. **不编造**：查不到就返回空 + 明确说明，不用相近项凑数（`strict` 可关）。
4. **只读**：所有查询不修改任何数据文件。

用法
----
    from minghuidian_kb import MingHuidianKB
    kb = MingHuidianKB()                    # 默认在脚本所在目录找 _layers/

    kb.office("吏部尚书")        # 官职档案：品级/职掌/沿革/下属/出处
    kb.org("户部")               # 衙门档案：品级/编制/沿革/属官/下辖
    kb.geo("苏州府")             # 地理档案：层级/隶属/卫所/驿站/仓场/辖县
    kb.rule("漕运")              # 制度查询：历代事例 + 年代链
    kb.timeline("漕运")          # 制度时间线
    kb.rank("正三品")            # 品级：章服/房舍/伞盖/鞍辔
    kb.njc("户部")               # 两京对照
    kb.xref("户部")              # 互见
    kb.num("苏州府")             # 数字文册
    kb.obj("衮冕")               # 器物
    kb.profile("苏州府")         # 全景档案（一网打尽）
    kb.ask("漕运怎么运")         # 自然语言式分发
    kb.search("一条鞭")          # 全文检索
    kb.children("户部")          # 父子树展开
    kb.path("苏州府")            # 从根到叶的路径
    kb.stats()                   # 库概况
    kb.check()                   # 自检

命令行
------
    python minghuidian_kb.py office 吏部尚书
    python minghuidian_kb.py profile 苏州府
    python minghuidian_kb.py ask "漕运怎么运到北京"
    python minghuidian_kb.py tree 户部 --depth 3
    python minghuidian_kb.py stats
    python minghuidian_kb.py check
"""
from __future__ import annotations

import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.abspath(__file__))


def _discover_layers():
    """自动定位数据目录，使本脚本在项目根或交付包(_deliver/04_接口/)下都能直接用。

    依次尝试：
      1. <脚本目录>/_layers                       项目根布局
      2. <脚本目录>/../02_数据/_layers            交付包布局
      3. <脚本目录>/../_layers
      4. 向上最多 3 层逐级找 _layers / 02_数据/_layers
    找到第一个含 _kg_join.json 的目录即返回。
    """
    cands = [
        os.path.join(ROOT, "_layers"),
        os.path.join(ROOT, "02_数据", "_layers"),
        os.path.join(ROOT, "..", "_layers"),
        os.path.join(ROOT, "..", "02_数据", "_layers"),
    ]
    up = ROOT
    for _ in range(3):
        up = os.path.dirname(up)
        if not up or up == os.path.dirname(up):
            break
        cands.append(os.path.join(up, "_layers"))
        cands.append(os.path.join(up, "02_数据", "_layers"))
        cands.append(os.path.join(up, "_deliver", "02_数据", "_layers"))
    for c in cands:
        c = os.path.abspath(c)
        if os.path.isfile(os.path.join(c, "..", "_kg_join.json")) or \
           os.path.isfile(os.path.join(c, "_kg_join.json")):
            return c
    for c in cands:
        c = os.path.abspath(c)
        if os.path.isdir(c):
            return c
    return os.path.join(ROOT, "_layers")


LAYERS = _discover_layers()

# 全角/异体字 → 规范字（查询侧归一，便于用户随便打）
NORM_MAP = str.maketrans({
    "戸": "户", "戶": "户", "礼": "礼", "豊": "礼", "钦": "钦", "鉄": "铁", "鐡": "铁",
    "蘓": "苏", "甦": "苏", "邉": "边", "辺": "边", "塲": "场", "場": "场", "塡": "填",
    "効": "效", "敎": "教", "舆": "舆", "凢": "凡", "畧": "略", "寳": "宝", "寶": "宝",
    "弩": "弩", "煖": "暖", "煖": "暖", "脉": "脉", "䖍": "虔", "虔": "虔", "塟": "葬",
    "朩": "木", "曽": "曾", "増": "增", "徳": "德", "徴": "征", "征": "征", "収": "收",
    "𨔛": "递", "𣲖": "派", "𠫵": "参", "参": "参", "㕘": "参", "衞": "卫", "衛": "卫",
    "䕶": "护", "護": "护", "縂": "总", "總": "总", "督": "督", "𨽻": "隶", "隷": "隶",
    "𥂁": "盐", "塩": "盐", "鹽": "盐", "廵": "巡", "𨛦": "郡", "縣": "县", "府": "府",
    "鐡": "铁", "𨯳": "铁", "塩": "盐", "粜": "粜", "糴": "籴", "𥸤": "籲",
    "絾": "纻", "苎": "纻", "紵": "纻", "𤣥": "玄", "縀": "缎", "叚": "缎",
    "𧶘": "赍", "𠡠": "敕", "勅": "敕", "𠡠": "敕", "𢡮": "恤", "卹": "恤",
    "眀": "明", "朙": "明", "㑹": "会", "會": "会", "𢑴": "彝", "彝": "彝",
    "嘑": "呼", "㱕": "归", "歸": "归", "𤼵": "发", "發": "发", "𢄂": "历",
    "厯": "历", "暦": "历", "曆": "历", "歴": "历", "𡊮": "袁", "𨜒": "蓟",
    "瓯": "瓯", "甌": "瓯", "闽": "闽", "閩": "闽",
})

STOP_WORDS = {"凡", "例", "按", "今", "其", "及", "凡例", "国朝", "洪武", "永乐"}

# 俗名 → 书中正名（用户口语与典制原文的桥）
COLLOQUIAL = {
    "驿站": "驿传", "驿": "驿传", "邮驿": "驿传", "铺递": "驿传",
    "仓库": "仓储", "粮仓": "仓储", "太仓": "仓储",
    "军屯": "屯田", "屯垦": "屯田",
    "盐运": "盐法", "盐引": "盐法", "盐课": "盐法",
    "税粮": "赋役", "田赋": "赋役", "户口": "赋役",
    "漕粮": "漕运", "运粮": "漕运",
    "科举考试": "科举", "考试": "科举",
    "钱币": "钱法", "纸币": "钱法", "宝钞": "钱法",
    "马匹": "马政", "养马": "马政",
    "边防": "卫所军伍", "军制": "卫所军伍", "卫所": "卫所军伍",
    "刑法": "刑罚", "刑罚": "刑罚", "律例": "刑罚", "诉讼": "刑罚",
    "宗室": "宗藩", "皇室": "宗藩",
    "祭祀典礼": "祭祀", "典礼": "祭祀",
    "选官": "铨选考课", "考核": "铨选考课",
    "外交": "朝贡", "藩国": "朝贡",
    "水利": "水利河防", "河工": "水利河防",
    "朝服": "冠服", "冠服": "冠服", "服制": "冠服",
    "仪仗": "仪仗", "卤簿": "仪仗",
    "品级": "品级", "官阶": "品级",
}


def resolve_theme(term):
    """把用户俗名映射到本书的正名（找不到就原样返回）。"""
    t = norm(term)
    if t in COLLOQUIAL:
        return COLLOQUIAL[t]
    return t


def theme_tokens(question):
    """在整句问题里扫描俗名/正名 token，返回命中的正名列表（长词优先）。"""
    q = norm(question)
    out = []
    for k in sorted(COLLOQUIAL, key=len, reverse=True):
        if len(k) >= 2 and k in q:
            c = COLLOQUIAL[k]
            if c not in out:
                out.append(c)
    return out


def norm(s):
    if not s:
        return ""
    return (s or "").translate(NORM_MAP).strip()


def _key(texts):
    """归一化索引键：去空白、去标点。非字符串元素安全跳过。"""
    parts = []
    for t in texts:
        if isinstance(t, str):
            parts.append(t)
        elif isinstance(t, dict):
            parts.append(str(t.get("name") or t.get("text") or t.get("title") or ""))
        elif t is not None:
            parts.append(str(t))
    return re.sub(r"[\s　·、,。；;：:（）()【】\[\]]", "", norm("".join(parts)))


class MingHuidianKB:
    """《明会典》(正德本) 知识库统一查询接口。"""

    def __init__(self, layers_dir=LAYERS, join_path=None, registry_path=None):
        self.dir = layers_dir
        self.root = os.path.dirname(os.path.abspath(layers_dir))
        self._c = {}

        def L(name):
            if name not in self._c:
                p = os.path.join(self.dir, name + ".json")
                self._c[name] = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
            return self._c[name]

        self._L = L
        self.offices = L("office_profiles")
        self.orgs = L("org_profiles")
        self.geos = L("geo")
        self.rules = L("rules")
        self.rank_seq = L("rank_sequence")
        self.ranks = L("rank")
        self.njcs = L("njc")
        self.xrefs = L("xref")
        self.nums = L("num")
        self.objs = L("objs")
        self.cits = L("cits")
        self.reports = L("reports")
        self.tims = L("tim")
        self.engs = L("eng_tags")
        self.laws = L("laws")
        self.ents = L("ents")
        self.nams = L("nams")
        self.rituals = L("rituals")
        self.dress = L("dress")
        self.inspect = L("inspect")
        self.foreign = L("foreign")
        self.materials = L("materials")
        self.office_tree = L("office_tree")
        self.org_tree = L("org_tree")
        self.vocab = L("vocab")

        jp = join_path or os.path.join(self.root, "_kg_join.json")
        self.join = {}
        if os.path.exists(jp):
            for r in json.load(open(jp, encoding="utf-8")):
                self.join[r["item_id"]] = r
        rp = registry_path or os.path.join(self.root, "_item_registry.json")
        self.registry = json.load(open(rp, encoding="utf-8")) if os.path.exists(rp) else {}

        self._idx()

    # ---------------- 索引 ----------------
    def _idx(self):
        self.i_off = {}
        for o in self.offices:
            for k in {_key([o.get("office_name", "")])}:
                self.i_off.setdefault(k, []).append(o)
        self.i_org = {}
        for o in self.orgs:
            self.i_org.setdefault(_key([o.get("org_name", "")]), []).append(o)
        self.i_geo = {}
        for g in self.geos:
            self.i_geo.setdefault(_key([g.get("name", "")]), []).append(g)
        # 兼容变体：去掉尾部行政通名
        for src, dst in ((self.i_geo, "geo"),):
            for k in list(src):
                base = re.sub(r"(府|州|县|卫|所|司|布政使司|都司|宣慰司)$", "", k)
                if base and base != k:
                    src.setdefault(base, [])
                    for v in src[k]:
                        if v not in src[base]:
                            src[base].append(v)
        self.i_rank = {}
        for r in self.ranks:
            self.i_rank.setdefault(_key([r.get("level", "")]), []).append(r)
        for r in self.rank_seq:
            self.i_rank.setdefault(_key([r.get("level", "")]), [])
        # 制度/职掌反查：官职 → 出现的 rule
        self.i_rule_off = {}
        for r in self.rules:
            for m in (r.get("subject") or ""):
                pass
        # 父子映射（join 层）
        self.children_of = {}
        for iid, j in self.join.items():
            for c in (j.get("children") or []):
                self.children_of.setdefault(iid, []).append(c)
        # 索引：制度主题 + section 名（用于实体抽取与 ask 分发）
        self.i_theme = {}
        for t in self.tims:
            self.i_theme.setdefault(norm(t.get("theme", "")), []).append(t)
            for w in (t.get("keywords") or []):
                self.i_theme.setdefault(norm(w), []).append(t)
        self.sections = {}
        for it in self.registry.values():
            s = it.get("section") or ""
            if len(s) >= 2:
                self.sections.setdefault(s, []).append(it.get("item_id"))
        # 文本检索缓存
        self._blobs = {}
        for iid, it in self.registry.items():
            self._blobs[iid] = norm((it.get("title") or "") + (it.get("original") or ""))

    # ---------------- 通用 ----------------
    def _item(self, iid):
        it = dict(self.registry.get(iid) or {})
        if not it:
            return None
        it["layer_count"] = (self.join.get(iid) or {}).get("layer_count", 0)
        return it

    def _src(self, iid, limit=220):
        it = self.registry.get(iid) or {}
        return {
            "item_id": iid,
            "volume": it.get("volume"),
            "node_kind": it.get("node_kind"),
            "section": it.get("section"),
            "excerpt": (it.get("original") or it.get("title") or "")[:limit],
        }

    @staticmethod
    def _fold(s):
        return _key([s])

    # ---------------- 1. 官职 ----------------
    def office(self, name, strict=False, max_items=30):
        """官职档案：品级 / 体系 / 编制 / 职掌 / 属官 / 沿革 / 出处。"""
        k = self._fold(name)
        hits = list(self.i_off.get(k) or [])
        if not hits:
            hits = [o for kk, v in self.i_off.items() if k and (k in kk or kk in k) for o in v]
        if not hits and strict:
            return {"query": name, "found": False, "reason": "office_profiles 无此官"}
        out = {"query": name, "found": bool(hits), "offices": []}
        # 品级序列里的位置：段内常是多官连写，用后缀匹配（"吏部尚书" ⊂ "六部尚书都察院…"）
        lv, tail = [], norm(name)
        for r in self.rank_seq:
            for seg in r.get("segments") or []:
                if tail in norm(seg) or (len(tail) >= 3 and tail[-3:] in norm(seg)):
                    lv.append({"level": r["level"], "segment": seg[:80]})
        # 官名尾缀级兜底：如 "吏部尚书" 未整词命中，就按 "尚书" 归品
        if not lv and len(tail) >= 1:
            for r in self.rank_seq:
                for seg in r.get("segments") or []:
                    if tail[-1] in norm(seg) and r["level"] not in [x["level"] for x in lv]:
                        lv.append({"level": r["level"], "segment": seg[:80]})
                        break
        for o in hits[:5]:
            rec = dict(o)
            rec["rank_seq_refs"] = lv[:8]
            rec["tree"] = self._tree_node(o.get("office_name"), self.office_tree)
            out["offices"].append(rec)
        # 出处：官名出现在哪些底座条里
        srcs = []
        for iid, blob in self._blobs.items():
            if k and k in blob:
                it = self.registry[iid]
                srcs.append({"item_id": iid, "volume": it.get("volume"),
                             "section": it.get("section"),
                             "excerpt": (it.get("original") or "")[:200]})
        srcs.sort(key=lambda x: (x["volume"] or 0, x["item_id"]))
        out["source_items"] = srcs[:max_items]
        return out

    # ---------------- 2. 衙门 ----------------
    def org(self, name, strict=False):
        """衙门档案：品级 / 编制 / 职掌 / 属官 / 沿革 / 下辖。"""
        k = self._fold(name)
        hits = list(self.i_org.get(k) or [])
        if not hits:
            hits = [o for kk, v in self.i_org.items() if k and (k in kk or kk in k) for o in v]
        if not hits and strict:
            return {"query": name, "found": False, "reason": "org_profiles 无此衙门"}
        out = {"query": name, "found": bool(hits), "orgs": []}
        for o in hits[:5]:
            rec = dict(o)
            rec["tree"] = self._tree_node(o.get("org_name"), self.org_tree)
            rec["offices_under"] = [x.get("office_name") for x in self.offices
                                    if _key([x.get("parent_office", "")]) == self._fold(o.get("org_name"))]
            out["orgs"].append(rec)
        return out

    @staticmethod
    def _tree_node(name, tree):
        k = _key([name or ""])
        stack = list(tree.get("roots") or [])
        seen = 0
        while stack and seen < 4000:
            n = stack.pop()
            seen += 1
            if _key([n.get("office_name") or n.get("org_name") or ""]) == k:
                return {"found": True, "parent": n.get("parent_label", ""),
                        "children": [c.get("office_name") or c.get("org_name") for c in (n.get("children") or [])][:40],
                        "child_count": len(n.get("children") or [])}
            stack.extend(n.get("children") or [])
        return {"found": False}

    # ---------------- 3. 地理 ----------------
    def geo(self, name, strict=False):
        """地理档案：层级 / 隶属 / 辖县 / 卫所 / 驿站 / 仓场 / 出处。
        若 geo 树无此名，退回 nams 的驿递/仓场名录与全文检索。"""
        canon = resolve_theme(name)
        k = self._fold(name)
        kc = self._fold(canon)
        hits = list(self.i_geo.get(k) or self.i_geo.get(kc) or [])
        if not hits:
            hits = [g for kk, v in self.i_geo.items()
                    if k and (k in kk or kk in k or (kc and kc in kk)) for g in v]
        if not hits:
            # 退回：名录层（驿递名录 / 仓场名录 / 卫所名录 / 行政区划）+ section 主题
            named = []
            for n in self.nams:
                if not k:
                    continue
                blob = _key([n.get("name", ""), n.get("nam_type", "")])
                if (k in blob or (kc and kc in blob)
                        or any(k in _key([e]) for e in (n.get("entries") or []))):
                    named.append({"nam_type": n.get("nam_type"), "name": n.get("name"),
                                  "item_id": n.get("item_id"),
                                  "matches": [e for e in (n.get("entries") or [])
                                              if k in _key([e])][:20],
                                  "entries": (n.get("entries") or [])[:30]})
            sec_ids = [i for s, ids in self.sections.items()
                       if s and (k in self._fold(s) or (kc and kc in self._fold(s)))
                       for i in ids]
            src = [self._src(i, 200) for i in sec_ids[:24]]
            if named or src:
                return {"query": name, "canonical": canon, "found": True, "places": [],
                        "kind": "names", "nam_records": named[:20], "source_items": src}
        if not hits and strict:
            return {"query": name, "found": False, "reason": "geo 无此地理"}
        out = {"query": name, "found": bool(hits), "places": []}
        for g in hits[:4]:
            kids = [x for x in self.geos if x.get("parent_id") == g.get("geo_id")
                    or _key([x.get("parent", "")]) == self._fold(g.get("name"))]
            chain, cur, hop = [], g, 0
            while cur and hop < 8:
                chain.append({"name": cur.get("name"), "type": cur.get("type")})
                pid = cur.get("parent_id")
                nxt = next((x for x in self.geos if x.get("geo_id") == pid), None) if pid else None
                if not nxt:
                    pn = cur.get("parent")
                    nxt = next((x for x in self.geos if _key([x.get("name", "")]) == _key([pn or ""])), None)
                cur, hop = nxt, hop + 1
            out["places"].append({
                "name": g.get("name"), "type": g.get("type"), "level": g.get("level"),
                "parent": g.get("parent"), "administered_by": g.get("administered_by"),
                "garrisons": (g.get("garrisons") or [])[:40],
                "post_stations": (g.get("post_stations") or [])[:40],
                "granaries": (g.get("granaries") or [])[:40],
                "children": [{"name": c.get("name"), "type": c.get("type")} for c in kids][:80],
                "child_count": len(kids),
                "ancestry": list(reversed(chain)),
                "source": self._src(g.get("item_id")) if g.get("item_id") else None,
            })
        return out

    # ---------------- 4. 制度 / 事例 ----------------
    def rule(self, keyword, limit=40):
        """制度查询：命中 rules 的事例 + 年代链 + 所属制度主题 + 相关 section/出处。"""
        canon = resolve_theme(keyword)
        k = self._fold(canon)
        hits = [r for r in self.rules if k and (k in _key([r.get("original", ""), r.get("subject", "")]))]
        # 书中正名（驿传/仓储…）再兜一层 section
        secs = [s for s in self.sections if k and k in self._fold(s)]
        if not hits and secs:
            ids = {i for s in secs for i in self.sections[s]}
            hits = [r for r in self.rules if r.get("item_id") in ids]
        eras = []
        for r in hits:
            for e in (r.get("era") or []):
                if e not in eras:
                    eras.append(e)
        topics = [t for t in self.tims if k and k in self._fold(t.get("theme", ""))]
        if not topics:
            topics = [t for t in self.tims
                      if any(k and (k in self._fold(x) or self._fold(x) in k)
                             for x in (t.get("keywords") or []))]
        src_ids = sorted({r.get("item_id") for r in hits if r.get("item_id")})
        return {
            "query": keyword, "canonical": canon, "found": bool(hits), "count": len(hits),
            "eras": eras[:24], "topics": topics,
            "sections": secs[:12],
            "source_items": [self._src(i, 180) for i in src_ids[:limit]],
            "rules": [{"item_id": r.get("item_id"), "volume": r.get("volume"),
                       "type": r.get("type"), "subject": r.get("subject"),
                       "action": r.get("action"), "condition": r.get("condition"),
                       "era": r.get("era"), "original": (r.get("original") or "")[:220]}
                      for r in hits[:limit]],
        }

    def timeline(self, theme=""):
        """制度时间线。给关键词返回匹配主题的 16 条 TIM；空则全列。
        先做俗名→正名映射（"驿站"→"驿传"），再匹配主题名/关键词/section。"""
        if not theme:
            return {"themes": self.tims}
        canon = resolve_theme(theme)
        k = self._fold(canon)
        hit = [t for t in self.tims if k in _key([t.get("theme", ""), " ".join(t.get("keywords") or [])])]
        if not hit:
            hit = [t for t in self.tims if any(k in _key([x]) or _key([x]) in k
                                               for x in (t.get("keywords") or []))]
        if not hit:
            hit = [t for t in self.tims if k and k in self._fold(t.get("theme", ""))]
        return {"query": theme, "canonical": canon, "found": bool(hit), "themes": hit,
                "sections": [s for s in self.sections if k and k in self._fold(s)][:12]}

    # ---------------- 5. 品级 ----------------
    def rank(self, level):
        """品级：章服 / 房舍 / 伞盖 / 鞍辔 / 器物 / 该品官名录。"""
        k = self._fold(level)
        recs = [r for r in self.ranks if k in _key([r.get("level", ""), r.get("category", "")])]
        seq = [r for r in self.rank_seq if k in _key([r.get("level", "")])]
        return {"query": level, "found": bool(recs or seq), "rank": recs,
                "sequence": [{"level": s["level"], "order": s.get("order"),
                              "segment_count": s.get("segment_count"),
                              "marker": s.get("marker_item"),
                              "sample": (s.get("segments") or [""])[0][:120],
                              "item_count": len(s.get("item_ids") or [])} for s in seq]}

    # ---------------- 6. 两京 / 互见 ----------------
    def njc(self, topic):
        k = self._fold(topic)
        hits = [n for n in self.njcs if k in _key([n.get("topic", ""), n.get("beijing", ""),
                                                   n.get("nanjing", ""), n.get("original", "")])]
        return {"query": topic, "found": bool(hits), "njc": hits[:20]}

    def xref(self, target):
        k = self._fold(target)
        hits = [x for x in self.xrefs if k in _key([x.get("target", ""), x.get("target_org", ""),
                                                    x.get("original", ""), x.get("note", "")])]
        return {"query": target, "found": bool(hits), "xref": hits[:40]}

    # ---------------- 7. 数字 / 器物 / 文书 ----------------
    def num(self, subject, limit=40):
        k = self._fold(subject)
        hits = [n for n in self.nums if k in _key([n.get("subject", ""), n.get("context", ""),
                                                   n.get("original", "")])]
        return {"query": subject, "found": bool(hits), "count": len(hits), "nums": hits[:limit]}

    def obj(self, name, limit=30):
        """名物/器物查询：先查 vocab 词表（具体名物），再退回 objs 类目。"""
        k = self._fold(name)
        vo = [v for v in self.vocab if k and (k == self._fold(v["name"])
                                              or k in self._fold(v["name"]))]
        exact = [v for v in vo if k == self._fold(v["name"])]
        pool = (exact or vo)[:limit]
        # 原文出处
        srcs = []
        for v in pool[:6]:
            for iid in v.get("item_ids", [])[:4]:
                s = self._src(iid, 160)
                if s:
                    srcs.append(s)
        hits = [o for o in self.objs if k and k in _key([o.get("obj_name", ""), o.get("context", "")])]
        return {"query": name, "found": bool(pool or hits),
                "vocab": [{"name": v["name"], "kind": v["kind"], "item_count": v["item_count"],
                           "hits": v["count"], "contexts": v["contexts"]} for v in pool],
                "category_hits": hits[:limit], "sources": srcs[:24]}

    def document(self, name, limit=30):
        """公文/册籍（REPORT）+ 引书（CIT）。"""
        k = self._fold(name)
        rp = [r for r in self.reports if k in _key([r.get("doc_name", ""), r.get("context", "")])]
        ct = [c for c in self.cits if k in _key([c.get("cited_work", ""), c.get("context", "")])]
        return {"query": name, "found": bool(rp or ct), "reports": rp[:limit], "cits": ct[:limit]}

    # ---------------- 8. 全文检索 ----------------
    def search(self, text, limit=40, min_len=2):
        """全文检索（标题+原文，异体字已归一）。"""
        k = self._fold(text)
        if len(k) < min_len:
            return {"query": text, "found": False, "reason": "关键词过短"}
        hits = []
        for iid, blob in self._blobs.items():
            if k in blob:
                it = self.registry[iid]
                p = blob.find(k)
                hits.append({
                    "item_id": iid, "volume": it.get("volume"), "section": it.get("section"),
                    "node_kind": it.get("node_kind"),
                    "layer_count": (self.join.get(iid) or {}).get("layer_count", 0),
                    "snippet": blob[max(0, p - 30):p + 90],
                })
        hits.sort(key=lambda x: (-x["layer_count"], x["item_id"]))
        return {"query": text, "found": bool(hits), "count": len(hits), "hits": hits[:limit]}

    # ---------------- 9. 父子树 ----------------
    def children(self, name, depth=2):
        """展开父子树。接受官名/衙门名/地名，自动选树。"""
        k = self._fold(name)
        tree = None
        for t in (self.office_tree, self.org_tree):
            stack, seen = list(t.get("roots") or []), 0
            while stack and seen < 5000:
                n = stack.pop(); seen += 1
                if _key([n.get("office_name") or n.get("org_name") or ""]) == k:
                    tree = (n, "office" if "office_name" in n else "org")
                    break
                stack.extend(n.get("children") or [])
            if tree:
                break
        if not tree:
            return {"query": name, "found": False, "reason": "两棵树中都无此节点"}
        node, kind = tree

        def flat(n, d):
            yield {"name": n.get("office_name") or n.get("org_name"), "depth": d,
                   "rank": n.get("rank", ""), "children": len(n.get("children") or [])}
            if d >= depth:
                return
            for c in (n.get("children") or []):
                yield from flat(c, d + 1)

        return {"query": name, "found": True, "kind": kind,
                "nodes": list(flat(node, 0))}

    def path(self, name):
        """从根到叶的路径（地理树 + office/org 树）。"""
        k = self._fold(name)
        # geo
        g = next((x for x in self.geos if self._fold(x.get("name", "")) == k), None)
        if g:
            return {"query": name, "found": True, "kind": "geo",
                    "ancestry": self.geo(name)["places"][0]["ancestry"]}
        for t, kind in ((self.office_tree, "office"), (self.org_tree, "org")):
            chain = self._find_path(t, k)
            if chain:
                return {"query": name, "found": True, "kind": kind, "ancestry": chain}
        return {"query": name, "found": False}

    def _find_path(self, tree, k):
        def dfs(n, acc):
            nm = n.get("office_name") or n.get("org_name") or ""
            acc = acc + [{"name": nm, "rank": n.get("rank", "")}]
            if _key([nm]) == k:
                return acc
            for c in (n.get("children") or []):
                r = dfs(c, acc)
                if r:
                    return r
            return None
        for r in (tree.get("roots") or []):
            got = dfs(r, [])
            if got:
                return got
        return None

    # ---------------- 10. 全景档案 ----------------
    def profile(self, name):
        """一网打尽：把某词在**所有层**的命中汇总成一份档案。"""
        out = {"query": name, "found": False, "layers": {}}
        for tag, fn in (("office", self.office), ("org", self.org), ("geo", self.geo)):
            r = fn(name)
            if r.get("found"):
                out["layers"][tag] = r
        for tag, fn, key in (("njc", self.njc, "njc"), ("xref", self.xref, "xref"),
                             ("num", self.num, "nums"), ("obj", self.obj, "objs"),
                             ("rule", self.rule, "rules"), ("timeline", self.timeline, "themes"),
                             ("rank", self.rank, "rank")):
            r = fn(name)
            if r.get("found"):
                out["layers"][tag] = r
        s = self.search(name)
        if s.get("found"):
            out["layers"]["search"] = {"count": s["count"], "top": s["hits"][:15]}
        out["found"] = bool(out["layers"])
        # 结构位置
        out["tree"] = self.children(name, depth=1)
        out["path"] = self.path(name)
        return out

    # ---------------- 11. ask 分发 ----------------
    ROUTES = [
        (r"品级|几品|正[一二三四五六七八九]品|从[一二三四五六七八九]品", "rank"),
        (r"两京|南京|北京.*对照|对照", "njc"),
        (r"互见|参见|同事例|详见", "xref"),
        (r"怎么|如何|流程|事例|制度|演变|沿革|历代", "rule"),
        (r"多少|几里|几石|几贯|数|额|总数", "num"),
        (r"旗|扇|冠|服|冕|轿|辂|仪仗|器物|陈设", "obj"),
        (r"册|勘合|文凭|文书|榜|引", "document"),
        (r"卫|所|驿|递运|仓|府|州|县|司|管辖|隶属", "geo"),
    ]

    def ask(self, question):
        """粗粒度自然语言分发：判断问的是哪一层，再抽取实体查询。"""
        q = norm(question)
        route = None
        for pat, tag in self.ROUTES:
            if re.search(pat, q):
                route = tag
                break
        entities = self._extract_entities(q)
        res = {"question": question, "route": route, "entities": entities}
        if not entities:
            # 俗名 → 正名 → 主题线
            nq = norm(question)
            toks = theme_tokens(question)
            th = [n for n in self.i_theme if n and n in nq]
            for c in toks:
                if c not in th and c in self.i_theme:
                    th.append(c)
            if not th:
                kq = _key([nq])
                th = [s for s in self.sections if kq and kq in self._fold(s)]
                for c in toks:
                    for s in self.sections:
                        if c in self._fold(s) and s not in th:
                            th.append(s)
            if th:
                res["entities"] = th[:3]
                res["result"] = self.rule(th[0])
                res["timeline"] = self.timeline(th[0])
                return res
            res["result"] = self.search(q)
            return res
        fn = {"rank": self.rank, "njc": self.njc, "xref": self.xref, "rule": self.rule,
              "num": self.num, "obj": self.obj, "document": self.document, "geo": self.geo}.get(route)
        if route == "rule":
            fn = self.rule
        ent = entities[0]
        primary = fn(ent) if fn else self.profile(ent)
        res["result"] = primary
        if not primary.get("found"):
            res["result"] = self.search(ent)
        if len(entities) > 1:
            res["also"] = {e: {"found": self.profile(e)["found"]} for e in entities[1:4]}
        return res

    def _extract_entities(self, q):
        """从问题里抠出已知实体（官/衙/地/名物），按出现位置排序。"""
        pool = []
        for o in self.offices:
            n = o.get("office_name") or ""
            if len(n) >= 2 and n in q:
                pool.append((q.find(n), n))
        for o in self.orgs:
            n = o.get("org_name") or ""
            if len(n) >= 2 and n in q:
                pool.append((q.find(n), n))
        for g in self.geos:
            n = g.get("name") or ""
            if len(n) >= 2 and n in q:
                pool.append((q.find(n), n))
        for v in self.vocab:
            n = v.get("name") or ""
            if len(n) >= 2 and n in q and v.get("item_count", 0) >= 2:
                pool.append((q.find(n), n))
        # 制度主题词（漕运/驿传/盐法/卫所…）
        for n in self.i_theme:
            if len(n) >= 2 and n in q:
                pool.append((q.find(n), n))
        pool.sort(key=lambda x: (x[0], -len(x[1])))
        out, seen = [], set()
        for _, n in pool:
            if n in seen:
                continue
            if any(n != s and n in s for s in seen):
                continue
            seen.add(n); out.append(n)
        return out[:6]

    # ---------------- 12. 概况 / 自检 ----------------
    @staticmethod
    def _tree_meta(t):
        """树文件兼容：老版可能是裸 roots 列表，新版是含元信息的 dict。"""
        if isinstance(t, dict):
            return t
        if isinstance(t, list):
            return {"roots": t, "total_roots": len(t)}
        return {"roots": [], "total_roots": 0}

    def stats(self):
        d = lambda x: len(x)
        ot, gt = self._tree_meta(self.office_tree), self._tree_meta(self.org_tree)
        gt_geo = self._tree_meta(getattr(self, "geo_tree", {}))
        return {
            "底座条数": len(self.registry),
            "join 条数": len(self.join),
            "孤立条": sum(1 for j in self.join.values() if j.get("layer_count", 0) == 0),
            "层规模": {
                "office_profiles": d(self.offices), "org_profiles": d(self.orgs),
                "geo": d(self.geos), "rules": d(self.rules), "ents": d(self.ents),
                "nams": d(self.nams), "num": d(self.nums), "objs": d(self.objs),
                "reports": d(self.reports), "cits": d(self.cits), "xref": d(self.xrefs),
                "njc": d(self.njcs), "rank": d(self.ranks), "rank_sequence": d(self.rank_seq),
                "tim": d(self.tims), "laws": d(self.laws), "rituals": d(self.rituals),
                "dress": d(self.dress), "inspect": d(self.inspect),
                "foreign": d(self.foreign), "materials": d(self.materials),
            },
            "树": {"office_tree_roots": ot.get("total_roots"),
                   "office_tree_reachable": ot.get("total_reachable"),
                   "org_tree_roots": gt.get("total_roots"),
                   "org_tree_reachable": gt.get("total_reachable"),
                   "geo_tree_roots": gt_geo.get("total_roots")},
        }

    def check(self):
        """自检：接口可用性 + 关键实体可查性。"""
        probes = ["吏部尚书", "户部", "苏州府", "漕运", "正三品", "衮冕", "驿站"]
        rows = []
        for p in probes:
            r = self.profile(p)
            rows.append({"probe": p, "found": r["found"],
                         "layers": sorted(r["layers"].keys())})
        return {"ok": all(r["found"] for r in rows), "probes": rows,
                "stats": self.stats()}


# ================= 命令行 =================
def _pp(obj, indent=2):
    print(json.dumps(obj, ensure_ascii=False, indent=indent)[:20000])


def main(argv):
    if not argv:
        print(__doc__)
        return 0
    kb = MingHuidianKB()
    cmd, rest = argv[0], argv[1:]
    if cmd == "stats":
        _pp(kb.stats()); return 0
    if cmd == "check":
        r = kb.check(); _pp(r)
        return 0 if r["ok"] else 1
    if cmd in ("office", "org", "geo", "rule", "num", "obj", "document",
               "njc", "xref", "rank", "timeline", "search", "path", "profile"):
        if not rest:
            print(f"用法: {cmd} <关键词>"); return 2
        _pp(getattr(kb, cmd)(rest[0])); return 0
    if cmd == "tree":
        if not rest:
            print("用法: tree <名称> [--depth N]"); return 2
        depth = 2
        if "--depth" in rest:
            i = rest.index("--depth")
            depth = int(rest[i + 1])
        _pp(kb.children(rest[0], depth=depth)); return 0
    if cmd == "ask":
        _pp(kb.ask(" ".join(rest))); return 0
    print(f"未知命令: {cmd}")
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
