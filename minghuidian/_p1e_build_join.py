# -*- coding: utf-8 -*-
"""
P1-E: 校验 + 跨层整合重建 + 报告。

  1) 修正 domain_tags 的 group/volume（P0 重建后卷号已变动）。
  2) 重建 _kg_join.json / _kg_join_flat.csv：条目 × 全部子层（含新 TIM/laws/orgs）。
  3) 参照完整性校验（各层 item_id 是否都能在底座找到）。
  4) 输出 P1 完成报告所需统计。
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


# ---------- 1) 修正 domain_tags ----------
dt = load("domain_tags")
fixed_dt = 0
for d in dt:
    vol = d.get("volume")
    if not isinstance(vol, int):
        vol = int(str(d.get("item_id", "0-0")).split("-")[0])
        d["volume"] = vol
    g = VOL2GROUP.get(vol, "")
    if d.get("group") != g:
        d["group"] = g
        fixed_dt += 1

# 1b) 补齐 P0 新增条目（P0 重建后 2238 条无 domain 标注）
have = {d["item_id"] for d in dt}
vol_dom = defaultdict(Counter)
vol_sub = defaultdict(Counter)
for d in dt:
    vol_dom[d["volume"]][d.get("domain")] += 1
    vol_sub[d["volume"]][d.get("sublayer")] += 1
added_dt = 0
for iid, it in reg.items():
    if iid in have:
        continue
    vol = it.get("volume") or int(iid.split("-")[0])
    dom = vol_dom[vol].most_common(1)[0][0] if vol_dom[vol] else "ORG"
    sub = vol_sub[vol].most_common(1)[0][0] if vol_sub[vol] else dom + "-OTHER"
    dt.append({"item_id": iid, "volume": vol, "group": VOL2GROUP.get(vol, ""),
               "domain": dom, "sublayer": sub, "title": (it.get("title") or "")[:60],
               "_filled": True})
    added_dt += 1
dt.sort(key=lambda x: x["item_id"])
# 去重（原始 domain_tags 存在重复 item_id）
_seen, _dedup = set(), []
for d in dt:
    if d["item_id"] in _seen:
        continue
    _seen.add(d["item_id"])
    _dedup.append(d)
dt = _dedup
json.dump(dt, open(os.path.join(LAYERS, "domain_tags.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# ---------- 2) 加载各层 ----------
L = {n: load(n) for n in ["ents", "rules", "nams", "cits", "laws", "inspect",
                          "rituals", "dress", "foreign", "materials", "eng_tags",
                          "person_profiles", "process_profiles"]}
org_profiles = load("org_profiles")

# 衙门名索引（用于条目→衙门反查）
ORG_NAMES = sorted({p["org_name"] for p in org_profiles}, key=len, reverse=True)
ORG_BLACK = {"群", "司务厅", "照磨所", "经历司", "检校", "巡检司", "牧监", "税课司局",
             "河泊所", "批验所", "都指挥使司", "卫指挥使司", "千户所", "百户所",
             "提刑按察使司", "各祠祭署", "五官正", "太医院十三科"}

# ---------- 3) 构建 join ----------
join = {}
for iid, it in reg.items():
    vol = it.get("volume") or int(iid.split("-")[0])
    join[iid] = {
        "item_id": iid, "volume": vol, "group": VOL2GROUP.get(vol, ""),
        "node_kind": it.get("node_kind", ""), "section": it.get("section", ""),
        "title": (it.get("title") or "")[:60],
        "rules": [], "ents": [], "nams": [], "cits": [], "laws": [], "inspect": [],
        "rituals": [], "dress": [], "foreign": [], "materials": [], "eng": [],
        "offices": [], "process": [], "orgs": [], "layer_count": 0,
    }

def add(layer_key, iid, rec):
    if iid in join:
        join[iid][layer_key].append(rec)

for r in L["rules"]:
    add("rules", r.get("item_id"), {"rule_id": r.get("id") or r.get("rule_id", ""), "type": r.get("type", ""),
                  "subject": r.get("subject", ""), "era": r.get("era", ""),
                  "event_types": r.get("event_types", [])})
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
    add("process", x.get("item_id"), {"process_name": x.get("process_name", ""), "process_type": x.get("process_type", "")})

# 条目 → 衙门 反查
for iid, it in reg.items():
    blob = (it.get("title") or "") + (it.get("original") or "")
    hit = [o for o in ORG_NAMES if o not in ORG_BLACK and o in blob]
    join[iid]["orgs"] = hit[:20]

# layer_count
BUCKETS = ["rules", "ents", "nams", "cits", "laws", "inspect", "rituals", "dress",
           "foreign", "materials", "eng", "offices", "process", "orgs"]
for j in join.values():
    j["layer_count"] = sum(1 for b in BUCKETS if j[b])

join_list = sorted(join.values(), key=lambda x: x["item_id"])
json.dump(join_list, open(os.path.join(ROOT, "_kg_join.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

with open(os.path.join(ROOT, "_kg_join_flat.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["item_id", "volume", "group", "node_kind", "section", "title", "layer_count",
                "rules", "ents", "nams", "cits", "laws", "inspect", "rituals", "dress",
                "foreign", "materials", "eng", "offices", "process", "orgs"])
    for j in join_list:
        w.writerow([j["item_id"], j["volume"], j["group"], j["node_kind"], j["section"], j["title"],
                    j["layer_count"]] + [len(j[b]) for b in BUCKETS])

# ---------- 4) 校验 ----------
print("=" * 66)
print("P1-E 校验")
print("=" * 66)
print(f"底座条目: {len(reg)}  |  join 条目: {len(join_list)}")
print(f"domain_tags: {len(dt)} 条（group 修正 {fixed_dt}，补齐 {added_dt}）")

# 参照完整性
dangling = {}
for name, recs in L.items():
    bad = 0
    for r in recs:
        iid = r.get("item_id")
        if iid and iid not in reg:
            bad += 1
    if bad:
        dangling[name] = bad
print(f"悬空 item_id 引用: {dangling if dangling else '无'}")

# 分层覆盖
print("\n子层规模与条目覆盖:")
for name, recs in L.items():
    ids = {r.get("item_id") for r in recs if r.get("item_id")}
    print(f"  {name:18s} 记录 {len(recs):6d} | 覆盖条目 {len(ids):6d}")
print(f"  {'org_profiles':18s} 记录 {len(org_profiles):6d}")

lc = Counter(j["layer_count"] for j in join_list)
print("\n跨层分布:")
for k in sorted(lc):
    print(f"  {k} 层: {lc[k]:6d} 条")
multi = sum(v for k, v in lc.items() if k >= 2)
print(f"\n多层覆盖(≥2层): {multi} 条 ({multi*100//len(join_list)}%)")

# 每卷多层率
vol_multi = defaultdict(lambda: [0, 0])
for j in join_list:
    v = j["volume"]
    vol_multi[v][1] += 1
    if j["layer_count"] >= 2:
        vol_multi[v][0] += 1
worst = sorted(vol_multi.items(), key=lambda x: (x[1][0] / x[1][1] if x[1][1] else 1))[:8]
print("\n多层覆盖率最低的 8 卷:")
for v, (m, t) in worst:
    print(f"  卷{v:3d}: {m}/{t} = {m*100//max(t,1)}%")
