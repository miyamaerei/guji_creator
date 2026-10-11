# -*- coding: utf-8 -*-
import os, re, html as h
ROOT = os.path.dirname(os.path.abspath(__file__))  # 项目根：脚本自身位置推导
fp = os.path.join(ROOT, '新官轨范_章节', '02_卷下_牧民备用.xhtml')
c = open(fp, encoding='utf-8').read()
its1 = re.findall(r'<p class="item">(.*?)</p>', c, re.S)
print('class=item count:', len(its1))
its2 = re.findall(r'<p[^>]*>(.*?)</p>', c, re.S)
print('fallback count:', len(its2))
out = ['its1=%d its2=%d' % (len(its1), len(its2))]
for m in its2:
    out.append(repr(h.unescape(m).strip()))
open(os.path.join(ROOT, '_check_02.txt'), 'w', encoding='utf-8').write('\n'.join(out))
