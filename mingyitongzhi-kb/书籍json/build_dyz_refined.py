# -*- coding: utf-8 -*-
r"""
大明一统志 卷本级精修切条器（从原文生成，逐卷处理）

用法：
    python build_dyz_refined.py 03          # 只切卷03 → 精修卷本/03_真定府.json + 打印预览
    python build_dyz_refined.py 03 22 87    # 切多卷
    python build_dyz_refined.py --all       # 全 91 卷（卷00 + 卷01-90）
    python build_dyz_refined.py 03 --dry    # 只打印不写文件

设计（全部由盘面实测得出，见 docs/样例-大明一统志-著录与结构实测.md）：
  1. 原文范围：`明一统志.txt` 行 1 起，至混入的《钦定大清一统志》卷首标记行为止（尾段整块排除并记证据）。
  2. 卷界：卷题记「明一统志卷N」变体（明/眀 × 统/統/綂）共 177 处；本器按「本卷卷题记 → 下一卷卷题记」取段，
     卷内尾重复标、`<史部,…>` 著录标、`钦定四库全书`、`明 李贤等 撰` 一律判为结构行，不入条文本但逐条登记。
  3. 条目锚点 = 「建置沿革」（两京十三司各府州卫）/「沿革」（卷89-90 外夷）在【】之外的出现——
     条题行是会缺、会粘连、会被缺字切坏的排版，门块是本书稳定的结构不变量。
  4. 条题 = 锚前裸段回找（剥 【】注与门名后最靠近锚点的名称段）；实测三种落点：名+【四至】紧贴锚、
     独立题名行、粘在上一行行尾。取不出即 title=null 并写 条题依据，取到亦逐条写 条题来源，
     边界与四至等级不合的加记 条题存疑（不猜边界）。无锚条目（卷1 京师、卷6 南京、卷7 中都）
     按独立题名行成条；「XX府下」首行是跨卷分写标记，不成条目，登记 续写 并回填母条。
  5. 一段不拉：本卷全部非结构行字符（去空白）= 各条 text（去空白）按文档序拼接，逐卷断言相等。
  6. 行级标识：每枚行锚 = 一个原文行，id 沿用联邦表现行规则 `records.local_id = <item_id>#<序号>`
     （实测 kb.sqlite：xyf '01-001#0'；装载后 uid = '<book_id>:<local_id>'），并带原文绝对行号可直查 txt。
  7. 精修：只对「同一字的旧形与通行形并存」的异体族归一到**通行形**（实测逐族登记，表见 VARIANTS）。
     本书 txt 是半成品转换本，旧形常占多数（峯>峰、竒>奇、畧>略、夀>寿、羣>群、闗>关），
     频次投票测到的是转换不彻底的程度而非字形对错，故不用频次选目标。
     私用区缺字形（PUA）保留原样并计数，绝不臆补。
"""
import io
import glob
import json
import os
import re
import sys
from collections import Counter

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
KB = os.path.dirname(HERE)
TXT = os.path.join(KB, "明一统志.txt")
OUT = os.path.join(HERE, "精修卷本")
CONTRACT = "dyz-volume/1"

CN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def cn2num(s):
    if "十" in s:
        a, b = s.split("十", 1)
        return (CN.get(a, 1) if a else 1) * 10 + (CN.get(b, 0) if b else 0)
    return CN.get(s, 0)


# 卷题记（含四种用字变体）
MARK = re.compile(r"^[明眀]一[统統綂]志卷([一二三四五六七八九十]{1,3})$")
STRUCT_EQ = {"钦定四库全书"}
AUTHOR = re.compile(r"^[明眀]?李贤等撰$")
TAILMARK = re.compile(r"^<史部.*大清一统志")

# 门名（实测封闭词表 30 个；只认行首，见 cut_sections）
MEN = ["建置沿革", "文职公署", "武职公署", "沿革", "郡名", "形胜", "风俗", "山川", "土产",
       "公署", "学校", "书院", "宫室", "关梁", "寺观", "祠庙", "陵墓", "古迹", "名宦",
       "人物", "列女", "烈女", "仙释", "流寓", "藩封", "城池", "坛庙", "山陵", "苑囿", "桥梁"]
