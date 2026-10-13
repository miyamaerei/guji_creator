# -*- coding: utf-8 -*-
"""把校准结果写回 _src 源数据文件"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 遍历 _src 目录下所有 rules 文件，批量校准
src_dir = os.path.join(ROOT, "_src")
fixed_count = 0

for fname in os.listdir(src_dir):
    if not fname.endswith(".py") or "rules" not in fname:
        continue
    fpath = os.path.join(src_dir, fname)
    with open(fpath, encoding="utf-8") as f:
        content = f.read()

    # 简单替换：type = "义务" → 根据内容判断
    # 这里只做标记校准，类型校准需要看原文
    # 先做 source_marker 校准
    new_content = content
    # 找出所有 RECORDS = [...] 块
    # 太复杂，直接重新生成 rules 源数据

print("需要重新生成 rules 源数据")

# 方案：直接从 _layers/rules.json 反向生成 _src 文件
rules = json.load(open(os.path.join(ROOT, "_layers", "rules.json"), encoding="utf-8"))

# 按 item_id 分组
by_vol = {}
for r in rules:
    vol = int(r["item_id"].split("-")[0])
    by_vol.setdefault(vol, []).append(r)

for vol, recs in by_vol.items():
    # 清理 None 值
    cleaned = []
    for r in recs:
        cr = {k: v for k, v in r.items() if v is not None}
        cleaned.append(cr)
    outpath = os.path.join(src_dir, f"_rules_ai_calibrated_{vol:03d}.py")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write(f'"""校准后：卷{vol} 规则"""\n\n')
        f.write("RECORDS = ")
        json.dump(cleaned, f, ensure_ascii=False, indent=1, default=str)
    fixed_count += len(cleaned)

print(f"已生成 {len(by_vol)} 个校准后规则文件，共 {fixed_count} 条")
