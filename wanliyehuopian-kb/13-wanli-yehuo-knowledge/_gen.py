# -*- coding: utf-8 -*-
"""Append gap-fill records for volumes 02-05 of 《万历野获编》.
Existing records are preserved byte-identical: new single-line JSON records are
inserted before the records-array close bracket."""
import json, re, os
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

E = {}
exec(open('scripts/_kg_enums.py', encoding='utf-8').read(), E)
ENTITY_TYPES=set(E['ENTITY_TYPES']); ENTRY_ROLES=set(E['ENTRY_ROLES'])
FACTIONS=set(E['FACTIONS']); CONF=set(E['CONFIDENCE'])
RULE_TYPES=set(E['RULE_TYPES']); RULE_ORIGINS=set(E['RULE_ORIGINS']); ACTUAL_PRACTICE=set(E['ACTUAL_PRACTICE'])
EVENT_TYPES=set(E['EVENT_TYPES']); EVENT_SIG=set(E['EVENT_SIGNIFICANCE']); SOURCE_TYPES=set(E['SOURCE_TYPES']); VS=set(E['VS_OFFICIAL_HISTORY'])
APPT_STATUS=set(E['APPT_STATUS']); CONTROVERSY=set(E['CONTROVERSY'])
REL_TYPES=set(E['RELATION_TYPES']); DIRECTION=set(E['DIRECTION']); EV_STR=set(E['EVIDENCE_STRENGTH'])
CIT_TYPES=set(E['CITATION_TYPES']); CIT_PURP=set(E['CITATION_PURPOSES'])
STANCES=set(E['STANCES']); COMM_TYPES=set(E['COMMENTARY_TYPES']); TONES=set(E['TONES']); FIRSTHAND=set(E['FIRSTHAND'])
MING_CATS=set(E['MING_CATEGORIES']); REIGN_FOCUS=set(E['REIGN_FOCUS'])
TME_CATS=set(E['TME_CATEGORIES']); REIGN_ORDER=E['REIGN_ORDER']
REG_CATS=set(E['REG_CATEGORIES'])

reg=json.load(open('_item_registry.json',encoding='utf-8'))['records']
ORIG={r['item_id']:r['original'] for r in reg}

LAYER_KEY={'ents':'ent_id','rules':'rule_id','events':'event_id','appts':'appt_id','rels':'rel_id',
 'cits':'cit_id','opns':'opn_id','mings':'ming_id','tmes':'tme_id','regs':'reg_id'}

NEW=defaultdict(lambda: defaultdict(list))  # vol->layer->[rec]
_cnt={}
def nid(vol,layer):
    path=f'_layers/{layer}/{layer}_{vol}.json'
    key=LAYER_KEY[layer]
    if (vol,layer) not in _cnt:
        m=0
        if os.path.exists(path):
            d=json.load(open(path,encoding='utf-8')); recs=d['records'] if isinstance(d,dict) else d
            for r in recs:
                mm=re.findall(r'(\d+)',r.get(key,''))
                if mm: m=max(m,int(mm[-1]))
        _cnt[(vol,layer)]=m
    _cnt[(vol,layer)]+=1
    n=_cnt[(vol,layer)]
    if layer=='ents': return 'ENT-%04d'%n
    if layer=='tmes': return 'YHB-TME-%s-%03d'%(vol,n)
    return '%s-%s-%03d'%({'rules':'RULE','events':'EVT','appts':'APPT','rels':'REL','cits':'CIT','opns':'OPN','mings':'MING','regs':'REG'}[layer],vol,n)

ENT=[4000]
def next_ent():
    v=ENT[0]; ENT[0]+=1
    assert v<=4199,'ENT pool exhausted'
    return 'ENT-%04d'%v

def en(val,allowed,f,layer,iid):
    assert val in allowed, f'ENUM {layer}.{f}={val!r} bad @ {iid}'

NEW_IDS=set()
def _add(vol,layer,rec):
    validate(layer,rec)
    NEW[vol][layer].append(rec)

