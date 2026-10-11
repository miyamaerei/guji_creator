# -*- coding: utf-8 -*-
"""提取 02-11 卷 XHTML 条目文本为干净 TXT（供 AI 逐条分析）"""
import os, re, html as h

OUT = r"C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat"
CH = os.path.join(OUT, "新官轨范_章节")
EX = os.path.join(OUT, "_extract")
os.makedirs(EX, exist_ok=True)

files = [f for f in sorted(os.listdir(CH)) if re.match(r"0[2-9]|1[01]", f) and f.endswith(".xhtml")]
for fn in files:
    content = open(os.path.join(CH, fn), encoding="utf-8").read()
    items = re.findall(r'<p class="item">(.*?)</p>', content, re.S)
    if not items:
        items = re.findall(r'<p[^>]*>(.*?)</p>', content, re.S)
    lines = []
    for i, m in enumerate(items, 1):
        t = h.unescape(m).strip()
        t = re.sub(r"\s+", "", t)
        if t.startswith("√"):
            t = t[1:]
        lines.append(f"条{i}|{t}")
    out = os.path.join(EX, fn.replace(".xhtml", ".txt"))
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    print(fn, "->", len(lines), "条")
