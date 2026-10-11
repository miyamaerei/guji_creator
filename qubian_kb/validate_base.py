# -*- coding: utf-8 -*-
"""底座验证 validate_base.py —— 独立回读校验（写文件输出，不依赖 stdout）"""
import json
import os
import re

OUT_DIR = os.path.dirname(os.path.abspath(__file__))  # 项目根：脚本自身位置推导
REPORT = os.path.join(OUT_DIR, "base_验证缺漏清单.txt")
errors = []
warns = []

with open(os.path.join(OUT_DIR, "_item_registry.json"), encoding="utf-8") as f:
    reg = json.load(f)

# 1. 条数
total = len(reg)
if total != 76:
    errors.append(f"总条数={total}，应为 76")
else:
    warns.append(f"总条数={total} OK")

# 2. key 唯一 + item_id 格式
keys = list(reg.keys())
if len(set(keys)) != len(keys):
    errors.append("存在重复 key")
for k in keys:
    if not re.fullmatch(r"\d{2}-\d{3}", k):
        errors.append(f"非法 item_id: {k}")

# 3. 入层计数（卷01-20）
in_layer = sum(1 for v in reg.values() if v.get("in_layer"))
if in_layer != 71:
    errors.append(f"入层条数={in_layer}，应为 71")
else:
    warns.append(f"入层条数={in_layer} OK（卷01-20）")

# 4. 试点条目 title 核对
pilot = {
    "01-001": "嘉靖三十八年己未（1559年），七月三十日，亥时，余生。",
    "02-001": "万历三十一年癸卯（1603年），余四十五岁。",
    "15-001": "天启三年癸亥（1623年），余六十五岁。",
    "20-001": "天启七年丁卯（1627年），余六十九岁。",
}
for pid, expected in pilot.items():
    if pid not in reg:
        errors.append(f"试点条目缺失: {pid}")
    elif reg[pid].get("title", "")[:20] != expected[:20]:
        errors.append(f"试点条目 title 不符 {pid}: {reg[pid].get('title','')[:30]}")

# 5. 卷内条号连续性（每卷 001..N）
per_vol = {}
for k in keys:
    vol = k.split("-")[0]
    per_vol.setdefault(vol, []).append(int(k.split("-")[1]))
for vol, seqs in per_vol.items():
    seqs.sort()
    if seqs != list(range(1, len(seqs) + 1)):
        errors.append(f"卷 {vol} 条号不连续: {seqs}")

# 6. _extract 文件条数合计 = 76
ext_dir = os.path.join(OUT_DIR, "_extract")
ext_total = 0
ext_files = {}
for fn in sorted(os.listdir(ext_dir)):
    if not fn.endswith(".txt"):
        continue
    with open(os.path.join(ext_dir, fn), encoding="utf-8-sig") as f:
        n = sum(1 for line in f if line.startswith("条") and "|" in line)
    ext_total += n
    ext_files[fn] = n
if ext_total != 76:
    errors.append(f"_extract 条数合计={ext_total}，应为 76")
else:
    warns.append(f"_extract 条数合计={ext_total} OK（{len(ext_files)} 个卷文件）")

# 7. volume_summary 核对
with open(os.path.join(OUT_DIR, "volume_summary.csv"), encoding="utf-8-sig") as f:
    lines = f.read().strip().splitlines()
if len(lines) != 23 + 1:  # 头 + 00/01-20/21/22 = 23 行卷
    warns.append(f"volume_summary 行数={len(lines)}，预期 24（含表头）")

with open(REPORT, "w", encoding="utf-8") as f:
    f.write(f"《蘧编》底座验证缺漏清单\n{'=' * 40}\n")
    f.write(f"总条数: {total}\n")
    f.write(f"入层条数: {in_layer}（卷01-20）\n")
    f.write(f"_extract 文件数: {len(ext_files)}，条数合计: {ext_total}\n")
    f.write(f"卷文件明细: {ext_files}\n")
    f.write(f"\n[ERROR] {len(errors)} 项\n")
    for e in errors:
        f.write(f"  - {e}\n")
    f.write(f"\n[WARN/OK] {len(warns)} 项\n")
    for w in warns:
        f.write(f"  - {w}\n")
    f.write(f"\n结论: {'PASS' if not errors else 'FAIL'}\n")

print(f"[验证] {REPORT}")
print(f"[验证] errors={len(errors)} warns={len(warns)} 结论={'PASS' if not errors else 'FAIL'}")
for e in errors:
    print("  ERR:", e)
