# -*- coding: utf-8 -*-
"""
时间线视图生成器 —— _views/timeline/<item_id>.json
======================================================

对应 schemas.md §10「查询视图」：按政区聚合的沿革时间线 JSON（每政区 = 一文件）。

数据来源：TME 纪年事件（何时发生）+ EVO 阶段切片（政区视角阶段），按 item_id
归并、按（reign 顺序, year, slot）排序后输出；两源互补，同一政区一条时间线。

输出：
  _views/timeline/<item_id>.json   每条目一文件
  _views/timeline/_index.json      全书索引（item_id -> 条目名 + 事件数）

用法：
  python scripts/build_timeline.py            # 重建全部
  python scripts/build_timeline.py 01,03      # 只重建指定卷
"""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402
from _kg_enums import REIGN_ORDER  # noqa: E402

# TME 事件优先显示，EVO 阶段为补充（避免双写同一沿革）
_KIND = {"tme": "事件", "evo": "阶段"}


def _read(obj: dict) -> list:
    return obj.get("records", [])


def _sort_key(ev) -> tuple:
    reign = ev.get("reign", "")
    order = REIGN_ORDER.get(reign, 999)
    year = ev.get("year", 0) if isinstance(ev.get("year", 0), int) else 0
    return (order, year, ev.get("slot", 0))


def _project(r: dict, layer: str) -> dict:
    """投影为时间线条目（统一字段）。"""
    out = {
        "kind": _KIND.get(layer, layer),
        "id": r.get("id", ""),
        "era_raw": r.get("era_raw", ""),
        "year": r.get("year", None),
        "reign": r.get("reign", ""),
    }
    if layer == "tme":
        out["category"] = r.get("category", "")
        out["text"] = r.get("event", "")
    else:
        out["change_type"] = r.get("change_type", "")
        out["text"] = r.get("change", "")
    return out


def build(volumes=None) -> dict:
    by_item: dict[str, list] = {}
    index: dict[str, dict] = {}

    for layer in ("tmes", "evos"):
        for p in C.layer_files(layer):
            vol = os.path.basename(p).split("_")[-1].split(".")[0]
            if volumes is not None and vol not in volumes:
                continue
            for r in _read(_load(p)):
                item = r.get("item_id", "")
                if not item:
                    continue
                by_item.setdefault(item, []).append(_project(r, layer.rstrip("s")))

    out_dir = os.path.join(C.PATHS["views"], "timeline")
    os.makedirs(out_dir, exist_ok=True)
    for item, evs in sorted(by_item.items()):
        evs.sort(key=_sort_key)
        doc = {"item_id": item, "events": evs, "count": len(evs)}
        C.atomic_write_json(os.path.join(out_dir, f"{item}.json"), doc)
        index[item] = {"count": len(evs), "first": evs[0]["era_raw"] if evs else ""}

    C.atomic_write_json(
        os.path.join(out_dir, "_index.json"),
        {
            "generator": "build_timeline.py",
            "item_count": len(index),
            "items": index,
        },
    )
    return index


def _load(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    vols = None
    if len(sys.argv) > 1:
        vols = set(sys.argv[1].split(","))
    index = build(vols)
    total = sum(v["count"] for v in index.values())
    print(
        "OK timeline: items=%d events=%d -> %s"
        % (len(index), total, os.path.join(C.PATHS["views"], "timeline"))
    )


if __name__ == "__main__":
    main()
