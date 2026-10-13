# -*- coding: utf-8 -*-
"""P2：批量建子部门父子关系"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
ents = json.load(open(os.path.join(ROOT, "_layers", "ents.json"), encoding="utf-8"))

# 六部清单
BUBU = ["吏部", "户部", "礼部", "兵部", "刑部", "工部"]

# 建立名称→实体映射
ent_map = {e["text"]: e for e in ents}

# 推断父子关系
fixed = 0
for e in ents:
    name = e["text"]
    if e.get("parent_id") and e["parent_id"] != "未明":
        continue

    # 规则：名称以"司"结尾，且包含某部名
    if name.endswith("司") and len(name) > 3:
        for bu in BUBU:
            if bu in name and bu != name:
                e["parent_id"] = bu
                e["node_type"] = "子部门"
                fixed += 1
                break

    # 规则：名称含"都察院"的，父节点是都察院
    elif "都察院" in name and name != "都察院":
        e["parent_id"] = "都察院"
        e["node_type"] = "子部门"
        fixed += 1

    # 规则：名称含"大理寺"的，父节点是大理寺
    elif "大理寺" in name and name != "大理寺":
        e["parent_id"] = "大理寺"
        e["node_type"] = "子部门"
        fixed += 1

print(f"批量建父子关系: {fixed} 条")

# 统计
node_types = Counter(e.get("node_type", "未明") for e in ents)
print("\n节点类型分布:")
for t, c in node_types.most_common():
    print(f"  {t}: {c}")

with open(os.path.join(ROOT, "_layers", "ents.json"), "w", encoding="utf-8") as f:
    json.dump(ents, f, ensure_ascii=False, indent=1)
print("\n已写回")
