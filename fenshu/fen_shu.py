# -*- coding: utf-8 -*-
"""
《焚书》（[明]李贽 著，张建业 译注，中华书局《中华经典名著全本全注全译》丛书）
EPUB 结构化工具

功能：
  1. parse      拆分为带标记的分卷 TXT + 结构化 JSON（含校对报告）
  2. 篇目       按卷列出篇目
  3. 原文       按卷/篇只拿原文
  4. 题解       拿某篇的写作背景（题解）
  5. 注释       按篇取段落对应词的解释，或按关键词全书检索
  6. 译文       按篇取对应译文（可只看第 N 段）
  7. 检索       在原文/题解/注释/译文中全文检索

用法示例：
  python fen_shu.py parse
  python fen_shu.py 原文 --卷 卷一 --输出 原文_卷一.txt
  python fen_shu.py 原文 --篇 童心说
  python fen_shu.py 题解 --篇 童心说
  python fen_shu.py 注释 --篇 答周西岩 --锚 ①
  python fen_shu.py 注释 --词 生知
  python fen_shu.py 译文 --篇 童心说 --段 1
  python fen_shu.py 检索 --词 童心
"""
import argparse
import datetime
import glob
import io
import json
import os
import re
import sys
import zipfile
from html.parser import HTMLParser

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BASE = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE, "焚书_结构化.json")
TXT_DIR = os.path.join(BASE, "分卷txt")
YUANWEN_DIR = os.path.join(BASE, "原文txt")
REPORT_PATH = os.path.join(BASE, "校对报告.txt")

BOOK_TITLE = "焚书"
VOL_LABELS = {  # 卷号 -> (卷名, 文件前缀)
    "卷一": ("书答", "卷一_书答"),
    "卷二": ("书答", "卷二_书答"),
    "卷三": ("杂述", "卷三_杂述"),
    "卷四": ("杂述", "卷四_杂述"),
    "卷五": ("读史", "卷五_读史"),
    "卷六": ("诗", "卷六"),
}

NOTE_KEY_RE = re.compile(
    r"^(?P<key>[①-⑳]|\(\d{1,2}\)|（\d{1,2}）)\s*[:：]?\s*(?P<rest>.*)$"
)
MARKER_RE = re.compile(r"^【(.+?)】$")


# ---------------------------------------------------------------------------
# 1. HTML 块解析
# ---------------------------------------------------------------------------
class Block:
    __slots__ = ("tag", "cls", "text", "sups", "bold", "anchor")

    def __init__(self, tag, cls, text, sups, bold, anchor):
        self.tag = tag
        self.cls = cls
        self.text = text
        self.sups = sups      # sup 标注文本（如 ①、②、(21)）
        self.bold = bold      # 是否含 <b>
        self.anchor = anchor  # h1/h2/h3 的 id（如 b001）

    def __repr__(self):
        return f"<{self.tag} class={self.cls!r} text={self.text[:20]!r}>"


