# -*- coding: utf-8 -*-
"""《客座赘语》知识工程 —— 底座打包器 build_base.py

按 skill `kezuo-zhuiyu-knowledge` §2 执行：
  第 1 步 章节拆分：10 卷 + 版本说明卷（00），命名 `NN_卷名.txt`；
  第 2 步 条目切分：以原文【标题】为条边界，主键 `NN-NNN`；
  第 3 步 指纹库 `_item_registry.json`（original / norm）；
  第 4 步 卷帙级 task 清单 `_build/_tasks.json`。

产物：
  _extract/00_版本说明与序.txt | 01_卷一.txt ... 10_卷十.txt   （`条N|正文`）
  _item_registry.json                                          （NN-NNN -> original/norm）
  _build/volume_summary.json|.csv                              （分卷条目数/条号区间/阅读模式）
  _build/base_report.json|txt                                  （底座自检报告，含对账）
  _build/_tasks.json                                           （卷帙级任务清单）
  _build/_volume_summary.txt                                   （人读分卷汇总）

用法：
  python build_base.py            # 全量切分
  python build_base.py --check    # 只自检不写盘
"""

from __future__ import annotations

import re
import sys

from _kg_pack_base import (
    ALL_VOLUMES,
    BUILD_DIR,
    BUILD_VERSION,
    EXTRACT_DIR,
    REGISTRY_PATH,
    SOURCE_DIR,
    VOLUME_MODE_HINT,
    VOLUME_NAME,
    VOLUMES,
    item_key,
    normalize_text,
    now_stamp,
    read_text,
    sha256_file,
    strip_indent,
    write_csv,
    write_json,
    write_text,
)

# 期待条目总数（方案基线）：00 卷 5 条 + 正文 10 卷按【标题】计 471 条 = 476 条
# （473 个标题 - 2 处相邻标题合并：卷一【巾】【履】、卷五【前记异闻一百则】+【吴桓王时…】）
EXPECTED_ITEMS = 476
EXPECTED_PREFACE = 5
EXPECTED_MAIN = 471

BODY_MARK_RE = re.compile(
    r"[\u2500]+\s*卷\s*[一二三四五六七八九十]+\s*正文\s*[\u2500]+"
)
TITLE_RE = re.compile(r"^【.*?】\s*$")
NOTE_RE = re.compile(r"^[①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳]+")
PAGE_NO_RE = re.compile(r"^\d{1,3}$")

# 卷十尾部特例：466 行"万历戊午孟秋十一日…"为【逐园居士再识】正文，标题后置。
# 切分时该段暂归上一条（【前乙酉举人见后乙酉】），写完退出前移入【逐园居士再识】。
TAIL_REPARENT = "万历戊午孟秋十一日"


def find_body_mark(lines: list[str], volume: str) -> int:
    """定位正文标记行（── 卷X 正文 ──），返回其行号；找不到则报错。"""
    for i, ln in enumerate(lines):
        if BODY_MARK_RE.search(ln) and "正文" in ln:
            return i
    raise ValueError(f"卷 {volume} 未找到正文标记行（── 卷X 正文 ──），请人工核对")


