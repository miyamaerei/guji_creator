# -*- coding: utf-8 -*-
"""后定树 pass3（builder 修复后全量重跑，从零建词典）：
  1) 词典 = 旧树 377 词种子（旧词典抽查无内部锚串）
  2) 括注锚点预扫：head 在**最后一个锚点**处截断（修 pass1 的 rfind-12 定长缺陷）
  3) 词典消毒：任何名称不得在词身含锚点字（坑：金吾右卫羽林前卫类粘串）
  4) 建树 + pending 词尾锚点拆分复核 → 回填 → 重跑至 0 pending
  5) 对账：卫/所/土司叶数 vs L121 总额 493/359、奴儿干 384、逐字源行回验
"""
import json, io, sys, re
from collections import Counter

sys.path.insert(0, 'assets/tools')
sys.path.insert(0, 'scripts')
import _weisuo_builder as B

OLD_INDEX = '_data/weis/wei_name_index.json'
NEW_INDEX = '_data/weis/wei_name_index_new.json'
CAND = '_data/weis/candidates_66_new.json'

def has_internal_anchor(name):
    """词身（去掉末尾锚后）仍含锚点字 → 粘连串。"""
    for a in B.ALL_ANCHORS:
        if name.endswith(a):
            body = name[:-len(a)]
            return any(x in body for x in ('卫', '所', '地面')) or re.search(
                r'(?<!长)(?<!宣慰)(?<!宣尉)(?<!招讨)(?<!安)司|(?<!千户)所(?!.*)', body) and bool(
                re.search(r'卫|所', body))
    return False

_ANCHER_SORTED = sorted(B.ALL_ANCHORS + ['使司', '指挥使司', '留守司', '都司'], key=len, reverse=True)

def clean_name(name):
    """词典准入：长度≤12、无标点括号、以锚结尾、词身无内部锚字。"""
    if not name or len(name) > 12:
        return False
    if re.search(r"[，。；：,;.()（）\s]", name):
        return False
    anchor = next((a for a in _ANCHER_SORTED if name.endswith(a)), None)
    if anchor is None:
        return False
    body = name[:-len(anchor)]
    if not body:
        return False  # 裸锚（卫/所/司）不入典
    return not re.search(r'[卫站寨]|地面', body) and not ('所' in body and not body.endswith('千户'))

index = dict(json.load(io.open(OLD_INDEX, encoding='utf-8'))['index'])
seed_n = len(index)
bad_seed = [k for k in index if not clean_name(k)]
print('seed rejected:', len(bad_seed), bad_seed[:8])
for k in bad_seed:
    index.pop(k)
lines = {no: ln for no, ln in B.load_source_lines('66', 122, 251)}

# 2) 括注锚点预扫（anchor-correct：最右锚点**结束位**取名，修 pass1 rfind-12 缺陷）
_LEAD_GUARD = re.compile(r'^(?:地面|千户所|使司|群牧所|仪卫司|招讨司|安抚司|万户府|宣尉使司|宣慰使司|长官司|都司|指挥使司|[卫所司站寨])')

def acceptable(name):
    return clean_name(name) and not _LEAD_GUARD.match(name)

for no, ln in lines.items():
    for m in B.BRACKET_RE.finditer(ln):
        head = ln[:m.start()]
        # 所有锚点的结束位（复合锚整词命中：千户所/使司/地面/仪卫司…）
        ends = []
        for a in _ANCHER_SORTED:
            p = head.rfind(a)
            if p >= 0:
                ends.append((p + len(a), p))
        if not ends:
            continue
        end, start = max(ends)
        # 名称起点 = 上一个锚点结束位之后
        prev_end = 0
        for a in _ANCHER_SORTED:
            p = head.rfind(a, 0, start)
            if p >= 0 and p + len(a) > prev_end:
                prev_end = p + len(a)
        name = head[prev_end:end]
        if acceptable(name):
            it = index.setdefault(name, {'count': 0, 'first': None})
            it['count'] += 1
            if it['first'] is None:
                it['first'] = 'L%d' % no

def split_anchor(text):
    """先按句读断串（夹注混正文处），再在每个锚点（长锚优先）后断开。"""
    out = []
    for part in re.split(r"[，。；：,;.]+", text):
        if not part:
            continue
        pieces, buf, i = [], '', 0
        while i < len(part):
            hit = next((a for a in B.ALL_ANCHORS if part.startswith(a, i)), None)
            if hit:
                buf += hit; i += len(hit)
                pieces.append(buf); buf = ''
            else:
                buf += part[i]; i += 1
        if buf:
            pieces.append(buf)
        out.extend(pieces)
    return out

