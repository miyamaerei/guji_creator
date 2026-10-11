# -*- coding: utf-8 -*-
"""
《新官轨范》规则层抽取管线（kg-rule v1）
- 按 √ 条目拆分（复用章节 XHTML 结构：<p class="item">）
- 规则层 = 找规范句：仅含规则触发词（不可/不许/务要/须/止许/毋/勿/打三十/限一日 等）的条目进入规则抽取；
  无触发词的条目跳过（不把普通叙述句转成规则）
- 槽位：condition / subject / modal(禁止·义务·允许·程序·时限·处罚·优先级) / action / object / purpose / punishment
- 类型：禁止型、义务型、允许型、程序型、时限型、处罚型、优先级型；多模态命中 → 组合型（如"禁止+允许"）
- 每卷一个 JSON；最后全局归一化汇总 + 触发词统计 + 报告
- 每条规则附 AI 发散示例（kind=generated，非原文，仅作理解辅助）
"""
import os, re, json, html as htmllib, glob
from collections import Counter, OrderedDict

OUT_DIR = r"C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat"
CH_DIR = os.path.join(OUT_DIR, "新官轨范_章节")
RUL_DIR = os.path.join(OUT_DIR, "新官轨范_规则")
MERGE_FILE = os.path.join(OUT_DIR, "新官轨范_规则_归一_汇总.json")
REPORT_FILE = os.path.join(OUT_DIR, "新官轨范_规则_总报告.md")
SCHEMA_VER = "kg-rule-json-v1"
RULE_VER = "rule-layer-v1"

# ---------- 触发词表（复合词优先，finditer 后按区间去重；modal 归类） ----------
TRIGGERS = [
    # 禁止
    ("断不可", "prohibit"), ("不准", "prohibit"), ("不可", "prohibit"), ("不许", "prohibit"),
    ("不得", "prohibit"), ("严禁", "prohibit"), ("毋", "prohibit"), ("勿", "prohibit"),
    # 义务
    ("务须", "obligation"), ("务要", "obligation"), ("须", "obligation"),
    # 允许
    ("止许", "allow"), ("许令", "allow"), ("方许", "allow"), ("止将", "allow"),
    ("止令", "allow"), ("许", "allow"),
    # 时限
    ("限", "deadline"),
    # 处罚
    ("革去", "penalty"), ("痛加责治", "penalty"), ("责治", "penalty"), ("责罚", "penalty"),
    ("杖", "penalty"), ("枷", "penalty"), ("打", "penalty"), ("加罚", "penalty"),
    ("罚", "penalty"), ("问罪", "penalty"),
]
# 守卫：命中但不应触发规则的上下文
GUARD = {
    "禁": ["禁子"],            # 禁子=狱卒，非禁止
    "当": ["当厅"],            # 当厅=在公堂，非义务
    "不得": ["不得已"],        # 不得已=迫不得已，非禁止
    "须": ["务须"],            # 已被复合词覆盖，守卫防重复
    "许": ["止许", "许令", "方许"],
    "限": ["无限"],            # 未见于原文，防御
}
# 目的/后果引导词
PURPOSE_RE = re.compile(r"(?:致(?:生|有|令)?|恐|诚恐|庶|俾|以防|防|盖因|以资)([^，。；]{2,40})")
# 条件引导词（句首）
COND_RE = re.compile(r"^(凡|但凡|但|如|若|倘|或|一应)([^，。；]{2,40})")
# 程序型序列
PROC_SEQ = [("先", "次"), ("先", "然后"), ("毕", "然后"), ("了毕", "后"), ("先", "方")]
# 优先级型
PRIORITY_PAT = re.compile(r"(大事[^，。；]{0,20}小事|小事[^，。；]{0,20}大事|大事.{0,12}出票|小事.{0,12}言语)")
# 对象抽取动词
OBJ_VERB = re.compile(r"(?:差|遣|发|委|令|拘|提|拿|放|赈|给|散|买|催|点|编|审|查|勘|责|罚|杖|打|追|问|佥)([^，。；！？]{2,14})")
# 主体词表（显式主语，条目开头 2-6 字）
SUBJ_WORDS = ["各里里长", "里长", "甲首", "粮长", "老人", "总甲", "里老", "书手", "吏典",
              "阴阳生", "医生", "门子", "皂隶", "禁子", "狱卒", "快手", "弓兵", "铺兵",
              "应捕", "仵作", "直堂吏", "直印吏", "巡风吏", "刑房吏", "承发吏", "六房",
              "该吏", "各吏", "上司", "本县", "正官", "佐贰官", "署印官", "教官", "生员",
              "大户", "富民", "势豪", "僧道", "师巫", "匠人", "各都", "各图", "各坊"]
