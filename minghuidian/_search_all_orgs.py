# -*- coding: utf-8 -*-
"""从原文搜索所有机构名称，批量补全org_profiles"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# 加载item_registry
registry = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 搜索所有带"司"、"寺"、"监"、"府"、"所"的机构名
print("=" * 60)
print("从原文搜索机构名称:")
print("=" * 60)

# 提取所有可能的机构名
org_names = set()
for item_id, item in registry.items():
    original = item.get("original", "")

    # 匹配模式：XX司、XX寺、XX监、XX府、XX所
    patterns = [
        r"([一-龥]{2,6}清吏司)",
        r"([一-龥]{2,4}寺)",
        r"([一-龥]{2,4}监)",
        r"([一-龥]{2,4}府)",
        r"([一-龥]{2,4}所)",
        r"(司务厅)",
        r"(照磨所)",
        r"(检校)",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, original)
        for m in matches:
            if 2 <= len(m) <= 8:
                org_names.add(m)

print(f"\n找到 {len(org_names)} 个可能的机构名:")
for name in sorted(org_names):
    print(f"  - {name}")