def split_volume_text(lines_body: list[str]) -> tuple[list[dict], list[int]]:
    """卷正文区条目切分。

    规则（对齐 skill §2.3）：
      * 【标题】行为条边界；标题文本保留进 original 正文（含括【】）；
      * 相邻标题（中间无正文，如【巾】+【履】、卷五前记异闻+吴桓王时）合并为一条；
      * 脚注行（①… 开头）原样保留，归当前条；
      * 纯数字行（页码/分页符，如 "0"、"1"）剔除，不进入条目、计入 dropped；
      * 空行即段落分隔（卷五复合条内每空行一则子则，保持单条、段义划分留待数据层）；
      * 正文字符一律只剥离段首缩进空白，正文一字不丢。
    返回 (items, dropped)：
      items: [{"title": str|None, "paras": [str,...]}, ...]（paras 为正文段列表，不含标题）；
      dropped: 被剔除的页码行在正文区内的行号列表。
    """
    items: list[dict] = []
    cur: dict | None = None
    buf: list[str] = []
    dropped: list[int] = []

    def flush_para() -> None:
        nonlocal buf
        if buf and cur is not None:
            cur["paras"].append("\n".join(buf))
        buf = []

    def push_item() -> None:
        nonlocal cur
        if cur is not None:
            if cur["paras"] or cur["title"]:
                items.append(cur)
        cur = None

    for idx, raw in enumerate(lines_body, start=1):
        line = raw.rstrip("\r")
        if not line.strip():
            flush_para()
            continue
        core = strip_indent(line)
        if PAGE_NO_RE.match(core) and len(core) <= 3:
            flush_para()
            dropped.append(idx)
            continue
        if TITLE_RE.match(core):
            flush_para()
            if cur is not None and not cur["paras"]:
                # 相邻标题合并：当前条目尚无正文，标题并入（【巾】【履】式共享正文）
                cur["title"] = (cur["title"] or "") + core
                continue
            push_item()
            cur = {"title": core, "paras": []}
            continue
        if cur is None:
            cur = {"title": None, "paras": []}
        if NOTE_RE.match(core):
            flush_para()
            cur["paras"].append(core)
            continue
        buf.append(core)
    flush_para()
    push_item()
    return items, dropped


def reparse_vol10_tail(items: list[dict]) -> None:
    """卷十尾部特例：把正文段 '万历戊午孟秋十一日…' 从【前乙酉举人见后乙酉】
    移入【逐园居士再识】（标题在正文之后，切分规则按标题先行，故手工校正）。"""
    for it in items:
        if it.get("title") == "【逐园居士再识】":
            for prev in items:
                for k, para in enumerate(prev["paras"]):
                    if para.startswith(TAIL_REPARENT):
                        it["paras"].insert(0, prev["paras"].pop(k))
                        return
    sys.stderr.write("[warn] 卷十未找到【逐园居士再识】条目，尾部特例未生效\n")


def items_to_text(it: dict) -> str:
    """条目写入文本：标题（若有，原文含【】）+ 空行 + 各正文段（\n 分隔）。"""
    parts: list[str] = []
    if it.get("title"):
        parts.append(it["title"])
    parts.extend(it["paras"])
    return "\n\n".join(parts)


def split_preface(full_lines: list[str]) -> list[dict]:
    """00 版本说明卷：从全本提取 5 条（丛书总序/导读/点校说明/原序/四库提要）。

    锚点均为已核实的原文行首文本（见 2026-10-10 全本行号核对记录）：
      丛书总序  69-76（69 首句 -> 《南京稀见文献丛刊》编委会署名行，含）
      导读     80-101（80 首句 -> 101 '三、朴实无华…' 段末，含）
      点校说明 103-134（103 '至于点校方面' -> 134 '2009年2月12日于蜗云阁' 署名，含）
      原序     138-140（138 首句 -> 140 '万历丁巳夏五，遁园居士书。'，含）
      四库提要 4434+4436（标题行 -> 4436 正文行'（浙江鲍士恭家藏本）'，含）
    返回 [{"title": keyword, "paras": [str]}, ...]
    """

    def find_line(keyword: str, start: int = 0) -> int:
        for i in range(start, len(full_lines)):
            if keyword in full_lines[i]:
                return i
        raise ValueError(f"全本中未找到锚点：{keyword}（自 {start} 行起）")

    segs = [
        ("丛书总序", "南京是我国著名的七大古都之一", "《南京稀见文献丛刊》编委会"),
        ("导读", "《客座赘语》10卷，为明代顾起元", "三、朴实无华"),
        ("点校说明", "至于点校方面，有几点说明如下", "2009年2月12日于蜗云阁"),
        ("原序", "余顷年多愁多病", "万历丁巳夏五，遁园居士书。"),
    ]
    items: list[dict] = []
    cursor = 0
    for name, start_kw, end_kw in segs:
        s = find_line(start_kw, cursor)
        e = find_line(end_kw, s + 1)
        cursor = e + 1
        paras = []
        buf: list[str] = []
        for ln in full_lines[s : e + 1]:
            core = strip_indent(ln)
            if not core:
                if buf:
                    paras.append("\n".join(buf))
                    buf = []
                continue
            buf.append(core)
        if buf:
            paras.append("\n".join(buf))
        items.append({"title": None, "paras": paras, "preface_name": name})

    # 四库提要：标题行 + 正文行（续游标之后，避开目录）
    ti = find_line("【《四库全书总目》提要】", cursor)
    body_i = find_line("（浙江鲍士恭家藏本）", ti + 1)
    paras2: list[str] = []
    buf2: list[str] = []
    for ln in full_lines[ti : body_i + 1]:
        core = strip_indent(ln)
        if not core:
            if buf2:
                paras2.append("\n".join(buf2))
                buf2 = []
            continue
        buf2.append(core)
    if buf2:
        paras2.append("\n".join(buf2))
    items.append({"title": None, "paras": paras2, "preface_name": "四库提要"})
    return items


