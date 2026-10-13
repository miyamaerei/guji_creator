# -*- coding: utf-8 -*-
"""
《平平言》EPUB 拆解脚本（参照前四书拆分方案）
- 读取 EPUB/chapters/chapter-*.xhtml，h1 为篇名（去除排版装饰符 ●），p 为段落
- 保留标题（卷首篇目、○/△ 分节标题原样）、篇名（【篇名】行）、正文内容
- 输出：原文\序.txt、凡例.txt、卷一~四.txt、跋.txt + 全卷合并文件
"""
import os
import zipfile
from html.parser import HTMLParser

EPUB = r"C:\Users\Administrator\Downloads\平平言.epub"
OUT = r"E:\git\ToolBox\guji\pingpingyan-kb"
OUT_DIR = os.path.join(OUT, "原文")

ORDER = [
    ("chapter-fc8749d33883.xhtml", "序"),
    ("chapter-50c008c294ea.xhtml", "凡例"),
    ("chapter-b4f0694ac594.xhtml", "卷一"),
    ("chapter-56e3b4ca9b7f.xhtml", "卷二"),
    ("chapter-e6c0b5fe0386.xhtml", "卷三"),
    ("chapter-974ede8f63fc.xhtml", "卷四"),
    ("chapter-7f8dd7437185.xhtml", "跋"),
]


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = ""
        self.ps = []
        self.cur = None

    def handle_starttag(self, tag, attrs):
        if tag in ("h1", "p"):
            self.cur = []

    def handle_data(self, data):
        if self.cur is not None:
            self.cur.append(data)

    def handle_endtag(self, tag):
        if tag in ("h1", "p") and self.cur is not None:
            txt = "".join(self.cur).strip()
            if tag == "h1":
                self.h1 = txt
            else:
                self.ps.append(txt)
            self.cur = None


def clean(t):
    import html
    return html.unescape(t).replace("\u3000", "").lstrip("●").strip()


os.makedirs(OUT_DIR, exist_ok=True)

merged = []
merged.append("平平言（原文全卷合并）")
merged.append("（清·方大湜 撰，官箴书，序、凡例、四卷及跋按原书顺序合并）")
merged.append("")

sep = "=" * 60
with zipfile.ZipFile(EPUB) as z:
    for fn, name in ORDER:
        raw = z.read("EPUB/chapters/" + fn).decode("utf-8", "ignore")
        p = P()
        p.feed(raw)
        title = clean(p.h1) or name
        paras = [clean(s) for s in p.ps if s.strip()]
        lines = ["【" + title + "】", ""]
        for para in paras:
            lines.append(para)
        fpath = os.path.join(OUT_DIR, name + ".txt")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        merged.append(sep)
        merged.append("【" + title + "】")
        merged.append(sep)
        merged.append("")
        merged.extend(paras)
        merged.append("")
        print(f"写出 {name}.txt 段落{len(paras)} 字数{sum(len(s) for s in paras)} 标题={title}")

with open(os.path.join(OUT_DIR, "平平言_原文_全卷合并.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(merged))
print("合并文件已写出 | 总字符:", sum(len(l) for l in merged))
