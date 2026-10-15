# -*- coding: utf-8 -*-
"""后定树 AI 复核批次 3：`已上/已下/俱` 类**区块级注**归位（SKILL.md §16-5、§6.2）。

候选树把这类注挂在**段尾卫叶**上（切段器只看得到前一个词），但原文语义是
「前/后**一整组**卫所」的整体说明（隶属、添设、旧无后设、改属），留在叶上会造成
① 归属错位（读者以为只指这一卫）② 区块信息被复制/漏读。

归位算法（确定性，可重跑）：
  同一父节点（都司/土官/块）的叶序列里，按出现顺序找边界注：
    - `已上… / 以上… / 俱… / 自…` → 覆盖**自上一个边界以来到本叶**的连续叶段（上型）
    - `已下… / 以下… / 此下…`     → 覆盖**本叶之后到下一个边界**的连续叶段（下型）
  注串从叶 notes 摘除，写入父节点 `group_notes[]`：
    {text, scope, anchor_leaf, covers[], src_loc, note_class}
  note_class：含「属」→ 隶属群注；含「添设/后设/旧无」→ 设置群注；其余→ 说明群注。

产物：`_data/weis/candidates_66_new.reviewed.json`（候选树本体不改，便于对账重跑）
      `_data/weis/new_blocknotes.json`（群注登记表，供 C14/L1 隶属转写消费）
"""
import json, io, re, sys
from collections import Counter

sys.path.insert(0, 'scripts')
from _common import atomic_write_json

CAND = '_data/weis/candidates_66_new.json'
OUT = '_data/weis/candidates_66_new.reviewed.json'
REG = '_data/weis/new_blocknotes.json'

UP_RE = re.compile(r"^(?:已上|以上|俱|自|此上)")
DOWN_RE = re.compile(r"^(?:已下|以下|此下)")
LEAF_LEVELS = ('卫', '所', '土司', '驿', '地面', '寨')

d = json.load(io.open(CAND, encoding='utf-8'))
root = d['tree']['root']

register = []
stats = Counter()


def classify_note(t):
    if '属' in t:
        return '隶属群注'
    if any(k in t for k in ('添设', '后设', '旧无', '增设')):
        return '设置群注'
    if any(k in t for k in ('改', '调', '革', '并', '升')):
        return '沿革群注'
    return '说明群注'


def process(node):
    kids = node.get('children') or []
    # 叶序列（含中间块节点的重置：块/都司/府等子容器另起一组）
    seq = [i for i, c in enumerate(kids) if c.get('level') in LEAF_LEVELS]
    names = {i: kids[i].get('name') for i in seq}
    order = seq
    last_boundary = -1  # 上一个边界在 order 中的下标
    for pos, ci in enumerate(order):
        leaf = kids[ci]
        notes = leaf.get('notes') or []
        keep = []
        for t in notes:
            if t.startswith('属'):
                # 单叶隶属注（如「天全六番招讨使司(属都司)」）不是群注，但它**切断**
                # 后续 `已上…` 的覆盖范围——否则群注会把已自注归属的土司也圈进去
                # （实测 L148「已上属茂州卫」曾误含 天全六番招讨使司）。
                last_boundary = pos
                keep.append(t)
                continue
            if not (UP_RE.match(t) or DOWN_RE.match(t)):
                keep.append(t)
                continue
            scope = '上' if UP_RE.match(t) else '下'
            if scope == '上':
                covers = [names[k] for k in order[last_boundary + 1:pos + 1]]
            else:
                nxt = len(order)
                for q in range(pos + 1, len(order)):
                    nn = kids[order[q]].get('notes') or []
                    if any(UP_RE.match(x) or DOWN_RE.match(x) or x.startswith('属') for x in nn):
                        nxt = q
                        break
                covers = [names[k] for k in order[pos + 1:nxt]]
                covers = [names[ci]] + covers
            last_boundary = pos
            entry = {
                'text': t, 'scope': scope, 'anchor_leaf': leaf.get('name'),
                'covers': covers, 'src_loc': leaf.get('src_loc'),
                'note_class': classify_note(t), 'parent_block': node.get('name'),
                'parent_src': node.get('src_loc'),
            }
            register.append(entry)
            stats[entry['note_class']] += 1
            stats['scope_' + scope] += 1
        if keep or notes:
            leaf['notes'] = keep
            if notes:
                leaf.setdefault('note_meta', []).append(
                    {'promoted': 'group_notes', 'from': 'AI 复核批次 3（区块级注归位）'})
    for c in kids:
        process(c)


# 归位前先记录原叶级注总数
def leaf_notes_total(n):
    acc = [0]

    def w(x):
        if x.get('level') in LEAF_LEVELS:
            acc[0] += len(x.get('notes') or [])
        for ch in x.get('children') or []:
            w(ch)
    w(n)
    return acc[0]


before = leaf_notes_total(root)
process(root)
after = leaf_notes_total(root)
block_note_total = len(register)


# 把 register 写回父节点 group_notes
def all_nodes(n):
    out = [n]
    for c in n.get('children') or []:
        out.extend(all_nodes(c))
    return out


nodes = all_nodes(root)
idx = {(x.get('name'), x.get('src_loc')): x for x in nodes}
for e in register:
    p = idx.get((e['parent_block'], e['parent_src']))
    if p is None:
        print('!! 父节点缺失:', e['parent_block'], e['parent_src'], e['text'][:20])
        continue
    p.setdefault('group_notes', []).append(
        {k: e[k] for k in ('text', 'scope', 'anchor_leaf', 'covers', 'src_loc', 'note_class')})

d['meta']['reviewed_pass'] = ('批次3 区块级注归位：叶级注 %d → %d，群注 %d 条'
                               '（上型 %d／下型 %d）' % (
                                   before, after, block_note_total,
                                   stats['scope_上'], stats['scope_下']))
out = dict(d)
out['tree'] = d['tree']
atomic_write_json(OUT, out)
atomic_write_json(REG, {'meta': {'vol': '66', 'list_ver': 'new',
                                 'note': '已上/已下/俱 类区块级注登记表（AI 复核批次 3 产物）',
                                 'total': len(register),
                                 'by_class': dict(stats)},
                        'group_notes': register})
print('叶级注 %d → %d；群注登记 %d 条' % (before, after, len(register)))
print('分类：', json.dumps({k: v for k, v in stats.items()}, ensure_ascii=False))
print('写入', OUT, '/', REG)