MEN_SET = set(MEN)
ANCHOR = ("建置沿革", "沿革")          # 条目锚
# 条题尾字（地理单位）
SUFFIX = "府州县卫司国堡站驿关巡司"

# 校勘补题：卷内条目锚前无条题行，原文四至/粮行孤立残留（docs/样例-…实测.md 逐条有行号证据）
FIXED_TITLE = {
    "22": ("济南府", "行1117 山东布政司→行1118 总叙→行1119 孤立【粮…】→行1120 建置沿革，条题行整行缺失；"
                      "本卷辖境按《大明一统志》山东布政司治所与 卷23 兖州府 前之序补济南府"),
    "32": ("西安府", "陕西布政司治所，条题行整行缺失（同 卷22 型：孤立【粮…】+建置沿革）"),
    "49": ("南昌府", "江西布政司治所，条题行整行缺失（同 卷22 型）"),
    "74": ("福州府", "福建布政司治所，条题行与孤立【粮…】皆缺（同 卷22 型且更残）"),
}

# 异体族：目标一律取「通行字形」，不用本书出现频次投票。
# 原因（实测）：`明一统志.txt` 是半成品转换本——通行形与四库旧形在同一篇里并存且旧形常占多数
# （髙3254>高879、徳3415>德1217、峯1555>峰549、逺1307>远109、嵗1326>岁314、夀834>寿235、羣579>群26）。
# 频次投票测到的是「转换不彻底的程度」，不是字形对错。本书底本已是通行/简化向（無/東/書/國/歲/遠/歷/龍 全为 0），
# 残留的只是四库旧字形，故归一到通行形与全书一致，不改繁简立场。
# 只收「同一字的不同写法」；查/槎、序/庠、他/它、亦/也、洲/州、雷/溜、兖/衮 这类形近而词不同的不碰。
VARIANTS = {
    "明": ["眀"], "卫": ["衞"], "关": ["闗", "関"], "峰": ["峯"], "奇": ["竒"],
    "略": ["畧"], "宁": ["寜", "甯"], "寿": ["夀"], "岁": ["歳", "嵗"], "群": ["羣"],
    "往": ["徃"], "窗": ["窓"], "貌": ["皃"], "概": ["槩"], "真": ["眞"],
    "冒": ["冐"], "船": ["舡"], "遍": ["徧"],
    "高": ["髙"], "德": ["徳"], "为": ["爲"], "远": ["逺"], "历": ["厯"],
    "熙": ["熈"], "番": ["畨"], "峨": ["峩"], "琴": ["琹"],
}


def strip_ws(s):
    return re.sub(r"[\s\u3000]+", "", s)


def load_lines():
    raw = io.open(TXT, encoding="utf-8-sig").read()
    return raw.split("\n")


def body_end(lines):
    """明一统志正文结束行（混入的《钦定大清一统志》卷首起始行号，1 起）"""
    for i, l in enumerate(lines):
        if TAILMARK.match(l.replace("　", "").strip()):
            return i          # 0-based 切片上界
    return len(lines)


def build_refine_map(lines, end):
    """实测：各异体族在本书的行数 → 归一表（变体→通行形）+ 逐族证据"""
    text = "".join(lines[:end])
    cmap = {}
    stats = []
    for std, vs in VARIANTS.items():
        n_std = text.count(std)
        hits = [(v, text.count(v)) for v in vs if text.count(v)]
        if not hits:
            continue
        for v, _ in hits:
            cmap[v] = std
        stats.append({"通行": std, "通行形实测": n_std,
                      "改字": {v: n for v, n in hits},
                      "改字数": sum(n for _, n in hits)})
    return cmap, stats


def volume_ranges(lines, end):
    """→ [(no, head_line0, tail_line0)]；卷00=卷首（题/序/表/职名）"""
    marks = []
    for i in range(end):
        s = strip_ws(lines[i])
        m = MARK.match(s)
        if m:
            marks.append((i, cn2num(m.group(1))))
    vols = []
    first_head = marks[0][0] if marks else 0
    if first_head > 0:
        vols.append(("00", 0, first_head))
    k = 0
    while k < len(marks):
        i0, n = marks[k]
        j = k
        while j + 1 < len(marks) and marks[j + 1][1] == n:
            j += 1                      # 同卷的尾部重复标
        nxt = marks[j + 1][0] if j + 1 < len(marks) else end
        vols.append(("%02d" % n, i0, nxt))
        k = j + 1
    return vols, marks


