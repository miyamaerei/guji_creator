# -*- coding: utf-8 -*-
"""
P1-D: 扩充 org_profiles 至 200+ 衙门，建 部→司→科 树。

策略：
  1) 以 _p1d_seed_orgs.json 为种子（含 parent/品级/职责/归属卷）。
  2) 对每个衙门在 _item_registry.json 中定位「出处」：
       - 优先取其所属卷的「沿革」条（首条）作为 history/source；
       - 其次取全书中首次出现该名的条目作为 source。
  3) 与既有 org_profiles.json 合并：保留既有丰富字段，补齐 volume/parent/child。
  4) 重建 parent_org / child_orgs 一致性，输出树。
"""
import json, os, re
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")

REG = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
# 幂等：始终以 P1-D 之前的备份为基线，避免重复运行造成别名串扰
_OLD_BASE = os.path.join(ROOT, "_backup_p0", "org_profiles.pre_p1d.json")
OLD = json.load(open(_OLD_BASE if os.path.exists(_OLD_BASE)
                    else os.path.join(LAYERS, "org_profiles.json"), encoding="utf-8"))
SEED = json.load(open(os.path.join(ROOT, "_p1d_seed_orgs.json"), encoding="utf-8"))["orgs"]

# ---------- 索引 ----------
# 每卷首条「沿革」（衙门本传）
VOL_FIRST = {}
VOL_HEADER = {}   # 卷 -> 首条 id
vol_items = defaultdict(list)
for k, v in REG.items():
    vol_items[v["volume"]].append((k, v))
for vol, items in vol_items.items():
    items.sort(key=lambda x: x[0])
    VOL_HEADER[vol] = items[0][0]
    for k, v in items:
        if v.get("node_kind") == "沿革":
            VOL_FIRST[vol] = (k, v)
            break

# 名称 -> 首次出现条目
NAME_FIRST = {}
for k, v in sorted(REG.items()):
    blob = (v.get("title") or "") + (v.get("original") or "") + (v.get("section") or "")
    for name in re.findall(r"[\u4e00-\u9fff]{2,12}", blob):
        pass  # 太慢，改为按需检索


def find_first(name, aliases=None, vol=None):
    """在 registry 中找该衙门出处条目 id + volume（优先本卷）。"""
    cands = [name] + list(aliases or [])

    def scan(pred):
        # 先找 沿革 条（衙门本传）
        for k, v in sorted(REG.items()):
            if v.get("node_kind") != "沿革" or not pred(v):
                continue
            blob = (v.get("title") or "") + (v.get("original") or "")
            if any(c in blob for c in cands):
                return k, v["volume"]
        # 再按条目顺序取首个提及
        for k, v in sorted(REG.items()):
            if not pred(v):
                continue
            blob = (v.get("title") or "") + (v.get("original") or "")
            if any(c in blob for c in cands):
                return k, v["volume"]
        return None, None

    if vol:
        k, vv = scan(lambda v: v["volume"] == vol)
        if k:
            return k, vv
    return scan(lambda v: True)


def vol_header_info(vol):
    """返回该卷首条 (id, node) 及其原文，作为衙门「本传」。"""
    if vol in VOL_FIRST:
        return VOL_FIRST[vol]
    if vol in VOL_HEADER:
        k = VOL_HEADER[vol]
        return k, REG[k]
    return None, None


# ---------- 抽取 history ----------
ERA_RE = re.compile(r"(洪武|建文|永乐|洪熙|宣德|正统|景泰|天顺|成化|弘治|正德|嘉靖|隆庆|万历)"
                    r"(元年|二年|三年|四年|五年|六年|七年|八年|九年|十年|十一年|十二年|十三年|"
                    r"十四年|十五年|十六年|十七年|十八年|十九年|二十年|二十一年|二十二年|"
                    r"二十三年|二十四年|二十五年|二十六年|二十七年|二十八年|二十九年|三十年|"
                    r"初|间|末)?")
VERB = ["置", "设", "改", "罢", "革", "复", "增", "减", "并", "升", "降", "立", "定", "裁", "归并"]


def split_events(text, limit=8):
    """从沿革原文中粗切事件句。"""
    if not text:
        return []
    # 按朝代纪年切分
    parts = []
    idxs = [m.start() for m in ERA_RE.finditer(text)]
    if not idxs:
        return []
    idxs.append(len(text))
    for i in range(len(idxs) - 1):
        seg = text[idxs[i]:idxs[i + 1]]
        if len(seg) < 4:
            continue
        m = ERA_RE.match(seg)
        era = m.group(0) if m else ""
        parts.append({"year": era, "event": seg[len(era):][:40]})
        if len(parts) >= limit:
            break
    return parts


