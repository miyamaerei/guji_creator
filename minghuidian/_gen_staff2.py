# -*- coding: utf-8 -*-
"""批量生成 NAM：含人员配置的衙门"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

def cn2num(s):
    cn = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
    if s.isdigit():
        return int(s)
    if s in cn:
        return cn[s]
    if "十" in s:
        parts = s.split("十")
        tens = cn.get(parts[0], 1) if parts[0] else 1
        ones = cn.get(parts[1], 0) if len(parts) > 1 and parts[1] else 0
        return tens * 10 + ones
    return 0

records = []
seq = 0

for iid, item in reg.items():
    original = item["original"]
    title = item["title"]
    matches = re.findall(r"(司吏|典吏|吏目|攒典|令史|书吏)\s*([一二三四五六七八九十百\d]+)\s*名", original)
    if not matches:
        continue
    if len(title) > 15 or title.endswith("名"):
        continue

    seq += 1
    staff = [{"role": role, "count": cn2num(count)} for role, count in matches]

    records.append({
        "id": f"NAM-STAFF-{seq:03d}",
        "item_id": iid,
        "name": title,
        "nam_type": "人员配置",
        "scope": "户部",
        "entries": [{"seq": i+1, "office": s["role"], "count": s["count"]} for i, s in enumerate(staff)],
        "staff_config": staff,
    })

print(f"生成 {len(records)} 条人员配置 NAM")

outpath = os.path.join(ROOT, "_src", "_nam_ai_staff_auto.py")
with open(outpath, "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动生成：部门人员配置"""\n\n')
    f.write("RECORDS = ")
    json.dump(records, f, ensure_ascii=False, indent=1)
print(f"已写入 {outpath}")
