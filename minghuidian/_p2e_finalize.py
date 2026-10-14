# -*- coding: utf-8 -*-
"""
P2-E: 四新层（RANK/NJC/XREF/GEO）校验 + 跨层整合重建 + P2 报告统计。

  1) 加载全部子层（含 P2 新增 rank/njc/xref/geo）。
  2) 重建 _kg_join.json / _kg_join_flat.csv：条目 × 全部子层。
  3) 参照完整性校验：各层 item_id / parent_id / 目标衙门。
  4) 输出 P2 完成报告所需统计。
"""
import json, os, csv
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")

reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

VOL2GROUP = {1: "G0 宗人府"}
for v in range(2, 16):   VOL2GROUP[v] = "G1 吏部"
for v in range(16, 42):  VOL2GROUP[v] = "G2 户部"
for v in range(42, 106): VOL2GROUP[v] = "G3 礼部"
for v in range(106, 130):VOL2GROUP[v] = "G4 兵部"
for v in range(130, 144):VOL2GROUP[v] = "G5 刑部"
for v in range(144, 164):VOL2GROUP[v] = "G6 工部"
for v in range(164, 179):VOL2GROUP[v] = "G7 诸文职"
for v in range(179, 181):VOL2GROUP[v] = "G8 诸武职"


def load(name):
    p = os.path.join(LAYERS, name + ".json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


# ---------- 0) 修正 domain_tags ----------
dt = load("domain_tags")
for d in dt:
    vol = d.get("volume")
    if not isinstance(vol, int):
        vol = int(str(d.get("item_id", "0-0")).split("-")[0])
        d["volume"] = vol
    d["group"] = VOL2GROUP.get(vol, "")
have = {d["item_id"] for d in dt}
vol_dom, vol_sub = defaultdict(Counter), defaultdict(Counter)
for d in dt:
    vol_dom[d["volume"]][d.get("domain")] += 1
    vol_sub[d["volume"]][d.get("sublayer")] += 1
for iid, it in reg.items():
    if iid in have:
        continue
    vol = it.get("volume") or int(iid.split("-")[0])
    dom = vol_dom[vol].most_common(1)[0][0] if vol_dom[vol] else "ORG"
    sub = vol_sub[vol].most_common(1)[0][0] if vol_sub[vol] else dom + "-OTHER"
    dt.append({"item_id": iid, "volume": vol, "group": VOL2GROUP.get(vol, ""),
               "domain": dom, "sublayer": sub, "title": (it.get("title") or "")[:60],
               "_filled": True})
dt.sort(key=lambda x: x["item_id"])
_seen, _dedup = set(), []
for d in dt:
    if d["item_id"] in _seen:
        continue
    _seen.add(d["item_id"])
    _dedup.append(d)
dt = _dedup
json.dump(dt, open(os.path.join(LAYERS, "domain_tags.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ---------- 1) 加载各层 ----------
OLD = ["ents", "rules", "nams", "cits", "laws", "inspect", "rituals", "dress",
       "foreign", "materials", "eng_tags", "person_profiles", "process_profiles"]
NEW = ["rank", "njc", "xref", "geo", "num", "reports", "objs"]
L = {n: load(n) for n in OLD + NEW}
org_profiles = load("org_profiles")

ORG_NAMES = sorted({p["org_name"] for p in org_profiles}, key=len, reverse=True)
ORG_BLACK = {"群", "司务厅", "照磨所", "经历司", "检校", "巡检司", "牧监", "税课司局",
             "河泊所", "批验所", "都指挥使司", "卫指挥使司", "千户所", "百户所",
             "提刑按察使司", "各祠祭署", "五官正", "太医院十三科"}

# ---------- 2) 构建 join ----------
BUCKETS = ["rules", "ents", "nams", "cits", "laws", "inspect", "rituals", "dress",
           "foreign", "materials", "eng", "offices", "process", "orgs",
           "rank", "njc", "xref", "geo", "num", "reports", "objs"]

join = {}
for iid, it in reg.items():
    vol = it.get("volume") or int(iid.split("-")[0])
    j = {"item_id": iid, "volume": vol, "group": VOL2GROUP.get(vol, ""),
         "node_kind": it.get("node_kind", ""), "section": it.get("section", ""),
         "title": (it.get("title") or "")[:60], "layer_count": 0}
    for b in BUCKETS:
        j[b] = []
    join[iid] = j


def add(key, iid, rec):
    if iid and iid in join:
        join[iid][key].append(rec)


for r in L["rules"]:
    add("rules", r.get("item_id"), {"rule_id": r.get("id") or r.get("rule_id", ""),
                                    "type": r.get("type", ""), "subject": r.get("subject", ""),
                                    "era": r.get("era", ""), "event_types": r.get("event_types", [])})
for e in L["ents"]:
    add("ents", e.get("item_id"), {"text": e.get("text", ""), "type": e.get("type", "")})
for n in L["nams"]:
    add("nams", n.get("item_id"), {"nam_type": n.get("nam_type", ""), "name": n.get("name", "")})
for c in L["cits"]:
    add("cits", c.get("item_id"), {"cited_work": c.get("cited_work", "")})
for x in L["laws"]:
    add("laws", x.get("item_id"), {"crime": x.get("crime", ""), "punishment_type": x.get("punishment_type", "")})
for x in L["inspect"]:
    add("inspect", x.get("item_id"), {"affair_type": x.get("affair_type", ""), "name": x.get("name", "")})
for x in L["rituals"]:
    add("rituals", x.get("item_id"), {"ritual_type": x.get("ritual_type", ""), "ritual_name": x.get("ritual_name", "")})
for x in L["dress"]:
    add("dress", x.get("item_id"), {"category": x.get("category", ""), "name": x.get("name", "")})
for x in L["foreign"]:
    add("foreign", x.get("item_id"), {"type": x.get("type", ""), "name": x.get("name", "")})
for x in L["materials"]:
    add("materials", x.get("item_id"), {"material": x.get("material", ""), "quantity": x.get("quantity", ""),
                                        "unit": x.get("unit", "")})
for x in L["eng_tags"]:
    add("eng", x.get("item_id"), {"sublayer": x.get("sublayer", ""), "title": x.get("title", "")})
for x in L["person_profiles"]:
    add("offices", x.get("item_id"), {"office_name": x.get("office_name", "")})
for x in L["process_profiles"]:
    add("process", x.get("item_id"), {"process_name": x.get("process_name", ""),
                                      "process_type": x.get("process_type", "")})

# ---- P2 新增四层 ----
for r in L["rank"]:                                   # 品级 → 条目（sources: {类别: item_id}）
    for cat, iid in (r.get("sources") or {}).items():
        add("rank", iid, {"rank_id": r.get("rank_id"), "level": r.get("level"),
                          "category": r.get("category"), "cat": cat})
for x in L["njc"]:                                    # 两京对照（京/南京/凡例 三向挂载）
    for key, role in (("beijing_item", "北京"), ("nanjing_item", "南京"), ("source_item", "凡例")):
        add("njc", x.get(key), {"njc_id": x.get("njc_id"), "type": x.get("type"),
                                "topic": x.get("topic"), "role": role})
for x in L["xref"]:                                   # 互见
    add("xref", x.get("from_item"), {"xref_id": x.get("xref_id"), "ref_type": x.get("ref_type"),
                                     "target": x.get("target"), "target_org": x.get("target_org", "")})
for x in L["geo"]:                                    # 地理（每名录行可含多个地名，截断 60）
    if len(join.get(x.get("item_id"), {}).get("geo", [])) < 60:
        add("geo", x.get("item_id"), {"geo_id": x.get("geo_id"), "name": x.get("name"),
                                      "type": x.get("type"), "level": x.get("level")})

# ---- P3 新增三层 ----
for x in L["num"]:                                    # 数字则例
    add("num", x.get("item_id"), {"num_id": x.get("num_id"), "subject": x.get("subject"),
                                  "quantity": x.get("quantity"), "unit": x.get("unit"),
                                  "category": x.get("category")})
for x in L["reports"]:                                # 文册·勘合
    add("reports", x.get("item_id"), {"rep_id": x.get("rep_id"), "doc_name": x.get("doc_name"),
                                      "doc_category": x.get("doc_category")})
for x in L["objs"]:                                   # 器物
    add("objs", x.get("item_id"), {"obj_id": x.get("obj_id"), "obj_name": x.get("obj_name"),
                                   "obj_category": x.get("obj_category")})

# 条目 → 衙门 反查
for iid, it in reg.items():
    blob = (it.get("title") or "") + (it.get("original") or "")
    join[iid]["orgs"] = [o for o in ORG_NAMES if o not in ORG_BLACK and o in blob][:20]

for j in join.values():
    j["layer_count"] = sum(1 for b in BUCKETS if j[b])

join_list = sorted(join.values(), key=lambda x: x["item_id"])
json.dump(join_list, open(os.path.join(ROOT, "_kg_join.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

with open(os.path.join(ROOT, "_kg_join_flat.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item_id", "volume", "group", "node_kind", "section", "title", "layer_count"] + BUCKETS)
    for j in join_list:
        w.writerow([j["item_id"], j["volume"], j["group"], j["node_kind"], j["section"],
                    j["title"], j["layer_count"]] + [len(j[b]) for b in BUCKETS])

# ---------- 3) 校验 ----------
print("=" * 68)
print("P2-E 校验：四新层 + 跨层整合")
print("=" * 68)
print(f"底座条目 {len(reg)}  |  join 条目 {len(join_list)}  |  domain_tags {len(dt)}")

print("\n[1] 参照完整性（item_id 是否都能在底座找到）")
for name, recs in L.items():
    ids = [r.get("item_id") or r.get("from_item") or r.get("beijing_item")
           for r in recs]
    bad = sum(1 for i in ids if i and i not in reg)
    mark = "OK" if bad == 0 else f"!! {bad} 悬空"
    print(f"  {name:18s} 记录 {len(recs):6d} | {mark}")

print("\n[2] 各层内部一致性")
geo = L["geo"]
gids = {g["geo_id"] for g in geo}
dangling_p = [g["geo_id"] for g in geo if g["parent_id"] and g["parent_id"] not in gids]
roots = [g["name"] for g in geo if not g["parent_id"]]
print(f"  geo   : {len(geo)} 节点，根 {len(roots)}，parent_id 悬空 {len(dangling_p)}")
lv = Counter(g["level"] for g in geo)
print(f"         层级: {dict(lv)}")
rank = L["rank"]
print(f"  rank  : {len(rank)} 条，品级 {len({r['level'] for r in rank})} 种"
      f"（{[r['level'] for r in rank[:15]]}…）")
njc = L["njc"]
print(f"  njc   : {len(njc)} 条，type {dict(Counter(x['type'] for x in njc))}")
xref = L["xref"]
print(f"  xref  : {len(xref)} 条，ref_type {dict(Counter(x['ref_type'] for x in xref))}，"
      f"含 target_org {sum(1 for x in xref if x.get('target_org'))}")

print("\n[3] 跨层：新层与条目/衙门的挂接")
for key in ("rank", "njc", "xref", "geo"):
    items = [j for j in join_list if j[key]]
    print(f"  {key:5s}: 命中条目 {len(items):5d}  |  "
          f"示例 {items[0]['item_id'] if items else '—'}")
xr_org = [x for x in xref if x.get("target_org")]
hit = sum(1 for x in xr_org if x["target_org"] in set(ORG_NAMES))
print(f"  xref.target_org 指向已收录衙门: {hit}/{len(xr_org)}")

print("\n[4] 跨层分布（layer_count）")
lc = Counter(j["layer_count"] for j in join_list)
for k in sorted(lc):
    print(f"  {k:2d} 层: {lc[k]:6d}")
multi = sum(v for k, v in lc.items() if k >= 2)
print(f"  多层覆盖(≥2层): {multi} 条 ({multi * 100 // len(join_list)}%)")

print("\n[5] QC 目标")
print(f"  NJC 条目数 ≥30  ->  {len(njc)}  {'达标' if len(njc) >= 30 else '未达标'}")
print(f"  GEO 省级 15      ->  {lv.get('省', 0)}")
print(f"  RANK 覆盖 公侯伯…九品 -> {len(rank)}")

json.dump({"geo_levels": dict(lv), "njc_types": dict(Counter(x["type"] for x in njc)),
           "xref_types": dict(Counter(x["ref_type"] for x in xref)),
           "layer_count": {str(k): v for k, v in lc.items()}},
          open(os.path.join(ROOT, "_p2_stats.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\n统计已写入 _p2_stats.json")
