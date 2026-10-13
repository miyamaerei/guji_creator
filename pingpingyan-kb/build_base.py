# -*- coding: utf-8 -*-
"""《平平言》底座（C3）：切卷 → 切条（卷首清单 × 正文 ○ 对齐）→ 归一 → 指纹库 → 对账报告。

四段式 ①。用法（从工程根 pingpingyan-kb/ 执行）：
    python build_base.py
    python build_base.py --expect "01:84,02:87,03:43,04:70"   # 可选：按期望条数自校验

输入（切分主源，实例内 UTF-8）：12-pingpingyan-knowledge/assets/sources/卷一.txt ~ 卷四.txt
格式（四卷统一）：
    【平平言卷X】               卷标记
    巴陵方大湜菊人著           作者行（跳过）
    ……卷首标题清单（无 ○）……  清单行（不进入条目，用于切分对齐与对账）
    ○标题正文                  条目行（标题与正文同行，以卷首清单对齐切分标题）
    ……                         条目正文续行（无 ○，追加到当前条目）

输出：
    _extract/NN_卷名.txt      行格式：条N|○标题|正文
    _item_registry.json      {item_id: {original, norm}}（原文唯一源，只入不出）
    _build/base_report.txt   对账报告（每卷清单/○数/条目数 + 标题清单 + 合并版交叉校验 + 总计）
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from _kg_pack_base import SOURCE_DIR, write_json  # noqa: E402

VOLUME_NAMES = {1: "卷一", 2: "卷二", 3: "卷三", 4: "卷四"}
VOL_FILES = {1: "卷一.txt", 2: "卷二.txt", 3: "卷三.txt", 4: "卷四.txt"}

# norm 归一规则（轻归一：SKILL.md §2.5 明确的异体→简体映射 + 少量常见异体；
# 缺字/■〈…〉/【 】夹注保留原形不臆补；标点保持原文不加改）
NORM_MAP = {
    "厯": "历", "廵": "巡", "覈": "核", "曡": "叠", "賸": "剩", "衞": "卫",
    "嚮": "向", "註": "注", "幷": "并", "閒": "间", "箇": "个", "羣": "群",
    "飬": "养", "貯": "贮", "枽": "桑", "勅": "敕", "覩": "睹", "囘": "回",
}
NORM_MAP = {ord(k): v for k, v in NORM_MAP.items()}


def norm_text(s: str) -> str:
    return s.translate(NORM_MAP)


def read_nonempty(path):
    lines = io.open(path, encoding="utf-8").read().splitlines()
    return [ln.strip() for ln in lines if ln.strip()]


def parse_volume(path):
    """返回 (vol_no, name, toc_titles, items)。
    toc_titles：卷首清单标题；items：[(title, body)]，title 为正文 ○ 标题（与清单对齐）。"""
    lines = read_nonempty(path)
    if not lines:
        return None, None, [], []
    m = re.match(r"^【平平言卷([一二三四])】$", lines[0])
    if not m:
        raise ValueError("卷标记缺失: %s 首行=%r" % (path, lines[0]))
    cn = {"一": 1, "二": 2, "三": 3, "四": 4}[m.group(1)]
    # 跳过作者行（^巴陵方大湜菊人著），其后到第一个 ○ 行为卷首清单
    body_start = 1
    if len(lines) > 1 and re.match(r"^巴陵方大湜菊人著", lines[1]):
        body_start = 2
    first_o = None
    for i in range(body_start, len(lines)):
        if lines[i].startswith("○"):
            first_o = i
            break
    if first_o is None:
        raise ValueError("无正文 ○ 条目: %s" % path)
    toc = lines[body_start:first_o]  # 卷首清单标题（不进入条目）
    # 正文区：○ 行 = 新条目；非 ○ 行 = 当前条目正文续行
    raw_items = []
    for line in lines[first_o:]:
        if line.startswith("○"):
            raw_items.append([line[1:], ""])  # 暂存"○ 后内容"与正文
        else:
            if not raw_items:
                raise ValueError("○ 条目之前出现正文续行: %s" % path)
            body = raw_items[-1][1]
            raw_items[-1][1] = body + ("\n" if body else "") + line
    # 用卷首清单对齐切分标题（第 i 个 ○ 行 ↔ 清单第 i 个标题）
    items, warns = [], []
    for i, (rest, body) in enumerate(raw_items):
        title = None
        if i < len(toc) and rest.startswith(toc[i]):
            title = toc[i]
            body = rest[len(toc[i]):] + ("\n" + body if body else "")
        else:
            title = rest[:20] + ("…" if len(rest) > 20 else "")
            warns.append("第 %d 个 ○ 行未匹配卷首清单标题（前20字=%r）" % (i + 1, rest[:20]))
        items.append((title, body))
    return cn, VOLUME_NAMES[cn], toc, items, warns


def build():
    os.makedirs(os.path.join(ROOT, "_extract"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "_build"), exist_ok=True)
    registry = {}
    report_lines = []
    total = 0
    all_warns = []
    for no in sorted(VOL_FILES):
        path = os.path.join(SOURCE_DIR, VOL_FILES[no])
        vol_no, name, toc, items, warns = parse_volume(path)
        all_warns.extend("[卷%02d] %s" % (no, w) for w in warns)
        # _extract
        fname = os.path.join(ROOT, "_extract", "%02d_%s.txt" % (no, name))
        with io.open(fname, "w", encoding="utf-8") as f:
            for seq, (title, body) in enumerate(items, 1):
                f.write("条%d|○%s|%s\n" % (seq, title, body))
        # 指纹库
        for seq, (title, body) in enumerate(items, 1):
            item_id = "%02d-%03d" % (no, seq)
            original = "○" + title + ("\n" + body if body else "")
            registry[item_id] = {"original": original, "norm": norm_text(original)}
        total += len(items)
        report_lines.append("卷%02d %s：清单 %d 条 / 正文 ○ %d 条 / 条目 %d 条%s"
                            % (no, name, len(toc), len(items), len(items),
                               "" if len(toc) == len(items) else "  ⚠️ 清单与正文 ○ 数不一致！"))
        for seq, (title, _) in enumerate(items, 1):
            report_lines.append("    %02d-%03d  %s" % (no, seq, title))
    report_lines.append("合计 %d 条" % total)
    report_lines.append("")
    report_lines.append("== 切分警告 ==")
    report_lines.extend(all_warns or ["（无）"])
    # 合并版交叉校验（序/凡例/跋无 ○，合并版 ○ 总数应 = 条目总数）
    merged = os.path.join(SOURCE_DIR, "平平言_原文_全卷合并.txt")
    if os.path.isfile(merged):
        mcount = sum(1 for ln in io.open(merged, encoding="utf-8") if ln.startswith("○"))
        report_lines.append("")
        report_lines.append("== 合并版交叉校验 ==")
        report_lines.append("合并版 ○ 行 %d 条 vs 卷拆分条目 %d 条 → %s"
                            % (mcount, total, "OK ✓" if mcount == total else "MISMATCH ✗"))
    with io.open(os.path.join(ROOT, "_build", "base_report.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    write_json(os.path.join(ROOT, "_item_registry.json"), registry)

    print("\n".join(report_lines))
    # --expect 自校验（可选）
    for arg in sys.argv[1:]:
        if arg.startswith("--expect="):
            expect = {k: int(v) for k, v in
                      (kv.split(":") for kv in arg.split("=", 1)[1].split(","))}
            actual = {("%02d" % no): len(items) for no, _, _, items, _ in
                      (parse_volume(os.path.join(SOURCE_DIR, VOL_FILES[no])) for no in VOL_FILES)}
            diff = {k: (expect[k], actual.get(k)) for k in expect if expect[k] != actual.get(k)}
            print("自校验:", "OK" if not diff else "MISMATCH %r" % diff)
    return total


if __name__ == "__main__":
    build()
