# -*- coding: utf-8 -*-
"""条原文指纹库生成器：从 12 个 XHTML 一次性解析 274 条原文，产出 _item_registry.json。
口径：original=去√后的逐字原文（保留标点/缺字□/异体）；norm=去空白版（供比对）。"""
import os, re, json, html as htmllib

CH_DIR = r"C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat\新官轨范_章节"
OUT = r"C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat\_item_registry.json"

def norm(s):
    return re.sub(r"\s+", "", s)

reg = {}
for fn in sorted(os.listdir(CH_DIR)):
    if not fn.endswith(".xhtml"):
        continue
    ch = fn[:2]
    content = open(os.path.join(CH_DIR, fn), encoding="utf-8").read()
    items = re.findall(r'<p class="item">(.*?)</p>', content, re.S)
    if not items:
        items = re.findall(r'<p[^>]*>(.*?)</p>', content, re.S)
    for i, it in enumerate(items, 1):
        txt = htmllib.unescape(it).strip()
        if txt.startswith("√"):
            txt = txt[1:].lstrip()
        item_id = f"{ch}-{i:03d}"
        reg[item_id] = {"original": txt, "norm": norm(txt)}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(reg, f, ensure_ascii=False, indent=1)
print("items =", len(reg))
missing = [k for k, v in reg.items() if not v["original"]]
print("empty =", len(missing), missing[:5])
