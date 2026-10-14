# -*- coding: utf-8 -*-
"""P2.5-A: 驿站/递运所/仓场并入 GEO（Q6「一地设哪些驿站、有哪些仓场」）。

三类名目格式一致：**地名在前、设施名在后**（表格拍平后可能跨行），
故统一用 leftmost-longest 扫描 + `last_place` 游标：
  地名（府/州/县/卫/所/都司/布政司/长官司…）→ 更新游标
  设施名（驿/递运所/仓）→ 挂到当前游标
源：驿站=卷119(119-020起)+卷120；递运所=卷121(121-006起)；仓场=卷39+卷40。
"""
import json, re, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
geo = json.load(open(os.path.join(ROOT, "_layers/geo.json"), encoding="utf-8"))

# 幂等：先剥离上一次生成的 驿/递运所/仓 节点，并清空挂载字段
STATION_TYPES = {"驿", "递运所", "仓"}
geo = [g for g in geo if g.get("type") not in STATION_TYPES]
for g in geo:
    g["post_stations"] = []
    g["granaries"] = []

PUA = {0xE5AB: "隶", 0xEA1F: "弘", 0xF5F6: "封", 0xEB08: "卷", 0xE205: "笙", 0xE6A2: "雨"}


def nz(t):
    return "".join(PUA.get(ord(c), c) for c in t)


VAR = str.maketrans("蘓呉髙徳寳峯鎭鳯頴澂栁亰衞廵闗畨邉槀", "苏吴高德宝峰镇凤颍澄柳京卫巡关番边藁")


def nv(s):
    return s.translate(VAR)


by_name = defaultdict(list)
by_name_norm = defaultdict(list)
for g in geo:
    by_name[g["name"]].append(g)
    by_name_norm[nv(g["name"])].append(g)
gidx = max(int(g["geo_id"].split("-")[1]) for g in geo)


def resolve(name):
    """地名 → GEO 节点（原名 / OCR 变体 / 补后缀）。"""
    if not name:
        return None
    for cand in (name, nv(name)):
        if cand in by_name:
            return by_name[cand][0]
        if cand in by_name_norm:
            return by_name_norm[cand][0]
    # 补后缀（如「济南」→「济南府」）
    for suf in ("府", "州", "县", "卫", "所", "都司", "布政使司", "布政司",
                "都指挥使司", "留守司", "军民指挥使司", "宣慰使司", "长官司", "指挥使司"):
        c = name + suf
        if c in by_name:
            return by_name[c][0]
        if nv(c) in by_name_norm:
            return by_name_norm[nv(c)][0]
    # 去尾字再补（如「苏州府」误作「蘓州」）
    if len(name) >= 2:
        for suf in ("府", "州", "县", "卫", "所"):
            c = name[:-1] + suf
            if c in by_name:
                return by_name[c][0]
            if nv(c) in by_name_norm:
                return by_name_norm[nv(c)][0]
    return None


def add_node(name, ntype, parent, item_id, original):
    global gidx
    gidx += 1
    rec = {"geo_id": f"GEO-{gidx:04d}", "name": nv(name), "type": ntype,
           "parent": parent["name"] if parent else "", "parent_id": parent["geo_id"] if parent else "",
           "children": [], "level": ntype,
           "administered_by": parent["name"] if parent else "",
           "garrisons": [], "post_stations": [], "granaries": [],
           "volume": reg[item_id]["volume"], "item_id": item_id,
           "original": (original or "")[:120]}
    geo.append(rec)
    return rec


# ---------------- 通用扫描器 ----------------
PLACE_RX = re.compile(
    r"[\u4e00-\u9fff]{1,4}(?:军民指挥使司|卫指挥使司|都指挥使司|指挥使司|宣慰使司|招讨使司|"
    r"长官司|军民府|都司|布政使司|行都司|留守司|盐运使司|盐运司|千户所|守御所|府|州|县|卫|所)")
