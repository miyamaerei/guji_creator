# -*- coding: utf-8 -*-
"""《平平言》白话文全卷合并脚本
- 读取 7 篇白话译文，按 序→凡例→卷一→卷二→卷三→卷四→跋 顺序合并
- 每篇以 分隔线 + ◆篇名标题 起头（结构参照原文合并文件）
"""
import os

OUT = r"E:\git\ToolBox\guji\pingpingyan-kb\白话文"
ORDER = ["序", "凡例", "卷一", "卷二", "卷三", "卷四", "跋"]


def lines(p):
    with open(p, encoding="utf-8") as f:
        return [l.rstrip() for l in f.read().splitlines() if l.strip()]


merged = []
merged.append("平平言（白话文全卷合并）")
merged.append("（清·方大湜 撰，官箴书，白话文翻译，序、凡例、四卷及跋按原书顺序合并）")
merged.append("")
sep = "=" * 60
for name in ORDER:
    ls = lines(os.path.join(OUT, name + "_白话.txt"))
    merged.append(sep)
    merged.append(f"◆ {name}")
    merged.append(sep)
    merged.append("")
    merged.extend(ls[1:])  # 首行【篇名】已由◆标题承担
    merged.append("")

with open(os.path.join(OUT, "平平言_白话文_全卷合并.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(merged))
heads = [l for l in merged if l.startswith("◆ ")]
print("merged written | chars:", sum(len(l) for l in merged), "| lines:", len(merged))
print("◆ 标题:", heads)
