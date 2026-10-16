# -*- coding: utf-8 -*-
r"""
《物理夜航船：直觉与猜算》OCR layout.json → guji 书籍json 契约（book-json/1.1）

源   : MinerU 风格 PDF OCR 解析输出，**两份 layout.json** 拼合为整书
       A: printed 1-176   （OCR 200 页，偏移 -23）  第 1-6 章（6.2 节中途）
       B: printed 177-365 （OCR 189 页，偏移 -177） 6.2 节余下 + 6.3 + 第 7-9 章 + 附录 + 译后记
       两文件在印刷页 176/177 处**首尾相接**（A 末页 176 与 B 首页 177 同属 6.2 节，无缺口无重叠）
       书名原文 Fly by Night Physics: How Physicists Use the Backs of Envelopes
       著 [美] 徐一鸿 (A. Zee) / 译 姬扬 / 世界图书出版有限公司北京分公司 2024.10
       ISBN 978-7-5232-1686-6
输出 : <OUT>/<书名>_校对版.json + <OUT>/分卷json/NN_<卷名>.json
       OUT 默认 E:\git\ToolBox\guji\yehangchuan\书籍json
       两份 layout.json 放置于 yehangchuan/_source/layout_A.json、layout_B.json

结构定位（关键：不靠正则找章号，靠目录页 + 印刷页码偏移）
  * A 偏移 -23、B 偏移 -177（各自由 page_number 块实测，偏移恒定）
  * 两份源先按「印刷页」归一到同一坐标系，再统一走章/节定位
  * 章隔页版式不统一：第 4 章隔页无「第4章」字样（首块 title 即章名）；第 1/3 章章号与章名分属两块

条目口径
  * 一个「节」（1.1 / 1.2 … / 6.2）或一个独立标题为一条 item
  * title = 所属层级标题（最近的小节/小标题）
  * text  = 正文全文（含公式 LaTeX）
  * 公式  : 行内 inline_equation → $...$；行间 interline_equation → 独立成段 $$...$$
"""
import io
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)

# OCR 源放 <根>/yehangchuan/_source/（按仓库规则 **/_source/** 不入仓，重跑前需自行放置）
SRC_A = os.path.join(ROOT, "yehangchuan", "_source", "layout_A.json")
SRC_B = os.path.join(ROOT, "yehangchuan", "_source", "layout_B.json")
DEFAULT_OUT = os.path.join(ROOT, "yehangchuan", "书籍json")

BOOK = "物理夜航船"
BOOK_ID = "yhc"
CONTRACT = "book-json/1.1"

# 两份源：印刷页 = OCR 页 + offset。A 覆盖 1-176，B 覆盖 177-365。
SOURCES = [
    {"tag": "A", "path": SRC_A, "offset": -23, "span": (1, 176)},
    {"tag": "B", "path": SRC_B, "offset": 177, "span": (177, 365)},
]
TOC_OCR_A = (4, 5, 6)       # 目录页：A 的 OCR 4-6（印刷 i-x 与正文起始）
LAST_PRINTED = 365


def load(path):
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def save(path, doc):
    with io.open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)


def safe_name(s):
    return re.sub(r'[\\/:*?"<>|]', "_", s)


# ---------------------------------------------------------------- 文本抽取

def spans_text(block):
    """块内所有 span 的 content 顺序拼接，行内公式包 $...$"""
    out = []
    for line in block.get("lines", []):
        for sp in line.get("spans", []):
            c = sp.get("content", "")
            if not c:
                continue
            if sp.get("type") == "inline_equation":
                c = "$" + c.strip() + "$"
            out.append(c)
    return "".join(out)


def block_text(block):
    t = block.get("type")
    if t == "interline_equation":
        raw = spans_text(block).strip()
        if raw.startswith("$") and raw.endswith("$"):     # 已是行内包裹
            raw = raw[1:-1].strip()
        return "$$" + raw + "$$"
    if t in ("image", "table", "chart"):
        return ""
    return spans_text(block)


