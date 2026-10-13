# -*- coding: utf-8 -*-
"""P1：重新分类RUL type"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))

# 重新分类规则
fixed = Counter()
for r in rules:
    iid = r["item_id"]
    original = reg.get(iid, {}).get("original", "")

    if r["type"] == "义务" and original:
        # 禁止类关键词
        if re.search(r"不许|毋得|毋|勿|不得|不准|禁止", original):
            r["type"] = "禁止"
            fixed["义务→禁止"] += 1
        # 时限类关键词
        elif re.search(r"限.*日|限.*月|三年考满|六年考察", original):
            r["type"] = "时限"
            fixed["义务→时限"] += 1
        # 处罚类关键词
        elif re.search(r"笞|杖|徒|流|充军|罢职|为民", original):
            r["type"] = "处罚"
            fixed["义务→处罚"] += 1
        # 程序类关键词
        elif re.search(r"先.*后|由.*官.*奏|行.*部.*覆", original):
            r["type"] = "程序"
            fixed["义务→程序"] += 1

print("重新分类结果:")
for k, c in fixed.most_common():
    print(f"  {k}: {c} 条")

# 统计新的分布
types = Counter(r["type"] for r in rules)
print("\n新类型分布:")
for t, c in types.most_common():
    print(f"  {t}: {c} ({c*100//len(rules)}%)")

with open(os.path.join(ROOT, "_layers", "rules.json"), "w", encoding="utf-8") as f:
    json.dump(rules, f, ensure_ascii=False, indent=1)
print("\n已写回")
