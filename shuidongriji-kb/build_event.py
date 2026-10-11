# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— L5 事件打包器（build_event）
======================================================
读 sources/_event_ai_NN.py → 校验（item_id/必填/事件类型枚举）→ 注入 original
→ 每卷 JSON + 汇总。未建模条目由验证脚本如实单列缺口。
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from _kg_enums import EVENT_TYPES, EVENT_TYPES_VERSION, check_enum

KEY_FIELDS = ["event_id", "item_id", "type", "action"]
ID_FIELD = "event_id"


def enum_checker(rec, issues, item_id):
    etype = rec.get("type")
    try:
        if etype:
            check_enum(etype, EVENT_TYPES, "事件类型", EVENT_TYPES_VERSION)
    except ValueError as e:
        issues.append(f"卷 {item_id[:2]} {item_id}：{e}")


def build(volumes=None, verbose=True):
    out = os.path.join(common.DATA_DIR, "event")
    issues = common.layer_build("event", volumes, KEY_FIELDS, enum_checker, out,
                                id_field=ID_FIELD, verbose=verbose)
    if issues:
        print(f"\n[事件层校验问题 {len(issues)} 条]")
        for i in issues[:20]:
            print("  -", i)
    else:
        print("\n事件层校验通过（问题数 = 0）")
    return issues


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="L5 事件打包器")
    ap.add_argument("--volumes", nargs="*")
    args = ap.parse_args()
    build(volumes=args.volumes)