def page_blocks(page):
    """按阅读顺序取 preproc_blocks（para_blocks 有 56 页与之不一致，弃用）"""
    bl = page.get("preproc_blocks") or []
    return sorted(bl, key=lambda b: (b.get("index") if b.get("index") is not None else 0))


# ---------------------------------------------------------------- 双源载入

def load_pages():
    """把两份 layout.json 归一到同一「印刷页」坐标系。

    返回 (by_printed, toc_pages)
      by_printed : {印刷页: page_dict}，两份源各自按 offset 平移后合并
      toc_pages  : 目录页 page_dict 列表（来自 A，印刷号为负/零，单独返回）
    """
    by_printed = {}
    toc_pages = []
    for s in SOURCES:
        doc = load(s["path"])
        off = s["offset"]
        lo, hi = s["span"]
        n_in = 0
        for p in doc["pdf_info"]:
            ocr = p.get("page_idx")
            printed = ocr + off
            if printed < lo or printed > hi:
                # 低于 lo 的是前置页（印刷 <=0），只在 A 里收作目录/前置
                if s["tag"] == "A" and printed < lo:
                    if ocr in TOC_OCR_A:
                        toc_pages.append(p)
                    by_printed.setdefault(printed, p)
                continue
            if printed in by_printed and s["tag"] == "A":
                continue          # B 优先（衔接页以 B 为准由下方 span 决定）
            by_printed[printed] = p
            n_in += 1
        print("  源%s 偏移%+d 覆盖印刷页 %d-%d，收 %d 页" % (s["tag"], off, lo, hi, n_in))
    return by_printed, toc_pages


def printed_pages_sorted(by_printed):
    return sorted(by_printed)


# ---------------------------------------------------------------- 目录（印刷页号 → 章节）

TOC_OCR_PAGES = (4, 5, 6)
_re_sec = re.compile(r"^(\d+\.\d+)\s*(.*)$")
_re_chp = re.compile(r"^第(\d+)章\s*(.*)$")
# 附录/后置：附录Cp / 附录 Del / 附录 FSW …；以及无编号后置篇目
_re_app = re.compile(r"^附录\s*([A-Za-z]+)\s*[:：]\s*(.*)$")
_re_back = re.compile(r"^(生卒年|部分练习解答|推荐阅读|译后记.*|索引|致谢|后记)$")


def parse_toc(pages):
    """从目录页解析 [(级别, 编号, 标题, 印刷页, 目录出现序)]

    目录每页是一个大 text 块，块内以 \\n 分行；先拆行再逐行解析。
    级别：1=章(第N章)  2=节(N.M)  3=附录  4=后置篇目(生卒年/练习解答/推荐阅读/译后记…)
    前三条无页码或页码为罗马数字（i / iii / xi），会被跳过，由前置卷另行处理。
    """
    lines = []
    for p in pages:
        for b in page_blocks(p):
            for ln in block_text(b).split("\n"):
                if ln.strip():
                    lines.append(ln.strip())

    rows, order = [], 0
    for raw in lines:
        t = re.sub(r"[.\u00b7\u2026\s]{2,}", " ", raw).strip()
        if not t:
            continue
        nums = re.findall(r"(\d+)\s*$", t)
        if not nums:
            continue
        page_no = int(nums[-1])
        head = t[: len(t) - len(nums[-1])].strip().rstrip(".．\u00b7\u2026 ")
        if not head:
            continue
        order += 1
        m = _re_sec.match(head)
        if m:
            rows.append((2, m.group(1), m.group(2).strip(), page_no, order))
            continue
        m = _re_chp.match(head)
        if m:
            rows.append((1, m.group(1), m.group(2).strip(), page_no, order))
            continue
        m = _re_app.match(head)
        if m:
            rows.append((3, m.group(1), m.group(2).strip() or m.group(1), page_no, order))
            continue
        s = norm_txt(head)
        if _re_back.match(s):
            rows.append((4, s, s, page_no, order))
            continue
    return rows


# ---------------------------------------------------------------- 主抽取

