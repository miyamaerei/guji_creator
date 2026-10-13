# -*- coding: utf-8 -*-
"""
底座打包器：切分 + 章节 + _extract + 指纹库。
用法：
  python build_base.py                    全量权威重建
  python build_base.py --volumes 01       单卷增量（合并写回，不覆盖共享文件）
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C

VOLS = ["01", "02", "03", "04", "05"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volumes", default=None, help="如 01,02；缺省=全量")
    args = ap.parse_args()
    vols = C.iter_volumes(args.volumes)
    incremental = args.volumes is not None

    lines = C.read_source_lines()
    all_entries = C.split_entries(lines)
    by_vol = {v: [e for e in all_entries if e["volume"] == v] for v in VOLS}

    # ---- 合并写回指纹库（增量语义：加载现有 → 只重算请求卷 → 合并）----
    if incremental and os.path.isfile(C.REGISTRY):
        with open(C.REGISTRY, "r", encoding="utf-8") as f:
            reg = json.load(f)
        for k in list(reg.keys()):
            if k.split("-")[0] in vols:
                del reg[k]
    else:
        reg = {}

    for v in vols:
        ents = by_vol[v]
        # 章节文件
        name = C.VOL_NAMES[v]
        ch = ["# 职官志 %s（卷%s）" % (name, v), ""]
        for e in ents:
            ch.append(e["text"])
            ch.append("")
        C.atomic_write_text(os.path.join(C.CHAPTERS, "%s_%s.md" % (v, name)),
                            "\n".join(ch))

        # _extract\NN_卷名.txt  格式 条N|正文
        ex = []
        for e in ents:
            n = int(e["item_id"].split("-")[1])
            ex.append("条%d|%s" % (n, e["text"]))
        C.atomic_write_text(os.path.join(C.EXTRACT, "%s_%s.txt" % (v, name)),
                            "\n".join(ex) + "\n")

        # 指纹库
        for e in ents:
            reg[e["item_id"]] = {"original": e["text"], "norm": C.norm_text(e["text"])}

    # 排序后写盘（key 排序，便于 diff）
    reg = {k: reg[k] for k in sorted(reg.keys())}
    C.atomic_write_json(C.REGISTRY, reg)

    # ---- 报告 ----
    rep = []
    rep.append("=== 底座构建报告 ===")
    rep.append("模式: %s" % ("增量 %s" % ",".join(vols) if incremental else "全量重建"))
    rep.append("源文件: %s" % C.SRC)
    rep.append("总行数(含空行): %d" % len(lines))
    rep.append("")
    rep.append("%-4s %-8s %-8s %-8s %s" % ("卷", "非空行", "条目", "起始行", "item_id 范围"))
    tot = 0
    for v in VOLS:
        ents = by_vol[v]
        tot += len(ents)
        if ents:
            rng = "%s ~ %s" % (ents[0]["item_id"], ents[-1]["item_id"])
            rep.append("%-4s %-8d %-8d %-8d %s" % (v, len(ents), len(ents),
                                                   ents[0]["lineno"], rng))
    rep.append("")
    rep.append("条目合计: %d" % tot)
    rep.append("指纹库条目: %d" % len(reg))
    rep.append("item_id 唯一: %s" % ("是" if len(reg) == tot else "否 —— 有跳号/重号"))
    # item_id 连续性
    gaps = []
    for v in VOLS:
        ents = by_vol[v]
        for i, e in enumerate(ents, 1):
            if e["item_id"] != "%s-%03d" % (v, i):
                gaps.append(e["item_id"])
    rep.append("item_id 连续: %s（异常 %d 处）" % ("是" if not gaps else "否", len(gaps)))
    rep.append("")
    rep.append("章节文件: chapters/%s_卷名.md" % "NN")
    rep.append("抽原文:   _extract/NN_卷名.txt（格式 条N|正文）")
    rep.append("指纹库:   _item_registry.json")

    out = os.path.join(C.ROOT, "_base_report.txt")
    C.atomic_write_text(out, "\n".join(rep) + "\n")
    print("OK 条目=%d 指纹库=%d -> %s" % (tot, len(reg), out))


if __name__ == "__main__":
    main()
