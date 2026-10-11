# -*- coding: utf-8 -*-
import re, html as h
fp = r'C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat\新官轨范_章节\02_卷下_牧民备用.xhtml'
c = open(fp, encoding='utf-8').read()
its1 = re.findall(r'<p class="item">(.*?)</p>', c, re.S)
print('class=item count:', len(its1))
its2 = re.findall(r'<p[^>]*>(.*?)</p>', c, re.S)
print('fallback count:', len(its2))
out = ['its1=%d its2=%d' % (len(its1), len(its2))]
for m in its2:
    out.append(repr(h.unescape(m).strip()))
open(r'C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat\_check_02.txt', 'w', encoding='utf-8').write('\n'.join(out))