def build_structure(toc_rows):
    """目录 → [{unit}, ...]

    每项 unit：
      {"kind":"ch"|"app"|"back", "no", "title", "page", "order", "sections":[...]}
    章（kind=ch）带 sections（目录里的 N.M 节，供正文按节切分）；
    附录/后置（app/back）自成一条 unit，不隶属任何章。
    级别映射：1=章 2=节 3=附录 4=后置篇目
    """
    units = []
    for lvl, no, title, page, order in toc_rows:
        if lvl == 2:
            if units and units[-1]["kind"] == "ch":
                units[-1]["sections"].append(
                    {"no": no, "title": title, "page": page, "order": order})
            continue
        units.append({"kind": {1: "ch", 3: "app", 4: "back"}[lvl],
                      "no": no, "title": title, "page": page, "order": order,
                      "sections": []})
    return units


def chapter_start_ocr(ch):
    """章隔页所在 OCR 页 = 印刷页 + |偏移|（印刷页 = OCR 页 + PAGE_OFFSET，OFFSET=-23）"""
    return ch["page"]


# ---------------------------------------------------------------- 正文分段

# 章隔页上的「章名」块会紧跟章号出现，需识别并并入章标题
CHAPTER_HEAD_RE = re.compile(r"^第(\d+)章\s*(.*)$")
SECTION_HEAD_RE = re.compile(r"^(\d+\.\d+)\s*(.+)$")
APP_HEAD_RE = re.compile(r"^附录\s*([A-Za-z]+)\s*[:：]\s*(.*)$")


def is_chapter_divider_page(page, ch):
    """判断该印刷页是否为第 ch 章的章隔页。

    章隔页版式不统一（见勘察结论），需多路判据：
      1) 出现「第N章」标题块（第1/2/3/5/6/7/9章）
      2) 出现该章章名块且同页列出 >=2 条该章节标题（第4章无「第4章」字样、
         第8章无 title 块，章名落成 text 块）
    """
    ch_no = int(ch["no"])
    want = title_key(ch["title"])
    has_head = False
    has_name = False
    sec_hits = 0
    for b in page_blocks(page):
        t = block_text(b).strip()
        m = CHAPTER_HEAD_RE.match(t)
        if m and int(m.group(1)) == ch_no:
            has_head = True
        if want and title_key(t).startswith(want):
            has_name = True
        ms = SECTION_HEAD_RE.match(t)
        if ms and ms.group(1).split(".")[0] == str(ch_no):
            sec_hits += 1
    if has_head:
        return True
    return has_name and sec_hits >= 2


def norm_txt(s):
    return re.sub(r"[\s\u3000]+", "", s or "")


def title_key(s):
    return norm_txt(s).replace("：", ":").replace("，", ",")


def collect_units(by_printed, units):
    """按印刷页顺序收集 (印刷页, block)，并切分「章 / 附录 / 后置篇目」区间。

    返回 (front_units, [ (unit, div_units, body_units) ])
      front_units : 第一个章隔页之前的全部块（前置内容）
      div_units   : 该章/篇首页的块（章隔页或附录首页）
      body_units  : 区间内其余块
    """
    pgs = printed_pages_sorted(by_printed)
    last = pgs[-1]

    # 章节候选：章 + 附录 + 后置篇目（三者都会开启新卷）
    tops = [u for u in units if u["kind"] in ("ch", "app", "back")]
    tops.sort(key=lambda u: u["order"])

    # 定位每个 top 的起始印刷页（用目录页号，再校验/微调）
    for u in tops:
        guess = u["page"]
        found = None
        if guess in by_printed and (u["kind"] != "ch" or is_chapter_divider_page(by_printed[guess], u)):
            found = guess
        else:
            for i in range(max(0, guess - 3), min(last, guess + 4) + 1):
                if i not in by_printed:
                    continue
                if u["kind"] == "ch":
                    if is_chapter_divider_page(by_printed[i], u):
                        found = i
                        break
                else:
                    if _page_has_top_head(by_printed[i], u):
                        found = i
                        break
        if found is None:
            print("  [WARN] %s%s 首页未定位到（目录印刷页 %s）" % (
                "第" + u["no"] + "章" if u["kind"] == "ch" else u["kind"] + " " + u["no"],
                "", u["page"]))
            found = guess
        if found != guess:
            print("  [校正] %s 起页 印刷 %d（目录 %d）" % (
                u["no"], found, guess))
        u["start"] = found

    for i, u in enumerate(tops):
        u["end"] = tops[i + 1]["start"] if i + 1 < len(tops) else last + 1

    # 前置卷：印刷页 <= 第一个 top 起页-1（含负号/零号前置页）
    front_units = []
    first_start = tops[0]["start"]
    for i in pgs:
        if i >= first_start:
            continue
        for b in page_blocks(by_printed[i]):
            front_units.append((i, b))

    out = []
    for u in tops:
        div_units, body_units = [], []
        for i in pgs:
            if i < u["start"] or i >= u["end"]:
                continue
            for b in page_blocks(by_printed[i]):
                (div_units if i == u["start"] else body_units).append((i, b))
        out.append((u, div_units, body_units))
    return front_units, out


