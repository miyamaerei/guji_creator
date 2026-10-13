# -*- coding: utf-8 -*-
"""批量生成引用源数据：识别典籍直引段"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

CIT_BOOKS = ["诸司职掌", "明集礼", "皇明祖训", "大诰", "大明令", "洪武礼制", "大明律", "礼记", "周礼", "仪礼"]

# 读取现有引用
src_dir = os.path.join(ROOT, "_src")
covered_items = set()
for f in os.listdir(src_dir):
    if f.startswith("_cit_ai_") and f.endswith(".py"):
        import importlib.util
        spec = importlib.util.spec_from_file_location("m", os.path.join(src_dir, f))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        for r in m.RECORDS:
            covered_items.add(r["item_id"])

new_cits = []
seq = len(covered_items)

for iid, item in reg.items():
    if iid in covered_items:
        continue
    original = item["original"]
    for book in CIT_BOOKS:
        if book in original:
            seq += 1
            new_cits.append({
                "id": f"CIT-{seq:03d}",
                "item_id": iid,
                "cited_work": book,
                "citation_type": "直引",
                "context": "典籍直引",
            })
            break

print(f"新提取引用: {len(new_cits)} 条")

# 写入源数据
outpath = os.path.join(src_dir, "_cit_ai_auto.py")
with open(outpath, "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动生成：典籍引用"""\n\n')
    f.write("RECORDS = ")
    json.dump(new_cits, f, ensure_ascii=False, indent=1)
print(f"已写入 {outpath}")
