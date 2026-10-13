# -*- coding: utf-8 -*-
"""从原文逐条提取官职名 - 人工标注版"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# ===== 官职名模式 =====
# 明代常见官职后缀
OFFICE_SUFFIXES = [
    "尚书", "侍郎", "郎中", "员外郎", "主事",
    "都御史", "副都御史", "佥都御史", "御史",
    "大理寺卿", "少卿", "寺丞",
    "通政使", "通政副使",
    "太常寺卿", "太常寺少卿",
    "光禄寺卿", "光禄寺少卿",
    "鸿胪寺卿", "鸿胪寺少卿",
    "太仆寺卿", "太仆寺少卿",
    "祭酒", "司业",
    "学士", "侍读", "侍讲", "修撰", "编修", "检讨",
    "布政使", "按察使", "知府", "知州", "知县",
    "都督", "都指挥", "总兵", "副总兵", "参将",
    "宗人令", "宗正", "宗人",
]

def extract_offices_from_text(text):
    """从文本中提取官职名"""
    offices = []
    for suffix in OFFICE_SUFFIXES:
        # 找 "XX+suffix" 的模式
        pattern = r"([一-龥]{1,6}" + suffix + r")"
        matches = re.findall(pattern, text)
        for m in matches:
            # 过滤掉明显不对的
            if len(m) >= 2 and len(m) <= 8:
                # 不能包含动词/虚词
                if not any(kw in m for kw in ["设", "改", "置", "革", "为", "以", "于", "后", "又", "复", "凡", "一", "先", "后"]):
                    offices.append(m)
    return list(set(offices))

# ===== 逐卷提取 =====
all_offices = []
office_items = {}  # office -> [item_ids]

# 先处理G1吏部（卷2-13）
for vol in range(2, 14):
    items = [(iid, item) for iid, item in reg.items() if int(iid.split("-")[0]) == vol]
    for iid, item in items:
        text = item["title"] + " " + item["original"]
        offices = extract_offices_from_text(text)
        for off in offices:
            all_offices.append(off)
            if off not in office_items:
                office_items[off] = []
            office_items[off].append(iid)

print(f"【G1吏部 官职名提取】")
print(f"  共提取: {len(all_offices)} 个官职名（含重复）")
print(f"  去重后: {len(office_items)} 个不同官职名")
print(f"\n  官职名列表（按出现次数排序）:")

office_count = Counter(all_offices)
for off, cnt in office_count.most_common(50):
    print(f"    {off:20s} ({cnt}次, 来自{len(office_items[off])}条)")

# 保存
offices_data = []
for off, cnt in office_count.most_common():
    offices_data.append({
        "office_name": off,
        "count": cnt,
        "source_items": office_items[off],
    })

with open(os.path.join(ROOT, "_layers", "offices_manual.json"), "w", encoding="utf-8") as f:
    json.dump(offices_data, f, ensure_ascii=False, indent=1)

print(f"\n已保存: _layers/offices_manual.json")
