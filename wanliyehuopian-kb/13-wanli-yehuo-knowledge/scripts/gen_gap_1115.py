# -*- coding: utf-8 -*-
"""卷11-15缺失条目补漏生成器: 49个item, 追加写入 _layers/*/(*_11..15.json)"""
import json, re, glob, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE)
sys.path.insert(0, os.path.join(BASE, 'scripts'))
import _kg_enums as E

LAYERS = ['ents','rules','events','appts','rels','opns','cits','mings','tmes','regs']
IDKEY = {'ents':'ent_id','rules':'rule_id','events':'event_id','appts':'appt_id','rels':'rel_id',
         'opns':'opn_id','cits':'cit_id','mings':'ming_id','tmes':'tme_id','regs':'reg_id'}

# ---------- 1. 源文本条目全文 ----------
def build_item_texts():
    t = open('assets/sources/万历野获编.txt', encoding='utf-8').read()
    vols = {'11':'●卷十一','12':'●卷十二','13':'●卷十三','14':'●卷十四','15':'●卷十五'}
    nxt  = {'11':'●卷十二','12':'●卷十三','13':'●卷十四','14':'●卷十五','15':'●卷十六'}
    texts = {}
    for v in vols:
        seg = t[t.index(vols[v]):t.index(nxt[v])]
        parts = seg.split('【')
        idx = 0
        for p in parts[1:]:
            idx += 1
            body = re.split(r'[○●]', p)[0]
            title, rest = body.split('】', 1)
            text = re.sub(r'\s+', '', '【' + title + '】' + rest)
            texts['%s-%03d' % (v, idx)] = text
    return texts

TEXTS = build_item_texts()

# ---------- 2. 现有文件加载与ID起点 ----------
def load(layer, vol):
    fp = '_layers/%s/%s_%s.json' % (layer, layer, vol)
    data = json.load(open(fp, encoding='utf-8'))
    assert isinstance(data, list), '%s_%s 不是顶层数组' % (layer, vol)
    return data

EXIST = {}
NEXT = {}
for v in ['11','12','13','14','15']:
    for L in LAYERS:
        recs = load(L, v)
        EXIST[(L, v)] = recs
        mx = 0
        for r in recs:
            tail = str(r.get(IDKEY[L], '')).rsplit('-', 1)[-1]
            if tail.isdigit():
                mx = max(mx, int(tail))
        NEXT[(L, v)] = mx + 1

ENT_COUNTER = [4400]
ENT_POOL_MAX = 4599

def next_ent():
    i = ENT_COUNTER[0]
    if i > ENT_POOL_MAX:
        raise RuntimeError('ENT pool exhausted')
    ENT_COUNTER[0] += 1
    return 'ENT-%04d' % i

new_records = {}  # (layer, vol) -> list
item_ent_ids = {}  # (item, key) -> ent_id
item_evt_ids = {}  # (item, key) -> event_id
item_tme_ids = {}  # (item, key) -> tme_id
errors = []

def eref(item, key):
    ent_id = item_ent_ids.get((item, key))
    if ent_id is None:
        errors.append('ent ref missing: %s %s' % (item, key))
        return 'ENT-4400'
    return ent_id

def erefs(item, keys):
    return [eref(item, k) for k in (keys or [])]

def evref(item, keys):
    return [item_evt_ids.get((item, k), 'EVT-??') for k in (keys or [])]

def tmeref(item, keys):
    return [item_tme_ids.get((item, k), 'YHB-TME-??') for k in (keys or [])]

def add(layer, vol, rec):
    new_records.setdefault((layer, vol), []).append(rec)

# ---------- 3. 数据定义 ----------
# ent: (key, text, role, norm=None, type='person', faction='无', career=None, conf='high', exam=None)
# 其余层字段见 add_* 函数

VOL_ITEMS = {}  # vol -> [item dicts]

def ent(e):
    k, t = e[0], e[1]
    d = dict(key=k, text=t)
    d['role'] = e[2]
    d['norm'] = e[3] if len(e) > 3 and e[3] else t
    d['type'] = e[4] if len(e) > 4 else 'person'
    d['faction'] = e[5] if len(e) > 5 else '无'
    d['career'] = e[6] if len(e) > 6 else None
    d['conf'] = e[7] if len(e) > 7 else 'high'
    d['exam'] = e[8] if len(e) > 8 else None
    return d

