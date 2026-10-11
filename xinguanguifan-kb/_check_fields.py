# -*- coding: utf-8 -*-
import json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = os.path.dirname(os.path.abspath(__file__))     # 项目根：脚本自身位置推导
def load(rel):
    return json.load(open(os.path.join(BASE, rel), encoding='utf-8'))
r = load(r'新官轨范_规则_ai\归一_汇总.json')['rules']
p = load(r'新官轨范_流程_ai\归一_汇总.json')['processes']
e = load(r'新官轨范_事件_ai\归一_汇总.json')['events']
s = load(r'新官轨范_结构_ai\归一_汇总.json')
out = []
out.append('RULE keys: %s' % sorted(r[0].keys()))
out.append('RULE[0]: type=%s modals=%s subject_ent_ids=%s' % (r[0].get('type'), r[0].get('modals'), r[0].get('subject_ent_ids')))
types = {}
for x in r:
    types[x.get('type')] = types.get(x.get('type'), 0) + 1
out.append('RULE type 分布: %s' % types)
out.append('PROC keys: %s' % sorted(p[0].keys()))
out.append('PROC[0]: event_type=%s steps=%d events=%s' % (p[0].get('event_type'), len(p[0].get('steps', [])), p[0].get('events')))
out.append('EVENT keys: %s' % sorted(e[0].keys()))
out.append('EVENT[0]: type=%s who_ent_ids=%s' % (e[0].get('type'), e[0].get('who_ent_ids')))
ev_types = {}
for x in e:
    ev_types[x.get('type')] = ev_types.get(x.get('type'), 0) + 1
out.append('EVENT type 分布: %s' % ev_types)
secs = {}
for sec in ['ledgers', 'times', 'docs', 'actors', 'frauds']:
    arr = s.get(sec, [])
    secs[sec] = len(arr)
    if arr:
        out.append('STRUCT %s[0] keys: %s' % (sec, sorted(arr[0].keys())))
out.append('STRUCT 维度数量: %s' % secs)
# join 结构
j = load(r'_kg_join.json')['entries'][0]
out.append('JOIN[0] keys: %s' % sorted(j.keys()))
open(os.path.join(BASE, '_check_fields.txt'), 'w', encoding='utf-8').write('\n'.join(out))
