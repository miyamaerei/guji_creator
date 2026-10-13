# -*- coding: utf-8 -*-
"""统一打包器：读 _src/_*_ai_NN.py → 校验枚举 → 输出 _layers/*.json"""
import os, sys, json, glob, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import _kg_enums as enums

LAYERS_DIR = os.path.join(ROOT, "_layers")
os.makedirs(LAYERS_DIR, exist_ok=True)


def load_src(path):
    spec = importlib.util.spec_from_file_location("src_mod", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.RECORDS


def check_enum(group, value, errs):
    allowed = enums.ENUM_GROUPS.get(group, [])
    if allowed and value not in allowed:
        errs.append(f"枚举 {group} 未注册值: {value}")


def build_ents():
    errs, items = [], []
    for f in sorted(glob.glob(os.path.join(ROOT, "_src", "_ents_ai_*.py"))):
        for r in load_src(f):
            check_enum("ENTITY", r["type"], errs)
            if r.get("rank_order"):
                check_enum("ORG_ORDER", r["rank_order"], errs)
            items.append(r)
    with open(os.path.join(LAYERS_DIR, "ents.json"), "w", encoding="utf-8") as fp:
        json.dump(items, fp, ensure_ascii=False, indent=1)
    return len(items), errs


def build_rules():
    errs, items = [], []
    # 加载底座原文用于校准
    reg_path = os.path.join(ROOT, "_item_registry.json")
    reg = json.load(open(reg_path, encoding="utf-8")) if os.path.exists(reg_path) else {}

    for f in sorted(glob.glob(os.path.join(ROOT, "_src", "_rules_ai_*.py"))):
        for r in load_src(f):
            # === 自动校准 ===
            iid = r.get("item_id", "")
            original = reg.get(iid, {}).get("original", "")

            # 类型校准：义务 → 禁止/时限
            if r["type"] == "义务" and original:
                import re
                if re.search(r"不许|毋得|毋|勿|禁止|不得|不准", original):
                    r["type"] = "禁止"
                elif re.search(r"限.*日|限.*月|三年|五年|十年", original):
                    r["type"] = "时限"

            # 标记校准：凡 → 奏准/议准/令/诏/敕
            if r.get("source_marker", "凡") == "凡" and original:
                if "奏准" in original:
                    r["source_marker"] = "奏准"
                elif "议准" in original:
                    r["source_marker"] = "议准"
                elif "奏定" in original:
                    r["source_marker"] = "奏定"
                elif "议定" in original:
                    r["source_marker"] = "议定"
                elif original.startswith("洪武") and "令" in original[:20]:
                    r["source_marker"] = "令"
                elif original.startswith("永乐") and "令" in original[:20]:
                    r["source_marker"] = "令"
            # === 校准结束 ===

            check_enum("RUL", r["type"], errs)
            check_enum("SOURCE_MARKER", r.get("source_marker", ""), errs)
            items.append(r)
    with open(os.path.join(LAYERS_DIR, "rules.json"), "w", encoding="utf-8") as fp:
        json.dump(items, fp, ensure_ascii=False, indent=1)
    return len(items), errs


def build_nams():
    errs, items = [], []
    for f in sorted(glob.glob(os.path.join(ROOT, "_src", "_nam_ai_*.py"))):
        for r in load_src(f):
            check_enum("NAM", r["nam_type"], errs)
            items.append(r)
    with open(os.path.join(LAYERS_DIR, "nams.json"), "w", encoding="utf-8") as fp:
        json.dump(items, fp, ensure_ascii=False, indent=1)
    return len(items), errs


def build_cits():
    errs, items = [], []
    for f in sorted(glob.glob(os.path.join(ROOT, "_src", "_cit_ai_*.py"))):
        for r in load_src(f):
            check_enum("CIT", r["citation_type"], errs)
            items.append(r)
    with open(os.path.join(LAYERS_DIR, "cits.json"), "w", encoding="utf-8") as fp:
        json.dump(items, fp, ensure_ascii=False, indent=1)
    return len(items), errs


def main():
    print("=== 打包器（枚举单点 v%s）===" % enums.VERSION)
    total_err = []
    for name, fn in [("ents", build_ents), ("rules", build_rules),
                     ("nams", build_nams), ("cits", build_cits)]:
        n, errs = fn()
        print("  %-6s: %d 条, %d 错误" % (name, n, len(errs)))
        for e in errs:
            print("    ✗", e)
        total_err.extend(errs)
    if total_err:
        print("\nFAIL: %d 个枚举错误" % len(total_err))
        return 1
    print("\nPASS: 所有层打包完成，枚举全命中")
    return 0


if __name__ == "__main__":
    sys.exit(main())
