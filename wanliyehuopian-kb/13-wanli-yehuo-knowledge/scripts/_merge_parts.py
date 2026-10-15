# -*- coding: utf-8 -*-
"""_merge_parts.py —— 把 _part_grpN.py 片段按条目顺序合并进 gen_gap01_part2.py。

用法：
    python -X utf8 _merge_parts.py --check      # 只体检，不写盘
    python -X utf8 _merge_parts.py --write      # 体检通过后写盘

体检内容：
  1. 五个片段文件是否齐全、语法是否可编译；
  2. 各片段实际覆盖的 item_id 集合，与预期（01-009..01-053，去掉 006/007/008）比对；
  3. 是否与 part2 既有条目（006/007/008）重复；
  4. 是否有 item_id 缺失或越界。

**幂等性（重要修正）**
part2 = head(既有的 006/007/008) + 五个片段 + 末尾单个 go()。
head 的边界用「首个片段条目注释」定位，而**不是** `rfind("    go()")`：
后者在第一次合并后会把已合并的片段也算进 head，导致第二次合并时
整批片段被再追加一遍（历史 bug：part2 曾出现 01-009..01-053 的两份副本）。
现在 head 固定取到 `01-009` 条目注释之前，重复运行结果一致。
"""
import io
import os
import re
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
p2 = os.path.join(HERE, "gen_gap01_part2.py")

GRPS = ["_part_grp1.py", "_part_grp2.py", "_part_grp3.py",
        "_part_grp4.py", "_part_grp5.py"]

# 预期：01-009 .. 01-053（006/007/008 已存在于 part2 的 head 中）
EXPECTED = ["01-%03d" % i for i in range(9, 54)]

# head 与片段的分界：第一个片段条目（01-009）的注释行
HEAD_END_RE = re.compile(r'^\s*# =+ 01-009 ', re.M)


def items_in(text):
    """片段里出现的 item_id。"""
    return set(re.findall(r'"(01-\d{3})"', text))


def split_head(src):
    """把 part2 切成 head（006/007/008，含 build 头部）与已有正文。

    返回 (head, 是否切到一个已经合并过的正文)。
    head 以 01-009 注释为界；若找不到该注释说明 part2 尚未合并过片段，
    此时 head 取到末尾 go() 之前。
    """
    m = HEAD_END_RE.search(src)
    if m:
        return src[:m.start()], True
    j = src.rfind("    go()")
    return (src[:j] if j >= 0 else src), False


def main():
    write = "--write" in sys.argv
    errs = []
    frags = {}

    for g in GRPS:
        p = os.path.join(HERE, g)
        if not os.path.exists(p):
            errs.append("缺失片段 %s" % g)
            continue
        t = open(p, encoding="utf-8").read()
        try:
            # 片段是「缩进 4 空格的语句序列」，需包进函数体才能编译
            compile("def _wrap():\n" + t, g, "exec")
        except SyntaxError as e:
            errs.append("%s 语法错误：%s (line %s)" % (g, e.msg, e.lineno))
            continue
        frags[g] = t
        ids = sorted(items_in(t))
        print("%-16s %6d 字符  条目 %d 个  %s .. %s"
              % (g, len(t), len(ids), ids[0] if ids else "-", ids[-1] if ids else "-"))

    if errs:
        print("\n!!! 体检失败：")
        for e in errs:
            print("   ", e)
        return 1

    # 覆盖比对
    covered = set()
    for t in frags.values():
        covered |= items_in(t)
    missing = [i for i in EXPECTED if i not in covered]
    extra = sorted(covered - set(EXPECTED))
    dup3 = sorted(covered & {"01-006", "01-007", "01-008"})
    if missing:
        errs.append("缺条目 %d 个：%s" % (len(missing), missing))
    if extra:
        errs.append("越界条目（不在预期内）：%s" % extra)
    if dup3:
        errs.append("与既有 006/007/008 重复：%s" % dup3)

    print("\n覆盖 %d / %d 条" % (len(covered & set(EXPECTED)), len(EXPECTED)))
    if errs:
        print("!!! 体检失败：")
        for e in errs:
            print("   ", e)
        return 1

    # 合并：head + 各片段（去掉片段末尾自身的 go()）+ 单个 go()
    src = open(p2, encoding="utf-8").read()
    head, had_merged = split_head(src)
    if had_merged:
        print("（part2 已含合并正文，按 01-009 分界重建 —— 幂等）")
    body = [head.rstrip("\n")]
    for g in GRPS:
        t = frags[g].rstrip()
        # 去掉片段末尾自己的 go()
        j = t.rfind("go()")
        if j >= 0:
            line_start = t.rfind("\n", 0, j) + 1
            t = t[:line_start].rstrip("\n")
        body.append("")
        body.append(t)
    body.append("")
    body.append("    go()")
    merged = "\n".join(body) + "\n"

    try:
        compile(merged, "merged", "exec")
    except SyntaxError as e:
        print("!!! 合并后语法错误：%s (line %s)" % (e.msg, e.lineno))
        return 1

    # 自检：条目数应恰好 48（006..053），无重复
    seen = re.findall(r'# =+ (01-\d{3}) ', merged)
    dup = sorted({x for x in seen if seen.count(x) > 1})
    print("合并后 %d 字符（原 %d）  条目块 %d 个" % (len(merged), len(src), len(seen)))
    if dup:
        print("!!! 合并后仍有重复条目块：%s" % dup)
        return 1

    if not write:
        print("（未写盘；加 --write 落盘）")
        return 0
    with open(p2, "w", encoding="utf-8", newline="") as f:
        f.write(merged)
    print("已写盘：", p2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