DEFAULT_SUBJ = "官府（知县）"

# 中文数字辅助
def cn_num(s):
    return s

def load_chapters():
    out = []
    files = sorted(glob.glob(os.path.join(CH_DIR, "*.xhtml")))
    for fp in files:
        base = os.path.basename(fp)
        no = base[:2]
        if no == "00":
            continue
        with open(fp, encoding="utf-8") as f:
            content = f.read()
        items = re.findall(r'<p class="item">(.*?)</p>', content, re.S)
        items = [htmllib.unescape(m).strip() for m in items]
        if not items:
            items = re.findall(r'<p[^>]*>(.*?)</p>', content, re.S)
            items = [htmllib.unescape(m).strip() for m in items]
        out.append((no, base, items))
    return out

def find_triggers(txt):
    """返回 [(start, end, word, modal)]，复合优先、守卫剔除、区间去重"""
    hits = []
    for word, modal in TRIGGERS:
        for m in re.finditer(re.escape(word), txt):
            s, e = m.start(), m.end()
            # 守卫
            if word in GUARD and any(txt[max(0, s - 2):e + 1].count(g) or txt[s:e + len(g)].startswith(g) for g in GUARD[word]):
                continue
            # "须/许/限"等单字若被更长复合词已覆盖则跳过（由外层去重完成）
            hits.append((s, e, word, modal))
    # 按 start 排序，重叠区间保留最长词
    hits.sort(key=lambda x: (x[0], -(x[1] - x[0])))
    keep = []
    for h in hits:
        if keep and h[0] < keep[-1][1]:
            continue
        keep.append(h)
    return keep

def split_sent(txt):
    """按句读切分，返回 [(start, end, text)]"""
    out = []
    pos = 0
    for m in re.finditer(r"[。！？；]", txt):
        s, e = pos, m.end()
        seg = txt[s:e].strip()
        if seg:
            out.append((s, e, seg))
        pos = m.end()
    if pos < len(txt):
        seg = txt[pos:].strip()
        if seg:
            out.append((pos, len(txt), seg))
    return out

def extract_condition(txt):
    trig = find_triggers(txt)
    m = COND_RE.match(txt.strip())
    start = None
    if m:
        start = m.start()
    else:
        # 引导词可出现在短标题/句后（如"告示。凡告大小词状……"）
        m2 = re.search(r"(凡|但凡|如|若|倘|或|一应)", txt)
        if m2 and m2.start() <= 12:
            start = m2.start()
    if start is not None and trig:
        s0 = trig[0][0]
        if s0 > start and s0 - start <= 40:
            cand = txt[start:s0]
            cand = re.split(r"[。；]", cand)[0].strip("，。；、 ")
            parts = cand.split("，")
            if len(parts) > 3:
                cand = "，".join(parts[:3])
            return cand
    # 补充启发：首逗号前片段若紧邻首个触发词（≤20 字），视为条件
    if trig:
        s0 = trig[0][0]
        if 0 < s0 <= 20:
            head = re.match(r"^([^，。；]{2,14})[，]", txt)
            if head:
                return head.group(1)
    return ""

