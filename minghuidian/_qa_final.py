# -*- coding: utf-8 -*-
"""P2.5/P3/P1 收尾后：Q1–Q10 十问可答性复测（逐题取数作答）。"""
import json
from collections import Counter, defaultdict

L = lambda n: json.load(open(f"_layers/{n}.json", encoding="utf-8"))
geo = L("geo"); rank = L("rank"); njc = L("njc"); xref = L("xref"); tim = L("tim")
rules = L("rules"); cits = L("cits"); num = L("num"); reps = L("reports"); objs = L("objs")
offices = L("office_profiles"); tags = L("domain_tags")
join = json.load(open("_kg_join.json", encoding="utf-8"))
PUA = {0xE5AB: "隶", 0xEA1F: "弘", 0xF5F6: "封", 0xEB08: "卷"}


def nz(t):
    return "".join(PUA.get(ord(c), c) for c in t)


def H(t):
    print("\n" + "=" * 80 + f"\n{t}\n" + "=" * 80)


H("Q1 制度因革链（漕运 洪武→弘治）")
cy = next((t for t in tim if t["theme"] == "漕运"), None)
print(f"TIM 制度主题 {len(tim)} 个：", [t["theme"] for t in tim])
if cy:
    print(f"漕运链：{cy['era_span']}，规则 {cy['rule_count']}，年号 {len(cy['era_chain'])}")
    for c in cy["era_chain"]:
        print(f"   {c['era']}（{c['count']}）事件={c['events']}")

H("Q2 一条「凡…」事例的完整要素")
full = [x for x in rules if x.get("condition") and x.get("punishment") and x.get("era")]
print(f"四要素齐全（subject/action/condition/punishment+era）的事例：{len(full)} 条")
r = full[0] if full else rules[0]
print(json.dumps({k: r.get(k) for k in ("item_id", "type", "subject", "action", "condition",
                                        "punishment", "punishment_level", "era")},
                 ensure_ascii=False, indent=1)[:600])

H("Q3 六部各司职掌边界 / 见某司")
print(f"xref {len(xref)} 条；「见某司」示例：")
for x in [x for x in xref if x["ref_type"] == "见某司" and x.get("target_org")][:5]:
    print(f"   {x['from_item']} 「{x['target']}」-> {x['target_org']}")

H("Q4 某官职完整档案")
o = next((x for x in offices if "尚书" in x["office_name"] and x.get("rank")), offices[0])
print(json.dumps({k: o.get(k) for k in ("office_name", "rank", "system", "headcount",
                                        "duties", "location", "parent_org", "salary")},
                 ensure_ascii=False, indent=1)[:600])

H("Q5 两京差异")
print(f"NJC {len(njc)} 条：", dict(Counter(x["type"] for x in njc)))
for n in [n for n in njc if n["type"] == "制度差异"][:5]:
    print(f"   [{n.get('subtype')}] {n['difference'][:52]}")

H("Q6 一地全景（苏州府 / 通州）")
for nm in ("苏州府", "通州"):
    for g in geo:
        if g["name"] == nm and g["type"] in ("府", "州"):
            ch = [x["name"] for x in geo if x.get("parent_id") == g["geo_id"]]
            print(f"   {nm}（{g['type']}）: 下级={ch[:8]}… 卫={g.get('garrisons')} "
                  f"驿={g.get('post_stations')} 仓={g.get('granaries')}")
            break

H("Q7 品级→章服→房舍（三品/七品）")
for lv in ("三品", "七品"):
    r = next((x for x in rank if x["level"] == lv), None)
    if r:
        print(f"   {lv}: 常服={str(r.get('changfu'))[:60]} 房舍={str(r.get('housing'))[:50]}")

H("Q8 数字则例（夏税/秋粮/盐课 数额）")
print(f"NUM 层 {len(num)} 条：", dict(Counter(x["category"] for x in num)))
for kw in ("夏税", "秋粮", "盐钞"):
    rs = [x for x in num if x["subject"] == kw]
    print(f"   {kw}: {len(rs)} 条，例：", [f"{x['quantity']}{x['unit']}" for x in rs[:4]])

H("Q9 出处溯源（CIT 部书 + REPORT 文册）")
print(f"CIT {len(cits)} 条，覆盖 {len({x['cited_work'] for x in cits})} 部书：",
      dict(Counter(x["cited_work"] for x in cits).most_common(8)))
print(f"REPORT {len(reps)} 条：", dict(Counter(x["doc_category"] for x in reps)))
print(f"OBJ 器物 {len(objs)} 条：", dict(Counter(x["obj_category"] for x in objs)))

H("Q10 一条事例牵涉的实体反查")
j = max(join, key=lambda x: x["layer_count"])
print(f"条目 {j['item_id']} 挂 {j['layer_count']} 子层：",
      [b for b in j if isinstance(j[b], list) and j[b]])
print("   rules:", j["rules"][:2])
print("   geo  :", j["geo"][:2])
print("   num  :", j["num"][:2])

H("汇总：各层规模")
for n in ("geo", "rank", "njc", "xref", "tim", "rules", "cits", "num", "reports", "objs",
          "office_profiles", "ents", "nams", "laws", "rituals", "dress", "materials"):
    print(f"   {n:18s} {len(L(n)):6d}")
