# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - 底座构建（annotate.py）

对应 SKILL.md §2 底座（公共地基，先做）：
  1. 输入唯一权威源 assets/sources/先进遗风_全本.txt（pitfalls.md #11：外部资料不作抽取依据）
  2. 按汉字卷名直接映射卷号（#24：卷上=01、卷下=02，不依赖读取顺序）
  3. 空行分段为「条」；书名行与卷标记行不入条目；装饰分隔线（全行=）剔除
  4. 输出 data/_extract/{vol}_{卷名}.txt（格式 条N|正文，N=卷内序从 1 起）
  5. 生成指纹库 data/_item_registry.json（key=NN-NNN，value={original, norm}）
     norm 缺省 = original；可用 --norm-map 提供异体字/词形归一映射（濓->濂 等）
  6. 幂等：临时文件 + rename 原子落盘（#14）；--volumes 增量合并写回共享文件（#12）

用法示例：
  python annotate.py                          # 全量重建底座（权威口径）
  python annotate.py --volumes 02             # 只重算卷 02（增量合并写回）
  python annotate.py --norm-map norms.json    # 应用归一映射后重建
  python annotate.py --expect "01:58,02:42"   # 对照预期条数（卷上 58 / 卷下 42）
"""

from __future__ import annotations

import argparse
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

import _kg_config as cfg
from _kg_pack_base import (
    atomic_write_json,
    load_json,
    print_progress,
    volumes_to_rebuild,
)

SEPARATOR_RE = re.compile(r"^=+\s*$")


# ---------------------------------------------------------------------------
# 解析
# ---------------------------------------------------------------------------


def parse_source(text: str) -> Tuple[Dict[str, List[str]], List[str]]:
    """解析全本 -> (卷名 -> 条目列表[正文], 元信息[卷边界行])。

    规则：
      * 全行 = 开头的行是装饰分隔线，剔除；
      * 含 VOLUME_MAP 键的行是卷边界锚点（本身不入条目，见 SKILL §2.3）；
      * 卷标记之前的一切非空行（书名行等）忽略；
      * 卷区间内按空行分条，连续空行并入上一段。
    """
    volumes: Dict[str, List[str]] = {}
    meta: List[str] = []
    current_vol: Optional[str] = None
    para: List[str] = []

    def flush() -> None:
        nonlocal para
        if para:
            if current_vol is not None:
                volumes.setdefault(current_vol, []).append("".join(para))
            para = []

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            flush()
            continue
        if SEPARATOR_RE.match(line):
            continue
        if line in cfg.VOLUME_MAP:
            flush()
            current_vol = line
            meta.append(f"卷边界: {line} -> {cfg.VOLUME_MAP[line]}")
            continue
        if current_vol is None:
            continue  # 卷标记之前的内容（书名行等）不入条目
        para.append(line)
    flush()
    return volumes, meta


# ---------------------------------------------------------------------------
# 卷产物与指纹库
# ---------------------------------------------------------------------------


def build_extract(
    volumes: Dict[str, List[str]], requested: Optional[List[str]]
) -> Dict[str, str]:
    """写 _extract/{vol}_{卷名}.txt（条N|正文），返回 {item_id: original}。"""
    items: Dict[str, str] = {}
    for vol_name, paras in volumes.items():
        vol = cfg.VOLUME_MAP[vol_name]
        if requested is not None and vol not in requested:
            continue
        lines = [f"条{i}|{p}" for i, p in enumerate(paras, start=1)]
        out_path = os.path.join(cfg.EXTRACT_DIR, f"{vol}_{vol_name}.txt")
        tmp = out_path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines) + "\n")
        os.replace(tmp, out_path)
        for i, p in enumerate(paras, start=1):
            items[f"{vol}-{i:03d}"] = p
    return items


def build_registry(
    items: Dict[str, str],
    requested: Optional[List[str]],
    norm_map: Optional[Dict[str, str]],
) -> Dict[str, Dict[str, str]]:
    """构建指纹库（增量合并语义：#12 --volumes 只重算请求卷，其余卷保留不动）。"""
    existing: Dict[str, Dict[str, str]] = load_json(cfg.REGISTRY_FILE, {}) or {}
    new_reg = dict(existing)
    touched_vols = set()
    for item_id, original in items.items():
        vol = item_id.split("-")[0]
        touched_vols.add(vol)
        norm = original
        if norm_map:
            norm = "".join(norm_map.get(ch, ch) for ch in original)  # 单字映射
        new_reg[item_id] = {"original": original, "norm": norm}
    # requested 卷的旧键若本次未重算到（卷内条数变化导致键消失）应清除
    if requested is not None:
        for vol in requested:
            for key in [
                k for k in new_reg if k.startswith(vol + "-") and k not in items
            ]:
                del new_reg[key]
    atomic_write_json(cfg.REGISTRY_FILE, new_reg)
    return new_reg