def validate(layer,r):
    iid=r['item_id']
    if layer=='ents':
        en(r['type'],ENTITY_TYPES,'type',layer,iid)
        for x in r['role_in_entry']: en(x,ENTRY_ROLES,'role',layer,iid)
        en(r['faction'],FACTIONS,'faction',layer,iid); en(r['confidence'],CONF,'confidence',layer,iid)
    elif layer=='rules':
        en(r['type'],RULE_TYPES,'type',layer,iid); en(r['rule_origin'],RULE_ORIGINS,'rule_origin',layer,iid)
        en(r['actual_practice'],ACTUAL_PRACTICE,'actual_practice',layer,iid); en(r['confidence'],CONF,'confidence',layer,iid)
    elif layer=='events':
        assert r.get('event_id'), 'events need event_id'
        en(r['type'],EVENT_TYPES,'type',layer,iid); en(r['event_significance'],EVENT_SIG,'event_significance',layer,iid)
        en(r['source_type'],SOURCE_TYPES,'source_type',layer,iid); en(r['vs_official_history'],VS,'vs_official_history',layer,iid)
    elif layer=='appts':
        en(r['status'],APPT_STATUS,'status',layer,iid); en(r['controversy'],CONTROVERSY,'controversy',layer,iid)
    elif layer=='rels':
        en(r['relation_type'],REL_TYPES,'relation_type',layer,iid); en(r['direction'],DIRECTION,'direction',layer,iid)
        en(r['evidence_strength'],EV_STR,'evidence_strength',layer,iid)
    elif layer=='cits':
        en(r['citation_type'],CIT_TYPES,'citation_type',layer,iid); en(r['citation_purpose'],CIT_PURP,'citation_purpose',layer,iid)
    elif layer=='opns':
        en(r['stance'],STANCES,'stance',layer,iid); en(r['commentary_type'],COMM_TYPES,'commentary_type',layer,iid)
        en(r['tone'],TONES,'tone',layer,iid); en(r['firsthand_witness'],FIRSTHAND,'firsthand_witness',layer,iid)
    elif layer=='mings':
        en(r['category'],MING_CATS,'category',layer,iid); en(r['reign_focus'],REIGN_FOCUS,'reign_focus',layer,iid)
        en(r['firsthand_witness'],FIRSTHAND,'firsthand_witness',layer,iid)
    elif layer=='tmes':
        en(r['category'],TME_CATS,'category',layer,iid); en(r['era']['reign'],set(REIGN_ORDER),'era.reign',layer,iid)
    elif layer=='regs':
        en(r['category'],REG_CATS,'category',layer,iid); en(r['vs_official_history'],VS,'vs_official_history',layer,iid)

def ent_ref(iids,ents):
    return [ents[i] for i in iids]

