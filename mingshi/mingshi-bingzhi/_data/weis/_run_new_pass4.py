# -*- coding: utf-8 -*-
"""后定树 pass4（AI 复核批次 1 回填 + builder 漏采修复后重跑）：

  前置修复（builder `_weisuo_builder.py`）：
    ⑤ dense_head——无括号夹注长卫列行（L142 陕西都司 / L154 广西都司 /
      L185 湖广都司）原整行误判说明段，**整行漏采 90+ 卫所**（坑 #55 最重实例）。
  本脚本动作：
    1) 词典基线 = pass3 产物 wei_name_index_new.json
    2) AI 复核批次 1：pending 粘连段**逐条对照源行定边界**，卫名显式回填
       （_LEAD_GUARD 会拒收「卫辉前千户所/所力卫」类首字即锚的正名，故显式入典）
    3) 迭代建树至 pending=0（拆分器只作兜底，边界以本批复核名单为准）
    4) 逐字源行回验 + 粘串体检 + 计数对账
  校验：每个回填名必须**逐字出现在所引源行**，否则报错退出。
"""
import json, io, sys, re
from collections import Counter

sys.path.insert(0, 'assets/tools')
sys.path.insert(0, 'scripts')
import _weisuo_builder as B
from _common import atomic_write_json

OLD_INDEX = '_data/weis/wei_name_index.json'
NEW_INDEX = '_data/weis/wei_name_index_new.json'
CAND = '_data/weis/candidates_66_new.json'

_ANCHER_SORTED = sorted(B.ALL_ANCHORS + ['使司', '指挥使司', '留守司', '都司'],
                        key=len, reverse=True)


def clean_name(name):
    if not name or len(name) > 14:
        return False
    if re.search(r"[，。；：,;.()（）\s]", name):
        return False
    anchor = next((a for a in _ANCHER_SORTED if name.endswith(a)), None)
    if anchor is None:
        return False
    body = name[:-len(anchor)]
    if not body:
        return False
    return not re.search(r'[卫站寨]|地面', body) and not ('所' in body and not body.endswith('千户'))


_LEAD_GUARD = re.compile(r'^(?:地面|千户所|使司|群牧所|仪卫司|招讨司|安抚司|万户府|宣尉使司|'
                         r'宣慰使司|长官司|都司|指挥使司|[卫所司站寨])')


def split_anchor(text):
    out = []
    for part in re.split(r"[，。；：,;.]+", text):
        if not part:
            continue
        pieces, buf, i = [], '', 0
        while i < len(part):
            hit = next((a for a in B.ALL_ANCHORS if part.startswith(a, i)), None)
            if hit:
                buf += hit
                i += len(hit)
                pieces.append(buf)
                buf = ''
            else:
                buf += part[i]
                i += 1
        if buf:
            pieces.append(buf)
        out.extend(pieces)
    return out


# ---------------------------------------------------------------- AI 复核批次 1
# 每条 = (源行号, [按源行顺序的卫/所/土司全名])，边界由 AI 对照原文判定。
REVIEWED = [
    (148, ['潘斡寨长官司', '八郎安抚司', '阿角寨安抚司', '麻儿匝安抚司', '芒儿者安抚司']),
    (156, ['十八寨千户所', '通海前前千户所', '通海右右千户所',
           '永平前前千户所', '永平后后千户所']),
    (160, ['黄平千户所', '普市千户所', '重安千户所', '安龙千户所', '白撒千户所', '摩泥千户所',
           '关索岭千户所', '阿落密千户所', '平夷千户所', '安南千户所', '乐民千户所', '七星关千户所']),
    (162, ['新添长官司', '小平伐长官司', '把平寨长官司', '丹平长官司', '丹行长官司']),
    (172, ['卫辉前千户所', '林县千户所', '邓州前千户所', '唐县右千户所',
           '周府仪卫司', '唐府仪卫司', '伊府仪卫司', '赵府仪卫司', '郑府仪卫司',
           '崇府仪卫司', '徽府仪卫司', '赵府群牧所', '郑府群牧所', '崇府群牧所', '徽府群牧所']),
    (181, ['新化亮寨千户所', '隆里千户所', '平茶屯千户所',
           '楚府仪卫司', '荆府仪卫司', '雍府仪卫司', '荣府仪卫司', '岷府仪卫司', '吉府仪卫司',
           '荆府群牧所', '雍府群牧所', '荣府群牧所', '吉府群牧所']),
    (183, ['五寨长官司', '筸子坪长官司', '田家洞长官司', '保靖州军民宣慰使司', '东乡五路安抚司']),
    (227, ['薄罗卫', '塔麻所卫', '布儿哈卫', '亦思察河卫', '失剌卫', '卜忽秃卫', '撒里卫', '你实卫',
            '平河卫', '忽里吉山卫', '阿乞卫', '台郎卫', '塞克卫', '拜苦卫', '所力卫', '巴里卫',
            '塔纳卫', '木郎卫', '额克卫', '勒伏卫', '式木卫', '树哈卫', '肥哈答卫', '盖千卫',
            '英秃卫', '乞忽卫', '阿林卫', '哈儿速卫', '巴答卫', '脱木卫', '忽把卫', '速哈儿卫',
            '马失卫', '塔赛卫', '劄里卫', '者哈卫', '恨克卫', '哈失卫', '交枝卫', '葛卫',
            '艾答卫', '亦蛮卫', '哈察卫', '革出卫', '卜答卫', '蜀河卫', '秃里赤山卫', '赛因卫',
            '忙哈卫']),
    (243, ['陇答卫指挥使司']),
    (241, ['乌思藏都指挥使司', '朵甘卫都指挥使司']),
    (249, ['沙儿可万户府', '乃竹万户府', '罗思端万户府', '别思麻万户府']),
]

