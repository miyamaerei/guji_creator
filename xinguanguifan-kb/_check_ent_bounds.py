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
    its = [h.unescape(m).strip() for m in its]
    for i, t in enumerate(its, 1):
        texts[f'{no}-{i:03d}'] = t.lstrip('√').strip()
bad = []
for f in sorted(glob.glob(ANN + '\\*.json')):
    d = json.load(open(f, encoding='utf-8'))
    for e in d['entities']:
        iid = f"{d['chapter_no']}-{int(e['source'].split('#条')[-1]):03d}"
        L = len(texts.get(iid, ''))
        if e['end'] > L or e['start'] < 0 or e['start'] > e['end'] or e['start'] > L:
            bad.append((iid, e.get('text'), e['start'], e['end'], L, e['type'], e['source']))
out = ['bad count: %d' % len(bad)]
for b in bad[:40]:
    out.append(str(b))
open(os.path.join(ROOT, '_check_ent_bounds_out.txt'), 'w', encoding='utf-8').write('\n'.join(out))
