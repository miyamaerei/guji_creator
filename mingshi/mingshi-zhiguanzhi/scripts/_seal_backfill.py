# -*- coding: utf-8 -*-
"""v11-① 印信回填（ORG.seal）

原文依据：礼部条「凡诸司之印信，领其制度。」之后的一整段（约 900 字），
逐条给出「机构清单 → 印信类型 → 钮式 → 尺寸 → 篆文」。

原文形态（节录）：
  宗人府、五军都督府，俱正一品，银印，三台，方三寸四分，厚一寸。
  六部都察院、各都司，俱正二品，银印，二台，方三寸二分，厚八分。
  ……
  各州县儒学、仓库、驿递、闸坝批验所、抽分竹木局、河泊所、织染局、
  税课局、阴阳学、医学、僧正司、道正司、僧会司、道会司，俱未入流，
  铜条记，阔一寸三分，长二寸五分，厚二分一厘。
  已上俱直纽，九叠篆文。
  监察御史，铜印，直纽，有眼，方一寸五分，厚三分，八叠篆文。
  总制、总督、巡抚并镇守、公差等官，铜关防，直纽，阔一寸九分五厘，
  长二寸九分，厚三分，九叠篆文。

设计要点：
  1. 该段是「一份清单对应一个印信规格」，清单内用「、」分隔、以「，俱/，」收束；
  2. 规格串内可能自带括注（如内阁「(内阁，银印，直纽，方一寸七分，厚六分，玉箸篆文。)」）；
  3. 「已上俱直纽，九叠篆文」是**先前所有条目的公共钮式与篆文**，须回填；
  4. 机构名须与 ORG 树节点名归一匹配（如「各都司」→ 都指挥使司、
     「各布政司」→ 承宣布政使司），匹配不上的**不填**（宁缺毋滥）。
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import _common as C
import _kg_enums as E

# ---- 机构名归一：原文清单用词 → ORG 树节点名 ----
# 只做**有明确对应**的映射；无对应者不填
ALIAS = {
    "各都司": "都指挥使司",
    "各布政司": "承宣布政使司",
    "各按察司": "提刑按察使司",
    "各盐运司": "都转运盐使司",
    "各卫": "卫指挥使司",
    "京卫": "京卫指挥使司",
    "各卫千户所": "千户所",
    "各卫百户所": "百户所",
    # 原文简称 → 树节点全称（实测差异：原文用紧缩史名，树用规范全称）
    "通政司":      "通政使司",
    "五城兵马司":  "五城兵马指挥司",
    "顺天":        "顺天府",
    "应天":        "应天府",
    "大兴":        "大兴县",
    "宛平":        "宛平县",
    "上元":        "上元县",
    "江宁":        "江宁县",
    "张真人":      "正一真人",
    "国子监绳愆厅": "国子监",
    "王府长史司典簿厅": "王府长史司",
    # 原文清单里用「X、Y」并列但树上是**独立节点**者，由 SPLIT_JOINED 处理；
    # 以下为原文紧缩形 → 树全称
    "吏户礼兵刑工六部": "六部",          # 兜底，实际走 LIUBU 展开
    "各府":        "府",
    "各州县儒学":  "儒学",
    "各府卫儒学":  "儒学",
    "仓库":        "仓",
    "驿递":        "驿",
    "闸坝批验所":  "批验所",
    "河道":        None,               # 非机构，忽略
    "守御":        None,
}

# ---- 原文把多个独立机构并列成一个 token（无「、」分隔），须拆开 ----
SPLIT_JOINED = {
    "六科行人司":       ["六科", "行人司"],
    "京卫武学":         ["京卫", "武学"],
    "鸿胪寺各署":       ["鸿胪寺"],
    "鸿胪寺各府":       ["鸿胪寺"],
    "各府卫儒学":       ["儒学"],
    "各州县儒学":       ["儒学"],
    "各府儒学":         ["儒学"],
    "各卫儒学":         ["儒学"],
    "上林苑监各署":     ["上林苑监"],
    "王府纪善":         ["王府长史司"],
    "王府审理所":       ["王府长史司"],
    "僧纲司道纪司":     ["僧纲司", "道纪司"],
    "僧正司":           ["僧纲司"],
    "道正司":           ["道纪司"],
    "僧会司":           ["僧纲司"],
    "道会司":           ["道纪司"],
    # 原文用**史名**、树用**规范全称**（实测差异清单）
    "留守司":           ["留守司"],           # 树上有「留守司」节点
    "宣慰司":           ["宣慰使司"],
    "宣抚司":           ["宣抚司"],
    "招讨司":           ["招讨司"],
    "安抚司":           ["安抚司"],
    "长官司":           ["长官司"],
    "各布政司":         ["承宣布政使司"],
    "各按察司":         ["提刑按察使司"],
    "各盐运司":         ["都转运盐使司"],
    "各州":             ["州"],
    "各县":             ["县"],
    "各府":             ["府"],
    "仓":               ["仓"],
    "织染局":           ["织染杂造局"],
    "税课局":           ["税课司"],
    "僧纲司":           ["僧纲司"],
    "道纪司":           ["道纪司"],
    "阴阳学":           ["阴阳学"],
    "医学":             ["医学"],
    "税课司":           ["税课司"],
    "僧录司":           ["僧录司"],
    "道录司":           ["道录司"],
    "会同馆":           ["会同馆"],
    "教坊司":           ["教坊司"],
    "文思院":           ["文思院"],
    # 末轮：原文清单里的「X司狱司 / X经历司 / X照磨所」等**下属衙门**，
    # 树上是「X」节点的子节点或未建节点 → 映射到父机构（印信随本衙）
    "留守司司狱司":     ["留守司"],
    "宣抚司经历司":     ["宣抚司"],
    "顺天":             ["顺天府"],
    "应天":             ["应天府"],
    "应天二府":         ["应天府"],
    "各布政司照磨所":   ["承宣布政使司"],
    "各都司经历司":     ["都指挥使司"],
    "各都司司狱司":     ["都指挥使司"],
    "各按察司经历司":   ["提刑按察使司"],
    "各按察司照磨所":   ["提刑按察使司"],
    "各府经历司":       ["府"],
    "各府照磨所":       ["府"],
    "各卫经历司":       ["卫指挥使司"],
    "王府长史司典簿厅": ["王府长史司"],
    "都察院经历司":     ["都察院"],
    "都察院各照磨所":   ["都察院"],
    "都察院各司狱司":   ["都察院"],
    "大理寺左右司":     ["大理寺"],
    "鸿胪寺主簿厅":     ["鸿胪寺"],
    "鸿胪寺各署":       ["鸿胪寺"],
    "钦天监主簿厅":     ["钦天监"],
    "国子监绳愆厅":     ["国子监"],
    "国子监典籍厅":     ["国子监"],
    "博士厅":           ["国子监"],
    "典簿厅":           ["国子监"],
    "工部营缮所":       ["工部"],
    "兵部典牧所":       ["兵部"],
    "户部照磨所":       ["户部"],
    "刑部司狱司":       ["刑部"],
    "园马寺":           ["苑马寺"],
    "苑马寺":           ["苑马寺"],
    "各盐运司":         ["都转运盐使司"],
    "盐运司":           ["都转运盐使司"],
    # 土司系列：原文用「宣慰司/宣抚司/招讨司/安抚司/长官司」（无「使」字）
    "宣慰司":           ["宣慰使司"],
    "招讨司":           ["招讨司"],
    "安抚司":           ["安抚司"],
    # 末轮（v11 收口）：源表用近义/下属衙门名，树用规范全称。
    # 实测命中依据已逐条核原文，无依据的一律**不加**（宁缺毋滥）。
    "河泊所闸坝官":     ["河泊所", "闸坝批验所"],
    "僧纲司道纪司":     ["僧纲司", "道纪司"],
    "市舶提举司":       ["市舶司"],
    "宣慰使司":         ["宣慰司"],
    "道":               ["各道"],          # 源表「各道」未见 → 保持未命中
    "内府诸库房厂":     ["内府宝钞等各库"],
}
# 需要拆分的复合项（一个清单元素含多个机构）
SPLIT = {
    "六部都察院": ["六部", "都察院"],
    "各府卫儒学": ["各府儒学", "各卫儒学"],
}


def _norm_name(raw):
    """去掉修饰前缀「各/诸/俱」等，返回候选节点名列表。"""
    raw = raw.strip()
    if not raw:
        return []
    if raw in SPLIT_JOINED:
        # 拆分结果仍须过 ALIAS（如「各府卫儒学」→儒学 /
        # 「各州县儒学」→儒学），否则别名不生效
        out = []
        for x in SPLIT_JOINED[raw]:
            out.extend([x] + ([ALIAS[x]] if ALIAS.get(x) else []))
        return list(dict.fromkeys(out))
    if raw in SPLIT:
        return SPLIT[raw]
    cands = []
    if raw in ALIAS and ALIAS[raw]:
        cands.append(ALIAS[raw])
    cands.append(raw)
    # 「各X」→「X」；「各A、B」已在切分阶段处理
    if raw.startswith("各") or raw.startswith("诸"):
        cands.append(raw[1:])
        cands.append(raw[1:] + "司" if not raw[1:].endswith("司") else raw[1:])
    # 「X司」↔「X」
    if raw.endswith("司"):
        cands.append(raw[:-1])
    else:
        cands.append(raw + "司")
    return [c for c in dict.fromkeys(cands) if c]


# ---- 「总制、总督、巡抚并镇守、公差等官」→ 铜关防：须映射到全部差遣类节点 ----
# 原文该组是**差遣官**的统一规格，凡 ORG.level == "差遣" 的节点均适用。
QIANCE_SEAL = {"type": "铜关防", "knob": "直纽", "size": "阔一寸九分五厘/长二寸九分",
               "thickness": "厚三分", "script": "九叠篆文"}
# 「六部」是缩写，须展开为实际节点名
LIUBU = ["吏部", "户部", "礼部", "兵部", "刑部", "工部"]


def parse_seal_clauses(text):
    """返回 [ {orgs:[原始机构名…], seal:{…}, raw:…, line_no:N} ]"""
    m = re.search(r"凡诸司之印信，领其制度。", text)
    if not m:
        return []
    # 段末标志：「外国王印三等」之后与本段无关
    seg_start = m.end()
    seg_end = text.find("外国王印三等", seg_start)
    if seg_end < 0:
        seg_end = seg_start + 2000
    seg = text[seg_start:seg_end]

    # 公共钮式/篆文：段末「已上俱直纽，九叠篆文。」
    common_knob, common_script = "未明", "未明"
    cm = re.search(r"已上俱(直纽|虎纽|三台|二台)，(九叠篆文|八叠篆文|玉箸篆文|柳叶篆文)", seg)
    if cm:
        common_knob, common_script = cm.group(1), cm.group(2)

    out = []
    # 段首括注：原文首条为「(内阁，银印，直纽，方一寸七分，厚六分，玉箸篆文。)」，
    # 括号内自带句号，须**先摘出**再对其余部分按「。」切句。
    pm0 = re.match(r"^[(（]([^)）]+)[)）]", seg)
    if pm0:
        inner = pm0.group(1).rstrip("。")
        toks = [t.strip() for t in inner.split("，") if t.strip()]
        out.append({"orgs": [toks[0]] if toks else [],
                    "seal": parse_spec(toks[1:]),
                    "raw": inner,
                    "knob_default": "未明", "script_default": "未明"})
        seg = seg[pm0.end():]

    parts = [p.strip() for p in seg.split("。") if p.strip()]

    for part in parts:
        part = part.strip()
        if not part or "已上俱" in part or "外国王印" in part:
            continue

        # 括注型：主语在括号内。首组为「(内阁，银印，……。)」——
        # 整段以「(」开头，故 part 首字符是「(」，需先剥壳。
        pm = re.match(r"^[(（]([^)）]+)[)）]$", part)
        if pm:
            inner = pm.group(1)
            toks = [t.strip() for t in inner.split("，") if t.strip()]
            orgs = [toks[0]] if toks else []
            spec = parse_spec(toks[1:])
            out.append({"orgs": orgs, "seal": spec, "raw": inner,
                        "knob_default": common_knob, "script_default": common_script})
            continue

        # 普通型：以「，」切开，前段为机构清单，后段为规格。
        #
        # 复合句（v11 修）：原文常见「A、B、C，俱正三品，D、E，俱从三品，铜印…」——
        # 两个品级组共享同一印信规格。旧版只取第一个「俱X品」之前的机构，
        # D、E 整组被丢弃（实测 苑马寺、宣慰司、招讨司、安抚司 全部漏采）。
        # 判据：句内出现 **≥2 个「俱X品」** ⟹ 按「俱X品」切段，逐段独立登记。
        toks = [t.strip() for t in part.split("，") if t.strip()]
        if len(toks) < 2:
            continue
        spec_word = re.compile(r"^(银印|铜印|铜关防|铜条记|金印|镀金印)$")
        grade_word = re.compile(r"^[正从][一二三四五六七八九]品$|^未入流$|^俱")
        # 复合句判定：spec 词之前的「俱X品」个数 ≥2
        spec_pos = next((i for i, t in enumerate(toks) if spec_word.match(t)), len(toks))
        grade_marks = [i for i, t in enumerate(toks)
                       if i < spec_pos and grade_word.match(t)]
        if len(grade_marks) >= 2:
            # 首段可能**无品级标记**（如「A、B、王府审理所，俱正六品，…」），
            # 须把 spec 词之前、首个标记之前的 token 作为独立首段并入。
            gidx = grade_marks
            if grade_marks[0] > 0:
                lead = toks[:grade_marks[0]]
                lead_orgs = [o.strip() for o in "、".join(lead).split("、") if o.strip()]
                lead_orgs = [re.sub(r"^俱.*?品$|^[正从][一二三四五六七八九]品$|^未入流$",
                                    "", o).strip() for o in lead_orgs]
                lead_orgs = [o for o in lead_orgs if o]
                if lead_orgs:
                    out.append({"orgs": lead_orgs,
                                "seal": parse_spec(toks[grade_marks[0]:spec_pos]
                                                   + toks[spec_pos:]),
                                "raw": part,
                                "knob_default": common_knob,
                                "script_default": common_script})
            for gi, gstart in enumerate(gidx):
                gend = gidx[gi + 1] if gi + 1 < len(gidx) else spec_pos
                seg_toks = toks[gstart:gend]
                if not seg_toks:
                    continue
                gtxt = seg_toks[0]
                org_txt = "、".join(seg_toks[1:])
                orgs = [o.strip() for o in org_txt.split("、") if o.strip()]
                orgs = [re.sub(r"^俱.*?品$|^[正从][一二三四五六七八九]品$|^未入流$",
                               "", o).strip() for o in orgs]
                orgs = [o for o in orgs if o]
                if not orgs:
                    continue
                spec = parse_spec([gtxt] + toks[spec_pos:])
                out.append({"orgs": orgs, "seal": spec, "raw": part,
                            "knob_default": common_knob,
                            "script_default": common_script})
            continue

        # 单一品级型：机构清单 = 规格起点前的所有 token
        idx = None
        for i, t in enumerate(toks):
            if spec_word.match(t) or grade_word.match(t) or t == "俱正一品":
                idx = i
                break
        if idx is None or idx == 0:
            continue
        org_txt = "、".join(toks[:idx])
        # 机构清单里可能混入「俱X品」的品级标注
        orgs = [o.strip() for o in org_txt.split("、") if o.strip()]
        orgs = [re.sub(r"^俱.*?品$|^[正从][一二三四五六七八九]品$|^未入流$", "", o).strip()
                for o in orgs]
        orgs = [o for o in orgs if o]
        spec = parse_spec(toks[idx:])
        out.append({"orgs": orgs, "seal": spec, "raw": part,
                    "knob_default": common_knob, "script_default": common_script})
    return out


def parse_spec(toks):
    """从规格 token 列表解析 seal 字典。"""
    s = {"type": "未明", "knob": "未明", "size": "未明",
         "thickness": "未明", "script": "未明"}
    joined = "，".join(toks)
    for t in toks:
        if t in E.SEAL_TYPES:
            s["type"] = t
        elif t in ("直纽", "虎纽"):
            s["knob"] = t
        elif t in ("三台", "二台"):
            s["knob"] = t
        elif t == "有眼":
            s["knob"] = "有眼"
        elif t in E.SEAL_SCRIPTS:
            s["script"] = t
        # 厚度必须在尺寸之前判，否则「厚一寸」的「一寸」会被尺寸正则吃掉
        if re.match(r"^厚[一-龥]+分", t) or re.match(r"^厚[一-龥]+寸$", t):
            s["thickness"] = t
        elif re.match(r"^方[一-龥]+分(厘)?$", t) or re.match(r"^方[一-龥]+寸$", t):
            s["size"] = t
        elif re.match(r"^(阔|长)[一-龥]+分(厘)?$", t):
            s["size"] = (s["size"] + "/" + t) if s["size"] != "未明" else t
    return s


def collect_seal_map(text, orgs=None):
    """机构名 → seal dict（已归一）。

    orgs: 传入 ORG 节点名列表时，额外处理两类**非字面匹配**：
      (a) 「六部」展开为吏户礼兵刑工六部；
      (b) 差遣类（ORG.level=="差遣"）统一适用「总制、总督、巡抚并镇守、公差等官」的铜关防。
    """
    out = {}
    for cl in parse_seal_clauses(text):
        seal = dict(cl["seal"])
        if seal["knob"] == "未明" and cl["knob_default"] != "未明":
            seal["knob"] = cl["knob_default"]
        if seal["script"] == "未明" and cl["script_default"] != "未明":
            seal["script"] = cl["script_default"]
        for raw in cl["orgs"]:
            # 「六部都察院」这类复合项：先看是否含「六部」
            if "六部" in raw:
                for b in LIUBU:
                    out.setdefault(b, seal)
                rest = raw.replace("六部", "").strip()
                if rest:
                    for nm in _norm_name(rest):
                        out.setdefault(nm, seal)
                continue
            for nm in _norm_name(raw):
                out.setdefault(nm, seal)
    return out


def apply_qiance_seal(orgs, smap):
    """差遣类节点统一适用铜关防（原文「总制、总督、巡抚并镇守、公差等官」）。"""
    n = 0
    for o in orgs:
        if o.get("level") == "差遣" and o["name"] not in smap:
            smap[o["name"]] = dict(QIANCE_SEAL)
            n += 1
    return n


def apply_nanjing_seal(orgs, smap):
    """南京官印信随北京（原文第 04-001 条「南京官品秩，俱同北京」）。

    实现：剥掉名称前缀「南京」，用北京同名节点查 seal。
    北京侧无同名者（如 南京总督粮储 / 南京提督操江）→ 不填。
    """
    n = 0
    for o in orgs:
        nm = o["name"]
        if not nm.startswith("南京") or nm in smap:
            continue
        bj = nm[2:]
        # 「南京五城兵马司」→ 北京侧「五城兵马指挥司」须走 ALIAS
        cands = [bj] + _norm_name(bj)
        for c in dict.fromkeys(cands):
            if c in smap:
                s = dict(smap[c])
                s["inherited_from"] = c          # 标记来源，可溯源
                smap[nm] = s
                n += 1
                break
    return n


def backfill(orgs, reg, errs):
    """给 ORG 记录回填 seal。返回 (命中数, 映射表大小, 差遣补充数)。"""
    text = "\n".join(t for _, t in C.read_source_lines())
    smap = collect_seal_map(text)
    nq = apply_qiance_seal(orgs, smap)
    nj = apply_nanjing_seal(orgs, smap)

    hit = 0
    for o in orgs:
        seal = smap.get(o["name"])
        if seal is None:
            continue
        s = dict(seal)
        s["confidence"] = 0.85
        # 校验枚举合法性（越界即报，防手误）
        for k, enum in (("type", E.SEAL_TYPES), ("knob", E.SEAL_KNOBS),
                        ("script", E.SEAL_SCRIPTS)):
            if s.get(k) not in enum:
                errs.append("%s seal.%s 越界: %s" % (o.get("item_id"), k, s.get(k)))
        o["seal"] = s
        hit += 1
    return hit, len(smap), (nq, nj)


if __name__ == "__main__":
    text = "\n".join(t for _, t in C.read_source_lines())
    cls = parse_seal_clauses(text)
    print("解析到印信条目 %d 组" % len(cls))
    tot = 0
    for cl in cls:
        tot += len(cl["orgs"])
        print("  [%s] %s" % ("/".join(cl["orgs"][:4]) + ("…" if len(cl["orgs"]) > 4 else ""),
                             cl["seal"]))
    print("机构名合计 %d" % tot)
    smap = collect_seal_map(text)
    print("归一后唯一机构名 %d" % len(smap))
