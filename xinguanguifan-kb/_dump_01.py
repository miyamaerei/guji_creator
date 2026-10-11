# -*- coding: utf-8 -*-
"""把指纹库中的 01 卷原文 dump 为 _extract\01_卷上_体立为政事情.txt（条N|正文），统一阅读源。"""
import json, os
reg = json.load(open(r"C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat\_item_registry.json", encoding="utf-8"))
out = []
for i in range(1, 95):
    item_id = f"01-{i:03d}"
    out.append(f"条{i}|{reg[item_id]['original']}")
open(r"C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat\_extract\01_卷上_体立为政事情.txt", "w", encoding="utf-8").write("\n".join(out))
print("dumped 94 items")
