# -*- coding: utf-8 -*-
"""检查L4六部业务域层37个子层的覆盖情况"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
tags = json.load(open(os.path.join(ROOT, "_layers", "domain_tags.json"), encoding="utf-8"))

# 全部37个子层
ALL_SUBLAYERS = {
    "SEL": ["SEL-XUAN", "SEL-KAO", "SEL-FENG", "SEL-LI", "SEL-DING", "SEL-HUANG"],
    "FIN": ["FIN-TIAN", "FIN-SHUI", "FIN-CAO", "FIN-CANG", "FIN-LU", "FIN-TU", "FIN-ZA"],
    "RIT": ["RIT-CHAO", "RIT-SI", "RIT-JIA", "RIT-FU", "RIT-GONG", "RIT-SENG", "RIT-YUE", "RIT-SHEN"],
    "MIL": ["MIL-XUAN", "MIL-WEI", "MIL-GUAN", "MIL-YI", "MIL-MA", "MIL-QI"],
    "LAW": ["LAW-LI", "LAW-WU", "LAW-HUI", "LAW-ZANG", "LAW-TU"],
    "ENG": ["ENG-DIAN", "ENG-WANG", "ENG-LING", "ENG-YU", "ENG-JUN", "ENG-LIAO", "ENG-HE"],
}

# 统计每个子层的数量
sublayer_count = Counter(t["sublayer"] for t in tags)

print("=" * 70)
print("L4 六部业务域层 37 个子层覆盖检查")
print("=" * 70)

missing = []
thin = []

for domain, sublayers in ALL_SUBLAYERS.items():
    print(f"\n【{domain}域】")
    print(f"  {'子层':15s} {'数量':>6s} {'状态':>8s}")
    print("  " + "-" * 40)

    total = 0
    for sl in sublayers:
        cnt = sublayer_count.get(sl, 0)
        total += cnt

        if cnt == 0:
            status = "❌ 缺失"
            missing.append(sl)
        elif cnt < 10:
            status = "⚠️ 太少"
            thin.append((sl, cnt))
        elif cnt < 50:
            status = "🟡 一般"
        else:
            status = "✅ 充足"

        print(f"  {sl:15s} {cnt:6d}   {status}")

    # OTHER
    other = sublayer_count.get(domain + "-OTHER", 0)
    print(f"  {'OTHER':15s} {other:6d}   (未分类)")

print(f"\n{'=' * 70}")
print(f"总结")
print(f"{'=' * 70}")
print(f"总子层数: 37")
print(f"缺失: {len(missing)}个")
for sl in missing:
    print(f"  ❌ {sl}")

print(f"\n太少(<10条): {len(thin)}个")
for sl, cnt in thin:
    print(f"  ⚠️ {sl}: {cnt}条")
