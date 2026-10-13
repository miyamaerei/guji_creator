# -*- coding: utf-8 -*-
"""核验《平平言》七篇白话译文：
- 行数：译文非空行数 >= 原文非空行数
- ○/△ 标题：原文全部标题逐字出现在译文中
- 卷首篇目：原文篇目条目逐条出现在译文中
- 篇名行 / 结构标记：首行一致，（卷首篇目）/（正文）标记齐全
"""
import os

SRC = r"E:\git\ToolBox\guji\pingpingyan-kb\原文"
OUT = r"E:\git\ToolBox\guji\pingpingyan-kb\白话文"
FILES = ["序", "凡例", "卷一", "卷二", "卷三", "卷四", "跋"]


def lines(p):
    with open(p, encoding="utf-8") as f:
        return [l.strip() for l in f.read().splitlines() if l.strip()]


allok = True
for name in FILES:
    sl = lines(os.path.join(SRC, name + ".txt"))
    op = os.path.join(OUT, name + "_白话.txt")
    if not os.path.exists(op):
        print(name, ": 译文文件缺失!")
        allok = False
        continue
    tl = lines(op)
    tset = set(tl)

    # 1) 行数
    ok_lines = len(tl) >= len(sl)

    # 2) ○/△ 标题
    sec = [l for l in sl if l.startswith(("○", "△"))]
    miss_sec = [s for s in sec if s not in tset]
    ok_sec = not miss_sec

    # 3) 卷首篇目（作者行之后、第一个○/△之前）
    toc = []
    body_at = None
    for i, l in enumerate(sl):
        if l.startswith(("○", "△")):
            body_at = i
            break
    if body_at is not None and len(sl) > 2:
        toc = sl[2:body_at]
    miss_toc = [t for t in toc if t not in tset]
    ok_toc = not miss_toc

    # 4) 篇名行 + 结构标记
    ok_head = sl[0] == tl[0]
    mark_req = ["（卷首篇目）"] if toc else []
    mark_req.append("（正文）")
    miss_mark = [m for m in mark_req if m not in tset]
    ok_mark = not miss_mark

    ok = ok_lines and ok_sec and ok_toc and ok_head and ok_mark
    if not ok:
        allok = False
    print("=" * 20, name, "=" * 20)
    print(f"  原文非空行 {len(sl)} | 译文非空行 {len(tl)} | 行数OK: {ok_lines}")
    print(f"  ○/△标题 原文{len(sec)} | 缺失: {miss_sec if miss_sec else '无'}")
    print(f"  卷首篇目 原文{len(toc)} | 缺失: {miss_toc if miss_toc else '无'}")
    print(f"  篇名行一致: {ok_head} | 结构标记: {'OK' if ok_mark else '缺 ' + str(miss_mark)}")
    print(f"  => {'OK' if ok else '异常'}")

print("=" * 60)
print("总体:", "ALL OK" if allok else "HAS ISSUES")