class HtmlBlocks(HTMLParser):
    """把 HTML 正文抽成有序块列表，sup 文本原样内联并单独记录。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []
        self._cur = None
        self._cls = ""
        self._id = None
        self._parts = []  # (is_sup, text)
        self._bold = False
        self._sup = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("h1", "h2", "h3", "p"):
            self._cur = tag
            self._cls = a.get("class", "")
            self._id = a.get("id")
            self._parts = []
            self._bold = False
            self._sup = 0
        elif tag == "b" and self._cur:
            self._bold = True
        elif tag == "sup" and self._cur:
            self._sup += 1
        elif tag == "br" and self._cur:
            self._parts.append((False, "\n"))

    def handle_endtag(self, tag):
        if tag == "sup" and self._cur:
            self._sup = max(0, self._sup - 1)
        elif tag in ("h1", "h2", "h3", "p") and self._cur == tag:
            text = "".join(t for _, t in self._parts)
            sups = [t for s, t in self._parts if s]
            if text.strip() or sups:
                self.blocks.append(
                    Block(tag, self._cls, text.strip(), sups, self._bold, self._id)
                )
            self._cur = None

    def handle_data(self, data):
        if self._cur is not None and data:
            self._parts.append((self._sup > 0, data))


def parse_blocks(path):
    with io.open(path, encoding="utf-8") as f:
        raw = f.read()
    p = HtmlBlocks()
    p.feed(raw)
    return p.blocks, raw


def get_title(raw):
    m = re.search(r"<title>(.*?)</title>", raw, re.S)
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------------------
# 2. 结构化组装（原文 + 题解 + 注释 + 译文）
# ---------------------------------------------------------------------------
def parse_note(text):
    """把一条注释拆成 {key, term, text}。"""
    m = NOTE_KEY_RE.match(text)
    if m:
        key = m.group("key")
        rest = m.group("rest")
    else:
        key = None
        rest = text
    # 词头：取第一个全角/半角冒号前的短词（≤6 字）作为“词”
    head = rest.split("：", 1)[0].split(":", 1)[0].strip()
    term = head if 0 < len(head) <= 6 else None
    return {"key": key, "term": term, "text": rest}


def strip_trailing_sups(text, sups):
    """去掉标题末尾的 sup 标注，如 “答澹然师①” -> “答澹然师”。"""
    for s in reversed(sups):
        if text.endswith(s):
            text = text[: -len(s)].rstrip()
    return text


class Unit:
    __slots__ = ("seq", "original", "anchors", "notes", "translation")

    def __init__(self, seq):
        self.seq = seq
        self.original = []      # 原文段
        self.anchors = []       # 每原文段的 sup 标注列表（按段）
        self.notes = []         # [{key, term, text}]
        self.translation = []   # 译文段

    def empty(self):
        return not (self.original or self.notes or self.translation)

    def to_dict(self, align):
        return {
            "seq": self.seq,
            "原文": self.original,
            "标注": self.anchors,
            "注释": self.notes,
            "译文": self.translation,
            "对齐": align,
        }


class StructBuilder:
    """把“卷/篇/子篇 + 题解/原文/注释/译文”流式组装成树。"""

    def __init__(self, root_kind="volume"):
        self.root_kind = root_kind  # volume | article（自序用）
        self.volumes = []           # root_kind=volume
        self.front_article = None   # root_kind=article
        self.cur_vol = None
        self.cur_article = None
        self.cur_sub = None
        self.mode = None            # None | 题解 | 注释 | 译文
        self.pending = None
        self.seq = 0
        self.article_seq = 0
        self.warnings = []

    # -- 基础操作 ------------------------------------------------------------
    def _new_unit(self):
        self.seq += 1
        self.pending = Unit(self.seq)

    def _flush(self):
        if self.pending and not self.pending.empty():
            target = self.cur_sub if self.cur_sub is not None else self.cur_article
            if target is not None:
                n_o, n_t = len(self.pending.original), len(self.pending.translation)
                align = "1:1" if (n_o and n_t and n_o == n_t) else "整体"
                target["units"].append(self.pending.to_dict(align))
        self._new_unit()

    def _target(self):
        return self.cur_sub if self.cur_sub is not None else self.cur_article

    # -- 事件 ----------------------------------------------------------------
    def on_h1(self, text):
        self._flush()
        self.mode = None
        if self.root_kind == "volume":
            m = re.match(r"(卷[一二三四五六])(?:\s*(.*))?$", text)
            no = m.group(1) if m else text
            rest = (m.group(2) or "").strip() if m else ""
            self.cur_vol = {"no": no, "name": rest, "full": text, "articles": []}
            self.volumes.append(self.cur_vol)
            self.cur_article = None
            self.cur_sub = None
        else:
            self.article_seq += 1
            art = {
                "id": f"fm-a{self.article_seq:02d}",
                "title": text,
                "title_anchors": [],
                "ti_jie": [],
                "units": [],
                "sub_articles": [],
            }
            self.front_article = art
            self.cur_article = art
            self.cur_sub = None

    def on_h2(self, text, sups, anchor):
        self._flush()
        self.mode = None
        self.article_seq += 1
        vol = self.cur_vol if self.root_kind == "volume" else None
        no = vol["no"] if vol else "卷首"
        if vol and no.startswith("卷") and len(no) == 2:
            j = "一二三四五六".index(no[1]) + 1
        else:
            j = "0"
        art = {
            "id": f"j{j}-{self.article_seq:03d}",
            "title": strip_trailing_sups(text, sups),
            "title_anchors": list(sups),
            "anchor": anchor,
            "ti_jie": [],
            "units": [],
            "sub_articles": [],
        }
        if vol:
            vol["articles"].append(art)
        else:
            self.front_article = art
        self.cur_article = art
        self.cur_sub = None

    def on_h3(self, text, sups, anchor):
        self._flush()
        self.mode = None
        self.article_seq += 1
        sub = {
            "id": f"{self.cur_article['id']}-{len(self.cur_article['sub_articles']) + 1:02d}",
            "title": strip_trailing_sups(text, sups),
            "title_anchors": list(sups),
            "anchor": anchor,
            "ti_jie": [],
            "units": [],
            "sub_articles": [],
        }
        self.cur_article["sub_articles"].append(sub)
        self.cur_sub = sub

    def on_marker(self, name):
        if name == "题解":
            self._flush()
            self.mode = "题解"
        elif name in ("注释", "译文"):
            # 注释/译文都归属当前单元；单元在下一个原文段/标题/题解出现时闭合
            self.mode = name
        else:
            self.mode = None

    def on_original(self, text, sups):
        if self.pending and (self.pending.notes or self.pending.translation):
            self._flush()
        self.mode = None
        self.pending.original.append(text)
        self.pending.anchors.append(list(sups))

    def on_content(self, text, sups):
        target = self._target()
        if self.mode == "题解":
            if sups:
                # 源书特例：诗序/诗行等原文段丢失了【原文】标记，直接跟在题解后
                self.mode = None
                who = target["title"] if target else "?"
                self.warnings.append(f"题解区带标注段按原文处理：《{who}》 | {text[:30]}…")
                self.on_original(text, sups)
                return
            if target is not None:
                target["ti_jie"].append(text)
        elif self.mode == "注释":
            note = parse_note(text)
            if note["key"] is None:
                self.warnings.append(
                    f"注释无序号标记：{target and target['title'] or '?'} | {text[:40]}"
                )
            self.pending.notes.append(note)
        elif self.mode == "译文":
            self.pending.translation.append(text)
        else:
            # 无小节标记：紧跟原文段的 block1 视为原文续段（长诗跨行等情况）
            if (
                self.pending
                and self.pending.original
                and not (self.pending.notes or self.pending.translation)
            ):
                self.pending.original.append(text)
                self.pending.anchors.append(list(sups))
            elif target is not None:
                target.setdefault("body", []).append(text)

    def finish(self):
        self._flush()
        if self.cur_vol and self.root_kind == "volume":
            # 卷六的 h2 是诗体类别（自身无正文、只有子篇）-> 标记 type=category
            for art in self.cur_vol["articles"]:
                if not art["units"] and not art["ti_jie"] and art["sub_articles"]:
                    art["type"] = "category"
                else:
                    art.setdefault("type", "article")


# ---------------------------------------------------------------------------
# 3. 通读文件 -> 文档模型
# ---------------------------------------------------------------------------
def list_part_files():
    epub = None
    hits = glob.glob(os.path.join(BASE, "*.epub"))
    if hits:
        epub = hits[0]
    return epub


def iter_parts():
    """按文件名顺序产出 (序号, 路径, 块列表, 原始html)。"""
    epub = list_part_files()
    if epub is None:
        raise FileNotFoundError("目录下未找到 *.epub 文件")
    with zipfile.ZipFile(epub) as z:
        names = sorted(
            n for n in z.namelist() if re.fullmatch(r"text/part\d{4}\.html", n)
        )
        for n in names:
            raw = z.read(n).decode("utf-8")
            p = HtmlBlocks()
            p.feed(raw)
            m = re.search(r"part(\d+)\.html", n)
            yield int(m.group(1)), n, p.blocks, raw


FRONT_NAMES = {
    0: "书名页",
    1: "版权页",
    2: "目录",
    3: "李贽论",
    4: "凡例",
    5: "自序",
}


def build_document():
    doc = {
        "meta": {
            "书名": BOOK_TITLE,
            "作者": "李贽",
            "译注者": "张建业",
            "版本": "中华书局《中华经典名著全本全注全译》丛书（全二册），2018年7月",
            "来源": list_part_files(),
            "生成时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "结构": "卷 -> 篇(h2) -> 子篇(h3) -> 单元{原文段s, 注释, 译文段s}；题解为各篇写作背景",
        },
        "front_matter": [],
        "volumes": [],
        "appendices": [],
    }

    sb = StructBuilder(root_kind="volume")
    warnings = []
    front_warnings = []
    front_seq = 0
    appendix_builder = None
    cur_appendix = None
    appendix_title = None

    for idx, name, blocks, raw in iter_parts():
        title = get_title(raw)

        if idx <= 5:  # 卷首
            if idx == 5:  # 自序：走结构化流程
                sb2 = StructBuilder(root_kind="article")
                for b in blocks:
                    _feed_structured(sb2, b, warnings)
                sb2.finish()
                front_warnings.extend(sb2.warnings)
                doc["front_matter"].append(
                    {
                        "id": f"fm-{front_seq + 1:02d}",
                        "title": "自序",
                        "type": "annotated",
                        "source": name,
                        "article": sb2.front_article,
                    }
                )
                front_seq += 1
            else:
                paras = [b.text for b in blocks if b.tag == "p"]
                doc["front_matter"].append(
                    {
                        "id": f"fm-{front_seq + 1:02d}",
                        "title": FRONT_NAMES.get(idx, title),
                        "type": "preface" if idx == 3 else "plain",
                        "source": name,
                        "paragraphs": paras,
                    }
                )
                front_seq += 1
            continue

        # 正文 / 附录
        if idx == 218:  # 封底（空页，HTML 头部误带附录二标题）
            doc["appendices"].append(
                {"title": "封底", "source": name, "articles": [], "paragraphs": []}
            )
            continue
        if blocks and blocks[0].tag == "h1" and (
            blocks[0].text.startswith("附录") or blocks[0].text == "封底"
        ):
            # 开启/切换附录
            appendix_title = blocks[0].text
            appendix_builder = {"title": appendix_title, "source": name, "articles": [], "paragraphs": []}
            doc["appendices"].append(appendix_builder)
            cur_appendix = None
            for b in blocks[1:]:
                _feed_appendix(appendix_builder, b, cur_appendix)
            continue

        if appendix_builder is not None and blocks and blocks[0].tag == "h1":
            pass  # 卷标题不会出现在附录之后；防御分支

        # 常规卷内正文
        for b in blocks:
            _feed_structured(sb, b, warnings)

    sb.finish()
    doc["volumes"] = sb.volumes
    doc["warnings"] = sb.warnings + front_warnings

    # 卷名补全
    for vol in doc["volumes"]:
        no = vol["no"]
        if no in VOL_LABELS:
            vol["name"] = VOL_LABELS[no][0]
    return doc


def _feed_structured(sb, b, warnings):
    if b.tag == "h1":
        sb.on_h1(b.text)
    elif b.tag == "h2":
        sb.on_h2(b.text, b.sups, b.anchor)
    elif b.tag == "h3":
        sb.on_h3(b.text, b.sups, b.anchor)
    elif b.tag == "p":
        m = MARKER_RE.match(b.text)
        if m and b.cls == "calibre1":
            sb.on_marker(m.group(1))
        elif b.cls == "calibre1":
            sb.on_original(b.text, b.sups)
        elif b.cls in ("block1", "block"):
            sb.on_content(b.text, b.sups)
        else:
            sb.on_content(b.text)  # 兜底：归为正文内容


def _feed_appendix(app, b, cur):
    """附录：center(加粗)=篇题，block=作者，block1=正文行。"""
    if b.tag == "h1":
        return
    if b.tag == "p" and b.cls == "center" and b.bold and b.text:
        art = {"title": strip_trailing_sups(b.text, b.sups), "author": None, "paragraphs": []}
        app["articles"].append(art)
        return art
    if app["articles"]:
        art = app["articles"][-1]
        if b.cls == "block" and art["author"] is None and b.text:
            art["author"] = b.text
            return art
        if b.tag == "p" and b.text:
            art["paragraphs"].append(b.text)
            return art
    if b.tag == "p" and b.text:
        app["paragraphs"].append(b.text)
    return None


# ---------------------------------------------------------------------------
# 4. TXT 渲染
# ---------------------------------------------------------------------------
def render_units(units, out):
    for u in units:
        if u["原文"]:
            out.append("【原文】")
            for para in u["原文"]:
                out.append(para)
                out.append("")
            out.pop()
        if u["注释"]:
            out.append("【注释】")
            for n in u["注释"]:
                out.append(f"{n['key'] or ''}{n['text']}")
            out.append("")
        if u["译文"]:
            out.append("【译文】")
            for para in u["译文"]:
                out.append(para)
            out.append("")


def render_article(art, out, level=0):
    lab = "【子篇】" if level else "【篇】"
    out.append(f"{lab}{art['title']}")
    if art.get("ti_jie"):
        out.append("【题解】")
        for p in art["ti_jie"]:
            out.append(p)
        out.append("")
    render_units(art["units"], out)
    for sub in art["sub_articles"]:
        out.append("")
        render_article(sub, out, level + 1)


def build_txt(doc):
    os.makedirs(TXT_DIR, exist_ok=True)

    # ---- 卷首 ----
    head = ["=" * 46, f"《{BOOK_TITLE}》卷首", "=" * 46, ""]
    for fm in doc["front_matter"]:
        head.append(f"【{fm['title']}】")
        if fm["type"] == "annotated":
            render_article(fm["article"], head, 0)
        else:
            for p in fm["paragraphs"]:
                head.append(p)
            head.append("")
    with io.open(os.path.join(TXT_DIR, "卷首.txt"), "w", encoding="utf-8-sig") as f:
        f.write("\n".join(head))

    # ---- 各卷 ----
    for vol in doc["volumes"]:
        no = vol["no"]
        prefix = VOL_LABELS.get(no, (no, no.replace(" ", "_")))[1]
        out = ["=" * 46, f"《{BOOK_TITLE}》分卷 · {vol['full']}", "=" * 46, ""]
        for art in vol["articles"]:
            out.append("")
            render_article(art, out, 0)
        with io.open(os.path.join(TXT_DIR, f"{prefix}.txt"), "w", encoding="utf-8-sig") as f:
            f.write("\n".join(out))

    # ---- 附录 ----
    for app in doc["appendices"]:
        out = ["=" * 46, f"《{BOOK_TITLE}》{app['title']}", "=" * 46, ""]
        if app["paragraphs"]:
            out.extend(app["paragraphs"])
            out.append("")
        for art in app["articles"]:
            out.append("")
            out.append(f"【篇】{art['title']}")
            if art["author"]:
                out.append(f"【作者】{art['author']}")
            out.append("")
            out.extend(art["paragraphs"])
            out.append("")
        safe = app["title"].replace(" ", "_")
        with io.open(os.path.join(TXT_DIR, f"{safe}.txt"), "w", encoding="utf-8-sig") as f:
            f.write("\n".join(out))


def build_yuanwen_txt(doc):
    """仅原文的分卷 TXT。"""
    os.makedirs(YUANWEN_DIR, exist_ok=True)
    for vol in doc["volumes"]:
        no = vol["no"]
        prefix = VOL_LABELS.get(no, (no, no.replace(" ", "_")))[1]
        out = ["=" * 46, f"《{BOOK_TITLE}》原文 · {vol['full']}", "=" * 46, ""]

        def walk(art):
            out.append(f"【篇】{art['title']}")
            for u in art["units"]:
                for para in u["原文"]:
                    out.append(para)
                    out.append("")
                out.pop()
            for sub in art["sub_articles"]:
                out.append("")
                walk(sub)

        for art in vol["articles"]:
            out.append("")
            walk(art)
        with io.open(os.path.join(YUANWEN_DIR, f"{prefix}_原文.txt"), "w", encoding="utf-8-sig") as f:
            f.write("\n".join(out))


# ---------------------------------------------------------------------------
# 5. 校对报告
# ---------------------------------------------------------------------------
def build_report(doc):
    lines = [f"《{BOOK_TITLE}》解析校对报告", "=" * 46, ""]
    total_articles = total_subs = total_units = 0
    issues = []
    for vol in doc["volumes"]:
        for art in vol["articles"]:
            total_articles += 1
            for u in art["units"]:
                total_units += 1
                n_o, n_n, n_t = len(u["原文"]), len(u["注释"]), len(u["译文"])
                if n_o and n_t and n_o != n_t:
                    issues.append(
                        f"[段数不对齐] {vol['no']}《{art['title']}》单元{u['seq']}：原文{n_o}段 / 译文{n_t}段"
                    )
                if n_o and not n_t:
                    issues.append(
                        f"[无译文] {vol['no']}《{art['title']}》单元{u['seq']}：有原文{n_o}段，无译文"
                    )
            for sub in art["sub_articles"]:
                total_subs += 1
                for u in sub["units"]:
                    total_units += 1
                    n_o, n_t = len(u["原文"]), len(u["译文"])
                    if n_o and n_t and n_o != n_t:
                        issues.append(
                            f"[段数不对齐] {vol['no']}《{art['title']}·{sub['title']}》单元{u['seq']}：原文{n_o}段 / 译文{n_t}段"
                        )
                    if n_o and not n_t:
                        issues.append(
                            f"[无译文] {vol['no']}《{art['title']}·{sub['title']}》单元{u['seq']}：有原文{n_o}段，无译文"
                        )
    lines.append(f"卷数：{len(doc['volumes'])}　篇数：{total_articles}　子篇数：{total_subs}　单元数：{total_units}")
    lines.append(f"卷首条目：{len(doc['front_matter'])}　附录：{len(doc['appendices'])}")
    lines.append("")
    lines.append("— 结构提示（诗歌卷多原文段对一译文属正常；散文篇如出现请人工核对） —")
    for it in issues:
        lines.append(it)
    lines.append("")
    lines.append("— 解析告警 —")
    for w in doc.get("warnings", []):
        lines.append(w)
    if not issues and not doc.get("warnings"):
        lines.append("（无）")
    with io.open(REPORT_PATH, "w", encoding="utf-8-sig") as f:
        f.write("\n".join(lines))
    return lines


# ---------------------------------------------------------------------------
# 6. 查询
# ---------------------------------------------------------------------------
def load_doc():
    if not os.path.exists(JSON_PATH):
        doc = build_document()
        save_doc(doc)
        return doc
    with io.open(JSON_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_doc(doc):
    with io.open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)


def norm_vol(s):
    s = (s or "").strip()
    if not s:
        return None
    s = s.replace(" ", "")
    if s.startswith("卷") and " " not in s and len(s) <= 3:
        return s
    if re.fullmatch(r"[1-6]", s):
        return "卷" + "一二三四五六"[int(s) - 1]
    # 形如 “卷一 书答” 全名
    m = re.match(r"(卷[一二三四五六])", s)
    return m.group(1) if m else None


def find_articles(doc, title, vol=None):
    """返回 (卷显示名, article, 是否子篇, 父篇) 列表。"""
    hits = []

    def scan(articles, volname):
        for art in articles:
            if title and title in art["title"]:
                hits.append((volname, art, False, None))
            for sub in art["sub_articles"]:
                if title and title in sub["title"]:
                    hits.append((volname, sub, True, art))

    vno = norm_vol(vol)
    for vol in doc["volumes"]:
        if vno and vol["no"] != vno:
            continue
        scan(vol["articles"], vol["full"])
    if not vno or vno == "卷首":
        for fm in doc["front_matter"]:
            if fm["type"] == "annotated":
                a = fm["article"]
                if title and title in a["title"]:
                    hits.append(("卷首", a, False, None))
    if not title:
        return hits
    return hits


def pick(hits, vol=None):
    if not hits:
        return None, "未找到匹配篇目"
    if len(hits) > 1:
        names = [f"{v}《{a['title']}》" for v, a, _, _ in hits]
        return None, "匹配到多篇：" + "、".join(names[:10]) + "（请用 --卷 或更精确的 --篇 限定）"
    return hits[0], None


def out_write(text, path=None):
    if path:
        with io.open(path, "w", encoding="utf-8-sig") as f:
            f.write(text)
        print(f"已写入：{path}")
    else:
        print(text)


# ---------------------------------------------------------------------------
# 7. CLI
# ---------------------------------------------------------------------------
def cmd_parse(_):
    doc = build_document()
    save_doc(doc)
    build_txt(doc)
    build_yuanwen_txt(doc)
    report = build_report(doc)
    print("解析完成：")
    print("  JSON    ->", JSON_PATH)
    print("  分卷TXT ->", TXT_DIR)
    print("  原文TXT ->", YUANWEN_DIR)
    print("  校对    ->", REPORT_PATH)
    print()
    print("\n".join(report))


def cmd_mulu(args):
    doc = load_doc()
    vno = norm_vol(args.卷)
    for vol in doc["volumes"]:
        if vno and vol["no"] != vno:
            continue
        print(f"【{vol['full']}】")
        for art in vol["articles"]:
            print("  " + art["title"])
            for sub in art["sub_articles"]:
                print("      └ " + sub["title"])


def cmd_yuanwen(args):
    doc = load_doc()
    vno = norm_vol(args.卷)
    if args.篇:
        hits = find_articles(doc, args.篇, args.卷)
        hit, err = pick(hits, args.卷)
        if err:
            print(err)
            return
        volname, art, is_sub, parent = hit
        out = [f"《{BOOK_TITLE}》{volname} {art['title']}（原文）", ""]

        def walk(a):
            out.append(f"【{a['title']}】")
            for u in a["units"]:
                for p in u["原文"]:
                    out.append(p)
            out.append("")

        if is_sub:
            walk(art)
        else:
            for u in art["units"]:
                for p in u["原文"]:
                    out.append(p)
            out.append("")
            for sub in art["sub_articles"]:
                out.append("")
                walk(sub)
        out_write("\n".join(out), args.输出)
    else:
        # 整卷原文
        parts = []
        for vol in doc["volumes"]:
            if vno and vol["no"] != vno:
                continue
            for art in vol["articles"]:
                parts.append(f"【{art['title']}】")
                for u in art["units"]:
                    parts.extend(u["原文"])
                for sub in art["sub_articles"]:
                    parts.append(f"  【{sub['title']}】")
                    for u in sub["units"]:
                        parts.extend(u["原文"])
            out_write("\n".join(parts), args.输出)
            if not args.输出:
                break


def cmd_tijie(args):
    doc = load_doc()
    hits = find_articles(doc, args.篇, args.卷)
    hit, err = pick(hits, args.卷)
    if err:
        print(err)
        return
    volname, art, is_sub, parent = hit
    print(f"《{BOOK_TITLE}》{volname}《{art['title']}》题解（写作背景）：")
    for p in art.get("ti_jie", []):
        print()
        print(p)
    if not art.get("ti_jie"):
        print("（本篇无题解）")


def cmd_zhushi(args):
    doc = load_doc()
    if args.词:
        # 全书检索词语解释
        found = 0
        for vol in doc["volumes"]:
            for art in vol["articles"]:
                for a in [art] + art["sub_articles"]:
                    for u in a["units"]:
                        for n in u["注释"]:
                            hay = f"{n['term'] or ''} {n['text']}"
                            if args.词 in hay:
                                found += 1
                                key = n["key"] or ""
                                print(f"{vol['no']}《{a['title']}》　{key}{n['text']}")
        if not found:
            print(f"未找到包含“{args.词}”的注释")
        return
    hits = find_articles(doc, args.篇, args.卷)
    hit, err = pick(hits, args.卷)
    if err:
        print(err)
        return
    volname, art, is_sub, parent = hit
    print(f"《{BOOK_TITLE}》{volname}《{art['title']}》注释：")
    for u in art["units"]:
        for n in u["注释"]:
            key = n["key"] or ""
            if args.锚 and key != args.锚:
                continue
            # 标注出处：该标注出现在哪段原文
            where = ""
            for i, ancs in enumerate(u["标注"], 1):
                if key in ancs:
                    where = f"（第{i}段原文标注 {key}）"
            print(f"{key}{n['text']}{where}")
    if args.锚:
        print(f"（仅显示标注 {args.锚} 的条目；如无输出，说明该篇没有此标注）")


def cmd_yiwen(args):
    doc = load_doc()
    hits = find_articles(doc, args.篇, args.卷)
    hit, err = pick(hits, args.卷)
    if err:
        print(err)
        return
    volname, art, is_sub, parent = hit
    units = art["units"] or [
        s for sub in art["sub_articles"] for s in sub["units"]
    ]
    print(f"《{BOOK_TITLE}》{volname}《{art['title']}》译文：")
    for k, u in enumerate(units, 1):
        if args.段 and k != args.段:
            continue
        if not u["译文"]:
            print(f"（第{k}段无译文）")
            continue
        print(f"—— 第{k}段 ——")
        if u["对齐"] == "1:1":
            for i, (o, t) in enumerate(zip(u["原文"], u["译文"]), 1):
                print(f"〔原文{i}〕{o}")
                print(f"〔译文{i}〕{t}")
                print()
        else:
            for i, o in enumerate(u["原文"], 1):
                print(f"〔原文{i}〕{o}")
            print("〔译文〕")
            for t in u["译文"]:
                print(t)
            print()


def cmd_sousuo(args):
    doc = load_doc()
    kw = args.词
    total = 0
    for vol in doc["volumes"]:
        for art in vol["articles"]:
            for a in [art] + art["sub_articles"]:
                loc = f"{vol['no']}《{a['title']}》"
                for p in a.get("ti_jie", []):
                    if kw in p:
                        total += 1
                        print(f"[题解] {loc}：…{p[max(0, p.find(kw) - 30):p.find(kw) + 40]}…")
                for u in a["units"]:
                    for o in u["原文"]:
                        if kw in o:
                            total += 1
                            print(f"[原文] {loc}：…{o[max(0, o.find(kw) - 30):o.find(kw) + 40]}…")
                    for n in u["注释"]:
                        hay = f"{n['term'] or ''} {n['text']}"
                        if kw in hay:
                            total += 1
                            print(f"[注释] {loc}：…{hay[max(0, hay.find(kw) - 30):hay.find(kw) + 40]}…")
                    for t in u["译文"]:
                        if kw in t:
                            total += 1
                            print(f"[译文] {loc}：…{t[max(0, t.find(kw) - 30):t.find(kw) + 40]}…")
    print(f"（共 {total} 处）" if total else f"未找到“{kw}”")


def main():
    ap = argparse.ArgumentParser(description="《焚书》EPUB 结构化工具", prog="fen_shu.py")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("parse", help="重新解析EPUB，生成JSON与分卷TXT")
    p.set_defaults(fn=cmd_parse)

    for name, fn, help_txt in [
        ("篇目", cmd_mulu, "按卷列出篇目"),
        ("原文", cmd_yuanwen, "按卷/篇只拿原文"),
        ("题解", cmd_tijie, "取某篇写作背景"),
        ("注释", cmd_zhushi, "取段落对应词解释 / 全书检索"),
        ("译文", cmd_yiwen, "取对应译文"),
        ("检索", cmd_sousuo, "全文检索"),
    ]:
        p = sub.add_parser(name, help=help_txt)
        p.add_argument("--卷", default=None, help="卷名，如 卷一 或 1")
        p.add_argument("--篇", default=None, help="篇目标题（支持模糊）")
        p.add_argument("--锚", default=None, help="注释标注，如 ①")
        p.add_argument("--词", default=None, help="关键词")
        p.add_argument("--段", type=int, default=None, help="单元序号（译文用）")
        p.add_argument("--输出", default=None, help="输出到文件（原文用）")
        p.set_defaults(fn=fn)

    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
