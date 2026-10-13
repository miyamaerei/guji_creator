# -*- coding: utf-8 -*-
"""开ENG-MAT工程物料层：承接工部的物料清单"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 物料+数量模式：杉木三百二根 / 苏木一斤 / 砖瓦若干
MATERIAL_PATTERN = re.compile(r"([一二三四五六七八九十百千万零两\d]+)\s*([斤两根个块疋匹丈尺寸石斗升合钱两者艘辆间座所])")

MATERIAL_NAMES = [
    "杉木", "松木", "柏木", "楠木", "樟木", "榆木", "木",
    "砖", "瓦", "石灰", "琉璃",
    "苏木", "颜料", "油漆", "金", "银", "铜", "铁",
    "布", "绢", "罗", "缎", "纱", "纻丝",
    "柴", "炭", "煤",
    "米", "麦", "豆", "草",
    "纸", "墨", "笔",
    "油", "蜡",
]

def extract_material(title, original):
    """提取物料+数量"""
    materials = []
    text = title + " " + original

    # 找物料名+数量的组合
    for name in MATERIAL_NAMES:
        # 匹配 "XX物料 N数量单位"
        pattern = re.compile(name + r"\s*([一二三四五六七八九十百千万零两\d]+)\s*([斤两根个块疋匹丈尺寸石斗升合钱两者艘辆间座所])")
        matches = pattern.findall(text)
        for qty, unit in matches:
            materials.append({
                "material": name,
                "quantity": qty,
                "unit": unit,
            })
    return materials

# 批量提取G6工部（卷146-163）
mat_records = []
mat_seq = 0

for iid, item in reg.items():
    vol = int(iid.split("-")[0])
    if 146 <= vol <= 163:
        materials = extract_material(item["title"], item["original"])
        for m in materials:
            mat_seq += 1
            mat_records.append({
                "mat_id": f"MAT-{mat_seq:04d}",
                "item_id": iid,
                "material": m["material"],
                "quantity": m["quantity"],
                "unit": m["unit"],
            })

print(f"【ENG-MAT 工程物料层】{len(mat_records)} 条")
print()

# 物料分布
mat_dist = Counter(m["material"] for m in mat_records)
print("物料分布 Top15:")
for name, cnt in mat_dist.most_common(15):
    print(f"  {name:8s}: {cnt:4d}条")

# 按卷分布
by_vol = Counter()
for m in mat_records:
    vol = int(m["item_id"].split("-")[0])
    by_vol[vol] += 1

print(f"\n按卷分布:")
for vol in sorted(by_vol.keys()):
    print(f"  卷{vol}: {by_vol[vol]}条")

# 保存
outpath = os.path.join(ROOT, "_layers", "materials.json")
with open(outpath, "w", encoding="utf-8") as f:
    json.dump(mat_records, f, ensure_ascii=False, indent=1)
print(f"\n已保存: {outpath}")