def is_struct(s):
    return (not s) or s.startswith("<史部") or s in STRUCT_EQ or bool(MARK.match(s)) \
        or bool(AUTHOR.match(strip_ws(s)))


def depth0_mask(t):
    """【】深度：返回逐位是否在括号外（深度 0）"""
    d, mask = 0, []
    for ch in t:
        if ch == "】" and d > 0:
            d -= 1
            mask.append(False)
            continue
        mask.append(d == 0)
        if ch == "【":
            d += 1
    return mask


def find_anchors(t, mask):
    out = []
    for w in ANCHOR:
        for m in re.finditer(w, t):
            if mask[m.start()]:
                out.append((m.start(), w))
    out.sort()
    # 卷89-90 外夷只有「沿革」；「建置沿革」内含「沿革」→ 去重（同一位置只留最长的）
    ded = []
    for pos, w in out:
        if ded and pos - ded[-1][0] < len("建置沿革") and w == "沿革":
            continue
        if ded and pos == ded[-1][0]:
            continue
        ded.append((pos, w))
    return ded


NAMECH = r"[\u4e00-\u9fff\ue000-\uf8ff]"     # 汉字 + 私用区缺字形（题名常被 PUA 切开，不能只认汉字）
SUFFIX2 = SUFFIX + "所"                      # 条题尾字再收「所」（守御千户所）
BR = re.compile(r"【[^】]*】")


def sizhi(note):
    """四至括号：方位字起、含 至/抵/距/界/里。实测条目头括号用此形，山川/土产注作「在…」不成此形。"""
    return bool(re.match(r"^[东南北西]", note)) and bool(re.search(r"[至抵距界里]", note[:48]))


def blank_spans(s, spans):
    """等长置 \\x00，保住偏移（后续裸段回找要用同一套坐标）"""
    out = list(s)
    for a, b in spans:
        for k in range(a, b):
            out[k] = "\x00"
    return "".join(out)


def build_name_index(text):
    """全书「名 + 【四至】」题名索引。锚前裸段被土产/人名前粘时（实测 行尾题名串），用本索引裁出可核尾巴。"""
    idx = Counter()
    for m in re.finditer(NAMECH + r"{1,16}(?=【)", text):
        run, i = m.group(0), m.end()
        j = text.find("】", i)
        if j < 0 or not sizhi(text[i + 1:j]):
            continue
        for L in range(3, min(len(run), 12) + 1):
            if run[-L:][-1] in SUFFIX2:
                idx[run[-L:]] += 1
    return idx