def build() -> dict:
    if not SOURCE_DIR.exists():
        raise SystemExit(f"未找到源目录：{SOURCE_DIR}（可用环境变量 KZZ_SRC 覆盖）")

    registry: dict[str, dict] = {}
    volume_summary: list[dict] = []
    tasks: list[dict] = []
    empty_items = 0
    dropped_log: dict[str, list[int]] = {}
    verse_lines: list[dict] = []  # 页裂续行提示（正文行被页码打断）

    for vol, name in VOLUMES:
        if vol == "00":
            src = SOURCE_DIR / "客座赘语_全本.txt"
        else:
            src = SOURCE_DIR / f"客座赘语_{name}.txt"
        if not src.exists():
            raise SystemExit(f"缺少源文件（00卷读全本《客座赘语_全本.txt》）：{src}")
        full_lines = read_text(src).split("\n")

        if vol == "00":
            items = split_preface(full_lines)
        else:
            mark_i = find_body_mark(full_lines, vol)
            body = full_lines[mark_i + 1 :]
            items, dropped = split_volume_text(body)
            if dropped:
                dropped_log[vol] = [mark_i + 1 + d for d in dropped]
            if vol == "10":
                reparse_vol10_tail(items)

        lines_out: list[str] = []
        seq = 0
        for it in items:
            text = items_to_text(it)
            if not text.strip():
                empty_items += 1
            seq += 1
            item_id = item_key(vol, seq)
            registry[item_id] = {"original": text, "norm": normalize_text(text)}
            lines_out.append(f"条{seq}|{text}")

        write_text(EXTRACT_DIR / f"{vol}_{name}.txt", "\n".join(lines_out) + "\n")
        volume_summary.append(
            {
                "volume": vol,
                "name": name,
                "count": len(items),
                "item_range": [f"{vol}-001", f"{vol}-{len(items):03d}"]
                if items
                else [],
                "mode_hint": VOLUME_MODE_HINT.get(vol, ""),
            }
        )
        tasks.append(
            {
                "volume": vol,
                "name": name,
                "item_count": len(items),
                "extract": str(EXTRACT_DIR / f"{vol}_{name}.txt"),
                "mode_hint": VOLUME_MODE_HINT.get(vol, ""),
                "steps": ["通读", "写入", "三连自检", "build", "复核"],
                "layers": sorted(LAYER_LIST),
            }
        )

    write_json(REGISTRY_PATH, registry)
    write_json(
        BUILD_DIR / "volume_summary.json",
        {
            "generated_at": now_stamp(),
            "builder": BUILD_VERSION,
            "source_dir": str(SOURCE_DIR),
            "volumes": volume_summary,
        },
    )
    write_csv(
        BUILD_DIR / "volume_summary.csv",
        volume_summary,
        ["volume", "name", "count", "item_range", "mode_hint"],
    )
    write_json(BUILD_DIR / "_tasks.json", {"generated_at": now_stamp(), "tasks": tasks})

    counts = {v["volume"]: v["count"] for v in volume_summary}
    total = sum(counts.values())
    preface = counts.get("00", 0)
    main_total = total - preface

    report = {
        "generated_at": now_stamp(),
        "builder": BUILD_VERSION,
        "source_dir": str(SOURCE_DIR),
        "total_items": total,
        "total_chars": sum(len(v["original"]) for v in registry.values()),
        "preface_items": preface,
        "main_items": main_total,
        "expected_items": EXPECTED_ITEMS,
        "expected_main": EXPECTED_MAIN,
        "expected_preface": EXPECTED_PREFACE,
        "gap_items": total - EXPECTED_ITEMS,
        "gap_main": main_total - EXPECTED_MAIN,
        "gap_preface": preface - EXPECTED_PREFACE,
        "volumes_missing": [n for n, _ in VOLUMES if n not in counts],
        "empty_items": empty_items,
        "per_volume": counts,
        "dropped_page_lines": dropped_log,
        "missing_char_items": sorted(
            k for k, v in registry.items() if "☐" in v["original"]
        ),
        "merged_titles": [
            "01-020【巾】【履】",
            "05-005【前记异闻一百则】【吴桓王时…】",
            "10-046【逐园居士再识】（卷末再识段移入）",
        ],
        "verdict": "与方案基线一致。"
        if total == EXPECTED_ITEMS
        else "与方案基线存在差异，已在缺口表登记，需人工核对。",
    }
    write_json(BUILD_DIR / "base_report.json", report)

    lines = [
        "《客座赘语》底座自检报告",
        "=" * 48,
        f"源目录：{SOURCE_DIR}",
        f"生成时间：{report['generated_at']}",
        "",
        f"条目总数：{total}（方案基线 {EXPECTED_ITEMS}，差 {report['gap_items']:+d}）",
        f"正文条目：{main_total}（基线 {EXPECTED_MAIN}，差 {report['gap_main']:+d}）",
        f"序/版本说明：{preface}（基线 {EXPECTED_PREFACE}，差 {report['gap_preface']:+d}）",
        f"总字数（original，含标题与标点）：{report['total_chars']}",
        f"空条目：{empty_items}",
        f"缺卷：{report['volumes_missing'] or '无'}",
        f"剔除纯数字页眉/页码行：{sum(len(v) for v in dropped_log.values())} 处",
        "",
        "分卷条目数：",
    ]
    for v in volume_summary:
        lines.append(
            f"  {v['volume']} {v['name']:<6} {v['count']:>4} 条   {v['item_range']}"
        )
    write_text(BUILD_DIR / "_volume_summary.txt", "\n".join(lines) + "\n")
    return report


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(
        description="《客座赘语》底座打包器：章节切分 + 条粒度指纹库"
    )
    ap.add_argument("--check", action="store_true", help="只自检不写盘")
    args = ap.parse_args()

    if args.check:
        print(f"[check] 源目录：{SOURCE_DIR}")
        print(
            f"[check] 方案基线：总数 {EXPECTED_ITEMS}（00卷 {EXPECTED_PREFACE} + 正文 {EXPECTED_MAIN}）"
        )
        for vol, name in VOLUMES:
            src = SOURCE_DIR / (
                "客座赘语_全本.txt" if vol == "00" else f"客座赘语_{name}.txt"
            )
            print(f"[check] {'OK ' if src.exists() else 'MISS'} {name}: {src}")
        return
    report = build()
    print(
        f"[产物] _extract/*.txt | _item_registry.json | _build/volume_summary.* | "
        f"_build/base_report.json | _build/_tasks.json | _build/_volume_summary.txt"
    )
    print(
        f"[完成] 条目总数 {report['total_items']}，00卷 {report['preface_items']} + 正文 {report['main_items']}"
    )


LAYER_LIST: list[str] = [
    "ent",
    "event",
    "cit",
    "obj",
    "cus",
    "ming",
    "geo",
    "appt",
    "nam",
    "lit",
    "opn",
    "rel",
    "trl",
]


if __name__ == "__main__":
    main()
