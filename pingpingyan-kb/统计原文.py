# -*- coding: utf-8 -*-
"""统计《平平言》原文各篇行数与 ○/△ 标题数，核对与任务描述一致。"""
import os, re

SRC = r"E:\git\ToolBox\guji\pingpingyan-kb\原文"
FILES = ["序.txt", "凡例.txt", "卷一.txt", "卷二.txt", "卷三.txt", "卷四.txt", "跋.txt"]


def lines(p):
    with open(p, encoding="utf-8") as f:
        return [l.strip() for l in f.read().splitlines() if l.strip()]


total = 0
for name in FILES:
    ls = lines(os.path.join(SRC, name))
    marks = [l for l in ls if l.startswith(("○", "△"))]
    sub = [l for l in ls if not l.startswith(("○", "△"))]
    # 卷首篇目 = 作者行之后、第一个○/△之前的所有无标记行（仅卷类适用）
    toc = []
    body_start = None
    for i, l in enumerate(ls):
        if l.startswith(("○", "△")):
            body_start = i
            break
    if body_start is not None and ls[0].startswith("【") and body_start > 2:
        toc = ls[2:body_start]
    nchars = sum(len(l) for l in ls)
    print(f"{name}: 非空行 {len(ls)} | ○/△标题 {len(marks)} | 卷首篇目 {len(toc)} | 字符 {nchars}")
    total += len(marks)
print("○/△ 标题总数:", total)
