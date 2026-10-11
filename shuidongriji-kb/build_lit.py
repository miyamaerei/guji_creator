# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— LIT 文献资产打包器（build_lit）
==========================================================
读 sources/_lit_ai_NN.py → 校验（item_id/必填/文献类型枚举）→ 注入 original
→ 每卷 JSON + 汇总。整卷抄录长文（圣旨/碑文/长记）各算一条。
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from _kg_enums import LIT_TYPES, LIT_TYPES_VERSION, check_enum

KEY_FIELDS = ["lit_id", "item_id", "title", "author", "type"]
ID_FIELD = "lit_id"


def enum_checker(rec, issues, item_id):
    ltype = rec.get("type")
    try:
        if ltype:
            check_enum(ltype, LIT_TYPES, "文献类型", LIT_TYPES_VERSION)
    except ValueError as e:
        issues.append(f"卷 {item_id[:2]} {item_id}：{e}")


def build(volumes=None, verbose=True):
    out = os.path.join(common.DATA_DIR, "lit")
    issues = common.layer_build("lit", volumes, KEY_FIELDS, enum_checker, out,
                                id_field=ID_FIELD, verbose=verbose)
    if issues:
        print(f"\n[LIT 校验问题 {len(issues)} 条]")
        for i in issues[:20]:
            print("  -", i)
    else:
        print("\nLIT 校验通过（问题数 = 0）")
    return issues


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="LIT 文献资产打包器")
    ap.add_argument("--volumes", nargs="*")
    args = ap.parse_args()
    build(volumes=args.volumes)
