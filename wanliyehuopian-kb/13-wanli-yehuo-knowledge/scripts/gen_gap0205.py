# -*- coding: utf-8 -*-
"""
卷02-05 知识工程补漏生成器（gen_gap0205.py）
为实测缺口中卷 02-05 的 41 个未覆盖条目补全各层记录并追加写回。

- 卷 02-05 层文件均为 {"records": [...]} 包裹形态（与现状一致）
- 新 ENT ID 池：ENT-4950 起（全库现有最大 ENT-4941）
- 其余层 ID 顺延各卷各层现有最大序号
- 枚举严格取自 scripts/_kg_enums.py（写入前逐个软校验，只报告不静默）
- 溯源硬校验：所有 original/evidence/quoted_text 必须是该条目源文段（去空白）的子串
  源文段按 _audit_origins.py 同款分段逻辑从 assets/sources/万历野获编.txt 重建
- ents 字段风格：卷 02-04 为风格 A（含 start/end/confidence，start/end 按去空白段内偏移）；
  卷 05 为风格 B（无 start/end/confidence），与各卷现有记录保持一致
"""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "assets" / "sources" / "万历野获编.txt"
VOLS = ["02", "03", "04", "05"]
ENT_START = 4950

REG = json.load(open(BASE / "_item_registry.json", encoding="utf-8"))["records"]

# ---------------------------------------------------------------- 源文分段
_flat = re.sub(r"[\s\u3000]", "", open(SRC, encoding="utf-8").read())
_fpos = [(m.group(1), m.start()) for m in re.finditer(r"【([^】]{1,40})】", _flat)]


def build_segments(vol):
    """registry 条目与源文【标题】锚点顺序对齐，返回 {item_id: 去空白源文段}"""
    items = [r for r in REG if r["item_id"].startswith(vol + "-")]
    ordered, idx = [], 0
    for r in items:
        t = r["entry_title"]
        j = None
        for k in range(idx, len(_fpos)):
            if _fpos[k][0] == t:
                j = k
                break
        ordered.append((r["item_id"], j))
        if j is not None:
            idx = j + 1
    out = {}
    for i, (iid, j) in enumerate(ordered):
        if j is None:
            out[iid] = None
            continue
        start = _fpos[j][1]
        end = len(_flat)
        for (iid2, j2) in ordered[i + 1:]:
            if j2 is not None:
                end = _fpos[j2][1]
                break
        out[iid] = _flat[start:end]
    return out


SEG = {v: build_segments(v) for v in VOLS}

ERRORS = []


def chk(cond, msg):
    if not cond:
        ERRORS.append(msg)


def q(item, s, field):
    """溯源校验：s 必须是该条目源文段的逐字子串"""
    seg = SEG.get(item[:2], {}).get(item)
    if seg is None:
        ERRORS.append("%s %s: 无源文段" % (item, field))
        return
    if not isinstance(s, str) or s not in seg:
        ERRORS.append("%s %s: 非原文 %r" % (item, field, (s or "")[:40]))


# ---------------------------------------------------------------- 枚举单点
import _kg_enums as K

ENTITY_TYPES, ENTRY_ROLES, FACTIONS = K.ENTITY_TYPES, K.ENTRY_ROLES, K.FACTIONS
RULE_TYPES, RULE_ORIGINS, ACTUAL_PRACTICE = K.RULE_TYPES, K.RULE_ORIGINS, K.ACTUAL_PRACTICE
EVENT_TYPES, EVENT_SIGNIFICANCE, SOURCE_TYPES = K.EVENT_TYPES, K.EVENT_SIGNIFICANCE, K.SOURCE_TYPES
VS_OFFICIAL_HISTORY, APPT_STATUS, CONTROVERSY = K.VS_OFFICIAL_HISTORY, K.APPT_STATUS, K.CONTROVERSY
RELATION_TYPES, DIRECTION, EVIDENCE_STRENGTH = K.RELATION_TYPES, K.DIRECTION, K.EVIDENCE_STRENGTH
CITATION_TYPES, CITATION_PURPOSES = K.CITATION_TYPES, K.CITATION_PURPOSES
STANCES, COMMENTARY_TYPES, TONES, FIRSTHAND = K.STANCES, K.COMMENTARY_TYPES, K.TONES, K.FIRSTHAND
MING_CATEGORIES, REIGN_FOCUS = K.MING_CATEGORIES, K.REIGN_FOCUS
TME_CATEGORIES, REIGN_ORDER = K.TME_CATEGORIES, K.REIGN_ORDER
REG_CATEGORIES = K.REG_CATEGORIES


# ---------------------------------------------------------------- 构造器
_ent_pool = ENT_START


def E(item, text, norm, typ="person", roles=("关联人物",), faction="无",
      exam=None, span=None, conf="high"):
    global _ent_pool
    eid = "ENT-%d" % _ent_pool
    _ent_pool += 1
    q(item, text, "ent.text")
    chk(typ in ENTITY_TYPES, "ent type %s" % typ)
    for r in roles:
        chk(r in ENTRY_ROLES, "role %s" % r)
    chk(faction in FACTIONS, "faction %s" % faction)
    return {"ent_id": eid, "item_id": item, "text": text, "type": typ,
            "normalized": norm, "confidence": conf, "role_in_entry": list(roles),
            "faction": faction, "exam_info": exam, "career_span": span}


def RULE(rid, item, typ, modals, condition, subject, action, original,
         origin, practice, tmark, subj_ents=(), obj=None, purpose=None,
         punishment=None, conf="high", viol=None):
    q(item, original, "rule.original")
    chk(typ in RULE_TYPES, "rule type %s" % typ)
    chk(origin in RULE_ORIGINS, "origin %s" % origin)
    chk(practice in ACTUAL_PRACTICE, "practice %s" % practice)
    return {"rule_id": rid, "item_id": item, "type": typ, "modals": list(modals),
            "condition": condition, "subject": subject,
            "subject_ent_ids": list(subj_ents), "action": action, "object": obj,
            "purpose": purpose, "punishment": punishment, "original": original,
            "confidence": conf, "rule_origin": origin,
            "actual_practice": practice, "violation_evidence": viol,
            "time_marker": tmark}


def EVT(eid, item, typ, who, action, what, when, where, original,
        significance, impact, stype, vs, who_ents=(), rel_evts=()):
    q(item, original, "evt.original")
    chk(typ in EVENT_TYPES, "evt type %s" % typ)
    chk(significance in EVENT_SIGNIFICANCE, "sig %s" % significance)
    chk(stype in SOURCE_TYPES, "stype %s" % stype)
    chk(vs in VS_OFFICIAL_HISTORY, "vs %s" % vs)
    return {"event_id": eid, "item_id": item, "type": typ, "who": who,
            "who_ent_ids": list(who_ents), "action": action, "what": what,
            "when": when, "where": where, "original": original,
            "event_significance": significance, "political_impact": impact,
            "source_type": stype, "vs_official_history": vs,
            "related_events": list(rel_evts)}


def APPT(aid, item, person, office, when, status, evidence, original,
         person_ents=(), office_ents=(), inst=None, inst_ents=(), ctx=None,
         contro="无争议", faction_impl=None, concurrent=()):
    q(item, original, "appt.original")
    q(item, evidence, "appt.evidence")
    chk(status in APPT_STATUS, "status %s" % status)
    chk(contro in CONTROVERSY, "contro %s" % contro)
    return {"appt_id": aid, "item_id": item, "person": person,
            "person_ent_ids": list(person_ents), "office": office,
            "office_ent_ids": list(office_ents), "institution": inst,
            "institution_ent_ids": list(inst_ents), "when": when, "status": status,
            "evidence": evidence, "original": original,
            "appointment_context": ctx, "controversy": contro,
            "faction_implication": faction_impl, "concurrent_posts": list(concurrent)}


def REL(rid, item, pa, pb, rtype, direction, evidence, original,
        pa_ents=(), pb_ents=(), evo=None, conseq=None, strength="直接表述", span=None):
    q(item, original, "rel.original")
    q(item, evidence, "rel.evidence")
    chk(rtype in RELATION_TYPES, "rt %s" % rtype)
    chk(direction in DIRECTION, "dir %s" % direction)
    chk(strength in EVIDENCE_STRENGTH, "strength %s" % strength)
    return {"rel_id": rid, "item_id": item, "person_a": pa,
            "person_a_ent_ids": list(pa_ents), "person_b": pb,
            "person_b_ent_ids": list(pb_ents), "relation_type": rtype,
            "direction": direction, "evidence": evidence, "original": original,
            "relationship_evolution": evo, "political_consequence": conseq,
            "evidence_strength": strength, "time_span": span}


def CIT(cid, item, work, ctype, context, original, purpose, work_ents=(),
        acc=None, quoted=None):
    q(item, original, "cit.original")
    if quoted:
        q(item, quoted, "cit.quoted_text")
    chk(ctype in CITATION_TYPES, "ctype %s" % ctype)
    chk(purpose in CITATION_PURPOSES, "purpose %s" % purpose)
    return {"cit_id": cid, "item_id": item, "cited_work": work,
            "cited_work_ent_ids": list(work_ents), "citation_type": ctype,
            "context": context, "original": original,
            "citation_purpose": purpose, "accuracy_note": acc,
            "quoted_text": quoted}


def OPN(oid, item, topic, stance, argument, original, ctype, tone, fw,
        targets=(), ev=None, parallel=None):
    q(item, original, "opn.original")
    chk(stance in STANCES, "stance %s" % stance)
    chk(ctype in COMMENTARY_TYPES, "ct %s" % ctype)
    chk(tone in TONES, "tone %s" % tone)
    chk(fw in FIRSTHAND, "fw %s" % fw)
    return {"opn_id": oid, "item_id": item, "topic": topic, "stance": stance,
            "argument": argument, "original": original, "commentary_type": ctype,
            "target_entities": list(targets), "evidence_cited": ev,
            "historical_parallel": parallel, "tone": tone,
            "firsthand_witness": fw}


def MING(mid, item, era, who, what, when, where, category, original,
         reign_focus, fw, who_ents=(), ref_evts=(), first_person=False, supp=None):
    q(item, original, "ming.original")
    chk(category in MING_CATEGORIES, "ming cat %s" % category)
    chk(reign_focus in REIGN_FOCUS, "reign %s" % reign_focus)
    chk(fw in FIRSTHAND, "fw %s" % fw)
    return {"ming_id": mid, "item_id": item, "era": era, "who": who,
            "who_ent_ids": list(who_ents), "what": what, "when": when,
            "where": where, "category": category, "first_person": first_person,
            "ref_events": list(ref_evts), "original": original,
            "reign_focus": reign_focus, "firsthand_witness": fw,
            "supplements_what": supp}


def ERA(reign, order, text, year=None, dynasty="明"):
    return {"dynasty": dynasty, "reign": reign, "year": year,
            "order": order, "text": text}


def TME(tid, item, era, target, action, content, category, original,
        target_ents=(), rel_evo=None, rel_org=None, inst_target=None,
        cause=None, before=None, after=None):
    q(item, original, "tme.original")
    chk(category in TME_CATEGORIES, "tme cat %s" % category)
    return {"tme_id": tid, "item_id": item, "era": era, "target": target,
            "target_ent_ids": list(target_ents), "action": action,
            "content": content, "category": category, "related_evo": rel_evo,
            "related_org": rel_org, "ref_item": item, "original": original,
            "institution_target": inst_target, "cause": cause,
            "before_after": {"before": before, "after": after}}


def REG2(rid, item, name, category, establishment, summary, practice, original,
         vs, tme_ids=(), abuses=(), figures=()):
    q(item, original, "reg.original")
    chk(category in REG_CATEGORIES, "reg cat %s" % category)
    chk(practice in ACTUAL_PRACTICE, "practice %s" % practice)
    chk(vs in VS_OFFICIAL_HISTORY, "vs %s" % vs)
    return {"reg_id": rid, "item_id": item, "name": name, "category": category,
            "establishment": establishment, "tme_ids": list(tme_ids),
            "content_summary": summary, "actual_practice": practice,
            "abuses_reform": list(abuses), "key_figures": list(figures),
            "original": original, "vs_official_history": vs}


# ---------------------------------------------------------------- ID 计数器
class Seq:
    def __init__(self, n):
        self.n = n

    def nid(self):
        self.n += 1
        return self.n


NEXT = {
    "02": {"rules": 5, "events": 12, "appts": 18, "rels": 8, "opns": 16,
           "cits": 8, "mings": 12, "tmes": 10, "regs": 5},
    "03": {"rules": 4, "events": 10, "appts": 9, "rels": 6, "opns": 12,
           "cits": 10, "mings": 11, "tmes": 8, "regs": 6},
    "04": {"rules": 5, "events": 8, "appts": 8, "rels": 5, "opns": 8,
           "cits": 6, "mings": 9, "tmes": 6, "regs": 6},
    "05": {"rules": 8, "events": 10, "appts": 9, "rels": 8, "opns": 10,
           "cits": 8, "mings": 10, "tmes": 6, "regs": 6},
}
SEQ = {v: {L: Seq(n) for L, n in d.items()} for v, d in NEXT.items()}
NEW = {v: {} for v in VOLS}


def add(layer, vol, recs):
    NEW[vol].setdefault(layer, []).extend(recs)


def rid(layer, vol, prefix):
    return "%s-%s-%03d" % (prefix, vol, SEQ[vol][layer].nid())


# ================================================================ 卷 02
V = "02"

# ---- 02-014 更正殿名 ----
e_taizu = E("02-014", "太祖", "朱元璋", "person", ("主体",), span="洪武—建文")
e_wenzong = E("02-014", "文皇", "朱棣", "person", ("关联人物",), span="永乐")
e_shizong = E("02-014", "世宗", "嘉靖帝", "person", ("主体",), span="嘉靖")
e_zhangjue = E("02-014", "张槚", "张槚", "person", ("主体",), span="隆庆")
e_gaoyi = E("02-014", "高仪", "高仪", "person", ("关联人物",), span="隆庆")
e_lifang = E("02-014", "李芳", "李芳", "person", ("关联人物",), faction="宦官", span="隆庆")
e_zhanghong = E("02-014", "张宏", "张宏", "person", ("关联人物",), faction="宦官", span="万历")
e_shenli = E("02-014", "沈鲤", "沈鲤", "person", ("关联人物",), span="万历")
e_wangshizhen = E("02-014", "王世贞", "王世贞", "person", ("关联人物",), span="嘉靖—万历")
e_mukai = E("02-014", "毛恺", "毛恺", "person", ("关联人物",), span="隆庆")
e_tengxiang = E("02-014", "滕祥", "滕祥", "person", ("关联人物",), faction="宦官", span="隆庆")
add("ents", V, [e_taizu, e_wenzong, e_shizong, e_zhangjue, e_gaoyi, e_lifang,
                e_zhanghong, e_shenli, e_wangshizhen, e_mukai, e_tengxiang])

ev1 = EVT(rid("events", V, "EVT"), "02-014", "制度变动", "世宗",
          "更改三大殿名号", "更奉天殿曰皇极、华盖殿曰中极、谨身殿曰建极，取《洪范》之义",
          "嘉靖中", "北京", "世宗更其名曰皇极，而华盖殿则曰中极，谨身殿曰建极，盖取《洪范》之义",
          "制度变动", "宫殿名号去太祖初号，议者以为字面相同意义不美", "文献转引",
          "补正史之阙", who_ents=[e_shizong["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "02-014", "朝政", "张槚",
          "奏请恢复太祖殿名", "御史张槚请改仍太祖旧号，大宗伯高仪以皇考所定且遗诏不及殿名，乞存三年无改之义，遂不果易",
          "隆庆初元", "北京", "至隆庆初元，而御史张槚请改仍太祖旧号。时，高仪为大宗伯，以为皇考所定，且遗诏中多所改正，独不及殿名，乞存之，以存“三年无改”之义。遂不果易",
          "一般掌故", "殿名复旧之议被搁置", "文献转引", "正史不载",
          who_ents=[e_zhangjue["ent_id"], e_gaoyi["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "02-014", "朝政", "李芳",
          "请改南北郊合祀天地", "太监李芳请合祀南北郊天地如国初典制，礼臣以议出中官执不许",
          "隆庆中", "北京", "其与张侍御同时，则有太监李芳。请改南北郊合祀天地如国初典制，礼臣亦执不许。盖以议出中官",
          "一般掌故", "中官议礼见格", "文献转引", "正史不载",
          who_ents=[e_lifang["ent_id"]])
ev4 = EVT(rid("events", V, "EVT"), "02-014", "朝政", "沈鲤",
          "议崇祀陈献章于孔庙", "今上甲申议崇祀陈献章於孔庙，礼臣沈鲤疑大榼张宏主之不肯行，内阁票发多官会议允祀，由是与政府不协",
          "万历甲申", "北京", "其后，今上甲申议崇祀陈献章於孔庙。礼臣为沈鲤，亦疑大榼张宏主之，不肯行。而内阁竟票发多官，会议允祀，由是与政府不协",
          "一般掌故", "从祀之议引发内阁与礼臣不和", "文献转引", "补正史之阙",
          who_ents=[e_shenli["ent_id"], e_zhanghong["ent_id"]])
add("events", V, [ev1, ev2, ev3, ev4])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "02-014", "禁止", ["乞存"], "皇考所定殿名",
         "礼臣", "存皇考所定殿名不轻改",
         "以为皇考所定，且遗诏中多所改正，独不及殿名，乞存之，以存“三年无改”之义",
         "祖制", "遵行", "隆庆初元", subj_ents=[e_gaoyi["ent_id"]],
         purpose="存三年无改之义"),
    RULE(rid("rules", V, "RULE"), "02-014", "程序", ["必曰"], "列圣封拜功臣",
         "朝廷", "封拜功臣以奉天为号",
         "太宗继之，一切封拜诸功臣，必曰“奉天靖难”。其次曰“奉天翊卫、奉天翊运”。至列圣所封者，无论为功勋，为恩泽，为文武，亦必“奉天”为号，至今不改",
         "祖制", "遵行", "永乐以后", subj_ents=[e_wenzong["ent_id"]]),
])

add("rels", V, [
    REL(rid("rels", V, "REL"), "02-014", "张槚", "高仪", "同僚", "双向",
        "至隆庆初元，而御史张槚请改仍太祖旧号。时，高仪为大宗伯",
        "至隆庆初元，而御史张槚请改仍太祖旧号。时，高仪为大宗伯，以为皇考所定，且遗诏中多所改正，独不及殿名，乞存之，以存“三年无改”之义。遂不果易",
        pa_ents=[e_zhangjue["ent_id"]], pb_ents=[e_gaoyi["ent_id"]],
        evo="议复殿名与存皇考旧号相持", conseq="殿名复旧之议不果", span="隆庆初元"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-014", "太祖奉天殿号", "肯定",
        "作者按断太祖奉天二字实千古独见万世不可易，非皇极建极所能替代",
        "按太祖“奉天”二字，实千古独见，万世不可易",
        "褒扬", "严肃", "传闻", targets=[e_taizu["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "02-014", "完颜氏皇极殿名", "否定",
        "作者考辨金世宗天眷元年改名皇极殿先于本朝，尤为不典",
        "完颜氏上京宫殿，其正寝取名乾元殿，盖袭唐世旧号。至天眷元年，改名皇极殿，则亡金先已称之，尤为不典",
        "考辨", "客观", "传闻"),
    OPN(rid("opns", V, "OPN"), "02-014", "李芳张宏之为人", "肯定",
        "作者称李芳能读书喜谏诤，为金英覃昌之流亚，张宏继冯保柄事亦有称于时",
        "李芳者能读书，喜谏诤，穆宗於裕邸，代滕祥柄事，益发舒，屡指上过举，积久不能平，乃杖之百，下法司论斩，刑官毛恺等力争之不能得。其人亦金英、覃昌之流亚也。张宏继冯保柄事，亦有称於时",
        "褒扬", "惋惜", "传闻",
        targets=[e_lifang["ent_id"], e_zhanghong["ent_id"], e_mukai["ent_id"], e_tengxiang["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-014", "嘉靖中", "世宗", "改三殿名号",
         "嘉靖中", "北京", "制度", "世宗更其名曰皇极，而华盖殿则曰中极，谨身殿曰建极，盖取《洪范》之义",
         "嘉靖", "传闻", who_ents=[e_shizong["ent_id"]], ref_evts=[ev1["event_id"]],
         supp="三大殿名号更定始末"),
    MING(rid("mings", V, "MING"), "02-014", "隆庆初元", "张槚", "请复太祖殿名不果",
         "隆庆初元", "北京", "朝政", "至隆庆初元，而御史张槚请改仍太祖旧号。时，高仪为大宗伯，以为皇考所定，且遗诏中多所改正，独不及殿名，乞存之，以存“三年无改”之义。遂不果易",
         "隆庆", "传闻", who_ents=[e_zhangjue["ent_id"], e_gaoyi["ent_id"]],
         ref_evts=[ev2["event_id"]], supp="殿名复旧之议搁置"),
])

add("tmes", V, [
    TME(rid("tmes", V, "YHB-TME"), "02-014",
        ERA("嘉靖", 12, "嘉靖中"),
        "三大殿", "改称",
        "奉天殿改皇极殿、华盖殿改中极殿、谨身殿改建极殿，取《洪范》六极之义",
        "改称", "世宗更其名曰皇极，而华盖殿则曰中极，谨身殿曰建极，盖取《洪范》之义",
        target_ents=[], cause="世宗亲定礼乐薄视百王",
        before="奉天殿、华盖殿、谨身殿（太祖初定）",
        after="皇极殿、中极殿、建极殿"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-014", "大朝会正殿名号制度", "礼制",
         "太祖初定奉天殿，世宗改皇极中极建极，隆庆议复不果",
         "大朝会正殿曰奉天殿，门名亦如之；文皇营北京仍其名；世宗更名皇极，华盖曰中极，谨身曰建极；隆庆初张槚请复旧号，高仪以皇考所定乞存，遂不果易；今殿与门再罹祝融，鼎建在迩，仍用太祖初号",
         "变通", "太祖初定大朝会正殿曰奉天殿，门名亦如之",
         "补正史之阙", figures=[e_taizu["ent_id"], e_shizong["ent_id"], e_zhangjue["ent_id"]]),
])

add("cits", V, [
    CIT(rid("cits", V, "CIT"), "02-014", "《洪范》", "暗用",
        "世宗改殿名取洪范六极之义，议者以为字面相同意义不美",
        "世宗更其名曰皇极，而华盖殿则曰中极，谨身殿曰建极，盖取《洪范》之义",
        "佐证"),
    CIT(rid("cits", V, "CIT"), "02-014", "《祖训》", "直引",
        "引祖训所载奉天法祖与大圭之文，证太祖奉天二字之重",
        "以故《祖训》中云：“皇帝所执大圭，上镂'奉天法祖'四字，遇亲王尊行者，必手秉此圭，始受其拜。以至臣下诰、敕命中，必首云'奉天承运皇帝'。”",
        "立论", quoted="皇帝所执大圭，上镂'奉天法祖'四字"),
])

# ---- 02-020 圣诞忌辰同日 ----
e_shizong2 = E("02-020", "世宗", "嘉靖帝", "person", ("主体",), span="嘉靖")
e_xiaoci = E("02-020", "孝慈高皇后", "马皇后", "person", ("关联人物",), span="洪武")
e_maowenjian = E("02-020", "毛文简", "毛澄", "person", ("关联人物",), span="嘉靖")
e_wangwenzhuang = E("02-020", "汪文庄", "汪俊", "person", ("关联人物",), span="嘉靖")
add("ents", V, [e_shizong2, e_xiaoci, e_maowenjian, e_wangwenzhuang])

ev1 = EVT(rid("events", V, "EVT"), "02-020", "朝政", "世宗",
          "定圣诞忌辰同日先祭后贺之仪",
          "嘉靖三年遇圣诞，礼部汪文庄请即以是日先行孝慈奉祭礼然后嵩呼大庆，上允之，四十余年不复辍",
          "嘉靖三年", "北京", "至嘉靖三年，又遇圣诞，时礼部为汪文庄，请即以是日先行孝慈奉祭礼，然后嵩呼大庆，一切如先朝故事。上允之，四十余年不复辍",
          "制度变动", "定忌辰圣诞同日先行祭后贺之制", "文献转引", "补正史之阙",
          who_ents=[e_shizong2["ent_id"], e_wangwenzhuang["ent_id"]])
add("events", V, [ev1])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "02-020", "程序", ["请", "允之"],
         "圣诞与先朝忌辰同日", "礼臣",
         "是日先行孝慈奉祭礼，然后嵩呼大庆",
         "至嘉靖三年，又遇圣诞，时礼部为汪文庄，请即以是日先行孝慈奉祭礼，然后嵩呼大庆，一切如先朝故事。上允之，四十余年不复辍",
         "奏议定", "遵行", "嘉靖三年起", subj_ents=[e_wangwenzhuang["ent_id"]],
         purpose="凶吉并行不废祀"),
    RULE(rid("rules", V, "RULE"), "02-020", "程序", ["请", "俱杀之"],
         "圣诞先一日称贺", "礼臣",
         "并习仪及山呼之礼俱杀之",
         "及即位，礼臣毛文简请先一日称贺，但并习仪及山呼之礼，俱杀之。行之二年矣",
         "奏议定", "变通", "嘉靖初", subj_ents=[e_maowenjian["ent_id"]]),
])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "02-020", "毛文简", "礼部尚书", "嘉靖初",
         "现任", "礼臣毛文简请先一日称贺",
         "及即位，礼臣毛文简请先一日称贺，但并习仪及山呼之礼，俱杀之",
         person_ents=[e_maowenjian["ent_id"]], ctx="世宗即位后圣诞贺仪之议"),
    APPT(rid("appts", V, "APPT"), "02-020", "汪文庄", "礼部尚书", "嘉靖三年",
         "现任", "时礼部为汪文庄，请即以是日先行孝慈奉祭礼",
         "至嘉靖三年，又遇圣诞，时礼部为汪文庄，请即以是日先行孝慈奉祭礼，然后嵩呼大庆，一切如先朝故事",
         person_ents=[e_wangwenzhuang["ent_id"]], ctx="嘉靖三年圣诞忌辰同日议礼"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-020", "忌辰同日行礼次序", "肯定",
        "作者谓均为在天之灵自不宜轩此轾彼，嗣君自尽其诚，普天臣子申祝釐之敬则先凶后吉亦无不可",
        "是又不然，均为在天之灵，自不宜轩此轾彼。若嗣君必当自尽其诚，但普天臣子又欲申祝釐之敬，则先凶后吉，亦无不可",
        "中立评述", "客观", "传闻"),
    OPN(rid("opns", V, "OPN"), "02-020", "宋朝洛蜀哭则不歌之争", "讽刺",
        "作者设想使其事在宋朝又有洛蜀哭则不歌之争，将成一大党论",
        "使其事在宋朝，又有洛蜀哭则不歌之争，成一大党论矣",
        "讽刺", "嘲讽", "传闻", parallel="北宋洛蜀党争"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-020", "嘉靖三年", "世宗", "定圣诞忌辰同日仪",
         "嘉靖三年", "北京", "制度", "至嘉靖三年，又遇圣诞，时礼部为汪文庄，请即以是日先行孝慈奉祭礼，然后嵩呼大庆，一切如先朝故事。上允之，四十余年不复辍",
         "嘉靖", "传闻", who_ents=[e_shizong2["ent_id"]], ref_evts=[ev1["event_id"]],
         supp="孝慈高皇后忌辰与世宗圣诞同日行礼次序"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-020", "圣诞贺仪", "礼制",
         "嘉靖初定先一日称贺杀习仪山呼之礼，嘉靖三年定同日先祭后贺",
         "世宗以孝慈高皇后忌辰与己圣诞同日，初命先一日称贺并杀习仪山呼之礼；嘉靖三年从汪文庄议，是日先行孝慈奉祭礼然后嵩呼大庆，四十余年不复辍",
         "变通", "八月初十日，为孝慈高皇后忌辰，而世宗皇帝以是日诞生",
         "补正史之阙", figures=[e_shizong2["ent_id"], e_xiaoci["ent_id"]]),
])

# ---- 02-023 进诗献谀得罪 ----
e_shizong3 = E("02-023", "世宗", "嘉靖帝", "person", ("主体",), span="嘉靖")
e_panyuan = E("02-023", "潘渊", "潘渊", "person", ("关联人物",), span="嘉靖")
e_zhangzhentong = E("02-023", "张振通", "张振通", "person", ("关联人物",), span="嘉靖")
e_chenfei = E("02-023", "陈棐", "陈棐", "person", ("主体",), span="嘉靖")
e_xiayan = E("02-023", "夏言", "夏言", "person", ("关联人物",), span="嘉靖")
add("ents", V, [e_shizong3, e_panyuan, e_zhangzhentong, e_chenfei, e_xiayan])

