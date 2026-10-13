# -*- coding: utf-8 -*-
"""
《吕公实政录》EPUB -> TXT 拆分脚本
- 按卷拆分：每卷一个 txt（保留卷名、卷首篇目、正文）
- 合并：生成全卷合并 txt（按原书顺序：明职序引+卷一、民务卷二~四、乡甲约卷一~六、风宪约序+卷一~二）
"""
import zipfile, re, os
from html import unescape
from html.parser import HTMLParser

EPUB = r"C:\Users\Administrator\Downloads\吕公实政录.epub"
OUT_DIR = r"E:\git\ToolBox\guji\shizhenglu-kb\原文"
os.makedirs(OUT_DIR, exist_ok=True)

# 按原书阅读顺序排列：(epub内部文件, 所属部, 标题)
ORDER = [
    ("OEBPS/Chapter183396.html", "明职", "新吾吕先生实政录序"),
    ("OEBPS/Chapter183397.html", "明职", "明职引"),
    ("OEBPS/Chapter183398.html", "明职", "卷一"),
    ("OEBPS/Chapter183399.html", "民务", "卷之二"),
    ("OEBPS/Chapter183400.html", "民务", "卷之三"),
    ("OEBPS/Chapter183401.html", "民务", "卷之四"),
    ("OEBPS/Chapter183402.html", "乡甲约", "卷之一"),
    ("OEBPS/Chapter183403.html", "乡甲约", "卷之二"),
    ("OEBPS/Chapter183404.html", "乡甲约", "卷之三"),
    ("OEBPS/Chapter183405.html", "乡甲约", "卷之四"),
    ("OEBPS/Chapter183406.html", "乡甲约", "卷之五"),
    ("OEBPS/Chapter183407.html", "乡甲约", "卷之六"),
    ("OEBPS/Chapter183408.html", "风宪约", "重刊风宪约序"),
    ("OEBPS/Chapter183409.html", "风宪约", "卷之一"),
    ("OEBPS/Chapter183410.html", "风宪约", "卷之二"),
]


class TextExtractor(HTMLParser):
    """提取 h1 标题与 p 段落的纯文本（保持出现顺序）。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []      # [(kind, text)]  kind: 'h1' | 'p'
        self.cur = None       # 当前正在收集的元素
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "p"):
            self.cur = tag
            self.buf = []

    def handle_endtag(self, tag):
        if tag in ("h1", "p") and self.cur == tag:
            text = "".join(self.buf)
            text = text.replace("\r", " ").replace("\n", " ")
            text = re.sub(r"[ \t\u3000]+", " ", text).strip()
            if text:
                self.blocks.append((tag, text))
            self.cur = None
            self.buf = []

    def handle_data(self, data):
        if self.cur:
            self.buf.append(data)


def extract_blocks(zf, path):
    raw = zf.read(path).decode("utf-8", errors="replace")
    # 只取 body 内的内容
    m = re.search(r"<body[^>]*>(.*)</body>", raw, re.S)
    body = m.group(1) if m else raw
    parser = TextExtractor()
    parser.feed(body)
    return parser.blocks


def clean_text(s):
    return unescape(s).replace("\r", " ").replace("\n", " ").replace("\t", " ")


def main():
    zf = zipfile.ZipFile(EPUB)
    results = []  # (部, 标题, 卷名行, 篇目list, 正文list)
    for path, part, title in ORDER:
        blocks = extract_blocks(zf, path)
        paras = [t for k, t in blocks if k == "p"]
        h1 = next((t for k, t in blocks if k == "h1"), None)
        # 卷名行：部 + 标题（原书 h1 只有卷号，这里补上部名以区分同名卷）
        vol_label = f"{part}·{title}"
        # 找出第一个 ○/△ 开头的段落 => 正文起点；若整卷无 ○/△ 标记（如序文、单篇长文），则全部视为正文
        body_start = None
        for i, p in enumerate(paras):
            if p.startswith("○") or p.startswith("△"):
                body_start = i
                break
        if body_start is not None:
            toc_list, body_list = paras[:body_start], paras[body_start:]
        else:
            toc_list, body_list = [], paras
        results.append((part, title, vol_label, h1, toc_list, body_list))

    # ---------- 1. 按卷写独立文件 ----------
    for part, title, vol_label, h1, toc_list, body_list in results:
        lines = [f"【{vol_label}】"]
        if toc_list:
            lines.append("（卷首篇目）")
            lines.extend(toc_list)
        if body_list:
            lines.append("（正文）")
            lines.extend(body_list)
        content = "\n".join(lines) + "\n"
        fname = f"{vol_label}.txt"
        with open(os.path.join(OUT_DIR, fname), "w", encoding="utf-8") as f:
            f.write(content)
        print("written:", fname, "| chars:", len(content))

    # ---------- 2. 全卷合并 ----------
    merged = []
    merged.append("吕公实政录（原文全卷合并）")
    merged.append("明·吕坤 撰")
    merged.append("（按原书顺序合并：明职序引及卷一、民务卷二至四、乡甲约卷一至六、风宪约序及卷一至二）")
    merged.append("")
    sep = "=" * 60
    last_part = None
    for part, title, vol_label, h1, toc_list, body_list in results:
        if part != last_part:
            merged.append(sep)
            merged.append(f"【{part}】")
            merged.append(sep)
            merged.append("")
            last_part = part
        merged.append(f"◆ {vol_label}")
        merged.append("")
        if toc_list:
            merged.append("（卷首篇目）")
            merged.extend(toc_list)
            merged.append("")
        merged.append("（正文）")
        merged.extend(body_list)
        merged.append("")
    with open(os.path.join(OUT_DIR, "吕公实政录_原文_全卷合并.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(merged))
    print("\nmerged written: 吕公实政录_原文_全卷合并.txt | chars:", sum(len(l) for l in merged))


if __name__ == "__main__":
    main()
