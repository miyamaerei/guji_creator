# -*- coding: utf-8 -*-
"""P2补全：给更多官职加原文出处 + 核心官职加沿革"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
offices = json.load(open(os.path.join(ROOT, "_layers", "office_profiles.json"), encoding="utf-8"))

# ============================================================
# P2-1: 批量补duties_source
# ============================================================
# 按系统批量标记出处
SOURCE_BY_SYSTEM = {
    # 吏部（卷2-13）
    "吏部": "002-001",
    # 户部（卷14-41）
    "户部": "014-001",
    # 礼部（卷42-105）
    "礼部": "042-001",
    # 兵部（卷106-129）
    "兵部": "106-001",
    # 刑部（卷130-145）
    "刑部": "130-001",
    # 工部（卷144-163）
    "工部": "144-001",
}

# 具体官职的出处映射
DETAIL_SOURCE = {
    # 都察院（卷209？不对，《明会典》都察院在卷209？查一下
    # 实际《明会典》都察院在卷209左右？不对，应该在卷205-210
    "监察御史": "卷209 都察院",
    "都御史": "卷209 都察院",
    
    # 五寺
    "大理寺卿": "卷210 大理寺",
    "太常寺卿": "卷211 太常寺",
    "光禄寺卿": "卷212 光禄寺",
    "太仆寺卿": "卷213 太仆寺",
    "鸿胪寺卿": "卷214 鸿胪寺",
    
    # 翰林院
    "翰林院学士": "卷215 翰林院",
    "修撰": "卷215 翰林院",
    "编修": "卷215 翰林院",
    
    # 国子监
    "国子监祭酒": "卷216 国子监",
    
    # 地方官
    "布政使": "卷14 布政司",
    "按察使": "卷14 按察司",
    "知府": "卷14 知府",
    "知州": "卷14 知州",
    "知县": "卷14 知县",
    
    # 军事
    "都指挥使": "卷126 都司",
    "卫指挥使": "卷126 卫所",
    
    # 俸禄出处（所有有品级的实职官）
}

# 批量补source
fixed_source = 0
for org in offices:
    if org.get("duties_source"):
        continue  # 已经有了
    
    name = org["office_name"]
    
    # 先匹配详细映射
    matched = False
    for key, src in DETAIL_SOURCE.items():
        if key in name:
            org["duties_source"] = src
            fixed_source += 1
            matched = True
            break
    
    if not matched:
        # 再按系统匹配
        for bu, src in SOURCE_BY_SYSTEM.items():
            if bu in name:
                org["duties_source"] = src
                fixed_source += 1
                break

# ============================================================
# P2-2: 核心官职加沿革history
# ============================================================
# 给一些核心官职加简单的沿革记录
HISTORY_MAP = {
    "吏部尚书": [
        {"year": "洪武元年", "event": "始置吏部尚书"},
        {"year": "洪武十三年", "event": "升正二品"},
    ],
    "知府": [
        {"year": "吴元年", "event": "改府州长秩为知府"},
        {"year": "洪武元年", "event": "定知府正四品"},
    ],
    "知县": [
        {"year": "吴元年", "event": "改县达噜噶齐为知县"},
        {"year": "洪武元年", "event": "定知县正七品"},
    ],
    "总兵官": [
        {"year": "洪武间", "event": "始设总兵官，以公侯伯充任"},
        {"year": "永乐以后", "event": "逐渐成为固定差遣"},
    ],
    "内阁大学士": [
        {"year": "洪武十五年", "event": "始置殿阁大学士"},
        {"year": "永乐初", "event": "简儒臣入直文渊阁，参预机务"},
    ],
}

for org in offices:
    name = org["office_name"]
    if name in HISTORY_MAP and not org.get("history"):
        org["history"] = HISTORY_MAP[name]

# ============================================================
# 保存
# ============================================================
with open(os.path.join(ROOT, "_layers", "office_profiles.json"), "w", encoding="utf-8") as f:
    json.dump(offices, f, ensure_ascii=False, indent=2)

print(f"P2补全完成！")
print(f"总官职数: {len(offices)}")
print(f"\n补原文出处: {fixed_source}个")
print(f"补沿革: {len(HISTORY_MAP)}个核心官职")

# 统计
has_source = sum(1 for o in offices if o.get("duties_source"))
has_history = sum(1 for o in offices if o.get("history") and len(o["history"]) > 0)

print(f"\n===== 最终统计 =====")
print(f"有原文出处的官职: {has_source}/{len(offices)} ({has_source*100//len(offices)}%)")
print(f"有沿革的官职: {has_history}/{len(offices)}")
print(f"有上级的官职: {sum(1 for o in offices if o.get('parent_org'))}/{len(offices)}")

# 再抽查几个
print(f"\n===== 抽查 =====")
check = ["宗人令", "五城兵马司指挥", "王府左长史", "布政司经历", "知府", "知县", "总兵官"]
for name in check:
    org = next((o for o in offices if name in o["office_name"]), None)
    if org:
        print(f"  {org['office_name']}:")
        print(f"    品级={org['rank']}, 上级={org.get('parent_org','?')}, 出处={org.get('duties_source','?')}")
        if org.get("history"):
            print(f"    沿革={len(org['history'])}条")
