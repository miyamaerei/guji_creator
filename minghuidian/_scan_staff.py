# -*- coding: utf-8 -*-
"""批量补人员配置：从 NAM 中提取"司吏X名/典吏X名"模式"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 读取现有 NAM
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))

# 查找含"司吏/典吏/吏目"的条目
staff_count = 0
for n in nams[:50]:
    if "staff_config" in n:
        staff_count += 1

print(f"当前含 staff_config 的 NAM: {staff_count} 条")

# 从原文中提取"司吏X名"模式
new_staff = []
for iid, item in reg.items():
    original = item["original"]
    # 匹配 "司吏二名 典吏四名" 模式
    matches = re.findall(r"(司吏|典吏|吏目|攒典|令史|书吏)\s*([一二三四五六七八九十百\d]+)\s*名", original)
    if matches:
        new_staff.append({
            "item_id": iid,
            "title": item["title"][:30],
            "staff": matches,
        })

print(f"从原文提取到 {len(new_staff)} 条含人员配置的条目")
for s in new_staff[:10]:
    print(f"  {s['item_id']}: {s['title']} → {s['staff']}")
