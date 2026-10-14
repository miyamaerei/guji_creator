#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Timeline Views —— TME 时间沿革的派生视图（SKILL §11 / schemas §8）。

位置：在 enrich_layers.py 之后、build_kg_join.py 之前运行。
数据源：_layers/tmes/tmes.json（已校验层，enrich 后含 era/target/action/related_evo）。

产出（_views/timeline/）：
  <制度或机构>.json   按 office 聚合的 TME 条目，REIGN_ORDER 升序 + year 升序（time_key）
  _index.json         全部视图索引（office -> 文件、条目数、时间跨度）

纪律：只读 tmes.json，不修改任何层文件；文件名来自 office 文本（清洗非法字符后）；
time_key = f"{REIGN_ORDER[reign]:02d}-{year or 0:04d}"，同 key 按 id 稳定排序。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    BASE_DIR,
    REIGN_ORDER,
    VIEWS_DIR,
    load_json,
    save_json,
)

TME_FILE = BASE_DIR / "_layers" / "tmes" / "tmes.json"
OUT_DIR = VIEWS_DIR / "timeline"
INDEX_FILE = OUT_DIR / "_index.json"


def _slug(office: str) -> str:
    """office 名 → 安全文件名（保留中文/数字/字母，其余转 _）。"""
    s = re.sub(r'[\\/:*?"<>|\s]+', "_", office.strip())
    s = re.sub(r"_+", "_", s).strip("_")
    return s[:60] or "未命名"


def _time_key(reign: str, year) -> str:
    rk = REIGN_ORDER.get(reign, 99)
    yk = int(year) if isinstance(year, int) else 0
    return f"{rk:02d}-{yk:04d}"


def main() -> None:
    print("=== Build Timeline Views ===")
    data = load_json(TME_FILE, {})
    recs = data.get("records", [])
    print(f"  TME 源: {len(recs)} 条")

    # 按 office 聚合
    groups: Dict[str, List[dict]] = {}
    for r in recs:
        off = r.get("office", "") or "未命名"
        groups.setdefault(off, []).append(r)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    index: Dict[str, dict] = {}
    n_entries = 0
    for off in sorted(groups):
        items = groups[off]
        # 按 reign 顺序 + year 升序，同 key 按 id 稳定
        items.sort(
            key=lambda x: (
                REIGN_ORDER.get(x.get("reign", ""), 99),
                int(x.get("era", {}).get("year") or 0)
                if isinstance(x.get("era"), dict)
                else 0,
                x.get("id", ""),
            )
        )
        view = {
            "office": off,
            "entry_count": len(items),
            "entries": [],
        }
        for x in items:
            era = x.get("era") if isinstance(x.get("era"), dict) else {}
            reign = era.get("reign") or x.get("reign", "")
            year = era.get("year")
            view["entries"].append(
                {
                    "id": x.get("id", ""),
                    "item_id": x.get("item_id", ""),
                    "category": x.get("category", ""),
                    "reign": reign,
                    "year": year,
                    "time_key": _time_key(reign, year),
                    "action": x.get("action", ""),
                    "content": x.get("content", ""),
                    "target": x.get("target", {}),
                    "related_evo": x.get("related_evo", ""),
                    "ref_item": x.get("ref_item", ""),
                }
            )
            n_entries += 1
        fname = _slug(off) + ".json"
        save_json(OUT_DIR / fname, view)
        yrs = [e["year"] for e in view["entries"] if e["year"] is not None]
        index[off] = {
            "file": fname,
            "entry_count": len(items),
            "reign_span": [view["entries"][0]["reign"], view["entries"][-1]["reign"]],
            "year_span": [min(yrs), max(yrs)] if yrs else None,
        }

    save_json(
        INDEX_FILE,
        {
            "views": len(index),
            "entries": n_entries,
            "items": dict(sorted(index.items())),
        },
    )
    print(f"  视图: {len(index)} 个 office / 共 {n_entries} 条 TME 条目")
    print(f"  输出: {OUT_DIR.relative_to(BASE_DIR)}/（含 _index.json）")
    print("=== build_views 完成 ===")


if __name__ == "__main__":
    main()
