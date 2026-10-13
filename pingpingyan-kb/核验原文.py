# -*- coding: utf-8 -*-
"""核验《平平言》原文拆分结果"""
import os

OUT_DIR = r"E:\git\ToolBox\guji\pingpingyan-kb\原文"
FILES = ["序", "凡例", "卷一", "卷二", "卷三", "卷四", "跋"]


def lines(p):
    with open(p, encoding="utf-8") as f:
        return [l.strip() for l in f.read().splitlines() if l.strip()]


allok = True
for name in FILES:
    fp = os.path.join(OUT_DIR, name + ".txt")
    if not os.path.exists(fp):
        print(name, ": 缺失!")
        allok = False
        continue
    ls = lines(fp)
    secs = [l for l in ls if l.startswith(("○", "△"))]
    ok = ls[0].startswith("【") and len(ls) >= 2
    if not ok:
        allok = False
    print(f"{name}: 行数{len(ls)} 首行{ls[0]} ○△标题{len(secs)} {'OK' if ok else '异常'}")

mg = lines(os.path.join(OUT_DIR, "平平言_原文_全卷合并.txt"))
sep = "=" * 60
banners = []
expect = False
for l in mg:
    if l == sep:
        expect = True
    elif expect and l.startswith("【"):
        banners.append(l)
        expect = False
    else:
        expect = False
print("合并文件: 篇横幅", len(banners), "个:", banners)
print("总体:", "ALL OK" if (allok and len(banners) == 7) else "HAS ISSUES")