def process_item(item):
    vid = item['item'][:2]
    it = item['item']
    text = TEXTS.get(it, '')
    # --- ents ---
    for e in item.get('ents', []):
        d = ent(e)
        st = text.find(d['text'])
        if st < 0:
            errors.append('ent text not found: %s %r' % (it, d['text']))
            st, en = 0, len(d['text'])
        else:
            en = st + len(d['text'])
        rid = next_ent()
        item_ent_ids[(it, d['key'])] = rid
        add('ents', vid, {
            'ent_id': rid, 'item_id': it, 'text': d['text'], 'type': d['type'],
            'normalized': d['norm'], 'start': st, 'end': en, 'confidence': d['conf'],
            'source': it, 'role_in_entry': d['role'], 'faction': d['faction'],
            'exam_info': d['exam'], 'career_span': d['career']})
    # --- rules ---
    for r in item.get('rules', []):
        rid = 'RULE-%s-%03d' % (vid, NEXT[('rules', vid)]); NEXT[('rules', vid)] += 1
        add('rules', vid, {
            'rule_id': rid, 'item_id': it, 'type': r['type'], 'modals': r['modals'],
            'condition': r['cond'], 'subject': r['subj'], 'subject_ent_ids': erefs(it, r.get('srefs')),
            'action': r['action'], 'object': r['obj'], 'purpose': r.get('purpose'),
            'punishment': r.get('pun'), 'original': r['orig'], 'confidence': 'high',
            'rule_origin': r['ro'], 'actual_practice': r['ap'],
            'violation_evidence': r.get('ve'), 'time_marker': r['tm']})
    # --- events ---
    for x in item.get('events', []):
        rid = 'EVT-%s-%03d' % (vid, NEXT[('events', vid)]); NEXT[('events', vid)] += 1
        item_evt_ids[(it, x['k'])] = rid
        add('events', vid, {
            'event_id': rid, 'item_id': it, 'type': x['type'], 'who': x['who'],
            'who_ent_ids': erefs(it, x.get('wrefs')), 'action': x['action'], 'what': x['what'],
            'when': x['when'], 'where': x['where'], 'original': x['orig'],
            'event_significance': x['sig'], 'political_impact': x['impact'],
            'source_type': x['src'], 'vs_official_history': x['vs'], 'related_events': []})
    # --- appts ---
    for x in item.get('appts', []):
        rid = 'APPT-%s-%03d' % (vid, NEXT[('appts', vid)]); NEXT[('appts', vid)] += 1
        add('appts', vid, {
            'appt_id': rid, 'item_id': it, 'person': x['person'],
            'person_ent_ids': erefs(it, x['pref']), 'office': x['office'], 'office_ent_ids': [],
            'institution': x.get('inst'), 'institution_ent_ids': [], 'when': x['when'],
            'status': x['status'], 'evidence': x['evid'], 'original': x.get('orig', x['evid']),
            'appointment_context': x.get('ctx'), 'controversy': x.get('contro', '无争议'),
            'faction_implication': x.get('facimp'), 'concurrent_posts': x.get('conc', [])})
    # --- rels ---
    for x in item.get('rels', []):
        rid = 'REL-%s-%03d' % (vid, NEXT[('rels', vid)]); NEXT[('rels', vid)] += 1
        add('rels', vid, {
            'rel_id': rid, 'item_id': it, 'person_a': x['a'], 'person_a_ent_ids': erefs(it, x['aref']),
            'person_b': x['b'], 'person_b_ent_ids': erefs(it, x['bref']),
            'relation_type': x['type'], 'direction': x.get('dir', '单向'),
            'evidence': x['ev'], 'original': x.get('orig', x['ev']),
            'relationship_evolution': x.get('evol'), 'political_consequence': x.get('poly'),
            'evidence_strength': x.get('stre', '直接表述'), 'time_span': x.get('ts')})
    # --- cits ---
    for x in item.get('cits', []):
        rid = 'CIT-%s-%03d' % (vid, NEXT[('cits', vid)]); NEXT[('cits', vid)] += 1
        add('cits', vid, {
            'cit_id': rid, 'item_id': it, 'cited_work': x['work'], 'cited_work_ent_ids': [],
            'citation_type': x['ctype'], 'context': x['ctx'], 'original': x['orig'],
            'citation_purpose': x['purpose'], 'accuracy_note': x.get('acc'),
            'quoted_text': x.get('qt')})
    # --- opns ---
    for x in item.get('opns', []):
        rid = 'OPN-%s-%03d' % (vid, NEXT[('opns', vid)]); NEXT[('opns', vid)] += 1
        add('opns', vid, {
            'opn_id': rid, 'item_id': it, 'topic': x['topic'], 'stance': x['stance'],
            'argument': x['arg'], 'original': x['orig'], 'commentary_type': x['ctype'],
            'target_entities': erefs(it, x.get('tgt')), 'evidence_cited': x.get('evc'),
            'historical_parallel': x.get('hp'), 'tone': x['tone'],
            'firsthand_witness': x.get('fw', '不详')})
    # --- mings ---
    for x in item.get('mings', []):
        rid = 'MING-%s-%03d' % (vid, NEXT[('mings', vid)]); NEXT[('mings', vid)] += 1
        add('mings', vid, {
            'ming_id': rid, 'item_id': it, 'era': x['era'], 'who': x['who'],
            'who_ent_ids': erefs(it, x.get('wrefs')), 'what': x['what'], 'when': x['when'],
            'where': x.get('where'), 'category': x['cat'], 'first_person': x.get('fp', False),
            'ref_events': evref(it, x.get('refs')), 'original': x['orig'],
            'reign_focus': x['rf'], 'firsthand_witness': x['fw'],
            'supplements_what': x.get('supp')})
    # --- tmes ---
    for x in item.get('tmes', []):
        rid = 'YHB-TME-%s-%03d' % (vid, NEXT[('tmes', vid)]); NEXT[('tmes', vid)] += 1
        item_tme_ids[(it, x['k'])] = rid
        order = E.REIGN_ORDER.get(x['reign'])
        add('tmes', vid, {
            'tme_id': rid, 'item_id': it,
            'era': {'dynasty': x.get('dyn', '明'), 'reign': x['reign'], 'year': x.get('year'),
                    'order': order, 'text': x['text']},
            'target': x['target'], 'target_ent_ids': erefs(it, x.get('trefs')),
            'action': x['action'], 'content': x['content'], 'category': x['cat'],
            'related_evo': item_tme_ids.get((it, x['evo'])) if x.get('evo') else None,
            'related_org': x.get('org'), 'ref_item': it, 'original': x['orig'],
            'institution_target': x.get('inst', x['target']), 'cause': x.get('cause'),
            'before_after': {'before': x.get('before'), 'after': x.get('after')}})
    # --- regs ---
    for x in item.get('regs', []):
        rid = 'REG-%s-%03d' % (vid, NEXT[('regs', vid)]); NEXT[('regs', vid)] += 1
        add('regs', vid, {
            'reg_id': rid, 'item_id': it, 'name': x['name'], 'category': x['cat'],
            'establishment': x['est'], 'tme_ids': tmeref(it, x.get('trefs')),
            'content_summary': x['sum'], 'actual_practice': x['ap'],
            'abuses_reform': x.get('abuse', []), 'key_figures': erefs(it, x.get('kf')),
            'original': x['orig'], 'vs_official_history': x['vs']})

