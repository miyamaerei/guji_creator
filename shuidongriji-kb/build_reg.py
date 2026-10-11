# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— REG 典章制度打包器（build_reg）
==========================================================
读 sources/_reg_ai_NN.py → 校验（item_id/必填/制度类型枚举）→ 注入 original
→ 每卷 JSON + 汇总。一条目多项制度拆多条记录共享 item_id。
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from _kg_enums import REG_TYPES, REG_TYPES_VERSION, check_enum

KEY_FIELDS = ["reg_id", "item_id", "name", "type", "content"]
ID_FIELD = "reg_id"


def enum_checker(rec, issues, item_id):
    rtype = rec.get("type")
    try:
        if rtype:
            check_enum(rtype, REG_TYPES, "制度类型", REG_TYPES_VERSION)
    except ValueError as e:
        issues.append(f"卷 {item_id[:2]} {item_id}：{e}")


def build(volumes=None, verbose=True):
    out = os.path.join(common.DATA_DIR, "reg")
    issues = common.layer_build("reg", volumes, KEY_FIELDS, enum_checker, out,
                                id_field=ID_FIELD, verbose=verbose)
    if issues:
        print(f"\n[REG 校验问题 {len(issues)} 条]")
        for i in issues[:20]:
            print("  -", i)
    else:
        print("\nREG 校验通过（问题数 = 0）")
    return issues


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="REG 典章制度打包器")
    ap.add_argument("--volumes", nargs="*")
    args = ap.parse_args()
    build(volumes=args.volumes)
