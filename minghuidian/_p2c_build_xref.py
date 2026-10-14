# -*- coding: utf-8 -*-
"""
P2-C: 建 L3.XREF 互见层。

复原凡例所述「各以类书而总注其后曰已上某」的分组体系，以及正文中的互见与隶属变动：
  - 已上某    分组总注（如"已上皆东宫官""已上后俱革""已上皆南京"）
  - 见某司    互见（如"见验封司""见考功司""见于诸司"）
  - 今归某司  隶属变动（如"今归本司""今归并二仓"）
  - 旧隶/改隶 隶属变动（如"旧属南阳府""改隶兵部"）
  - 本司掌行  职掌归属
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT, "_layers")
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
org_names = sorted({p["org_name"] for p in json.load(open(os.path.join(LAYERS, "org_profiles.json"), encoding="utf-8"))},
                   key=len, reverse=True)

ORG_ALT = "|".join(re.escape(o) for o in org_names if len(o) >= 2 and o not in
                   {"群", "司务厅", "照磨所", "经历司", "检校", "巡检司", "牧监"})

PATTERNS = [
    ("已上某分组", re.compile(r"已上[\u4e00-\u9fff]{1,8}")),
    ("见某司",     re.compile(r"见(?:于)?(?:" + ORG_ALT + r"|诸司|本部|各[部司院寺])")),
    ("今归某司",   re.compile(r"今归(?:" + ORG_ALT + r"|本司|并[\u4e00-\u9fff]{2,6})")),
    ("隶属变动",   re.compile(r"(?:旧隶|旧属|先隶|原隶|改隶|改属|并入|归并)(?:" + ORG_ALT +
                              r"|[\u4e00-\u9fff]{2,6}(?:府|州|县|卫|所))")),
    ("本司掌行",   re.compile(r"本司掌行")),
]
# 仅这些类型需要挂衙门
ORG_TYPES = {"见某司", "今归某司", "隶属变动", "本司掌行"}

GEN_SKIP = {"今归圣主"}  # 诗词误匹配


def match_org(text):
    for o in org_names:
        if len(o) >= 2 and o in text:
            return o
    return ""


xref = []
seen = set()
idx = 0
for k, v in sorted(reg.items()):
    blob = v.get("original") or ""
    if not blob:
        continue
    for rtype, pat in PATTERNS:
        for m in pat.finditer(blob):
            frag = m.group(0)
            if any(s in frag for s in GEN_SKIP):
                continue
            # 取上下文分句
            s = blob.rfind("　", 0, m.start())
            e = blob.find("　", m.end())
            ctx = blob[(s + 1 if s >= 0 else 0):(e if e >= 0 else len(blob))][:160]
            key = (k, rtype, frag)
            if key in seen:
                continue
            seen.add(key)
            idx += 1
            target = frag
            if rtype == "已上某分组":
                target = frag[2:].strip()
            elif rtype == "本司掌行":
                target = "本司"
            xref.append({
                "xref_id": f"XREF-{idx:03d}",
                "from_item": k,
                "from_volume": v["volume"],
                "from_layer": v.get("section") or "",
                "ref_type": rtype,
                "target": target,
                "target_org": match_org(frag) if rtype in ORG_TYPES else "",
                "note": ctx,
                "original": frag,
            })

json.dump(xref, open(os.path.join(LAYERS, "xref.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

from collections import Counter
print("=" * 60)
print(f"XREF 层：{len(xref)} 条")
print("类型分布:", dict(Counter(x["ref_type"] for x in xref)))
print("可挂衙门:", sum(1 for x in xref if x["target_org"]))
print("=" * 60)
for x in xref[:8]:
    print(f"{x['xref_id']} [{x['from_item']}] {x['ref_type']} -> {x['target'][:20]} | org={x['target_org']}")
print("...")
for x in [y for y in xref if y["ref_type"] == "已上某分组"][:8]:
    print(f"{x['xref_id']} [{x['from_item']}] 分组: {x['target'][:26]} | {x['note'][:40]}")
print("...")
for x in [y for y in xref if y["ref_type"] in ("今归某司", "隶属变动", "本司掌行")][:8]:
    print(f"{x['xref_id']} [{x['from_item']}] {x['ref_type']}: {x['original'][:30]} | org={x['target_org']}")