def _probes(name, aliases=None):
    """生成匹配用的名称变体（含去尾缀词干）。"""
    ps = [name] + list(aliases or [])
    stem = re.sub(r"(承宣布政使司|都转运盐使司|盐课提举司|清吏司|司务厅|照磨所|经历司|经歴司|"
                  r"寺|监|院|司|府|部|局|库|仓|所|科|道|卫)$", "", name)
    if stem and stem != name:
        ps.append(stem)
    return list(dict.fromkeys([p for p in ps if p]))


def derive_history(name, vol, aliases=None):
    """在衙门所属卷内找「以该衙门为主语」的沿革条；再退回全局。"""
    probes = _probes(name, aliases)

    def best_in(pool):
        best, bestpos = None, 10 ** 9
        for k, v in pool:
            blob = v.get("original") or ""
            for c in probes:
                pos = blob.find(c)
                if 0 <= pos < bestpos:
                    bestpos, best = pos, (k, v)
        return best, bestpos

    # 1) 本卷沿革，取名称出现最靠前者
    if vol:
        pool = [(k, v) for k, v in sorted(REG.items())
                if v["volume"] == vol and v.get("node_kind") == "沿革"]
        best, pos = best_in(pool)
        if best and pos <= 120:
            evs = split_events(best[1].get("original") or "")
            if evs:
                return evs, best[0]
    # 2) 全局沿革（主语须靠前）
    pool = [(k, v) for k, v in sorted(REG.items()) if v.get("node_kind") == "沿革"]
    best, pos = best_in(pool)
    if best and pos <= 40:
        evs = split_events(best[1].get("original") or "")
        if evs:
            return evs, best[0]
    return [], None


# ---------- 合并 ----------
# 既有 profile 建立索引（按 org_name 与去后缀名）
def base_name(n):
    return re.sub(r"(清吏司|司务厅|照磨所|经历司|经歴司)$", "", n)


old_by_name = {}
for o in OLD:
    old_by_name[o.get("org_name", "")] = o

new_profiles = []
added, updated = 0, 0
seen = set()
for s in SEED:
    name = s["name"]
    if name in seen:
        continue
    seen.add(name)

    # 找既有（兼容旧名，如 文选司 vs 文选清吏司）
    existing = old_by_name.get(name)
    if not existing:
        for alias in [name] + s.get("aliases", []):
            if alias in old_by_name:
                existing = old_by_name[alias]
                break

    prof = dict(existing) if existing else {}
    prof["org_name"] = name
    # 分类以种子为准（统一受控词表）
    prof["category"] = s.get("category") or prof.get("category")
    prof["rank"] = prof.get("rank") or s.get("rank") or ""
    prof["duties"] = prof.get("duties") or s.get("duties") or ""
    prof["note"] = prof.get("note") or s.get("note") or ""
    prof["parent_org"] = s.get("parent")            # 种子为准（可改）
    prof["volume"] = s.get("volume")
    prof["child_orgs"] = []                          # 重建

    # 出处定位
    src_id, src_vol = find_first(name, s.get("aliases"), prof.get("volume"))
    if src_id:
        prof.setdefault("source", src_id)
        if not prof.get("volume"):
            prof["volume"] = src_vol

    # 沿革
    hist, hid = derive_history(name, prof.get("volume"), s.get("aliases"))
    if hist and not prof.get("history"):
        prof["history"] = hist
    if hid:
        prof["history_source"] = hid
        prof["source"] = hid

    # 跨卷沿革特例（布政使司沿革在卷17、锦衣卫沿革在卷180首条）
    if not prof.get("history"):
        ov = "017-001" if name.endswith("承宣布政使司") else ("180-001" if name == "锦衣卫" else None)
        if ov and ov in REG:
            evs = split_events(REG[ov].get("original") or "")
            if evs:
                prof["history"] = evs
                prof["history_source"] = ov
                prof["source"] = ov

    if existing:
        updated += 1
    else:
        added += 1
    new_profiles.append(prof)

# ---------- 重建 child_orgs ----------
by_name = {p["org_name"]: p for p in new_profiles}
for p in new_profiles:
    par = p.get("parent_org")
    if par and par in by_name:
        kids = by_name[par].setdefault("child_orgs", [])
        if p["org_name"] not in kids:
            kids.append(p["org_name"])

# ---------- 校验 ----------
dangling = [p["org_name"] for p in new_profiles if p.get("parent_org") and p["parent_org"] not in by_name]

