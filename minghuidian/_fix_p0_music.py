# -*- coding: utf-8 -*-
"""P0修复：乐章类NAM从"官职题名"改成"乐章名录" """
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))

MUSIC_KEYWORDS = ["乐章", "之曲", "迎神", "送神", "初献", "亚献", "终献", "彻馔", "送神"]

fixed = 0
for n in nams:
    if n["nam_type"] == "官职题名":
        name = n["name"]
        if any(k in name for k in MUSIC_KEYWORDS) or (len(name) <= 6 and "曲" in name):
            n["nam_type"] = "乐章名录"
            fixed += 1

print(f"修复乐章误判: {fixed} 条")

with open(os.path.join(ROOT, "_layers", "nams.json"), "w", encoding="utf-8") as f:
    json.dump(nams, f, ensure_ascii=False, indent=1)
print("已写回 nams.json")