def owner_before(t, mask, a_pos, prev_end, nameidx):
    """条题回找：把锚前间隙 [prev_end, a_pos) 剥成裸段，取最靠近锚点的那一段。

    实测条题有三种落点，归结为同一条规则：
      ① 名+【四至】紧贴锚（安南/于阗/叠溪守御军民千户所/开封府上）
      ② 独立题名行（西蕃/古麻刺国/百花国）
      ③ 粘在上一行行尾（罗定州/上隆州/大古刺军民宣慰使司）——上一行的前半是本条门尾
    前粘（土产串吃进名左，实测 卷87「水乳香大X州」）不猜边界：整段照收并用「条题存疑」把
    四至「自X治」与题名尾字的矛盾登记出来，交校勘处置；
    取不出、又不成题名形态，或题名与锚之间夹门名（说明该名属上一条）→ 返回 null 并写原因。
    """
    gap = t[prev_end:a_pos]
    bare = blank_spans(gap, [(m.start(), m.end()) for m in BR.finditer(gap)])
    bare = blank_spans(bare, [(m.start(), m.end())
                              for w in MEN for m in re.finditer(re.escape(w), bare)])
    m = re.search(NAMECH + r"{1,12}$", bare.rstrip("\x00 \n\r　"))
    if not m:
        return None, None, "锚前间隙剥去括号注与门名后无名称段"
    cand, cut = m.group(0), m.start()
    if cand in MEN_SET:
        return None, None, "锚前裸段 %s 是门名，不作条题" % cand
    rest = gap[cut + len(cand):]
    for w in MEN:
        for mm in re.finditer(re.escape(w), rest):
            if mask[prev_end + cut + len(cand) + mm.start()]:
                return None, None, "题名与锚之间夹门名 %s（该名属上一条的门，不夺）" % w
    nb = re.match(r"\s*【([^】]*)】", rest)
    if nb:
        if not sizhi(nb.group(1)):
            return None, None, "锚前裸段 %s 后的括号注不成四至形" % cand
        basis = "锚前四至题名（名+四至括号紧邻锚点）"
        g0 = re.search(r"自([\u4e00-\u9fff]{1,3})(?:治|城)", nb.group(1))
        if g0 and g0.group(1) != cand[-1]:
            basis += "；条题存疑：四至作「自%s治」而题名尾字为「%s」，名左或有前粘、名右或有续写标记，不猜边界" % (
                g0.group(1), cand[-1])
    elif not rest.strip("\x00 \n\r　"):
        head_part = gap[:cut].rstrip("\x00 \n\r　")
        if (not head_part or head_part.endswith("\n")) and len(cand) <= 8:
            basis = "锚前独立题名行"
        elif cand[-1] in SUFFIX2:
            basis = "锚前行尾题名串（门尾与本条条题同处一行，已按锚前裸段分家）"
        elif nameidx.get(cand):
            basis = "锚前行尾题名串（全书四至题名索引可核）"
        else:
            return None, None, "锚前裸段 %s 不成题名形态（无四至括号、非独立行、尾字不在地理单位表）" % cand
    else:
        return None, None, "题名与锚之间夹正文「%s…」，不夺" % rest.strip("\x00 \n\r　")[:12]
    return cand, prev_end + cut, basis


def cut_sections(t, start, end):
    """条内按门切 sections（门名只认行首，实测本书每门起一行）。
    sections 是不重叠平铺（契约 V3）；门下的属县/属州链另登记为 子目（可嵌套，不混进平铺）。"""
    seg = t[start:end]
    mask = depth0_mask(seg)
    cuts = []
    for w in MEN:
        for m in re.finditer(re.escape(w), seg):
            p = m.start()
            if not mask[p]:
                continue
            # 粘连行的门（不在行首）不猜，另按异常登记
            if p == 0 or seg[p - 1] == "\n":
                cuts.append((p, w))
    # 「建置沿革」里的「沿革」去掉
    cuts = [c for c in cuts if not (c[1] == "沿革" and any(x[1] == "建置沿革" and c[0] - x[0] == 4 for x in cuts))]
    cuts.sort()
    uniq = []
    for c in cuts:
        if uniq and c[0] - uniq[-1][0] < 2:
            continue
        uniq.append(c)
    secs = []
    if not uniq or uniq[0][0] > 0:
        secs.append({"kind": "条", "name": "总叙", "start": 0, "end": (uniq[0][0] if uniq else len(seg))})
    for i, (p, w) in enumerate(uniq):
        e = uniq[i + 1][0] if i + 1 < len(uniq) else len(seg)
        secs.append({"kind": "门", "name": w, "start": p, "end": e})
    # 子目：只取 建置沿革/沿革 门下的「属名【注】属名【注】」链（地理隶属，实测可核）
    subs = []
    for s in secs:
        if s["name"] not in ANCHOR:
            continue
        for m in re.finditer(r"([\u4e00-\u9fff]{1,12}?[" + SUFFIX + r"])(?=【)", seg[s["start"]:s["end"]]):
            if mask[s["start"] + m.start()] and m.group(1) != s["name"]:
                subs.append({"name": m.group(1), "门": s["name"],
                             "start": s["start"] + m.start(), "end": s["start"] + m.end()})
    return secs, subs


