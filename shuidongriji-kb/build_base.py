# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— 底座生成器（build_base）
=================================================
产出（SKILL.md §2 底座）：
  _extract/volumes/NN_卷名.xhtml   卷文件（38 卷 + 卷 00 四库提要）
  _extract/items/NN_卷名.txt       条目切分（条N|正文）
  _extract/_item_registry.json     指纹库（{NN-NNN: {original, norm}}）
  _extract/volume_summary.csv      卷概要（条目数/字数/最长行，供各层按卷模式分配优先级）

切分规则（已探查确认，2026-10-10）：
  * 卷首 = "水东日记卷X" 前一行含"钦定四库全书"（38 个）；卷尾落款 = 行尾"水东日记卷X"
  * 卷内正文以换行分行，每行 = 一条候选条目（叙事/文献卷行=条；名录/谱牒卷行=表格行，
    由 NAM/APPT 层按卷阅读模式重组，底座不做语义合并）
  * 装饰行剔除：`<子部...>` 书签行、卷首标题行（明　叶盛　撰）
  * 卷尾落款剥离：行尾"水东日记卷X"正则剥离（独立标题行剥离后整行丢弃）

幂等：全量重建（可重复运行，--volumes NN 支持单卷重跑）。
"""
import argparse
import csv
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (EXTRACT_DIR, INPUT_TXT, ITEMS_DIR, REGISTRY_PATH,
                    VOLUMES_DIR, VOL_CN, VOL_CN_REV, normalize_text,
                    write_json, write_text, load_json)

VOL_MARK = re.compile(r"水东日记卷[一二三四五六七八九十]+")
TAIL_MARK = re.compile(r"水东日记卷[一二三四五六七八九十]+$")
TITLE_LINE = re.compile(r"^\s*明\s*叶盛\s*撰\s*$")
KU_TITLE = re.compile(r"^\s*钦定四库全书\s*$")
DECOR_LINE = re.compile(r"^\s*<子部")


def split_volumes(text):
    """返回 [(卷号 '01'..'38', 卷首起始位置, 卷名), ...]，卷 00 单独处理。"""
    marks = [(m.group(0), m.start()) for m in VOL_MARK.finditer(text)]
    heads = []
    for v, idx in marks:
        prev = text[max(0, idx - 12):idx].replace("\n", " ")
        if "钦定四库全书" in prev:
            heads.append((VOL_CN_REV[v].zfill(2), idx, v))
    heads.sort(key=lambda x: x[1])
    return heads


def extract_volume_lines(text, start, end):
    """提取卷内正文行：剔装饰/标题/落款，返回 [(正文, 是否剥离落款后为空)] 处理后的行列表。"""
    seg = text[start:end]
    lines = []
    for raw in seg.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if TITLE_LINE.match(line) or KU_TITLE.match(line) or DECOR_LINE.match(line):
            continue
        line = TAIL_MARK.sub("", line).strip()  # 剥离行尾落款
        if not line:
            continue
        lines.append(line)
    return lines


def clean_legacy():
    """清理旧版 build_base 产物（卷号无前导零的 1_~9_ 文件），保证幂等目录。"""
    for d in (VOLUMES_DIR, ITEMS_DIR):
        if not os.path.isdir(d):
            continue
        for fn in os.listdir(d):
            if re.match(r"^\d{1}_", fn):
                p = os.path.join(d, fn)
                print(f"[清理旧格式] {p}")
                os.remove(p)


def build(volumes=None, verbose=True):
    clean_legacy()
    text = io.open(INPUT_TXT, encoding="utf-8").read()
    heads = split_volumes(text)
    if len(heads) != 38:
        raise RuntimeError(f"卷首识别异常：期望 38 个，实际 {len(heads)} 个")

    # 卷 00：四库提要（开头 → 卷一首）
    vol00_text = text[:heads[0][1]]
    vol00_lines = extract_volume_lines(vol00_text, 0, len(vol00_text))

    # 增量模式（--volumes）：保留既有共享指纹库，仅重算所请求卷（防截断 1197 条）；
    # 全量模式（不带 --volumes）：从空重建（权威口径，可清陈旧键）。
    is_scoped = bool(volumes)
    registry = (load_json(REGISTRY_PATH) or {}) if is_scoped else {}
    summary = []

    all_vols = [("00", vol00_lines, "四库提要")] + \
               [(no, extract_volume_lines(text, start, heads[i + 1][1] if i + 1 < len(heads) else len(text)), name)
                for i, (no, start, name) in enumerate(heads)]

    for no, lines, name in all_vols:
        if volumes and no not in volumes:
            continue
        # 条目切分
        items = [(no, i + 1, l) for i, l in enumerate(lines)]
        # 卷文件（xhtml）
        xhtml_parts = [f"<h1>《水东日记》{name}（{no} 卷）</h1>",
                       f"<p>条目数：{len(items)}　字符数：{sum(len(l) for _, _, l in items)}</p>", "<ol>"]
        for no_, seq, body in items:
            xhtml_parts.append(f"<li id=\"item-{no}-{seq:03d}\"><p>{body}</p></li>")
        xhtml_parts.append("</ol>")
        write_text(os.path.join(VOLUMES_DIR, f"{no}_{name}.xhtml"), "\n".join(xhtml_parts))
        # 条目文件
        item_lines = [f"条{seq}|{body}" for _, seq, body in items]
        write_text(os.path.join(ITEMS_DIR, f"{no}_{name}.txt"), "\n".join(item_lines))
        # 指纹库
        for _, seq, body in items:
            registry[f"{no}-{seq:03d}"] = {
                "original": body,
                "norm": normalize_text(body),
            }
        # 概要
        if items:
            maxlen = max(len(b) for _, _, b in items)
            summary.append({
                "volume": no, "name": name, "items": len(items),
                "chars": sum(len(b) for _, _, b in items),
                "max_line": maxlen,
                "mode_hint": mode_hint(no, len(items), maxlen),
            })
        if verbose:
            print(f"卷 {no} {name}: {len(items)} 条（{sum(len(b) for _, _, b in items)} 字）")

    write_json(REGISTRY_PATH, registry)
    csv_path = os.path.join(EXTRACT_DIR, "volume_summary.csv")
    if is_scoped and os.path.exists(csv_path):
        # 概要同样增量合并：保留未请求卷的行，所请求卷以本次重算覆盖
        by_vol = {}
        with io.open(csv_path, encoding="utf-8-sig", newline="") as f:
            for row in csv.DictReader(f):
                # CSV 读回为字符串，转回数字保证与本次重算行同型（sum/排序一致）
                for num_key in ("items", "chars", "max_line"):
                    if num_key in row:
                        row[num_key] = int(row[num_key])
                by_vol[row["volume"]] = row
        for s in summary:
            by_vol[s["volume"]] = s
        summary = [by_vol[k] for k in sorted(by_vol)]
    with io.open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["volume", "name", "items", "chars", "max_line", "mode_hint"])
        w.writeheader()
        w.writerows(summary)

    total = sum(s["items"] for s in summary)
    print(f"\n底座完成：{len(all_vols)} 卷（含卷 00），条目合计 {total}，指纹库 {len(registry)} 条")
    return summary


def mode_hint(no, item_count, max_line):
    """卷级阅读模式提示（volume-profile.md 的简化映射，供执行时参考；以实际为准）。
    名录/谱牒/文献卷行结构特殊，提示给 NAM/APPT/LIT 层分配优先级。"""
    roster_vols = {"17", "29"}          # 表格式题名
    genealogy_vols = {"15", "16", "18", "20"}  # 谱牒密集
    longdoc_vols = {"19", "22", "35", "13", "26"}  # 整篇长文
    if no in roster_vols:
        return "名录优先（行=表格行，NAM 全数组化+APPT 提取任职）"
    if no in genealogy_vols:
        return "谱牒优先（NAM 谱牒登记 entries 空数组+REL 亲属关系）"
    if no in longdoc_vols:
        return "文献优先（LIT 全抽+TRL 长文重点译）"
    if item_count <= 10 and max_line >= 800:
        return "文献优先（长文卷，行=条长文）"
    return "按 volume-profile.md 模式执行"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="《水东日记》底座生成器")
    ap.add_argument("--volumes", nargs="*", help="仅重建指定卷，如 --volumes 01 02")
    args = ap.parse_args()
    build(volumes=args.volumes)