ev1 = EVT(rid("events", V, "EVT"), "02-023", "文化", "潘渊",
          "进嘉靖龙飞颂", "天台知县潘渊进嘉靖《龙飞颂》内外六十四图凡五百段一万二千章，上命开写正文再上，不闻赏罚",
          "嘉靖四年", "北京", "如嘉靖四年，天台知县潘渊，进嘉靖《龙飞颂》，内外六十四图，凡五百段，一万二千章，效苏蕙织锦回文体以献，其用心亦勤矣。上以其文字纵横，不可辨识，命开写正文再上之。然其时不闻有赏，尚不闻被罚也",
          "轶闻", "献颂不赏不罚", "文献转引", "正史不载",
          who_ents=[e_panyuan["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "02-023", "司法", "张振通",
          "献中兴颂诗获谴", "朝天宫道士张振通进献中兴颂诗等，诏下法司逮击讯问",
          "嘉靖十三年", "北京", "至嘉靖十三年，朝天宫道士张振通奏：“臣祝釐之暇，作《中兴颂》诗二十一首，金台八景，武夷九曲，皇陵八咏，以及瑞露、白鹊、白兔，俱有诗上进。乞赐宸翰序文。”下部议，以猥鄙陈渎，替逾狂悖，希图进用，诏下法司逮击讯问",
          "一般掌故", "进谀希恩反得谴", "文献转引", "正史不载",
          who_ents=[e_zhangzhentong["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "02-023", "司法", "陈棐",
          "衍敕谕为箴诗获谴", "给事中陈棐将敕谕衍作箴诗十章上之，上大怒谓其上同天语，令自陈状后降调外任",
          "嘉靖二十六年", "北京", "而给事中陈棐者，将敕谕衍作箴诗十章上之，上大怒，谓棐舞文墨，辄欲将此上同天语，风示在外臣工，甚为狂僭。令自陈状，棐服罪，乃降调外任",
          "一般掌故", "逢君求荣反得辱", "文献转引", "正史不载",
          who_ents=[e_chenfei["ent_id"]])
ev4 = EVT(rid("events", V, "EVT"), "02-023", "人事", "夏言",
          "进天赐时玉赋得褒入相", "乙未春正月朔大雪，礼卿夏言进《天赐时玉赋》，上大悦以忠爱褒之，甫逾年而入相",
          "嘉靖乙未", "北京", "然前此乙未年春正月朔大雪，上谕大臣曰：“今日欲与卿等一见，但蒙天赐时玉耳。”礼卿夏言。即进《天赐时玉赋》以献，上大悦，以忠爱褒之，甫逾年而入相矣",
          "人物转折", "夏言以献赋得入相", "文献转引", "补正史之阙",
          who_ents=[e_xiayan["ent_id"]])
add("events", V, [ev1, ev2, ev3, ev4])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "02-023", "禁止", ["大怒"],
         "臣工将敕谕衍为诗文", "臣工",
         "不得将上敕谕衍作文句上同天语",
         "上大怒，谓棐舞文墨，辄欲将此上同天语，风示在外臣工，甚为狂僭",
         "诏令", "遵行", "嘉靖二十六年", subj_ents=[e_chenfei["ent_id"]],
         punishment="令自陈状，降调外任", viol="陈棐衍敕谕为箴诗十章上之"),
])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "02-023", "陈棐", "给事中", "嘉靖二十六年",
         "贬谪", "而给事中陈棐者，将敕谕衍作箴诗十章上之",
         "而给事中陈棐者，将敕谕衍作箴诗十章上之，上大怒，谓棐舞文墨，辄欲将此上同天语，风示在外臣工，甚为狂僭。令自陈状，棐服罪，乃降调外任",
         person_ents=[e_chenfei["ent_id"]], contro="有争议",
         ctx="朝觐竣事衍敕谕为箴诗获谴"),
    APPT(rid("appts", V, "APPT"), "02-023", "夏言", "礼部尚书", "嘉靖乙未",
         "升迁", "礼卿夏言。即进《天赐时玉赋》以献，上大悦，以忠爱褒之，甫逾年而入相矣",
         "礼卿夏言。即进《天赐时玉赋》以献，上大悦，以忠爱褒之，甫逾年而入相矣",
         person_ents=[e_xiayan["ent_id"]], ctx="以献赋得褒逾年入相"),
])

add("rels", V, [
    REL(rid("rels", V, "REL"), "02-023", "夏言", "世宗", "上下级", "单向",
        "礼卿夏言。即进《天赐时玉赋》以献，上大悦，以忠爱褒之",
        "礼卿夏言。即进《天赐时玉赋》以献，上大悦，以忠爱褒之，甫逾年而入相矣",
        pa_ents=[e_xiayan["ent_id"]], pb_ents=[e_shizong3["ent_id"]],
        evo="由礼卿以献媚得褒入相", span="嘉靖乙未"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-023", "献诗文颂圣之遭际", "讽刺",
        "作者谓富贵前定，圣主喜怒偶然值之，容悦无益，陈棐素善逢君而不为求荣得辱",
        "此非上同圣语乎？乃知富贵前定，圣主喜怒偶然值之，容悦无益也",
        "讽刺", "嘲讽", "传闻", targets=[e_chenfei["ent_id"], e_xiayan["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "02-023", "世宗朝献颂之繁", "中立",
        "作者总断古今献诗文颂圣者史不胜纪，惟世宗朝最为繁夥而遭际自不同",
        "古今献诗文颂圣者，史不胜纪，然惟世宗朝最为繁夥，乃遭际亦自不同",
        "中立评述", "客观", "传闻"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-023", "嘉靖四年—二十六年", "世宗",
         "献诗文颂圣者遭际不一", "嘉靖间", "北京", "文化",
         "古今献诗文颂圣者，史不胜纪，然惟世宗朝最为繁夥，乃遭际亦自不同",
         "嘉靖", "传闻", who_ents=[e_shizong3["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"], ev4["event_id"]],
         supp="潘渊进颂无赏罚、张振通被逮、陈棐获谴、夏言得褒入相四事对比"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-023", "臣工进献诗文之禁", "礼制",
         "嘉靖二十六年禁臣工以敕谕衍文上同天语",
         "世宗朝献诗文颂圣者繁夥，嘉靖十三年张振通以猥鄙陈渎被逮，二十六年陈棐衍敕谕为箴诗获谴降调，遂禁将上谕衍文上同天语",
         "遵行", "上大怒，谓棐舞文墨，辄欲将此上同天语，风示在外臣工，甚为狂僭",
         "补正史之阙", figures=[e_shizong3["ent_id"], e_chenfei["ent_id"]]),
])

# ---- 02-025 庙议献谄不用 ----
e_shang_jj = E("02-025", "上", "嘉靖帝", "person", ("主体",), span="嘉靖")
e_yu = E("02-025", "舆", "陈凤", "person", ("关联人物",), span="嘉靖", conf="medium")
e_jiangrubi = E("02-025", "江汝璧", "江汝璧", "person", ("主体",), span="嘉靖")
e_guoxiyan = E("02-025", "郭希颜", "郭希颜", "person", ("主体",), span="嘉靖")
e_zhangcong = E("02-025", "张", "张璁", "person", ("关联人物",), span="嘉靖", conf="medium")
e_guie = E("02-025", "萼", "桂萼", "person", ("关联人物",), span="嘉靖", conf="medium")
add("ents", V, [e_shang_jj, e_yu, e_jiangrubi, e_guoxiyan, e_zhangcong, e_guie])

ev1 = EVT(rid("events", V, "EVT"), "02-025", "朝政", "舆",
          "请增建庙制伦次被斥", "尚宾司丞舆请增建庙制伦次绘图上之，意在尊睿宗，上不悦下法司鞫之，特命冠带闲住",
          "嘉靖中", "北京", "嘉靖中，太庙被灾，寻即鼎建，时，尚宾司丞舆首上议，请增建庙制伦次，绘图上之，其意在尊睿宗也。上不悦，下法司鞫之，拟以纳赎还职，上特命冠带闲住",
          "一般掌故", "献谄增庙制者被斥闲住", "文献转引", "正史不载",
          who_ents=[e_yu["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "02-025", "朝政", "江汝璧",
          "请备亲庙预立世室报寝", "国子监司业江汝璧请奉皇考入居昭庙并预立世室，又上言皇考入庙宜迁穆庙之首，上皆报寝",
          "嘉靖中", "北京", "又数月，国子监司业江汝璧请备亲庙，谓上享祀宗宫，考庙不可独缺，宜奉皇考入居昭庙。又，请预立世室，以待皇考",
          "一般掌故", "尊兴献之议屡寝", "文献转引", "正史不载",
          who_ents=[e_jiangrubi["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "02-025", "朝政", "郭希颜",
          "请如太祖立四亲庙报寝", "赞善郭希颜请如太祖立四亲庙以明未有无父之国，无非为睿考计久远，上皆报寝",
          "嘉靖中", "北京", "又，赞善郭希颜，则请如太祖立四亲庙，以明未有无父之国，无非为睿考计久远，而上皆报寝",
          "一般掌故", "立亲庙之议报寝", "文献转引", "正史不载",
          who_ents=[e_guoxiyan["ent_id"]])
ev4 = EVT(rid("events", V, "EVT"), "02-025", "司法", "江汝璧",
          "坐科场事革职为民", "汝璧已进少詹事，坐科场事革职为民",
          "嘉靖中", "北京", "不逾岁，汝璧已进少詹事，坐科场事革职为民",
          "人物转折", "由少詹事革职为民", "文献转引", "补正史之阙",
          who_ents=[e_jiangrubi["ent_id"]])
add("events", V, [ev1, ev2, ev3, ev4])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "02-025", "程序", ["下谕", "复旧制"],
         "太庙被灾鼎建后", "世宗",
         "仍复旧制：太祖正南面之位，成祖以下及睿考俱同堂而序，享毕各归於寝",
         "其冬，上自下谕，仍复旧制：太祖正南面之位，成祖以下，及睿考俱同堂而序，享毕，各归於寝。已如敕奉行矣",
         "上谕", "遵行", "嘉靖中", subj_ents=[e_shang_jj["ent_id"]],
         purpose="正太祖南面之位，睿考不得独尊"),
])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "02-025", "江汝璧", "国子监司业", "嘉靖中",
         "升迁", "又数月，国子监司业江汝璧请备亲庙",
         "又数月，国子监司业江汝璧请备亲庙，谓上享祀宗宫，考庙不可独缺，宜奉皇考入居昭庙",
         person_ents=[e_jiangrubi["ent_id"]], ctx="太庙鼎建时议亲庙"),
    APPT(rid("appts", V, "APPT"), "02-025", "郭希颜", "赞善", "嘉靖中",
         "贬谪", "又，赞善郭希颜，则请如太祖立四亲庙",
         "又，赞善郭希颜，则请如太祖立四亲庙，以明未有无父之国，无非为睿考计久远，而上皆报寝",
         person_ents=[e_guoxiyan["ent_id"]], ctx="议立四亲庙报寝"),
])