REGION_RX = re.compile(r"(北直隶|南直隶|[\u4e00-\u9fff]{2,4}布政使司|[\u4e00-\u9fff]{2,4}都司|辽东都司)")
YI_RX = re.compile(r"[\u4e00-\u9fff]{2,5}(?:水马驿|马驿|水驿|驿)")
DY_RX = re.compile(r"[\u4e00-\u9fff]{2,4}(?:递运所)")
CANG_RX = re.compile(r"[\u4e00-\u9fff]{2,5}仓")


def scan_links(items, item_rx, node_type, field, seed_place=None, skip_exact=()):
    """items: [(k,v)]；返回 (抽取数, 挂靠数, 节点dict)。逐字符记录来源条目，保证溯源。"""
    parts, owner = [], []
    for k, v in items:
        if v.get("node_kind") == "事例":
            continue
        s = nz(v.get("original") or "")
        parts.append(s)
        owner.extend([k] * len(s))
        parts.append("\u3000")
        owner.append(k)
    stream = "".join(parts)
    total = linked = 0
    nodes = {}
    last_place = seed_place
    i, n = 0, len(stream)
    while i < n:
        # 优先取设施名：同一位置若设施名命中，说明其后紧跟的是新地名，
        # 绝不能让 PLACE_RX 向前吞掉设施名（如「安庄驿贵州」）。
        m = item_rx.match(stream, i)
        if m:
            best = ("item", m.group(0))
        else:
            best = None
            for typ, rx in (("region", REGION_RX), ("place", PLACE_RX)):
                mm = rx.match(stream, i)
                if mm and (best is None or len(mm.group(0)) > len(best[1])):
                    best = (typ, mm.group(0))
        if not best:
            i += 1
            continue
        typ, name = best
        src_id = owner[i] if i < len(owner) else items[0][0]
        i += len(name)
        if typ == "region":
            last_place = name
        elif typ == "place":
            last_place = name
        else:
            if name in skip_exact or name.endswith(("本县马驿",)):
                continue
            total += 1
            tgt = resolve(last_place)
            if tgt is None:
                continue
            if name not in nodes:
                nodes[name] = add_node(name, node_type, tgt, src_id, name)
            if nv(name) not in tgt.setdefault(field, []):
                tgt[field].append(nv(name))
            linked += 1
    return total, linked, nodes


# 卷119 名目自 119-020 起；卷120 全卷；卷121 名目自 121-006 起
station_items = sorted([(k, v) for k, v in reg.items()
                        if (v["volume"] == 119 and k >= "119-020") or v["volume"] == 120])
diyun_items = sorted((k, v) for k, v in reg.items() if v["volume"] == 121 and k >= "121-006")

t1, l1, nd1 = scan_links(station_items, YI_RX, "驿", "post_stations", skip_exact=("计天下水马驿",))
t2, l2, nd2 = scan_links(diyun_items, DY_RX, "递运所", "post_stations", skip_exact=("计天下递运所",))
print(f"[驿站] 抽取 {t1}，挂靠 {l1} = {l1/max(t1,1)*100:.1f}%；驿节点 {len(nd1)}")
print(f"[递运所] 抽取 {t2}，挂靠 {l2} = {l2/max(t2,1)*100:.1f}%；递运所节点 {len(nd2)}")

# ---------------- 仓场（卷39 京仓 + 卷40 各省仓） ----------------
# 剔除政策/凡例长文（如「国家仓庾之设徧于天下…」「…大使…攒典…」），避免误抽「国家仓」
NOISE = ("徧", "攒典", "大使", "斗级", "具列于后", "不备録")
cang_items = sorted([(k, v) for k, v in reg.items() if v["volume"] in (39, 40)
                     and not any(w in nz(v.get("original") or "") for w in NOISE)])
t3, l3, nd3 = scan_links(cang_items, CANG_RX, "仓", "granaries", seed_place="顺天府")
print(f"[仓场] 抽取 {t3}，挂靠 {l3} = {l3/max(t3,1)*100:.1f}%；仓节点 {len(nd3)}")

json.dump(geo, open(os.path.join(ROOT, "_layers/geo.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
n_ps = sum(1 for g in geo if g.get("post_stations"))
n_gr = sum(1 for g in geo if g.get("granaries"))
print(f"GEO 总节点 {len(geo)}；有驿站 {n_ps}；有仓场 {n_gr}")