def build(no, head, stop, lines, cmap, nameidx):
    """核心：一卷 → 条目列表 + 覆盖/精修实测"""
    seg_lines = []
    struct = []
    for i in range(head, stop):
        raw = lines[i]
        s = raw.strip().strip("　").strip()
        if is_struct(s):
            struct.append((i + 1, s))
            continue
        seg_lines.append((i + 1, s))
    body = "\n".join(t for _, t in seg_lines)
    lineno_at = []
    line_ranges = []                      # 原文行 → body/text 坐标区间（精修逐字等长，坐标不变）
    pos = 0
    for ln, t in seg_lines:
        line_ranges.append((ln, pos, pos + len(t)))
        pos += len(t) + 1
        lineno_at.extend([ln] * len(strip_ws(t)))
    # 精修：异体归一（逐字表，长度不变）
    refine_n = 0
    chars = list(body)
    fam_of = {k: v for k, v in cmap.items()}
    for i, c in enumerate(chars):
        if c in fam_of:
            chars[i] = fam_of[c]
            refine_n += 1
    text = "".join(chars)
    mask = depth0_mask(text)
    anchors = find_anchors(text, mask)
    items = []
    fix = FIXED_TITLE.get(no.lstrip("0") or "0")
    # 两遍：① 每个锚先回找条题（拿到起点）；② 条目区间 = 本条起点 → 下一条起点。
    # 早先按「锚点→下一锚点」切，会把下一条的「条题+四至【】」整块吞进上一条，造成重复（卷02 实测 +87 字）。
    cands = []
    for k, (ap, w) in enumerate(anchors):
        prev = anchors[k - 1][0] if k else 0
        nm, st, why = owner_before(text, mask, ap, prev, nameidx)
        start = st if nm else ap
        if nm is None and k + 1 == len(anchors) and fix:
            nm = fix[0]
        cands.append((ap, w, nm, start, why))
    # 卷首块（第一条起点之前的一切）
    first_start = cands[0][3] if cands else len(text)
    head_text = text[:first_start]
    first_line = next((l.strip() for l in head_text.split("\n") if l.strip()), "")
    cont = re.match(r"^(%s{1,10})[上下]$" % NAMECH, first_line)
    if strip_ws(head_text) and not anchors and not cont and len(first_line) <= 6 and no != "00":
        # 无锚条目（实测 卷1 京师、卷6 南京、卷7 中都：独立题名行 + 总叙 + 诸门，全书只有这类条目无沿革锚）
        secs, subs = cut_sections(text, 0, len(text))
        off = text.find(first_line)
        src_line = next((ln for ln, s, e in line_ranges if s <= off < e), line_ranges[0][0])
        items.append({"id": "%s-TMP" % no, "title": first_line, "level": "item", "anchor": None,
                      "text": head_text, "sections": secs, "子目": subs, "_rng": (0, len(text)),
                      "条题来源": "独立题名行（本卷无 建置沿革/沿革 锚；实测行%d 即题名「%s」）"
                                  % (src_line, first_line)})
    elif strip_ws(head_text):
        mb = re.match(r"^(%s{2,10}布政司)$" % NAMECH, first_line)
        htitle = mb.group(1) if mb else (first_line if 0 < len(first_line) <= 6 else "卷%s 卷首" % no)
        it = {"id": "%s-000" % no, "title": htitle, "level": "volume-head", "text": head_text,
              "sections": [], "_rng": (0, first_start),
              "说明": "本卷第一条之前的文字：卷首序/布政司总叙/类目行，或跨卷续写（实测 177 处卷题记、91 卷块）"}
        if cont:
            it["续写"] = {"标记行": first_line, "母条主干": cont.group(1), "母条": None,
                          "依据": "本卷首行为「%s」：实测本书把一府分写两卷，下卷首行以此标记续写"
                                  "（卷26 行1374 开封府下、卷33 行1667 西安府下）；母条按题名主干在前卷匹配，见 母条"
                                  % first_line}
        items.append(it)
    for k, (ap, w, nm, start, why) in enumerate(cands):
        end = cands[k + 1][3] if k + 1 < len(cands) else len(text)
        if start > end:                       # 兜底：区间不倒挂
            start = end
        t = text[start:end]
        secs, subs = cut_sections(text, start, end)
        it = {"id": "%s-TMP" % no, "title": nm, "level": "item", "anchor": w,
              "text": t, "sections": secs, "子目": subs, "_rng": (start, end)}
        if nm:
            it["条题来源"] = why
        else:
            it["条题依据"] = "锚点前取不出条题（%s）；不猜，正文完整保留在 text" % (why or "无匹配")
        if fix and nm == fix[0]:
            it["条题依据"] = "校勘补题：" + fix[1]
        items.append(it)
    # 重新编号（000 之后从 001 起）
    n = 0
    for it in items:
        if it["id"].endswith("000"):
            continue
        n += 1
        it["id"] = "%s-%03d" % (no, n)
    # 行级标识：套联邦表既有规则 records.local_id = <item_id>#<序号>（实测 xyf 01-001#0）
    # 每行一枚，id 在本卷内唯一；一条若跨行、一行若被两条粘连分吃，都各自成枚且都带原文绝对行号可回查。
    straddle = 0
    for it in items:
        a, b = it.pop("_rng")
        anchors_line = []
        for j, (ln, s, e) in enumerate(line_ranges):
            if s < b and e > a:
                lo, hi = max(s, a), min(e, b)
                anchors_line.append({"id": "%s#%d" % (it["id"], len(anchors_line)),
                                     "行": ln, "start": lo - a, "end": hi - a})
                if lo != s or hi != e:
                    straddle += 1
        it["行锚"] = anchors_line
    # 覆盖断言：原文（同样做异体归一，逐字表长度不变）去空白 == 各条 text 按文档序拼接去空白
    src = strip_ws("".join(cmap.get(c, c) for c in body))
    got = strip_ws("".join(it["text"] for it in items))
    cov = {"原文字符": len(src), "入条字符": len(got), "相等": src == got}
    if not cov["相等"]:
        # 找出第一个差异位置（按行定位，便于修判据）
        for i, (a, b) in enumerate(zip(src, got)):
            if a != b:
                cov["首个差异"] = {"偏移": i, "原文": src[i:i + 40], "入条": got[i:i + 40],
                                  "行号": lineno_at[min(i, len(lineno_at) - 1)]}
                break
        else:
            cov["截断处"] = {"原文余": src[len(got):len(got) + 40]}
    # 行锚自检：枚数=原文行数（跨条行各成一枚）、id 唯一、逐行拼接字符数 = 入条字符数
    la = [x for it in items for x in it["行锚"]]
    cov["行锚"] = {"枚数": len(la), "本卷原文行": len(line_ranges), "跨条行": straddle,
                  "id唯一": len({x["id"] for x in la}) == len(la),
                  "逐行无丢": sum(len(strip_ws(it["text"][x["start"]:x["end"]]))
                                for it in items for x in it["行锚"]) == len(got),
                  # 每一行都要有下落：要么是行锚，要么是登记在 meta 的结构行
                  "行全覆盖": sorted({x["行"] for x in la} | {ln for ln, _ in struct})
                            == list(range(head + 1, stop + 1))}
    pua = sum(1 for c in body if 0xE000 <= ord(c) <= 0xF8FF)
    return items, cov, refine_n, pua, struct, seg_lines