# ---------- 4. 数据导入、处理、覆盖断言 ----------
import gap_data_a, gap_data_b, gap_data_c, gap_data_d
DATA = (gap_data_a.DATA_PART + gap_data_b.DATA_PART +
        gap_data_c.DATA_PART + gap_data_d.DATA_PART)

for item in DATA:
    process_item(item)

gap = json.load(open('_gap_missing.json', encoding='utf-8'))
missing = set()
for v in ['11', '12', '13', '14', '15']:
    missing |= set(gap[v])
covered = set(i['item'] for i in DATA)
cov_err = sorted(missing ^ covered)
if cov_err:
    errors.append('coverage mismatch: %s' % cov_err)
print('items in gap list: %d, items in data: %d, symmetric diff: %s'
      % (len(missing), len(covered), cov_err))

if errors:
    print('ERRORS (%d), ABORT before write:' % len(errors))
    for e in errors:
        print('  ', e)
    raise SystemExit(1)

# ---------- 5. 回写（保留旧记录，追加新记录，顶层数组） ----------
total_new = 0
per = {}
for (layer, vol) in [(L, v) for v in ['11','12','13','14','15'] for L in LAYERS]:
    recs = new_records.get((layer, vol), [])
    if not recs:
        continue
    old = EXIST[(layer, vol)]
    allrecs = old + recs
    fp = '_layers/%s/%s_%s.json' % (layer, layer, vol)
    lines = ['[']
    for i, r in enumerate(allrecs):
        lines.append('  ' + json.dumps(r, ensure_ascii=False, separators=(',', ':'))
                     + (',' if i < len(allrecs) - 1 else ''))
    lines.append(']')
    with open(fp, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(lines) + '\n')
    total_new += len(recs)
    per[(vol, layer)] = len(recs)

print('ENT used: %d, last=%s, pool max allowed ENT-4599' % (ENT_COUNTER[0] - 4400, 'ENT-%04d' % (ENT_COUNTER[0] - 1)))
print('total new records: %d' % total_new)
for (vol, layer), n in sorted(per.items()):
    print('vol%s %-7s +%d' % (vol, layer, n))
print('errors: 0')
print('DONE')