def _page_has_top_head(page, u):
    """附录/后置篇目的首页：出现同名的 title/text 块"""
    key = title_key(u["title"])
    for b in page_blocks(page):
        t = norm_txt(block_text(b))
        if not t:
            continue
        if key and key in t:
            return True
        m = APP_HEAD_RE.match(t)
        if m and m.group(1).lower() == str(u["no"]).lower():
            return True
    return False


def split_sections(body_units, c):
    """按节标题（N.M 前缀）切分章正文；返回 [ (sec_dict, [units]) ]

    c["sections"] 是目录里该章的节清单（顺序即目录顺序）。
    正文里出现的 N.M 标题块若在该清单内即开新节；不在清单内则并回当前节。
    """
    by_no = {s["no"]: s for s in c.get("sections", [])}

    cur = None
    groups = []
    for (pi, b) in body_units:
        t = block_text(b).strip()
        m = SECTION_HEAD_RE.match(t) if b.get("type") == "title" else None
        if m and m.group(1) in by_no:
            s = dict(by_no[m.group(1)])
            cur = {"sec": s, "units": [(pi, b)]}
            groups.append(cur)
            continue
        if cur is not None:
            cur["units"].append((pi, b))
    return groups


def units_to_text(units):
    """把块序列拼成正文；行间公式独立成段，段落用换行分隔"""
    parts = []
    for _, b in units:
        t = block_text(b)
        if not t or not t.strip():
            continue
        btype = b.get("type")
        if btype == "interline_equation":
            parts.append("\n" + t.strip() + "\n")
        else:
            parts.append(t.strip())
    # 合并：同一段内的块用空格连接，公式已有换行
    out = []
    for p in parts:
        if p.startswith("\n"):
            out.append(p)
        else:
            if out and not out[-1].endswith("\n"):
                out.append("")
            out.append(p)
    s = "\n".join(x for x in out if x != "")
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


# ---------------------------------------------------------------- 组装与落盘