index = dict(json.load(io.open(NEW_INDEX, encoding='utf-8'))['index'])
base_n = len(index)
lines = {no: ln for no, ln in B.load_source_lines('66', 122, 251)}

added = 0
for ln, names in REVIEWED:
    src = lines[ln]
    for nm in names:
        if nm not in src:
            print('FATAL 非逐字命中：L%d %s' % (ln, nm))
            sys.exit(1)
        if nm not in index:
            index[nm] = {'count': 0, 'first': 'L%d' % ln, 'ai_reviewed': True}
            added += 1
print('AI 复核批次 1 回填：%d 词（词典 %d → %d）' % (added, base_n, len(index)))

# ---------------------------------------------------------------- 迭代建树
for rnd in range(1, 7):
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
    extra = 0
    for n in pend:
        ln = int(n['src_loc'].split('L')[1])
        text = n['name']
        if text not in lines[ln]:
            print('  !! not-in-source:', n['src_loc'], text[:30])
            continue
        for p in split_anchor(text):
            if clean_name(p) and not _LEAD_GUARD.match(p) and p not in index:
                index[p] = {'count': 0, 'first': 'L%d' % ln}
                extra += 1
    if extra:
        print('  拆分器兜底回填：%d 词' % extra)

# ---------------------------------------------------------------- 末轮改名重放
def _find(n, pred):
    if pred(n):
        return n
    for c in n.get('children') or []:
        r = _find(c, pred)
        if r:
            return r


t211 = None  # 南京子树容器由 builder 直接建（block_title「南京卫所亲军卫」）


def glued_name(nm):
    """粘串体检：拆分器切出 **≥3** 个完整名段（≥3 字、以锚结尾）→ 粘连串。
    （2 段不算：「朵甘卫都指挥使司」「十八寨千户所」类复合专名会被误判。）"""
    ps = split_anchor(nm)
    return len([p for p in ps if p.endswith(tuple(B.ALL_ANCHORS)) and len(p) >= 3]) >= 3


# ---------------------------------------------------------------- 对账
cov = B.build_coverage(tree, [(no, lines[no]) for no in sorted(lines)], index)
print('FINAL coverage:', json.dumps({k: cov[k] for k in
      ('determined_count', 'pending_count', 'segment_coverage', 'coverage_ok',
       'bracket_notes_total', 'wei_name_index_size')}, ensure_ascii=False))

leafs = []


def w3(n):
    if n.get('level') in ('卫', '所', '土司', '驿', '地面', '寨'):
        leafs.append(n)
    for c in n.get('children') or []:
        w3(c)


w3(tree['root'])
bad = [x for x in leafs if x['name'] not in lines[int(x['src_loc'].split('L')[1])]]
glued = [x for x in leafs if glued_name(x['name'])]
print('leaf total:', len(leafs), Counter(x['level'] for x in leafs))
print('verbatim-miss:', len(bad), [b['name'] for b in bad[:6]])
print('glued-leaf:', len(glued), [g['name'] for g in glued[:8]])
print('to_review lines:', [x['line_no'] for x in tree['to_review']])
print('per-line pending:', Counter(x['src_loc'] for x in leafs if x.get('ai_review') == 'required'))

