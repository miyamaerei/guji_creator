# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— APPT 职官任职打包器（build_appt）
==========================================================
读 sources/_appt_ai_NN.py（AI 判定：任职动词词典+规则候选→AI 复核）
→ 校验（item_id/必填/任职状态枚举）→ 注入 original → 输出每卷 JSON + 汇总
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from _kg_enums import APPT_STATUS, APPT_STATUS_VERSION, check_enum

KEY_FIELDS = ["appointment_id", "item_id", "person", "office", "when", "status"]
ID_FIELD = "appointment_id"


def enum_checker(rec, issues, item_id):
    status = rec.get("status")
    try:
        if status:
            check_enum(status, APPT_STATUS, "任职状态", APPT_STATUS_VERSION)
    except ValueError as e:
        issues.append(f"卷 {item_id[:2]} {item_id}：{e}")


def build(volumes=None, verbose=True):
    out = os.path.join(common.DATA_DIR, "appt")
    issues = common.layer_build("appt", volumes, KEY_FIELDS, enum_checker, out,
                                id_field=ID_FIELD, verbose=verbose)
    if issues:
        print(f"\n[APPT 校验问题 {len(issues)} 条]")
        for i in issues[:20]:
            print("  -", i)
    else:
        print("\nAPPT 校验通过（问题数 = 0）")
    return issues


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="APPT 职官任职打包器")
    ap.add_argument("--volumes", nargs="*")
    args = ap.parse_args()
    build(volumes=args.volumes)
