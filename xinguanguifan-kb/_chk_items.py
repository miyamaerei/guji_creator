# -*- coding: utf-8 -*-
import re, html as h, os
CH = r"C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat\新官轨范_章节"
for fn in sorted(os.listdir(CH)):
    if not fn.endswith(".xhtml"):
        continue
    c = open(os.path.join(CH, fn), encoding="utf-8").read()
    items = re.findall(r'<p class="item">(.*?)</p>', c, re.S)
    if not items:
        items = re.findall(r'<p[^>]*>(.*?)</p>', c, re.S)
    print(fn, len(items))
