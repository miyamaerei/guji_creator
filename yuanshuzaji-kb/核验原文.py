# -*- coding: utf-8 -*-
"""核验《宛署杂记》原文拆分结果：文件完整性、标题覆盖、合并结构"""
import os

OUT_DIR = r"E:\git\ToolBox\guji\yuanshuzaji-kb\原文"
CN = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
      "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十"]
FILES = ["自序"] + ["卷" + c for c in CN]


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
    ok = head == "【" + name + "】" and len(ls) >= 2
    if not ok:
        allok = False
    print(f"{name}: 文件行数{len(ls)} 首行{head} ○△标题{len(secs)} {'OK' if ok else '异常'}")

mg = lines(os.path.join(OUT_DIR, "宛署杂记_原文_全卷合并.txt"))
sep = "=" * 60
# 横幅 = 分隔线后的【】行
banners = []
expect_banner = False
for l in mg:
    if l == sep:
        expect_banner = True
    elif expect_banner and l.startswith("【"):
        banners.append(l)
        expect_banner = False
    else:
        expect_banner = False
print("合并文件: 卷横幅", len(banners), "个:", banners)
print("总体:", "ALL OK" if (allok and banners == ["【" + f + "】" for f in FILES]) else "HAS ISSUES")
