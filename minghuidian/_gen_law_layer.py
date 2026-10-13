# -*- coding: utf-8 -*-
"""设计并批量生成法律条文层（LAW）"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))

# ===== 法律条文层 schema 设计 =====
# law_id: LAW-NNN
# item_id: 原文条目
# crime: 罪名（如"鬬殴"、"盗卖田宅"）
# crime_category: 罪名大类（贼盗/人命/鬬殴/骂詈/诉讼/受赃/诈伪/犯奸/杂犯/捕亡/断狱）
# punishment_type: 处罚类型（笞/杖/徒/流/死/充军/罢职/为民）
# punishment_level: 处罚等级（如"一百"、"三等"）
# condition: 适用条件（AI解读）
# source_law: 出处（明律/大诰/条例/奏准）
# relevant_orgs: 相关机构（刑部/都察院/大理寺）
# original: 原文片段

print("=" * 60)
print("法律条文层（LAW）批量提取")
print("=" * 60)

# 罪名大类映射
CRIME_CATEGORY = {
    "贼盗": ["谋反", "谋大逆", "谋叛", "恶逆", "不道", "盗", "劫", "贼"],
    "人命": ["杀人", "谋杀", "故杀", "斗殴杀", "过失杀"],
    "鬬殴": ["鬬殴", "殴", "打", "伤"],
    "骂詈": ["骂", "詈", "毁骂"],
    "诉讼": ["诉讼", "告状", "告", "诬告"],
    "受赃": ["受赃", "贪", "贿", "纳贿"],
    "诈伪": ["诈伪", "诈", "伪造", "假印"],
    "犯奸": ["奸", "奸淫", "和奸", "强奸"],
    "杂犯": ["杂犯", "赌博", "阉割"],
    "捕亡": ["捕亡", "逃", "逃亡", "越狱"],
    "断狱": ["断狱", "断罪", "听讼"],
    "户婚": ["户婚", "婚姻", "田宅", "钱粮", "户口"],
    "贼盗": ["谋反", "谋叛", "强盗", "窃盗"],
}

def classify_crime(subject):
    """根据subject判断罪名大类"""
    for cat, keywords in CRIME_CATEGORY.items():
        for kw in keywords:
            if kw in subject:
                return cat
    return "其他"

# 处罚类型提取
PUNISHMENT_PATTERNS = [
    (r"笞\s*([一二三四五六七八九十百\d]+)\s*下", "笞"),
    (r"杖\s*([一二三四五六七八九十百\d]+)\s*下", "杖"),
    (r"徒\s*([一二三四五六五\d]+)\s*年", "徒"),
    (r"流\s*([二三千]?)\s*里", "流"),
    (r"充军", "充军"),
    (r"死刑", "死"),
    (r"罢职", "罢职"),
    (r"为民", "为民"),
]

def extract_punishment(text):
    """从原文提取处罚"""
    for pattern, ptype in PUNISHMENT_PATTERNS:
        m = re.search(pattern, text)
        if m:
            level = m.group(1) if m.lastindex else ""
            return ptype, level
    return None, None

# 出处识别
def extract_source(text):
    if "大明律" in text or "明律" in text:
        return "大明律"
    elif "大诰" in text:
        return "大诰"
    elif "奏准" in text:
        return "奏准条例"
    elif "洪武" in text and "令" in text:
        return "洪武令"
    return "未明"

# 批量提取
laws = []
seq = 0

# 只处理G5刑部的规则（卷130-143）
for r in rules:
    vol = int(r["item_id"].split("-")[0])
    if not (130 <= vol <= 143):
        continue

    iid = r["item_id"]
    original = reg[iid]["original"]
    subject = r.get("subject", "")

    # 只处理看起来像罪名的subject
    # 罪名特征：不是机构名（不以部/院/寺结尾），且短
    if subject.endswith(("部", "院", "寺", "监", "司", "府")):
        continue
    if len(subject) > 10:
        continue

    seq += 1
    ptype, plevel = extract_punishment(original)
    source = extract_source(original)
    category = classify_crime(subject)

    laws.append({
        "law_id": f"LAW-{seq:03d}",
        "item_id": iid,
        "crime": subject,
        "crime_category": category,
        "punishment_type": ptype or "未明",
        "punishment_level": plevel or "",
        "source_law": source,
        "relevant_orgs": ["刑部"],
        "original": original[:80],
    })

print(f"\n提取法律条文: {len(laws)} 条")

# 统计
print("\n=== 罪名大类分布 ===")
cat_dist = Counter(l["crime_category"] for l in laws)
for c, n in cat_dist.most_common():
    print(f"  {c:10s}: {n:3d}")

print("\n=== 处罚类型分布 ===")
pun_dist = Counter(l["punishment_type"] for l in laws)
for p, n in pun_dist.most_common():
    print(f"  {p:10s}: {n:3d}")

print("\n=== 出处分布 ===")
src_dist = Counter(l["source_law"] for l in laws)
for s, n in src_dist.most_common():
    print(f"  {s:10s}: {n:3d}")

# 保存
outpath = os.path.join(ROOT, "_layers", "laws.json")
with open(outpath, "w", encoding="utf-8") as f:
    json.dump(laws, f, ensure_ascii=False, indent=1)
print(f"\n已保存: {outpath}")

# 抽样
print("\n=== 抽样3条 ===")
for l in laws[:3]:
    print(f"\n{l['law_id']} ({l['item_id']})")
    print(f"  罪名: {l['crime']} ({l['crime_category']})")
    print(f"  处罚: {l['punishment_type']} {l['punishment_level']}")
    print(f"  出处: {l['source_law']}")
    print(f"  原文: {l['original'][:50]}...")