def vol_name(no, items):
    its = [i for i in items if i["level"] == "item" and i["title"]]
    if no == "00":
        return "卷首"
    if its:
        return "、".join(i["title"] for i in its[:3]) + ("等" if len(its) > 3 else "")
    return "卷%s（无自有条目）" % no


def preview(no, items, struct, seg, cov):
    print("   ── 卷%s 结构预览（原文 %d 行 → 非结构行 %d，结构行 %d | 行锚 %s）"
          % (no, len(seg) + len(struct), len(seg), len(struct),
             json.dumps(cov["行锚"], ensure_ascii=False)))
    for ln, s in struct:
        print("      结构行 %5d │ %s" % (ln, s[:46]))
    for it in items:
        print("      %s [%s] %s %d字 行锚%d枚%s" % (it["id"], it["level"], it["title"] or "（无题）",
                                                   len(strip_ws(it["text"])), len(it["行锚"]),
                                                   "  " + it["条题依据"] if it.get("条题依据") else ""))
        for x in it["行锚"][:3] + ([] if len(it["行锚"]) <= 5 else it["行锚"][-2:]):
            print("         %s 行%-5d │ %s" % (x["id"], x["行"],
                                              strip_ws(it["text"][x["start"]:x["end"]])[:44]))
        secs = sorted(it.get("sections") or [], key=lambda x: x["start"])
        gates = [s for s in secs if s["kind"] == "门"]
        if gates:
            print("         门序:", "·".join("%s(%d)" % (g["name"], g["end"] - g["start"]) for g in gates))
        subs = it.get("子目") or []
        if subs:
            print("         子目(%d):" % len(subs), "、".join(x["name"] for x in subs[:16]) + ("…" if len(subs) > 16 else ""))
        for s in secs[:9]:
            body = strip_ws(it["text"][s["start"]:s["end"]])
            print("           ├ %s%-5s %5d %s" % (s["kind"], s["name"] or "—", s["end"] - s["start"], body[:38]))


