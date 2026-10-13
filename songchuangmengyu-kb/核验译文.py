# -*- coding: utf-8 -*-
"""核验《松窗梦语》白话译文：行数比对、合并结构"""
import os

SRC = r"E:\git\ToolBox\guji\songchuangmengyu-kb\原文"
OUT = r"E:\git\ToolBox\guji\songchuangmengyu-kb\白话文"
FILES = ["宦游纪", "南游纪", "北游纪", "东游纪", "西游纪", "北虏纪", "南夷纪",
         "东倭纪", "西番纪", "士人纪", "三农纪", "百工纪", "商贾纪", "象纬纪",
         "堪舆纪", "祥瑞纪", "灾异纪", "花木纪", "鸟兽纪", "方术纪", "盛遇纪",
         "异闻纪", "先世纪", "梦寐纪", "权势纪", "忠廉纪", "时序纪", "风俗纪",
         "自省纪", "铨部纪", "宗藩纪", "漕运纪", "两粤纪"]


def lines(p):
    with open(p, encoding="utf-8") as f:
        return [l.rstrip("\r\n") for l in f.read().splitlines()]


allok = True
for name in FILES:
    sl = lines(os.path.join(SRC, name + ".txt"))
    tp = os.path.join(OUT, name + "_白话.txt")
    if not os.path.exists(tp):
        print(name, ": 译文缺失!"); allok = False; continue
    tl = lines(tp)
    # 非空行比对
    sln = [l for l in sl if l.strip()]
    tln = [l for l in tl if l.strip()]
    ok = len(tln) >= len(sln) and tl[0].startswith("【")
    if not ok:
        allok = False
    print(f"{name}: 原文非空{len(sln)}行 译文非空{len(tln)}行 {'OK' if ok else '异常'}")

mg = lines(os.path.join(OUT, "松窗梦语_白话文_全卷合并.txt"))
heads = [l for l in mg if l.startswith("◆")]
print("合并文件: ◆分篇", len(heads), "个 | 首:", heads[0] if heads else "无", "| 末:", heads[-1] if heads else "无")
print("总体:", "ALL OK" if (allok and len(heads) == 33) else "HAS ISSUES")
