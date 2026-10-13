# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - 跨层整合打包器（build_kg_join.py）

把六层产物 + 条目指纹库汇总为统一的知识图谱索引，是「跨层整合」阶段的唯一出口，
消费方是 validate_layers.py 与交付物生成器，不要直接依赖 *_all.json 的零散结构。

产物：
    data/_layers/kg_join.json      机器可读主索引（fingerprints / layers / counts）
    data/_layers/kg_join_flat.csv  逻辑行扁平表（#18：按 JSON 记录逻辑行计数，
                                    非物理行数；含原始字节供审计）

逻辑行 = layer 一层的一个顶层记录（每行一级），嵌套数组（如 annotations 内多条注解）
作为一层内的逻辑行各自占行，不横向平铺（保持「一行一记录」稳定可 diff）。
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
from typing import Any, Dict, List, Optional

import _kg_config as cfg
from _kg_pack_base import (
    atomic_write_json,
    load_json,
    load_registry,
    main_guard,
    print_progress,
    volumes_to_rebuild,
    all_records_of,
)

JOIN_JSON = os.path.join(cfg.LAYERS_DIR, "kg_join.json")
JOIN_CSV = os.path.join(cfg.LAYERS_DIR, "kg_join_flat.csv")


def _flat_layer(layer: str, all_vols: List[str]) -> List[Dict[str, Any]]:
    """聚合某层所有卷的逻辑记录（用 *_all.json 若存在，否则回退逐卷）。"""
    all_path = os.path.join(cfg.LAYERS_DIR, f"{layer}_all.json")
    data = load_json(all_path)
    if data:
        return (
            all_records_of(data)
            if data.get("volumes")
            else list(data.get("records", []))
        )
    rows: List[Dict[str, Any]] = []
    for vol in all_vols:
        p = os.path.join(cfg.LAYERS_DIR, f"{layer}_{vol}.json")
        d = load_json(p)
        if d:
            rows.extend(d.get("records", []))
    return rows


def build_kg_join(requested: Optional[List[str]]) -> int:
    """重建跨层索引。requested 仅作用于提示信息；索引本身总是全量重建（轻量）。"""
    cfg.ensure_dirs()
    all_vols = sorted(cfg.VOLUME_MAP.values())
    registry = load_registry()

    fingerprints: List[Dict[str, Any]] = []
    for key, orig in sorted((registry or {}).items()):
        norm = (orig or {}).get("norm", "") if isinstance(orig, dict) else ""
        fingerprints.append(
            {
                "item_id": key,
                "volume": key.split("-", 1)[0],
                "original": orig.get("original", "") if isinstance(orig, dict) else "",
                "norm": norm,
            }
        )

    layers: Dict[str, Dict[str, Any]] = {}
    flat_rows: List[Dict[str, Any]] = []
    for layer in cfg.LAYER_ORDER:
        rows = _flat_layer(layer, all_vols)
        layers[layer] = {"records": rows, "total": len(rows)}
        for r in rows:
            flat_rows.append(
                {
                    "layer": layer,
                    "id": r.get("id", r.get("ent_id", "")),
                    "item_id": r.get("item_id", r.get("_gap", "")),
                    "volume": r.get("volume", ""),
                    "text": _row_short(r),
                    "json": json.dumps(r, ensure_ascii=False),
                }
            )

    payload = {
        "meta": {
            "project": "先进遗风",
            "source": cfg.SOURCE_FILE,
            "schema": "05-xianjinyifeng-knowledge/references/schemas.md",
            "total_fingerprints": len(fingerprints),
            "layers_total": {k: v["total"] for k, v in layers.items()},
        },
        "fingerprints": fingerprints,
        "layers": layers,
    }
    atomic_write_json(JOIN_JSON, payload)

    # 逻辑行 CSV（#18：行数 = 逻辑记录数，由本文件生成可审计）
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["layer", "id", "item_id", "volume", "text", "json"])
    for r in flat_rows:
        w.writerow(
            [r["layer"], r["id"], r["item_id"], r["volume"], r["text"], r["json"]]
        )
    with open(JOIN_CSV, "w", encoding="utf-8", newline="\n") as f:
        f.write(buf.getvalue())

    scope = "全部" if requested is None else ",".join(requested)
    print_progress(f"[kg_join] 重建完成（{scope}）: 指纹库 {len(fingerprints)} 条")
    for layer in cfg.LAYER_ORDER:
        print_progress(f"  [{layer}] {layers[layer]['total']} 逻辑记录")
    print_progress(f"  -> {JOIN_JSON}")
    print_progress(f"  -> {JOIN_CSV}（{len(flat_rows)} 逻辑行）")
    return 0


def _row_short(r: Dict[str, Any]) -> str:
    """取记录里最能说明内容的字段做 CSV 摘要列。"""
    for k in ("text", "translation", "topic", "relation_type", "office", "action"):
        if r.get(k):
            v = str(r[k]).replace("\n", " ").replace("\r", " ")
            return v[:80]
    return ""


def main() -> int:
    cfg.ensure_dirs()
    ap = argparse.ArgumentParser(
        description="《先进遗风》跨层整合打包器（build_kg_join）"
    )
    ap.add_argument("--volumes", default=None, help="提示用卷范围；索引本身全量重建")
    args = ap.parse_args()
    try:
        requested = volumes_to_rebuild(args.volumes)
    except ValueError as e:
        print_progress(f"[ERR] {e}")
        return 2
    return build_kg_join(requested)


if __name__ == "__main__":
    main_guard()
    raise SystemExit(main())