# 3/4) 迭代：建树 → 拆 pending → 回填 → 重跑
for rnd in range(1, 6):
    seq = [(no, lines[no]) for no in sorted(lines)]
    tree = B.build_candidate_tree(seq, 'new', '66', index)
    pend = []
    def w(n):
        if n.get('ai_review') == 'required':
            pend.append(n)
        for c in n.get('children') or []:
            w(c)
    w(tree['root'])
    print('round %d: pending=%d index=%d' % (rnd, len(pend), len(index)))
    if not pend:
        break
    # 特判：L211 南京子树总标题行（非卫列）→ rename 为块节点，不拆分
    for n in list(pend):
        if n['src_loc'] == '卷66-L211':
            n['name'] = '南京卫所'
            n['level'] = '块'
            n.pop('ai_review', None); n.pop('why', None)
            n['review_action'] = 'rename'
            n['review_note'] = 'AI 复核：◎南京卫所亲军卫 为南京子树总标题（§16-8 三子树分立：北京五府/南京/羁縻）'
            pend.remove(n)
            print('  L211 title rename applied')
    added = 0
    for n in pend:
        ln = int(n['src_loc'].split('L')[1])
        text = n['name']
        if text not in lines[ln].replace(' ', '') and text not in lines[ln]:
            print('  !! not-in-source:', n['src_loc'], text[:30]); continue
        pieces = split_anchor(text)
        for p in pieces:
            if p in ('卫', '所', '司', '站', '寨', '地面', '千户所', '群牧所', '仪卫司'):
                print('  ?? bare-suffix piece at', n['src_loc'], repr(text[:20])); continue
            if clean_name(p) and not _LEAD_GUARD.match(p):
                index.setdefault(p, {'count': 0, 'first': 'L%d' % ln})
                added += 1
            elif p not in ('卫', '所', '司') and len(p) > 2 and not clean_name(p):
                print('  drop piece:', n['src_loc'], repr(p[:16]))
    print('  backfilled names:', added)

cov = B.build_coverage(tree, [(no, lines[no]) for no in sorted(lines)], index)
# 末轮重建会丢内存改名 → 循环后统一重放（幂等）
def _find(n, pred):
    if pred(n):
        return n
    for c in n.get('children') or []:
        r = _find(c, pred)
        if r:
            return r
t211 = _find(tree['root'], lambda x: x.get('name') in ('◎南京卫所亲军卫', '南京卫所'))
if t211 is not None and t211.get('level') != '块':
    t211['name'] = '南京卫所'
    t211['level'] = '块'
    t211.pop('ai_review', None); t211.pop('why', None)
    t211['review_action'] = 'rename'
    print('  L211 rename replayed post-loop')
elif t211 is not None:
    print('  L211 already renamed in last round tree')
print('FINAL coverage:', json.dumps({k: cov[k] for k in
      ('determined_count', 'pending_count', 'segment_coverage', 'coverage_ok',
       'bracket_notes_total', 'wei_name_index_size')}, ensure_ascii=False))

# 结构复核
leafs = []
def w3(n):
    if n.get('level') in ('卫', '所', '土司', '驿', '地面', '寨'):
        leafs.append(n)
    for c in n.get('children') or []:
        w3(c)
w3(tree['root'])
bad = [x for x in leafs if x['name'] not in lines[int(x['src_loc'].split('L')[1])]]
glued = [x for x in leafs if re.search(r'[卫所].*[卫所司]', x['name'][:-1])]
print('leaf total:', len(leafs), Counter(x['level'] for x in leafs))
print('verbatim-miss:', len(bad), bad[:4])
print('glued-leaf:', len(glued), [g['name'] for g in glued[:8]])

json.dump({'index': index,
           'note': 'new段专用词典（种子=旧树%d词 + 锚点修正预扫 + pass3 AI复核回填）；原 wei_name_index.json 未动' % seed_n},
          io.open(NEW_INDEX, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
out = {'meta': {**{'vol': '66', 'list_ver': 'new', 'lines': 'L122-L251',
      'note': '规则引擎候选结果，必须经 AI 复核后方可写定稿（SKILL.md §13）'},
      'pass': 'pass3（builder 修复 + 词典从零重建）'},
      'tree': tree, 'coverage': cov}
json.dump(out, io.open(CAND, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 悬空行清单（应只剩张本/说明段）
print('to_review lines:', [x['line_no'] for x in tree['to_review']])
