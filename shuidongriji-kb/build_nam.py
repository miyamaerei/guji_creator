# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— NAM 名录谱牒打包器（build_nam）
==========================================================
读 sources/_nam_ai_NN.py → 校验（item_id/必填/名录类型枚举/entries 四元组）
→ 注入 original → 每卷 JSON + 汇总。

entries 四元组结构：{seq, person, courtesy_name, hometown, office}
（对应"六科旧僚题名"姓名/字/邑里/官位；无则填"未明"）
书信/叙事中仅提及族谱者：entries 空数组 + evidence 注明。
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from _kg_enums import NAM_ENTRY_FIELDS, NAM_TYPES, NAM_TYPES_VERSION, check_enum

KEY_FIELDS = ["nam_id", "item_id", "name", "category", "scope"]
ID_FIELD = "nam_id"
ENTRY_FIELDS = set(NAM_ENTRY_FIELDS)


def enum_checker(rec, issues, item_id):
    cat = rec.get("category")
    try:
        if cat:
            check_enum(cat, NAM_TYPES, "名录类型", NAM_TYPES_VERSION)
    except ValueError as e:
        issues.append(f"卷 {item_id[:2]} {item_id}：{e}")
    entries = rec.get("entries")
    if not isinstance(entries, list):
        issues.append(f"卷 {item_id[:2]} {item_id}：entries 必须是数组")
        return
    for e in entries:
        if not isinstance(e, dict):
            issues.append(f"卷 {item_id[:2]} {item_id}：entries 元素必须是对象")
            continue
        missing = ENTRY_FIELDS - set(e.keys())
        if missing:
            issues.append(f"卷 {item_id[:2]} {item_id}：entries 缺字段 {sorted(missing)}")
        for k in ("courtesy_name", "hometown", "office"):
            if e.get(k) in (None, ""):
                e[k] = "未明"


def build(volumes=None, verbose=True):
    out = os.path.join(common.DATA_DIR, "nam")
    issues = common.layer_build("nam", volumes, KEY_FIELDS, enum_checker, out,
                                id_field=ID_FIELD, verbose=verbose)
    if issues:
        print(f"\n[NAM 校验问题 {len(issues)} 条]")
        for i in issues[:20]:
            print("  -", i)
    else:
        print("\nNAM 校验通过（问题数 = 0）")
    return issues


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="NAM 名录谱牒打包器")
    ap.add_argument("--volumes", nargs="*")
    args = ap.parse_args()
    build(volumes=args.volumes)