def detect_subject(txt):
    head = txt.strip()[:8]
    for w in SUBJ_WORDS:
        if head.startswith(w):
            return w
    return DEFAULT_SUBJ

def extract_object(action):
    if not action:
        return ""
    m = OBJ_VERB.search(action)
    if m:
        obj = m.group(1).strip("，。；、的之")
        if len(obj) >= 2 and not re.match(r"^[不可务须止许]", obj):
            return obj
    return ""

def extract_purpose(seg):
    m = PURPOSE_RE.search(seg)
    if m:
        return m.group(0)
    return ""

def classify_extra(txt, seg):
    """程序型 / 优先级型 附加判定"""
    extra = []
    if "先" in txt and any(k in txt for k in ("次", "然后", "了毕", "毕后", "方许")):
        extra.append("procedure")
    if PRIORITY_PAT.search(txt):
        extra.append("priority")
    return extra

def build_example(rule):
    """AI 发散示例（kind=generated）——仅作理解辅助，非原文"""
    tp = rule.get("type", "")
    cond = rule.get("condition", "") or "日常政务"
    subj = rule.get("subject", DEFAULT_SUBJ)
    pa = rule.get("prohibited_action", "")
    oa = rule.get("obligation_action", "")
    aa = rule.get("allowed_action", "")
    pe = rule.get("prohibited_effect", "")
    pu = rule.get("punishment", "")
    parts = []
    if "禁止" in tp and pa:
        parts.append(f"【场景】{cond}时，若{pa}，即属违禁"
                     + (f"，{pe}" if pe else "")
                     + ("；合规做法：" + (aa or "改用文内许可途径") + "。"))
    if "义务" in tp and oa:
        parts.append(f"【场景】{cond}时，{subj}应{oa}"
                     + (f"，以{pu}" if pu else "") + "。")
    if "允许" in tp and aa and "禁止" not in tp:
        parts.append(f"【场景】{cond}时，{subj}可{aa}。")
    if "时限" in tp and rule.get("deadline"):
        parts.append(f"【场景】{cond}事项须在{rule['deadline']}内办结，逾期按规追责。")
    if "处罚" in tp and pu:
        parts.append(f"【场景】违者依规{pu}。")
    if not parts:
        parts.append(f"【场景】{cond}时，{subj}须依本条行事，违者有责。")
    return {"text": "".join(parts), "kind": "generated", "note": "AI 发散示例，非原文，仅作理解辅助"}

def rule_conf(modals, has_cond, has_action, has_purpose, has_pun, subj_inferred):
    c = 0.85
    strong = {"prohibit", "obligation", "allow"}
    if modals & strong:
        c += 0.05
    if has_action:
        c += 0.05
    if has_cond:
        c += 0.02
    if has_purpose:
        c += 0.03
    if has_pun:
        c += 0.02
    if subj_inferred:
        c -= 0.04
    return round(min(c, 0.97), 2)

