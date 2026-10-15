# -*- coding: utf-8 -*-
"""阶段二复核落盘：生成 candidates_66_old.reviewed.json
变更范围（严格限定，其余节点原样）：
  1) 区块级注归位（HANDOFF §4-2）：4 条「已上/俱」注从卫叶提升至块节点
  2) 复合串拆分：居庸关千户所、会州卫两处叶注剥离区块段
原 candidates_66_old.json 为阶段一产物，不改动（幂等：本脚本可从原文件重放）。
"""
import json, os, tempfile

SRC = '_data/weis/candidates_66_old.json'
DST = '_data/weis/candidates_66_old.reviewed.json'

d = json.load(open(SRC, encoding='utf-8'))

def find(root, path_names):
    n = root
    for nm in path_names:
        n = next(c for c in (n.get('children') or []) if c.get('name') == nm)
    return n

def leaf(block_node, name):
    return next(c for c in (block_node.get('children') or []) if c.get('name') == name)

def add_note(node, text, src_loc, provenance):
    node.setdefault('notes', []).append(text)
    node.setdefault('note_meta', []).append({
        'text': text, 'src_loc': src_loc, 'provenance': provenance,
        'review_ref': 'leaf_notes_review.json %s' % provenance})

changes = []

# --- 1. 北平都司（L110）：已上俱改为亲军 / 已上俱属后府 ---
bp = find(d['tree']['root'], ['五军都督府所属卫所', '后军都督府', '在外', '北平都司'])
tz = leaf(bp, '通州卫'); assert tz['notes'] == ['已上俱改为亲军']
tz['notes'] = []
jy = leaf(bp, '居庸关千户所'); assert jy['notes'] == ['后为隆庆卫已上俱属后府']
jy['notes'] = ['后为隆庆卫']
add_note(bp, '已上俱改为亲军', '卷66-L111', 'LN-80（原通州卫叶）')
add_note(bp, '已上俱属后府', '卷66-L111', 'LN-82 拆分后半（原居庸关千户所叶）')
changes.append('北平都司：+2 块注；通州卫叶注清空；居庸关千户所叶注剥离为「后为隆庆卫」')

# --- 2. 北平行都司（L112）：俱改调京卫 / 已上俱属后府 ---
bxx = find(d['tree']['root'], ['五军都督府所属卫所', '后军都督府', '在外', '北平行都司'])
hz = leaf(bxx, '会州卫'); assert hz['notes'] == ['俱改调京卫已上俱属后府']
hz['notes'] = []
add_note(bxx, '俱改调京卫', '卷66-L112', 'LN-85 拆分前半（原会州卫叶）')
add_note(bxx, '已上俱属后府', '卷66-L112', 'LN-85 拆分后半（原会州卫叶）')
changes.append('北平行都司：+2 块注；会州卫叶注清空（注已提升）')

# --- 3. 北平三护卫（L118）：俱为亲军 ---
ys = find(d['tree']['root'], ['五军都督府所属卫所', '后军都督府', '在外', '北平三护卫'])
hs = leaf(ys, '燕山中护卫'); assert hs['notes'] == ['俱为亲军']
hs['notes'] = []
add_note(ys, '俱为亲军', '卷66-L118', 'LN-87（原燕山中护卫叶）')
changes.append('北平三护卫：+1 块注；燕山中护卫叶注清空')

# --- 4. 山西三护卫（L120）：俱革 ---
sx = find(d['tree']['root'], ['五军都督府所属卫所', '后军都督府', '在外', '山西三护卫'])
ty = leaf(sx, '太原中护卫'); assert ty['notes'] == ['俱革']
ty['notes'] = []
add_note(sx, '俱革', '卷66-L120', 'LN-88（原太原中护卫叶）')
changes.append('山西三护卫：+1 块注；太原中护卫叶注清空')

# --- 计数器重算 ---
leaf_notes = block_notes = 0
def walk(n):
    global leaf_notes, block_notes
    k = n.get('level')
    ns = n.get('notes') or []
    if k in ('卫', '所'):
        leaf_notes += len(ns)
    elif ns:
        block_notes += len(ns)
    for ch in n.get('children') or []:
        walk(ch)
walk(d['tree']['root'])
d['coverage']['bracket_notes_total'] = leaf_notes + block_notes
d['coverage']['leaf_notes'] = leaf_notes
d['coverage']['block_notes'] = block_notes
d['meta']['reviewed'] = '2026-10-15 阶段二：卫级 88 条复核（leaf_notes_review.json）+ 已上区块注归位（HANDOFF §4-1/4-2）'

def atomic_write(path, obj):
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix='.tmp')
    with os.fdopen(fd, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)

atomic_write(DST, d)
print('\n'.join(changes))
print('leaf_notes=%d block_notes=%d total=%d' % (leaf_notes, block_notes, leaf_notes + block_notes))
