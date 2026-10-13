# -*- coding: utf-8 -*-
"""批量建父子关系：根据衙门名推断父节点"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
ents = json.load(open(os.path.join(ROOT, "_layers", "ents.json"), encoding="utf-8"))

# 根衙门清单（六部+院+寺+监）
ROOT_ORGS = ["吏部", "户部", "礼部", "兵部", "刑部", "工部",
             "都察院", "大理寺", "太常寺", "光禄寺", "鸿胪寺",
             "国子监", "钦天监", "太医院", "宗人府",
             "五军都督府", "前军都督府", "后军都督府", "左军都督府", "右军都督府",
             "锦衣卫", "行人司"]

# 建立名称→实体映射
ent_map = {e["text"]: e for e in ents}

# 推断父节点
fixed = 0
for e in ents:
    name = e["text"]
    if e.get("parent_id"):
        continue

    # 规则1：含"司"且名称>4字的，父节点可能是某部
    if name.endswith("司") and len(name) > 3:
        # 尝试找父部
        for root in ROOT_ORGS:
            if root in name:
                e["parent_id"] = root
                e["node_type"] = "子部门"
                fixed += 1
                break

    # 规则2：含"卫"的，父节点是"五军都督府"或"某都司"
    elif name.endswith("卫"):
        e["parent_id"] = "五军都督府"
        e["node_type"] = "卫所"
        fixed += 1

    # 规则3：含"所"的，父节点是某卫
    elif name.endswith("所"):
        e["parent_id"] = "某卫"
        e["node_type"] = "守御所"
        fixed += 1

    # 规则4：根节点
    elif name in ROOT_ORGS:
        e["parent_id"] = "全书"
        e["node_type"] = "根节点"
        fixed += 1

    # 规则5：其他默认
    else:
        e["parent_id"] = "未明"
        e["node_type"] = "未知"

print(f"已建父子关系: {fixed} 条")

# 统计
from collections import Counter
node_types = Counter(e.get("node_type", "未明") for e in ents)
print("\n节点类型分布:")
for t, c in node_types.most_common():
    print(f"  {t}: {c}")

# 写回
with open(os.path.join(ROOT, "_layers", "ents.json"), "w", encoding="utf-8") as f:
    json.dump(ents, f, ensure_ascii=False, indent=1)
print("\n已写回 ents.json")