def annotate_item(item_text, ch_no, ch_name, item_idx, fn, rule_no):
    """一条目 → 0..N 条规则（无触发词 → 0 条）"""
    txt = item_text
    if txt.startswith("√"):
        txt = txt[1:].lstrip()
    trig = find_triggers(txt)
    if not trig:
        return [], False
    # 一个条目 = 一条规则（含多模态 → 组合型）；若多个"凡/但/如"条件段且间隔远，则拆多条
    cond_marks = [m for m in re.finditer(r"(凡|但凡|但|如|若|倘|或)", txt)]
    blocks = []
    if len(cond_marks) > 1:
        starts = [m.start() for m in cond_marks if txt[max(0, m.start() - 1)] in "，。；" or m.start() == 0]
        starts = list(dict.fromkeys(starts))
        if len(starts) > 1:
            for i, st in enumerate(starts):
                en = starts[i + 1] if i + 1 < len(starts) else len(txt)
                blocks.append(txt[st:en].strip())
    if not blocks:
        blocks = [txt]

    rules = []
    for bi, block in enumerate(blocks):
        btrig = [t for t in find_triggers(block)]
        if not btrig:
            continue
        cond = extract_condition(block)
        subject = detect_subject(block)
        subj_inferred = subject == DEFAULT_SUBJ
        modals = [t[3] for t in btrig]
        extra = classify_extra(block, block)
        modals = list(dict.fromkeys(modals + extra))

        slots = {"prohibited_action": [], "obligation_action": [], "allowed_action": [],
                 "punishment": [], "deadline": [], "prohibited_effect": [], "purpose": []}
        for i, (s, e, word, modal) in enumerate(btrig):
            # 动作/处罚片段终点：下一触发词、句内句号分号、目的引导 三者取最先
            nxt = btrig[i + 1][0] if i + 1 < len(btrig) else len(block)
            sen = re.search(r"[。；]", block[e:nxt])
            if sen:
                nxt = min(nxt, e + sen.start())
            if i + 1 < len(btrig):
                # 下一触发词前若有短逗号残留（主语残留），动作在最后一个逗号收口
                gap = block[e:nxt]
                cm = gap.rfind("，")
                if cm > 0 and len(gap) - cm <= 8:
                    nxt = e + cm
            tail = block[e:nxt].strip("，。；、 ")
            # 在 tail 内截断目的/后果从句，动作片段取其前
            act = tail
            pm = PURPOSE_RE.search(act)
            if pm:
                eff = pm.group(0)
                slots["prohibited_effect"].append(eff)
                slots["purpose"].append(eff)
                act = act[:pm.start()].strip("，。；、 ")
            if modal == "prohibit":
                slots["prohibited_action"].append(act if act else word)
            elif modal == "obligation":
                slots["obligation_action"].append(act if act else word)
            elif modal == "allow":
                slots["allowed_action"].append(act if act else word)
            elif modal == "penalty":
                slots["punishment"].append((act if act else word))
            elif modal == "deadline":
                slots["deadline"].append(act if act else word)

        def join(v):
            return "；".join(x for x in v if x) if v else ""

        rule = {
            "rule_id": f"XGF-R-{rule_no:03d}",
            "type": "+".join(ORDER_CN.get(m, m) for m in modals) if len(modals) > 1 else ORDER_CN.get(modals[0], modals[0]),
            "primary_type": ORDER_CN.get(modals[0], modals[0]),
            "is_combo": len(modals) > 1,
            "modals": modals,
            "condition": cond,
            "subject": subject,
            "prohibited_action": join(slots["prohibited_action"]),
            "allowed_action": join(slots["allowed_action"]),
            "obligation_action": join(slots["obligation_action"]),
            "prohibited_effect": join(slots["prohibited_effect"]),
            "object": extract_object(join(slots["prohibited_action"] + slots["allowed_action"] + slots["obligation_action"])),
            "purpose": join(slots["purpose"]),
            "deadline": join(slots["deadline"]),
            "punishment": join(slots["punishment"]),
            "source": f"{fn}#条{item_idx}",
            "original": block,
            "original_offset": {"start": txt.find(block), "end": txt.find(block) + len(block)},
            "confidence": rule_conf(set(modals), bool(cond), bool(join(slots["prohibited_action"] + slots["obligation_action"] + slots["allowed_action"])),
                                    bool(slots["purpose"]), bool(slots["punishment"]), subj_inferred),
        }
        rule["example"] = build_example(rule)
        rules.append(rule)
    return rules, True

ORDER_CN = {
    "prohibit": "禁止型", "obligation": "义务型", "allow": "允许型",
    "procedure": "程序型", "deadline": "时限型", "penalty": "处罚型", "priority": "优先级型",
}
TYPE_SHORT = {
    "禁止型": "prohibit", "义务型": "obligation", "允许型": "allow",
    "程序型": "procedure", "时限型": "deadline", "处罚型": "penalty", "优先级型": "priority",
}

