# -*- coding: utf-8 -*-
"""工厂文档一致性体检。

真相源（改此处后须跑一遍确认全库无残留）：
  - pitfalls.md        版本 v15，坑号 #0–#64，合计 65 条
  - error-taxonomy.md  版本 v1.3，分族 16 族 A–P
  - A/B/G/P 四族合计    30 / 65 ≈ 46%（全为工程侧错误）

用法：python scripts_check_factory_consistency.py
退出码：0 = 无过期引用；1 = 有。
注意：CHECKS 的模式字面量会被自身匹配，故扫描时跳过本文件（见 main）。"""

import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SCAN_DIRS = ["SKILL.md", "assets", "references"]

CHECKS = [
    ("四族条数应为 30", r"(?<![0-9])29 ?/ ?6[35]", r"6[35] 条里"),
    ("总条数应为 65", r"(?<![0-9#])6[0-4] 条", r"(?<![0-9#])6[0-4] ?/ ?6|v1[0-9] |历史|当时"),
    ("占比应为 46%", r"(?<!\d)45%", r"停在 45%|45%→|45% →|仍停在"),
    ("族数应为 16 族", r"(?<!\d)1[45] 族", r"(A–O|主表)"),
    ("pitfalls 应为 v15", r"pitfalls v1[0-4](?!5)",
     r"v1[0-4] 为|#6[23] 于 v1[0-4]|v1[0-4] 补入|历史情况|历史：当时|当版"),
    ("taxonomy 应为 v1.3", r"error-taxonomy v1(?!\.3)",
     r"error-taxonomy v1[.．]?[0-9]? *[（(]|error-taxonomy \*\*v1|当时 error-taxonomy v1"),
]


def walk_targets():
    out = []
    for name in SCAN_DIRS:
        p = os.path.join(ROOT, name)
        if os.path.isfile(p):
            out.append(p)
        elif os.path.isdir(p):
            for r, _d, fs in os.walk(p):
                for f in fs:
                    if f.endswith((".md", ".py")):
                        out.append(os.path.join(r, f))
    return out


def main():
    hits = []
    me = os.path.basename(__file__)
    for p in walk_targets():
        f = os.path.basename(p)
        if f.startswith("_") or f == me:
            continue          # 跳过本体检脚本自身（其 CHECKS 表含模式字面量，会自匹配）
        try:
            text = io.open(p, encoding="utf-8").read()
        except OSError:
            continue
        rel = os.path.relpath(p, ROOT)
        lines = text.splitlines()
        for label, pat, ok in CHECKS:
            for m in re.finditer(pat, text):
                line_no = text[:m.start()].count("\n") + 1
                lane = lines[line_no - 1] if line_no <= len(lines) else ""
                col = m.start() - (text.rfind("\n", 0, m.start()) + 1)
                seg = lane[:150]
                ctx = lane[max(0, col - 14):col + 20]   # 命中处上下文，供「历史版本」类白名单判定
                if ok and (re.search(ok, seg) or re.search(ok, ctx)):
                    continue
                hits.append((rel, line_no, label, seg))

    print("扫描 %d 个文件" % len(walk_targets()))
    print("真相源：A/B/G/P = 30 / 65 ≈ 46% ｜ pitfalls v15 ｜ error-taxonomy v1.3 ｜ 16 族 A–P")
    print()
    if not hits:
        print("PASS：无过期数字/版本引用")
        return 0
    print("发现 %d 处过期引用：" % len(hits))
    for rel, line_no, label, seg in hits:
        print("  %-44s L%-5d %-16s %s" % (rel, line_no, label, seg))
    return 1


if __name__ == "__main__":
    sys.exit(main())
