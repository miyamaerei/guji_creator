# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - 通用层构建引擎（_kg_layer_builder.py）

供 APPT / REL / L5事件 / OPN / TRL 五个普通层打包器复用（每记录 = 一个业务 ID）。
L1 实体的主键表语义特殊（组级 ID + alias_index），由 build_ent_keys.py 单独实现。

流程（对应 SKILL.md §10 打包器约定：build_ 前缀、可重跑、幂等）：
  1. 逐卷加载 AI 源数据（_src/_<layer>_ai_<vol>.py/.json，源数据键名由 SRC_KEY 映射）
  2. 逐记录：item_id 存在性 -> 注入 original/norm（#3）-> 枚举封闭集硬校验（#27）
     -> 分配业务 ID（段位，#13/#22）-> 补 volume/layer 字段（#19）
  3. 全部校验通过后统一写盘：卷产物 *_<vol>.json + 全局聚合 *_all.json（#12 增量合并）
  4. 问题清单写 _validate/<layer>_打包问题.txt（#6 写文件输出，不依赖 stdout）

退出码：结构性 ERR 为 0；strict 枚举阻断或关键结构错误 -> 1。
"""

from __future__ import annotations

import argparse
import os
from typing import Any, Dict, List, Optional

import _kg_config as cfg
import _kg_enums as enums
from _kg_pack_base import (
    alloc_id,
    atomic_write_json,
    check_enum_fields,
    collect_enum_usage,
    inject_original,
    load_json,
    load_source,
    merge_layer_all,
    print_progress,
    slot_of,
    summary_problems,
    volumes_to_rebuild,
)

# 层 -> 必填字段（缺字段记 GAP，不阻断；「未明」显式写约定见 README）
REQUIRED_FIELDS: Dict[str, List[str]] = {
    "appt": ["person", "office"],
    "rel": ["person_a", "person_b", "relation_type", "direction"],
    "event": ["type", "who", "action"],
    "opn": ["topic", "stance"],
    "trl": ["translation"],
}


def build_records_layer(
    layer: str, requested: Optional[List[str]], strict: bool = False
) -> int:
    """通用层构建入口，返回退出码。"""
    cfg.ensure_dirs()
    prefix = cfg.LAYERS[layer]["id_prefix"]
    src_key = cfg.LAYERS[layer]["src_key"]
    problems: List[str] = []
    usage: Dict[str, Dict[str, int]] = {}

    requested_vols: Optional[List[str]] = requested

    # 读取请求卷（或全部卷）的卷列表：卷号来自配置文件可用的 01/02
    all_vols = sorted(cfg.VOLUME_MAP.values())
    vols = all_vols if requested_vols is None else requested_vols

    vol_records: Dict[str, List[Dict[str, Any]]] = {}
    registry = load_registry_safe()
    for vol in vols:
        top, errs = load_source(layer, vol)
        problems.extend(errs)
        if top is None:
            continue
        records: List[Dict[str, Any]] = []
        raw_list = top.get(src_key) or []
        for idx, rec in enumerate(raw_list, start=1):
            if not isinstance(rec, dict):
                problems.append(f"{layer} 卷{vol} 第{idx}条: 记录必须是 dict")
                continue
            item_id = rec.get("item_id")
            if not item_id:
                problems.append(
                    f"{layer} 卷{vol} 第{idx}条: 缺少 item_id（源数据必须写条号）"
                )
                rec["_gap"] = "缺少 item_id"
            item_id_s = str(item_id or "")
            problems.extend(inject_original(rec, item_id_s, registry))
            # 必填字段
            for f in REQUIRED_FIELDS.get(layer, []):
                if f not in rec or rec[f] is None or rec[f] == "":
                    problems.append(
                        f"{item_id}|{layer}: 缺少必填字段 {f}（GAP，未建模/未明需显式写）"
                    )
            # 枚举校验
            try:
                problems.extend(
                    check_enum_fields(layer, rec, str(item_id), strict=strict)
                )
            except ValueError:
                problems.append(f"{item_id}|{layer}: strict 枚举阻断")
                raise
            collect_enum_usage(layer, rec, usage)
            # 业务 ID（段位分配；源数据不手写，此处强制覆盖）
            rec["id"] = alloc_id(prefix, int(vol), slot_of(rec, idx))
            rec["volume"] = vol
            rec["layer"] = layer
            records.append(rec)
        vol_records[vol] = records

    # 统一写盘（先全量校验，全部通过后再落盘，strict 失败不产生半成品）
    agg_path = os.path.join(cfg.LAYERS_DIR, f"{layer}_all.json")
    if requested_vols is None:
        # 全量重建：一次性合并所有卷，避免逐卷 rebuild 覆盖前卷
        agg = merge_layer_all(agg_path, layer, vol_records, None)
        atomic_write_json(agg_path, agg)
        for vol, records in vol_records.items():
            vol_path = os.path.join(cfg.LAYERS_DIR, f"{layer}_{vol}.json")
            atomic_write_json(
                vol_path,
                {
                    "layer": layer,
                    "volume": vol,
                    "records": records,
                    "total": len(records),
                },
            )
    else:
        # 增量合并（#12）：只重算请求卷，其余卷从既有 _all.json 保留
        agg = load_json(agg_path, {}) or {}
        for vol, records in vol_records.items():
            vol_path = os.path.join(cfg.LAYERS_DIR, f"{layer}_{vol}.json")
            atomic_write_json(
                vol_path,
                {
                    "layer": layer,
                    "volume": vol,
                    "records": records,
                    "total": len(records),
                },
            )
            agg = merge_layer_all(agg_path, layer, {vol: records}, requested_vols)
        atomic_write_json(agg_path, agg) if agg else None

    # 校验问题落盘
    err, gap = summary_problems(problems, layer)
    report_path = os.path.join(cfg.VALIDATE_DIR, f"{layer}_打包问题.txt")
    with open(report_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# {layer} 层打包问题（ERR={err} GAP={gap}）\n")
        for p in problems:
            f.write(p + "\n")
        f.write(f"\n枚举使用分布:\n")
        for enum_key, dist in sorted(usage.items()):
            f.write(f"  {enum_key}: {len(dist)} 种值 {dict(sorted(dist.items()))}\n")

    print_progress(
        f"[{layer}] ERR={err} GAP={gap} 记录合计="
        f"{sum(len(r) for r in vol_records.values())}"
    )
    for v in sorted(vol_records.keys()):
        print_progress(f"  [{layer}] 卷{v}: {len(vol_records[v])} 条")
    print_progress(f"  问题清单: {report_path}")
    return 1 if err > 0 else 0


def load_registry_safe():
    """惰性加载指纹库（避免循环 import）。"""
    from _kg_pack_base import load_registry

    return load_registry()


def main_for(layer: str) -> int:
    cfg.ensure_dirs()
    ap = argparse.ArgumentParser(
        description=f"《先进遗风》{layer.upper()} 层打包器（build_{cfg.LAYERS[layer]['builder']}）"
    )
    ap.add_argument(
        "--volumes", default=None, help="只重算的卷号（01,02）；缺省全量重建"
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="枚举未匹配值直接阻断（#27），缺省收集-报告-暂存",
    )
    args = ap.parse_args()
    try:
        requested = volumes_to_rebuild(args.volumes)
    except ValueError as e:
        print_progress(f"[ERR] {e}")
        return 2
    return build_records_layer(layer, requested, strict=args.strict)
