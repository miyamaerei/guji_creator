# -*- coding: utf-8 -*-
"""
《宛署杂记》EPUB 拆解脚本（参照吕公实政录拆分方案）
- 读取 EPUB/chapters/chapter-*.xhtml，h1 为卷名，p 为段落
- 保留标题（○/△ 分节标题原样）、卷名（【卷名】行）、正文内容
- 输出：原文\自序.txt、原文\卷一~卷二十.txt + 全卷合并文件
"""
import os
import zipfile
from html.parser import HTMLParser

EPUB = r"C:\Users\Administrator\Downloads\宛署杂记-文硕阁-5d111746.epub"
OUT = r"E:\git\ToolBox\guji\yuanshuzaji-kb"
OUT_DIR = os.path.join(OUT, "原文")

# 书序目录顺序（含文件名与卷名）
ORDER = [
    ("chapter-dca2e9f6aeab.xhtml", "自序"),
    ("chapter-e34434edcb1b.xhtml", "卷一"),
    ("chapter-30e520dbedcf.xhtml", "卷二"),
    ("chapter-5142765dbe94.xhtml", "卷三"),
    ("chapter-276b81dbc5ca.xhtml", "卷四"),
    ("chapter-e49ffef7bcc7.xhtml", "卷五"),
    ("chapter-0781d3e56379.xhtml", "卷六"),
    ("chapter-5d6014444e41.xhtml", "卷七"),
    ("chapter-36f6012ca29f.xhtml", "卷八"),
    ("chapter-a25f2e17ee7a.xhtml", "卷九"),
    ("chapter-f7034fac634b.xhtml", "卷十"),
    ("chapter-56f16abb072c.xhtml", "卷十一"),
    ("chapter-190083461414.xhtml", "卷十二"),
    ("chapter-d291fcfcbd1d.xhtml", "卷十三"),
    ("chapter-94b4f70b7c27.xhtml", "卷十四"),
    ("chapter-1c799dd697ee.xhtml", "卷十五"),
    ("chapter-6e9baf538e68.xhtml", "卷十六"),
    ("chapter-000f67f5a1ef.xhtml", "卷十七"),
    ("chapter-5bb4d5971264.xhtml", "卷十八"),
    ("chapter-d3a7ce2fb3f8.xhtml", "卷十九"),
    ("chapter-0a9d9f4ae2d2.xhtml", "卷二十"),
]


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = ""
        self.ps = []
        self.cur = None
        self.tag = None

    def handle_starttag(self, tag, attrs):
        self.tag = tag
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
            self.tag = None


def unescape(t):
    import html
    return html.unescape(t).replace("\u3000", "")


os.makedirs(OUT_DIR, exist_ok=True)

merged = []
merged.append("宛署杂记（原文全卷合并）")
merged.append("（明·沈榜 撰，万历年间宛平县地方志，自序及二十卷按原书顺序合并）")
merged.append("")

sep = "=" * 60
with zipfile.ZipFile(EPUB) as z:
    for fn, name in ORDER:
        raw = z.read("EPUB/chapters/" + fn).decode("utf-8", "ignore")
        p = P()
        p.feed(raw)
        title = p.h1 or name
        paras = [unescape(s) for s in p.ps if s.strip()]
        # 单卷文件
        lines = ["【" + title + "】", ""]
        for para in paras:
            lines.append(para)
        fpath = os.path.join(OUT_DIR, name + ".txt")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        # 合并文件
        merged.append(sep)
        merged.append("【" + title + "】")
        merged.append(sep)
        merged.append("")
        merged.extend(paras)
        merged.append("")
        print(f"写出 {name}.txt 段落{len(paras)} 字数{sum(len(s) for s in paras)}")

with open(os.path.join(OUT_DIR, "宛署杂记_原文_全卷合并.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(merged))
print("合并文件已写出 | 总字符:", sum(len(l) for l in merged))
