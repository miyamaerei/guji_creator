# -*- coding: utf-8 -*-
"""核验《治谱》原文拆分结果"""
import os

OUT_DIR = r"E:\git\ToolBox\guji\zhipu-kb\原文"
FILES = ["序言目录", "卷之一", "卷之二", "卷之三", "卷之四", "卷之五",
         "卷之六", "卷之七", "卷之八", "卷之九", "卷之十", "卷之十补遗"]


def lines(p):
    with open(p, encoding="utf-8") as f:
        return [l for l in f.read().splitlines()]


allok = True
for name in FILES:
    fp = os.path.join(OUT_DIR, name + ".txt")
    if not os.path.exists(fp):
        print(name, ": 缺失!"); allok = False; continue
    ls = lines(fp)
    nonempty = [l for l in ls if l.strip()]
    ok = len(ls) >= 2 and nonempty
    if not ok:
        allok = False
    print(f"{name}: 行数{len(ls)} 非空{len(nonempty)} 字符{sum(len(l) for l in ls)} 首行{ls[0][:30] if ls else '空'} {'OK' if ok else '异常'}")

mg = lines(os.path.join(OUT_DIR, "治谱_原文_全卷合并.txt"))
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
print("合并文件: 篇横幅", len(banners), "个")
print("总体:", "ALL OK" if (allok and len(banners) == 12) else "HAS ISSUES")