def resolve_continuations(built):
    """跨卷分写标记回填母条：本卷首行为「XX府下」（实测 卷27 开封府下、卷33 西安府下）时，
    这块文字是前一卷同名条目（如 卷26「开封府上」）的续写，不是新条目。
    母条只按题名主干在同一批已生成的前序卷里匹配；匹不到留 null 并写未决原因，不猜。"""
    for i in range(len(built)):
        for it in built[i][3]:
            c = it.get("续写")
            if not c:
                continue
            base = c["母条主干"]
            hit = None
            pat = re.compile(r"^%s(?:[上下])?$" % re.escape(base))
            for j in range(i - 1, -1, -1):
                for p in reversed(built[j][3]):
                    if p["level"] == "item" and p["title"] and pat.match(p["title"]):
                        hit = {"卷": built[j][0], "id": p["id"], "题名": p["title"]}
                        break
                if hit:
                    break
            c["母条"] = hit
            if not hit:
                c["未决原因"] = "前序卷内无题名主干为「%s」的条目（本批只含 %d 卷；补全需 --all 重算）" % (
                    base, len(built))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    allv = "--all" in sys.argv
    dry = "--dry" in sys.argv
    show = "--preview" in sys.argv or "--dry" in sys.argv
    want = {a.zfill(2) for a in args if a.isdigit()}
    lines = load_lines()
    end = body_end(lines)
    cmap, refine_stats = build_refine_map(lines, end)
    nameidx = build_name_index("".join(cmap.get(c, c) for c in "\n".join(
        l.strip().strip("　").strip() for l in lines[:end])))
    vols, marks = volume_ranges(lines, end)
    todo = [v for v in vols if allv or v[0] in want]
    if not dry:
        os.makedirs(OUT, exist_ok=True)
    print("== 大明一统志 精修切条 | 原文行 1-%d（%d 字符）| 尾部《钦定大清一统志》卷自行 %d 起整块排除 =="
          % (end, sum(len(strip_ws(l)) for l in lines[:end]), end + 1))
    print("   卷题记 %d 处 / 卷块 %d 个 | 异体归一 %d 族 %d 字 → 通行形（全篇实测：%s）"
          % (len(marks), len(vols), len(refine_stats), sum(s["改字数"] for s in refine_stats),
             " ".join("%s←%s(%d)" % (s["通行"], "/".join(s["改字"]), s["改字数"]) for s in refine_stats)))
    built = []
    for no, head, stop in todo:
        items, cov, refine_n, pua, struct, seg = build(no, head, stop, lines, cmap, nameidx)
        built.append((no, head, stop, items, cov, refine_n, pua, struct, seg))
    resolve_continuations(built)
    for no, head, stop, items, cov, refine_n, pua, struct, seg in built:
        nm = vol_name(no, items)
        n_item = sum(1 for i in items if i["level"] == "item")
        doc = {
            "meta": {
                "书名": "大明一统志", "契约": CONTRACT, "卷号": no, "卷名": nm,
                "生成": "本文件由 书籍json/build_dyz_refined.py 从 明一统志.txt 直接切条生成（非知识层回填）",
                "原文行段": [head + 1, stop], "结构行数": len(struct),
                "结构行": [{"行": ln, "text": t} for ln, t in struct],
                "条目数": n_item, "覆盖": cov,
                "id规则": {
                    "条目": "<卷号>-<三位条号>（03-001）；03-000 = 第一条之前的卷首/无锚块，不计入条目数",
                    "行锚": "<item_id>#<条内行序>（03-001#0）——形式沿用联邦表现行规则"
                           "（实测 kb.sqlite records.local_id：xyf '01-001#0'，装载后 uid='<book_id>:<local_id>'）。"
                           "序号取条内行序而非表里的全书流水号（实测同表 01-001#0 之后是 01-007#2，跨条连号），"
                           "理由：流水号随他卷增删漂移，条内序稳定；id 带卷号+条号前缀，全书仍逐行唯一",
                    "行": "行锚的 行 字段 = 明一统志.txt 绝对行号，可直接回查原文行",
                    "子目": "条下属县/属州，用 start/end 定位在 text 内，不占 id 空间",
                    "条题": "锚前裸段回找：把锚前间隙的 【】注与门名等长置空，取最靠近锚点的名称段为本条条题。"
                            "实测条题三种落点——名+【四至】紧贴锚（安南/叠溪守御军民千户所）、独立题名行（西蕃/百花国）、"
                            "粘在上一行行尾（罗定州/大古刺军民宣慰使司）。取不出即 title=null 并写 条题依据；"
                            "取到了逐条写 条题来源，边界与四至等级不合的加记 条题存疑，不猜。"
                            "无锚条目（卷1 京师、卷6 南京、卷7 中都）按独立题名行成条；"
                            "跨卷分写的「XX府下」首行不成条目，登记为 续写 并回填母条"},
                "精修": {"异体改字": refine_n, "缺字形PUA": pua,
                         "归一表": {v: s["通行"] for s in refine_stats for v in s["改字"]},
                         "归一依据": {"实测族": refine_stats,
                                    "说明": "目标是通行字形，不按本书频次投票：txt 为半成品转换本，"
                                            "底本已是通行/简化向（無/東/書/國/歲/遠/歷 实测全为 0），"
                                            "残留的只是四库旧字形且常占多数（髙3254>高879、徳3415>德1217、"
                                            "峯1555>峰549、逺1307>远109、嵗1326>岁314），"
                                            "按频次投票等于把没转换干净的字形固化"}},
            },
            "volumes": [{"no": no, "name": nm, "file": "明一统志.txt",
                         "count": n_item, "items": items}],
        }
        path = os.path.join(OUT, "%s_%s.json" % (no, re.sub(r'[\\/:*?"<>|]', "_", nm)[:40]))
        la = cov["行锚"]
        und = [i["id"] for i in items if i["level"] == "item" and not i["title"]]
        dbt = [i["id"] for i in items if "条题存疑" in (i.get("条题来源") or "")]
        good = (cov["相等"] and la["id唯一"] and la["逐行无丢"] and la["行全覆盖"]
                and la["枚数"] >= la["本卷原文行"] - la["跨条行"])
        print("%s卷%s %-26s 条%3d 字符%d/%d 行锚%d枚(跨条%d) 精修%d字 PUA%d 结构行%d 无题%d 存疑%d"
              % ("OK " if good else "!! ", no, nm[:26], n_item, cov["入条字符"], cov["原文字符"],
                 la["枚数"], la["跨条行"], refine_n, pua, len(struct), len(und), len(dbt)))
        if not cov["相等"]:
            print("     差异:", json.dumps(cov.get("首个差异") or cov.get("截断处"), ensure_ascii=False))
        if und or dbt:
            print("     条题 无题:%s 存疑:%s" % (",".join(und) or "-", ",".join(dbt) or "-"))
        if show:
            preview(no, items, struct, seg, cov)
        if not dry:
            for old in glob.glob(os.path.join(OUT, "%s_*.json" % no)):
                if old != path:
                    os.remove(old)      # 题名改动会换文件名；旧名是同一卷的上一版，留着就是重复入账
            with io.open(path, "w", encoding="utf-8") as f:
                json.dump(doc, f, ensure_ascii=False, indent=1)
    if dry:
        print("（--dry 未写文件）")
    else:
        print("输出目录:", os.path.relpath(OUT, KB))


if __name__ == "__main__":
    main()
