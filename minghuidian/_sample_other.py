# -*- coding: utf-8 -*-
"""抽样看OTHER类条目内容，找关键词线索"""
import json, os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
tags = json.load(open(os.path.join(ROOT, "_layers", "domain_tags.json"), encoding="utf-8"))

# 按卷组抽样OTHER类
GROUPS = [
    ("G1 吏部 SEL", list(range(2, 14))),
    ("G2 户部 FIN", list(range(14, 42))),
    ("G3 礼部 RIT", list(range(42, 106))),
    ("G4 兵部 MIL", list(range(106, 130))),
    ("G5 刑部 LAW", list(range(130, 146))),
    ("G6 工部 ENG", list(range(146, 164))),
]

for gname, vols in GROUPS:
    print(f"\n{'='*60}")
    print(f"【{gname}】OTHER类抽样")
    print(f"{'='*60}")

    # 找该卷组的OTHER类条目
    other_tags = [t for t in tags if int(t["volume"]) in vols and t["sublayer"].endswith("OTHER")]
    print(f"OTHER总数: {len(other_tags)}")

    # 抽样10条
    sample = other_tags[:10]
    for t in sample:
        iid = t["item_id"]
        item = reg[iid]
        print(f"\n  {iid}: {item['title'][:50]}")
        print(f"    原文: {item['original'][:60]}...")
