# -*- coding: utf-8 -*-
"""批量生成实体源数据：从 NAM 中提取衙门名"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 读取现有实体
src_dir = os.path.join(ROOT, "_src")
existing_names = set()
for f in os.listdir(src_dir):
    if f.startswith("_ents_ai_") and f.endswith(".py"):
        import importlib.util
        spec = importlib.util.spec_from_file_location("m", os.path.join(src_dir, f))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for r in m.RECORDS:
            existing_names.add(r["text"])

# 读取 NAM
nams = json.load(open(os.path.join(ROOT, "_layers", "nams.json"), encoding="utf-8"))

ORG_SUFFIX = ["部", "院", "寺", "监", "司", "府", "卫", "所", "局", "仓", "库", "厂", "署"]

new_ents = []
seen = set()

for n in nams:
    name = n["name"]
    if name in existing_names or name in seen:
        continue
    if any(name.endswith(s) for s in ORG_SUFFIX):
        seen.add(name)
        new_ents.append({
            "item_id": n["item_id"],
            "text": name,
            "type": "institution",
            "rank_order": "未明",
            "confidence": "medium",
        })

print(f"新提取实体: {len(new_ents)} 条")

# 写入源数据
outpath = os.path.join(src_dir, "_ents_ai_auto_g4.py")
with open(outpath, "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动生成：批量实体"""\n\n')
    f.write("RECORDS = ")
    json.dump(new_ents, f, ensure_ascii=False, indent=1)
print(f"已写入 {outpath}")
