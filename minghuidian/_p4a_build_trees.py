# -*- coding: utf-8 -*-
"""
P4-A 父子关系重建（打通与交付 · 第一件）

目标：把三棵树真正"长出来"，消除悬空引用。

  1) ORG 树   org_profiles 329 → parent_org 267 条已填、悬空 0；但 child_orgs 仅 36 条。
              本步由 parent_org 反算 child_orgs，并输出 org_tree.json / org_tree.md。
  2) OFFICE 树 office_profiles 566 → parent_office 393 条，其中 155 条"悬空"。
              悬空分三类：
                (a) 指向**虚根**（皇帝 / 朝廷 / —）→ 建虚拟根节点
                (b) 指向**衙门名**（吏部 / 都察院 …）→ 建"org 锚点"节点，并桥接 office↔org
                (c) 指向**简称/别名**（尚书 / 都御史 / 侍郎 …）→ 用同层级补全规则归一
              输出 office_tree.json / office_tree.md。
  3) GEO 树   geo 3883 → parent_id 已 0 悬空、children 与 parent_id 完全一致（仅需复核）；
              本步只做一致性再校验 + 补 `children` 排序稳定化。
  4) 三树统一输出 _trees.json，供查询接口与报告使用。

重跑幂等：只读取 _layers/*.json，写回同目录 + 根目录 _trees.json。
"""
import json, os, re
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")

VIRTUAL_ROOTS = {"皇帝", "朝廷", "—", "", "内府", "宗室"}