META = {
    "书名": BOOK,
    "版本": "校对版",
    "底本": "PDF 扫描本 OCR（MinerU 3.4.4 hybrid 解析，两份 layout.json 拼合：印刷页 1-176 与 177-365，"
            "覆盖全书正文、第 1-9 章、12 个附录、生卒年、部分练习解答、推荐阅读、译后记；"
            "原书页眉页脚与页码块未收入正文）",
    "item_id规则": "NN-NNN（卷号两位-条号三位，卷内 001 起连续）",
    "条字段": "id/title/text/level",
    "契约": CONTRACT,
    "book_id": BOOK_ID,
    "著者": "[美] 徐一鸿（A. Zee）",
    "译者": "姬扬",
    "朝代": None,
    "体裁": "科普（物理学夜航船/信封背面估算）",
    "成书年": None,
    "出版": "世界图书出版有限公司北京分公司 2024.10",
    "ISBN": "978-7-5232-1686-6",
    "原名": "Fly by Night Physics: How Physicists Use the Backs of Envelopes",
    "卷划分": "00=前置内容（封面/版权/目录/中译本序言/序言/量纲和基本常数）；01-09=第1-9章；"
              "10=附录与后置（附录 Cp/Del/Eg/ENS/FSW/Gal/Gr/Grp/L/M/N/VdW、生卒年、部分练习解答、推荐阅读、译后记）",
    "抽取依据": "码页标定：印刷页 = OCR page_idx + 偏移（源A 偏移 -23、源B 偏移 +177，各由 page_number 块实测且恒定）；"
                "两份源在印刷页 176/177 处首尾相接（同属 6.2 节，无缺口无重叠）；"
                "章/节/附录边界取自目录页（源A OCR 4-6，目录含全书至译后记）并在对应页校验命中",
    "源文件": "layout.json ×2（MinerU OCR 原始输出，源A 200 页 / 源B 189 页）",
}


def front_items(front_units):
    """前置内容 → 条目（按标题切分）

    退化情形：标题块后面直接跟另一个标题块（该标题下无正文，如「序言」「自然单位」），
    此时把标题挂到下一个有正文的条目上，避免出现 title==text 的空壳条。
    """
    segs = []
    cur_title, cur_units = None, []
    for pi, b in front_units:
        t = block_text(b).strip()
        if b.get("type") == "title" and t:
            if cur_units:
                segs.append((cur_title, cur_units))
            cur_title, cur_units = t, []
            continue
        cur_units.append((pi, b))
    if cur_units:
        segs.append((cur_title, cur_units))

    # 倒序合并：正文为空的段，其标题并入后一段标题（用「·」标记这是两个标题的并置，
    # 原书此处是两个连续标题块，中间无正文）
    out = []
    for title, units in reversed(segs):
        txt = units_to_text(units).strip()
        if not txt:
            if out:
                prev = out[-1][0]
                joined = title if not prev else (prev + "·" + title)
                out[-1] = (joined, out[-1][1], out[-1][2])
            continue
        out.append((title, txt, units))
    out.reverse()

    items = []
    for title, txt, _u in out:
        if not txt:
            continue
        items.append((title or "前置内容", txt))
    return items


def build(items_front, tops_out, all_toc):
    volumes = []

    # ---- 卷 00：前置内容
    v0_items = [{"id": "00-%03d" % (i + 1), "title": t, "text": x, "level": "item"}
                for i, (t, x) in enumerate(items_front)]
    if v0_items:
        volumes.append({"no": "00", "file": "00_前置内容.txt",
                        "name": "前置内容", "count": len(v0_items), "items": v0_items})

    # ---- 卷 01-09：各章；卷 10：附录与后置
    #   章：按节切条（首条并入章隔页内容）
    #   附录/后置篇目：整篇一条（不按节切，它们本身即一篇）
    back_items = []
    for u, div_units, body_units in tops_out:
        kind = u["kind"]
        if kind == "ch":
            no = "%02d" % int(u["no"])
            ch_name = "第%s章 %s" % (u["no"], u["title"])
            sec_groups = split_sections(body_units, u)
            div_txt = units_to_text(div_units).strip()
            items = []
            for g in sec_groups:
                sec = g["sec"]
                txt = units_to_text(g["units"])
                if not txt.strip():
                    continue
                items.append({"id": "", "title": sec["title"], "text": txt,
                              "level": "item", "section": sec["no"]})
            if not items:
                continue
            # 章隔页内容并入本章首条正文（不另立 -000 兜底条：
            # validate_book_json.py 第 75 行要求 条目总数 == 全部 items 数，
            # 而 book_json_augment.py V2 会把 -000 条排除，二者不可兼得）
            if div_txt:
                first = items[0]
                first["text"] = div_txt + "\n\n" + first["text"]
                first["title"] = ch_name
            for i, it in enumerate(items, 1):
                it["id"] = no + "-%03d" % i
            volumes.append({"no": no, "file": "%s_%s.txt" % (no, safe_name(u["title"])),
                            "name": ch_name, "count": len(items), "items": items})
        else:
            # 附录 / 后置篇目：整篇一条，title 用篇名，并入卷 10
            txt = units_to_text(div_units + body_units).strip()
            if not txt:
                continue
            back_items.append({"id": "", "title": u["title"], "text": txt,
                               "level": "item", "kind": kind, "no": u["no"]})

    if back_items:
        no = "10"
        for i, it in enumerate(back_items, 1):
            it["id"] = no + "-%03d" % i
        volumes.append({"no": no, "file": "10_附录与后置.txt",
                        "name": "附录与后置", "count": len(back_items), "items": back_items})
    return volumes


