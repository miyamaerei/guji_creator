# -*- coding: utf-8 -*-
"""批量补全实体层：从 rules 和 nams 中提取衙门/机构名"""
import json, os, re
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))

reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))
ents = json.load(open(os.path.join(ROOT, "_layers", "ents.json"), encoding="utf-8"))

# 已有实体名
existing = {e["text"] for e in ents if not e.get("item_id", "").startswith("VIRT")}
print(f"现有实体: {len(existing)} 个")

# 机构名后缀
ORG_SUFFIX = ["部", "院", "寺", "监", "司", "府", "卫", "所", "局", "仓", "库", "厂", "署", "司礼监", "御马监"]

# 从 rules 中提取
new_ents = {}

# 1. 从 rules.subject 提取
for r in rules:
    subj = r.get("subject", "")
    if subj and subj not in existing and subj not in new_ents:
        # 检查是否是机构名
        if any(subj.endswith(s) for s in ORG_SUFFIX) and len(subj) <= 8:
            new_ents[subj] = {
                "item_id": r["item_id"],
                "text": subj,
                "type": "institution",
                "rank_order": "未明",
                "confidence": "medium",
            }

# 2. 从 nams.name 提取
for n in nams:
    name = n["name"]
    if name not in existing and name not in new_ents:
        if any(name.endswith(s) for s in ORG_SUFFIX) and len(name) <= 10:
            new_ents[name] = {
                "item_id": n["item_id"],
                "text": name,
                "type": "institution",
                "rank_order": "未明",
                "confidence": "medium",
            }

print(f"新提取实体: {len(new_ents)} 个")

# 按卷组统计
new_by_vol = defaultdict(int)
for e in new_ents.values():
    vol = int(e["item_id"].split("-")[0])
    new_by_vol[vol] += 1

print("\n按卷组分布:")
GROUPS = [
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
for gname, vols in GROUPS:
    cnt = sum(new_by_vol.get(v, 0) for v in vols)
    print(f"  {gname}: +{cnt}")

# 追加到 ents
all_ents = ents + list(new_ents.values())
print(f"\n实体总数: {len(all_ents)} (原 {len(ents)} + 新增 {len(new_ents)})")

# 写回
with open(os.path.join(ROOT, "_layers", "ents.json"), "w", encoding="utf-8") as f:
    json.dump(all_ents, f, ensure_ascii=False, indent=1)
print("已写回 ents.json")
