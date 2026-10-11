# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— TRL 古今翻译打包器（build_trl）
==========================================================
读 sources/_trl_ai_NN.py（AI 逐条翻译，默认注释性翻译·余光中风格）
→ 校验（item_id/必填/翻译风格枚举）→ 注入 original → 每卷 JSON
→ 全书记译文本（现代文版本，卷为单位 .md，供直接阅读）

覆盖校验（条目数 = 翻译数）由 validate.py 执行。
"""
import argparse
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from _kg_enums import TRL_STYLES, TRL_STYLES_VERSION, check_enum

KEY_FIELDS = ["trl_id", "item_id", "translation", "style"]
ID_FIELD = "trl_id"


def enum_checker(rec, issues, item_id):
    style = rec.get("style")
    try:
        if style:
            check_enum(style, TRL_STYLES, "翻译风格", TRL_STYLES_VERSION)
    except ValueError as e:
        issues.append(f"卷 {item_id[:2]} {item_id}：{e}")


def build(volumes=None, verbose=True):
    out = os.path.join(common.DATA_DIR, "trl")
    issues = common.layer_build("trl", volumes, KEY_FIELDS, enum_checker, out,
                                id_field=ID_FIELD, verbose=verbose)
    # 全书记译文本（卷为单位）
    full_dir = os.path.join(out, "全书记译本")
    os.makedirs(full_dir, exist_ok=True)
    reg = common.load_registry()
    for vol_no, vol_file in common.iter_volumes():
        if volumes and vol_no not in volumes:
            continue
        vol_json = common.load_json(os.path.join(out, f"trl_{vol_no}.json"))
        if not vol_json:
            continue
        records = sorted(vol_json["records"], key=lambda r: r["item_id"])
        parts = [f"# 《水东日记》{vol_file.replace('.xhtml', '')} 现代文译本",
                 f"\n> 共 {len(records)} 条（TRL 注释性翻译·余光中风格）\n"]
        for r in records:
            note = r.get("note")
            parts.append(f"### {r['item_id']}\n\n{r['translation']}")
            if note:
                parts.append(f"\n> 注：{note}")
            parts.append("")
        common.write_text(os.path.join(full_dir, f"{vol_no}_全书记译本.md"), "\n".join(parts))
    if issues:
        print(f"\n[TRL 校验问题 {len(issues)} 条]")
        for i in issues[:20]:
            print("  -", i)
    else:
        print("\nTRL 校验通过（问题数 = 0）")
    return issues


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="TRL 古今翻译打包器")
    ap.add_argument("--volumes", nargs="*")
    args = ap.parse_args()
    build(volumes=args.volumes)