# ---------------------------------------------------------------------------
# 校验与报告（#6：写文件输出，不依赖 stdout）
# ---------------------------------------------------------------------------


def verify_items(
    registry: Dict[str, Dict[str, str]], expect: Optional[Dict[str, int]]
) -> List[str]:
    """对照预期条数并核对 item_id 连续（卷内 001..N 无缺号）。返回统计行。"""
    lines: List[str] = []
    by_vol: Dict[str, List[str]] = {}
    for item_id in sorted(registry.keys()):
        by_vol.setdefault(item_id.split("-")[0], []).append(item_id)
    for vol in sorted(by_vol.keys()):
        ids = by_vol[vol]
        n = len(ids)
        contig = all(ids[i] == f"{vol}-{i + 1:03d}" for i in range(n))
        lines.append(f"{vol}: {n} 条；编号连续={'是' if contig else '否'}")
        if expect and vol in expect and expect[vol] != n:
            lines.append(f"{vol}: 与预期 {expect[vol]} 不符！")
    lines.append(f"合计: {len(registry)} 条")
    if expect:
        total_expect = sum(expect.values())
        if total_expect != len(registry):
            lines.append(f"合计与预期 {total_expect} 不符！")
    return lines


def write_report(lines: List[str], meta: List[str]) -> str:
    """统计报告落盘到 _validate/annotate_统计.txt，返回路径。"""
    out = os.path.join(cfg.VALIDATE_DIR, "annotate_统计.txt")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("# 底座构建统计\n")
        for m in meta:
            f.write(m + "\n")
        for line in lines:
            f.write(line + "\n")
    return out


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------


def main() -> int:
    cfg.ensure_dirs()
    ap = argparse.ArgumentParser(description="《先进遗风》底座构建（annotate）")
    ap.add_argument(
        "--volumes",
        default=None,
        help="只重算的卷号，逗号分隔（如 01,02）；缺省全量重建",
    )
    ap.add_argument(
        "--norm-map", default=None, help="归一映射 JSON（{原字形/词: 归一词}）"
    )
    ap.add_argument("--expect", default=None, help="预期条数（如 01:58,02:42）")
    ap.add_argument(
        "--source", default=cfg.SOURCE_FILE, help="源全本路径（缺省使用配置默认）"
    )
    args = ap.parse_args()

    requested = volumes_to_rebuild(args.volumes)
    expect: Optional[Dict[str, int]] = None
    if args.expect:
        expect = {k: int(v) for k, v in (p.split(":") for p in args.expect.split(","))}

    if not os.path.exists(args.source):
        print_progress(f"[ERR] 源文件不存在: {args.source}")
        return 1
    with open(args.source, "r", encoding="utf-8-sig") as f:
        text = f.read()

    volumes, meta = parse_source(text)
    if requested is not None:
        missing = [
            v for v in requested if v not in [cfg.VOLUME_MAP[k] for k in volumes]
        ]
        if missing:
            print_progress(f"[ERR] 请求卷在源中未找到: {missing}")
            return 1

    norm_map: Optional[Dict[str, str]] = None
    if args.norm_map:
        raw = load_json(args.norm_map, None)
        norm_map = raw if isinstance(raw, dict) else None
        if norm_map:
            print_progress(f"[info] 应用归一映射 {len(norm_map)} 项")

    items = build_extract(volumes, requested)
    registry = build_registry(items, requested, norm_map)
    stats = verify_items(registry, expect)
    report_path = write_report(stats, meta)

    print_progress("-- 底座构建完成 --")
    for s in stats:
        print_progress("  " + s)
    print_progress(f"报告: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