# ---------- 修复陈旧 source（P0 重建后卷号变动导致） ----------
SRC_FIELDS = ("rank_source", "staff_source", "duties_source", "history_source")
fixed_src = 0
for p in new_profiles:
    vol = p.get("volume")

    def valid(s):
        if not s or not isinstance(s, str):
            return False
        m = re.search(r"(\d{3}-\d{3})", s)
        if not m:
            return False
        node = REG.get(m.group(1))
        if node is None or (vol and node.get("volume") != vol):
            return False
        blob = (node.get("title") or "") + (node.get("original") or "")
        return any(c in blob for c in _probes(p["org_name"]))

    for f in SRC_FIELDS:
        if p.get(f) and not valid(p[f]):
            p[f] = VOL_HEADER.get(vol, "") if vol else ""
            fixed_src += 1
    # source 优先取沿革本传，其次取同卷有效出处
    if not valid(p.get("source")):
        p["source"] = p.get("history_source") or (VOL_HEADER.get(vol, "") if vol else "")
        fixed_src += 1

# ---------- 输出 ----------
out_path = os.path.join(LAYERS, "org_profiles.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(new_profiles, f, ensure_ascii=False, indent=2)

# ---------- 组织树输出 ----------
def build_tree(name):
    p = by_name[name]
    node = {
        "org_name": name,
        "rank": p.get("rank") or "",
        "category": p.get("category") or "",
        "volume": p.get("volume"),
        "source": p.get("source") or "",
        "children": [build_tree(c) for c in sorted(p.get("child_orgs", [])) if c in by_name],
    }
    return node

ROOT_ORDER = ["宗人府", "吏部", "户部", "礼部", "兵部", "刑部", "工部", "都察院",
              "通政使司", "大理寺", "太常寺", "詹事府", "光禄寺", "鸿胪寺", "太仆寺",
              "国子监", "翰林院", "尚宝司", "钦天监", "太医院", "上林苑监", "僧录司",
              "道录司", "五军都督府", "锦衣卫", "内府二十四衙门",
              "吏科", "户科", "礼科", "兵科", "刑科", "工科", "中书科", "五城兵马司"]
tree_roots = [r for r in ROOT_ORDER if r in by_name]
tree = {"roots": [build_tree(r) for r in tree_roots],
        "total_orgs": len(new_profiles), "total_roots": len(tree_roots)}
with open(os.path.join(LAYERS, "org_tree.json"), "w", encoding="utf-8") as f:
    json.dump(tree, f, ensure_ascii=False, indent=2)

# 可读 Markdown
lines = ["# 明会典·衙门组织树", "",
         f"共 {len(new_profiles)} 个衙门，{len(tree_roots)} 个顶层机构。", ""]
def dump_md(name, depth):
    p = by_name[name]
    rk = p.get("rank") or "—"
    vl = f"〔卷{p.get('volume')}〕" if p.get("volume") else ""
    src = f" `{p.get('source')}`" if p.get("source") else ""
    lines.append("  " * depth + f"- **{name}**（{rk}）{vl}{src}")
    for c in sorted(p.get("child_orgs", [])):
        if c in by_name:
            dump_md(c, depth + 1)
for r in tree_roots:
    dump_md(r, 0)
    lines.append("")
with open(os.path.join(LAYERS, "org_tree.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

# ---------- 统计 ----------
cats = defaultdict(int)
for p in new_profiles:
    cats[p.get("category")] += 1
roots = [p["org_name"] for p in new_profiles if not p.get("parent_org")]
with_hist = sum(1 for p in new_profiles if p.get("history"))
with_duty = sum(1 for p in new_profiles if p.get("duties"))
with_rank = sum(1 for p in new_profiles if p.get("rank"))
with_src = sum(1 for p in new_profiles if p.get("source") or p.get("history_source"))

print("=" * 64)
print(f"org_profiles: {len(OLD)} -> {len(new_profiles)}  (新增 {added} / 补全 {updated})")
print(f"含 history: {with_hist} | 含 duties: {with_duty} | 含 rank: {with_rank} | 含出处: {with_src}")
print(f"顶层衙门(roots): {len(roots)}")
print(f"悬空 parent: {len(dangling)} -> {dangling}")
print(f"修复陈旧 source 字段: {fixed_src}")
print("分类分布:", dict(cats))
print("=" * 64)

# 输出树
def tree(name, depth=0, out=None):
    out = out if out is not None else []
    p = by_name[name]
    out.append("  " * depth + f"{name}（{p.get('rank') or '—'}）")
    for c in sorted(p.get("child_orgs", [])):
        tree(c, depth + 1, out)
    return out

print("\n===== 六部/寺监 部→司→科 树（节选） =====")
for r in ["吏部", "户部", "礼部", "兵部", "刑部", "工部", "都察院", "光禄寺", "太医院", "上林苑监", "五军都督府"]:
    if r in by_name:
        print("\n".join(tree(r)))
        print()
