# -*- coding: utf-8 -*-
"""核验《福惠全书》原文拆分结果：文件完整性、标题覆盖、合并结构"""
import os

OUT_DIR = r"E:\git\ToolBox\guji\fuhuiquanshu-kb\原文"
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
    fp = os.path.join(OUT_DIR, name + ".txt")
    if not os.path.exists(fp):
        print(name, ": 缺失!")
        allok = False
        continue
    ls = lines(fp)
    head = ls[0]
    secs = [l for l in ls if l.startswith(("○", "△"))]
    ok = head.startswith("【") and len(ls) >= 2
    if not ok:
        allok = False
    print(f"{name}: 行数{len(ls)} 首行{head[:18]} ○△标题{len(secs)} {'OK' if ok else '异常'}")

mg = lines(os.path.join(OUT_DIR, "福惠全书_原文_全卷合并.txt"))
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
print("合并文件: 卷横幅", len(banners), "个")
print("总体:", "ALL OK" if allok and len(banners) == 36 else "HAS ISSUES")
