# -*- coding: utf-8 -*-
"""QA 探针：模拟研究者提问，直接从各层取数作答，检验可答性与答案质量。"""
import json, re, os
from collections import defaultdict, Counter

L = lambda n: json.load(open(f"_layers/{n}.json", encoding="utf-8"))
geo = L("geo"); rank = L("rank"); njc = L("njc"); xref = L("xref")
reg = json.load(open("_item_registry.json", encoding="utf-8"))
tags = L("domain_tags")

by_id = {g["geo_id"]: g for g in geo}
kids = defaultdict(list)
for g in geo:
    if g.get("parent_id"):
        kids[g["parent_id"]].append(g)


def find(name, typ=None):
    return [g for g in geo if g["name"] == name and (typ is None or g["type"] == typ)]


def show_tree(g, depth=0, maxd=3, out=None):
    out = out if out is not None else []
    out.append("  " * depth + f"{g['name']}（{g['type']}）")
    if depth < maxd:
        for c in sorted(kids.get(g["geo_id"], []), key=lambda x: x["name"]):
            show_tree(c, depth + 1, maxd, out)
    return out


Q = []
print("=" * 80)
print("【Q6 地理】浙江布政使司下辖几府？杭州府领州几、县几？")
print("=" * 80)
zj = find("浙江布政使司", "布政司")
if zj:
    z = zj[0]
    fz = [c for c in kids[z["geo_id"]] if c["type"] == "府"]
    print(f"答：浙江布政使司下辖 {len(fz)} 府：", "、".join(sorted(x["name"] for x in fz)))
    hz = find("杭州府")
    if hz:
        h = hz[0]
        cs = kids[h["geo_id"]]
        zs = [c for c in cs if c["type"] == "州"]
        xs = [c for c in cs if c["type"] == "县"]
        print(f"杭州府：属州 {len(zs)}、直辖县 {len(xs)}")
        print("  县：", "、".join(x["name"] for x in xs))
        for zz in zs:
            print(f"  {zz['name']} ->", [y["name"] for y in kids[zz["geo_id"]]])

print()
print("=" * 80)
print("【Q6 二级展开】济南府「领州四县二十六」，四州各辖何县？")
print("=" * 80)
jn = find("济南府")
if jn:
    j = jn[0]
    direct = [c["name"] for c in kids[j["geo_id"]] if c["type"] == "县"]
    zs = [c for c in kids[j["geo_id"]] if c["type"] == "州"]
    print(f"答：济南府直辖县 {len(direct)} 个：{'、'.join(direct)}")
    tot = len(direct)
    for z in zs:
        ys = [y["name"] for y in kids[z["geo_id"]]]
        tot += len(ys)
        print(f"  属州 {z['name']} 辖 {len(ys)} 县：{'、'.join(ys)}")
    print(f"  合计县 {tot}（原文声明 26）")

print()
print("=" * 80)
print("【Q7 品级】一品官的朝服/公服/房舍规格？")
print("=" * 80)
for r in rank:
    if r["level"] == "一品":
        print("答：")
        for k in ("chaofu", "gongfu", "changfu", "housing", "tableware", "umbrella", "carriage"):
            v = r.get(k)
            if v:
                print(f"  {k}: {json.dumps(v, ensure_ascii=False)[:150]}")
        print("  sources:", r.get("sources"))
        break

print()
print("=" * 80)
print("【Q5 两京】南京与北京有哪些机构差异？")
print("=" * 80)
jg = [n for n in njc if n["type"] == "机构对照"]
zd = [n for n in njc if n["type"] == "制度差异"]
print(f"答：机构对照 {len(jg)} 条、制度差异 {len(zd)} 条。示例：")
for n in jg[:6]:
    print(f"  · {n['topic']}：北京={n.get('beijing','-')} / 南京={n.get('nanjing','-')}"
          f"  差={str(n.get('difference',''))[:50]}")
for n in zd[:4]:
    print(f"  · [制度差异] {n['topic']}：{str(n.get('difference',''))[:70]}")

print()
print("=" * 80)
print("【Q3 互见】「见某司」类互见指向何处？（前 8 条）")
print("=" * 80)
for x in [x for x in xref if x["ref_type"] == "见某司"][:8]:
    print(f"  {x['from_item']} 「{x['target']}」 -> target_org={x.get('target_org') or '（未解析）'}"
          f"  | {x['original'][:50]}")

print()
print("=" * 80)
print("【Q4 六部业务】关于「逃军」的律例/事例有多少？")
print("=" * 80)
hit = [t for t in tags if "逃军" in json.dumps(t, ensure_ascii=False)]
print(f"答：domain_tags 命中 {len(hit)} 条")
for t in hit[:5]:
    print(f"  {t['item_id']} 卷{t['volume']} [{t.get('domain')}/{t.get('sublayer')}] {t.get('title','')[:40]}")

print()
print("=" * 80)
print("【Q2 沿革】「宗人府」的沿革（卷1 本衙门沿革）")
print("=" * 80)
for k, v in sorted(reg.items()):
    if v["volume"] == 1 and v.get("node_kind") == "沿革":
        print(f"  {k}: {(v.get('original') or '')[:200]}")
