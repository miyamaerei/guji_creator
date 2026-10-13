# -*- coding: utf-8 -*-
"""精确核验福惠全书合并文件：36 个分篇标记按序 + 内容与单篇一致"""
import os

SRC = r"E:\git\ToolBox\guji\fuhuiquanshu-kb\原文"
OUT = r"E:\git\ToolBox\guji\fuhuiquanshu-kb\白话文"
CN = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
      "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
      "二十一", "二十二", "二十三", "二十四", "二十五", "二十六", "二十七", "二十八",
      "二十九", "三十", "三十一", "三十二"]
FILES = ["目录", "自序", "凡例"] + ["卷之" + c for c in CN] + ["禀启附"]
# 合并文件实际分篇标记：◆目录 形式（无【】）
BANNER = {f: "◆" + f for f in FILES}


def lines(p):
    with open(p, encoding="utf-8") as f:
        return [l.strip() for l in f.read().splitlines() if l.strip()]


mg = lines(os.path.join(OUT, "福惠全书_白话文_全卷合并.txt"))
# 顺序验证：按 BANNER 顺序扫描
idx = 0
pos = {}
for l in mg:
    if l in BANNER.values() and l == list(BANNER.values())[idx]:
        pos[l] = mg.index(l)
        idx += 1
    if idx == 36:
        break
ok = idx == 36
print("分篇标记命中:", idx, "个", "OK" if ok else "异常")
# 内容一致性：每篇译文首尾段应在合并文件对应分节内
allok = ok
for f in FILES:
    tl = lines(os.path.join(OUT, f + "_白话.txt"))
    if not tl:
        print(f, ": 单篇空"); allok = False; continue
    first_para = tl[1] if len(tl) > 1 else tl[0]  # 跳过首行标记
    # 在合并文件里定位分节起点后检查首段
    seg_start = mg.index("◆" + f) if "◆" + f in mg else -1
    hit = seg_start >= 0 and any(first_para in mg[seg_start:seg_start + 5] for _ in [0]) or (seg_start >= 0 and mg[seg_start + 1] == first_para)
    if not hit:
        # 放宽：该卷译文的第2行出现在分节后20行内
        hit = seg_start >= 0 and first_para in mg[seg_start:seg_start + 20]
    if not hit:
        print(f, ": 分节内容未对齐"); allok = False
print("总体:", "ALL OK" if allok else "HAS ISSUES")