def build(item, ents, events=None, tmes=None, rules=None, appts=None, rels=None,
          cits=None, opns=None, mings=None, regs=None):
    vol=item.split('-')[0]; o=ORIG[item]
    eids=[]
    for e in ents:
        eid=next_ent(); eids.append(eid)
        st=o.find(e['text'])
        rec={'ent_id':eid,'item_id':item,'text':e['text'],'type':e['type'],'normalized':e['normalized'],
             'start':st if st>=0 else 0,'end':(st+len(e['text'])) if st>=0 else len(e['text']),
             'confidence':e.get('conf','high'),'source':item,'role_in_entry':e['role'],
             'faction':e.get('faction','无'),'exam_info':e.get('exam'),'career_span':e.get('career')}
        _add(vol,'ents',rec)
    # events (assign ids first so mings can ref)
    ev_ids=[]
    for x in (events or []):
        eid=nid(vol,'events'); ev_ids.append(eid)
        rec={'event_id':eid,'item_id':item,'type':x['type'],'who':x['who'],
             'who_ent_ids':ent_ref(x['who_e'],eids),'action':x['action'],'what':x['what'],
             'when':x['when'],'where':x['where'],'original':x['original'],
             'event_significance':x['sig'],'political_impact':x.get('impact',''),
             'source_type':x.get('src','文献转引'),'vs_official_history':x.get('vs','未考'),
             'related_events':x.get('rel',[])}
        _add(vol,'events',rec)
    tme_ids=[]
    for x in (tmes or []):
        tid=nid(vol,'tmes'); tme_ids.append(tid)
        reign=x['reign']
        rec={'tme_id':tid,'item_id':item,'era':{'dynasty':'明','reign':reign,'year':x['year'],
             'order':REIGN_ORDER[reign],'text':x['era_text']},'target':x['target'],
             'target_ent_ids':ent_ref(x.get('target_e',[]),eids),'action':x['action'],
             'content':x['content'],'category':x['category'],'related_evo':x.get('evo'),
             'related_org':x.get('org'),'ref_item':item,'original':x['original'],
             'institution_target':x['target'],'cause':x.get('cause'),
             'before_after':{'before':x.get('before'),'after':x.get('after')}}
        _add(vol,'tmes',rec)
    for x in (rules or []):
        rid=nid(vol,'rules')
        rec={'rule_id':rid,'item_id':item,'type':x['type'],'modals':x['modals'],
             'condition':x['condition'],'subject':x['subject'],
             'subject_ent_ids':ent_ref(x.get('subj',[]),eids),'action':x['action'],
             'object':x.get('object'),'purpose':x.get('purpose'),'punishment':x.get('punish'),
             'original':x['original'],'confidence':x.get('conf','high'),
             'rule_origin':x['origin'],'actual_practice':x['practice'],
             'violation_evidence':x.get('viol'),'time_marker':x.get('time')}
        _add(vol,'rules',rec)
    for x in (appts or []):
        aid=nid(vol,'appts')
        rec={'appt_id':aid,'item_id':item,'person':x['person'],'person_ent_ids':ent_ref(x['person_e'],eids),
             'office':x['office'],'office_ent_ids':ent_ref(x.get('office_e',[]),eids),
             'institution':x.get('inst',''),'institution_ent_ids':ent_ref(x.get('inst_e',[]),eids),
             'when':x['when'],'status':x['status'],'evidence':x.get('ev',''),
             'original':x['original'],'appointment_context':x.get('ctx',''),
             'controversy':x.get('cont','无争议'),'faction_implication':x.get('fac'),
             'concurrent_posts':x.get('conc',[])}
        _add(vol,'appts',rec)
    for x in (rels or []):
        rid=nid(vol,'rels')
        rec={'rel_id':rid,'item_id':item,'person_a':x['a'],'person_a_ent_ids':ent_ref(x['a_e'],eids),
             'person_b':x['b'],'person_b_ent_ids':ent_ref(x['b_e'],eids),
             'relation_type':x['rel'],'direction':x.get('dir','单向'),'evidence':x.get('ev',''),
             'original':x['original'],'relationship_evolution':x.get('evo'),
             'political_consequence':x.get('cons'),'evidence_strength':x.get('str','直接表述'),
             'time_span':x.get('time')}
        _add(vol,'rels',rec)
    for x in (cits or []):
        cid=nid(vol,'cits')
        rec={'cit_id':cid,'item_id':item,'cited_work':x['work'],
             'cited_work_ent_ids':ent_ref(x.get('work_e',[]),eids),'citation_type':x['ctype'],
             'context':x['context'],'original':x['original'],'citation_purpose':x['purpose'],
             'accuracy_note':x.get('note'),'quoted_text':x.get('quoted')}
        _add(vol,'cits',rec)
    for x in (opns or []):
        oid=nid(vol,'opns')
        rec={'opn_id':oid,'item_id':item,'topic':x['topic'],'stance':x['stance'],
             'argument':x['arg'],'original':x['original'],'commentary_type':x['ctype'],
             'target_entities':ent_ref(x.get('tgt',[]),eids),'evidence_cited':x.get('ev'),
             'historical_parallel':x.get('par'),'tone':x['tone'],
             'firsthand_witness':x.get('fw','不详')}
        _add(vol,'opns',rec)
    for x in (mings or []):
        mid=nid(vol,'mings')
        rec={'ming_id':mid,'item_id':item,'era':x['era'],'who':x['who'],
             'who_ent_ids':ent_ref(x.get('who_e',[]),eids),
             'what':x['what'],'when':x['when'],'where':x.get('where',''),
             'category':x['category'],'first_person':x.get('fp',False),
             'ref_events':[ev_ids[i] for i in x.get('ref_ev',[])],'original':x['original'],
             'reign_focus':x['reign'],'firsthand_witness':x.get('fw','传闻'),
             'supplements_what':x.get('sup')}
        _add(vol,'mings',rec)
    for x in (regs or []):
        gid=nid(vol,'regs')
        rec={'reg_id':gid,'item_id':item,'name':x['name'],'category':x['category'],
             'establishment':x['est'],'tme_ids':[tme_ids[i] for i in x.get('tme',[])],
             'content_summary':x['content'],'actual_practice':x.get('practice',''),
             'abuses_reform':x.get('abuses',[]),'key_figures':ent_ref(x.get('key',[]),eids),
             'original':x['original'],'vs_official_history':x.get('vs','未考')}
        _add(vol,'regs',rec)

# ---- entity helper
def PE(text,norm=None,role=('主体',),**kw):
    d={'text':text,'type':'person','normalized':norm or text,'role':list(role)}
    d.update(kw); return d
def XE(text,typ,role=('客体',),**kw):
    d={'text':text,'type':typ,'normalized':kw.pop('norm',text),'role':list(role)}
    d.update(kw); return d

import specs  # noqa  (module holding all 41 build() calls)
specs.run(build,PE,XE)

# ---- write out
for vol in ('02','03','04','05'):
    for layer,recs in NEW[vol].items():
        path=f'_layers/{layer}/{layer}_{vol}.json'
        text=open(path,encoding='utf-8',newline='').read()
        nl='\r\n' if '\r\n' in text else '\n'
        close=text.rfind(']'); j=close-1
        while text[j].isspace(): j-=1
        assert text[j]=='}', path
        lines=[json.dumps(r,ensure_ascii=False,separators=(',',':')) for r in recs]
        add=','+(','+nl+'    ').join(['']+lines)
        open(path,'w',encoding='utf-8',newline='').write(text[:j+1]+add+text[j+1:])

# report
import collections
cnt=collections.defaultdict(int)
for vol in ('02','03','04','05'):
    for layer,recs in NEW[vol].items():
        cnt[(vol,layer)]=len(recs)
print(json.dumps({f'{v}/{l}':n for (v,l),n in sorted(cnt.items())},ensure_ascii=False,indent=1))
print('ENT used:',ENT[0]-4000,'first 4000 last',ENT[0]-1)
