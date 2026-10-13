# -*- coding: utf-8 -*-
"""加虚拟根节点，修复父子引用"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
ents = json.load(open(os.path.join(ROOT, "_layers", "ents.json"), encoding="utf-8"))

# 加虚拟根节点
virtual_nodes = [
    {"item_id": "VIRT-001", "text": "全书", "type": "institution", "node_type": "虚拟根", "parent_id": None, "confidence": "high"},
    {"item_id": "VIRT-002", "text": "未明", "type": "institution", "node_type": "虚拟根", "parent_id": "全书", "confidence": "low"},
    {"item_id": "VIRT-003", "text": "某卫", "type": "institution", "node_type": "虚拟根", "parent_id": "五军都督府", "confidence": "low"},
]

# 去重后添加
existing = {e["text"] for e in ents}
for vn in virtual_nodes:
    if vn["text"] not in existing:
        ents.append(vn)

print(f"添加虚拟根节点: {len(virtual_nodes)} 个")
print(f"实体总数: {len(ents)}")

# 写回
with open(os.path.join(ROOT, "_layers", "ents.json"), "w", encoding="utf-8") as f:
    json.dump(ents, f, ensure_ascii=False, indent=1)
print("已写回")
