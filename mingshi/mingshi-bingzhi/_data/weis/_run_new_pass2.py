# -*- coding: utf-8 -*-
"""后定树 AI 复核 pass2：87 个 pending 粘连段按**词尾锚点**逐卫拆分定边界。
原理（SKILL.md §6.3）：卫/所/司名本身不含词尾后缀字（卫/所/司/站/寨），
故粘连串在每个后缀字处切开即是正确边界（地面为双字锚点）。
拆出的全部名称逐字回验源行（A 族纪律），数量标签（站七类）剔除。
词典回填至 wei_name_index_new.json → 重跑 build_candidate_tree → 覆盖率复测。
"""
import json, io, sys, re

sys.path.insert(0, 'assets/tools')
sys.path.insert(0, 'scripts')
import _weisuo_builder as B

NEW_INDEX = '_data/weis/wei_name_index_new.json'
CAND = '_data/weis/candidates_66_new.json'
src_lines = {no: ln for no, ln in B.load_source_lines('66', 122, 251)}
index = json.load(io.open(NEW_INDEX, encoding='utf-8'))['index']

SUF = ('卫', '所', '司', '站', '寨', '地面')
COUNT_LABEL_RE = re.compile(r'^(?:卫|所|站|地面|寨|都指挥使司|指挥使司|宣尉使司|招讨司|万户府|千户所)[一二三四五六七八九十百千]$')

def split_glued(text):
    """在每个词尾锚点字后断开；返回 (pieces, 重构是否等于原文)。"""
    pieces, buf, i, ok = [], '', 0, True
    while i < len(text):
        if text.startswith('地面', i):
            buf += '地面'; i += 2
            pieces.append(buf); buf = ''
        elif text[i] in ('卫', '所', '司', '站', '寨'):
            buf += text[i]; i += 1
            pieces.append(buf); buf = ''
        else:
            buf += text[i]; i += 1
    if buf:
        pieces.append(buf)  # 尾缀无锚（如张本残串）——保留为一片待观察
    return pieces, ''.join(pieces) == text

# 1) 收集 pending
cand = json.load(io.open(CAND, encoding='utf-8'))
pend = []
def walk(n, parent):
    if n.get('ai_review') == 'required':
        pend.append((n, parent))
    for c in n.get('children') or []:
        walk(c, n)
walk(cand['tree']['root'], None)
print('pending segments:', len(pend))

report = []
dropped = []
for n, parent in pend:
    loc = n['src_loc']
    ln = int(loc.split('L')[1])
    text = n['name']
    pieces, ok = split_glued(text)
    if not ok:
        report.append(('SPLIT_MISMATCH', loc, text))
        continue
    # 逐字回验：该 pending 串应原样出现在源行
    if text not in src_lines[ln]:
        report.append(('NOT_IN_SOURCE', loc, text))
        continue
    for p in pieces:
        if COUNT_LABEL_RE.match(p):
            dropped.append((loc, p))
            continue
        index.setdefault(p, {'count': 0, 'first': None})
        index[p]['count'] += 1
        if index[p]['first'] is None:
            index[p]['first'] = 'L%d' % ln

# 特判：L211 ◎南京卫所亲军卫 是标题行不是卫列
t211 = [n for n, p in pend if n['src_loc'] == '卷66-L211']
for n in t211:
    for k in ('ai_review', 'why', 'cand'):
        n.pop(k, None)
    n['name'] = '南京卫所'
    n['level'] = '块'
    n['review_action'] = 'rename'
    n['review_note'] = 'AI 复核：◎南京卫所亲军卫 为南京子树总标题（非卫名粘连段）；南京亲军卫名单 L212 挂其下，◎五军都督府属 L213 为兄弟块（SKILL.md §16-8 三子树分立）'
    pend.remove((n, p)) if (n, p) in pend else None

json.dump({'index': index, 'note': 'new段专用词典副本（种子=旧树377词 + pass1预扫 + pass2 AI复核87段拆分回填）'},
          io.open(NEW_INDEX, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('index size:', len(index), '| dropped count-labels:', len(dropped), dropped[:6])
print('split anomalies:', report)

# 2) 重跑建树（同一词典）
lines = [(no, src_lines[no]) for no in sorted(src_lines)]
tree = B.build_candidate_tree(lines, 'new', '66', index)
cov = B.build_coverage(tree, lines, index)
print('pass2 coverage:', json.dumps({k: cov[k] for k in
      ('determined_count', 'pending_count', 'segment_coverage', 'coverage_ok',
       'bracket_notes_total', 'wei_name_index_size')}, ensure_ascii=False))

# 2b) L211 手工 rename 在重建树上重放（建树从原文来，前面对 cand 的改名仅存档）
def find_node(n, name):
    if n.get('name') == name:
        return n
    for c in n.get('children') or []:
        r = find_node(c, name)
        if r: return r
tgt = find_node(tree['root'], '◎南京卫所亲军卫') or find_node(tree['root'], '南京卫所亲军卫')
if tgt:
    tgt['name'] = '南京卫所'
    tgt['level'] = '块'
    tgt['ai_review'] = None
    tgt.pop('why', None)
    tgt['review_action'] = 'rename'
    print('L211 rename replayed on rebuilt tree')

# 3) 残留 pending 打印
pend2 = []
def walk2(n):
    if n.get('ai_review') == 'required':
        pend2.append((n['src_loc'], n['name']))
    for c in n.get('children') or []:
        walk2(c)
walk2(tree['root'])
print('residual pending:', len(pend2), pend2[:10])

out = {'meta': {**cand['meta'],
                'pass': 'pass2（AI 复核 87 pending 段词尾锚点拆分回填后重跑）',
                'l211_manual_rename': True},
       'tree': tree, 'coverage': cov}
json.dump(out, io.open(CAND, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 4) 结构对账：卫/所叶计数 + 名称逐字命中所在源行
leafs = []
def walk3(n):
    if n.get('level') in ('卫', '所'):
        leafs.append(n)
    for c in n.get('children') or []:
        walk3(c)
walk3(tree['root'])
bad = [x for x in leafs if x['name'] not in src_lines[int(x['src_loc'].split('L')[1])]]
print('leaf total:', len(leafs), '| verbatim-miss:', len(bad), bad[:5])
# 奴儿干段卫叶数 vs 数量行 384
def block_leafs(n, name):
    if n.get('name') == name:
        c = {'卫': 0, '所': 0}
        def w(m):
            if m.get('level') in ('卫', '所'): c[m['level']] += 1
            for ch in m.get('children') or []: w(ch)
        w(n)
        return c
    for ch in n.get('children') or []:
        r = block_leafs(ch, name)
        if r: return r
print('奴儿干都司 leafs:', block_leafs(tree['root'], '奴儿干都司'))
