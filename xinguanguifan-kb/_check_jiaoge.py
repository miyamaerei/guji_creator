# -*- coding: utf-8 -*-
import os, json, io, sys, glob, re, html as h
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))     # 项目根：脚本自身位置推导
CH = os.path.join(ROOT, '新官轨范_章节')
ANN = os.path.join(ROOT, '新官轨范_标注')
texts = {}
for fp in sorted(glob.glob(CH + '\\*.xhtml')):
    no = fp.split('\\')[-1][:2]
    if no == '00':
        continue
    c = open(fp, encoding='utf-8').read()
    its = re.findall(r'<p class="item">(.*?)</p>', c, re.S)
    if not its:
        its = re.findall(r'<p[^>]*>(.*?)</p>', c, re.S)
    its = [h.unescape(m).strip() for m in its]
    for i, t in enumerate(its, 1):
        texts[f'{no}-{i:03d}'] = t.lstrip('√').strip()
out = []
# 找含"交割"且实体为"交割"的条目
for f in sorted(glob.glob(ANN + '\\*.json')):
    d = json.load(open(f, encoding='utf-8'))
    for e in d['entities']:
        if e.get('text') == '交割':
            iid = f"{d['chapter_no']}-{int(e['source'].split('#条')[-1]):03d}"
            L = len(texts.get(iid, ''))
            out.append('交割实体: iid=%s s=%s e=%s textlen=%s type=%s' % (iid, e['start'], e['end'], L, e['type']))
            out.append('条目文本: ' + texts.get(iid, '<空>')[:120])
            out.append('---')
open(os.path.join(ROOT, '_check_jiaoge_out.txt'), 'w', encoding='utf-8').write('\n'.join(out))
print('done')
