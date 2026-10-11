# -*- coding: utf-8 -*-
import os, json, io, sys, glob, re, html as h
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
CH = r'C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat\新官轨范_章节'
ANN = r'C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat\新官轨范_标注'
texts = {}
for fp in sorted(glob.glob(os.path.join(CH, '*.xhtml'))):
    no = os.path.basename(fp)[:2]
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
out.append('chapters keys: %s' % sorted(set(k[:2] for k in texts)))
out.append('02 items: %d' % sum(1 for k in texts if k.startswith('02')))
for k in sorted(texts):
    if k.startswith('02'):
        out.append('%s len=%d text=%s' % (k, len(texts[k]), texts[k][:40]))
bad = []
for f in sorted(glob.glob(os.path.join(ANN, '*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    for e in d['entities']:
        iid = f"{d['chapter_no']}-{int(e['source'].split('#条')[-1]):03d}"
        L = len(texts.get(iid, ''))
        if e['end'] > L or e['start'] < 0 or e['start'] > e['end'] or e['start'] > L:
            bad.append((iid, e.get('text'), e['start'], e['end'], L))
out.append('bad count: %d' % len(bad))
for b in bad[:30]:
    out.append(str(b))
open(r'C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat\_check_ent_bounds2.txt', 'w', encoding='utf-8').write('\n'.join(out))
