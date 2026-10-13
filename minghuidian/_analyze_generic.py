# -*- coding: utf-8 -*-
"""泛化分析：统计 subject/nam_type 的泛化分布"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))

print("=" * 60)
print("泛化度分析报告")
print("=" * 60)

# ===== 1. RUL subject 泛化分析 =====
print("\n【1】RUL subject 泛化分析")
subjects = Counter(r.get("subject", "未明") for r in rules)
print(f"总规则数: {len(rules)}")
print(f"不同 subject 数量: {len(subjects)}")

# 泛化词清单
GENERIC_WORDS = ["各衙门", "各处", "有司", "诸司", "天下", "在外", "在内", "凡", "未明", ""]
generic_count = 0
generic_list = []

for sub, cnt in subjects.most_common(30):
    is_generic = any(gw in sub for gw in GENERIC_WORDS) or len(sub) <= 2
    if is_generic:
        generic_count += cnt
        generic_list.append((sub, cnt))

print(f"\n泛化 subject 数量: {generic_count} ({generic_count*100//len(rules)}%)")
print("\n泛化 subject TOP20:")
for sub, cnt in generic_list[:20]:
    print(f"  {sub:20s}: {cnt:4d} 条")

# ===== 2. RUL type 分布 =====
print("\n【2】RUL type 分布（看是否集中）")
types = Counter(r.get("type", "未明") for r in rules)
for t, c in types.most_common():
    pct = c * 100 // len(rules)
    print(f"  {t:10s}: {c:4d} ({pct}%)")

# ===== 3. NAM nam_type 分布 =====
print("\n【3】NAM nam_type 分布")
nam_types = Counter(n.get("nam_type", "未明") for n in nams)
for t, c in nam_types.most_common():
    pct = c * 100 // len(nams)
    print(f"  {t:15s}: {c:5d} ({pct}%)")

# ===== 4. 误判检测：乐章/诗词被标成官职 =====
print("\n【4】可能误判的 NAM（乐章/诗词名被标成官职）")
music_keywords = ["过门", "乐章", "曲", "歌", "辞", "咏", "奏"]
misjudged = []
for n in nams:
    name = n["name"]
    if n["nam_type"] == "官职题名" and any(k in name for k in music_keywords):
        misjudged.append((n["item_id"], name, n["nam_type"]))

print(f"可能误判: {len(misjudged)} 条")
for iid, name, nt in misjudged[:10]:
    print(f"  {iid}: {name[:20]} → {nt}")

# ===== 5. 按卷组看泛化度 =====
print("\n【5】按卷组看泛化度")
groups = [
    ("G0 宗人府", [1]),
    ("G1 吏部", list(range(2, 14))),
    ("G2 户部", list(range(14, 42))),
    ("G3 礼部", list(range(42, 106))),
    ("G4 兵部", list(range(106, 130))),
    ("G5 刑部", list(range(130, 144))),
    ("G6 工部", list(range(144, 164))),
    ("G7 诸文职", list(range(164, 179))),
    ("G8 诸武职", [179, 180]),
]

for gname, vols in groups:
    g_rules = [r for r in rules if int(r["item_id"].split("-")[0]) in vols]
    if not g_rules:
        continue
    g_generic = sum(1 for r in g_rules if any(gw in r.get("subject","") for gw in GENERIC_WORDS))
    pct = g_generic * 100 // len(g_rules)
    print(f"  {gname:12s}: {len(g_rules):4d} 条规则, 泛化 {g_generic:4d} ({pct}%)")
