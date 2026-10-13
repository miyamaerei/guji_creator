# -*- coding: utf-8 -*-
"""把org_profiles改成规范的数组+key/value格式"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# ===== 标准格式转换 =====
def parse_staff_to_array(staff_text):
    """把编制文本转成数组"""
    if not staff_text:
        return []

    # 解析类似 "尚书1人，左右侍郎各1人，文选/验封/稽勋/考功4司各郎中1人..."
    items = []

    # 简单拆分
    parts = re.split(r"[，。、]", staff_text)
    for part in parts:
        part = part.strip()
        if not part:
            continue

        # 尝试提取官职名和人数
        # 格式："尚书1人"、"左右侍郎各1人"、"郎中1人"
        match = re.match(r"(.+?)(各)?(\d+)人", part)
        if match:
            role = match.group(1).strip()
            count = int(match.group(3))
            items.append({"role": role, "count": count})
        else:
            # 如果解析不了，就原样放
            items.append({"role": part, "count": None})

    return items

def parse_history_to_array(history_text):
    """把沿革文本转成数组"""
    if not history_text:
        return []

    items = []

    # 按"，"或"。"拆分
    parts = re.split(r"[，。；]", history_text)
    for part in parts:
        part = part.strip()
        if not part:
            continue

        # 尝试提取年份和事件
        # 格式："洪武元年始置"、"十三年革中书省后升正二品"
        year_match = re.match(r"(洪武[一二三四五六七八九十百]+年|永乐[一二三四五六七八九十]+年|国初|洪武初)", part)
        if year_match:
            year = year_match.group(1)
            event = part[len(year):].strip()
            items.append({"year": year, "event": event})
        else:
            items.append({"year": None, "event": part})

    return items

# ===== 加载并转换 =====
org_profiles = json.load(open(os.path.join(ROOT, "_layers", "org_profiles.json"), encoding="utf-8"))

for org in org_profiles:
    # 编制：文本 → 数组
    if org.get("staff") and isinstance(org["staff"], str):
        org["staff"] = parse_staff_to_array(org["staff"])

    # 沿革：文本 → 数组
    if org.get("history") and isinstance(org["history"], str):
        org["history"] = parse_history_to_array(org["history"])

# ===== 输出示例 =====
print("=" * 70)
print("格式转换完成，示例：吏部")
print("=" * 70)

libu = [o for o in org_profiles if o["org_name"] == "吏部"][0]
print(f"\n部门: {libu['org_name']}")
print(f"品级: {libu['rank']}")
print(f"\n编制 (staff):")
for s in libu["staff"][:5]:
    print(f"  - {s}")
print(f"  ... 共 {len(libu['staff'])} 项")

print(f"\n沿革 (history):")
for h in libu["history"][:5]:
    print(f"  - {h}")
print(f"  ... 共 {len(libu['history'])} 项")

print(f"\n职责: {libu['duties']}")
print(f"位置: {libu['category']}")

# 保存
with open(os.path.join(ROOT, "_layers", "org_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(org_profiles, f, ensure_ascii=False, indent=2)

print(f"\n已保存：规范格式org_profiles.json")
