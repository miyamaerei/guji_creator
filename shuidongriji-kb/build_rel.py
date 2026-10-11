# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— REL 人物关系打包器（build_rel）
==========================================================
读 sources/_rel_ai_NN.py → 校验（item_id/必填/关系类型/方向枚举）→ 注入 original
→ 每卷 JSON + 汇总。只建文本有直接证据的关系（宁缺毋滥）。
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from _kg_enums import (REL_DIRECTIONS, REL_DIRECTIONS_VERSION, REL_TYPES,
                       REL_TYPES_VERSION, check_enum, check_in_list)

KEY_FIELDS = ["rel_id", "item_id", "person_a", "person_b", "relation_type"]
ID_FIELD = "rel_id"


def enum_checker(rec, issues, item_id):
    rtype = rec.get("relation_type")
    try:
        if rtype:
            check_enum(rtype, REL_TYPES, "关系类型", REL_TYPES_VERSION)
    except ValueError as e:
        issues.append(f"卷 {item_id[:2]} {item_id}：{e}")
    direction = rec.get("direction")
    try:
        if direction:
            check_in_list(direction, REL_DIRECTIONS, "关系方向", REL_DIRECTIONS_VERSION)
    except ValueError as e:
        issues.append(f"卷 {item_id[:2]} {item_id}：{e}")


def build(volumes=None, verbose=True):
    out = os.path.join(common.DATA_DIR, "rel")
    issues = common.layer_build("rel", volumes, KEY_FIELDS, enum_checker, out,
                                id_field=ID_FIELD, verbose=verbose)
    if issues:
        print(f"\n[REL 校验问题 {len(issues)} 条]")
        for i in issues[:20]:
            print("  -", i)
    else:
        print("\nREL 校验通过（问题数 = 0）")
    return issues


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="REL 人物关系打包器")
    ap.add_argument("--volumes", nargs="*")
    args = ap.parse_args()
    build(volumes=args.volumes)
