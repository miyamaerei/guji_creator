# -*- coding: utf-8 -*-
"""核验《宛署杂记》白话译文：行数比对、○/△标题覆盖、合并结构"""
import os

SRC = r"E:\git\ToolBox\guji\yuanshuzaji-kb\原文"
OUT = r"E:\git\ToolBox\guji\yuanshuzaji-kb\白话文"
CN = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
      "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十"]
FILES = ["自序"] + ["卷" + c for c in CN]


def lines(p):
    with open(p, encoding="utf-8") as f:
        return [l.strip() for l in f.read().splitlines() if l.strip()]


allok = True
for name in FILES:
    sl = lines(os.path.join(SRC, name + ".txt"))
    tp = os.path.join(OUT, name + "_白话.txt")
    if not os.path.exists(tp):
        print(name, ": 译文缺失!"); allok = False; continue
    tl = lines(tp)
    secs = [l for l in sl if l.startswith(("○", "△"))]
    miss = [s for s in secs if s not in tl]
    ok = len(tl) >= len(sl) and not miss
    if not ok: allok = False
    print(f"{name}: 原文{len(sl)}行 译文{len(tl)}行 ○△{len(secs)} 缺失{len(miss)} {'OK' if ok else '异常'}")

mg = lines(os.path.join(OUT, "宛署杂记_白话文_全卷合并.txt"))
heads = [l for l in mg if l.startswith("◆")]
print("合并文件: ◆分节", len(heads), "个 | 首节:", heads[0] if heads else "无", "| 末节:", heads[-1] if heads else "无")
print("总体:", "ALL OK" if (allok and len(heads) == 21) else "HAS ISSUES")
