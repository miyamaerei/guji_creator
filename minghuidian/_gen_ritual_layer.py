# -*- coding: utf-8 -*-
"""设计并批量生成礼仪流程层（RIT）"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))

# ===== 礼仪流程层 schema =====
# ritual_id: RIT-NNN
# item_id: 原文条目
# ritual_type: 礼仪大类（祭祀/朝会/冠礼/婚礼/丧礼/册命/巡幸/宴飨/科举）
# ritual_name: 具体礼仪名（如"郊祀"、"太庙时享"、"皇太子冠礼"）
# participants: 参与机构/人员
# timing: 时间节点（前期几日/正日）
# location: 地点（奉天殿/太庙/天坛）
# source: 出处（洪武礼制/明集礼/奏准）
# original: 原文片段

print("=" * 60)
print("礼仪流程层（RIT）批量提取")
print("=" * 60)

# 礼仪大类关键词
RITUAL_TYPES = {
    "祭祀": ["郊祀", "天坛", "地坛", "太庙", "宗庙", "社稷", "籍田", "先农", "释奠", "孔子", "庙享", "时享", "祫祭", "禘祭"],
    "朝会": "朝会 正旦 冬至 万寿圣节 朝贺 常朝 御殿".split(),
    "冠礼": ["冠礼", "冠", "加冠", "醮礼"],
    "婚礼": ["婚礼", "纳征", "纳采", "亲迎", "册妃", "纳妃"],
    "丧礼": ["丧礼", "丧仪", "丧", "丧葬", "谥", "册谥"],
    "册命": ["册宝", "册立", "册封", "册皇太子", "册亲王", "册皇后"],
    "巡幸": ["巡幸", "巡狩", "出巡", "谒陵", "耕籍"],
    "宴飨": ["宴飨", "宴", "赐宴", "大宴", "中宴", "小宴"],
    "科举": ["科举", "会试", "殿试", "乡试", "传胪", "金榜"],
    "卤簿": ["卤簿", "仪仗", "仪卫", "车驾", "驾"],
}

def classify_ritual(title, original):
    """根据标题和原文判断礼仪类型"""
    text = title + original
    for rtype, keywords in RITUAL_TYPES.items():
        for kw in keywords:
            if kw in text:
                return rtype, kw
    return "其他", ""

# 地点提取
LOCATIONS = ["奉天殿", "华盖殿", "谨身殿", "文华殿", "武英殿", "太庙", "天坛", "地坛",
             "社稷坛", "先农坛", "奉天门外", "奉天门", "皇极殿", "中极殿", "建极殿"]

def extract_location(text):
    for loc in LOCATIONS:
        if loc in text:
            return loc
    return "未明"

# 参与机构提取
ORGS = ["太常寺", "光禄寺", "鸿胪寺", "礼部", "翰林院", "钦天监", "太医院",
        "锦衣卫", "五军都督府", "宗人府", "六部"]

def extract_participants(text):
    found = []
    for org in ORGS:
        if org in text:
            found.append(org)
    return found if found else ["未明"]

# 出处识别
def extract_source(text):
    if "洪武礼制" in text:
        return "洪武礼制"
    elif "明集礼" in text:
        return "明集礼"
    elif "奏准" in text:
        return "奏准"
    elif "永乐" in text and "定" in text:
        return "永乐定"
    elif "洪武" in text and "定" in text:
        return "洪武定"
    return "未明"

# 批量提取（只处理G3礼部卷：42-105）
rituals = []
seq = 0

for iid, item in reg.items():
    vol = int(iid.split("-")[0])
    if not (42 <= vol <= 105):
        continue

    title = item["title"]
    original = item["original"]

    # 过滤太短的（不到20字的不算礼仪流程）
    if len(original) < 30:
        continue

    rtype, keyword = classify_ritual(title, original)

    # 只保留能识别出具体礼仪类型的（"其他"太多了）
    if rtype == "其他":
        continue

    seq += 1
    rituals.append({
        "ritual_id": f"RIT-{seq:03d}",
        "item_id": iid,
        "ritual_type": rtype,
        "ritual_name": keyword,
        "location": extract_location(original),
        "participants": extract_participants(original),
        "source": extract_source(original),
        "original": original[:80],
    })

print(f"\n提取礼仪流程: {len(rituals)} 条")

# 统计
print("\n=== 礼仪大类分布 ===")
type_dist = Counter(r["ritual_type"] for r in rituals)
for t, n in type_dist.most_common():
    print(f"  {t:8s}: {n:3d}")

print("\n=== 地点分布 ===")
loc_dist = Counter(r["location"] for r in rituals)
for l, n in loc_dist.most_common(10):
    print(f"  {l:10s}: {n:3d}")

print("\n=== 出处分布 ===")
src_dist = Counter(r["source"] for r in rituals)
for s, n in src_dist.most_common():
    print(f"  {s:10s}: {n:3d}")

# 保存
outpath = os.path.join(ROOT, "_layers", "rituals.json")
with open(outpath, "w", encoding="utf-8") as f:
    json.dump(rituals, f, ensure_ascii=False, indent=1)
print(f"\n已保存: {outpath}")

# 抽样
print("\n=== 抽样3条 ===")
for r in rituals[:3]:
    print(f"\n{r['ritual_id']} ({r['item_id']})")
    print(f"  类型: {r['ritual_type']} - {r['ritual_name']}")
    print(f"  地点: {r['location']}")
    print(f"  参与: {r['participants']}")
    print(f"  出处: {r['source']}")
    print(f"  原文: {r['original'][:50]}...")