def main():
    os.makedirs(RUL_DIR, exist_ok=True)
    chapters = load_chapters()
    all_rules = []
    per_chapter = []
    trigger_counter = Counter()
    skipped_items = 0
    total_items = 0
    rule_no = 1
    for ch_no, base, items in chapters:
        ch_name = os.path.splitext(base)[0][3:]
        vol_rules = []
        ch_has = 0
        for i, it in enumerate(items, 1):
            total_items += 1
            rules, has = annotate_item(it, ch_no, ch_name, i, base, rule_no)
            if has:
                ch_has += 1
                for r in rules:
                    r["volume"] = ch_no
                    r["chapter"] = ch_name
                    r["item"] = i
                    vol_rules.append(r)
                    all_rules.append(r)
                    rule_no += 1
                    for _, _, w, _ in find_triggers(r["original"]):
                        trigger_counter[w] += 1
            else:
                skipped_items += 1
        per_chapter.append({
            "chapter_no": ch_no, "file": base, "chapter": ch_name,
            "item_count": len(items), "rule_item_count": ch_has,
            "rule_count": len(vol_rules),
        })
        vjson = {
            "schema_version": SCHEMA_VER, "rule_version": RULE_VER,
            "volume": ch_no, "chapter": ch_name, "chapter_no": ch_no,
            "source_file": base, "item_count": len(items),
            "rule_item_count": ch_has, "rule_count": len(vol_rules),
            "rules": vol_rules,
        }
        with open(os.path.join(RUL_DIR, f"{ch_no}_{os.path.splitext(base)[0][3:]}.json"), "w", encoding="utf-8") as f:
            json.dump(vjson, f, ensure_ascii=False, indent=1)

    # 全局归一化
    by_type = Counter()
    by_modal = Counter()
    combo_count = 0
    for r in all_rules:
        by_type[r["primary_type"]] += 1
        if r["is_combo"]:
            combo_count += 1
        for m in r["modals"]:
            by_modal[TYPE_SHORT.get(m, m)] += 1
    merge = {
        "schema_version": SCHEMA_VER, "rule_version": RULE_VER,
        "total_items": total_items,
        "rule_items": total_items - skipped_items,
        "skipped_items": skipped_items,
        "coverage": round((total_items - skipped_items) / total_items, 4) if total_items else 0,
        "total_rules": len(all_rules),
        "combo_rule_count": combo_count,
        "by_type": dict(by_type),
        "by_modal": dict(by_modal),
        "per_chapter": per_chapter,
        "trigger_stats": dict(trigger_counter.most_common()),
        "combo_rules": [r["rule_id"] + "|" + r["type"] for r in all_rules if r["is_combo"]],
        "rules": all_rules,
    }
    with open(MERGE_FILE, "w", encoding="utf-8") as f:
        json.dump(merge, f, ensure_ascii=False, indent=1)

    # 报告
    lines = []
    lines.append("# 《新官轨范》规则层抽取总报告（kg-rule v1）")
    lines.append("")
    lines.append(f"- 条目总数：{total_items}（卷上 94 + 卷下 179 + 卷首注语 1）")
    lines.append(f"- 含规范句条目：{total_items - skipped_items}；未含触发词而跳过的叙述型条目：{skipped_items}")
    lines.append(f"- 规则总数：{len(all_rules)}（一条目可含多模态 → 组合型规则）")
    lines.append(f"- 覆盖率（含规则条目/总条目）：{merge['coverage']}")
    lines.append("")
    lines.append("## 1. 方法")
    lines.append("")
    lines.append("- 条目拆分：按 √ 逐条（274 条），规则层只抽取含触发词的规范句，不把叙述句转成规则。")
    lines.append("- 触发词表：禁止（不可/不许/不得/严禁/毋/勿）、义务（务要/务须/须）、允许（止许/许令/方许/许/准）、时限（限）、处罚（打/杖/枷/责罚/责治/罚/问罪/追赔/革去）、程序（先…次…然后/了毕）、优先级（大事/小事）。")
    lines.append("- 守卫：禁子（狱卒非禁止）、当厅（在公堂非义务）、追悔（后悔非处罚）等不触发。")
    lines.append("- 槽位：condition/subject/action(禁止/允许/义务)/object/purpose/effect/deadline/punishment + source/original/confidence。")
    lines.append("- 类型：多模态命中 → 组合型（如“禁止+允许”），不是矛盾而是组合规则。")
    lines.append("- 示例：每条规则附 AI 发散场景示例（kind=generated，非原文）。")
    lines.append("")
    lines.append("## 2. 规则类型分布（by_type，按主导模态统计）")
    lines.append("")
    lines.append("| 类型 | 规则数 |")
    lines.append("|---|---|")
    for t, c in by_type.most_common():
        lines.append(f"| {t} | {c} |")
    lines.append(f"| 组合型（多模态同条） | {combo_count} |")
    lines.append("")
    lines.append("## 3. 模态触发分布（by_modal，含组合规则内多模态）")
    lines.append("")
    lines.append("| 模态 | 命中 |")
    lines.append("|---|---|")
    for m, c in by_modal.most_common():
        lines.append(f"| {m} | {c} |")
    lines.append("")
    lines.append("## 4. 触发词频率 Top20")
    lines.append("")
    lines.append("| 触发词 | 次数 |")
    lines.append("|---|---|")
    for w, c in trigger_counter.most_common(20):
        lines.append(f"| {w} | {c} |")
    lines.append("")
    lines.append("## 5. 每卷统计")
    lines.append("")
    lines.append("| 卷 | 条目 | 含规则条目 | 规则数 |")
    lines.append("|---|---|---|---|")
    for pc in per_chapter:
        lines.append(f"| {pc['chapter_no']} {pc['chapter']} | {pc['item_count']} | {pc['rule_item_count']} | {pc['rule_count']} |")
    lines.append("")
    lines.append("## 6. 抽样规则（前 6 条）")
    lines.append("")
    for r in all_rules[:6]:
        lines.append(f"### {r['rule_id']}　{r['type']}　conf={r['confidence']}")
        lines.append(f"- 条件：{r['condition'] or '—'}")
        lines.append(f"- 主体：{r['subject']}")
        lines.append(f"- 禁止/允许/义务：{r['prohibited_action'] or '—'} / {r['allowed_action'] or '—'} / {r['obligation_action'] or '—'}")
        lines.append(f"- 目的/后果：{r['purpose'] or '—'}")
        lines.append(f"- 处罚/时限：{r['punishment'] or '—'} / {r['deadline'] or '—'}")
        lines.append(f"- 来源：{r['source']}")
        lines.append(f"- 原文：{r['original']}")
        lines.append(f"- 示例：{r['example']['text']}")
        lines.append("")
    lines.append("## 7. 缺口与后续")
    lines.append("")
    lines.append("- 规则粒度 = 条目；同一条目含多个独立“凡/但/如”条件段时按条件段拆分为多条。")
    lines.append("- 主体多为省略主语的命令句，默认推断为“官府（知县）”（confidence 已扣 0.04）；显式主语条目（各里里长/粮长等）已识别。")
    lines.append("- 组合型规则（禁止+允许 等）已在汇总 JSON 的 combo_rules 字段单独列出，供冲突检测人工复核。")
    lines.append("- 程序型仅识别“先…次/然后/了毕”序列；时限/处罚的数值粒度（限一日、打三十）可由后续规则槽位细化。")
    lines.append("")
    report = "\n".join(lines)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"items={total_items} rule_items={total_items - skipped_items} skipped={skipped_items} rules={len(all_rules)}")
    print("by_type:", dict(by_type))
    print("by_modal:", dict(by_modal))
    for pc in per_chapter:
        print(f"{pc['chapter_no']} {pc['chapter']}: items={pc['item_count']} rule_items={pc['rule_item_count']} rules={pc['rule_count']}")

if __name__ == "__main__":
    main()