def write_out(out, volumes):
    # 剥离抽取期脚手架字段（kind/no 仅用于建卷期排序，section 由 title 体现）
    ITEM_KEYS = ("id", "title", "text", "level")
    for v in volumes:
        v["items"] = [{k: it[k] for k in ITEM_KEYS if k in it} for it in v["items"]]

    doc = {
        "meta": dict(META),
        "卷数": len(volumes),
        "条目总数": sum(len(v["items"]) for v in volumes),
        "volumes": volumes,
    }
    os.makedirs(out, exist_ok=True)
    whole = os.path.join(out, BOOK + "_校对版.json")
    save(whole, doc)

    vdir = os.path.join(out, "分卷json")
    os.makedirs(vdir, exist_ok=True)
    for f in os.listdir(vdir):
        if f.endswith(".json"):
            os.remove(os.path.join(vdir, f))
    for v in volumes:
        name = v.get("name") or v["file"].replace(".txt", "")
        fn = "%s_%s.json" % (v["no"], safe_name(name))
        save(os.path.join(vdir, fn), {"meta": dict(META), "volumes": [v]})

    # 全文纯文本：既是人读底本，也让 book_json_augment.digitize 能量到「数字化」
    srcdir = os.path.join(os.path.dirname(out), "_source")
    os.makedirs(srcdir, exist_ok=True)
    lines, n = [], 0
    for v in volumes:
        for it in v["items"]:
            n += 1
            lines.append(it["text"])
    with io.open(os.path.join(srcdir, BOOK + ".txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("纯文本底座：%s（%d 段）" % (os.path.join(srcdir, BOOK + ".txt"), n))

    return whole, doc


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT
    print("出 : %s" % out)

    by_printed, toc_pages = load_pages()
    pgs = printed_pages_sorted(by_printed)
    print("合并后印刷页 %d..%d（共 %d 页）" % (pgs[0], pgs[-1], len(pgs)))

    toc_rows = parse_toc(toc_pages)
    units = build_structure(toc_rows)
    n_ch = sum(1 for u in units if u["kind"] == "ch")
    n_app = sum(1 for u in units if u["kind"] == "app")
    n_back = sum(1 for u in units if u["kind"] == "back")
    n_sec = sum(len(u["sections"]) for u in units)
    if not units:
        raise SystemExit("目录解析失败")
    print("目录：%d 章 / %d 节 / %d 附录 / %d 后置篇目" % (n_ch, n_sec, n_app, n_back))

    front_units, tops_out = collect_units(by_printed, units)
    print("前置块数 %d" % len(front_units))

    items_front = front_items(front_units)
    volumes = build(items_front, tops_out, toc_rows)

    print("\n卷：")
    for v in volumes:
        print("  %s 条=%-4d  %s  <- %s" % (
            v["no"], v["count"], v.get("name"), v["file"]))

    whole, doc = write_out(out, volumes)
    print("\n写出：%s" % whole)
    print("卷数=%d 条目总数=%d" % (doc["卷数"], doc["条目总数"]))
    empty = [it["id"] for v in volumes for it in v["items"] if not it["text"].strip()]
    if empty:
        print("空 text 条目 %d 个：%s" % (len(empty), empty[:10]))


if __name__ == "__main__":
    main()
