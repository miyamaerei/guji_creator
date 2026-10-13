# -*- coding: utf-8 -*-
"""
《松窗梦语》EPUB 拆解脚本（参照前三书拆分方案）
- 读取 EPUB/chapters/chapter-*.xhtml，h1 为纪名（保留），p 为段落
- 宦游纪被 EPUB 拆为 4 个章节文件，合并回一个整篇
- 输出：原文\<纪名>.txt（33 篇）+ 全卷合并文件
"""
import os
import zipfile
from html.parser import HTMLParser

EPUB = r"C:\Users\Administrator\Downloads\松窗梦语-文硕阁-2236627c.epub"
OUT = r"E:\git\ToolBox\guji\songchuangmengyu-kb"
OUT_DIR = os.path.join(OUT, "原文")

# 篇章顺序：每篇为 (输出名, [章节文件名...])
ORDER = [
    ("宦游纪", ["chapter-be982157797b.xhtml", "chapter-436e8d842e7f.xhtml",
                "chapter-c9d267e90b8c.xhtml", "chapter-365c7f6a1818.xhtml"]),
    ("南游纪", ["chapter-b9e6c7b1837d.xhtml"]),
    ("北游纪", ["chapter-0927d3129716.xhtml"]),
    ("东游纪", ["chapter-293adb699048.xhtml"]),
    ("西游纪", ["chapter-13b6d26910ab.xhtml"]),
    ("北虏纪", ["chapter-1790122c32ec.xhtml"]),
    ("南夷纪", ["chapter-521395845aa0.xhtml"]),
    ("东倭纪", ["chapter-3b2cc03062aa.xhtml"]),
    ("西番纪", ["chapter-c9f54facc062.xhtml"]),
    ("士人纪", ["chapter-81f342f1e882.xhtml"]),
    ("三农纪", ["chapter-8901bbf05132.xhtml"]),
    ("百工纪", ["chapter-b0e166cc8e0d.xhtml"]),
    ("商贾纪", ["chapter-d85f151f6272.xhtml"]),
    ("象纬纪", ["chapter-80a5676ddebb.xhtml"]),
    ("堪舆纪", ["chapter-3bb33e7021ee.xhtml"]),
    ("祥瑞纪", ["chapter-f987853bd038.xhtml"]),
    ("灾异纪", ["chapter-a404573d055e.xhtml"]),
    ("花木纪", ["chapter-18a2825a915c.xhtml"]),
    ("鸟兽纪", ["chapter-7327c1823e25.xhtml"]),
    ("方术纪", ["chapter-2c0648f106c9.xhtml"]),
    ("盛遇纪", ["chapter-f788b13a6de6.xhtml"]),
    ("异闻纪", ["chapter-6e22f1aa3635.xhtml"]),
    ("先世纪", ["chapter-2dbf7b2d5859.xhtml"]),
    ("梦寐纪", ["chapter-e690c83a2d18.xhtml"]),
    ("权势纪", ["chapter-b814092eb136.xhtml"]),
    ("忠廉纪", ["chapter-64b8a1d5f67b.xhtml"]),
    ("时序纪", ["chapter-e0f0c114520f.xhtml"]),
    ("风俗纪", ["chapter-97c778d4e483.xhtml"]),
    ("自省纪", ["chapter-ea65b601e714.xhtml"]),
    ("铨部纪", ["chapter-e0185b187c2f.xhtml"]),
    ("宗藩纪", ["chapter-38bf00d13f95.xhtml"]),
    ("漕运纪", ["chapter-8dc0995146d1.xhtml"]),
    ("两粤纪", ["chapter-e20128ef5ac1.xhtml"]),
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
    return html.unescape(t).replace("\u3000", "").strip()


os.makedirs(OUT_DIR, exist_ok=True)

merged = []
merged.append("松窗梦语（原文全卷合并）")
merged.append("（明·张瀚 撰，笔记体，三十三纪按原书顺序合并）")
merged.append("")

sep = "=" * 60
with zipfile.ZipFile(EPUB) as z:
    for name, fns in ORDER:
        paras = []
        for fn in fns:
            raw = z.read("EPUB/chapters/" + fn).decode("utf-8", "ignore")
            p = P()
            p.feed(raw)
            paras.extend([clean(s) for s in p.ps if s.strip()])
        lines = ["【" + name + "】", ""]
        for para in paras:
            lines.append(para)
        fpath = os.path.join(OUT_DIR, name + ".txt")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        merged.append(sep)
        merged.append("【" + name + "】")
        merged.append(sep)
        merged.append("")
        merged.extend(paras)
        merged.append("")
        print(f"写出 {name}.txt 段落{len(paras)} 字数{sum(len(s) for s in paras)}")

with open(os.path.join(OUT_DIR, "松窗梦语_原文_全卷合并.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(merged))
print("合并文件已写出 | 总字符:", sum(len(l) for l in merged))