def load(name):
    p = os.path.join(LAYERS, name + ".json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


orgs = load("org_profiles")
offs = load("office_profiles")
geo = load("geo")

ORG_NAMES = {o["org_name"] for o in orgs}
OFF_NAMES = {o["office_name"] for o in offs}


# ============================================================
# 1) ORG 树：由 parent_org 反算 child_orgs
# ============================================================
org_by_name = {o["org_name"]: o for o in orgs}

# 清空重建 child_orgs（幂等）
for o in orgs:
    o["child_orgs"] = []

org_dangling = []
for o in orgs:
    p = (o.get("parent_org") or "").strip()
    if not p:
        continue
    if p in org_by_name:
        org_by_name[p]["child_orgs"].append(o["org_name"])
    else:
        org_dangling.append((o["org_name"], p))

# 悬空 parent_org 也建虚拟节点（保持引用不丢）
org_virtual = {}
for name, p in org_dangling:
    org_virtual.setdefault(p, []).append(name)

# 去重 + 排序
for o in orgs:
    o["child_orgs"] = sorted(set(o["child_orgs"]))


def build_org_node(o, seen):
    if o["org_name"] in seen:
        return None
    seen.add(o["org_name"])
    return {
        "org_name": o["org_name"],
        "rank": o.get("rank", ""),
        "category": o.get("category", ""),
        "location": o.get("location", ""),
        "volume": o.get("volume", ""),
        "source": o.get("source", ""),
        "history_count": len(o.get("history") or []),
        "staff_count": len(o.get("staff") or []),
        "children": [],
    }


org_roots = []
_seen = set()
for o in orgs:
    if not (o.get("parent_org") or "").strip():
        n = build_org_node(o, _seen)
        if n:
            org_roots.append(n)


def fill_org(node, seen):
    o = org_by_name[node["org_name"]]
    for c in o["child_orgs"]:
        if c in org_by_name:
            ch = build_org_node(org_by_name[c], seen)
            if ch:
                node["children"].append(ch)
                fill_org(ch, seen)


for r in org_roots:
    fill_org(r, _seen)

# 虚拟根（悬空 parent 引用）单独挂
org_virtual_nodes = []
for vname, kids in sorted(org_virtual.items()):
    org_virtual_nodes.append({
        "org_name": vname,
        "virtual": True,
        "children": [{"org_name": k, "virtual_child": True, "children": []} for k in sorted(kids)],
    })


def count_org(nodes):
    n = 0
    for x in nodes:
        n += 1 + count_org(x.get("children") or [])
    return n


# ============================================================
# 2) OFFICE 树：悬空 parent 三类处理
# ============================================================
# 2.1 别名归一：把 parent_office 的简称补全为规范 office_name
#
# 关键洞察：会典里的"上级"多是**同衙内的班序上级**，简称只在**本衙门**内有意义。
#   浙江道监察御史.parent = 都御史   → 都察院左都御史
#   太常寺典簿.parent     = 寺丞     → 太常寺寺丞
# 故先取官职名的**衙门前缀**（如"都察院""太常寺"）去消歧，再退回全库唯一匹配。
ORG_PREFIXES = sorted({o["org_name"] for o in orgs}, key=len, reverse=True)
ALIAS_OVERRIDE = {
    # 明确映射（会典用语 → 主档规范名）
    "都御史": ["左都御史", "右都御史"],
    "副都御史": ["左副都御史", "右副都御史"],
    "佥都御史": ["左佥都御史", "右佥都御史"],
    "寺卿": None,       # 由前缀消歧
    "少卿": None,
    "寺丞": None,
    "照磨": None,
}

# 精确覆盖表：本衙前缀也消歧不了的、跨衙/斜杠/散官连缀的情况，逐条钉死。
#   key=官职名, value=上级规范名（""=提升为根）
EXACT_PARENT = {
    "六部司务": "吏部尚书",          # 六部共名，取吏部为代表
    "翰林院五经博士": "翰林院学士",
    "翰林修撰": "翰林院学士",
    "通政司知事": "通政使",
    "府照磨": "府经历",
    "钦天监五官灵台郎": "钦天监监副",
    "钦天监五官保章正": "钦天监监副",
    "钦天监五官司历": "钦天监监副",
    "知县": "知府",                  # 「知州/知府」取知府
    "税课局大使": "知府",
    "仓大使": "知府",
    "驿丞": "知府",
    "河泊所官": "知府",
    "府儒学训导": "府儒学教授",
    "州儒学训导": "州儒学学正",
    "税课局副使": "税课局大使",
    "都督同知": "左都督",
    "卫指挥同知": "卫指挥使",
    "卫指挥佥事": "卫指挥同知",
    "卫镇抚": "卫指挥佥事",
    "总兵官": "兵部尚书",            # 「皇帝/兵部」取兵部
    "郎中": "兵部武选清吏司郎中",     # 六部共名，取兵部武选清吏司为代表（唯一进主档的郎中）
}


def resolve_alias(off_name, p, off_names):
    """把简称 parent 解析为规范 office_name；失败返回 None。"""
    # (0) 精确覆盖表优先
    if off_name in EXACT_PARENT:
        tgt = EXACT_PARENT[off_name]
        if tgt in off_names:
            return tgt
    # (a) 显式映射
    if p in ALIAS_OVERRIDE and ALIAS_OVERRIDE[p]:
        for cand in ALIAS_OVERRIDE[p]:
            if cand in off_names:
                return cand
    # (b) 本衙门前缀消歧：取官职名里出现的 org 前缀
    prefix = ""
    for pr in ORG_PREFIXES:
        if off_name.startswith(pr) or pr in off_name:
            prefix = pr
            break
    if prefix:
        cands = [x for x in off_names if x.startswith(prefix) and x.endswith(p)]
        if len(cands) == 1:
            return cands[0]
        if len(cands) > 1:
            # 优先"左"侧 / 更短名
            cands.sort(key=lambda s: (0 if "左" in s else 1, len(s)))
            return cands[0]
    # (c) 全库唯一后缀匹配
    cands = [x for x in off_names if x.endswith(p)]
    if len(cands) == 1:
        return cands[0]
    # (d) 全库含匹配
    cands = [x for x in off_names if p in x]
    if len(cands) == 1:
        return cands[0]
    return None


# 2.2 分类每个 parent
off_parent_kind = {}
alias_unresolved = []
for o in offs:
    p = (o.get("parent_office") or "").strip()
    if not p:
        off_parent_kind[o["office_name"]] = ("root", "")
    elif p in OFF_NAMES:
        off_parent_kind[o["office_name"]] = ("office", p)
    elif p in VIRTUAL_ROOTS:
        off_parent_kind[o["office_name"]] = ("virtual", p)
    elif p in ORG_NAMES:
        off_parent_kind[o["office_name"]] = ("org", p)
    else:
        r = resolve_alias(o["office_name"], p, OFF_NAMES)
        if r and r != o["office_name"]:
            off_parent_kind[o["office_name"]] = ("office", r)
            o["parent_office_resolved"] = r
        else:
            off_parent_kind[o["office_name"]] = ("alias", p)
            alias_unresolved.append((o["office_name"], p))

# 2.3 由 parent 反算 child_offices（幂等重建）
off_by_name = {o["office_name"]: o for o in offs}
for o in offs:
    o["child_offices"] = []
    o["child_orgs"] = []

for o in offs:
    kind, p = off_parent_kind[o["office_name"]]
    if kind == "office":
        off_by_name[p]["child_offices"].append(o["office_name"])
    elif kind == "org":
        # 官职挂在衙门下 → 写入该 org 的 child_offices 与 office 的 parent_org
        o["parent_org"] = p
        org_by_name[p]["child_offices"] = org_by_name[p].get("child_offices", [])
        org_by_name[p]["child_offices"].append(o["office_name"])

for o in offs:
    off_by_name[o["office_name"]]["child_offices"] = sorted(set(o["child_offices"]))

# 2.3b 环路检测：alias 消歧可能造环（寺丞→少卿→寺卿→寺丞）。
#       检测有向图中的环，把环内"最长名"的 parent 断开（退化为 root），保证树无环。
_adj = {}
for o in offs:
    kind, p = off_parent_kind[o["office_name"]]
    _adj[o["office_name"]] = p if kind == "office" else None

_WHITE, _GRAY, _BLACK = 0, 1, 2
_color = {n: _WHITE for n in _adj}
cycles_broken = []


def _dfs(n, stack):
    _color[n] = _GRAY
    stack.append(n)
    nxt = _adj.get(n)
    if nxt:
        if _color.get(nxt) == _GRAY:
            # 找到环：stack 中 nxt..n
            ring = stack[stack.index(nxt):]
            victim = max(ring, key=len)
            _adj[victim] = None
            cycles_broken.append((victim, ring))
            _color[n] = _BLACK
            stack.pop()
            return True
        if _color.get(nxt) == _WHITE:
            if _dfs(nxt, stack):
                _color[n] = _BLACK
                stack.pop()
                return True
    stack.pop()
    _color[n] = _BLACK
    return False


for n in list(_adj):
    if _color[n] == _WHITE:
        _dfs(n, [])

for name in cycles_broken:
    off_parent_kind[name[0]] = ("cycle_broken", "")
    _adj[name[0]] = None

# 依断环结果重算 child_offices
for o in offs:
    o["child_offices"] = []
for o in offs:
    kind, p = off_parent_kind[o["office_name"]]
    if kind == "office":
        off_by_name[p]["child_offices"].append(o["office_name"])
for o in offs:
    off_by_name[o["office_name"]]["child_offices"] = sorted(set(off_by_name[o["office_name"]]["child_offices"]))

# 2.4 建 office 树（只展开 office→office 边）
_oseen = set()


def build_off_node(o):
    if o["office_name"] in _oseen:
        return None
    _oseen.add(o["office_name"])
    return {
        "office_name": o["office_name"],
        "rank": o.get("rank", ""),
        "type": o.get("type", ""),
        "system": o.get("system", ""),
        "location": o.get("location", ""),
        "headcount": o.get("headcount", 0),
        "salary": o.get("salary"),
        "history_count": len(o.get("history") or []),
        "children": [],
    }


def fill_off(node):
    o = off_by_name[node["office_name"]]
    for c in o["child_offices"]:
        if c in off_by_name:
            ch = build_off_node(off_by_name[c])
            if ch:
                node["children"].append(ch)
                fill_off(ch)


# 根：无 parent 或 parent 为 virtual/alias
off_roots = []
for o in offs:
    kind, p = off_parent_kind[o["office_name"]]
    if kind in ("root", "virtual", "alias"):
        n = build_off_node(o)
        if n:
            n["parent_label"] = p or "（无上级）"
            n["parent_kind"] = kind
            off_roots.append(n)
for r in off_roots:
    fill_off(r)

# 未被 office 树覆盖的（挂在 org 下的官）
off_covered = set(_oseen)
org_anchored = defaultdict(list)
for o in offs:
    kind, p = off_parent_kind[o["office_name"]]
    if o["office_name"] not in off_covered and kind == "org":
        org_anchored[p].append({
            "office_name": o["office_name"], "rank": o.get("rank", ""),
            "type": o.get("type", ""), "headcount": o.get("headcount", 0),
        })

# 2.5 孤立官：既无 parent_office 又未挂衙门 —— 尝试用"本衙门前缀"补一个 org 锚
off_orphan_final = []
for o in offs:
    if o["office_name"] in off_covered or o.get("parent_org"):
        continue
    if (o.get("parent_office") or "").strip():
        continue
    hit = ""
    for pr in ORG_PREFIXES:
        if o["office_name"].startswith(pr) and pr in ORG_NAMES:
            hit = pr
            break
    if hit:
        o["parent_org"] = hit
        org_anchored[hit].append({
            "office_name": o["office_name"], "rank": o.get("rank", ""),
            "type": o.get("type", ""), "headcount": o.get("headcount", 0),
        })
    else:
        off_orphan_final.append(o["office_name"])

# ============================================================
# 3) GEO 树一致性复核
# ============================================================
geo_by_id = {g["geo_id"]: g for g in geo}
geo_children = defaultdict(list)
geo_roots = []
for g in geo:
    pid = (g.get("parent_id") or "").strip()
    if pid and pid in geo_by_id:
        geo_children[pid].append(g["geo_id"])
    else:
        geo_roots.append(g["geo_id"])

geo_mismatch = 0
for g in geo:
    cur = sorted(g.get("children") or [])
    want = sorted(geo_children.get(g["geo_id"], []))
    if cur != want:
        geo_mismatch += 1
    g["children"] = want  # 稳定化

# ============================================================
# 4) 写回 + 输出
# ============================================================
json.dump(orgs, open(os.path.join(LAYERS, "org_profiles.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(offs, open(os.path.join(LAYERS, "office_profiles.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(geo, open(os.path.join(LAYERS, "geo.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

org_tree = {"roots": org_roots, "virtual_roots": org_virtual_nodes,
            "total_orgs": len(orgs), "total_roots": len(org_roots),
            "total_reachable": count_org(org_roots)}
json.dump(org_tree, open(os.path.join(LAYERS, "org_tree.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

office_tree = {"roots": off_roots, "org_anchored": dict(org_anchored),
               "total_offices": len(offs), "total_roots": len(off_roots),
               "total_reachable": count_org(off_roots),
               "alias_unresolved": [{"office": a, "parent_label": b} for a, b in alias_unresolved],
               "cycles_broken": [{"office": a, "ring": b} for a, b in cycles_broken],
               "orphan_offices": sorted(off_orphan_final)}
json.dump(office_tree, open(os.path.join(LAYERS, "office_tree.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

trees = {
    "org": {"roots": len(org_roots), "virtual": len(org_virtual_nodes),
            "total": len(orgs), "reachable": count_org(org_roots)},
    "office": {"roots": len(off_roots), "total": len(offs),
               "reachable": count_org(off_roots),
               "org_anchored_orgs": len(org_anchored),
               "org_anchored_offices": sum(len(v) for v in org_anchored.values()),
               "orphans": len(office_tree["orphan_offices"])},
    "geo": {"roots": len(geo_roots), "total": len(geo),
            "mismatch_before": geo_mismatch},
}
json.dump(trees, open(os.path.join(ROOT, "_trees.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)


# ============================================================
# 5) Markdown 视图
# ============================================================
def md_org(node, depth, out, maxd=3):
    if depth > maxd:
        return
    pad = "  " * depth
    out.append(f"{pad}- **{node['org_name']}**"
               + (f"（{node['rank']}）" if node.get("rank") else "")
               + (f" `{node['category']}`" if node.get("category") else ""))
    for c in node.get("children") or []:
        md_org(c, depth + 1, out, maxd)


lines = ["# ORG 衙门树（P4-A 重建）", "",
         f"> 衙门 {len(orgs)} 个 ｜ 根 {len(org_roots)} 个 ｜ 主树可达 {count_org(org_roots)} 个 ｜ "
         f"虚拟根 {len(org_virtual_nodes)} 个", ""]
for r in org_roots:
    md_org(r, 0, lines)
if org_virtual_nodes:
    lines += ["", "## 虚拟根（原悬空 parent_org）", ""]
    for v in org_virtual_nodes:
        lines.append(f"- **{v['org_name']}**")
        for c in v["children"]:
            lines.append(f"  - {c['org_name']}")
open(os.path.join(LAYERS, "org_tree.md"), "w", encoding="utf-8").write("\n".join(lines))


def md_off(node, depth, out, maxd=4):
    if depth > maxd:
        return
    pad = "  " * depth
    out.append(f"{pad}- **{node['office_name']}**"
               + (f"（{node['rank']}）" if node.get("rank") else "")
               + (f" `{node['system']}/{node['type']}`" if node.get("system") else ""))
    for c in node.get("children") or []:
        md_off(c, depth + 1, out, maxd)


olines = ["# OFFICE 官职树（P4-A 重建）", "",
          f"> 官职 {len(offs)} 个 ｜ 树根 {len(off_roots)} 个 ｜ 可达 {count_org(off_roots)} 个 ｜ "
          f"office→office 边 {sum(1 for v in off_parent_kind.values() if v[0]=='office')} 条 ｜ "
          f"挂衙门的官 {sum(len(v) for v in org_anchored.values())} 个 / {len(org_anchored)} 衙门", ""]
# 按 parent_label 分组展示根，避免 212 个孤立小节
_by_label = defaultdict(list)
for r in off_roots:
    _by_label[r["parent_label"]].append(r)
for label in sorted(_by_label, key=lambda x: (-len(_by_label[x]), x)):
    group = _by_label[label]
    roots_with_kids = [r for r in group if r["children"]]
    olines.append(f"## 上级：{label}（{len(group)} 个根，其中 {len(roots_with_kids)} 个有下属）")
    olines.append("")
    for r in sorted(group, key=lambda x: x["office_name"]):
        if r["children"]:
            md_off(r, 0, olines, maxd=4)
        else:
            olines.append(f"- {r['office_name']}（{r['rank']}） `{r['system']}/{r['type']}`")
    olines.append("")
if org_anchored:
    olines += ["", "## 挂在衙门下的官（未入 office 树）", ""]
    for oname, kids in sorted(org_anchored.items()):
        olines.append(f"- **{oname}**")
        for k in kids:
            olines.append(f"  - {k['office_name']}（{k['rank']}）")
open(os.path.join(LAYERS, "office_tree.md"), "w", encoding="utf-8").write("\n".join(olines))


# ============================================================
# 6) 校验输出
# ============================================================
print("=" * 68)
print("P4-A 父子关系重建")
print("=" * 68)
print(f"\n[ORG 树]  衙门 {len(orgs)} ｜ 根 {len(org_roots)} ｜ 主树可达 {count_org(org_roots)}"
      f" ｜ 虚拟根 {len(org_virtual_nodes)}")
print(f"          child_orgs 填充: {sum(1 for o in orgs if o['child_orgs'])}/{len(orgs)}"
      f"（重建前 36）")
print(f"          悬空 parent_org: {len(org_dangling)} → 已建虚拟根承接")
if org_dangling:
    print(f"          悬空样例: {org_dangling[:6]}")

print(f"\n[OFFICE 树] 官职 {len(offs)} ｜ 根 {len(off_roots)} ｜ 可达 {count_org(off_roots)}")
print(f"          父子边(office→office): {sum(1 for v in off_parent_kind.values() if v[0]=='office')}"
      f" ｜ 有子者 {sum(1 for o in offs if o['child_offices'])}")
kk = Counter(v[0] for v in off_parent_kind.values())
print(f"          parent 分类: {dict(kk)}")
print(f"          alias 未解析: {len(alias_unresolved)}"
      + (f"  样例 {alias_unresolved[:5]}" if alias_unresolved else "  ✅ 全部解析"))
print(f"          断环: {len(cycles_broken)}"
      + (f"  样例 {[c[0] for c in cycles_broken[:4]]}" if cycles_broken else "  ✅ 无环"))
print(f"          挂衙门下的官: {sum(len(v) for v in org_anchored.values())} 个 / "
      f"{len(org_anchored)} 衙门（重建前 0，office→org 桥已建）")
print(f"          仍孤立（无 parent 也未挂衙门）: {len(off_orphan_final)}")
if off_orphan_final:
    print(f"          样例: {off_orphan_final[:8]}")

print(f"\n[GEO 树]  {len(geo)} 节点 ｜ 根 {len(geo_roots)} ｜ children 校正 {geo_mismatch} 处"
      f" → 现与 parent_id 完全一致")

print(f"\n写出: _layers/org_tree.json|md, _layers/office_tree.json|md, _trees.json")
