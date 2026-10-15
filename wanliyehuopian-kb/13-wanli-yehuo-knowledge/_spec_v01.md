================================================================================
万历野获编 卷01 缺口补全 —— 撰写规范（给撰写者的唯一契约）
================================================================================

【产出】一个 Python 文件片段（不要写 import / 不要写 def），内容为按条目顺序追加
的层记录构造调用。最终由 build(g) 内联执行，g 提供全部构造器。

【可用的构造器（精确签名，照抄参数名）】

E(item, text, norm, typ="person", roles=("关联人物",), faction="无",
  exam=None, span=None, conf="high")
   -> 返回 ent 对象；**必须把返回值收集进列表，最后 ents += [...]**，不能丢弃
   text 必须是该条目源文（去空白后）的**逐字子串**；norm 是标准化名（不必是原文）
   typ ∈ ENTITY_TYPES；roles 是 tuple，每项 ∈ ENTRY_ROLES；faction ∈ FACTIONS
   span 是时代标记如 "洪武"/"嘉靖"（自由文本）

RULE(rid, item, typ, modals, condition, subject, action, original,
     origin, practice, tmark, subj_ents=(), obj=None, purpose=None,
     punishment=None, conf="high", viol=None)
   rid 用 rid("rules", V, "RULE") 生成
   typ ∈ RULE_TYPES；modals 是 list；origin ∈ RULE_ORIGINS；
   practice ∈ ACTUAL_PRACTICE **只能填裸 key，绝不能带句号后的解释文字**
   original 必须是源文逐字子串（长文可用「…」连接多段，每段都须逐字）

EVT(eid, item, typ, who, action, what, when, where, original,
    sig, impact, stype, vs, who_ents=(), related=())
   typ ∈ EVENT_TYPES；**sig ∈ EVENT_SIGNIFICANCE 的 key（重大政治/制度变动/
   人物转折/一般掌故/轶闻）——注意不是 value（不是「重大政治事件」）**
   stype ∈ SOURCE_TYPES（亲历/传闻/文献转引/综合）
   vs ∈ VS_OFFICIAL_HISTORY

APPT(aid, item, person, office, when, status, evidence, original,
     person_ents=(), office_ents=(), inst=None, inst_ents=(), ctx=None,
     contro="无争议", faction_impl=None, concurrent=())
   **参数名是 faction_impl，不是 faction**（输出键为 faction_implication）
   status ∈ APPT_STATUS；contro ∈ CONTROVERSY

REL(rid, item, pa, pb, rtype, direction, evidence, original,
    pa_ents=(), pb_ents=(), evo=None, conseq=None, strength="直接表述", span=None)
   rtype ∈ RELATION_TYPES；direction ∈ DIRECTION；strength ∈ EVIDENCE_STRENGTH

CIT(cid, item, work, ctype, context, original, purpose, work_ents=(), acc=None, quoted=None)
   ctype ∈ CITATION_TYPES；purpose ∈ CITATION_PURPOSES

OPN(oid, item, topic, stance, argument, original, ctype, tone, fw,
    targets=(), ev=None, parallel=None)
   stance ∈ STANCES（肯定/否定/怀疑/讽刺/中立）—— **「惋惜」属 TONES，不是 STANCES**
   ctype ∈ COMMENTARY_TYPES；tone ∈ TONES
   fw ∈ FIRSTHAND（亲历/亲闻/传闻/不详）—— **不是 SOURCE_TYPES**

MING(mid, item, era, who, what, when, where, category, original,
     reign_focus, fw, who_ents=(), ref_evts=(), first_person=False, supp=None)
   category ∈ MING_CATEGORIES（朝政/人物/科举/风俗/灾异/亲历见闻/制度/边政/军事/社会/文化/宗教/其他）
   reign_focus ∈ REIGN_FOCUS；fw ∈ FIRSTHAND

TME(tid, item, era, target, action, content, category, original,
    target_ents=(), rel_evo=None, rel_org=None, inst_target=None,
    cause=None, before=None, after=None)
   tid 用 tid(V) 生成；category ∈ TME_CATEGORIES

REG2(rid, item, name, category, establishment, summary, practice, original,
     vs, tme_ids=(), abuses=(), figures=())
   category ∈ REG_CATEGORIES（官制/科举/礼制/军事/财政/司法/边政/宦官/宗室/其他）
   —— **没有「文化」，要填「其他」**
   practice ∈ ACTUAL_PRACTICE；vs ∈ VS_OFFICIAL_HISTORY

【ID 生成】rid("rules"|"events"|"appts"|"rels"|"opns"|"cits"|"mings"|"regs", V, "RULE"|"EVT"|...)
卷01 起始序号：rules=3, events=5, appts=3, rels=2, opns=5, cits=2, mings=6, tmes=12, regs=4
（脚本已内置，直接调用 rid(...) / tid(V) 即可）

【add】add("events", V, [...]) / add("rules", V, [...]) 等；ents 用 go() 收口。

【硬性纪律】
1. **溯源**：所有 original / evidence / quoted_text / ent.text 必须是该 item 源文段
   （去空白后）的逐字子串。长文可用「…」分多段，每段都须逐字。**绝不允许编造或
   改写原文用字**（含标点：是「、」就不要写「，」）。
2. **枚举只用 key**：见上，任何 value 形态（带「事件」后缀、「惋惜」、「文化」、
   「文献转引」填进 fw 位）都会导致校验失败。
3. **ent.text 必须是源文里真实出现的字面**：源文写「上」就不要写「太祖」，
   源文写「萼」就不要写「桂萼」。
4. 条目顺序严格按 01-006 .. 01-053。

【ENT 池】无需管理，E() 自动分配。
================================================================================