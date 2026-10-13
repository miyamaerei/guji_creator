# -*- coding: utf-8 -*-
"""核验《松窗梦语》原文拆分结果"""
import os

OUT_DIR = r"E:\git\ToolBox\guji\songchuangmengyu-kb\原文"
FILES = ["宦游纪", "南游纪", "北游纪", "东游纪", "西游纪", "北虏纪", "南夷纪",
         "东倭纪", "西番纪", "士人纪", "三农纪", "百工纪", "商贾纪", "象纬纪",
         "堪舆纪", "祥瑞纪", "灾异纪", "花木纪", "鸟兽纪", "方术纪", "盛遇纪",
         "异闻纪", "先世纪", "梦寐纪", "权势纪", "忠廉纪", "时序纪", "风俗纪",
         "自省纪", "铨部纪", "宗藩纪", "漕运纪", "两粤纪"]


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
    ok = ls[0] == "【" + name + "】" and len(ls) >= 2
    if not ok:
        allok = False
    print(f"{name}: 行数{len(ls)} 首行{ls[0]} {'OK' if ok else '异常'}")

mg = lines(os.path.join(OUT_DIR, "松窗梦语_原文_全卷合并.txt"))
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
print("总体:", "ALL OK" if (allok and banners == ["【" + f + "】" for f in FILES]) else "HAS ISSUES")