pend_nodes = [x for x in leafs if x.get('ai_review') == 'required']
for p in pend_nodes:
    ln = int(p['src_loc'].split('L')[1])
    src = lines[ln]
    i = src.find(p['name'])
    print('PEND', p['src_loc'], '| lvl', p['level'], '|', repr(p['name'])[:60])
    print('     ctx<<', src[max(0, i - 26):i], '【', p['name'][:26], '】', src[i + len(p['name']):i + len(p['name']) + 20])


# ------------------------------------------------ AI 复核批次 2：无括号夹注定边界
# 两处「夹注混入正文」的 pending（坑 #55 家族）由 AI 判定为**注**而非卫所名：
#   L142 岷州卫旧军民指挥使司，嘉靖二十四年添设岷州，四十年革，(后存卫)
#        → 岷州卫 一叶，其余三串全是沿革注（纪年明写，嘉靖二十四年/四十年）
#   L160 贵州前卫旧无，后设)  ← 坏括注缺左括号
#        → 贵州前卫 一叶 + 注「旧无，后设」；其后 12 个千户所为都司直属所
def _parent_of(root, node):
    stack = [root]
    while stack:
        n = stack.pop()
        for c in n.get('children') or []:
            if c is node:
                return n
            stack.append(c)
    return None


def _nodes(root, pred):
    out = []
    stack = [root]
    while stack:
        n = stack.pop()
        if pred(n):
            out.append(n)
        stack.extend(n.get('children') or [])
    return out


for nm in ('岷州卫', '贵州前卫'):
    for n in _nodes(tree['root'], lambda x, m=nm: x.get('name') == m):
        print('NODE', n['src_loc'], nm, 'notes=', n.get('notes'), 'ai=', n.get('ai_review'))

patches = []
for p in pend_nodes:
    ln = int(p['src_loc'].split('L')[1])
    if ln == 142 and p['name'] in ('嘉靖二十四年添设岷州', '四十年革'):
        parent = _parent_of(tree['root'], p)
        mz = next((c for c in parent['children'] if c.get('name') == '岷州卫'), None)
        assert mz is not None, 'L142 岷州卫叶缺失，无法归注'
        note = p['name']
        if note not in mz.get('notes', []):
            mz.setdefault('notes', []).append(note)
        mz.setdefault('note_meta', []).append({
            'from': 'AI 复核批次 2（无括号夹注，源行 L142 逐字）', 'verbatim': note})
        mz['ai_review'] = 'reviewed'
        parent['children'].remove(p)
        patches.append({'action': 'merge', 'src_loc': p['src_loc'],
                        'text': note, 'into': '岷州卫',
                        'reason': '原文「岷州卫旧军民指挥使司，嘉靖二十四年添设岷州，四十年革」'
                                  '为无括号夹注（沿革注），非独立卫所名；纪年明写可转 C14'})
    elif ln == 160 and p['name'] == '旧无':
        parent = _parent_of(tree['root'], p)
        gz = next((c for c in parent['children'] if c.get('name') == '贵州前卫'), None)
        assert gz is not None, 'L160 贵州前卫叶缺失'
        if '旧无，后设' not in gz.get('notes', []):
            gz.setdefault('notes', []).append('旧无，后设')
        gz.setdefault('note_meta', []).append(
            {'from': 'AI 复核批次 2（坏括注缺左括号，源行 L160 逐字）', 'verbatim': '旧无，后设'})
        gz['ai_review'] = 'reviewed'
        parent['children'].remove(p)
        patches.append({'action': 'merge', 'src_loc': p['src_loc'], 'text': '旧无，后设',
                        'into': '贵州前卫',
                        'reason': '原行「贵州前卫旧无，后设)」缺左括号，夹注被误切成叶；'
                                  '归并为贵州前卫沿革注（无纪年→era 未明）'})
    elif ln == 160 and p['name'].startswith('后设)'):
        parent = _parent_of(tree['root'], p)
        names = ['黄平千户所', '普市千户所', '重安千户所', '安龙千户所', '白撒千户所',
                 '摩泥千户所', '关索岭千户所', '阿落密千户所', '平夷千户所', '安南千户所',
                 '乐民千户所', '七星关千户所']
        src = lines[160]
        pos = [src.find(x) for x in names]
        assert all(i >= 0 for i in pos), 'L160 所名逐字校验失败'
        assert pos == sorted(pos), 'L160 所名顺序与源行不符'
        idx_self = parent['children'].index(p)
        parent['children'].pop(idx_self)
        for k, x in enumerate(names):
            parent['children'].insert(idx_self + k, {
                'name': x, 'level': '所', 'src_loc': '卷66-L160', 'notes': [],
                'confidence': 0.9, 'ai_review': 'reviewed',
                'review_action': 'split', 'review_note': 'AI 复核批次 2：pending 粘串逐字拆分',
                'children': []})
        patches.append({'action': 'split', 'src_loc': p['src_loc'],
                        'text': p['name'][:24] + '…', 'new_names': names,
                        'reason': '坏括注残串「后设)」剥离后为贵州都司直辖 12 千户所，逐字定界'})

