# -*- coding: utf-8 -*-
"""把指纹库中的 01 卷原文 dump 为 _extract\01_卷上_体立为政事情.txt（条N|正文），统一阅读源。"""
import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))  # 项目根：脚本自身位置推导
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
out = []
for i in range(1, 95):
    item_id = f"01-{i:03d}"
    out.append(f"条{i}|{reg[item_id]['original']}")
open(os.path.join(ROOT, "_extract", "01_卷上_体立为政事情.txt"), "w", encoding="utf-8").write("\n".join(out))
print("dumped 94 items")
