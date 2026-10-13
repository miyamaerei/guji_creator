# -*- coding: utf-8 -*-
"""核验 15 个译文文件与合并文件结构"""
import os

src_dir = r"E:\git\ToolBox\guji\shizhenglu-kb\原文"
out_dir = r"E:\git\ToolBox\guji\shizhenglu-kb\白话文"
files = ["明职·新吾吕先生实政录序", "明职·明职引", "明职·卷一", "民务·卷之二",
         "民务·卷之三", "民务·卷之四", "乡甲约·卷之一", "乡甲约·卷之二",
         "乡甲约·卷之三", "乡甲约·卷之四", "乡甲约·卷之五", "乡甲约·卷之六",
         "风宪约·重刊风宪约序", "风宪约·卷之一", "风宪约·卷之二"]


def lines(p):
    with open(p, encoding="utf-8") as f:
        return [l.strip() for l in f.read().splitlines() if l.strip()]


allok = True
for name in files:
    sl = lines(os.path.join(src_dir, name + ".txt"))
    op = os.path.join(out_dir, name + "_白话.txt")
    if not os.path.exists(op):
        print(name, ": 译文文件缺失!")
        allok = False
        continue
    tl = lines(op)
    sec = [l for l in sl if l.startswith(("○", "△"))]
    miss = [s for s in sec if s not in tl]
    ok = (len(tl) >= len(sl)) and not miss
    if not ok:
        allok = False
    status = "OK" if ok else ("异常! 标题缺失:" + str(miss))
    print(name, ": 原文", len(sl), "行 译文", len(tl), "行", status)

mg = lines(os.path.join(out_dir, "吕公实政录_白话文_全卷合并.txt"))
heads = [l for l in mg if l.startswith("◆ ")]
parts = [l for l in mg if l.startswith("【") and l.endswith("】")]
print("合并文件：◆标题", len(heads), "个")
print("分部横幅:", parts)
print("总体:", "ALL OK" if (allok and len(heads) == 15 and len(parts) == 4) else "HAS ISSUES")
