# -*- coding: utf-8 -*-
"""主程序复核：build_layers.py 之外的三件事。
1) C3 抄原文检测：扫描 ENTS/STRUCTS/REGS/OPNS 所有文本字段，若与该条 original
   有 >=15 字连续重合，视为违规。
2) 覆盖度：每卷有多少条 item_id 至少有 1 个 ent / struct / reg / opn。
3) 每卷条数汇总表。
只读，不改任何源文件。
"""
import json, os, sys, glob, importlib, collections, re

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
REG = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

def load_src():
    buckets = collections.defaultdict(lambda: {"ENTS": [], "STRUCTS": [], "REGS": [], "OPNS": []})
    src_dir = os.path.join(ROOT, "_src")
    files = sorted(glob.glob(os.path.join(src_dir, "_*_ai.py")))
    for f in files:
        modname = os.path.splitext(os.path.basename(f))[0]
        mod = importlib.import_module(f"_src.{modname}")
        importlib.reload(mod)
        for layer in ("ENTS", "STRUCTS", "REGS", "OPNS"):
            buckets[modname][layer] = list(getattr(mod, layer, []))
    return buckets

def longest_common_substr(a, b):
    """简单 LCS 长度，只用于 C3 粗筛（原文长，字段短，DP 矩阵不大）。"""
    if not a or not b:
        return 0
    la, lb = len(a), len(b)
    prev = [0] * (lb + 1)
    best = 0
    for i in range(1, la + 1):
        cur = [0] * (lb + 1)
        ai = a[i-1]
        for j in range(1, lb + 1):
            if ai == b[j-1]:
                cur[j] = prev[j-1] + 1
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best

def main():
    buckets = load_src()

    # ---- 汇总表 ----
    print("=" * 78)
    print(f"{'file':<22} {'ENTS':>6} {'STRUCTS':>8} {'REGS':>6} {'OPNS':>6}")
    print("-" * 78)
    grand = {"ENTS": 0, "STRUCTS": 0, "REGS": 0, "OPNS": 0}
    all_iid = collections.defaultdict(lambda: {"ent": set(), "struct": set(), "reg": set(), "opn": set()})
    for modname, layers in sorted(buckets.items()):
        counts = {k: len(v) for k, v in layers.items()}
        for k in grand: grand[k] += counts[k]
        print(f"{modname:<22} {counts['ENTS']:>6} {counts['STRUCTS']:>8} {counts['REGS']:>6} {counts['OPNS']:>6}")
        for (iid, *_rest) in layers["ENTS"]:
            all_iid[iid]["ent"].add(iid)
        for row in layers["STRUCTS"]:
            all_iid[row[0]]["struct"].add(row[0])
        for row in layers["REGS"]:
            all_iid[row[0]]["reg"].add(row[0])
        for row in layers["OPNS"]:
            all_iid[row[0]]["opn"].add(row[0])
    print("-" * 78)
    print(f"{'TOTAL':<22} {grand['ENTS']:>6} {grand['STRUCTS']:>8} {grand['REGS']:>6} {grand['OPNS']:>6}")
    print()

    # ---- 每卷覆盖率 ----
    by_vol = collections.defaultdict(lambda: {"total": 0, "ent": 0, "struct": 0, "reg": 0, "opn": 0})
    for iid, meta in REG.items():
        vol = iid.split("-")[0]
        by_vol[vol]["total"] += 1
        if iid in all_iid:
            for layer in ("ent", "struct", "reg", "opn"):
                if all_iid[iid][layer]:
                    by_vol[vol][layer] += 1
    print("=" * 78)
    print(f"{'vol':<6} {'total':>6} {'has_ent':>8} {'has_struct':>11} {'has_reg':>8} {'has_opn':>8}")
    print("-" * 78)
    for vol in sorted(by_vol):
        m = by_vol[vol]
        print(f"{vol:<6} {m['total']:>6} {m['ent']:>8} {m['struct']:>11} {m['reg']:>8} {m['opn']:>8}")
    print()

    # ---- 完全没 ent 的条目（硬约束：ent 至少覆盖核心实体） ----
    no_ent = []
    for iid in REG:
        if iid.split("-")[0] != "01" and iid not in all_iid:
            no_ent.append(iid)
    if no_ent:
        print(f"⚠  {len(no_ent)} 条 item_id 在任何层都没被提到（卷01已除外）:")
        for iid in no_ent[:30]:
            print(f"    - {iid}  {REG[iid]['title']}")
        if len(no_ent) > 30:
            print(f"    ... 还有 {len(no_ent)-30} 条")
    else:
        print("✓ 卷02~11 每条 item_id 至少在一个层出现")
    print()

    # ---- C3 抄原文检测 ----
    violations = []
    TEXT_IDX = {
        "ENTS": [(1, "text"), (5, "normalized")],
        "STRUCTS": [(3, "target"), (4, "content")],
        "REGS": [(1, "name"), (3, "content"), (5, "target")],
        "OPNS": [(1, "topic"), (3, "argument")],
    }
    for modname, layers in buckets.items():
        for layer_name, idx_list in TEXT_IDX.items():
            for row in layers[layer_name]:
                iid = row[0]
                orig = REG.get(iid, {}).get("original", "")
                if not orig:
                    continue
                for col, field in idx_list:
                    val = str(row[col]) if col < len(row) else ""
                    if not val:
                        continue
                    hit = longest_common_substr(orig, val)
                    if hit >= 15:
                        violations.append((modname, layer_name, iid, field, hit, val[:40]))
    print("=" * 78)
    if violations:
        print(f"✗ C3 抄原文违规 {len(violations)} 处（连续重合 >=15 字）：")
        for v in violations:
            print(f"    [{v[0]}] {v[1]} {v[2]}.{v[3]}  LCS={v[4]}  「{v[5]}…」")
    else:
        print("✓ C3 通过：所有文本字段与原文最长连续重合 <15 字")
    print()

if __name__ == "__main__":
    main()
