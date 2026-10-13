# -*- coding: utf-8 -*-
"""修正：G8卫所并入GEO层 + 从G1/G4提取OFFICIAL官职"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ===== 1. 扩充GEO层：把G8的卫所名录也加进去 =====
geo_existing = json.load(open(os.path.join(ROOT, "_layers", "geo.json"), encoding="utf-8"))

GEO_LEVELS = {
    "布政司": "省",
    "府": "府",
    "州": "州",
    "县": "县",
    "卫": "卫",
    "千户所": "所",
}

def extract_geo(title, original):
    geos = []
    if len(title) < 30:
        parts = re.split(r"[\s　]+", title)
        for p in parts:
            p = p.strip()
            if not p or len(p) < 2:
                continue
            level = None
            for suffix, lv in GEO_LEVELS.items():
                if p.endswith(suffix):
                    level = lv
                    break
            if level:
                geos.append({"name": p, "level": level})
    return geos

# 重新提取GEO：G2户部(14-41) + G8五军都督府卫所(179-180)
new_geo = []
seq = len(geo_existing)  # 接续编号

for iid, item in reg.items():
    vol = int(iid.split("-")[0])
    # G2 户部 + G8 卫所
    if (14 <= vol <= 41) or (179 <= vol <= 180):
        geos = extract_geo(item["title"], item["original"])
        for g in geos:
            seq += 1
            new_geo.append({
                "geo_id": f"GEO-{seq:04d}",
                "item_id": iid,
                "name": g["name"],
                "level": g["level"],
            })

# 合并去重（按 name + item_id）
all_geo = geo_existing + new_geo
seen = set()
unique_geo = []
for g in all_geo:
    key = (g["item_id"], g["name"])
    if key not in seen:
        seen.add(key)
        unique_geo.append(g)

print(f"【GEO 地理区划层】")
print(f"  原有: {len(geo_existing)}条")
print(f"  新增G8卫所: {len(new_geo)}条")
print(f"  合并去重后: {len(unique_geo)}条")

level_dist = Counter(g["level"] for g in unique_geo)
for lv, c in level_dist.most_common():
    print(f"    {lv}: {c}")

# 保存
with open(os.path.join(ROOT, "_layers", "geo.json"), "w", encoding="utf-8") as f:
    json.dump(unique_geo, f, ensure_ascii=False, indent=1)

# ===== 2. 从G1吏部/G4兵部提取OFFICIAL官职 =====
OFFICE_SUFFIXES = [
    "大夫", "郎", "少卿", "寺丞", "主事", "郎中", "员外郎",
    "御史", "都督", "都指挥", "总兵", "副总兵", "参将",
    "尚书", "侍郎", "都御史", "副都御史", "佥都御史",
    "知府", "知州", "知县", "同知", "通判",
    "指挥使", "指挥同知", "指挥佥事", "千户", "百户",
]

def extract_offices_from_text(title, original):
    """从文本中提取官职名"""
    offices = []
    text = title + " " + original
    for suffix in OFFICE_SUFFIXES:
        # 匹配 "XX大夫" "XX郎中" 等
        matches = re.findall(r"([一-龥]{2,8}" + suffix + r")", text)
        for m in matches:
            if len(m) <= 10:  # 排除太长的
                offices.append(m)
    return list(set(offices))  # 去重

# 从G1吏部/G4兵部提取
off_records = []
off_seq = 0

for iid, item in reg.items():
    vol = int(iid.split("-")[0])
    # G1 吏部 + G4 兵部
    if (2 <= vol <= 13) or (106 <= vol <= 129):
        offices = extract_offices_from_text(item["title"], item["original"])
        for off in offices:
            off_seq += 1
            off_records.append({
                "off_id": f"OFF-{off_seq:04d}",
                "item_id": iid,
                "office_name": off,
            })

print(f"\n【OFFICIAL 官职名录层】")
print(f"  提取: {len(off_records)}条")

# 官职名出现频率top20
off_counter = Counter(o["office_name"] for o in off_records)
print(f"  Top20高频官职:")
for name, cnt in off_counter.most_common(20):
    print(f"    {name:12s}: {cnt}")

# 保存
with open(os.path.join(ROOT, "_layers", "offices.json"), "w", encoding="utf-8") as f:
    json.dump(off_records, f, ensure_ascii=False, indent=1)

print(f"\n已保存: geo.json + offices.json")
