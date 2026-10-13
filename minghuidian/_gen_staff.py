# -*- coding: utf-8 -*-
"""批量提取人员配置：从卷6/7切分结果里识别"X名"格式，生成 staff_config 条目"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 已覆盖的 item_id
covered = set()
for layer in ["ents", "rules", "nams", "cits"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        for r in json.load(open(p, encoding="utf-8")):
            covered.add(r["item_id"])

# 吏职识别正则
STAFF_PATTERN = re.compile(r"^(提控|都吏|掾史|令史|司吏|典吏|攒典|承发|门吏|狱典)")

records = []
seq = 0

for vol in [6, 7]:
    vol_items = sorted([iid for iid in reg if int(iid.split("-")[0]) == vol and iid not in covered])
    current_yamen = None
    current_staff = []

    for iid in vol_items:
        title = reg[iid]["title"]
        body = reg[iid]["original"]

        # 衙门名：短行（<8字），不含"凡"/年号
        is_yamen = (len(title) <= 8
                    and not title.startswith(("凡", "国初"))
                    and not re.match(r"^(洪武|永乐|宣德|正统|成化|弘治)", title)
                    and not STAFF_PATTERN.match(title))

        if is_yamen:
            # 保存上一条
            if current_yamen and current_staff:
                seq += 1
                records.append({
                    "id": f"NAM-STAFF-{vol:03d}-{seq:03d}",
                    "item_id": f"{vol:03d}-{current_yamen[1]:03d}",
                    "name": f"{current_yamen[0]}·人员配置",
                    "nam_type": "人员配置",
                    "scope": "吏部",
                    "staff_config": current_staff,
                })
            current_yamen = (title, int(iid.split("-")[1]))
            current_staff = []
        else:
            # 提取吏职
            m = STAFF_PATTERN.match(title)
            if m:
                role = m.group(1)
                # 从 body 提取人数
                count_m = re.search(r"(\d+|几拾几|各[一二三四五六七八九十]+|后革|后添设)", body)
                count = count_m.group(1) if count_m else "未明"
                current_staff.append({"role": role, "count": count})

    # 最后一条
    if current_yamen and current_staff:
        seq += 1
        records.append({
            "id": f"NAM-STAFF-{vol:03d}-{seq:03d}",
            "item_id": f"{vol:03d}-{current_yamen[1]:03d}",
            "name": f"{current_yamen[0]}·人员配置",
            "nam_type": "人员配置",
            "scope": "吏部",
            "staff_config": current_staff,
        })

print(f"提取 {len(records)} 条人员配置")
# 写入
with open(os.path.join(ROOT, "_src", "_nam_ai_staff_06_07.py"), "w", encoding="utf-8") as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write('"""自动提取：卷6/7 部门人员配置"""\n\n')
    f.write("RECORDS = ")
    json.dump(records, f, ensure_ascii=False, indent=1)
print("已写入 _nam_ai_staff_06_07.py")
