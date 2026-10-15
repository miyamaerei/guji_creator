# -*- coding: utf-8 -*-
"""Phase ① 探查（十一）：省级镇兵钱粮清单（国家总账的骨架）+ 运送途径全文扫描"""
import io, re
from collections import Counter

P = r"E:\git\ToolBox\guji\mingshi\mingshi-shihuozhi\食货志.txt"
lines = io.open(P, encoding="utf-8").read().split("\n")
T = "\n".join(lines)

print("### A. 「某镇：主兵/客兵…」型总账段（找行号与全文）")
for i, l in enumerate(lines):
    s = l.strip()
    if re.search(r"(宣府|大同|山西|延绥|宁夏|甘肃|固原|蓟州|辽东|保定|密云|昌平|易州)：", s):
        print("  L%-4d [%d字] %s" % (i+1, len(s), s[:200]))
        print()

print()
print("### B. 运送途径相关句（陆运/水运/车运/递运/程限）")
for i, l in enumerate(lines):
    s = l.strip()
    if re.search(r"(运道|水次|輓运|车运|递运|海运饷|运船|遮洋|浅船|漕河)", s):
        print("  L%-4d %s" % (i+1, s[:160]))

print()
print("### C. 「一县」「每县」型县级税额")
for i, l in enumerate(lines):
    s = l.strip()
    if re.search(r"(一县|每县|县额|县之|有司徵收)", s):
        print("  L%-4d %s" % (i+1, s[:200]))
