# -*- coding: utf-8 -*-
"""核验《福惠全书》白话译文：行数比对、○/△标题覆盖、合并结构"""
import os

SRC = r"E:\git\ToolBox\guji\fuhuiquanshu-kb\原文"
OUT = r"E:\git\ToolBox\guji\fuhuiquanshu-kb\白话文"
CN = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
      "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
      "二十一", "二十二", "二十三", "二十四", "二十五", "二十六", "二十七", "二十八",
      "二十九", "三十", "三十一", "三十二"]
FILES = ["目录", "自序", "凡例"] + ["卷之" + c for c in CN] + ["禀启附"]


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

mg_path = os.path.join(OUT, "福惠全书_白话文_全卷合并.txt")
if not os.path.exists(mg_path):
    mg_path = r"E:\git\ToolBox\guji\fuhuiquanshu-kb\福惠全书_白话文_全卷合并.txt"
mg = lines(mg_path)
heads = [l for l in mg if l.startswith("◆")]
print("合并文件: ◆分篇", len(heads), "个 | 首:", heads[0] if heads else "无", "| 末:", heads[-1] if heads else "无")
print("总体:", "ALL OK" if (allok and len(heads) == 36) else "HAS ISSUES")
