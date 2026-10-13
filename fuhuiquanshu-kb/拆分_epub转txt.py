# -*- coding: utf-8 -*-
"""
《福惠全书》EPUB 拆解脚本（参照吕公实政录/宛署杂记拆分方案）
- 读取 EPUB/chapters/chapter-*.xhtml，h1 为卷名（去除排版装饰符 ●），p 为段落
- 保留标题（○/△ 分节标题原样）、卷名（【卷名】行）、正文内容
- 输出：原文\目录.txt、自序.txt、凡例.txt、卷之一~卷之三十二.txt、禀启附.txt + 全卷合并文件
"""
import os
import zipfile
from html.parser import HTMLParser

EPUB = r"C:\Users\Administrator\Downloads\福惠全书.epub"
OUT = r"E:\git\ToolBox\guji\fuhuiquanshu-kb"
OUT_DIR = os.path.join(OUT, "原文")

# 书序目录顺序（含文件名与卷名）
ORDER = [
    ("chapter-831a50a6ae92.xhtml", "目录"),
    ("chapter-9e9c7d7387ab.xhtml", "自序"),
    ("chapter-be9ae5c7e07c.xhtml", "凡例"),
    ("chapter-2ab1130fbcc8.xhtml", "卷之一"),
    ("chapter-594ac3fe67e5.xhtml", "卷之二"),
    ("chapter-1a625b8cdd24.xhtml", "卷之三"),
    ("chapter-0e38cf4e1edc.xhtml", "卷之四"),
    ("chapter-ede10c3adce3.xhtml", "卷之五"),
    ("chapter-0a94f3a168a0.xhtml", "卷之六"),
    ("chapter-58d13853f596.xhtml", "卷之七"),
    ("chapter-fc12eebe327e.xhtml", "卷之八"),
    ("chapter-d8257437ea6e.xhtml", "卷之九"),
    ("chapter-5d8cb476270f.xhtml", "卷之十"),
    ("chapter-e6df832140a1.xhtml", "卷之十一"),
    ("chapter-9a86d6c7c1bc.xhtml", "卷之十二"),
    ("chapter-a206eaabeec2.xhtml", "卷之十三"),
    ("chapter-54b3e7df4fef.xhtml", "卷之十四"),
    ("chapter-aed7374583e8.xhtml", "卷之十五"),
    ("chapter-c62c3db9bc32.xhtml", "卷之十六"),
    ("chapter-7722b9dcd6fe.xhtml", "卷之十七"),
    ("chapter-fba1fff92897.xhtml", "卷之十八"),
    ("chapter-ea5965daf7bf.xhtml", "卷之十九"),
    ("chapter-1a2fbde4ac49.xhtml", "卷之二十"),
    ("chapter-58a4fac0781a.xhtml", "卷之二十一"),
    ("chapter-9d2790af8986.xhtml", "卷之二十二"),
    ("chapter-9adc21cbbc3c.xhtml", "卷之二十三"),
    ("chapter-56d2eeb5b96e.xhtml", "卷之二十四"),
    ("chapter-cac585e53544.xhtml", "卷之二十五"),
    ("chapter-f0b8278b9629.xhtml", "卷之二十六"),
    ("chapter-febe51d88bfd.xhtml", "卷之二十七"),
    ("chapter-2d05f85d7af1.xhtml", "卷之二十八"),
    ("chapter-f4eb58d9cbd9.xhtml", "卷之二十九"),
    ("chapter-65df1dec3192.xhtml", "卷之三十"),
    ("chapter-cc0d950bd2ed.xhtml", "卷之三十一"),
    ("chapter-615f676b1913.xhtml", "卷之三十二"),
    ("chapter-54d01e180390.xhtml", "禀启附"),
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
    t = html.unescape(t).replace("\u3000", "")
    return t.lstrip("●").strip()


os.makedirs(OUT_DIR, exist_ok=True)

merged = []
merged.append("福惠全书（原文全卷合并）")
merged.append("（清·黄六鸿 撰，官箴书，目录、自序、凡例、三十二卷及禀启附按原书顺序合并）")
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

with open(os.path.join(OUT_DIR, "福惠全书_原文_全卷合并.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(merged))
print("合并文件已写出 | 总字符:", sum(len(l) for l in merged))
