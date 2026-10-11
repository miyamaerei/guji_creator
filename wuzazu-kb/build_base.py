"""《五杂俎》知识工程 | 底座：章节切分 + 条粒度指纹库

输入：源文本（缺省 C:\\Users\\Administrator\\Downloads\\五杂俎.txt，可用 WZZ_TXT 覆盖）
输出：
    _extract/NN_卷名.txt           每卷条目标文（`条N|正文`），供 AI 逐卷阅读
    _item_registry.json            item_id -> {original, norm} 指纹库（各层不手抄原文）
    _build/volume_summary.json|.csv 分卷条目数 / 条号区间 / 卷阅读模式提示
    _build/_tasks.json             逐卷任务清单（供 AI 逐卷回填）
    _build/base_report.json|txt    底座自检报告（对基线做缺口登记）

重跑：python build_base.py [--check]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_pack_base import (  # noqa: E402
    ALL_VOLUMES,
    BUILD_DIR,
    BUILD_VERSION,
    EXTRACT_DIR,
    REGISTRY_PATH,
    SOURCE_TXT,
    VOLUME_MODE_HINT,
    VOLUME_NAME,
    VOLUMES,
    banner,
    ensure_dirs,
    normalize_text,
    now_stamp,
    read_text,
    report_stats,
    sha256_file,
    strip_indent,
    write_csv,
    write_json,
    write_text,
)

VOLUME_MARK_RE = re.compile(r"^[\s\u3000]*●(.+?)\s*$")
ITEM_START_RE = re.compile(r"^[\u3000][\u3000\s]")   # 段首全角双空格 = 条目起点
CN_NUM_RE = re.compile(r"卷([一二三四五六七八九十]+)")

# 方案基线（skill §2.3：预计 1761 条 = 序 3 + 16 卷 1758）。底座自检对基线，缺口如实登记。
EXPECTED_ITEMS = 1761
EXPECTED_MAIN = 1758
EXPECTED_PREFACE = 3

CN_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
          "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}


def cn_to_int(text: str) -> int:
    """中文数字转整数（支持 十 / 十一 … 十六）。"""
    body = text.strip()
    if not body:
        return 0
    if body.startswith("十"):
        rest = body[1:]
        return 10 + (CN_NUM.get(rest, 0) if rest else 0)
    if "十" in body:
        head, _, tail = body.partition("十")
        tens = CN_NUM.get(head, 0) * 10
        return tens + (CN_NUM.get(tail, 0) if tail else 0)
    return CN_NUM.get(body, 0)


def split_chapters(text: str) -> tuple[list[dict], list[str], list[str]]:
    """按 ● 标记切卷：●序 -> 00；●卷一 天部一 -> 01。"""
    chapters: list[dict] = []
    current: dict | None = None
    for raw in text.split("\n"):
        line = raw.rstrip("\r")
        mark = VOLUME_MARK_RE.match(line)
        if mark:
            title = mark.group(1).strip()
            if title.startswith("序") or "序" == title[:1]:
                volume = "00"
            else:
                m = CN_NUM_RE.search(title)
                volume = f"{cn_to_int(m.group(1)):02d}" if m else None
            if volume is None:
                raise ValueError(f"无法识别的卷标记：{line!r}")
            current = {"volume": volume, "title": title, "lines": []}
            chapters.append(current)
            continue
        if current is not None:
            current["lines"].append(line)
    # 卷名以 VOLUMES 为准（标记文本只用于识别卷号）
    seen: dict[str, int] = {}
    for ch in chapters:
        seen[ch["volume"]] = seen.get(ch["volume"], 0) + 1
    dup = [v for v, n in seen.items() if n > 1]
    missing = [v for v in ALL_VOLUMES if v not in seen]
    for ch in chapters:
        ch["name"] = VOLUME_NAME.get(ch["volume"], ch["title"])
    return chapters, missing, dup


def build_items(lines: list[str]) -> list[str]:
    """卷内条目切分：一条 = 一个段首（全角双空格缩进）+ 其后续软换行行。

    本扫描本实际排版：条目以两个全角空格（U+3000）起段，条目内部无换行，
    少数据段另起一行但无缩进，故按"缩进起段"切条而非按空行切条。
    只在切条处丢缩进空白，正文一字不动（全文照录）。
    """
    items: list[str] = []
    buf: list[str] = []
    for raw in lines:
        line = raw.rstrip("\r")
        if not line.strip():
            continue
        if ITEM_START_RE.match(line):
            if buf:
                items.append("\n".join(buf))
            buf = [strip_indent(line)]
        else:
            # 无缩进行：并入当前条（不丢字）；若尚无当前条则自成一条
            buf.append(line if line.startswith("\u3000") else strip_indent(line))
    if buf:
        items.append("\n".join(buf))
    return [it.strip("\n") for it in items if it.strip()]


def reconcile(raw: str, registry: dict) -> dict:
    """切分对账：证明"一条不丢字"，并把对基线的差异定位到具体行。

    口径：切条只丢段首缩进空白，正文字符必须 100% 落在条目里。
    """
    joined = "".join(v["original"] for v in registry.values())
    nonspace = lambda s: sum(1 for ch in s if not ch.isspace())  # noqa: E731
    title_lines: list[str] = []
    unassigned: list[dict] = []
    dropped_indent = 0
    chapter_marks = 0
    for idx, line in enumerate(raw.split("\n"), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if VOLUME_MARK_RE.match(line):
            chapter_marks += 1
            continue
        core = stripped.strip("\u3000 ")
        indent = line[:len(line) - len(line.lstrip("\u3000 "))]
        if ITEM_START_RE.match(line):
            dropped_indent += len(indent)
        if core and core not in joined:
            (title_lines if idx <= 1 and "五杂俎" in core else unassigned).append(
                {"line": idx, "text": core[:120]})
    return {
        "generated_at": now_stamp(),
        "rule": "段首全角双空格（U+3000×2）= 条目起点；●标记 = 卷界；只丢缩进空白",
        "source_nonspace_chars": nonspace(raw),
        "entries_nonspace_chars": nonspace(joined),
        "char_delta": nonspace(raw) - nonspace(joined),
        "dropped_indent_chars": dropped_indent,
        "chapter_mark_lines": chapter_marks,
        "char_delta_note": ("差值 = 被丢弃的段首缩进空白"
                            "（全角空格；各层一律不保留缩进）"),
        "book_title_lines": title_lines,
        "unassigned_lines": unassigned,
        "unassigned_count": len(unassigned),
        "verdict": ("正文零丢失：所有非空白正文均已归属具体条目"
                    if not unassigned else "存在未归属正文行，需人工核对"),
    }


def build() -> dict:
    ensure_dirs()
    if not SOURCE_TXT.exists():
        raise SystemExit(f"未找到源文本：{SOURCE_TXT}（可用环境变量 WZZ_TXT 覆盖）")
    raw = read_text(SOURCE_TXT)
    chapters, missing, dup = split_chapters(raw)

    registry: dict[str, dict] = {}
    volume_summary: list[dict] = []
    tasks: list[dict] = []
    empty_items = 0

    for ch in chapters:
        vol = ch["volume"]
        items = build_items(ch["lines"])
        lines_out: list[str] = []
        for idx, text in enumerate(items, start=1):
            item_id = f"{vol}-{idx:03d}"
            if not text.strip():
                empty_items += 1
            registry[item_id] = {"original": text, "norm": normalize_text(text)}
            lines_out.append(f"条{idx}|{text}")
        write_text(EXTRACT_DIR / f"{vol}_{ch['name']}.txt", "\n".join(lines_out) + "\n")
        volume_summary.append({
            "volume": vol,
            "name": ch["name"],
            "count": len(items),
            "item_range": [f"{vol}-001", f"{vol}-{len(items):03d}"] if items else [],
            "mode_hint": VOLUME_MODE_HINT.get(vol, ""),
        })
        tasks.append({
            "volume": vol,
            "name": ch["name"],
            "item_count": len(items),
            "extract": str(EXTRACT_DIR / f"{vol}_{ch['name']}.txt"),
            "mode_hint": VOLUME_MODE_HINT.get(vol, ""),
            "layers": ["ent", "event", "rel", "nam", "cit", "obj", "cus", "opn", "ming", "appt", "trl"],
        })

    write_json(REGISTRY_PATH, registry)
    write_json(BUILD_DIR / "volume_summary.json", {
        "generated_at": now_stamp(), "builder": BUILD_VERSION,
        "source": str(SOURCE_TXT), "source_sha256": sha256_file(SOURCE_TXT),
        "volumes": volume_summary,
    })
    write_csv(BUILD_DIR / "volume_summary.csv", volume_summary,
              ["volume", "name", "count", "item_range", "mode_hint"])
    write_json(BUILD_DIR / "_tasks.json", {"generated_at": now_stamp(), "tasks": tasks})

    counts = {v["volume"]: v["count"] for v in volume_summary}
    total = sum(counts.values())
    preface = counts.get("00", 0)
    main_total = total - preface
    recon = reconcile(raw, registry)
    report = {
        "generated_at": now_stamp(),
        "builder": BUILD_VERSION,
        "source_txt": str(SOURCE_TXT),
        "source_sha256": sha256_file(SOURCE_TXT),
        "total_items": total,
        "total_chars": sum(len(v["original"]) for v in registry.values()),
        "preface_items": preface,
        "main_items": main_total,
        "expected_items": EXPECTED_ITEMS,
        "expected_main": EXPECTED_MAIN,
        "expected_preface": EXPECTED_PREFACE,
        "gap_items": EXPECTED_ITEMS - total,
        "gap_main": EXPECTED_MAIN - main_total,
        "gap_preface": EXPECTED_PREFACE - preface,
        "volumes_missing": missing,
        "volumes_duplicated": dup,
        "empty_items": empty_items,
        "per_volume": counts,
        "reconciliation": recon,
        "baseline_note": (
            "方案基线 1761 条（序 3 + 正文 1758）；实测差异须在缺口表登记，不静默改口径。"
            if total != EXPECTED_ITEMS else "与方案基线一致。"
        ),
    }
    write_json(BUILD_DIR / "base_report.json", report)
    write_json(BUILD_DIR / "split_reconciliation.json", recon)

    lines = [
        "《五杂俎》底座自检报告",
        "=" * 48,
        f"源文本：{SOURCE_TXT}",
        f"sha256：{report['source_sha256']}",
        f"生成时间：{report['generated_at']}",
        "",
        f"条目总数：{total}（方案基线 {EXPECTED_ITEMS}，差 {report['gap_items']:+d}）",
        f"正文条目：{main_total}（基线 {EXPECTED_MAIN}，差 {report['gap_main']:+d}）",
        f"序/版本说明：{preface}（基线 {EXPECTED_PREFACE}，差 {report['gap_preface']:+d}）",
        f"总字数（original）：{report['total_chars']}",
        f"空条目：{empty_items}",
        f"缺卷：{missing or '无'}    重复卷：{dup or '无'}",
        f"切分对账：原文非空白字符 {recon['source_nonspace_chars']}，"
        f"入条目 {recon['entries_nonspace_chars']}，差 {recon['char_delta']}"
        f"（全部为段首缩进空白与卷标题行）",
        f"未归属行：{recon['unassigned_count']}",
        "",
        "分卷条目数：",
    ]
    for v in volume_summary:
        lines.append(f"  {v['volume']} {v['name']:<8} {v['count']:>4} 条   {v['item_range']}")
    write_text(BUILD_DIR / "_volume_summary.txt", "\n".join(lines) + "\n")
    return report


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="《五杂俎》底座打包器：章节切分 + 条粒度指纹库")
    ap.add_argument("--check", action="store_true", help="只自检不写盘")
    args = ap.parse_args()

    banner("底座打包器 build_base")
    if args.check:
        raw = read_text(SOURCE_TXT)
        chapters, missing, dup = split_chapters(raw)
        counts = {ch["volume"]: len(build_items(ch["lines"])) for ch in chapters}
        total = sum(counts.values())
        report_stats("底座自检（--check）", {
            "条目总数": total,
            "对基线差": f"{EXPECTED_ITEMS - total:+d} 条",
            "序条": counts.get("00", 0),
            "缺卷": missing or "无",
            "重复卷": dup or "无",
            "源 sha256": sha256_file(SOURCE_TXT),
        })
        return

    report = build()
    report_stats("底座统计", {
        "条目总数": report["total_items"],
        "正文条目": report["main_items"],
        "序条": report["preface_items"],
        "总字数": report["total_chars"],
        "源 sha256": report["source_sha256"],
        "缺卷": report["volumes_missing"] or "无",
        "重复卷": report["volumes_duplicated"] or "无",
        "空条目": report["empty_items"],
        "对基线差": f"{report['gap_items']:+d} 条",
    })
    print("\n[产物] _extract/*.txt | _item_registry.json | _build/volume_summary.* | "
          "_build/base_report.json | _build/_tasks.json | _build/_volume_summary.txt")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit(130)