# AI 复核批次 2b：切段器锚集不含「万户府」类复合尾缀 →  determined 但**四名一串**
GLUED_SPLIT = {
    '沙儿可万户府乃竹万户府罗思端万户府别思麻万户府':
        ['沙儿可万户府', '乃竹万户府', '罗思端万户府', '别思麻万户府'],
}
for n in list(leafs):
    parts = GLUED_SPLIT.get(n['name'])
    if not parts:
        continue
    parent = _parent_of(tree['root'], n)
    src = lines[int(n['src_loc'].split('L')[1])]
    pos = [src.find(x) for x in parts]
    assert all(i >= 0 for i in pos) and pos == sorted(pos), 'L249 逐字/顺序校验失败'
    k = parent['children'].index(n)
    parent['children'].pop(k)
    for j, x in enumerate(parts):
        parent['children'].insert(k + j, {
            'name': x, 'level': '土司', 'src_loc': n['src_loc'], 'notes': [],
            'confidence': 0.9, 'ai_review': 'reviewed', 'review_action': 'split',
            'review_note': 'AI 复核批次 2b：万户府复合尾缀漏锚，逐字定界',
            'children': []})
    patches.append({'action': 'split', 'src_loc': n['src_loc'], 'text': n['name'],
                    'new_names': parts,
                    'reason': '切段器尾缀锚集不含「万户府」，四名连成一串；按源行逐字拆分'})
    leafs = []
    w3(tree['root'])

if patches:
    # 复核后 stat 重算（build_coverage 读的是建树时的 stat，未反映 AI 动作）
    leafs = []
    w3(tree['root'])
    pend_left = [x for x in leafs if x.get('ai_review') == 'required']
    det2 = len(leafs) - len(pend_left)
    cov = {'determined_count': det2, 'pending_count': len(pend_left),
           'segment_coverage': round(det2 / len(leafs), 4) if leafs else 0.0,
           'coverage_min': cov['coverage_min'],
           'coverage_ok': (det2 / len(leafs) >= cov['coverage_min']) if leafs else False,
           'bracket_notes_total': sum(len(n.get('notes') or []) for n in leafs),
           'bracket_strip_rate': 1.0,
           'wei_name_index_size': cov['wei_name_index_size'],
           'src_lines': cov['src_lines']}
    tree['stat'] = {'determined': det2, 'pending': len(pend_left)}
    print('AI 复核批次 2 动作数:', len(patches), '| 剩余 pending:', len(pend_left))
    glued = [x for x in leafs if glued_name(x['name'])]
    print('glued-leaf after patch:', len(glued), [g['name'][:24] for g in glued])
    bad = [x for x in leafs if x['name'] not in lines[int(x['src_loc'].split('L')[1])]]
    print('post-patch coverage:', json.dumps(cov, ensure_ascii=False))
    print('post-patch leaf:', len(leafs), Counter(x['level'] for x in leafs))
    for p in pend_left:
        print('  STILL PEND', p['src_loc'], p['name'][:40])

if bad or glued or cov['pending_count']:
    print('未收敛：保留内存树供检查，不写盘')
    sys.exit(2)

json.dump({'index': index,
           'note': 'new段专用词典（pass3 产物 %d 词 + AI 复核批次 1 回填）；'
                   '原 wei_name_index.json（旧树 377 词）未动' % base_n},
          io.open(NEW_INDEX, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
out = {'meta': {'vol': '66', 'list_ver': 'new', 'lines': 'L122-L251',
                'note': '规则引擎候选结果，必须经 AI 复核后方可写定稿（SKILL.md §13）',
                'pass': 'pass4（dense_head 漏采修复 + AI 复核批次 1/2 定边界）',
                'review_actions': patches},
       'tree': tree, 'coverage': cov}
atomic_write_json(CAND, out)
print('written', CAND)
