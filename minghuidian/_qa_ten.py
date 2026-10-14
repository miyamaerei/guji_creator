# -*- coding: utf-8 -*-
"""Q1–Q10 十问可答性探针：逐题取数作答，供质量评估。"""
import json, re
from collections import defaultdict, Counter

L = lambda n: json.load(open(f"_layers/{n}.json", encoding="utf-8"))
reg = json.load(open("_item_registry.json", encoding="utf-8"))
tags = L("domain_tags")
geo = L("geo"); rank = L("rank"); njc = L("njc"); xref = L("xref")
tim = L("tim"); rules = L("rules"); cits = L("cits")
offices = L("office_profiles"); orgs = L("org_profiles")
join = json.load(open("_kg_join.json", encoding="utf-8"))

print("=" * 82)
print("Q1 制度因革链（漕运 洪武→弘治）")
print("=" * 82)
hit = [t for t in tags if "漕运" in (t.get("title") or "") or "漕运" in json.dumps(t, ensure_ascii=False)]
print(f"domain_tags 命中 {len(hit)} 条；tim 层主题示例：")
print("  tim topics:", [t["topic"] for t in tim[:8]])
# 从 rules 找漕运 era
cy = [r for r in rules if "漕运" in (r.get("original") or "") or "漕运" in (r.get("subject") or "")]
print(f"rules 含「漕运」{len(cy)} 条；带 era 的 {sum(1 for r in cy if r.get('era'))} 条")
for r in cy[:5]:
    print(f"  {r['item_id']} era={r.get('era')} | {(r.get('original') or '')[:60]}")

print()
print("=" * 82)
print("Q2 一条「凡…」事例的完整要素")
print("=" * 82)
r = next((x for x in rules if x.get("condition") and x.get("era")), rules[0])
print(json.dumps({k: r.get(k) for k in
      ("item_id","type","subject","action","condition","era","event_types","subject_org_id","original")},
      ensure_ascii=False, indent=1)[:700])

print()
print("=" * 82)
print("Q3 六部各司职掌边界 / 见某司")
print("=" * 82)
print(f"xref 198 条；「见某司」示例（含 target_org）：")
for x in [x for x in xref if x["ref_type"] == "见某司" and x.get("target_org")][:6]:
    print(f"  {x['from_item']} 「{x['target']}」-> {x['target_org']}")

print()
print("=" * 82)
print("Q4 某官职完整档案（如「户部尚书」）")
print("=" * 82)
o = next((x for x in offices if "尚书" in x["office_name"] and x.get("system") == "文职"), offices[0])
print(json.dumps({k: o.get(k) for k in
      ("office_name","rank","system","headcount","duties","location","parent_org","salary","child_offices")},
      ensure_ascii=False, indent=1)[:700])

print()
print("=" * 82)
print("Q5 两京差异")
print("=" * 82)
print(f"NJC 38 条（机构对照 33 / 制度差异 4 / 凡例 1）")
for n in [n for n in njc if n["type"] == "机构对照"][:5]:
    print(f"  {n['topic']}: 京={n.get('beijing')} 南={n.get('nanjing')} | {str(n.get('difference'))[:45]}")

print()
print("=" * 82)
print("Q6 一地全景（苏州府：属县/卫所/驿站/仓场）")
print("=" * 82)
by_id = {g["geo_id"]: g for g in geo}
kids = defaultdict(list)
for g in geo:
    if g.get("parent_id"):
        kids[g["parent_id"]].append(g)
sz = [g for g in geo if g["name"] == "苏州府"]
if sz:
    s = sz[0]
    print("  苏州府下级:", [c["name"] for c in kids[s["geo_id"]]])
    print("  garrisons/post_stations/granaries 字段:", s.get("garrisons"), s.get("post_stations"), s.get("granaries"))

print()
print("=" * 82)
print("Q7 品级→章服→车舆→房舍（三品 vs 七品 对比）")
print("=" * 82)
for lv in ("三品", "七品"):
    r = next((x for x in rank if x["level"] == lv), None)
    if r:
        print(f"  {lv}: 常服={json.dumps(r.get('changfu'),ensure_ascii=False)[:70]}")
        print(f"        房舍={str(r.get('housing'))[:55]}")

print()
print("=" * 82)
print("Q8 数字则例（夏税秋粮/盐引 数额）")
print("=" * 82)
fin = [t for t in tags if t.get("domain") == "FIN"]
print(f"FIN 类条目 {len(fin)} 条；materials 60 条；含具体数额的 tag 示例：")
for t in fin[:4]:
    print(f"  {t['item_id']} 卷{t['volume']} [{t.get('sublayer')}] {t.get('title','')[:45]}")

print()
print("=" * 82)
print("Q9 出处溯源（CIT）")
print("=" * 82)
print(f"cits 97 条，cited_work 分布：", Counter(c["cited_work"] for c in cits).most_common(8))

print()
print("=" * 82)
print("Q10 一条事例牵涉的实体反查")
print("=" * 82)
j = join[0] if isinstance(join, list) else list(join.values())[0]
print("join 记录键:", list(j.keys())[:20])
