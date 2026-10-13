# -*- coding: utf-8 -*-
"""
《吕公实政录》白话文全卷合并脚本
- 读取 15 个分卷白话文译文文件，按原书顺序合并为一个文件
- 结构参照原文合并文件：分部横幅 + ◆卷名标题
"""
import os

OUT = r"E:\git\ToolBox\guji\shizhenglu-kb\白话文"
ORDER = [
    ("明职", "明职·新吾吕先生实政录序"),
    ("明职", "明职·明职引"),
    ("明职", "明职·卷一"),
    ("民务", "民务·卷之二"),
    ("民务", "民务·卷之三"),
    ("民务", "民务·卷之四"),
    ("乡甲约", "乡甲约·卷之一"),
    ("乡甲约", "乡甲约·卷之二"),
    ("乡甲约", "乡甲约·卷之三"),
    ("乡甲约", "乡甲约·卷之四"),
    ("乡甲约", "乡甲约·卷之五"),
    ("乡甲约", "乡甲约·卷之六"),
    ("风宪约", "风宪约·重刊风宪约序"),
    ("风宪约", "风宪约·卷之一"),
    ("风宪约", "风宪约·卷之二"),
]


def lines(p):
    with open(p, encoding="utf-8") as f:
        return [l.rstrip() for l in f.read().splitlines() if l.strip()]


merged = []
merged.append("吕公实政录（白话文全卷合并）")
merged.append("（《实政录》全书 12 卷及序引的白话文翻译，按原书顺序合并）")
merged.append("")
sep = "=" * 60
last = None
for part, name in ORDER:
    if part != last:
        merged.append(sep)
        merged.append(f"【{part}】")
        merged.append(sep)
        merged.append("")
        last = part
    ls = lines(os.path.join(OUT, name + "_白话.txt"))
    merged.append(f"◆ {name}")
    merged.append("")
    merged.extend(ls[1:])  # 首行【卷名】已由◆标题承担
    merged.append("")

with open(os.path.join(OUT, "吕公实政录_白话文_全卷合并.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(merged))
print("merged written | chars:", sum(len(l) for l in merged), "| lines:", len(merged))
