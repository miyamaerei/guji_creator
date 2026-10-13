# -*- coding: utf-8 -*-
"""
《治谱》原文拆分脚本
- 输入：E:\git\ToolBox\guji\zhipu-kb\治谱.txt（OCR 文本，4985 行）
- 按卷标记行号切分为 12 个文件，忠实保留原始 OCR 文本（含 ○ 句读符号、竖排断行、错字）
- 输出：原文\<卷名>.txt + 全卷合并文件
"""
import os

SRC = r"E:\git\ToolBox\guji\zhipu-kb\治谱.txt"
OUT_DIR = r"E:\git\ToolBox\guji\zhipu-kb\原文"

# (卷名, 起始行, 结束行(不含)) —— 行号经探查确认
VOLS = [
    ("序言目录", 0, 7),
    ("卷之一", 7, 51),
    ("卷之二", 51, 591),
    ("卷之三", 591, 611),
    ("卷之四", 611, 1445),
    ("卷之五", 1445, 2059),
    ("卷之六", 2059, 2319),
    ("卷之七", 2319, 2883),
    ("卷之八", 2883, 2892),
    ("卷之九", 2892, 3398),
    ("卷之十", 3398, 4206),
    ("卷之十补遗", 4206, 4985),
]

with open(SRC, encoding="utf-8") as f:
    lines = f.read().splitlines()

os.makedirs(OUT_DIR, exist_ok=True)

merged = []
merged.append("治谱（原文全卷合并）")
merged.append("（明·佘自强 撰，官箴书，OCR 扫描文本：序言目录、卷一至卷十及卷十补遗按原书顺序合并，保留原始句读符号与竖排断行，未校对）")
merged.append("")

sep = "=" * 60
for name, s, e in VOLS:
    seg = lines[s:e]
    paras = [l.rstrip() for l in seg]
    fpath = os.path.join(OUT_DIR, name + ".txt")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write("\n".join(paras))
    merged.append(sep)
    merged.append("【" + name + "】")
    merged.append(sep)
    merged.append("")
    merged.extend(paras)
    merged.append("")
    chars = sum(len(l) for l in paras)
    nonempty = sum(1 for l in paras if l.strip())
    print(f"写出 {name}.txt 行{len(paras)} 非空{nonempty} 字符{chars}")

with open(os.path.join(OUT_DIR, "治谱_原文_全卷合并.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(merged))
print("合并文件已写出 | 总字符:", sum(len(l) for l in merged))