add("rels", V, [
    REL(rid("rels", V, "REL"), "02-025", "江汝璧", "郭希颜", "同僚", "双向",
        "就江、郭两疏细详之，则汝璧之议，尤为狂恣蔑礼",
        "就江、郭两疏细详之，则汝璧之议，尤为狂恣蔑礼",
        pa_ents=[e_jiangrubi["ent_id"]], pb_ents=[e_guoxiyan["ent_id"]],
        evo="两人先后请尊兴献帝，其议皆报寝", conseq="并遭斥逐", span="嘉靖中"),
    REL(rid("rels", V, "REL"), "02-025", "舆", "桂萼", "父子亲属", "单向",
        "舆即谀臣萼之子，将窃父故智取宠",
        "舆即谀臣萼之子，将窃父故智取宠，不意其遭斥也",
        pa_ents=[e_yu["ent_id"]], pb_ents=[e_guie["ent_id"]],
        evo="效父故智取宠反遭斥", conseq="特命冠带闲住", span="嘉靖中"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-025", "江郭两疏", "否定",
        "作者断江汝璧之议尤为狂恣蔑礼，郭希颜以吊奇至杀身岂非下愚之尤",
        "而郭希颜遂以吊奇至杀身，岂非下愚之尤哉！就江、郭两疏细详之，则汝璧之议，尤为狂恣蔑礼",
        "贬斥", "愤慨", "传闻", targets=[e_jiangrubi["ent_id"], e_guoxiyan["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "02-025", "张桂诸臣之招徕", "讽刺",
        "作者谓上入绍之初大礼未定故贵张桂诸臣以招徕天下，至是且二十年称宗入庙礼无可加，而此辈憸邪犹仍佞习",
        "盖上入绍之初，大礼未定，人心方摇，故贵张、桂诸臣，以招徕天下，至是且二十年矣，称宗入庙，礼无可加。而此辈憸邪，犹仍佞习，为横飞直拜之地",
        "讽刺", "嘲讽", "传闻", targets=[e_zhangcong["ent_id"], e_guie["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-025", "嘉靖中", "世宗",
         "太庙议礼尊兴献之请皆寝", "嘉靖中", "北京", "制度",
         "嘉靖中，太庙被灾，寻即鼎建，时，尚宾司丞舆首上议，请增建庙制伦次，绘图上之，其意在尊睿宗也",
         "嘉靖", "传闻", who_ents=[e_shang_jj["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"]],
         supp="舆、江汝璧、郭希颜先后请尊兴献帝皆不省"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-025", "太庙同堂异室之制", "礼制",
         "嘉靖中太庙灾后仍复旧制，太祖正南面，成祖以下及睿考同堂而序",
         "太庙被灾寻即鼎建，请增庙制者被斥；江汝璧、郭希颜等请备亲庙立四亲庙皆报寝；上自下谕仍复旧制，太祖正南面之位，成祖以下及睿考俱同堂而序，享毕各归於寝",
         "遵行", "其冬，上自下谕，仍复旧制：太祖正南面之位，成祖以下，及睿考俱同堂而序，享毕，各归於寝。已如敕奉行矣",
         "补正史之阙", figures=[e_shang_jj["ent_id"], e_jiangrubi["ent_id"], e_guoxiyan["ent_id"]]),
])

# ---- 02-027 工匠见知 ----
e_shizong5 = E("02-027", "世宗", "嘉靖帝", "person", ("主体",), span="嘉靖")
e_leili = E("02-027", "雷礼", "雷礼", "person", ("主体",), span="嘉靖")
e_xugao = E("02-027", "徐杲", "徐杲", "person", ("主体",), span="嘉靖")
e_zhaowenhua = E("02-027", "赵文华", "赵文华", "person", ("关联人物",), span="嘉靖")
e_ouyangbijin = E("02-027", "欧阳必进", "欧阳必进", "person", ("关联人物",), span="嘉靖")
e_yansong = E("02-027", "分宜", "严嵩", "person", ("关联人物",), span="嘉靖")
e_xujie = E("02-027", "华亭", "徐阶", "person", ("关联人物",), span="嘉靖")
e_yanshifan = E("02-027", "世蕃", "严世蕃", "person", ("关联人物",), span="嘉靖")
e_xufan = E("02-027", "璠", "徐璠", "person", ("关联人物",), span="嘉靖")
add("ents", V, [e_shizong5, e_leili, e_xugao, e_zhaowenhua, e_ouyangbijin,
                e_yansong, e_xujie, e_yanshifan, e_xufan])

ev1 = EVT(rid("events", V, "EVT"), "02-027", "灾异", "世宗",
          "奉天等三殿并奉天门灾", "嘉靖三十六年四月奉天等三殿并奉天门灾，上迫欲先成门工以便朝谒",
          "嘉靖三十六年四月", "北京", "按奉天等三殿并奉天门灾，在嘉靖三十六年四月。时，上迫欲先成门工，以便朝谒",
          "一般掌故", "三殿门灾后急于兴工", "文献转引", "补正史之阙",
          who_ents=[e_shizong5["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "02-027", "人事", "欧阳必进",
          "门成得一品", "文华屡疏迁延被尽夺其官，用必进甫匝岁门成，必进得一品",
          "嘉靖三十七年", "北京", "而文华不能纠缠，屡疏迁延。上大怒，尽夺其官，而用必进，甫匝岁门成，必进得一品",
          "人物转折", "欧阳必进以门工得一品", "文献转引", "补正史之阙",
          who_ents=[e_ouyangbijin["ent_id"], e_zhaowenhua["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "02-027", "制度变动", "徐杲",
          "木匠操斤新宫告成", "永寿宫再建雷礼总其成，木匠徐杲一人拮据经营，不三月而新宫告成，杲得正卿",
          "嘉靖中", "北京", "即永寿宫再建，雷总其成。而木匠徐杲，以一人拮据经营，操斤指示，闻其相度时，第四顾筹算，俄顷即出，而断材长短大小，不爽锱铢。上暂居玉熙，并不闻有斧凿声，不三月而新宫告成",
          "制度变动", "工匠以一手艺峻加至正卿", "文献转引", "正史不载",
          who_ents=[e_xugao["ent_id"], e_leili["ent_id"]])
add("events", V, [ev1, ev2, ev3])

add("rels", V, [
    REL(rid("rels", V, "REL"), "02-027", "赵文华", "严嵩", "父子亲属", "单向",
        "最后赵文华为分宜义子，欧阳必进为分宜妻弟",
        "最后赵文华为分宜义子，欧阳必进为分宜妻弟，特以贪戾与阘茸相继见逐，权臣毫不能庇",
        pa_ents=[e_zhaowenhua["ent_id"]], pb_ents=[e_yansong["ent_id"]],
        evo="以义子得进仍以贪戾见逐", conseq="权臣不能庇", span="嘉靖末"),
    REL(rid("rels", V, "REL"), "02-027", "欧阳必进", "严嵩", "姻亲", "单向",
        "欧阳必进为分宜妻弟",
        "欧阳必进为分宜妻弟，特以贪戾与阘茸相继见逐",
        pa_ents=[e_ouyangbijin["ent_id"]], pb_ents=[e_yansong["ent_id"]],
        evo="以妻弟进亦不能庇", conseq="相继见逐", span="嘉靖末"),
    REL(rid("rels", V, "REL"), "02-027", "徐璠", "徐阶", "父子亲属", "单向",
        "而华亭亦因以进少师，乃子尚宾丞璠，躐拜太常少卿",
        "而华亭亦因以进少师，乃子尚宾丞璠，躐拜太常少卿。识者不无代为恧焉",
        pa_ents=[e_xufan["ent_id"]], pb_ents=[e_xujie["ent_id"]],
        evo="父进少师子躐拜太常少卿", conseq="识者代为恧焉", span="嘉靖末"),
])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "02-027", "雷礼", "工部尚书", "嘉靖中",
         "现任", "则督工侍郎雷礼有劳，而躬自操作，则徐杲一人力也",
         "则督工侍郎雷礼有劳，而躬自操作，则徐杲一人力也",
         person_ents=[e_leili["ent_id"]], ctx="三殿门工督造"),
    APPT(rid("appts", V, "APPT"), "02-027", "徐杲", "工部尚书", "嘉靖末",
         "升迁", "比三殿落成时，徐杲已称尚书，上欲以太子太保宠之，而徐华亭力沮，谓无故事，得中止，仅支正一品俸",
         "比三殿落成时，徐杲已称尚书，上欲以太子太保宠之，而徐华亭力沮，谓无故事，得中止，仅支正一品俸",
         person_ents=[e_xugao["ent_id"]], contro="有争议",
         ctx="以木匠功峻加，徐阶力沮太子太保"),
    APPT(rid("appts", V, "APPT"), "02-027", "欧阳必进", "吏部尚书", "嘉靖末",
         "贬谪", "甫一月分宜又劝上改必进吏部，而圣怒遂不可解。先革孤卿并兼官，未几并尚书夺之",
         "甫一月分宜又劝上改必进吏部，而圣怒遂不可解。先革孤卿并兼官，未几并尚书夺之，其去工部半岁耳",
         person_ents=[e_ouyangbijin["ent_id"]], ctx="司空为苦海营改左都又改吏部触怒"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-027", "雷礼之勤敏", "肯定",
        "作者谓雷丰城以勤敏独为上所眷倚，即帝尧则哲之明何以过之",
        "而雷丰城以勤敏，独为上所眷倚，即帝尧则哲之明，何以过之？终上之世，雷长冬曹，无事不倚办",
        "褒扬", "严肃", "传闻", targets=[e_leili["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "02-027", "徐杲之才", "肯定",
        "作者谓徐杲之才自加人数等，以视文华必进直朴椒下材，上爱念不已倘再有营建杲必峻加",
        "杲亦谦退，不敢以士大夫自居，然其才自加人数等，以视文华、必进，直朴椒下材耳",
        "褒扬", "客观", "传闻", targets=[e_xugao["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "02-027", "大工加恩之不均", "讽刺",
        "作者记永寿宫加恩礼得一品杲得正卿华亭进少师，识者不无代为恧焉，三殿落成加恩百不及一",
        "识者不无代为恧焉",
        "讽刺", "嘲讽", "传闻", targets=[e_xujie["ent_id"], e_xufan["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-027", "嘉靖三十六年—末", "世宗",
         "三殿大工与工匠见知", "嘉靖间", "北京", "制度",
         "按奉天等三殿并奉天门灾，在嘉靖三十六年四月。时，上迫欲先成门工，以便朝谒",
         "嘉靖", "传闻", who_ents=[e_shizong5["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"]],
         supp="三殿灾后门工殿工用人及加恩细节"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-027", "大工督工加恩制度", "官制",
         "嘉靖中三殿门灾后急图兴工，督工者依次得恩",
         "三殿并门灾后文华迁延被夺官，必进匝岁门成一品；雷礼总永寿宫，徐杲一手操作新宫告成得正卿；三殿落成徐杲已称尚书，欲加以太子太保为徐阶所沮；加恩远不及永寿宫",
         "变通", "以故尚书之峻加金吾之世荫，上犹以为慊也",
         "补正史之阙", figures=[e_shizong5["ent_id"], e_leili["ent_id"], e_xugao["ent_id"]]),
])

# ---- 02-030 符印之式 ----
e_taizu2 = E("02-030", "太祖", "朱元璋", "person", ("关联人物",), span="洪武")
e_shizong6 = E("02-030", "世宗", "嘉靖帝", "person", ("关联人物",), span="嘉靖")
e_xuda = E("02-030", "徐达", "徐达", "person", ("关联人物",), span="洪武—永乐")
e_lanyu = E("02-030", "蓝玉", "蓝玉", "person", ("关联人物",), span="洪武")
e_fengsheng = E("02-030", "冯胜", "冯胜", "person", ("关联人物",), span="洪武")
e_qiufu = E("02-030", "邱福", "邱福", "person", ("关联人物",), span="永乐")
e_shengyong = E("02-030", "盛庸", "盛庸", "person", ("关联人物",), span="洪武—建文")
e_yanghong = E("02-030", "杨洪", "杨洪", "person", ("关联人物",), span="正统")
e_zhuyong = E("02-030", "朱永", "朱永", "person", ("关联人物",), span="成化")
e_quluan = E("02-030", "仇鸾", "仇鸾", "person", ("关联人物",), span="嘉靖")
e_xiaocihou = E("02-030", "孝慈后", "马皇后", "person", ("关联人物",), span="洪武")
add("ents", V, [e_taizu2, e_shizong6, e_xuda, e_lanyu, e_fengsheng, e_qiufu,
                e_shengyong, e_yanghong, e_zhuyong, e_quluan, e_xiaocihou])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "02-030", "程序", ["得用"],
         "臣下印信材质", "文武衙门",
         "一品二品衙门得用银造，三品以下俱用铜，以式之大小分高卑",
         "其臣下印信，则文武一品二品衙门，得用银造，三品以下俱用铜，惟以式之大小分高卑",
         "祖制", "遵行", "明兴以来"),
    RULE(rid("rules", V, "RULE"), "02-030", "优先级", ["虽", "亦"],
         "两京兆印信", "两京兆",
         "两京兆虽三品印亦银铸",
         "两京兆虽三品，印亦银铸，则以天府重也",
         "祖制", "遵行", "明兴以来"),
    RULE(rid("rules", V, "RULE"), "02-030", "程序", ["止", "惟"],
         "百官印信颗数", "百官",
         "百官印止一颗，惟巡按则有循环二印，拜命即佩印绶",
         "又百官印止一颗，惟巡按则有循环二印，以故拜命即佩印绶，且其文八叠，与大小文武特异",
         "祖制", "遵行", "明兴以来"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-030", "九叠篆文取义", "怀疑",
        "作者谓九叠篆文不知取义谓何，唐宋以来并无此篆法，疑乾元用九之意",
        "以上俱用九叠篆文，不知取义谓何？唐宋以来并无此篆法，盖创自本朝。意者乾元用九之意乎？",
        "考辨", "客观", "传闻"),
    OPN(rid("opns", V, "OPN"), "02-030", "巡按印制之异", "怀疑",
        "作者设问岂以斧绣雄剧特变其制耶",
        "岂以斧绣雄剧，特变其制耶？",
        "考辨", "客观", "传闻"),
    OPN(rid("opns", V, "OPN"), "02-030", "印章与将相二柄", "肯定",
        "作者总断文渊阁印失后再铸则阁权渐削，盖将相二大柄关於印章如此",
        "而文渊阁印，自今上丙戌失后，再铸则阁权渐削，陵夷以至今日。盖将相二大柄，关於印章如此",
        "感慨", "惋惜", "传闻"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-030", "明兴—嘉靖", "世宗",
         "宝玺增至二十四", "明初以来", "北京", "制度",
         "本朝初有十七宝，至世宗加制其七，今掌在符台者共二十四宝，盖金玉兼有之",
         "跨朝", "传闻", who_ents=[e_taizu2["ent_id"], e_shizong6["ent_id"]],
         supp="御宝自十七宝增至二十四宝之数"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-030", "符印制度", "官制",
         "明初十七宝，世宗加制其七为二十四宝；臣下一二品银印三品以下铜印",
         "御宝初十七宝世宗加七为二十四，金玉兼有；中宫之玺属女官收掌；太后进徽号另铸纯金新称；臣下一二品衙门银印、三品以下铜印，两京兆虽三品亦银铸，俱用九叠篆；巡按用方印式最小且有循环二印；挂印总兵官银印虎钮柳叶篆；内阁文渊阁印仅一寸七分亦用银，丙戌失后再铸而阁权渐削",
         "遵行", "本朝初有十七宝，至世宗加制其七，今掌在符台者共二十四宝，盖金玉兼有之",
         "补正史之阙", figures=[e_taizu2["ent_id"], e_shizong6["ent_id"]]),
])

# ---- 02-035 实录难据 ----
e_taizu3 = E("02-035", "太祖", "朱元璋", "person", ("关联人物",), span="洪武")
e_jianwen = E("02-035", "建文帝", "朱允炆", "person", ("关联人物",), span="建文")
e_yingzong = E("02-035", "英宗", "朱祁镇", "person", ("关联人物",), span="正统—天顺")
e_jingdi = E("02-035", "景帝", "朱祁钰", "person", ("关联人物",), span="景泰")
e_xingxiandi = E("02-035", "兴献帝", "朱祐杬", "person", ("关联人物",), span="嘉靖追崇")
e_feiwenxian = E("02-035", "费文宪", "费宏", "person", ("关联人物",), span="嘉靖")
e_zhangzuo = E("02-035", "张佐", "张佐", "person", ("关联人物",), faction="宦官", span="嘉靖")
e_shizong7 = E("02-035", "世宗", "嘉靖帝", "person", ("关联人物",), span="嘉靖")
add("ents", V, [e_taizu3, e_jianwen, e_yingzong, e_jingdi, e_xingxiandi,
                e_feiwenxian, e_zhangzuo, e_shizong7])

add("events", V, [
    EVT(rid("events", V, "EVT"), "02-035", "制度变动", "太祖",
        "太祖实录凡经三修", "开国功臣壮猷伟略稍不为靖难归伏诸公所喜者俱被划削",
        "洪武—永乐", "北京", "乃太祖录凡经三修，当时开国功臣，壮猷伟略，稍不为靖难归伏诸公所喜者，俱被划削",
        "制度变动", "实录三修致功臣事迹划削", "文献转引", "异于正史",
        who_ents=[e_taizu3["ent_id"]]),
    EVT(rid("events", V, "EVT"), "02-035", "制度变动", "兴献帝",
        "兴献帝以藩邸追崇亦修实录", "总裁费文宪等苦无措手，至假借承奉长史等所撰实录为张本，书成俱被酬赏",
        "嘉靖中", "北京", "至於兴献帝以藩邸追崇，亦修实录，何为者哉！其时总裁费文宪等，苦无措手，至假借承奉长史等所撰实录为张本，后书成，俱被酬赏",
        "一般掌故", "追崇帝实录假借长史所撰", "文献转引", "异于正史",
        who_ents=[e_xingxiandi["ent_id"], e_feiwenxian["ent_id"]]),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-035", "以实录为史", "否定",
        "作者谓本朝无国史以列帝实录为史已属纰漏，建文一朝四年荡灭无遗，景帝曲笔为多",
        "本朝无国史，以列帝实录为史，已属纰漏。乃太祖录凡经三修，当时开国功臣，壮猷伟略，稍不为靖难归伏诸公所喜者，俱被划削。建文帝一朝四年，荡灭无遗",
        "考辨", "严肃", "传闻"),
    OPN(rid("opns", V, "OPN"), "02-035", "张佐滥受世锦衣", "讽刺",
        "作者谓太监张佐辈滥受世锦衣，可哂亦可欢矣",
        "至太监张佐辈，滥受世锦衣，可哂亦可欢矣",
        "讽刺", "嘲讽", "传闻", targets=[e_zhangzuo["ent_id"]]),
])

add("cits", V, [
    CIT(rid("cits", V, "CIT"), "02-035", "《承天大志》", "泛引",
        "作者谓修承天大志亦然，开局太迟词林诸公各具事希宠纷纷不定，比成未几世宗已升遐",
        "其修《承天大志》亦然，但开局太迟，词林诸公，各具事希宠，纷纷不定，比成未几，则世宗已升遐矣",
        "对比"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-035", "洪武—嘉靖", "太祖",
         "实录修纂三修与建文荡灭", "明初以来", "北京", "制度",
         "本朝无国史，以列帝实录为史，已属纰漏",
         "跨朝", "传闻", who_ents=[e_taizu3["ent_id"]],
         supp="实录三修划削功臣、建文四年荡灭、兴献帝实录假借张本"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-035", "实录修纂制度", "其他",
         "明以列帝实录为史，太祖录经三修，建文实录荡灭，兴献帝亦修实录",
         "本朝无国史以实录为史；太祖录凡三修，不为靖难归伏诸公所喜之功臣俱被划削；建文一朝四年荡灭无遗，后人搜括捃拾百千之一二；景帝事附英宗录曲笔为多；兴献帝以藩邸追崇亦修实录，假借承奉长史所撰为张本；承天大志开局太迟希宠不定",
         "名存实亡", "本朝无国史，以列帝实录为史，已属纰漏",
         "异于正史", figures=[e_taizu3["ent_id"], e_jianwen["ent_id"], e_xingxiandi["ent_id"]]),
])

# ---- 02-039 朝觐官进献 ----
e_muzong = E("02-039", "穆宗", "隆庆帝", "person", ("主体",), span="隆庆")
e_jiangzigao = E("02-039", "姜子羔", "姜子羔", "person", ("主体",), span="隆庆")
add("ents", V, [e_muzong, e_jiangzigao])

ev1 = EVT(rid("events", V, "EVT"), "02-039", "朝政", "姜子羔",
          "请朝觐官进献羡余被驳", "陕西副使姜子羔请令朝觐官进献羡余并限为定制，上曰进献非事体且国用亦不藉此，其勿许，并禁借觐名科派",
          "穆宗戊辰", "北京", "当穆宗戊辰外计时，陕西副使姜子羔者上言：朝觐官各有路费及馈遗私帑，宜令进献羡余以佐国计。且限为定制：布政司三百两，按察司二百两，苑马行太仆一百两，运司府正二百五十两，府佐一百两，州县正官二百两，州县佐五十两。上曰：“进献非事体，且国用亦不藉此。其勿许。”且并禁入朝官员不得借觐名科派",
          "一般掌故", "进献之请被驳并禁科派", "文献转引", "补正史之阙",
          who_ents=[e_jiangzigao["ent_id"], e_muzong["ent_id"]])
add("events", V, [ev1])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "02-039", "禁止", ["勿许", "禁"],
         "朝觐官进献", "入朝官员",
         "不得进献羡余，不得借觐名科派",
         "上曰：“进献非事体，且国用亦不藉此。其勿许。”且并禁入朝官员不得借觐名科派",
         "上谕", "遵行", "穆宗戊辰", subj_ents=[e_muzong["ent_id"]],
         purpose="存事体、国用不藉进献"),
])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "02-039", "姜子羔", "陕西副使", "穆宗戊辰",
         "升迁", "陕西副使姜子羔者上言：朝觐官各有路费及馈遗私帑，宜令进献羡余以佐国计",
         "当穆宗戊辰外计时，陕西副使姜子羔者上言：朝觐官各有路费及馈遗私帑，宜令进献羡余以佐国计",
         person_ents=[e_jiangzigao["ent_id"]], contro="有争议",
         ctx="外计时建议进献羡余被驳"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-039", "穆宗不许进献", "肯定",
        "作者谓大哉王言，与岁进月进者天壤矣",
        "大哉王言，与岁进月进者天壤矣",
        "褒扬", "严肃", "传闻", targets=[e_muzong["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "02-039", "无碍官银之说", "讽刺",
        "作者谓夫既曰官银那有无碍之理，真掩耳盗铃也",
        "夫既曰官银，那有无碍之理，真掩耳盗铃也！",
        "讽刺", "嘲讽", "传闻"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-039", "穆宗戊辰", "穆宗",
         "禁朝觐官进献", "隆庆初", "北京", "朝政",
         "当穆宗戊辰外计时，陕西副使姜子羔者上言：朝觐官各有路费及馈遗私帑，宜令进献羡余以佐国计",
         "隆庆", "传闻", who_ents=[e_muzong["ent_id"], e_jiangzigao["ent_id"]],
         ref_evts=[ev1["event_id"]], supp="姜子羔进献羡余之请被驳并禁科派"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-039", "朝觐进献之禁", "财政",
         "穆宗戊辰禁朝觐官进献羡余及借觐名科派",
         "国用匮乏议加田赋关税搜索赎鍰，姜子羔请朝觐官进献羡余并限为定制，上以进献非事体勿许，并禁借觐名科派",
         "遵行", "上曰：“进献非事体，且国用亦不藉此。其勿许。”且并禁入朝官员不得借觐名科派",
         "补正史之阙", figures=[e_muzong["ent_id"], e_jiangzigao["ent_id"]]),
])

# ---- 02-042 贞观政要 ----
e_jinshang = E("02-042", "今上", "万历帝", "person", ("主体",), span="万历")
e_weizheng = E("02-042", "魏徵", "魏徵", "person", ("评论对象",), span="唐")
e_taizong = E("02-042", "唐太宗", "李世民", "person", ("评论对象",), span="唐")
e_shenshixing = E("02-042", "申时行", "申时行", "person", ("关联人物",), span="万历")
e_zhangjuzheng = E("02-042", "张居正", "张居正", "person", ("关联人物",), span="万历")
e_liuji = E("02-042", "刘基", "刘基", "person", ("引用人物",), span="元—明初")
e_luoyuren = E("02-042", "雒于仁", "雒于仁", "person", ("关联人物",), span="万历")
add("ents", V, [e_jinshang, e_weizheng, e_taizong, e_shenshixing, e_zhangjuzheng,
                e_liuji, e_luoyuren])

ev1 = EVT(rid("events", V, "EVT"), "02-042", "朝政", "今上",
          "经筵驳魏徵非贤者", "戊子二月讲毕上传谕阁臣申时行等驳魏徵忘君事仇固非贤者，产臣以伊尹就汤就桀为比又引刘基等元旧臣，上遂置不问",
          "万历戊子二月", "文华殿", "如戊子二月，以春和初启讲筵，上御文华。讲毕，复传谕阁臣申时行等，曰：“唐魏徵为何如人？”对以征能强谏，亦是贤臣。上驳云：“征先事李密，再事建成，后事太宗，忘君事仇，固非贤者。”",
          "一般掌故", "上评魏徵翻臣下之见", "文献转引", "正史不载",
          who_ents=[e_jinshang["ent_id"], e_shenshixing["ent_id"], e_weizheng["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "02-042", "朝政", "今上",
          "罢贞观政要改讲礼记", "上意终不释，命罢《贞观政要》而讲《礼记》，又允《通监》与《礼经》参讲，命先讲《尚书》徐及《通监》以至《大学衍义》",
          "万历戊子", "文华殿", "上意终不释，命罢《贞观政要》，而讲《礼记》。阁臣又言宋儒云：“读经则师其意，读史则师其迹，宜令《通监》与《礼经》参讲。”上允之。乃命先讲《尚书》，徐及《通监》，以至《大学衍义》",
          "制度变动", "经筵选书由政要改为礼记尚书通鉴", "文献转引", "正史不载",
          who_ents=[e_jinshang["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "02-042", "朝政", "今上",
          "政要罢后不复御文华", "自政要罢后次年四月遂不复御文华，广厦细旃迄成尘坌，辅臣屡请不允",
          "万历己丑四月", "文华殿", "然自政要罢后，次年四月遂不复御文华。广厦细旃，迄成尘坌，辅臣屡请不允",
          "一般掌故", "讲筵渐辍", "文献转引", "补正史之阙",
          who_ents=[e_jinshang["ent_id"]])
add("events", V, [ev1, ev2, ev3])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "02-042", "程序", ["宜令", "允之"],
         "经史参讲", "阁臣",
         "《通监》与《礼经》参讲，先讲《尚书》，徐及《通监》，以至《大学衍义》",
         "阁臣又言宋儒云：“读经则师其意，读史则师其迹，宜令《通监》与《礼经》参讲。”上允之。乃命先讲《尚书》，徐及《通监》，以至《大学衍义》",
         "奏议定", "遵行", "万历戊子", subj_ents=[e_shenshixing["ent_id"]]),
])

add("cits", V, [
    CIT(rid("cits", V, "CIT"), "02-042", "《贞观政要》", "泛引",
        "上初御讲幄辅臣即以劝讲，至是乃厌薄中辍",
        "然《贞观政要》，亦上初御讲幄，辅臣即以劝讲，至是乃厌薄中辍。或以张居正所进，终未审当圣意耶？",
        "掌故引用"),
    CIT(rid("cits", V, "CIT"), "02-042", "《通鉴》", "泛引",
        "今上元年冬杪张居正将本年讲章进呈已首列此书，上命镂版印行",
        "《通鉴》一书，今上元年冬杪，张居正当国，将本年讲章进呈，已首列此书，上命镂版印行矣",
        "掌故引用"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-042", "上之经史权衡", "肯定",
        "作者谓上之於经史后先权宜审矣，至评论魏征太宗真千古斧钺",
        "上之於经史，后先权宜审矣。至评论魏征、太宗，真千古斧钺",
        "褒扬", "严肃", "传闻", targets=[e_jinshang["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "02-042", "阁臣奏对", "否定",
        "作者惜乎对风诸语稍未能助高深，又以刘基辈元旧臣为比失当",
        "其时产臣以伊尹就汤就桀为比，已非其伦，又引太祖时佐命刘基等皆元旧臣，顾其人可用否耳，此语尤为失当",
        "贬斥", "惋惜", "传闻", targets=[e_shenshixing["ent_id"], e_liuji["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-042", "万历戊子—庚寅", "今上",
         "经筵罢贞观政要", "万历间", "北京", "文化",
         "如戊子二月，以春和初启讲筵，上御文华",
         "万历", "亲历", who_ents=[e_jinshang["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"]],
         supp="上评魏徵太宗、罢政要讲礼记、不复御文华、雒于仁四箴之疏诸事"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-042", "经筵日讲选书制度", "礼制",
         "万历初经筵先贞观政要，戊子改讲礼记，命通鉴与礼经参讲",
         "上初御讲幄辅臣劝讲贞观政要；戊子春讲筵上驳魏徵并传谕太宗协父弑兄家法不正，命罢政要讲礼记；允通鉴与礼经参讲，先尚书徐及通鉴以至大学衍义；政要罢后次年四月不复御文华，辅臣屡请不允",
         "变通", "上意终不释，命罢《贞观政要》，而讲《礼记》",
         "补正史之阙", figures=[e_jinshang["ent_id"], e_shenshixing["ent_id"], e_zhangjuzheng["ent_id"]]),
])

# ---- 02-043 冲圣日讲 ----
e_jinshang2 = E("02-043", "今上", "万历帝", "person", ("主体",), span="万历")
e_jiangling = E("02-043", "江陵相", "张居正", "person", ("关联人物",), span="万历")
e_yingzong2 = E("02-043", "英宗", "朱祁镇", "person", ("引用人物",), span="正统—天顺")
e_wangzhen = E("02-043", "王振", "王振", "person", ("关联人物",), faction="宦官", span="正统")
e_sanyang = E("02-043", "三杨", "杨士奇杨荣杨溥", "person", ("引用人物",), span="永乐—正统")
add("ents", V, [e_jinshang2, e_jiangling, e_yingzong2, e_wangzhen, e_sanyang])

ev1 = EVT(rid("events", V, "EVT"), "02-043", "制度变动", "今上",
          "日讲每日驾幸文华", "江陵相建议上每日於日初出时驾幸文华听儒臣讲读经书，少憩复御讲筵再读史书，至午膳还大内，惟三六九常朝暂免",
          "万历初", "文华殿", "今上初登大宝，江陵相建议，上每日於日初出时驾幸文华，听儒臣讲读经书。少憩片时，复御讲筵，再读史书。至午膳而后还大内。惟每月三六九常朝之日始暂免，此外即隆冬盛暑无间焉",
          "制度变动", "日讲由不拘期改为每日举行", "文献转引", "补正史之阙",
          who_ents=[e_jinshang2["ent_id"], e_jiangling["ent_id"]])
add("events", V, [ev1])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "02-043", "程序", ["用"],
         "列圣经筵", "朝廷",
         "经筵每月用初二、十二、廿二凡三日",
         "列圣经筵，每月用初二、十二、廿二、凡三日",
         "祖制", "遵行", "列朝"),
    RULE(rid("rules", V, "RULE"), "02-043", "程序", ["减杀"],
         "日讲礼仪", "朝廷",
         "日讲不拘期，一切礼仪视经筵俱减杀，仅侍班阁部大臣与词林讲官及侍书等官供事",
         "而日讲则不拘期，一切礼仪视经筵俱减杀，仅侍班阁部大臣，与词林讲官，及侍书等官供事",
         "祖制", "变通", "万历初", purpose="礼从其杀以便日讲"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-043", "今上早岁励精", "肯定",
        "作者谓十年之中圣学日新坐致太平之治，主上早岁励精真可只千古矣",
        "以故十年之中，圣学日新，坐致太平之治",
        "褒扬", "严肃", "亲闻", targets=[e_jinshang2["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "02-043", "英宗时三杨不纳诲", "否定",
        "作者谓英宗御极幼冲初不闻三杨诸公朝夕纳诲，遂使王振得盗国柄几危宗社",
        "昔英宗御极亦在幼冲，初不闻三杨诸公有此朝夕纳诲，遂使王振得盗国柄，几危宗社",
        "贬斥", "愤慨", "传闻", targets=[e_yingzong2["ent_id"], e_sanyang["ent_id"], e_wangzhen["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-043", "万历初", "今上",
         "日讲每日进讲不间寒暑", "万历初", "文华殿", "制度",
         "今上初登大宝，江陵相建议，上每日於日初出时驾幸文华，听儒臣讲读经书",
         "万历", "亲闻", who_ents=[e_jinshang2["ent_id"]], ref_evts=[ev1["event_id"]],
         supp="日讲由不拘期改为每日，十年不辍"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-043", "日讲制度", "礼制",
         "列圣每月三日经筵，日讲不拘期；万历初江陵建议每日进讲",
         "经筵每月初二、十二、廿二三日；日讲不拘期礼仪减杀，值日词臣进讲章备乙览；万历初上每日日初出驾幸文华听讲，少憩复御讲筵读史，至午膳还内，惟三六九常朝暂免，隆冬盛暑无间，十年圣学日新",
         "变通", "今上初登大宝，江陵相建议，上每日於日初出时驾幸文华，听儒臣讲读经书",
         "补正史之阙", figures=[e_jinshang2["ent_id"], e_jiangling["ent_id"]]),
])

# ---- 02-046 壬寅上寿 ----
e_jinshang3 = E("02-046", "上", "万历帝", "person", ("主体",), span="万历")
add("ents", V, [e_jinshang3])

ev1 = EVT(rid("events", V, "EVT"), "02-046", "朝政", "上",
          "壬寅上寿合七十岁", "壬寅之岁上圣龄甫满四旬而御极已三十年，内廷御辈以上诞生及在宥合之为七十岁上南山之觞",
          "万历壬寅秋八月", "大内", "壬寅之岁，上圣龄甫满四旬，而御极已三十年。至秋八月，值上万寿圣节，内廷{执曰}御辈，思别效嵩祝，以博天颜一启者，乃以上诞生及在宥，合之为七十岁，上南山之觞",
          "一般掌故", "万寿庆典合诞以七十岁计", "文献转引", "正史不载",
          who_ents=[e_jinshang3["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "02-046", "朝政", "诸采榷使",
          "争市瑰异名孝顺钱粮", "矿税甫罢而旋兴，诸采榷使争市瑰异未名之宝名孝顺钱粮，左藏为之充牣",
          "万历壬寅", "各地", "时矿税甫罢而旋兴，诸采榷使，方忧喜交并间，得此消息，争市瑰异未名之宝，名“孝顺钱粮”。充金帛之媵，左藏为之充牣",
          "一般掌故", "矿税使借上寿献媚", "文献转引", "补正史之阙")
add("events", V, [ev1, ev2])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-046", "上寿之举", "中立",
        "作者谓此举虽似不经，亦古所谓此非恶心也",
        "此举虽似不经，亦古所谓此非恶心也",
        "中立评述", "客观", "传闻", targets=[e_jinshang3["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "02-046", "榷税纵横", "否定",
        "作者谓圣情果大怡后乾德寿皇小南内诸工一切惟群下所请，而榷税纵横愈不可谏止矣",
        "而榷税纵横，愈不可谏止矣。然但行之禁掖，惟阉尹宫娃辈共献谀词而已，不以闻之大廷。故谏官无敢以其事显诤者",
        "讽刺", "愤慨", "传闻"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-046", "万历壬寅", "上",
         "万寿合七十岁上寿", "万历间", "大内", "风俗",
         "壬寅之岁，上圣龄甫满四旬，而御极已三十年",
         "万历", "亲闻", who_ents=[e_jinshang3["ent_id"]], ref_evts=[ev1["event_id"]],
         supp="内廷以上寿博天颜一启，矿税使献孝顺钱粮"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-046", "万寿进奉之滥", "财政",
         "万历壬寅矿税使以上寿为名进奉瑰异",
         "矿税甫罢旋兴，诸采榷使争市瑰异未名之宝名孝顺钱粮，大小监局竞奢斗侈罄其力以备进奉，左藏充牣；圣情大怡后诸工一切惟群下所请，榷税纵横不可谏止",
         "完全违背", "时矿税甫罢而旋兴，诸采榷使，方忧喜交并间，得此消息，争市瑰异未名之宝，名“孝顺钱粮”",
         "补正史之阙", figures=[e_jinshang3["ent_id"]]),
])

# ---- 02-049 章奏留中 ----
e_jinshang4 = E("02-049", "今上", "万历帝", "person", ("主体",), span="万历")
e_fuqing = E("02-049", "福清", "叶向高", "person", ("关联人物",), span="万历")
add("ents", V, [e_jinshang4, e_fuqing])

ev1 = EVT(rid("events", V, "EVT"), "02-049", "朝政", "今上",
          "章奏一切庋之禁中", "上厌臣下之屡聒，一切庋之禁中屡催不下，遇大小兴革主者自行其意第具本题知不复取上意可否",
          "万历中", "北京", "自今上厌臣下之屡聒，一切庋之禁中，屡催不下。初亦甚以为为苦，久而稍习，遇大小兴革，主者自行其意，第具本题知，不复取上意可否。而大权反下移矣",
          "制度变动", "章奏留中致大权下移", "文献转引", "异于正史",
          who_ents=[e_jinshang4["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "02-049", "朝政", "建言之人",
          "讲旨之例", "台省建白当取旨者，建言之人上疏以后即请谒政府云此本当条旨，政府唯唯如命一同属吏禀承长官，名曰讲旨",
          "万历中", "北京", "台省建白，间有当取旨者，则建言之人上疏以后，即请谒政府，云此本当条旨云云。政府即唯唯如命，一同属吏之禀承於长官，其名曰讲旨",
          "制度变动", "条旨之权下移政府", "文献转引", "正史不载")
add("events", V, [ev1, ev2])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "02-049", "程序", ["例"],
         "题本用印", "衙门",
         "题本用印系衙门公事例不留中，即不当上意再三更改亦可",
         "若题本用印，则系衙门公事，例不留中。即不当上意，再三更改亦可",
         "惯例", "名存实亡", "万历中", viol="自今上厌臣下之屡聒，一切庋之禁中，屡催不下"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-049", "章奏留中", "否定",
        "作者谓大权反下移矣，讲旨为互古未有之事",
        "而大权反下移矣",
        "感慨", "严肃", "亲闻", targets=[e_jinshang4["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "02-049", "讲旨之例", "讽刺",
        "作者谓政府唯唯如命一同属吏禀承长官，名曰讲旨，此互古未有之事，福清在时尚未然",
        "政府即唯唯如命，一同属吏之禀承於长官，其名曰讲旨。此互古未有之事，福清在时，尚未然",
        "讽刺", "嘲讽", "亲闻", targets=[e_fuqing["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-049", "万历中", "今上",
         "章奏留中与讲旨", "万历间", "北京", "朝政",
         "自今上厌臣下之屡聒，一切庋之禁中，屡催不下",
         "万历", "亲闻", who_ents=[e_jinshang4["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"]],
         supp="题本例不留中之制见毁于留中，讲旨为互古未有"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-049", "章奏处理制度", "官制",
         "先朝题本例不留中，万历中上厌屡聒一切庋之禁中",
         "先朝章奏不报闻者多是奏本，题本用印系衙门公事例不留中；自今上厌臣下屡聒，一切庋之禁中屡催不下，主者自行其意第具本题知，不复取上意可否；台省建白当取旨者请谒政府讲旨，大权下移",
         "名存实亡", "自今上厌臣下之屡聒，一切庋之禁中，屡催不下",
         "异于正史", figures=[e_jinshang4["ent_id"], e_fuqing["ent_id"]]),
])

# ---- 02-050 端阳 ----
e_jinshang5 = E("02-050", "今上", "万历帝", "person", ("关联人物",), span="万历")
e_xiaozong = E("02-050", "孝宗", "弘治帝", "person", ("引用人物",), span="弘治")
e_shizong8 = E("02-050", "世宗", "嘉靖帝", "person", ("引用人物",), span="嘉靖")
e_lishi = E("02-050", "李时", "李时", "person", ("关联人物",), span="嘉靖")
e_xiayan2 = E("02-050", "夏言", "夏言", "person", ("关联人物",), span="嘉靖")
e_guoxun = E("02-050", "郭勋", "郭勋", "person", ("关联人物",), span="嘉靖")
e_wanggongxiang = E("02-050", "王恭襄", "王宪", "person", ("关联人物",), span="正德", conf="medium")
add("ents", V, [e_jinshang5, e_xiaozong, e_shizong8, e_lishi, e_xiayan2,
                e_guoxun, e_wanggongxiang])

ev1 = EVT(rid("events", V, "EVT"), "02-050", "军事", "今上",
          "午日内操选内侍三千", "甲申岁午日预选少年强壮内侍三千名俱先娴习骑射，至期弯弧骋辔云锦成群，上大悦党赉二万余金",
          "万历甲申午日", "大内", "自内操事兴，至甲申岁之午日，预选少年强壮内侍三千名，俱先娴习骑射，至期弯弧骋辔，云锦成群，有京营所不逮者。上大悦，党赉二万余金",
          "一般掌故", "内操之盛京营不逮", "文献转引", "正史不载",
          who_ents=[e_jinshang5["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "02-050", "军事", "今上",
          "癸未谒陵始选内臣扈从", "今上因癸未谒陵始选内臣具军容扈从，旋跸后益广其伍，俱江陵败后事",
          "万历癸未", "陵寝", "今上因癸未谒陵，始选内臣具军容扈从，旋跸后益广其伍，俱江陵败后事也",
          "一般掌故", "内臣军容扈从之始", "文献转引", "补正史之阙",
          who_ents=[e_jinshang5["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "02-050", "军事", "正德诸阉",
          "内操起于正德初年", "禁本非观兵之所，内操其事起于正德初年，八虎辈各有裨列校仿效外廷，本兵王恭襄亦杂处中贵之中",
          "正德初", "大内", "按禁本非观兵之所，其事起于正德初年，盖不特八虎辈各有裨列校，仿效外廷，而本兵王恭襄，亦顶罛刺飘靛缨，杂处于中贵之中矣",
          "一般掌故", "内操之始", "文献转引", "正史不载",
          who_ents=[e_wanggongxiang["ent_id"]])
add("events", V, [ev1, ev2, ev3])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "02-050", "允许", ["得拜"],
         "令节赐物", "朝廷",
         "阁部大老及经筵日讲词臣得拜川扇香药诸赐，视他令节独优",
         "惟阁部大老，及经筵日讲词臣，得拜川扇香药诸赐，视他令节独优",
         "惯例", "遵行", "万历初"),
])

add("rels", V, [
    REL(rid("rels", V, "REL"), "02-050", "夏言", "郭勋", "同僚", "双向",
        "最后十五年，又同李时、夏言、郭勋泛舟西苑，赋诗唱和",
        "最后十五年，又同李时、夏言、郭勋泛舟西苑，赋诗唱和",
        pa_ents=[e_xiayan2["ent_id"]], pb_ents=[e_guoxun["ent_id"]],
        evo="同泛西苑赋诗唱和", span="嘉靖十五年"),
])

add("cits", V, [
    CIT(rid("cits", V, "CIT"), "02-050", "孝宗手书桃符", "直引",
        "作者记孝宗遇午节会于便殿手书一桃符，盖圣主好文宴衎自娱",
        "闻之先辈云：孝宗在御日，遇午节会于便殿手书一桃符，云：“采线结成长命缕，丹砂书就辟兵符。”盖圣主好文，宴衎自娱，又与后圣不同如此",
        "掌故引用", quoted="采线结成长命缕，丹砂书就辟兵符"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-050", "内操寝息", "否定",
        "作者谓近年来内教场已鞠为茂草，想武事置不讲矣",
        "近年来则内教场已鞠为茂草，想武事置不讲矣",
        "感慨", "惋惜", "亲闻"),
    OPN(rid("opns", V, "OPN"), "02-050", "寒食禁火之害", "否定",
        "作者谓介子推以五月五日自焚，古来以冬至后一百五日禁火，太原峭冷未解人多有死者，何不考订改正",
        "按介子推以五月五日自焚，而古来就以冬至后一百五日禁火，太原之地峭冷未解，因禁烟寒食。人多有死者。何不考订改正？",
        "考辨", "严肃", "传闻"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-050", "正德—万历", "今上",
         "午节射柳走骠骑与内操", "万历间", "京师", "风俗",
         "京师及边镇最重午节，至今各边，是日俱射柳较胜",
         "跨朝", "亲闻", who_ents=[e_jinshang5["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"]],
         supp="午节射柳、走骠骑、内操沿革与孝宗桃符故事"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-050", "内操制度", "军事",
         "正德初起于中贵仿效外廷，万历初广其伍，后寝",
         "内操起于正德初年，八虎辈各有裨列校仿效外廷，本兵王恭襄杂处中贵；今上癸未谒陵始选内臣具军容扈从，旋跸益广其伍；甲申午日预选内侍三千娴习骑射，党赉二万余金；然内教场已鞠为茂草，武事置不讲",
         "名存实亡", "近年来则内教场已鞠为茂草，想武事置不讲矣",
         "补正史之阙", figures=[e_jinshang5["ent_id"], e_wanggongxiang["ent_id"]]),
])

# ---- 02-051 七夕 ----
e_liyu = E("02-051", "李煜", "李煜", "person", ("关联人物",), span="五代")
e_congyi = E("02-051", "从益", "李从益", "person", ("关联人物",), span="五代")
add("ents", V, [e_liyu, e_congyi])

ev1 = EVT(rid("events", V, "EVT"), "02-051", "社会", "江浙间",
          "七夕先一日乞巧成俗", "江南李煜以七夕生，其弟从益自润州赴贺乃先一日乞巧，江浙间俱化之遂以成俗，直至宋化间始诏更定仍为七夕",
          "南唐—宋初", "江浙", "江南李煜以七夕生，至期其弟从益自润州赴贺，乃先一日乞巧，江浙间俱化之，遂以成俗，直至宋化间始诏更定仍为七夕",
          "一般掌故", "七夕前一日乞巧成俗后诏更定", "文献转引", "正史不载")
add("events", V, [ev1])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-051", "七夕更定之异", "讽刺",
        "作者谓先一日乞巧化之成俗直至宋间始诏更定，亦奇事也",
        "直至宋化间始诏更定仍为七夕。亦奇事也",
        "感慨", "嘲讽", "传闻"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-051", "今", "今上",
         "朝家七夕无闻", "万历间", "京师", "风俗",
         "今内廷虽尚设乞巧山子，兵仗局进乞巧针，至宫嫔辈则皆衣鹊桥补服，而外廷侍从不及拜赐矣，惟大榼辈以瓜果相饷遗",
         "万历", "亲闻", supp="内廷乞巧之设与外廷不及拜赐"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-051", "七夕乞巧之典", "礼制",
         "宋世禁中以金银摩睺罗分赐大臣，今内廷尚设乞巧山子进乞巧针",
         "宋世禁中以金银摩睺罗为玩具分赐大臣；今内廷尚设乞巧山子，兵仗局进乞巧针，宫嫔衣鹊桥补服，外廷侍从不及拜赐，惟大榼以瓜果相饷遗；民间闺阁儿女尚修乞巧故事而朝家独无闻",
         "名存实亡", "今内廷虽尚设乞巧山子，兵仗局进乞巧针，至宫嫔辈则皆衣鹊桥补服，而外廷侍从不及拜赐矣",
         "正史不载", figures=[]),
])

# ---- 02-053 六曹答诏称卿 ----
e_jinshang6 = E("02-053", "今上", "万历帝", "person", ("主体",), span="万历")
e_wanggeishi = E("02-053", "王给事", "王忽", "person", ("关联人物",), span="万历", conf="low")
add("ents", V, [e_jinshang6, e_wanggeishi])

ev1 = EVT(rid("events", V, "EVT"), "02-053", "制度变动", "今上",
          "己亥大计南六卿复称卿", "万历己亥大计南六卿自陈，旨下有得称卿者，一时以为荣遇，自后渐复旧制",
          "万历己亥", "北京", "万历己亥大计，南六卿自陈，旨下，有得称卿者，一时以为荣遇。自后渐复旧制，可谓厘正陋规矣",
          "制度变动", "南六卿答诏由叱名复称为卿", "文献转引", "补正史之阙",
          who_ents=[e_jinshang6["ent_id"]])
add("events", V, [ev1])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "02-053", "程序", ["称"],
         "六曹答诏", "朝廷",
         "六尚书与左右都御史一切谢恩乞休之类旨下皆称卿，以示重不论南北",
         "从来六尚书与左右都御史，一切谢恩乞休之类，旨下皆称卿，以示重，不论南北也",
         "惯例", "变通", "嘉靖之末以来",
         viol="嘉靖之末以至今上初年，凡南六卿一切叱名"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-053", "南六卿叱名", "否定",
        "作者谓嘉靖之末以至今上初年凡南六卿一切叱名，识者以为非体",
        "嘉靖之末，以至今上初年，凡南六卿一切叱名，识者以为非体",
        "贬斥", "严肃", "传闻"),
    OPN(rid("opns", V, "OPN"), "02-053", "王给事献媚之讥", "讽刺",
        "作者谓王给事辅臣条旨谓其献媚大僚为植党地，盖未谙典故耳",
        "王给事忽于建白疏内，辅臣条旨之，谓其献媚大僚，为植党地，盖未谙典故耳",
        "讽刺", "嘲讽", "传闻", targets=[e_wanggeishi["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-053", "万历己亥", "今上",
         "南六卿答诏复称卿", "万历间", "北京", "制度",
         "万历己亥大计，南六卿自陈，旨下，有得称卿者，一时以为荣遇",
         "万历", "亲闻", who_ents=[e_jinshang6["ent_id"]], ref_evts=[ev1["event_id"]],
         supp="南六卿由叱名复称卿，厘正陋规"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-053", "诏敕称卿之制", "官制",
         "六尚书都御史谢恩乞休旨下称卿，嘉靖末南六卿叱名，万历己亥复旧",
         "从来六尚书与左右都御史一切谢恩乞休之类旨下皆称卿以示重不论南北；嘉靖之末以至今上初年南六卿一切叱名，识者以为非体；万历己亥大计南六卿自陈有得称卿者，一时以为荣遇，自后渐复旧制",
         "变通", "从来六尚书与左右都御史，一切谢恩乞休之类，旨下皆称卿，以示重，不论南北也",
         "补正史之阙", figures=[e_jinshang6["ent_id"]]),
])

# ---- 02-054 御座后扇 ----
e_jinshang7 = E("02-054", "今主上", "万历帝", "person", ("主体",), span="万历")
e_zhuoying = E("02-054", "卓影", "卓影", "artifact", ("客体",))
add("ents", V, [e_jinshang7, e_zhuoying])

ev1 = EVT(rid("events", V, "EVT"), "02-054", "朝政", "今主上",
          "御门常朝执卓影卫座", "上御门常朝黼扆之后内执黄帕裹之有柄物，上升座拥蔽于后降座撤去，从来不曾展开，名曰卓影",
          "万历中", "皇极门", "今主上御门常朝，黼扆之后，内执一有柄之物，若擎扇然，用黄帕裹之，自上升座拥蔽于后，降座则撤去，从来不曾展开",
          "轶闻", "御朝仪卫用外夷所贡瑞物", "文献转引", "正史不载",
          who_ents=[e_jinshang7["ent_id"]])
add("events", V, [ev1])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "02-054", "卓影之名与用", "怀疑",
        "作者谓或疑为雉尾之属终莫知其真，后闻其名曰卓影乃先朝外夷所贡瑞物最能祓除不祥，未知果否",
        "后闻其名曰“卓影”，乃先朝外夷所贡瑞物，最能祓除不祥，以故临朝辄举，以卫御座。未知果否？",
        "考辨", "客观", "亲闻", targets=[e_zhuoying["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "02-054", "万历中", "今主上",
         "御座后扇卓影", "万历间", "皇极门", "制度",
         "今主上御门常朝，黼扆之后，内执一有柄之物，若擎扇然，用黄帕裹之，自上升座拥蔽于后",
         "万历", "亲闻", who_ents=[e_jinshang7["ent_id"]], ref_evts=[ev1["event_id"]],
         supp="御座后所执黄帕裹物名卓影，外夷所贡祓除不祥"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "02-054", "御朝仪卫之制", "礼制",
         "万历中御门常朝以卓影拥蔽御座",
         "上御门常朝黼扆之后内执黄帕裹之有柄物，上升座拥蔽于后降座撤去不曾展开，名曰卓影，乃先朝外夷所贡瑞物，最能祓除不祥，以故临朝辄举以卫御座",
         "遵行", "今主上御门常朝，黼扆之后，内执一有柄之物，若擎扇然，用黄帕裹之，自上升座拥蔽于后",
         "正史不载", figures=[e_jinshang7["ent_id"], e_zhuoying["ent_id"]]),
])

# ================================================================ 卷 03
V = "03"

# ---- 03-007 高丽女见疑 ----
e_shang_hw = E("03-007", "上", "朱元璋", "person", ("主体",), span="洪武")
e_zhouyi = E("03-007", "周谊", "周谊", "person", ("客体",), span="元—明初")
e_gengshenjun = E("03-007", "庚申君", "元顺帝", "person", ("关联人物",), span="元末")
add("ents", V, [e_shang_hw, e_zhouyi, e_gengshenjun])

ev1 = EVT(rid("events", V, "EVT"), "03-007", "边政", "太祖",
          "敕辽东备高丽", "洪武十三年高丽愆贡期，上赐诏诘责，敕辽东都指挥使司备谊女在宫之疑，命遣谊来京别有以处之",
          "洪武十三年", "辽东", "洪武十三年，高丽愆贡期，上赐诏诘责之。既而彼国遣使周谊来计事，上敕辽东都指挥使司曰：“高丽朝贡违约，朕拘其使，后纵之归，乃复怀诈，令谊作行人，非有谋而何？前元庚申君曾纳谊女于宫中，庚申君出奔，内臣得此女以归，今高丽数遣谊来使，殊有意焉，卿不可不备。敕至当遣谊来京，别有以处之。”",
          "重大政治", "以防女戎严敕边将", "文献转引", "补正史之阙",
          who_ents=[e_shang_hw["ent_id"], e_zhouyi["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "03-007", "边政", "太祖",
          "高丽入境者皆止于边", "命边将自今入境者皆止于边不许入见，虽有贡赋亦不许入献",
          "洪武十三年", "辽东", "仍命边将：“自今入境者，皆止于边，不许入见，虽有贡赋亦不许入献。”",
          "制度变动", "高丽贡使止于边不得入献", "文献转引", "补正史之阙",
          who_ents=[e_shang_hw["ent_id"]])
add("events", V, [ev1, ev2])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "03-007", "禁止", ["不许"],
         "高丽贡使入境", "高丽使者",
         "入境者皆止于边，不许入见，虽有贡赋亦不许入献",
         "仍命边将：“自今入境者，皆止于边，不许入见，虽有贡赋亦不许入献。”",
         "诏令", "遵行", "洪武十三年", subj_ents=[e_shang_hw["ent_id"]],
         purpose="严防女戎"),
])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "03-007", "周谊", "礼曹判书", "洪武十三年",
         "现任", "及周谊至京，署本国衔，为礼曹判书",
         "及周谊至京，署本国衔，为礼曹判书。上赐以袭衣，遣通事先归，留谊于京师",
         person_ents=[e_zhouyi["ent_id"]], inst="高丽礼曹", contro="有争议",
         ctx="署本国衔来京被留"),
])

add("rels", V, [
    REL(rid("rels", V, "REL"), "03-007", "周谊", "庚申君", "其他", "单向",
        "前元庚申君曾纳谊女于宫中，庚申君出奔，内臣得此女以归",
        "前元庚申君曾纳谊女于宫中，庚申君出奔，内臣得此女以归，今高丽数遣谊来使，殊有意焉",
        pa_ents=[e_zhouyi["ent_id"]], pb_ents=[e_gengshenjun["ent_id"]],
        evo="谊女曾纳元宫，元亡内臣得之归明", conseq="太祖终以女在宫为疑",
        strength="直接表述", span="元末—洪武十三年"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "03-007", "太祖严防女戎", "肯定",
        "作者谓圣主之严防女戎如此，又安得褒女骊姬之祸乎",
        "盖终以女在宫为疑。圣主之严防女戎如此，又安得褒女、骊姬之祸乎？",
        "褒扬", "严肃", "传闻", targets=[e_shang_hw["ent_id"]],
        parallel="周幽王褒姒、晋献公骊姬之祸"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "03-007", "洪武十三年", "太祖",
         "高丽女见疑严备边", "洪武间", "辽东", "边政",
         "洪武十三年，高丽愆贡期，上赐诏诘责之",
         "洪武", "传闻", who_ents=[e_shang_hw["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"]],
         supp="以谊女在宫为疑，高丽贡使止于边不许入献"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "03-007", "高丽朝贡之限", "边政",
         "洪武十三年高丽愆贡被诘，终以谊女在宫为疑",
         "高丽朝贡违约，前元庚申君曾纳周谊女于宫中，元亡内臣得此女以归；太祖敕辽东备之，遣谊来京别有以处之，留谊于京师；命边将自今入境者皆止于边不许入见，虽有贡赋亦不许入献",
         "遵行", "仍命边将：“自今入境者，皆止于边，不许入见，虽有贡赋亦不许入献。”",
         "补正史之阙", figures=[e_shang_hw["ent_id"], e_zhouyi["ent_id"]]),
])

# ---- 03-011 封妃异典 ----
e_taizu5 = E("03-011", "高皇帝", "朱元璋", "person", ("关联人物",), span="洪武")
e_xuanzong = E("03-011", "宣宗", "朱瞻基", "person", ("关联人物",), span="宣德")
e_xiaogonghou = E("03-011", "孝恭后", "孙氏", "person", ("关联人物",), span="宣德—正统")
e_shizong9 = E("03-011", "世宗", "嘉靖帝", "person", ("主体",), span="嘉靖")
e_rongfei = E("03-011", "荣妃杨氏", "杨氏", "person", ("关联人物",), span="嘉靖")
e_xiaojiehou = E("03-011", "孝洁皇后", "陈氏", "person", ("关联人物",), span="嘉靖")
e_shangmeiren = E("03-011", "尚美人", "尚氏", "person", ("关联人物",), span="嘉靖")
e_shoufei = E("03-011", "寿妃", "尚氏", "person", ("关联人物",), span="嘉靖")
add("ents", V, [e_taizu5, e_xuanzong, e_xiaogonghou, e_shizong9, e_rongfei,
                e_xiaojiehou, e_shangmeiren, e_shoufei])

ev1 = EVT(rid("events", V, "EVT"), "03-011", "宫廷", "高皇帝",
          "册李氏淑妃郭氏宁妃", "洪武十七年甲子册李氏为皇淑妃，进封郭氏为皇宁妃，而贵妃反不得皇字",
          "洪武十七年", "大内", "如高皇帝洪武十七年甲子，册李氏为皇淑妃，又进封郭氏为皇宁妃，而贵妃反不得“皇”字，此其异也",
          "一般掌故", "皇字未专属贵妃", "文献转引", "补正史之阙",
          who_ents=[e_taizu5["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "03-011", "宫廷", "世宗",
          "追封荣妃杨氏", "荣妃杨氏以宫人随上遭火灾而得追贲，谥以恭淑安僖四字，祔葬于孝洁皇后之侧",
          "嘉靖中", "大内", "如追封荣妃杨氏，乃以宫人随上遭火灾而得追贲，且谥以恭淑安僖四字，且祔葬于孝洁皇后之侧。此殊特之典，又前此未有者",
          "一般掌故", "宫人追妃并四字谥", "文献转引", "补正史之阙",
          who_ents=[e_rongfei["ent_id"], e_shizong9["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "03-011", "宫廷", "世宗",
          "击磬误槌幼者承宠", "世宗诵经运手击磬偶误槌他处，惟一幼者失声大笑，经辍后遂承更衣之宠，即尚美人，时年仅十三",
          "嘉靖中", "西宫", "闻之老内侍云：世宗一日诵经，运手击磬，偶误槌他处，诸侍女皆俯首不敢仰，惟一幼者失声大笑。上注目顾之，咸谓命在顷刻矣。经辍后，遂承更衣之宠，即世所称尚美人是也。从此贵宠震天下，时年仅十三，世宗已将耳顺矣",
          "人物转折", "幼者以大笑承宠贵震天下", "传闻", "正史不载",
          who_ents=[e_shangmeiren["ent_id"], e_shizong9["ent_id"]])
ev4 = EVT(rid("events", V, "EVT"), "03-011", "宫廷", "世宗",
          "册寿妃百余日上大渐", "其后册拜为寿妃，拜后百余日而上大渐，寿妃之薨在万历三十八年庚戌",
          "嘉靖末", "大内", "其后册拜为寿妃，拜后百余日，而上大渐。说者归罪寿妃，微似汉成帝之赵昭仪云。寿妃之薨，在万历三十八年庚戌。宫嫔承恩早，而下世晚者，近代少其比",
          "人物转折", "寿妃之宠与上大渐", "文献转引", "正史不载",
          who_ents=[e_shoufei["ent_id"]])
add("events", V, [ev1, ev2, ev3, ev4])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "03-011", "程序", ["必加"],
         "承恩殁没", "朝廷",
         "承恩殁没者必加封内爵，以是外廷得闻",
         "然承恩殁没者，必加封内爵，以是外廷得闻",
         "惯例", "遵行", "历朝"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "03-011", "荣妃追封之典", "肯定",
        "作者谓此殊特之典又前此未有者",
        "此殊特之典，又前此未有者",
        "考辨", "客观", "传闻", targets=[e_rongfei["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "03-011", "归罪寿妃", "讽刺",
        "作者谓说者归罪寿妃，微似汉成帝之赵昭仪云",
        "说者归罪寿妃，微似汉成帝之赵昭仪云",
        "讽刺", "嘲讽", "传闻", targets=[e_shoufei["ent_id"]],
        parallel="汉成帝赵昭仪"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "03-011", "洪武—嘉靖", "世宗",
         "妃嫔加皇字与追封之典", "明初以来", "大内", "制度",
         "皇贵妃始于宣庙朝，是固然矣。然亦有异者",
         "跨朝", "传闻", who_ents=[e_shizong9["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"], ev4["event_id"]],
         supp="皇字专属贵妃之始、荣妃追封、尚美人承宠、寿妃薨年诸异典"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "03-011", "妃嫔封号制度", "礼制",
         "皇贵妃之称始宣庙，此前皇字未专属贵妃",
         "洪武十七年册李氏皇淑妃、郭氏皇宁妃而贵妃不得皇字；文皇嫔御自贤妃下二十余人无得皇字者；至宣宗孝恭后而皇字始专属贵妃；世宗晚年西宫奉玄掖庭体例稍异，未封妃嫔之呼、荣妃追封四字谥、承恩殁没必加内爵皆为异典",
         "变通", "至宣宗孝恭后后，而“皇”字始专属贵妃矣",
         "补正史之阙", figures=[e_xuanzong["ent_id"], e_xiaogonghou["ent_id"], e_shizong9["ent_id"]]),
])

# ---- 03-023 颁行女训 ----
e_shizong10 = E("03-023", "世宗", "嘉靖帝", "person", ("主体",), span="嘉靖")
e_zhangshengtaihou = E("03-023", "章圣太后", "蒋氏", "person", ("主体",), span="嘉靖")
e_xiandi = E("03-023", "献帝", "朱祐杬", "person", ("关联人物",), span="嘉靖追崇")
e_zhangcong2 = E("03-023", "张璁", "张璁", "person", ("关联人物",), span="嘉靖")
e_guie2 = E("03-023", "桂萼", "桂萼", "person", ("主体",), span="嘉靖")
e_zhengfei = E("03-023", "郑妃", "郑氏", "person", ("关联人物",), span="万历")
add("ents", V, [e_shizong10, e_zhangshengtaihou, e_xiandi, e_zhangcong2, e_guie2, e_zhengfei])

ev1 = EVT(rid("events", V, "EVT"), "03-023", "朝政", "世宗",
          "欲刊行女训内训", "世宗以章圣太后所著《女训》示辅臣，复以《慈孝高皇后传》及仁孝皇后《内训》同示，欲与《女训》并刊行，张璁赞美请上御制跋语，奉旨允行",
          "嘉靖中", "北京", "世宗以章圣太后所著《女训》一卷示辅臣，其首即献帝为之序，次即太后自序，为目十有二。已复以《慈孝高皇后传》及仁孝皇后《内训》同示，欲与《女训》并刊行。辅臣张璁赞美，请上御制跋语于后，已奉旨允行矣",
          "一般掌故", "女训内训得旨刊行", "文献转引", "补正史之阙",
          who_ents=[e_shizong10["ent_id"], e_zhangshengtaihou["ent_id"], e_zhangcong2["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "03-023", "朝政", "桂萼",
          "献谀请设官女学", "次辅桂萼献谀谓宜仿古胎教选哲妇轮直，令两京布政司府州县各修官女学设庙奉先代女师之神，选行义父老掌其事每年十月开学十二月止",
          "嘉靖中", "北京", "次辅桂萼复献谀，谓《女训》一书，臣拜观详味，知天启中兴，圣贤继出，胚胎于此矣。宜仿古胎教，妊子及月，将二南诗古诗编成简明说词，选哲妇十余人以备轮直，凡中宫图书花鸟寓目之物，尤当一一拣择。又令两京布政司府州县各修官女学，设庙奉先代女师之神；傍有廊，为习女工之所；中一堂，为听教之堂。选行义父老掌其事，每年十月开学，十二月止",
          "一般掌故", "迂诞不经之议", "文献转引", "正史不载",
          who_ents=[e_guie2["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "03-023", "人事", "桂萼",
          "以病去位寻卒于家", "次年之春萼即以病去位，寻卒于家",
          "嘉靖中", "北京", "次年之春，萼即以病去位，寻卒于家",
          "人物转折", "献谀者去位卒家", "文献转引", "补正史之阙",
          who_ents=[e_guie2["ent_id"]])
ev4 = EVT(rid("events", V, "EVT"), "03-023", "文化", "郑妃",
          "重刊吕氏闺范作序启大狱", "近年重刊《吕氏闺范》，翊坤宫郑妃作序，说者遂有僭逼之疑，致启大狱贻祸迄今未解",
          "万历中", "北京", "近年重刊《吕氏闺范》，翊坤宫郑妃作序，凝其书仁孝后之《女诫》、章圣后之《女训》。说者遂有僭逼之疑，致启大狱，贻祸迄今未解",
          "重大政治", "闺范作序启大狱", "文献转引", "补正史之阙",
          who_ents=[e_zhengfei["ent_id"]])
add("events", V, [ev1, ev2, ev3, ev4])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "03-023", "程序", ["令", "选"],
         "官女学之设", "两京布政司府州县",
         "各修官女学，设庙奉先代女师之神，选行义父老掌其事，每年十月开学十二月止",
         "又令两京布政司府州县各修官女学，设庙奉先代女师之神；傍有廊，为习女工之所；中一堂，为听教之堂。选行义父老掌其事，每年十月开学，十二月止",
         "奏议定", "未明", "嘉靖中", subj_ents=[e_guie2["ent_id"]]),
    RULE(rid("rules", V, "RULE"), "03-023", "程序", ["欲选"],
         "女七岁以上入学", "有家法之人",
         "选大家有家法之人为媒氏，女七岁以上入学习《女训》者书其年月名籍令之收掌，国有大嘉礼按籍而取之",
         "又欲选大家有家法之人为媒氏，凡女七岁以上入学习《女训》者，书其年月名籍，令之收掌。国有大嘉礼，按籍而取之",
         "奏议定", "未明", "嘉靖中", subj_ents=[e_guie2["ent_id"]]),
])

add("cits", V, [
    CIT(rid("cits", V, "CIT"), "03-023", "《女训》", "直引",
        "世宗以章圣太后所著女训一卷示辅臣，其首献帝为之序次太后自序为目十有二",
        "世宗以章圣太后所著《女训》一卷示辅臣，其首即献帝为之序，次即太后自序，为目十有二",
        "立论", work_ents=[], quoted="为目十有二"),
    CIT(rid("cits", V, "CIT"), "03-023", "《内训》", "泛引",
        "与慈孝高皇后传同示，欲与女训并刊行",
        "已复以《慈孝高皇后传》及仁孝皇后《内训》同示，欲与《女训》并刊行",
        "佐证"),
    CIT(rid("cits", V, "CIT"), "03-023", "《吕氏闺范》", "泛引",
        "近年重刊吕氏闺范，翊坤宫郑妃作序，凝其书仁孝后之女诫章圣后之女训",
        "近年重刊《吕氏闺范》，翊坤宫郑妃作序，凝其书仁孝后之《女诫》、章圣后之《女训》",
        "对比"),
])

add("rels", V, [
    REL(rid("rels", V, "REL"), "03-023", "桂萼", "张璁", "同僚", "双向",
        "辅臣张璁赞美，请上御制跋语于后，已奉旨允行矣。次辅桂萼复献谀",
        "辅臣张璁赞美，请上御制跋语于后，已奉旨允行矣。次辅桂萼复献谀",
        pa_ents=[e_guie2["ent_id"]], pb_ents=[e_zhangcong2["ent_id"]],
        evo="萼以次辅继璁而益为献谀", span="嘉靖中"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "03-023", "桂萼之疏", "否定",
        "作者谓观萼此疏欲谀悦取宠而迂诞不经令人齿冷，萼素以直名何澜倒至此",
        "观萼此疏，欲谀悦取宠而迂诞不经，令人齿冷。萼素以直名，何澜倒至此也？",
        "贬斥", "愤慨", "传闻", targets=[e_guie2["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "03-023", "人之将死其言也善", "否定",
        "作者引古人云人之将死其言也善，验之此公殆不其然",
        "古人云：“人之将死，其言也善。”验之此公，殆不其然",
        "讽刺", "嘲讽", "传闻", targets=[e_guie2["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "03-023", "郑妃作序启大狱", "否定",
        "作者谓说者遂有僭逼之疑致启大狱贻祸迄今未解，是时不知何人视草不识忌讳乃尔",
        "说者遂有僭逼之疑，致启大狱，贻祸迄今未解。是时不知何人视草，不识忌讳乃尔",
        "贬斥", "严肃", "亲闻", targets=[e_zhengfei["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "03-023", "嘉靖中—万历", "世宗",
         "刊行女训与设女学之议", "嘉靖间", "北京", "文化",
         "世宗以章圣太后所著《女训》一卷示辅臣，其首即献帝为之序，次即太后自序，为目十有二",
         "跨朝", "传闻", who_ents=[e_shizong10["ent_id"], e_zhangshengtaihou["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"], ev4["event_id"]],
         supp="女训内训刊行、桂萼献谀设女学、郑妃作序启大狱"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "03-023", "女学之制", "礼制",
         "嘉靖中桂萼请两京府州县修官女学，每年十月开学十二月止",
         "世宗刊行章圣太后女训及仁孝皇后内训；桂萼请仿古胎教选哲妇轮直，令两京布政司府州县各修官女学，设庙奉先代女师之神，傍廊习女工，中堂听教，选行义父老掌其事，教矇瞽之人以女训讲解背诵量与俸给，提学官岁考阅之；又欲选有家法之人为媒氏按籍取女",
         "未明", "又令两京布政司府州县各修官女学，设庙奉先代女师之神；傍有廊，为习女工之所；中一堂，为听教之堂。选行义父老掌其事，每年十月开学，十二月止",
         "正史不载", figures=[e_guie2["ent_id"]]),
])

# ---- 03-026 皇后祔庙之礼 ----
e_pengshi = E("03-026", "彭时", "彭时", "person", ("关联人物",), span="成化")
e_shanglu = E("03-026", "商辂", "商辂", "person", ("关联人物",), span="成化")
e_yaokui = E("03-026", "姚夔", "姚夔", "person", ("关联人物",), span="成化")
e_liujian = E("03-026", "刘健", "刘健", "person", ("关联人物",), span="弘治")
e_xiaozong2 = E("03-026", "孝宗", "朱祐樘", "person", ("主体",), span="弘治")
e_xianzong = E("03-026", "宪宗", "朱见深", "person", ("关联人物",), span="成化")
e_xiaozhuang = E("03-026", "孝庄", "钱氏", "person", ("关联人物",), span="成化—弘治")
e_xiaosu = E("03-026", "孝肃", "周氏", "person", ("关联人物",), span="成化—弘治")
e_xiaozhen = E("03-026", "孝贞", "王氏", "person", ("关联人物",), span="弘治")
e_xiaomu = E("03-026", "孝穆", "纪氏", "person", ("关联人物",), span="成化—弘治")
e_shizong11 = E("03-026", "世宗", "嘉靖帝", "person", ("关联人物",), span="嘉靖")
e_xiaolie = E("03-026", "孝烈", "方氏", "person", ("关联人物",), span="嘉靖")
add("ents", V, [e_pengshi, e_shanglu, e_yaokui, e_liujian, e_xiaozong2, e_xianzong,
                e_xiaozhuang, e_xiaosu, e_xiaozhen, e_xiaomu, e_shizong11, e_xiaolie])

ev1 = EVT(rid("events", V, "EVT"), "03-026", "朝政", "彭时",
          "成化初议孝庄祔葬", "葬嫡后于他所诚为悖谬，彭时商辂姚夔诸大臣回天，礼卿姚文敏疏以同尊并列毫无低昂婉劝，孝肃曲意勉从",
          "成化初", "北京", "当时彭时、商辂、姚夔诸大臣，回天之力固伟矣，然礼卿姚文敏疏中云：“慈懿葬于左，皇太后万年后葬于右；慈懿今日祔于庙，皇太后他日亦祔于庙。同尊并列毫无低昂。”其词甚婉，故孝肃曲意勉从",
          "重大政治", "孝庄得祔葬祔庙", "文献转引", "补正史之阙",
          who_ents=[e_pengshi["ent_id"], e_shanglu["ent_id"], e_yaokui["ent_id"], e_xiaozhuang["ent_id"], e_xiaosu["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "03-026", "朝政", "孝宗",
          "定一帝一后之制", "弘治甲子孝肃始崩，孝宗以二后合葬为非礼，因玄宫先就无可奈何仍旧贯；祔庙一事刘健等引唐宋二后三后并尊旧事，上曰祖宗以来惟一帝一后，健等称诵赞决而祔庙之议遂定",
          "弘治甲子", "北京", "至于祔庙一事，刘健等尚祖姚夔旧说，引唐宋二后三后并尊旧事，以待上之自裁。而上乃曰：“祖宗以来，惟一帝一后。今若并祔，乃从朕坏起。况孝穆为朕生母，尚祀于奉慈殿。”又有事须师古，末世鄙亵不足学之语。健等始称诵赞决，而祔庙之议遂定",
          "制度变动", "一帝一后永为后世法", "文献转引", "补正史之阙",
          who_ents=[e_xiaozong2["ent_id"], e_liujian["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "03-026", "朝政", "世宗",
          "先祔孝烈后", "世宗先祔孝烈后，宁非祧仁宗而不恤者，亦以一帝一后成规已定，恐他日身所并食者不为孝烈而为元配孝洁，故预为之谋",
          "嘉靖中", "北京", "最后世宗先祔孝烈后，宁非祧仁宗而不恤者，亦以一帝一后成规已定，恐他日身所并食者不为孝烈，而为元配之孝洁，故预为之谋，其心苦矣",
          "一般掌故", "祔庙成规下的预谋", "文献转引", "异于正史",
          who_ents=[e_shizong11["ent_id"], e_xiaolie["ent_id"]])
add("events", V, [ev1, ev2, ev3])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "03-026", "禁止", ["惟一帝一后"],
         "帝后祔庙", "朝廷",
         "祖宗以来惟一帝一后，不得并祔",
         "祖宗以来，惟一帝一后。今若并祔，乃从朕坏起。况孝穆为朕生母，尚祀于奉慈殿",
         "祖制", "遵行", "弘治以来", subj_ents=[e_xiaozong2["ent_id"]],
         purpose="嫡庶昭然不敢逾尺寸"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "03-026", "孝宗之仁而断", "肯定",
        "作者谓孝宗恪遵古礼嫡庶昭然不敢逾尺寸，何其仁而断耶，孝宗之为孝岂非千古一人哉",
        "则孝宗恪遵古礼，嫡庶昭然，不敢逾尺寸，何其仁而断耶？",
        "褒扬", "严肃", "传闻", targets=[e_xiaozong2["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "03-026", "世宗先祔孝烈", "否定",
        "作者谓世宗先祔孝烈宁非祧仁宗而不恤者，其心苦矣，又断圣子神孙他日定当补救匡正安肯违礼拂经",
        "最后世宗先祔孝烈后，宁非祧仁宗而不恤者，亦以一帝一后成规已定，恐他日身所并食者不为孝烈，而为元配之孝洁，故预为之谋，其心苦矣。孰知圣子神孙，他日定当补救匡正，安肯违礼拂经，以成先帝之过举耶！",
        "贬斥", "严肃", "传闻", targets=[e_shizong11["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "03-026", "成化—嘉靖", "孝宗",
         "一帝一后祔庙之定", "成化以来", "北京", "制度",
         "宗庙大事，有以忠愤太过，激成莫解之祸者，无如嘉靖初之议大礼",
         "跨朝", "传闻", who_ents=[e_xiaozong2["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"]],
         supp="成化孝庄祔葬、弘治定一帝一后、世宗先祔孝烈三事"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "03-026", "皇后祔庙之制", "礼制",
         "成化初孝庄议祔葬，弘治好定一帝一后永为后世法",
         "成化初葬嫡后于他所为悖谬，彭时商辂姚夔力争，姚文敏以同尊并列毫无低昂婉劝，孝肃曲意勉从；弘治甲子孝肃崩，孝宗以二后合葬为非礼，因玄宫先就仍旧贯；祔庙刘健等引唐宋旧事，上以祖宗以来惟一帝一后拒并祔，孝贞合葬茂陵与宪宗同入太庙，孝穆祔葬别祀；世宗先祔孝烈为一帝一后成规下的预谋",
         "遵行", "于是一帝一后，永为后世法矣",
         "补正史之阙", figures=[e_xiaozong2["ent_id"], e_liujian["ent_id"], e_yaokui["ent_id"]]),
])

# ---- 03-029 庄肃后丧礼 ----
e_shizong12 = E("03-029", "世宗", "嘉靖帝", "person", ("主体",), span="嘉靖")
e_wuzong = E("03-029", "武宗", "朱厚照", "person", ("关联人物",), span="正德")
e_zhuangsuhou = E("03-029", "庄肃夏后", "夏氏", "person", ("客体",), span="正德—嘉靖")
e_zhangshengtaihou2 = E("03-029", "章圣太后", "蒋氏", "person", ("关联人物",), span="嘉靖")
e_fujing = E("03-029", "孚敬", "张璁", "person", ("关联人物",), span="嘉靖")
e_gongfei = E("03-029", "恭妃", "恭妃", "person", ("关联人物",), span="成化")
add("ents", V, [e_shizong12, e_wuzong, e_zhuangsuhou, e_zhangshengtaihou2, e_fujing, e_gongfei])

ev1 = EVT(rid("events", V, "EVT"), "03-029", "宫廷", "世宗",
          "定庄肃后不服丧", "嘉靖十四年正月武宗庄肃夏后崩，上曰于皇兄后无服制又迫圣母寿诞当青服视事，礼臣改请服制既绝不必举哀臣下亦不必奉慰",
          "嘉靖十四年正月", "北京", "嘉靖十四年正月，武宗庄肃夏后崩。礼臣上仪注，疑上素冠服举哀，及群臣行奉慰礼。上曰：“朕于皇兄后无服制，又迫圣母寿诞，朕当青服视事。”于是礼臣改请：“皇上服制既绝，不必举哀，臣下亦不必奉慰。”",
          "一般掌故", "庄肃后之丧不行举哀奉慰", "文献转引", "补正史之阙",
          who_ents=[e_shizong12["ent_id"], e_zhuangsuhou["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "03-029", "宫廷", "孚敬",
          "请圣母圣诞吉服终日", "越七日为章圣太后寿诞，上命百官不必赴衙门但于私第尽制，辅臣孚敬等言圣母圣诞吉礼重大宜吉服终日，上始悦而许之",
          "嘉靖十四年正月", "北京", "越七日，即为章圣太后寿诞，上命百官不必赴衙门，但于私第尽制，盖视群情也。辅臣孚敬等言：“圣母圣诞，吉礼重大，宜吉服终日。”上始悦而许之",
          "一般掌故", "寿诞吉服之请", "文献转引", "正史不载",
          who_ents=[e_fujing["ent_id"], e_zhangshengtaihou2["ent_id"]])
add("events", V, [ev1, ev2])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "03-029", "禁止", ["无服", "服绝"],
         "皇兄后之丧", "世宗",
         "于皇兄后无服制，服制既绝不举哀，臣下亦不奉慰",
         "朕于皇兄后无服制，又迫圣母寿诞，朕当青服视事",
         "祖制", "变通", "嘉靖十四年", subj_ents=[e_shizong12["ent_id"]]),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "03-029", "无服之断", "否定",
        "作者谓庄肃于世宗为同堂从嫂祖宗亦服緦麻，乃上曰无服礼臣亦曰服绝，不得其解",
        "且庄肃于世宗为同堂从嫂，祖宗亦服緦麻。乃上曰无服，礼臣亦曰服绝，不得其解。时贵溪长礼部",
        "考辨", "严肃", "传闻", targets=[e_shizong12["ent_id"], e_fujing["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "03-029", "嘉靖十四年", "世宗",
         "庄肃后丧礼不服", "嘉靖间", "北京", "制度",
         "嘉靖十四年正月，武宗庄肃夏后崩",
         "嘉靖", "传闻", who_ents=[e_shizong12["ent_id"], e_zhuangsuhou["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"]],
         supp="皇兄后无服制与圣母寿诞吉服两事"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "03-029", "皇后丧礼之制", "礼制",
         "嘉靖十四年定皇兄后无服制",
         "武宗庄肃夏后崩，上以于皇兄后无服制且迫圣母寿诞，当青服视事；礼臣改请服制既绝不举哀，臣下亦不奉慰；越七日章圣太后寿诞，孚敬请吉服终日获允；又以宪庙恭妃初丧免元旦庆贺",
         "变通", "于是礼臣改请：“皇上服制既绝，不必举哀，臣下亦不必奉慰。”",
         "补正史之阙", figures=[e_shizong12["ent_id"], e_zhuangsuhou["ent_id"]]),
])

# ---- 03-034 圣母并尊 ----
e_jingdi = E("03-034", "景帝", "朱祁钰", "person", ("关联人物",), span="景泰")
e_sunshi = E("03-034", "孙氏", "孙太后", "person", ("关联人物",), span="景泰—天顺")
e_wushi = E("03-034", "吴氏", "吴贤妃", "person", ("关联人物",), span="景泰")
e_xianzong2 = E("03-034", "宪宗", "朱见深", "person", ("关联人物",), span="成化")
e_qianshi = E("03-034", "钱氏", "慈懿皇太后", "person", ("关联人物",), span="成化—弘治")
e_zhoushi = E("03-034", "周氏", "孝肃", "person", ("关联人物",), span="成化—弘治")
e_jinshang8 = E("03-034", "今上", "万历帝", "person", ("主体",), span="万历")
e_chenhou = E("03-034", "陈", "仁圣皇太后", "person", ("主体",), span="万历")
e_lifei = E("03-034", "李", "慈圣皇太后", "person", ("主体",), span="万历")
e_jiangling2 = E("03-034", "江陵", "张居正", "person", ("关联人物",), span="万历")
e_gaoxinzhneg = E("03-034", "高新郑", "高拱", "person", ("关联人物",), span="隆庆—万历")
add("ents", V, [e_jingdi, e_sunshi, e_wushi, e_xianzong2, e_qianshi, e_zhoushi,
                e_jinshang8, e_chenhou, e_lifei, e_jiangling2, e_gaoxinzhneg])

ev1 = EVT(rid("events", V, "EVT"), "03-034", "朝政", "今上",
          "两宫并进皇太后", "隆庆六年六月即位甫六日高新郑见逐，江陵奉上面谕欲并尊两宫且于生母皇贵妃更加二字徽号，遂与礼臣议两宫并进为皇太后，嫡母陈加仁圣生母李加慈圣",
          "隆庆六年六月", "北京", "直至隆庆六年，今上六月即位，甫六日而高新郑见逐，江陵奉上面谕，欲并尊两宫，且于生母皇贵妃更加二字徽号。盖故反其词，以遏止阁臣，使不得执奏也。于是江陵与礼臣议两宫并进为皇太后，而于嫡母陈加仁圣，生母李加慈圣，各二字徽号而体貌俱无少别矣",
          "重大政治", "两宫并尊体貌无别", "文献转引", "补正史之阙",
          who_ents=[e_jinshang8["ent_id"], e_chenhou["ent_id"], e_lifei["ent_id"], e_jiangling2["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "03-034", "朝政", "今上",
          "三宫并列先于并尊之典", "新郑逐时内臣捧诏旨出其首云皇后懿旨皇贵妃令旨皇帝圣旨，是时已三宫并列，窬月始举并尊圣母之典",
          "隆庆六年六月", "北京", "按新郑逐时，内臣捧诏旨出，其首云：“皇后懿旨，皇贵妃令旨，皇帝圣旨。”云云。是时已三宫并列矣。窬月始举并尊圣母之典，又安能止勿行也",
          "一般掌故", "三宫并列于诏旨已见", "文献转引", "正史不载")
add("events", V, [ev1, ev2])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "03-034", "程序", ["并进"],
         "两宫尊号", "江陵与礼臣",
         "两宫并进为皇太后，嫡母加仁圣、生母加慈圣，各二字徽号",
         "于是江陵与礼臣议两宫并进为皇太后，而于嫡母陈加仁圣，生母李加慈圣，各二字徽号而体貌俱无少别矣",
         "诏令", "遵行", "隆庆六年", subj_ents=[e_jiangling2["ent_id"]]),
    RULE(rid("rules", V, "RULE"), "03-034", "禁止", ["不得封", "不得丁忧"],
         "臣下嫡母在堂", "臣下",
         "嫡母在堂者生母不得封，即生母殁亦不得丁忧，其自爱者不过给假治丧",
         "历朝以来，臣下嫡母在堂者，生母不得封；即生母殁，亦不得丁忧，其自爱者不过给假治丧",
         "祖制", "名存实亡", "历朝",
         viol="今三母并封。登之令甲，而所生即媵婢，亦得尽三年之哀"),
])

add("rels", V, [
    REL(rid("rels", V, "REL"), "03-034", "张居正", "慈圣皇太后", "其他", "单向",
        "时江陵公方欲内谄慈圣，以为固权地",
        "时江陵公方欲内谄慈圣，以为固权地，苟可异礼，何所不至！",
        pa_ents=[e_jiangling2["ent_id"]], pb_ents=[e_lifei["ent_id"]],
        evo="借并尊两宫内谄慈圣以固权", conseq="议者责以不力谏",
        strength="推断", span="隆庆六年"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "03-034", "江陵并尊两宫", "否定",
        "作者谓江陵方欲内谄慈圣以为固权地，苟可异礼何所不至",
        "时江陵公方欲内谄慈圣，以为固权地，苟可异礼，何所不至！",
        "贬斥", "愤慨", "传闻", targets=[e_jiangling2["ent_id"], e_lifei["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "03-034", "议者责不力谏", "否定",
        "作者谓议者责以不力谏误矣，三母并封登之令甲固君父旷荡之恩锡类所及",
        "而议者责以不力谏，误矣！历朝以来，臣下嫡母在堂者，生母不得封；即生母殁，亦不得丁忧，其自爱者不过给假治丧。今三母并封。登之令甲，而所生即媵婢，亦得尽三年之哀。此固君父旷荡之恩，锡类所及",
        "考辨", "严肃", "传闻", targets=[e_jiangling2["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "03-034", "后唐庄宗冠履倒置", "讽刺",
        "作者谓后唐庄宗以嫡母为太妃而以生母为太后冠履倒置，盖胡虏不学使然真贻笑千古",
        "至后唐庄宗，以嫡母为太妃，而以生母为太后，冠履倒置，盖胡虏不学使然，真贻笑千古",
        "讽刺", "嘲讽", "传闻", parallel="后唐庄宗"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "03-034", "隆庆六年", "今上",
         "两宫并尊圣母", "隆庆末", "北京", "制度",
         "直至隆庆六年，今上六月即位，甫六日而高新郑见逐，江陵奉上面谕，欲并尊两宫",
         "隆庆", "亲闻", who_ents=[e_jinshang8["ent_id"], e_chenhou["ent_id"], e_lifei["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"]],
         supp="两宫并进皇太后各加二字徽号，前此三宫并列已见诏旨"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "03-034", "两宫并尊之制", "礼制",
         "隆庆六年两宫并进皇太后，嫡母加仁圣生母加慈圣",
         "唐宋人主为妃嫔所出者尊后为太后进所生母为皇太妃嫡庶尚分；本朝列帝非后出者多不并尊，惟景帝初登极尊孙氏上圣太后、吴氏皇太后，宪宗初元孝庄孝肃并以天下养而钱氏加徽号周氏无尊号以别等威；隆庆六年今上即位两宫并进皇太后，各加二字徽号而体貌俱无少别，三母并封登之令甲",
         "变通", "直至隆庆六年，今上六月即位，甫六日而高新郑见逐，江陵奉上面谕，欲并尊两宫",
         "补正史之阙", figures=[e_jinshang8["ent_id"], e_chenhou["ent_id"], e_lifei["ent_id"], e_jiangling2["ent_id"]]),
])

# ---- 03-035 两宫同在位久 ----
e_rensheng = E("03-035", "仁圣皇太后", "陈氏", "person", ("主体",), span="万历")
e_cisheng = E("03-035", "慈圣皇太后", "李氏", "person", ("主体",), span="万历")
e_qianhou = E("03-035", "钱后", "钱氏", "person", ("引用人物",), span="成化—弘治")
e_xiaosuzhou = E("03-035", "孝肃周后", "周氏", "person", ("引用人物",), span="成化—弘治")
add("ents", V, [e_rensheng, e_cisheng, e_qianhou, e_xiaosuzhou])

ev1 = EVT(rid("events", V, "EVT"), "03-035", "宫廷", "仁圣皇太后",
          "两宫父母俱存修家人之敬", "上御极之初两宫并尊如成化初年故事，钱后称太后止五年而仁圣享孝养者二十五年，初登长乐时与慈圣父母俱存尚修家人之敬俾得通藉禁中",
          "万历间", "大内", "又钱后称太后止五年，而仁圣享孝养者二十五年。且初登长乐时，与慈圣父母俱存，两宫圣母，尚修家人之敬，俾得通藉禁中，尤为亘古未有之福",
          "一般掌故", "两宫并养二十五年为亘古未有", "文献转引", "补正史之阙",
          who_ents=[e_rensheng["ent_id"], e_cisheng["ent_id"]])
add("events", V, [ev1])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "03-035", "两宫同加尊号", "肯定",
        "作者谓不如今上同加尊号情礼并申之为愉快",
        "不如今上同加尊号，情礼并申之为愉快",
        "褒扬", "严肃", "亲闻", targets=[e_rensheng["ent_id"], e_cisheng["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "03-035", "亘古未有之福", "肯定",
        "作者谓两宫父母俱存俾得通藉禁中尤为亘古未有之福，慈圣遐龄正未可量恐又非孝肃周后所能企耳",
        "俾得通藉禁中，尤为亘古未有之福。今慈圣遐龄正未可量，恐又非孝肃周后所能企耳",
        "感慨", "客观", "亲闻", targets=[e_rensheng["ent_id"], e_cisheng["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "03-035", "万历间", "今上",
         "两宫圣母同在位久", "万历间", "大内", "制度",
         "今上嫡母曰仁圣皇太后，生母曰慈圣皇太后，当上御极之初，即已并尊，如成化初年故事",
         "万历", "亲闻", who_ents=[e_rensheng["ent_id"], e_cisheng["ent_id"]],
         ref_evts=[ev1["event_id"]], supp="两宫并尊同加尊号，享养二十五年"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "03-035", "太后尊养之礼", "礼制",
         "万历初两宫并尊同加徽号，仁圣享孝养二十五年",
         "今上嫡母仁圣、生母慈圣，御极之初即已并尊如成化初年故事；不独同加尊号情礼并申，且初登长乐时两宫父母俱存，尚修家人之敬俾得通藉禁中；钱后称太后止五年，仁圣享孝养二十五年",
         "遵行", "又钱后称太后止五年，而仁圣享孝养者二十五年",
         "补正史之阙", figures=[e_rensheng["ent_id"], e_cisheng["ent_id"]]),
])

# ---- 03-036 今上笃厚中宫 ----
e_jinshang9 = E("03-036", "上", "万历帝", "person", ("主体",), span="万历")
e_wangdewan = E("03-036", "王德完", "王德完", "person", ("主体",), span="万历")
e_shenyiguan = E("03-036", "沈一贯", "沈一贯", "person", ("关联人物",), span="万历")
e_zhengguifei = E("03-036", "郑贵妃", "郑氏", "person", ("关联人物",), span="万历")
e_zhonggong = E("03-036", "中宫", "王皇后", "person", ("客体",), span="万历")
add("ents", V, [e_jinshang9, e_wangdewan, e_shenyiguan, e_zhengguifei, e_zhonggong])

ev1 = EVT(rid("events", V, "EVT"), "03-036", "朝政", "王德完",
          "露章力谏中宫之谤", "庚子之冬京师盛传中宫久病抑郁成疾，工科都给事中王德完新自家居补官至都始露章力谏其辞哀婉而危切，上大怒下诏狱拷讯究问主使",
          "万历庚子冬", "北京", "至庚子之冬，京师盛传中宫久病，侍卫不过数人，其膳修服御，俱为主上裁减大半，抑郁成疾，渐濒危殆，都下贵贱长幼皆信之。盖其时已传旨修东宫，次第册立，未几遂有此谤。疑上且顿抑中宫，使之不全，以为次子夺嫡之地。大小臣工，俱忧骇莫敢发。时，工科都给事中王德完，新自家居补官至都，始露章力谏，其辞哀婉而危切。上大怒，下诏狱拷讯，究问主使之人，九卿台省俱力救不从",
          "重大政治", "谏臣下诏狱而中宫得全", "文献转引", "异于正史",
          who_ents=[e_wangdewan["ent_id"], e_jinshang9["ent_id"], e_zhonggong["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "03-036", "朝政", "沈一贯",
          "以密揭婉解霁威", "首揆久谢病，次辅沈一贯以密揭婉解，次日忽下圣谕谓中宫乃圣母选择元配见今同居一宫何尝有疾，上稍为霁威并寝所传圣谕不下",
          "万历庚子", "北京", "从首揆久谢病，次辅沈一贯，以密揭婉解。次日，忽下圣谕云：“中宫乃圣母选择元配，见今同居一宫，少有过失，岂不优容！迩年稍稍悍戾不慈，朕每事教训，务全妇道，中宫亦知改悟，何尝有疾？”云云。辅臣回奏不报，一贯又上奏，谓：“今日之谤，十年前已鼎沸。故上前谕，惟示首臣，不使一人得见。若以此谕外传，外人必谓上果不利于中宫。则数年之谤，本虚而反以为实。上数年之旨，本实而反以为虚。天下藩府，以至万国四夷，岁进表笺，称贺中宫，倘闻此语，尤为未便。其他语尤过激虽堪。”上稍为霁威，且示以皇长子册立稍迟之故，并寝所传圣谕不下",
          "一般掌故", "密揭婉解圣谕寝不下", "文献转引", "补正史之阙",
          who_ents=[e_shenyiguan["ent_id"], e_jinshang9["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "03-036", "朝政", "今上",
          "特旨建储人心大定", "上重彝伦畏名义，忽闻中外浮言谏臣伏阙遂不胜愧悔，此后伉俪弥笃恩礼有加，次年即特旨建储人心大定，去冬弥天疑谤一旦冰释",
          "万历辛丑", "北京", "上重彝伦，畏名义，即简礼中宫，或亦一时咈意致然。忽闻中外浮言，谏臣伏阙，遂不胜愧悔。此后伉俪弥笃，恩礼有加。次年，即特旨建储，人心大定，去冬弥天疑谤，一旦冰释",
          "制度变动", "建储定而中宫谤冰释", "文献转引", "补正史之阙",
          who_ents=[e_jinshang9["ent_id"], e_zhonggong["ent_id"]])
add("events", V, [ev1, ev2, ev3])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "03-036", "王德完", "工科都给事中", "万历庚子",
         "贬谪", "工科都给事中王德完，新自家居补官至都，始露章力谏，其辞哀婉而危切",
         "时，工科都给事中王德完，新自家居补官至都，始露章力谏，其辞哀婉而危切。上大怒，下诏狱拷讯，究问主使之人，九卿台省俱力救不从",
         person_ents=[e_wangdewan["ent_id"]], contro="有争议",
         ctx="家居补官即谏中宫之谤，廷杖削籍得免于死"),
    APPT(rid("appts", V, "APPT"), "03-036", "沈一贯", "次辅", "万历庚子",
         "现任", "次辅沈一贯，以密揭婉解",
         "从首揆久谢病，次辅沈一贯，以密揭婉解",
         person_ents=[e_shenyiguan["ent_id"]], ctx="首揆谢病时以密揭婉解"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "03-036", "王德完之谏", "肯定",
        "作者谓给事虞渊取日功真不世，阁臣犯颜苦口甘犯天威其善亦未可没",
        "给事虞渊取日，功真不世，而阁臣犯颜苦口，甘犯天威，其善亦未可没也",
        "褒扬", "严肃", "亲闻", targets=[e_wangdewan["ent_id"], e_shenyiguan["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "03-036", "上之笃厚中宫", "肯定",
        "作者谓上重彝伦畏名义，即简礼中宫或亦一时咈意致然，忽闻中外浮言谏臣伏阙遂不胜愧悔，此后伉俪弥笃",
        "上重彝伦，畏名义，即简礼中宫，或亦一时咈意致然。忽闻中外浮言，谏臣伏阙，遂不胜愧悔。此后伉俪弥笃，恩礼有加",
        "褒扬", "客观", "亲闻", targets=[e_jinshang9["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "03-036", "万历庚子—辛丑", "今上",
         "中宫之谤与建储", "万历间", "北京", "朝政",
         "自丙申两宫灾后，上移居毓德宫，既而又移启祥宫",
         "万历", "亲闻", who_ents=[e_jinshang9["ent_id"], e_zhonggong["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"]],
         supp="庚子中宫久病之谤、王德完下诏狱、沈一贯密揭、辛丑特旨建储"),
])

# ---- 03-037 恭妃进封 ----
e_xiaogonghou2 = E("03-037", "孝恭", "孙氏", "person", ("引用人物",), span="宣德—正统")
e_jinshang10 = E("03-037", "今上", "万历帝", "person", ("主体",), span="万历")
e_gongfei2 = E("03-037", "恭妃", "王氏", "person", ("主体",), span="万历")
e_defei = E("03-037", "郑氏", "郑贵妃", "person", ("关联人物",), span="万历")
e_sunrufa = E("03-037", "孙如法", "孙如法", "person", ("关联人物",), span="万历")
e_jiangyinglin = E("03-037", "姜应麟", "姜应麟", "person", ("关联人物",), span="万历")
add("ents", V, [e_xiaogonghou2, e_jinshang10, e_gongfei2, e_defei, e_sunrufa, e_jiangyinglin])

ev1 = EVT(rid("events", V, "EVT"), "03-037", "朝政", "今上",
          "郑氏特加皇贵妃", "今东宫生母初止封恭妃，而德妃郑氏乃特加皇贵妃，且皇第二子年止四岁，孙如法姜应麟辈曹起力谏",
          "万历初", "北京", "迨今上连举圣嗣，今东宫生母初止封恭妃，而德妃郑氏，乃特加皇贵妃，且皇第二子年止四岁，以故孙如法、姜应麟辈曹起力谏，亦惧他日有包藏祸心，妄援孝恭，以希横恩者为虑",
          "重大政治", "恭妃郑氏位号悬绝引谏", "文献转引", "补正史之阙",
          who_ents=[e_jinshang10["ent_id"], e_defei["ent_id"], e_gongfei2["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "03-037", "朝政", "今上",
          "元孙诞生恭妃进封", "直至元孙诞生上大霈中外，恭加慈圣徽号至十二字，而恭妃进封为皇贵妃锡以金册金宝，自此礼仪体貌一视翼坤并列左右",
          "万历中", "北京", "直至元孙诞生，上大霈中外，恭加慈圣徽号至十二字，而恭妃进封为皇贵妃，锡以金册金宝。自此礼仪体貌，一视翼坤，并列左右。天下始快然无遗憾，而圣心至是大白",
          "制度变动", "恭妃进封皇贵妃体貌一视翼坤", "文献转引", "补正史之阙",
          who_ents=[e_gongfei2["ent_id"], e_jinshang10["ent_id"]])
add("events", V, [ev1, ev2])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "03-037", "优先级", ["邻于"],
         "皇贵妃之体", "朝廷",
         "皇贵妃之体邻于正嫡，禁中大庆中宫奉侍仁圣而翼坤奉侍慈圣，得并讲姑媳之体",
         "皇贵妃之体，邻于正嫡，凡禁中大庆，奉请两宫，则中宫奉侍仁圣，而翼坤奉侍慈圣，得并讲姑媳之体，他贵嫔皆退避不敢望见",
         "祖制", "遵行", "万历间", subj_ents=[e_defei["ent_id"]]),
])

add("rels", V, [
    REL(rid("rels", V, "REL"), "03-037", "孙如法", "姜应麟", "同僚", "双向",
        "以故孙如法、姜应麟辈曹起力谏，亦惧他日有包藏祸心，妄援孝恭，以希横恩者为虑",
        "以故孙如法、姜应麟辈曹起力谏，亦惧他日有包藏祸心，妄援孝恭，以希横恩者为虑",
        pa_ents=[e_sunrufa["ent_id"]], pb_ents=[e_jiangyinglin["ent_id"]],
        evo="并谏郑氏特加皇贵妃事", conseq="长幼之序久已定", span="万历初"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "03-037", "郑氏横恩之惧", "怀疑",
        "作者谓其时姑假名号以慰翼坤而长幼之序久已定矣，虽远不知圣主乾断非臣下所能蠡测",
        "虽远不知圣主乾断，非臣下所能蠡测，其时姑假名号，以慰翼坤，而长幼之序，久已定矣",
        "考辨", "客观", "亲闻", targets=[e_jinshang10["ent_id"], e_defei["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "03-037", "恭妃进封之定", "肯定",
        "作者谓天下始快然无遗憾而圣心至是大白，盖主上于定名正分究竟无爽",
        "天下始快然无遗憾，而圣心至是大白。盖主上于定名正分，究竟无爽云",
        "褒扬", "严肃", "亲闻", targets=[e_gongfei2["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "03-037", "万历间", "今上",
         "恭妃进封皇贵妃", "万历间", "北京", "制度",
         "本朝贵妃之加“皇”字也，自孝恭始也",
         "万历", "亲闻", who_ents=[e_jinshang10["ent_id"], e_gongfei2["ent_id"], e_defei["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"]],
         supp="郑氏特加皇贵妃引谏、元孙诞生恭妃进封锡金册金宝"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "03-037", "皇贵妃位号之制", "礼制",
         "皇贵妃之称自孝恭始，万历初郑氏特加、恭妃后进封",
         "本朝贵妃加皇字自孝恭始，孝恭以诞元子进封未几元良正位即代让后居尊，先朝故事非可为训；今上初东宫生母止封恭妃而德妃郑氏特加皇贵妃，孙如法姜应麟力谏；太子册立后恭妃执礼犹谦亦掖廷旧制；元孙诞生恭妃进封皇贵妃锡金册金宝，礼仪体貌一视翼坤",
         "变通", "本朝贵妃之加“皇”字也，自孝恭始也",
         "补正史之阙", figures=[e_xiaogonghou2["ent_id"], e_jinshang10["ent_id"], e_gongfei2["ent_id"], e_defei["ent_id"]]),
])

# ---- 03-041 王妃殉节 ----
e_qingwang = E("03-041", "庆王", "朱伸域", "person", ("关联人物",), span="万历")
e_fangshi = E("03-041", "方氏", "庆王妃方氏", "person", ("主体",), span="万历")
e_bochengen = E("03-041", "哱承恩", "哱承恩", "person", ("关联人物",), span="万历")
e_zhenyuanwang = E("03-041", "镇原王", "朱仲", "person", ("关联人物",), span="万历")
add("ents", V, [e_qingwang, e_fangshi, e_bochengen, e_zhenyuanwang])

ev1 = EVT(rid("events", V, "EVT"), "03-041", "军事", "哱承恩",
          "宁夏兵变胁庆王", "壬辰年宁夏兵变，庆王新立为贼所胁屈节驯服，逆贼哱承恩逼王妃方氏欲行非礼",
          "万历壬辰", "宁夏", "壬辰年，宁夏兵变，庆王新立，为贼所胁，屈节驯服不待言。宪王之正妃方氏者，继册甫一年，即嫠居矣。逆贼哱承恩，逼之欲行非礼，妃乃抱世子匿于土窖，哱贼怒，搜捕苛急，惊悸薨逝",
          "重大政治", "王妃拒污惊悸薨逝", "文献转引", "补正史之阙",
          who_ents=[e_bochengen["ent_id"], e_fangshi["ent_id"], e_qingwang["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "03-041", "朝政", "镇原王",
          "奏妃守节自缢得旌", "管理府事镇原王以其事上闻，上恻然伤之差官慰问，未几又报妃实以本年四月初一日守节自缢，上曰妃贞烈可嘉宜加褒恤以风示天下，命礼部从厚议恤",
          "万历壬辰", "北京", "管理府事镇原王仲<宣隹>以其事上闻，上恻然伤之，差官慰问。未几，又报妃实以本年四月初一日，守节自缢。上曰：妃贞烈可嘉，宜加褒恤，以风示天下，命礼部从厚议恤来言",
          "一般掌故", "节妇得旌并从厚议恤", "文献转引", "补正史之阙",
          who_ents=[e_zhenyuanwang["ent_id"], e_fangshi["ent_id"]])
add("events", V, [ev1, ev2])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "03-041", "义务", ["宜加", "命"],
         "王妃守节自尽", "朝廷",
         "贞烈可嘉宜加褒恤以风示天下，礼部从厚议恤",
         "上曰：妃贞烈可嘉，宜加褒恤，以风示天下，命礼部从厚议恤来言",
         "诏令", "遵行", "万历壬辰", subj_ents=[e_zhenyuanwang["ent_id"]],
         purpose="风示天下"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "03-041", "妃死情状", "怀疑",
        "作者谓妃之义不受污事状必非伪，而死于穴处与死于雉经终莫能明，朝议亦不深核第遵明旨锡殊典",
        "盖妃之义不受污，事状必非伪，而死于穴处，与死于雉经，终莫能明。朝议亦不深核，第遵明旨，锡殊典而已",
        "考辨", "严肃", "传闻", targets=[e_fangshi["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "03-041", "庆府功罪不明", "否定",
        "作者谓其后事平亦更无实录，倘彼中将吏功罪亦贸如此，何以定诛赏耶",
        "其后事平，亦更无实录。倘彼中将吏功罪，亦贸，如此，何以定诛赏耶？",
        "贬斥", "愤慨", "传闻", targets=[e_qingwang["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "03-041", "万历壬辰", "庆王",
         "王妃殉节得旌", "万历间", "宁夏", "人物",
         "壬辰年，宁夏兵变，庆王新立，为贼所胁，屈节驯服不待言",
         "万历", "亲闻", who_ents=[e_fangshi["ent_id"], e_qingwang["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"]],
         supp="方氏拒污惊悸薨、报自缢、锡殊典而情状终莫能明"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "03-041", "节妇褒恤之制", "礼制",
         "万历壬辰庆王妃方氏守节自缢得旌，礼部从厚议恤",
         "壬辰宁夏兵变，王妃方氏抱世子匿土窖惊悸薨逝，复报以四月初一日守节自缢；上恻然伤之，谓贞烈可嘉宜加褒恤以风示天下，命礼部从厚议恤；朝议不深核第遵明旨锡殊典，其后事平更无实录",
         "遵行", "上曰：妃贞烈可嘉，宜加褒恤，以风示天下，命礼部从厚议恤来言",
         "补正史之阙", figures=[e_fangshi["ent_id"], e_zhenyuanwang["ent_id"]]),
])

# ================================================================ 卷 04
V = "04"

# ---- 04-008 使长侍长 ----
e_wenzong2 = E("04-008", "文皇", "朱棣", "person", ("关联人物",), span="永乐")
e_pingan = E("04-008", "平安", "平安", "person", ("关联人物",), span="建文—永乐")
add("ents", V, [e_wenzong2, e_pingan])

ev1 = EVT(rid("events", V, "EVT"), "04-008", "朝政", "文皇",
          "问建文故将相窘状", "文皇登极后问建文故将平安当时相窘状，安对此际欲生致使长耳",
          "永乐初", "北京", "如文皇登极后，问建文故将平安当时相窘状，安对曰：“此际欲生致使长耳。”今亲王不闻有此呼矣",
          "轶闻", "使长之称本于国初", "文献转引", "正史不载",
          who_ents=[e_wenzong2["ent_id"], e_pingan["ent_id"]])
add("events", V, [ev1])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "04-008", "程序", ["呼"],
         "国初臣下呼亲王", "臣下",
         "呼亲王俱为使长",
         "国初沿亡元余习，臣下呼亲王俱为使长，未知取义谓何",
         "惯例", "名存实亡", "国初"),
])

add("cits", V, [
    CIT(rid("cits", V, "CIT"), "04-008", "《荆钗记》", "直引",
        "引戏文怕触突侍长之语证侍长之号相传非一日",
        "今《荆钗记》戏文中，尚有“怕触突侍长”之语，则此号相传亦非一日",
        "佐证", quoted="怕触突侍长"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "04-008", "侍长之号之滥", "否定",
        "作者谓支庶猥贱不膺封号且恣为非礼者亦例受此呼，其辱朱邸极矣",
        "乃至支庶猥贱，不膺封号，且恣为非礼者，亦例受此呼，其辱朱邸极矣",
        "贬斥", "愤慨", "传闻"),
    OPN(rid("opns", V, "OPN"), "04-008", "使长取义", "怀疑",
        "作者谓臣下呼亲王为使长未知取义谓何",
        "国初沿亡元余习，臣下呼亲王俱为使长，未知取义谓何",
        "考辨", "客观", "传闻"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "04-008", "国初", "文皇",
         "亲王为使长侍长之号", "明初", "北京", "风俗",
         "国初沿亡元余习，臣下呼亲王俱为使长，未知取义谓何",
         "洪武", "传闻", who_ents=[e_wenzong2["ent_id"]], ref_evts=[ev1["event_id"]],
         supp="使长亡元余习、侍长为藩府女侍妾之长两号"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "04-008", "宗室称谓之制", "宗室",
         "国初臣下呼亲王为使长，今各藩府女有侍长之号",
         "国初沿亡元余习臣下呼亲王为使长，今亲王不闻有此呼；侍长之号则今各藩府之女俱有此称，云尊其为侍妾之长，乃至支庶猥贱不膺封号者亦例受此呼；荆钗记戏文尚有怕触突侍长之语，则此号相传亦非一日",
         "名存实亡", "又侍长之号，则今各藩府之女，俱有此称，会细叩何义，则云尊其为侍妾之长也",
         "正史不载", figures=[e_wenzong2["ent_id"], e_pingan["ent_id"]]),
])

# ---- 04-010 亲王迎谒 ----
e_luwang = E("04-010", "鲁王肇辉", "朱肇辉", "person", ("关联人物",), span="永乐")
e_daiwang = E("04-010", "代王", "代王", "person", ("关联人物",), span="正德")
e_jinwang = E("04-010", "晋王", "晋王", "person", ("关联人物",), span="正德")
e_shizong13 = E("04-010", "世宗", "嘉靖帝", "person", ("主体",), span="嘉靖")
e_zhaowang = E("04-010", "赵王", "赵王", "person", ("关联人物",), span="嘉靖")
e_tangwang = E("04-010", "唐王", "唐王", "person", ("关联人物",), span="万历")
e_xiangwang = E("04-010", "襄王", "襄王", "person", ("关联人物",), span="万历")
e_jiangling3 = E("04-010", "江陵张公", "张居正", "person", ("主体",), span="万历")
add("ents", V, [e_luwang, e_daiwang, e_jinwang, e_shizong13, e_zhaowang,
                e_tangwang, e_xiangwang, e_jiangling3])

ev1 = EVT(rid("events", V, "EVT"), "04-010", "朝政", "世宗",
          "幸承天府诸王迎谒", "嘉靖十八年世宗幸承天府，先敕谕路近王府封疆者出城候驾跪迎道傍，驾至行殿行五拜三叩头礼，赵王迎于磁州汝王迎于卫辉郑王迎于新郑周世孙迎于郑州徽王迎于钩州唐王迎于南阳府，俱宴赐有加",
          "嘉靖十八年", "承天府", "惟嘉靖十八年，世宗幸承天府，先敕谕路近王府封疆者，出城候驾，跪迎道傍。驾至行殿，行五拜三叩头礼，于是赵王迎于磁州，汝王迎于卫辉，郑王迎于新郑，周世孙迎于郑州，徽王迎于所封钩州（今禹州），唐王迎于所封南阳府，俱宴赐有加，而朝宗王会之盛极矣",
          "一般掌故", "诸王迎驾朝宗王会之盛", "文献转引", "补正史之阙",
          who_ents=[e_shizong13["ent_id"], e_zhaowang["ent_id"], e_tangwang["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "04-010", "朝政", "张居正",
          "过南阳唐王出郊谒", "万历六年故相江陵张公以葬父归过南阳，唐王出郊谒具宾主及答拜留款，张坐南面王相向讲敌礼；至襄阳府襄王亦仿唐例无少异",
          "万历六年", "南阳", "至万历六年，故相江陵张公，以葬父归，过南阳，唐王出郊谒，具宾主，及答拜留款。张坐南面，王相向讲敌礼。至襄阳府，则襄王亦仿唐例无少异",
          "一般掌故", "亲藩以得亲奉謦欬为幸事", "文献转引", "异于正史",
          who_ents=[e_jiangling3["ent_id"], e_tangwang["ent_id"], e_xiangwang["ent_id"]])
add("events", V, [ev1, ev2])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "04-010", "禁止", ["不许"],
         "亲王出城", "亲王",
         "非迎驾及扫墓不许出城一步",
         "故事，亲王非迎驾及扫墓，不许出城一步",
         "祖制", "完全违背", "万历中",
         viol="盖朝见伏谒之礼。一切不讲，而亲藩反以得亲奉謦欬为幸事。僭紊至此，安得不败！"),
])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "04-010", "张居正", "内阁首辅", "万历六年",
         "致仕", "故相江陵张公，以葬父归，过南阳",
         "至万历六年，故相江陵张公，以葬父归，过南阳，唐王出郊谒，具宾主，及答拜留款。张坐南面，王相向讲敌礼",
         person_ents=[e_jiangling3["ent_id"]], contro="有争议",
         ctx="葬父归过南阳受唐王郊谒"),
])

add("rels", V, [
    REL(rid("rels", V, "REL"), "04-010", "张居正", "唐王", "其他", "双向",
        "唐王出郊谒，具宾主，及答拜留款。张坐南面，王相向讲敌礼",
        "至万历六年，故相江陵张公，以葬父归，过南阳，唐王出郊谒，具宾主，及答拜留款。张坐南面，王相向讲敌礼",
        pa_ents=[e_jiangling3["ent_id"]], pb_ents=[e_tangwang["ent_id"]],
        evo="由伏谒之礼改为宾主敌礼", conseq="僭紊至此安得不败",
        span="万历六年"),
    REL(rid("rels", V, "REL"), "04-010", "襄王", "唐王", "同僚", "单向",
        "至襄阳府，则襄王亦仿唐例无少异",
        "至襄阳府，则襄王亦仿唐例无少异",
        pa_ents=[e_xiangwang["ent_id"]], pb_ents=[e_tangwang["ent_id"]],
        evo="仿唐王郊谒之例", strength="旁证", span="万历六年"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "04-010", "亲藩郊谒张居正", "否定",
        "作者谓朝见伏谒之礼一切不讲，亲藩反以得亲奉謦欬为幸事，僭紊至此安得不败",
        "盖朝见伏谒之礼。一切不讲，而亲藩反以得亲奉謦欬为幸事。僭紊至此，安得不败！",
        "贬斥", "愤慨", "亲闻", targets=[e_jiangling3["ent_id"], e_tangwang["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "04-010", "江陵勒二司长跪", "否定",
        "作者谓江陵先期遣牌云本阁部所过二司谒见俱遵见部礼，盖勒其长跪，手板折腰与州县下僚无异，妄自尊大并典制不复问矣",
        "又先期遣牌云：“本阁部所过，二司谒见，俱遵见部礼。”盖勒其长跪也，于是手板折腰，与州县下僚无异。但布按二司，惟入吏部，始行跪礼，至私第，则仍以客礼见。江陵妄自尊大，并典制不复问矣",
        "贬斥", "愤慨", "亲闻", targets=[e_jiangling3["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "04-010", "永乐—万历", "世宗",
         "亲王朝谒之典与僭紊", "永乐以来", "各地", "制度",
         "天子行幸，至藩王境内，例出迎谒",
         "跨朝", "亲闻", who_ents=[e_shizong13["ent_id"], e_jiangling3["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"]],
         supp="永乐鲁王来朝、嘉靖十八年诸王迎驾、万历六年唐王郊谒江陵"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "04-010", "亲王出城迎谒之制", "宗室",
         "祖宗朝亲王非迎驾及扫墓不许出城一步，万历六年唐王郊谒江陵而典制坏",
         "永乐七年鲁王肇辉来朝，武宗巡游最频未闻亲王朝谒；嘉靖十八年世宗幸承天府，敕谕路近王府出城候驾跪迎道傍，行五拜三叩头礼，诸王宴赐有加而朝宗王会之盛极矣；故事亲王非迎驾及扫墓不许出城一步；万历六年江陵葬父归过南阳，唐王出郊谒讲敌礼，襄王仿之，僭紊至极",
         "完全违背", "故事，亲王非迎驾及扫墓，不许出城一步",
         "异于正史", figures=[e_shizong13["ent_id"], e_jiangling3["ent_id"], e_tangwang["ent_id"]]),
])

# ---- 04-020 下殇追封 ----
e_xiaozong3 = E("04-020", "孝宗", "朱祐樘", "person", ("关联人物",), span="弘治")
e_zhanghou = E("04-020", "张后", "张皇后", "person", ("关联人物",), span="弘治")
e_yuedaowang = E("04-020", "蔚悼王", "蔚悼王", "person", ("客体",), span="弘治")
e_yuehuaiwang = E("04-020", "岳怀王厚熙", "朱厚熙", "person", ("客体",), span="嘉靖追崇")
e_xingxianwang = E("04-020", "兴献王", "朱祐杬", "person", ("关联人物",), span="嘉靖追崇")
e_shizong14 = E("04-020", "世宗", "嘉靖帝", "person", ("主体",), span="嘉靖")
e_zhangshengtaihou3 = E("04-020", "章圣太后", "蒋氏", "person", ("关联人物",), span="嘉靖")
e_yingshangwang = E("04-020", "颖殇王", "颖殇王", "person", ("客体",), span="嘉靖")
e_jiaiwang = E("04-020", "蓟哀王", "蓟哀王", "person", ("客体",), span="嘉靖")
e_xianzong3 = E("04-020", "宪宗", "朱见深", "person", ("关联人物",), span="成化")
e_wanguiren = E("04-020", "万贵人", "万贵妃", "person", ("关联人物",), span="成化")
e_wuhou = E("04-020", "吴后", "吴皇后", "person", ("关联人物",), span="成化")
e_aichongtaizi = E("04-020", "哀冲太子", "哀冲太子", "person", ("客体",), span="嘉靖")
e_zhangwenzhong = E("04-020", "张文忠", "张璁", "person", ("关联人物",), span="嘉靖")
add("ents", V, [e_xiaozong3, e_zhanghou, e_yuedaowang, e_yuehuaiwang, e_xingxianwang,
                e_shizong14, e_zhangshengtaihou3, e_yingshangwang, e_jiaiwang,
                e_xianzong3, e_wanguiren, e_wuhou, e_aichongtaizi, e_zhangwenzhong])

ev1 = EVT(rid("events", V, "EVT"), "04-020", "朝政", "世宗",
          "追封岳怀王", "嘉靖四年诏追封岳王谥曰怀，以章圣太后悼忆长子故上追崇，然竟无名可讳至三十九年始追赐今名",
          "嘉靖四年", "北京", "若岳怀王厚熙，为兴献王之长子，世宗同母兄也，生仅五日而薨。嘉靖四年。诏追封岳王，谥曰怀。时章圣太后在养。悼忆长子，故上追崇，以上承慈意，不失为孝。然竟无名可讳，至三十九年，始追赐今名，亦异矣",
          "一般掌故", "追崇同母兄以承慈意", "文献转引", "补正史之阙",
          who_ents=[e_shizong14["ent_id"], e_yuehuaiwang["ent_id"], e_zhangshengtaihou3["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "04-020", "朝政", "世宗",
          "追封颖殇王蓟哀王", "嘉靖十六年颖殇王生仅一日而薨、蓟哀王生仅半月而薨，亦追加王爵赐上谥",
          "嘉靖十六年", "北京", "至嘉靖十六年之颖殇王，则生仅一日而薨；十六年之蓟哀王，则生仅半月而薨，亦追加王爵，赐上谥，何也？",
          "一般掌故", "下殇一日半月亦追王爵", "文献转引", "补正史之阙",
          who_ents=[e_shizong14["ent_id"], e_yingshangwang["ent_id"], e_jiaiwang["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "04-020", "朝政", "世宗",
          "追谥哀冲太子", "世宗长子以嘉靖十二年八月生十月薨为阎妃所出，甫两月耳追名载填册谥为哀冲太子，与宪宗朝迥异",
          "嘉靖十二年", "北京", "至世宗长子，以嘉靖十二年八月生，十月薨，为阎妃所出，甫两月耳，追名载填册，谥为哀冲太子，与宪宗朝迥异矣。时永嘉张文忠第三次为首揆",
          "一般掌故", "两月之婴追谥太子", "文献转引", "补正史之阙",
          who_ents=[e_aichongtaizi["ent_id"], e_shizong14["ent_id"], e_zhangwenzhong["ent_id"]])
add("events", V, [ev1, ev2, ev3])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "04-020", "禁止", ["无追册"],
         "皇子下殇", "朝廷",
         "皇子下殇无追册",
         "本朝皇子下殇，无追册者",
         "祖制", "变通", "明兴以来",
         viol="嘉靖中岳怀王、颖殇王、蓟哀王、哀冲太子相继追封追谥"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "04-020", "下殇追封之滥", "否定",
        "作者谓蔚悼王破例追封然年亦三岁，颖殇王生仅一日蓟哀王生仅半月亦追加王爵赐上谥，何也；岳怀王至三十九年始追赐今名亦异矣",
        "至嘉靖十六年之颖殇王，则生仅一日而薨；十六年之蓟哀王，则生仅半月而薨，亦追加王爵，赐上谥，何也？",
        "考辨", "严肃", "传闻", targets=[e_shizong14["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "04-020", "成化元子不加封", "肯定",
        "作者谓万宠冠后宫时所生元子且已及期月竟不加封亦不赐名，时李文达当国盖以下殇未足当储位之重，其见卓矣",
        "时万宠冠后宫，吴后亦因之而废，所生乃元子，且已及期月，竟不加封，亦不赐名。时李文达当国，盖以下殇未足当储位之重，其见卓矣",
        "褒扬", "严肃", "传闻", targets=[e_xianzong3["ent_id"], e_wanguiren["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "04-020", "成化—嘉靖", "世宗",
         "皇子下殇追封之例", "成化以来", "北京", "制度",
         "本朝皇子下殇，无追册者",
         "跨朝", "传闻", who_ents=[e_shizong14["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"]],
         supp="蔚悼王、岳怀王、颖殇王、蓟哀王、哀冲太子追封与成化元子不加封之比"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "04-020", "皇子追封之制", "宗室",
         "本朝皇子下殇无追册，嘉靖间破例屡追",
         "蔚悼王为孝宗张后嫡出破例追封然年亦三岁；岳怀王厚熙为兴献王长子世宗同母兄，生仅五日而薨，嘉靖四年追封岳王谥怀，至三十九年始追赐今名；嘉靖十六年颖殇王生一日、蓟哀王生半月亦追加王爵；世宗长子甫两月追谥哀冲太子；惟成化元子已及期月竟不加封不赐名",
         "变通", "本朝皇子下殇，无追册者。唯蔚悼王，为孝宗张后嫡出，破例追封，然年亦三岁矣",
         "补正史之阙", figures=[e_shizong14["ent_id"], e_xiaozong3["ent_id"]]),
])

# ---- 04-021 庆府前后遭变 ----
e_qingwang2 = E("04-021", "庆王", "朱栴", "person", ("关联人物",), span="洪武")
e_wangtaihong = E("04-021", "王台浤", "朱台浤", "person", ("主体",), span="正德—嘉靖")
e_zhiduan = E("04-021", "寘鐇", "朱寘鐇", "person", ("关联人物",), span="正德")
e_zhangyong = E("04-021", "张永", "张永", "person", ("关联人物",), faction="宦官", span="正德")
e_yangyiqing = E("04-021", "杨一清", "杨一清", "person", ("关联人物",), span="正德—嘉靖")
e_wangshenyu = E("04-021", "今王伸域", "朱伸域", "person", ("关联人物",), span="万历")
add("ents", V, [e_qingwang2, e_wangtaihong, e_zhiduan, e_zhangyong, e_yangyiqing, e_wangshenyu])

ev1 = EVT(rid("events", V, "EVT"), "04-021", "军事", "寘鐇",
          "安化王之乱台浤守国", "正德五年安化王寘鐇之乱，庆王台浤守国在劳，特赐敕慰谕且以黄金三百白金五千赍之",
          "正德五年", "宁夏", "传至王台浤，先以正德五年安化王寘鐇之乱，守国在劳，特赐敕慰谕，且以黄金三百、白金五千赍之",
          "一般掌故", "守国有赏", "文献转引", "补正史之阙",
          who_ents=[e_zhiduan["ent_id"], e_wangtaihong["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "04-021", "朝政", "张永",
          "参台浤谄谀追还赐物", "督兵太监张永都御史杨一清参其谄谀寘鐇称臣卑辱，奉旨追还赐敕及所赐物",
          "正德中", "宁夏", "未几，督兵太监张永、都御史杨一清，参其谄谀寘鐇，称臣卑辱，奉旨追还赐敕及所赐物",
          "一般掌故", "先赏后罚", "文献转引", "补正史之阙",
          who_ents=[e_zhangyong["ent_id"], e_yangyiqing["ent_id"], e_wangtaihong["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "04-021", "朝政", "王台浤",
          "坐不法降庶人禁锢", "嘉靖四年又坐不法降庶人，以兵围守之，止给禄三百石又徙西安府禁锢",
          "嘉靖四年", "宁夏", "至嘉靖四年，又坐不法，降庶人，以兵围守之。止给禄三百石，又徙西安府禁锢",
          "制度变动", "由亲王降庶人徙西安", "文献转引", "补正史之阙",
          who_ents=[e_wangtaihong["ent_id"]])
ev4 = EVT(rid("events", V, "EVT"), "04-021", "军事", "今王伸域",
          "遭刘哱之变为所劫质", "万历十九年袭位，二十一年遭刘哱之变为所劫质，亦谄附乱卒以求苟免，奉严旨切责",
          "万历二十一年", "宁夏", "台浤四传而为今王伸域，以万历十九年袭位，二十一年遭刘哱之变，为所劫质，亦谄附乱卒，以求苟免。奉严旨切责，后事平，自言困辱之状",
          "重大政治", "后王先贬后褒", "文献转引", "补正史之阙",
          who_ents=[e_wangshenyu["ent_id"]])
add("events", V, [ev1, ev2, ev3, ev4])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "04-021", "处罚", ["降", "止给"],
         "亲王坐不法", "朝廷",
         "降庶人以兵围守，止给禄三百石，徙西安府禁锢",
         "至嘉靖四年，又坐不法，降庶人，以兵围守之。止给禄三百石，又徙西安府禁锢",
         "诏令", "遵行", "嘉靖四年", subj_ents=[e_wangtaihong["ent_id"]]),
])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "04-021", "张永", "督兵太监", "正德中",
         "现任", "督兵太监张永、都御史杨一清，参其谄谀寘鐇",
         "未几，督兵太监张永、都御史杨一清，参其谄谀寘鐇，称臣卑辱，奉旨追还赐敕及所赐物",
         person_ents=[e_zhangyong["ent_id"]], faction_impl="宦官", inst="军前",
         ctx="参庆王谄谀安化王"),
    APPT(rid("appts", V, "APPT"), "04-021", "杨一清", "都御史", "正德中",
         "现任", "督兵太监张永、都御史杨一清，参其谄谀寘鐇",
         "未几，督兵太监张永、都御史杨一清，参其谄谀寘鐇，称臣卑辱，奉旨追还赐敕及所赐物",
         person_ents=[e_yangyiqing["ent_id"]], inst="军前",
         ctx="与张永同参庆王"),
])

add("rels", V, [
    REL(rid("rels", V, "REL"), "04-021", "张永", "杨一清", "同僚", "双向",
        "督兵太监张永、都御史杨一清，参其谄谀寘鐇，称臣卑辱",
        "未几，督兵太监张永、都御史杨一清，参其谄谀寘鐇，称臣卑辱，奉旨追还赐敕及所赐物",
        pa_ents=[e_zhangyong["ent_id"]], pb_ents=[e_yangyiqing["ent_id"]],
        evo="同参庆王谄谀", conseq="追还赐敕赐物", span="正德中"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "04-021", "庆府两番屈节", "否定",
        "作者谓前王先赏后罚后王先贬后褒，总之变起意外屈节两番，建国虽二百年尽丧亲藩之体，可恨亦可羞矣",
        "盖前王先赏后罚，后王先贬后褒，虽所被国典不同，总之变起意外，屈节两番，抑扬互见，言之均堪泚颊。建国虽二百年，尽丧亲藩之体，可恨亦可羞矣！",
        "贬斥", "愤慨", "亲闻", targets=[e_wangtaihong["ent_id"], e_wangshenyu["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "04-021", "正德—万历", "庆王",
         "庆府前后遭变", "正德以来", "宁夏", "朝政",
         "庆王为太祖第十六子，初之国韦州，徙宁夏，在今镇城中",
         "跨朝", "亲闻", who_ents=[e_qingwang2["ent_id"], e_wangtaihong["ent_id"], e_wangshenyu["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"], ev4["event_id"]],
         supp="台浤正德守国之赏与谄谀之罚、嘉靖降庶人、伸域刘哱之变"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "04-021", "亲王约束之典", "宗室",
         "正德五年台浤守国之赏，旋以谄谀追还，嘉靖四年降庶人禁锢",
         "庆王为太祖第十六子，初国韦州徙宁夏；台浤以正德五年安化王之乱守国在劳，赐敕慰谕并黄金三百白金五千；张永杨一清参其谄谀寘鐇称臣卑辱，追还赐敕赐物；嘉靖四年又坐不法降庶人，兵围守止给禄三百石徙西安禁锢；四传为伸域，万历二十一年遭刘哱之变为所劫质亦谄附乱卒，后事平自言困辱，庆献王妃方氏抗节不受污以死得旌",
         "变通", "至嘉靖四年，又坐不法，降庶人，以兵围守之。止给禄三百石，又徙西安府禁锢",
         "补正史之阙", figures=[e_wangtaihong["ent_id"], e_wangshenyu["ent_id"]]),
])

# ---- 04-031 辽王贵牴罪恶 ----
e_liaowang = E("04-031", "辽王宪节", "朱宪节", "person", ("主体",), span="隆庆")
e_guiheng = E("04-031", "贵烚", "朱贵烚", "person", ("主体",), span="正统")
e_liaojianwang = E("04-031", "辽简王植", "朱植", "person", ("关联人物",), span="永乐—正统")
e_jiangling4 = E("04-031", "张江陵", "张居正", "person", ("关联人物",), span="隆庆—万历")
e_caoguang = E("04-031", "曹广", "曹广", "person", ("关联人物",), span="正统")
e_dushu = E("04-031", "杜述", "杜述", "person", ("关联人物",), span="正统")
e_liuyongze = E("04-031", "刘永泽", "刘永泽", "person", ("关联人物",), span="正统")
e_hongchaoxuan = E("04-031", "洪朝选", "洪朝选", "person", ("关联人物",), span="隆庆")
e_yingzong3 = E("04-031", "英宗", "朱祁镇", "person", ("关联人物",), span="正统")
add("ents", V, [e_liaowang, e_guiheng, e_liaojianwang, e_jiangling4, e_caoguang,
                e_dushu, e_liuyongze, e_hongchaoxuan, e_yingzong3])

ev1 = EVT(rid("events", V, "EVT"), "04-031", "司法", "贵烚",
          "正统四年罪恶尽发", "通川王贵烚嗣辽王在位十五年屡为抚按科道所弹治，英宗每降书戒之不悛，正统四年事尽发，奸通千户曹广等妻女数十人，杖死长史杜述擅笞荆州知府刘永泽",
          "正统四年", "荆州", "至正统四年，事尽发。初与江陵、沪溪二郡王淫乱，又奸通千户曹广等妻女数十人。非理奸死者十余人；又杖死长史杜述，擅笞荆州知府刘永泽；假以进贡为名，夺彝陵、江陵等州县军民柑橘，起人夫逼死者三十人",
          "重大政治", "辽王恶迹尽发", "文献转引", "补正史之阙",
          who_ents=[e_guiheng["ent_id"], e_caoguang["ent_id"], e_dushu["ent_id"], e_liuyongze["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "04-031", "朝政", "英宗",
          "革爵为庶人伴守坟茔", "上召王至京亲鞫之且示以诸弹章，王输服无辞，乃命遣归革爵为庶人伴守坟茔，仍支岁俸一千石，以庶弟兴山王贵燰嗣封",
          "正统四年", "北京", "上召王至京亲鞫之，且示以诸弹章，王输服无辞。乃命遣归，革爵为庶人，伴守坟茔，仍支岁俸一千石，以其庶弟兴山王贵燰嗣封。盖贵烚之当失国有余辜矣",
          "制度变动", "革爵庶人以弟嗣封", "文献转引", "补正史之阙",
          who_ents=[e_yingzong3["ent_id"], e_guiheng["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "04-031", "朝政", "辽王宪节",
          "隆庆初辽王之废", "辽王宪节之废也在隆庆初年，人至今有称冤者盖归罪张江陵有意殄之",
          "隆庆初", "北京", "辽王宪节之废也，事在隆庆初年，人至今有称冤者，盖归罪张江陵有意殄之也，不知辽之恶当废久矣",
          "重大政治", "辽王终覆其祀", "文献转引", "异于正史",
          who_ents=[e_liaowang["ent_id"], e_jiangling4["ent_id"]])
add("events", V, [ev1, ev2, ev3])

add("rels", V, [
    REL(rid("rels", V, "REL"), "04-031", "张居正", "辽王宪节", "恩怨", "单向",
        "人至今有称冤者，盖归罪张江陵有意殄之也",
        "辽王宪节之废也，事在隆庆初年，人至今有称冤者，盖归罪张江陵有意殄之也，不知辽之恶当废久矣",
        pa_ents=[e_jiangling4["ent_id"]], pb_ents=[e_liaowang["ent_id"]],
        evo="谈者谓辽废出于江陵有意殄之", conseq="人至今有称冤者",
        strength="推断", span="隆庆初"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "04-031", "辽王之废是否归罪江陵", "否定",
        "作者谓辽王宪节之废人至今有称冤者盖归罪张江陵有意殄之，不知辽之恶当废久矣，贵烚之当失国有余辜",
        "辽王宪节之废也，事在隆庆初年，人至今有称冤者，盖归罪张江陵有意殄之也，不知辽之恶当废久矣",
        "考辨", "严肃", "传闻", targets=[e_liaowang["ent_id"], e_jiangling4["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "04-031", "积不善遗殃", "讽刺",
        "作者谓二世为王恩以私怨一日杀宗室镇国将军恩鑡等八十人，不数日而长子死未几王亦疽发背薨，又一世而宪节终覆其祀，积不善遗殃如此",
        "积不善遗殃如此",
        "感慨", "严肃", "传闻", targets=[e_liaowang["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "04-031", "洪朝选存辽得罪之说", "否定",
        "作者谓按隆庆二年刑部侍郎洪朝选所上宪节罪状甚详皆罪在赦前，谈者反谓洪不阿江陵欲存辽得罪，真说梦耳",
        "按隆庆二年，刑部侍郎洪朝选，所上宪节罪状甚详，皆罪在赦前。谈者反谓洪不阿江陵，欲存辽得罪，真说梦耳！",
        "贬斥", "愤慨", "传闻", targets=[e_hongchaoxuan["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "04-031", "正统—隆庆", "辽王宪节",
         "辽王贵烚罪恶与辽府之废", "正统以来", "荆州", "朝政",
         "辽王宪节之废也，事在隆庆初年，人至今有称冤者，盖归罪张江陵有意殄之也",
         "跨朝", "传闻", who_ents=[e_liaowang["ent_id"], e_guiheng["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"]],
         supp="贵烚正统四年恶迹、革爵庶人、二世杀宗室、宪节隆庆初废"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "04-031", "亲王废黜之典", "宗室",
         "正统四年贵烚革爵为庶人伴守坟茔，隆庆初辽王宪节废",
         "辽简王植为太祖第十五子，庶弟二子通川王贵烚嗣辽王在位十五年屡为抚按科道弹治，英宗降书戒之不悛；正统四年事尽发，奸通曹广等妻女数十人、杖死长史杜述、擅笞荆州知府刘永泽、夺州县军民柑橘逼死人夫三十；上亲鞫之，革爵为庶人伴守坟茔仍支岁俸一千石，以庶弟兴山王贵燰嗣封；二世王恩一日杀宗室八十人，不数日长子死未几王亦疽发背薨；又一世而宪节终覆其祀",
         "遵行", "上召王至京亲鞫之，且示以诸弹章，王输服无辞。乃命遣归，革爵为庶人，伴守坟茔，仍支岁俸一千石",
         "补正史之阙", figures=[e_guiheng["ent_id"], e_yingzong3["ent_id"], e_liaowang["ent_id"]]),
])

# ---- 04-034 楚府前后遭变 ----
e_chuwang = E("04-034", "楚王", "楚愍王", "person", ("关联人物",), span="嘉靖")
e_yingyao = E("04-034", "英耀", "世子英耀", "person", ("主体",), span="嘉靖")
e_yingqian = E("04-034", "英佥", "楚恭王", "person", ("关联人物",), span="嘉靖")
e_wugangwang = E("04-034", "武冈王显槐", "朱显槐", "person", ("关联人物",), span="嘉靖")
e_jinwang2 = E("04-034", "今王", "今楚王", "person", ("关联人物",), span="万历")
e_huayue = E("04-034", "华越", "华越", "person", ("关联人物",), span="万历")
e_guojiangxia = E("04-034", "郭江夏", "郭江夏", "person", ("关联人物",), span="万历")
add("ents", V, [e_chuwang, e_yingyao, e_yingqian, e_wugangwang, e_jinwang2, e_huayue, e_guojiangxia])

ev1 = EVT(rid("events", V, "EVT"), "04-034", "司法", "英耀",
          "弑父伏法以弟嗣", "楚王为太祖第六子，传至愍王见弑于世子英耀，耀伏法，以庶子英佥嗣位是为恭王",
          "嘉靖中", "武昌", "楚王为太祖第六子，传至愍王，见弑于世子英耀。耀伏法，以庶子英佥嗣位，是为恭王，在位久无所出",
          "重大政治", "世子弑父伏法弟嗣", "文献转引", "补正史之阙",
          who_ents=[e_yingyao["ent_id"], e_yingqian["ent_id"], e_chuwang["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "04-034", "朝政", "武冈王显槐",
          "显槐监国尽取珍异", "英佥薨子尚幼，以武冈王显槐监国，武冈习知其所名子状，尽取先世所藏珍异宝货以去，国人畏发往事不敢诘",
          "嘉靖中", "武昌", "英佥薨，子尚幼，以武冈王显槐监国。武冈习知其所名子状，尽取先世所藏珍异宝货以去，国人畏发往事，不敢诘",
          "一般掌故", "监国者借往事挟取宝货", "文献转引", "正史不载",
          who_ents=[e_wugangwang["ent_id"], e_yingqian["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "04-034", "朝政", "今王",
          "华越等讦奏朝议不决", "今王嗣爵已三十年，宗人不复奉其约束，王尚以法绳之，致有华越等讦奏，朝议不能决；郭江夏署礼部素不平其事力主发勘因而去位",
          "万历中", "北京", "今王嗣爵已三十年，宗人不复奉其约束，王尚以法绳之，致有华越等讦奏，朝议不能决。郭江夏署礼部，素不平其事，力主发勘，因而去位，祸延缙绅，至今未已也",
          "一般掌故", "宗室讦奏延及缙绅", "文献转引", "补正史之阙",
          who_ents=[e_jinwang2["ent_id"], e_huayue["ent_id"], e_guojiangxia["ent_id"]])
add("events", V, [ev1, ev2, ev3])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "04-034", "程序", ["止存"],
         "世子为大逆", "朝廷",
         "只宜污潴其宫，止存郡王，听邻藩节制如故事",
         "英耀躬为大逆，恶逾商伤臣，只宜污潴其宫，止存郡王，听邻藩节制如故事",
         "祖制", "名存实亡", "嘉靖中",
         viol="何以茅土俨然，致恭王有李道儿之疑"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "04-034", "英佥嗣位之疑", "讽刺",
        "作者谓说者哗言不男，如晋海西公晚年为后计者甚密，武冈习知其所名子状尽取先世珍异宝货以去，国人畏发往事不敢诘",
        "说者哗言不男，如晋海西公晚年为后计者甚密。曾屡示意所厚藩僚，俱惧祸不敢承，乃谋于嬖幸，因有孪生二子事。英佥薨，子尚幼，以武冈王显槐监国。武冈习知其所名子状，尽取先世所藏珍异宝货以去，国人畏发往事，不敢诘",
        "讽刺", "嘲讽", "传闻", targets=[e_yingqian["ent_id"], e_wugangwang["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "04-034", "三国削爵与英耀之比", "否定",
        "作者谓英耀以嘉靖二十四年弑逆，三十五年微王载埨以夺田宅子女、四十二年伊王典楧以淫虐不法、辽王宪节以酗横杀人俱削爵除国，此三国不过纵汰失道尚至废锢，英耀躬为大逆恶逾商伤臣只宜污潴其宫止存郡王",
        "按英耀以嘉靖二十四年弑逆，三十五年微王载埨以夺田宅子女，四十二年伊王典楧以淫虐不法，未几辽王宪节以酗横杀人，俱削爵除国，身锢高墙，子孙俱为庶人。此三国，不过纵汰失道，尚至废锢。英耀躬为大逆，恶逾商伤臣，只宜污潴其宫，止存郡王，听邻藩节制如故事",
        "贬斥", "愤慨", "传闻", targets=[e_yingyao["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "04-034", "当国者之见", "否定",
        "作者谓愍王二子一剚刃所生一自斩其祀皆覆载所不受，时当国者为夏严二公其见终出新郑江陵之下令人邑邑",
        "然则愍王二子，一剚刃所生，一自斩其祀，皆覆载所不受也。时当国者为夏、严二公，其见终出新郑、江陵之下，令人邑邑",
        "感慨", "严肃", "传闻"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "04-034", "嘉靖—万历", "楚王",
         "楚府前后遭变", "嘉靖以来", "武昌", "朝政",
         "楚王为太祖第六子，传至愍王，见弑于世子英耀",
         "跨朝", "传闻", who_ents=[e_chuwang["ent_id"], e_yingyao["ent_id"], e_yingqian["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"]],
         supp="英耀弑逆伏法、英佥嗣位之疑、显槐监国、华越讦奏"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "04-034", "亲王承袭监国之制", "宗室",
         "嘉靖中英佥以庶子嗣恭王，子尚幼以武冈王显槐监国",
         "楚王为太祖第六子，传至愍王见弑于世子英耀，耀伏法以庶子英佥嗣位是为恭王，在位久无所出，说者哗言不男而谋于嬖幸有孪生二子事；英佥薨子尚幼，武冈王显槐监国，尽取先世珍异宝货以去；今王嗣爵三十年宗人不复奉约束，华越等讦奏朝议不能决，郭江夏力主发勘去位祸延缙绅；英耀大逆而茅土俨然，恭王有李道儿之疑",
         "变通", "英佥薨，子尚幼，以武冈王显槐监国。武冈习知其所名子状，尽取先世所藏珍异宝货以去，国人畏发往事，不敢诘",
         "异于正史", figures=[e_yingyao["ent_id"], e_yingqian["ent_id"], e_wugangwang["ent_id"]]),
])

# ---- 04-038 废齐之横 ----
e_qiwang = E("04-038", "齐王", "朱榑", "person", ("主体",), span="洪武—建文")
e_jianwendi = E("04-038", "建文", "朱允炆", "person", ("关联人物",), span="建文")
add("ents", V, [e_qiwang, e_jianwendi])

ev1 = EVT(rid("events", V, "EVT"), "04-038", "朝政", "齐王",
          "除国锢南京子孙为庶人", "齐王为太祖第七子，建文中坐废，靖难后复封，后复以谋叛除国锢南京，其子孙皆庶人有庶粮无名封",
          "建文—永乐", "南京", "齐王为太祖第七子，建文中坐废，靖难后复封。后复以谋叛除国，锢南京，其子孙皆庶人，有庶粮，无名封",
          "一般掌故", "齐府除国子孙庶人", "文献转引", "补正史之阙",
          who_ents=[e_qiwang["ent_id"], e_jianwendi["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "04-038", "社会", "齐府庶人",
          "支属横行留都", "今支属渐繁横行留都，廊下诸铺院中诸妓动辄出票取物不还值荐枕不损橐，以至僧寺亦罹其害",
          "万历中", "南京", "今支属渐繁，横行留都，廊下诸铺，院中诸妓，动辄出票。取物不还值，荐枕不损橐，以至僧寺亦罹其害",
          "一般掌故", "庶人支属肆虐留都", "文献转引", "正史不载")
add("events", V, [ev1, ev2])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "04-038", "废齐之横", "否定",
        "作者谓负贩不得志即设一几北面拜自称谢恩，次日击金带服象龙拜客，都下百寮习见以为故常不复致诘，亦随例与往还，正不可解",
        "尤可笑者，负贩不得志，即设一几北面拜，自称谢恩，次日击金带服象龙拜客，家中受人谒贺。正不知此章服从何来？都下百寮习见，以为故常，不复致诘，亦随例与往还。正不可解",
        "讽刺", "嘲讽", "亲闻"),
    OPN(rid("opns", V, "OPN"), "04-038", "自爱者不多得", "否定",
        "作者谓间有自爱者不多得也",
        "间有自爱者，不多得也",
        "感慨", "惋惜", "亲闻"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "04-038", "建文—万历", "齐王",
         "齐府庶人横于留都", "建文以来", "南京", "社会",
         "齐王为太祖第七子，建文中坐废，靖难后复封。后复以谋叛除国，锢南京，其子孙皆庶人，有庶粮，无名封",
         "跨朝", "亲闻", who_ents=[e_qiwang["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"]],
         supp="齐府除国后庶人支属出票取物、伪谢恩拜客诸横状"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "04-038", "宗室禁锢之制", "宗室",
         "齐王以谋叛除国锢南京，子孙皆庶人有庶粮无名封",
         "齐王为太祖第七子，建文中坐废，靖难后复封，后复以谋叛除国锢南京，子孙皆庶人有庶粮无名封；今支属渐繁横行留都，廊下诸铺院中诸妓动辄出票取物不还值荐枕不损橐，以至僧寺亦罹其害；负贩不得志即设一几北面拜自称谢恩，次日击金带服象龙拜客；都下百寮习见以为故常不复致诘",
         "名存实亡", "齐王为太祖第七子，建文中坐废，靖难后复封。后复以谋叛除国，锢南京，其子孙皆庶人，有庶粮，无名封",
         "正史不载", figures=[e_qiwang["ent_id"]]),
])

# ================================================================ 卷 05
V = "05"

# ---- 05-004 仪宾牙牌 ----
e_jingdi2 = E("05-004", "景皇帝", "朱祁钰", "person", ("关联人物",), span="景泰")
e_guanjun = E("05-004", "固安郡主", "固安郡主", "person", ("主体",), span="成化—弘治")
e_wangxian = E("05-004", "王宪", "王宪", "person", ("主体",), span="成化—弘治")
e_jiaxiang = E("05-004", "嘉祥长公主", "嘉祥长公主", "person", ("关联人物",), span="成化")
e_wangshi = E("05-004", "汪氏", "郕王妃汪氏", "person", ("关联人物",), span="成化—弘治")
e_yiwentaizi = E("05-004", "懿文太子", "朱标", "person", ("关联人物",), span="洪武")
add("ents", V, [e_jingdi2, e_guanjun, e_wangxian, e_jiaxiang, e_wangshi, e_yiwentaizi])

ev1 = EVT(rid("events", V, "EVT"), "05-004", "制度变动", "王宪",
          "郕府仪宾特给牙牌", "景皇帝女固安郡主以成化六年下嫁王宪，礼部特请宪系郕府仪宾乞给牙牌，上从之，命班行列都督佥事之下",
          "成化六年", "北京", "惟景皇帝女固安郡主，以成化六年下嫁王宪，礼部特请，宪系郕府仪宾，乞给牙牌。上从之，命班行列都督佥事之下，盖以从三品，居正二品之次也",
          "制度变动", "仪宾给牙牌为创见", "文献转引", "补正史之阙",
          who_ents=[e_guanjun["ent_id"], e_wangxian["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "05-004", "朝政", "今上",
          "固安公主卒丧礼一视嘉祥", "弘治四年固安公主卒，上命丧礼一视嘉祥长公主，时固安母汪氏尚称郕王妃，其女乃得异礼如此，上恩厚矣",
          "弘治四年", "北京", "弘治四年，固安公主卒，上命丧礼一视嘉祥长公主，嘉祥为宪宗亲女，时固安母汪氏，尚称郕王妃，其女乃得异礼如此，上恩厚矣",
          "一般掌故", "郡主丧礼比亲女", "文献转引", "补正史之阙",
          who_ents=[e_guanjun["ent_id"], e_wangshi["ent_id"]])
add("events", V, [ev1, ev2])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "05-004", "禁止", ["无得"],
         "外藩仪宾", "仪宾",
         "虽云尚主，无得系牙牌如京官例",
         "虽云尚主，无得击牙牌如京官例。惟景皇帝女固安郡主，以成化六年下嫁王宪，礼部特请，宪系郕府仪宾，乞给牙牌",
         "祖制", "变通", "洪武末以来",
         viol="礼部特请给牙牌，上从之，命班行列都督佥事之下"),
])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "05-004", "王宪", "郕府仪宾", "成化六年",
         "现任", "宪系郕府仪宾，乞给牙牌。上从之，命班行列都督佥事之下",
         "惟景皇帝女固安郡主，以成化六年下嫁王宪，礼部特请，宪系郕府仪宾，乞给牙牌。上从之，命班行列都督佥事之下",
         person_ents=[e_wangxian["ent_id"]], inst="郕府", contro="有争议",
         ctx="以从三品居正二品之次，创见给牙牌"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "05-004", "仪宾给牙牌", "肯定",
        "作者谓此后遣祀分祭宪亦供事如诸戚臣，实为创见",
        "此后遣祀分祭，宪亦供事，如诸戚臣，实为创见",
        "考辨", "客观", "传闻", targets=[e_wangxian["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "05-004", "江都公主之憾", "否定",
        "作者谓懿文太子三女长为江都公主下嫁驸马耿璿，文皇降为郡主仪宾皆以罪死，第三女年三岁以建文庚辰所生未有名封，直至成化二十一年八月始卒于高墙年已八十六岁，当时臣下无能推广圣泽使其终无匹偶以殁，其恩遇曾不及固安之百一，真足令人沥泣",
        "当时臣下无能推广圣泽，使其终无匹偶以殁，其恩遇曾不及固安之百一，真足令人沥泣",
        "感慨", "惋惜", "传闻", targets=[e_yiwentaizi["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "05-004", "成化—弘治", "景皇帝",
         "仪宾牙牌与固安公主丧礼", "成化以来", "北京", "制度",
         "各王府亲王位下仪宾，亚驸马一等，秩从二品",
         "跨朝", "传闻", who_ents=[e_guanjun["ent_id"], e_wangxian["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"]],
         supp="仪宾无牙牌之制与固安郡主特例、丧礼比嘉祥长公主"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "05-004", "仪宾待遇之制", "宗室",
         "洪武末皇孙女仪宾在都下者后分封选拜例居外藩，无得系牙牌如京官例",
         "各王府亲王位下仪宾亚驸马一等秩从二品；洪武末皇孙女仪宾在都下者其后分封选拜例居外藩，虽云尚主无得系牙牌如京官例；成化六年固安郡主下嫁王宪，礼部特请给牙牌，班行列都督佥事之下，创见；弘治四年公主卒丧礼一视嘉祥长公主；仪宾二品者阶为中奉大夫本文职而夷之右列督佥之下；嘉靖间仪宾周钺等用王宪例",
         "变通", "惟洪武末年，皇孙女仪宾在都下者，其后分封选拜，例居外藩。虽云尚主，无得击牙牌如京官例",
         "补正史之阙", figures=[e_jingdi2["ent_id"], e_wangxian["ent_id"]]),
])

# ---- 05-010 公主荫叙之滥 ----
e_guoxun2 = E("05-010", "郭勋", "郭勋", "person", ("关联人物",), span="嘉靖")
e_guoqiang = E("05-010", "郭勍", "郭勍", "person", ("主体",), span="嘉靖")
e_guozhen = E("05-010", "郭镇", "郭镇", "person", ("引用人物",), span="明初")
e_xiayan3 = E("05-010", "夏言", "夏言", "person", ("关联人物",), span="嘉靖")
e_xiemaogong = E("05-010", "谢懋功", "谢懋功", "person", ("关联人物",), span="万历")
e_yangtianzuo = E("05-010", "杨天佐", "杨天佐", "person", ("关联人物",), span="万历")
e_shensiming = E("05-010", "沈四明", "沈一贯", "person", ("关联人物",), span="万历")
e_fengzhuoan = E("05-010", "冯琢庵", "冯琦", "person", ("关联人物",), span="万历")
add("ents", V, [e_guoxun2, e_guoqiang, e_guozhen, e_xiayan3, e_xiemaogong,
                e_yangtianzuo, e_shensiming, e_fengzhuoan])

ev1 = EVT(rid("events", V, "EVT"), "05-010", "朝政", "郭勍",
          "援公主例请荫被夏言执罢", "嘉靖十二年武定侯郭勋族弟郭勍其高祖为驸马郭镇，援往年汝阳等公主例以请，上已允之，时礼卿夏言执称事例所无乃汝阳创始非故事宜禁，上然其言遂罢勍荫且永著为令",
          "嘉靖十二年", "北京", "嘉靖十二年，武定侯郭勋之族弟郭勍者，其高祖为驸马郭镇，援往年汝阳等公主例以请，上已允之。时，礼卿为夏言，执称事例所无，乃汝阳创始，非故事，宜禁。上然其言，遂罢勍荫，且永著为令",
          "制度变动", "公主文荫永著为令禁止", "文献转引", "补正史之阙",
          who_ents=[e_guoqiang["ent_id"], e_xiayan3["ent_id"], e_guozhen["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "05-010", "朝政", "今上",
          "册立恩诏许公主荫子", "万历壬寅三月以册立皇太子恩诏内许公主荫子送监读书，首被恩命者四人谢懋功杨天佐周居经郭梦兆",
          "万历壬寅三月", "北京", "今万历壬寅三月，以册立皇太子恩诏内，许公主荫子，送监读书。时首被恩命者四人：曰谢懋功，则与献帝第四女，永淳大长公主之孙；曰杨天佐，则英宗第四女，崇德大长公主之曾孙；曰周居经，则英宗长女，重庆大长公主之元孙，固已年远服绝矣。至郭梦兆者，为武定侯郭英苗裔，而太祖第十二女，永嘉贞懿大长公主之七世孙也",
          "制度变动", "公主荫子之禁大开", "文献转引", "异于正史",
          who_ents=[e_xiemaogong["ent_id"], e_yangtianzuo["ent_id"]])
add("events", V, [ev1, ev2])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "05-010", "禁止", ["无文荫"],
         "公主荫叙", "朝廷",
         "祖宗典制公主无文荫，自后间以陈乞得之然非例也",
         "祖宗典制，公主无文荫。自后间以陈乞得之，然非例也",
         "祖制", "完全违背", "嘉靖十二年以前",
         viol="今万历壬寅三月，以册立皇太子恩诏内，许公主荫子，送监读书"),
])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "05-010", "夏言", "礼部尚书", "嘉靖十二年",
         "现任", "时，礼卿为夏言，执称事例所无，乃汝阳创始，非故事，宜禁",
         "嘉靖十二年，武定侯郭勋之族弟郭勍者，其高祖为驸马郭镇，援往年汝阳等公主例以请，上已允之。时，礼卿为夏言，执称事例所无，乃汝阳创始，非故事，宜禁",
         person_ents=[e_xiayan3["ent_id"]], contro="有争议",
         ctx="执罢郭勍公主荫"),
    APPT(rid("appts", V, "APPT"), "05-010", "沈四明", "内阁首辅", "万历壬寅",
         "现任", "时，沈四明独当国，冯琢庵为礼卿，岂其识不逮贵溪耶？",
         "时，沈四明独当国，冯琢庵为礼卿，岂其识不逮贵溪耶？",
         person_ents=[e_shensiming["ent_id"]], contro="有争议",
         ctx="公主荫子恩诏之时独当国"),
])

add("rels", V, [
    REL(rid("rels", V, "REL"), "05-010", "郭勍", "郭镇", "父子亲属", "单向",
        "其高祖为驸马郭镇，援往年汝阳等公主例以请",
        "嘉靖十二年，武定侯郭勋之族弟郭勍者，其高祖为驸马郭镇，援往年汝阳等公主例以请",
        pa_ents=[e_guoqiang["ent_id"]], pb_ents=[e_guozhen["ent_id"]],
        evo="以高祖驸马援公主例请荫", conseq="永著为令禁止", span="嘉靖十二年"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "05-010", "许公主荫子之悖", "否定",
        "作者谓当时已禁其祖今日反许其孙于事理甚悖，幸门一启至四明而极矣，岂其识不逮贵溪耶",
        "当时已禁其祖，今日反许其孙，于事理甚悖。时，沈四明独当国，冯琢庵为礼卿，岂其识不逮贵溪耶？",
        "贬斥", "愤慨", "亲闻", targets=[e_shensiming["ent_id"], e_fengzhuoan["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "05-010", "祖宗亲尽亦祧", "肯定",
        "作者引王介甫因宗室辈有不看祖宗面上之言乃云祖宗亲尽亦祧何况贤辈，此真不易之论",
        "昔王介甫因宗室辈有“不看祖宗面上”之言，乃云：“祖宗亲尽亦祧，何况贤辈。”此真不易之论",
        "褒扬", "严肃", "传闻", parallel="宋王安石"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "05-010", "嘉靖—万历", "今上",
         "公主荫叙之禁与复开", "嘉靖以来", "北京", "制度",
         "祖宗典制，公主无文荫。自后间以陈乞得之，然非例也",
         "跨朝", "亲闻", who_ents=[e_guoqiang["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"]],
         supp="嘉靖十二年郭勍请荫被禁永著为令、万历壬寅恩诏复开许公主荫子"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "05-010", "公主荫叙之制", "宗室",
         "祖宗典制公主无文荫，嘉靖十二年永著为令，万历壬寅复开",
         "祖宗典制公主无文荫，自后间以陈乞得之然非例；嘉靖十二年郭勍援汝阳等公主例请荫，夏言执称事例所无乃汝阳创始非故事宜禁，上然其言遂罢勍荫且永著为令；万历壬寅三月以册立皇太子恩诏内许公主荫子送监读书，首被恩命者谢懋功杨天佐周居经郭梦兆四人，皆年远服绝；华亭草诏直云公主裔孙有志者送监读书，幸门一启至四明而极",
         "完全违背", "祖宗典制，公主无文荫。自后间以陈乞得之，然非例也",
         "异于正史", figures=[e_xiayan3["ent_id"], e_shensiming["ent_id"]]),
])

# ---- 05-016 惧内 ----
e_wangyangming = E("05-016", "王文成", "王阳明", "person", ("关联人物",), span="嘉靖")
e_shenwang = E("05-016", "申、王二相公", "申时行王锡爵", "person", ("关联人物",), span="万历")
e_qijiguang = E("05-016", "少保继光", "戚继光", "person", ("关联人物",), span="万历")
e_xiaoruxun = E("05-016", "萧都督如薰", "萧如薰", "person", ("关联人物",), span="万历")
e_yangyuanxiang = E("05-016", "杨太史元祥", "杨元祥", "person", ("关联人物",), span="万历")
e_wuzhong = E("05-016", "吴中", "吴中", "person", ("关联人物",), span="永乐—正统")
e_wangduo = E("05-016", "王铎", "王铎", "person", ("引用人物",), span="唐")
e_peitan = E("05-016", "裴谈", "裴谈", "person", ("引用人物",), span="唐")
e_wulonghou = E("05-016", "独孤后", "独孤伽罗", "person", ("引用人物",), span="隋")
add("ents", V, [e_wangyangming, e_shenwang, e_qijiguang, e_xiaoruxun, e_yangyuanxiang,
                e_wuzhong, e_wangduo, e_peitan, e_wulonghou])

ev1 = EVT(rid("events", V, "EVT"), "05-016", "社会", "诸将相",
          "明代名臣惧内之风", "本朝名臣亦大有此风，如吾浙王文成立功仗节九死不回而独严事夫人唯诺恐后，近年吴中申王二相公亦与夫人白首相庄不敢有二色",
          "嘉靖—万历", "各地", "本朝名臣，亦大有此风。往事不及知，如吾浙王文成之立功仗节，九死不回，而独严事夫人，唯诺恐后。近年吴中申、王二相公，亦与夫人白首相庄，不敢有二色",
          "一般掌故", "名臣惧内为风会", "文献转引", "正史不载",
          who_ents=[e_wangyangming["ent_id"], e_shenwang["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "05-016", "社会", "边帅",
          "虎臣为妻所制", "今上初蓟帅文登之戚少保继光、今宁夏帅萧都督如薰皆矫矫虎臣著庸边阃，俱为其妻所制",
          "万历初", "蓟镇宁夏", "至如今上初，蓟帅文登之戚少保继光、今宁夏帅萧都督如薰，皆矫矫虎臣，著庸边阃，俱为其妻所制",
          "一般掌故", "边帅亦惧内", "文献转引", "正史不载",
          who_ents=[e_qijiguang["ent_id"], e_xiaoruxun["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "05-016", "社会", "吴中",
          "吴中畏内剧", "永乐宣德间吴中为左都御史寻改刑工尚书至兼掌吏部加官至少保，其人好色多妾媵而妻严酷不敢近，禁中优人承应遂作《吴中畏内》一剧，上辄为一引满",
          "永乐—宣德", "北京", "其人好色多妾媵，而妻严酷不敢近。一日，领诰命归，妻令左右读其词，因问中曰：“此果圣语耶？”中曰：“不过词臣代言耳。”妻曰：“此翰林真无忝清华，即吴中一诰，何尝以一廉字许之。”中惭笑而已。盖中素以墨著也。其后禁中优人承应，遂作《吴中畏内》一剧，上辄为一引满。此亦惧内之最享福泽者，附记为诸公解嘲",
          "轶闻", "优人作剧上为一引满", "文献转引", "正史不载",
          who_ents=[e_wuzhong["ent_id"]])
add("events", V, [ev1, ev2, ev3])

add("cits", V, [
    CIT(rid("cits", V, "CIT"), "05-016", "裴谈事", "暗用",
        "唐孝和帝之赐宴见嘲于优人，至下比于裴谈",
        "乃若君相亦有之，则唐孝和帝之赐宴，见嘲于优人，至下比于裴谈",
        "掌故引用"),
    CIT(rid("cits", V, "CIT"), "05-016", "独孤后事", "暗用",
        "此亦何异隋之独孤后，以高颎爱妾生子遂憎之至杀之而后已也",
        "此亦何异隋之独孤后？以高颎爱妾生子，遂憎之，至杀之而后已也",
        "对比"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "05-016", "惧内之由", "肯定",
        "作者谓士大夫自中古以后多惧内者，盖名宦已成虑中冓有违言损其誉望也",
        "士大夫自中古以后多惧内者，盖名宦已成，虑中冓有违言，损其誉望也",
        "中立评述", "客观", "传闻"),
    OPN(rid("opns", V, "OPN"), "05-016", "唐末剧盗畏妻", "肯定",
        "作者谓朱温李克用一畏其妻张一敬其妻刘至与计军国大事，此其才智或自有足摄二主者",
        "唐末朱温、李克用，皆一时剧盗酋豪，一畏其妻张，每闻召，即中道而返；一敬其妻刘，至与计军国大事。此其才智，或自有足摄二主者",
        "中立评述", "客观", "传闻"),
    OPN(rid("opns", V, "OPN"), "05-016", "妒妇之惨毒", "否定",
        "作者谓汪司马长君无疆为妇陆氏所妒至刑厥夫为阉人，杨太史元祥与妇罗氏争言遂以刀自裁，尤惨毒之甚者抑更非前将相诸公比矣",
        "又若近日新安汪司马长君无疆，为妇陆氏所妒，至刑厥夫为阉人；蒲州杨太史元祥，与妇罗氏争言，遂以刀自裁。尤惨毒之甚者，抑更非前将相诸公比矣",
        "贬斥", "愤慨", "亲闻", targets=[e_yangyuanxiang["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "05-016", "永乐—万历", "王阳明",
         "明代惧内之风", "永乐以来", "各地", "风俗",
         "士大夫自中古以后多惧内者，盖名宦已成，虑中冓有违言，损其誉望也",
         "跨朝", "亲闻", who_ents=[e_wangyangming["ent_id"], e_shenwang["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"]],
         supp="王阳明严事夫人、申王二相公、戚萧二帅、吴中畏内剧诸事"),
])

# ---- 05-025 补荫 ----
e_lishanchang = E("05-025", "李韩公", "李善长", "person", ("关联人物",), span="明初")
e_fuyoude = E("05-025", "傅颍公", "傅友德", "person", ("关联人物",), span="明初")
e_wangshizhen2 = E("05-025", "王弇州", "王世贞", "person", ("关联人物",), span="嘉靖—万历")
e_fushi = E("05-025", "傅时", "傅时", "person", ("关联人物",), span="万历")
e_yuqian = E("05-025", "于忠愍", "于谦", "person", ("关联人物",), span="正统—景泰")
e_huzongxian = E("05-025", "胡襄愍", "胡宗宪", "person", ("关联人物",), span="嘉靖")
e_shixing = E("05-025", "石司马", "石星", "person", ("关联人物",), span="万历")
e_zhufengxiang = E("05-025", "朱侍御", "朱凤翔", "person", ("关联人物",), span="万历")
e_lingyunyi = E("05-025", "凌云翼", "凌云翼", "person", ("关联人物",), span="万历")
e_shiji = E("05-025", "史际", "史际", "person", ("关联人物",), span="嘉靖")
add("ents", V, [e_lishanchang, e_fuyoude, e_wangshizhen2, e_fushi, e_yuqian,
                e_huzongxian, e_shixing, e_zhufengxiang, e_lingyunyi, e_shiji])

ev1 = EVT(rid("events", V, "EVT"), "05-025", "朝政", "王世贞",
          "昌言当继故封", "开国无勋如李韩公傅颍公俱以嫌死不及嗣爵，嘉靖间继绝世亦无敢议及者，近代王弇州始昌言当继故封自是公论",
          "嘉靖—万历", "北京", "开国无勋，如李韩公、傅颍公，俱以嫌死，不及嗣爵。嘉靖间，继绝世，亦无敢议及者。近代王弇州，始昌言当继故封，自是公论",
          "一般掌故", "继绝世之议始自王世贞", "文献转引", "补正史之阙",
          who_ents=[e_lishanchang["ent_id"], e_fuyoude["ent_id"], e_wangshizhen2["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "05-025", "司法", "傅时",
          "冒称友德后人几欲承袭", "颍公之后有杭州市棍名傅时者冒称友德后人几欲承袭，会事败而止",
          "万历中", "杭州", "而颍公之后，遂有杭州市棍名傅时者，冒称友德后人，几欲承袭，会事败而止",
          "一般掌故", "冒袭事败", "文献转引", "正史不载",
          who_ents=[e_fushi["ent_id"], e_fuyoude["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "05-025", "朝政", "朱侍御",
          "疏请改于谦胡宗宪之荫", "近年朱侍御凤翔疏请改于忠愍谦之荫为锦衣，胡襄愍宗宪宜与外卫指挥，时东明石司马星在事覆准，得旨允行",
          "万历中", "北京", "近年朱侍御（凤翔）疏请改于忠愍（谦）之荫为锦衣，胡襄愍（宗宪）宜与外卫指挥，时东明石司马（星）在事覆准，得旨允行",
          "制度变动", "改荫得旨允行", "文献转引", "补正史之阙",
          who_ents=[e_zhufengxiang["ent_id"], e_yuqian["ent_id"], e_huzongxian["ent_id"], e_shixing["ent_id"]])
add("events", V, [ev1, ev2, ev3])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "05-025", "石星", "兵部尚书", "万历中",
         "现任", "时东明石司马（星）在事覆准，得旨允行",
         "近年朱侍御（凤翔）疏请改于忠愍（谦）之荫为锦衣，胡襄愍（宗宪）宜与外卫指挥，时东明石司马（星）在事覆准，得旨允行",
         person_ents=[e_shixing["ent_id"]], contro="有争议",
         ctx="覆准改于谦胡宗宪之荫"),
])

add("rels", V, [
    REL(rid("rels", V, "REL"), "05-025", "凌元超", "凌云翼", "父子亲属", "单向",
        "凌子元超、史子继书，俱历官指挥使佥事，锦衣大堂，虽已罢任，俱在辇下",
        "石司马覆疏时，凌子元超、史子继书，俱历官指挥使佥事，锦衣大堂，虽已罢任，俱在辇下",
        pa_ents=[e_lingyunyi["ent_id"]], pb_ents=[],
        evo="冒功当革二人之一为其子", conseq="依违其词云俟二臣身终之日再议",
        span="万历中"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "05-025", "二公后俱微甚", "中立",
        "作者谓然二公后俱微甚无可征考，而颍公之后有市棍冒称友德后人几欲承袭，盖汤邓常李诸将尚有裔孙为锦衣易于稽核",
        "然二公后俱微甚，无可征考。而颍公之后，遂有杭州市棍名傅时者，冒称友德后人，几欲承袭，会事败而止。盖汤、邓、常、李诸将，尚有裔孙为锦衣，易于稽核。二公在国初已夷于舆隶矣",
        "感慨", "惋惜", "传闻", targets=[e_lishanchang["ent_id"], e_fuyoude["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "05-025", "胡之功过与于之不朽", "肯定",
        "作者谓胡之功过相当即得一男爵非过，于忠愍本无后其子名晃者官至应天府尹已立侄为嗣，然富弼司马光在宋亦无子亦何害其不朽",
        "胡之功过相当，即得一男爵非过。若于忠愍本无后，其子名晃者，官至应天府尹，已立侄为嗣。然富弼、司马光在宋亦无子，亦何害其不朽",
        "褒扬", "严肃", "传闻", targets=[e_yuqian["ent_id"], e_huzongxian["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "05-025", "凌史二荫之剪抑", "否定",
        "作者谓凌洋山罗旁之功不下殷石汀此荫似不为滥，史雁峰以家丁拒倭绩虽少逊然破家徇国亦足为倡义者劝，徒以二公俱为故相江陵客不免剪抑太过",
        "凌洋山罗旁之功，不下殷石汀，此荫似不为滥。史雁峰以家丁拒倭，绩虽少逊，然破家徇国，亦足为倡义者劝。徒以二公俱为故相江陵客，不免剪抑太过",
        "贬斥", "愤慨", "亲闻", targets=[e_lingyunyi["ent_id"], e_shiji["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "05-025", "嘉靖—万历", "王世贞",
         "功臣补荫之议", "嘉靖以来", "北京", "制度",
         "开国无勋，如李韩公、傅颍公，俱以嫌死，不及嗣爵",
         "跨朝", "亲闻", who_ents=[e_lishanchang["ent_id"], e_fuyoude["ent_id"], e_wangshizhen2["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"]],
         supp="继绝世之议、傅时冒袭、改于谦胡宗宪之荫、凌史二荫剪抑"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "05-025", "功臣荫叙之制", "官制",
         "嘉靖间继绝世无敢议，王世贞昌言后公论始定；万历中改于谦胡宗宪之荫",
         "开国无勋如李韩公傅颍公俱以嫌死不及嗣爵，嘉靖间继绝世亦无敢议及，王弇州始昌言当继故封自是公论；傅时冒称友德后人几欲承袭事败而止；朱凤翔疏请改于忠愍之荫为锦衣、胡襄愍宜与外卫指挥，石星覆准得旨允行；又云尚有冒功当革者二人为故尚书凌云翼荫锦衣世千户、故少卿史际荫锦衣世百户，覆疏依违云俟二臣身终之日再议，其后继书子仍得世袭而凌氏以贫至今未袭",
         "变通", "近年朱侍御（凤翔）疏请改于忠愍（谦）之荫为锦衣，胡襄愍（宗宪）宜与外卫指挥，时东明石司马（星）在事覆准，得旨允行",
         "补正史之阙", figures=[e_wangshizhen2["ent_id"], e_shixing["ent_id"], e_yuqian["ent_id"]]),
])

# ---- 05-028 爵主兵主 ----
e_juezhu = E("05-028", "爵主", "爵主", "custom", ("主体",))
e_bingzhu = E("05-028", "兵主", "兵主", "custom", ("客体",))
add("ents", V, [e_juezhu, e_bingzhu])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "05-028", "允许", ["得"],
         "公侯伯家爵主", "爵主",
         "一切吉凶大事以及争阅构斗皆听爵主分剖曲直，其罪稍轻不必送法司者得自行笞禁不避尊行",
         "一切吉凶大事，以及争阅构斗，皆听爵主分剖曲直。其罪稍轻，不必送法司者，得自行笞禁，不避尊行，亦犹天家亲藩，及郡王体例，最合古人宗法",
         "惯例", "变通", "开国靖难诸故家"),
    RULE(rid("rules", V, "RULE"), "05-028", "程序", ["呼"],
         "军中僚伍称谓", "偏裨幕宾",
         "稍为雅谈者每呼正任总兵官为兵主，副将以下即贵至横玉仅呼为帅主",
         "又军中僚伍偏裨，以及幕宾，稍为雅谈者，每呼正任总兵官为兵主。此惟大将专生杀者为然，副将以下，即贵至横玉，仅呼为帅主耳",
         "惯例", "遵行", "万历中"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "05-028", "爵主之尊", "肯定",
        "作者谓亦犹天家亲藩及郡王体例，最合古人宗法",
        "亦犹天家亲藩，及郡王体例，最合古人宗法",
        "褒扬", "严肃", "传闻", targets=[e_juezhu["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "05-028", "暴贵者不能约束", "否定",
        "作者谓然惟开国靖难诸故家为然，其他暴贵者不能尽听约束矣",
        "然惟开国靖难诸故家为然，其他暴贵者，不能尽听约束矣",
        "感慨", "客观", "传闻", targets=[e_juezhu["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "05-028", "使主之称", "中立",
        "作者谓盖亦唐人以使主称节度大使意也，宋世使者出疆亦名正使为使主，其副使犯令虽尊官亦得用军法诛之",
        "盖亦唐人以使主称节度大使意也。宋世使者出疆，亦名正使为使主。其副使犯令，虽尊官亦得用军法诛之",
        "考辨", "客观", "传闻", parallel="唐节度使、宋正使"),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "05-028", "今", "公侯伯家",
         "爵主兵主之称", "万历间", "各地", "风俗",
         "凡公、侯、伯家，最尊嫡长，其承袭世封者，举宗呼为爵主",
         "万历", "亲闻", who_ents=[e_juezhu["ent_id"]],
         supp="公侯伯家爵主分剖曲直自行笞禁、军中呼总兵官为兵主"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "05-028", "爵主分权之制", "宗室",
         "开国靖难诸故家爵主得自行笞禁，最合古人宗法",
         "公侯伯家最尊嫡长，承袭世封者举宗呼为爵主，一切吉凶大事及争阅构斗皆听爵主分剖曲直，罪稍轻不必送法司者得自行笞禁不避尊行，亦犹天家亲藩及郡王体例；然惟开国靖难诸故家为然，其他暴贵者不能尽听约束；军中僚伍偏裨幕宾每呼正任总兵官为兵主，副将以下仅呼帅主，盖亦唐人以使主称节度大使意",
         "变通", "凡公、侯、伯家，最尊嫡长，其承袭世封者，举宗呼为爵主",
         "正史不载", figures=[e_juezhu["ent_id"], e_bingzhu["ent_id"]]),
])

# ---- 05-029 服色之僭 ----
e_neichen = E("05-029", "内臣", "在京内臣", "person", ("关联人物",), faction="宦官", span="万历")
e_wangfuchengfeng = E("05-029", "王府承奉", "王府承奉", "official", ("关联人物",), faction="宦官", span="万历")
e_huonanhai = E("05-029", "霍南海", "霍韬", "person", ("关联人物",), span="嘉靖")
e_shenshangqiu = E("05-029", "沈商邱", "沈思孝", "person", ("关联人物",), span="万历")
add("ents", V, [e_neichen, e_wangfuchengfeng, e_huonanhai, e_shenshangqiu])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "05-029", "禁止", ["僭拟"],
         "天下服饰", "勋戚内官妇人",
         "服饰不得僭拟无等，内臣不得服似蟒似斗牛之衣，王府承奉未赐者不得被蟒腰玉",
         "天下服饰，僭拟无等者，有三种。其一则勋戚，如公侯伯支子勋卫，为散骑舍人，其官止八品耳，乃家居或废罢者，皆衣麟服，击金带，顶褐盖，自称勋府",
         "祖制", "完全违背", "万历中",
         viol="在内臣稍家温者，辄服似蟒，似斗牛之衣，名为草兽，金碧晃目，扬鞭长安道上，无人敢问"),
])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "05-029", "霍南海", "尚书", "嘉靖间",
         "现任", "嘉靖间霍南海，近年沈商邱，俱抗疏昌言，力禁僭侈，而独不及此三种，何耶？",
         "嘉靖间霍南海，近年沈商邱，俱抗疏昌言，力禁僭侈，而独不及此三种，何耶？",
         person_ents=[e_huonanhai["ent_id"]], ctx="抗疏力禁僭侈"),
    APPT(rid("appts", V, "APPT"), "05-029", "沈商邱", "都给事中", "万历中",
         "现任", "嘉靖间霍南海，近年沈商邱，俱抗疏昌言，力禁僭侈，而独不及此三种，何耶？",
         "嘉靖间霍南海，近年沈商邱，俱抗疏昌言，力禁僭侈，而独不及此三种，何耶？",
         person_ents=[e_shenshangqiu["ent_id"]], ctx="抗疏力禁僭侈"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "05-029", "三种服饰僭越", "否定",
        "作者谓京师至贱如长班至积如教坊其妇外出莫不首戴珠箍身被文绣，一切白泽麒麟飞鱼坐蟒靡不有之，且乘坐肩舆揭帘露面与阁部公卿交错于康逵，真天地间大灾孽",
        "且乘坐肩舆，揭帘露面，与阁部公卿，交错于康逵，前驱既不呵止，大老亦不诘责，真天地间大灾孽",
        "贬斥", "愤慨", "亲闻"),
    OPN(rid("opns", V, "OPN"), "05-029", "霍沈禁僭不及三种", "讽刺",
        "作者谓嘉靖间霍南海近年沈商邱俱抗疏昌言力禁僭侈，而独不及此三种，何耶",
        "嘉靖间霍南海，近年沈商邱，俱抗疏昌言，力禁僭侈，而独不及此三种，何耶？",
        "讽刺", "嘲讽", "亲闻", targets=[e_huonanhai["ent_id"], e_shenshangqiu["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "05-029", "嘉靖—万历", "今上",
         "服饰僭越三种", "嘉靖以来", "京师", "风俗",
         "天下服饰，僭拟无等者，有三种",
         "跨朝", "亲闻", who_ents=[e_neichen["ent_id"], e_wangfuchengfeng["ent_id"]],
         supp="勋戚衣麟服、内臣服似蟒似斗牛、妇人袍带珠箍文绣三种僭越"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "05-029", "服饰等第之制", "礼制",
         "天下服饰僭拟无等者三种，嘉靖万历间抗疏力禁不及",
         "一为勋戚，公侯伯支子勋卫为散骑舍人其官止八品，乃家居或废罢者皆衣麟服击金带顶褐盖自称勋府，驸马庶子例为齐民而会见一人以白身纳外卫指挥空衔其衣亦如勋卫而衷以四爪象龙；一为内官，在京内臣稍家温者辄服似蟒似斗牛之衣名为草兽，王府承奉未赐者亦被蟒腰玉与抚按藩臬往远宴会恬不为怪；一为妇人，在外士人妻女相沿袭用袍带，京师至贱如长班至积如教坊其妇外出莫不首戴珠箍身被文绣，一切白泽麒麟飞鱼坐蟒靡不有之",
         "完全违背", "天下服饰，僭拟无等者，有三种",
         "异于正史", figures=[e_huonanhai["ent_id"], e_shenshangqiu["ent_id"]]),
])

# ---- 05-031 外戚封爵同邑 ----
e_ruchang = E("05-031", "茹常", "茹瑫", "person", ("关联人物",), span="洪武—建文")
e_lubing = E("05-031", "陆炳", "陆炳", "person", ("关联人物",), span="嘉靖")
e_wuan = E("05-031", "吴安", "吴安", "person", ("主体",), span="景泰—天顺")
e_xianfei = E("05-031", "贤妃吴氏", "吴氏", "person", ("关联人物",), span="宣德—景泰")
e_fangrui = E("05-031", "方锐", "方锐", "person", ("主体",), span="嘉靖")
e_xiaoliefang = E("05-031", "孝烈方后", "方氏", "person", ("关联人物",), span="嘉靖")
e_liyuan = E("05-031", "李远", "李远", "person", ("关联人物",), span="永乐")
e_lian = E("05-031", "李安", "李安", "person", ("关联人物",), span="永乐")
add("ents", V, [e_ruchang, e_lubing, e_wuan, e_xianfei, e_fangrui, e_xiaoliefang,
                e_liyuan, e_lian])

ev1 = EVT(rid("events", V, "EVT"), "05-031", "朝政", "吴安",
          "景帝登极封安平伯", "景帝登极已封故宣庙贤妃吴氏之弟名安者，其时贤妃称皇太后，故安循往例得开茅土",
          "景泰初", "北京", "如安平伯，则景帝登极，已封故宣庙贤妃吴氏之弟名安者，其时贤妃称皇太后，故安循往例，得开茅土",
          "制度变动", "外戚以废后弟封爵", "文献转引", "补正史之阙",
          who_ents=[e_wuan["ent_id"], e_xianfei["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "05-031", "朝政", "吴安",
          "英宗反正辞爵拜锦衣指挥使", "至英宗反正太后仍称贤妃，安辞爵邑，上准辞，拜锦衣指挥使矣",
          "天顺初", "北京", "至英宗反正，太后仍称贤妃，安辞爵邑，上准辞，拜锦衣指挥使矣",
          "一般掌故", "废后既夺之封", "文献转引", "补正史之阙",
          who_ents=[e_wuan["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "05-031", "朝政", "方锐",
          "以左都督进封安平伯", "嘉靖十八年世宗孝烈皇后父方锐以左都督进封，亦号安平伯，廿一年孝烈方后以宫婢构逆拥卫圣躬受非常宠眷，锐亦进侯爵",
          "嘉靖十八年", "北京", "嘉靖十八年，世宗孝烈皇后父方锐，以左都督进封，亦号安平伯，犹曰一时失误也。廿一年，孝烈方后以宫婢构逆，拥卫圣躬，受非常宠眷，锐亦进侯爵",
          "一般掌故", "外戚爵号相重至三见", "文献转引", "补正史之阙",
          who_ents=[e_fangrui["ent_id"], e_xiaoliefang["ent_id"]])
add("events", V, [ev1, ev2, ev3])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "05-031", "方锐", "左都督", "嘉靖十八年",
         "升迁", "世宗孝烈皇后父方锐，以左都督进封，亦号安平伯",
         "嘉靖十八年，世宗孝烈皇后父方锐，以左都督进封，亦号安平伯，犹曰一时失误也",
         person_ents=[e_fangrui["ent_id"]], contro="有争议",
         ctx="外戚进封而爵号与吴安相重"),
    APPT(rid("appts", V, "APPT"), "05-031", "吴安", "锦衣指挥使", "天顺初",
         "贬谪", "至英宗反正，太后仍称贤妃，安辞爵邑，上准辞，拜锦衣指挥使矣",
         "至英宗反正，太后仍称贤妃，安辞爵邑，上准辞，拜锦衣指挥使矣",
         person_ents=[e_wuan["ent_id"]], ctx="辞安平伯爵邑改拜锦衣指挥使"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "05-031", "当事者不学", "讽刺",
        "作者谓五等之爵其封号有至再，如忠诚伯前有文臣茹常后有武臣陆炳，以及惠安顺义之属屡见，虽于国体无关然识者已讥当事之不学至此",
        "五等之爵，其封号有至再者。如忠诚伯，前有文臣茹常，后有武臣陆炳。以及惠安、顺义之属，屡见矣。虽于国体无关，然识者已讥当事之不学至此",
        "讽刺", "嘲讽", "传闻", targets=[e_ruchang["ent_id"], e_lubing["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "05-031", "方锐仍号安平", "否定",
        "作者谓廿一年锐亦进侯爵，何以仍号安平不改正耶，况外戚爵邑有几，吴安为废后既夺之封岂是佳事，况废绝尤上所恶闻，犹幸世宗不核故牒得免深求，而当事元老贵溪分宜亦卤莽极矣",
        "廿一年，孝烈方后以宫婢构逆，拥卫圣躬，受非常宠眷，锐亦进侯爵。何以仍号安平，不改正耶？况外戚爵邑有几，吴安为废后既夺之封，岂是佳事？况废绝尤上所恶闻，犹幸世宗不核故牒，得免深求。而当事元老、贵溪、分宜，亦卤莽极矣！",
        "贬斥", "愤慨", "传闻", targets=[e_fangrui["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "05-031", "李安吴安俱不得延世", "讽刺",
        "作者谓按安平侯伯在永乐中直隶怀远人李远者以靖难功封侯，其子安袭伯爵即于文皇朝坐法削爵谪戍，至方锐而三见，李安与吴安俱不得延世其不祥尤甚，何以屡袭其号，盖是时上方事玄阁臣礼卿惟考据诸真灵位业耳",
        "至方锐而三见焉。李安与吴安，俱不得延世其不祥尤甚，何以屡袭其号，盖是时上方事玄，阁臣礼卿，惟考据诸真灵位业耳。其他古今之学，既不暇及也！",
        "讽刺", "嘲讽", "传闻", targets=[e_lian["ent_id"], e_wuan["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "05-031", "永乐—嘉靖", "世宗",
         "外戚封爵同邑之重合", "永乐以来", "北京", "制度",
         "五等之爵，其封号有至再者",
         "跨朝", "传闻", who_ents=[e_wuan["ent_id"], e_fangrui["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"]],
         supp="忠诚伯两见、安平伯三见，当事元老卤莽不核故牒"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "05-031", "外戚封爵之制", "宗室",
         "外戚爵号相重，安平伯至三见而不改正",
         "五等之爵封号有至再，忠诚伯前有文臣茹常后有武臣陆炳，惠安顺义之属屡见；安平伯景帝登极封故宣庙贤妃吴氏之弟吴安，英宗反正安辞爵邑拜锦衣指挥使；嘉靖十八年孝烈皇后父方锐以左都督进封亦号安平伯，廿一年进侯爵而仍号安平不改正；永乐中李远以靖难功封安平侯，其子安袭伯爵坐法削爵谪戍，至方锐而三见；当事元老贵溪分宜卤莽极矣",
         "完全违背", "五等之爵，其封号有至再者。如忠诚伯，前有文臣茹常，后有武臣陆炳",
         "补正史之阙", figures=[e_wuan["ent_id"], e_fangrui["ent_id"], e_lian["ent_id"]]),
])

# ---- 05-034 曹祖 ----
e_cao = E("05-034", "曹祖", "曹祖", "person", ("主体",), span="正德")
e_caoding = E("05-034", "鼎", "曹鼎", "person", ("关联人物",), span="正德")
e_zhangheling = E("05-034", "张鹤龄", "张鹤龄", "person", ("主体",), span="正德—嘉靖")
e_liujin = E("05-034", "刘瑾", "刘瑾", "person", ("关联人物",), faction="宦官", span="正德")
e_zhangzilin = E("05-034", "张子麟", "张子麟", "person", ("关联人物",), span="正德")
add("ents", V, [e_cao, e_caoding, e_zhangheling, e_liujin, e_zhangzilin])

ev1 = EVT(rid("events", V, "EVT"), "05-034", "司法", "曹祖",
          "上书数鼎恶被罪", "正德初刘瑾用事，曹祖上书数鼎恶且自言其生兆应天，曹祖之语多幻妄，瑾怒罪之械还浙",
          "正德初", "浙江", "正德初，刘瑾用事，祖上书数鼎恶，且自言其生兆应天。曹祖之语多幻妄，瑾怒罪之，械还浙",
          "一般掌故", "上书数子恶被械还", "文献转引", "正史不载",
          who_ents=[e_cao["ent_id"], e_liujin["ent_id"]])
ev2 = EVT(rid("events", V, "EVT"), "05-034", "司法", "曹祖",
          "击登闻鼓诉鹤龄阴图不轨", "正德十年十月又来依鼎，鼎不礼其父，祖遂并恨张氏，击登闻鼓诉鹤龄兄弟阴图不轨，上震怒命多官廷鞫又命司礼监东厂讯之，禁鹤龄兄弟不许朝参",
          "正德十年十月", "北京", "正德十年十月，又来依鼎，鼎不礼其父，祖遂并恨张氏，击登闻鼓，诉鹤龄兄弟阴图不轨。上震怒，命多官廷鞫，又命司礼监东厂讯之，禁鹤龄兄弟，不许朝参",
          "重大政治", "登闻鼓诉致侯门被禁", "文献转引", "补正史之阙",
          who_ents=[e_cao["ent_id"], e_zhangheling["ent_id"]])
ev3 = EVT(rid("events", V, "EVT"), "05-034", "司法", "张子麟",
          "祖自裁于狱穷治原问官", "会祖自裁于狱，上益疑怒降旨诘责，刑部尚书张子麟下原问主事及提牢巡风官于诏狱穷治之，覆疏谓祖所奏既无左验实惧罪服毒",
          "正德十年", "北京", "会祖自裁于狱，上益疑怒，降旨诘责。刑部尚书张子麟，下原问主事，及提牢巡风官于诏狱，穷治之。覆疏谓祖所奏，既无左验，实惧罪服毒",
          "一般掌故", "自裁疑怒穷治有司", "文献转引", "补正史之阙",
          who_ents=[e_zhangzilin["ent_id"], e_cao["ent_id"]])
add("events", V, [ev1, ev2, ev3])

add("rules", V, [
    RULE(rid("rules", V, "RULE"), "05-034", "程序", ["击"],
         "民间诉事", "民",
         "冤抑得击登闻鼓诉",
         "祖遂并恨张氏，击登闻鼓，诉鹤龄兄弟阴图不轨",
         "祖制", "遵行", "正德间"),
])

add("appts", V, [
    APPT(rid("appts", V, "APPT"), "05-034", "张子麟", "刑部尚书", "正德十年",
         "现任", "刑部尚书张子麟，下原问主事，及提牢巡风官于诏狱，穷治之",
         "刑部尚书张子麟，下原问主事，及提牢巡风官于诏狱，穷治之。覆疏谓祖所奏，既无左验，实惧罪服毒",
         person_ents=[e_zhangzilin["ent_id"]], contro="有争议",
         ctx="曹祖自裁后穷治原问官"),
])

add("opns", V, [
    OPN(rid("opns", V, "OPN"), "05-034", "曹祖自尽与否", "怀疑",
        "作者谓曹祖之果自尽与否终莫能明也，盖张氏弟兄生平宜破家杀身事不少，特坐以大逆则不服耳",
        "而曹祖之果自尽与否，终莫能明也。盖张氏弟兄生平宜破家杀身事不少，特坐以大逆，则不服耳",
        "考辨", "严肃", "传闻", targets=[e_cao["ent_id"], e_zhangheling["ent_id"]]),
    OPN(rid("opns", V, "OPN"), "05-034", "张氏平日横恣", "否定",
        "作者谓按寿宁建昌二侯在武宗朝已不免谋逆之谤，其平日横恣失人心可知，何待世宗时始败，且张氏惯以睚眦杀人，至嘉靖十二年延龄谳辞中所列杀僧杀婢诸事俱有宝迹",
        "按寿宁、建昌二侯，在武宗朝。已不免谋逆之谤，其平日横恣，失人心可知，何待世宗时始败？且张氏惯以睚眦杀人，至嘉靖十二年，延龄谳辞中，所列杀僧、杀婢诸事，俱有宝迹",
        "贬斥", "愤慨", "传闻", targets=[e_zhangheling["ent_id"]]),
])

add("mings", V, [
    MING(rid("mings", V, "MING"), "05-034", "正德—嘉靖", "曹祖",
         "张鹤龄被诬案", "正德以来", "北京", "朝政",
         "浙民曹祖，有子鼎，为寿宁侯张鹤龄仆。正德初，刘瑾用事，祖上书数鼎恶，且自言其生兆应天",
         "跨朝", "传闻", who_ents=[e_cao["ent_id"], e_zhangheling["ent_id"]],
         ref_evts=[ev1["event_id"], ev2["event_id"], ev3["event_id"]],
         supp="上书数鼎恶、登闻鼓诉阴图不轨、自裁于狱穷治原问官"),
])

add("regs", V, [
    REG2(rid("regs", V, "REG"), "05-034", "登闻鼓诉之制", "司法",
         "正德十年曹祖击登闻鼓诉寿宁侯张鹤龄兄弟阴图不轨",
         "浙民曹祖有子鼎为寿宁侯张鹤龄仆，正德初上书数鼎恶且自言生兆应天，语多幻妄为刘瑾所罪械还浙；正德十年十月复来依鼎，鼎不礼其父，祖遂并恨张氏击登闻鼓诉鹤龄兄弟阴图不轨，上震怒命多官廷鞫又命司礼监东厂讯之，禁鹤龄兄弟不许朝参；会祖自裁于狱，上益疑怒降旨诘责，刑部尚书张子麟下原问主事及提牢巡风官于诏狱穷治之，覆疏谓祖所奏既无左验证实惧罪服毒；张氏阖门惴恐乃大行金于内，昭圣亦百端祈请，事稍懈犹罚子麟等俸，二张朝参究终罢不许",
         "遵行", "正德十年十月，又来依鼎，鼎不礼其父，祖遂并恨张氏，击登闻鼓，诉鹤龄兄弟阴图不轨。上震怒，命多官廷鞫，又命司礼监东厂讯之，禁鹤龄兄弟，不许朝参",
         "补正史之阙", figures=[e_cao["ent_id"], e_zhangheling["ent_id"], e_zhangzilin["ent_id"]]),
])


# ================================================================ 写回
def load_item_originals():
    """{item_id: 去空白源文段}，用于计算 ents 的 start/end 偏移"""
    out = {}
    for v in VOLS:
        out.update(SEG[v])
    return out


def write_back():
    originals = load_item_originals()
    report = {}
    for vol, layers in NEW.items():
        report[vol] = {}
        for layer, new_recs in layers.items():
            path = BASE / "_layers" / layer / ("%s_%s.json" % (layer, vol))
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            assert isinstance(data, dict), (vol, layer, "期望 records 包裹")
            old_recs = data["records"]
            if layer == "ents":
                aligned = []
                for r in new_recs:
                    seg = originals.get(r["item_id"]) or ""
                    idx = seg.find(r["text"])
                    if vol in ("02", "03", "04"):
                        # 风格 A：含 start/end/confidence
                        aligned.append({
                            "ent_id": r["ent_id"], "item_id": r["item_id"],
                            "text": r["text"], "type": r["type"],
                            "normalized": r["normalized"],
                            "start": idx if idx >= 0 else None,
                            "end": idx + len(r["text"]) if idx >= 0 else None,
                            "confidence": r["confidence"],
                            "role_in_entry": r["role_in_entry"],
                            "faction": r["faction"], "exam_info": r["exam_info"],
                            "career_span": r["career_span"],
                        })
                    else:
                        # 卷05 风格 B：无 start/end/confidence
                        aligned.append({
                            "ent_id": r["ent_id"], "item_id": r["item_id"],
                            "text": r["text"], "type": r["type"],
                            "normalized": r["normalized"],
                            "role_in_entry": r["role_in_entry"],
                            "faction": r["faction"], "exam_info": r["exam_info"],
                            "career_span": r["career_span"],
                        })
                new_recs = aligned
            merged = old_recs + new_recs
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"records": merged}, f, ensure_ascii=False, indent=2)
                f.write("\n")
            report[vol][layer] = len(new_recs)
    return report


def main():
    # 1) 溯源 + 枚举校验（任一失败则不写盘）
    if ERRORS:
        print("!!! 校验失败 %d 项：" % len(ERRORS))
        for e in ERRORS:
            print("   ", e)
        print("未写盘。")
        return 1
    # 2) ENT 池越界检查
    used = _ent_pool - ENT_START
    print("ENT 池用量: ENT-%d .. ENT-%d (新分配 %d 个)" % (ENT_START, _ent_pool - 1, used))
    # 3) 写回
    report = write_back()
    for vol in sorted(report):
        print(vol, json.dumps(report[vol], ensure_ascii=False))
    print("TOTAL new records:", sum(sum(v.values()) for v in report.values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
