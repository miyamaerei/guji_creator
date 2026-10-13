# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - L1 实体层打包器（build_ent_keys.py）

语义与其余五层不同：annotation 不逐条分配业务 ID，而是「按 (规范化主名, 类型) 分组」
形成实体主键表 ent_keys.json，跨卷归并同一人物（如卷上「王守仁」卷下「阳明先生」归并为
ENT-01-001 一个实体），卷产物里的每条 annotation 只回填所属组 ent_id。

主键表结构（ent_keys.json）：
    {
      "meta": {"registry_version": 1, "updated_at": ..., "entity_total": N},
      "entities": [
        {"ent_id": "ENT-01-001", "key": "王守仁|person", "normalized": "王守仁",
         "type": "person", "count": 3, "first_source": "01-001",
         "surfaces": ["王守仁", "阳明先生"]}  # 该组出现过的一切原文词形
      ],
      "alias_index": {"王守仁": "ENT-01-001", "阳明先生": "ENT-01-001"},
      "normalized_inventory": [{"normalized": "王守仁", "type": "person", "ent_id": "..."}],
      "pending": [{"reason": "同名异型疑似两人", "surface": "...", "keys": [...]}]
    }

增量归并（#12 只重算请求卷）：
    - 非请求卷的旧组整体保留（跨卷归并信息不回退）；
    - 请求卷注解按 key 匹配旧组：命中 -> 复用旧 ent_id 并合并 surfaces/count/first_source；
    - 未命中 -> 分配新组 ID（首次出现条目的段位槽位），后续卷再出现同 key 自动并入。

用法：
    python build_ent_keys.py [--volumes 01,02] [--strict]
"""

from __future__ import annotations

import argparse
import copy
import os
import time
from typing import Any, Dict, List, Optional

import _kg_config as cfg
import _kg_enums as enums
from _kg_pack_base import (
    alloc_id,
    atomic_write_json,
    check_enum_fields,
    collect_enum_usage,
    load_json,
    load_registry,
    load_source,
    main_guard,
    merge_layer_all,
    print_progress,
    slot_of,
    summary_problems,
    volumes_to_rebuild,
)

ENT_KEYS_FILE = os.path.join(cfg.LAYERS_DIR, "ent_keys.json")


def _read_old_keys() -> Dict[str, Any]:
    """读取旧主键表（无则返回空骨架）。"""
    return load_json(ENT_KEYS_FILE) or {
        "entities": [],
        "alias_index": {},
        "pending": [],
    }


def build_ent_keys(requested: Optional[List[str]], strict: bool = False) -> int:
    """实体层构建主入口，返回退出码。"""
    cfg.ensure_dirs()
    problems: List[str] = []
    usage: Dict[str, Dict[str, int]] = {}
    all_vols = sorted(cfg.VOLUME_MAP.values())
    vols = all_vols if requested is None else requested
    registry = load_registry()

    # 1) 逐卷加载注解并统一校验（该卷注解全部通过才进入分组）
    vol_ann: Dict[str, List[Dict[str, Any]]] = {}
    for vol in vols:
        top, errs = load_source("ent", vol)
        problems.extend(errs)
        if top is None:
            continue
        anns: List[Dict[str, Any]] = []
        raw_list = top.get("annotations") or []
        for idx, rec in enumerate(raw_list, start=1):
            if not isinstance(rec, dict):
                problems.append(f"ent 卷{vol} 第{idx}条: 注解必须是 dict")
                continue
            item_id = rec.get("item_id")
            if not item_id:
                problems.append(
                    f"ent 卷{vol} 第{idx}条: 缺少 item_id（源数据必须写条号）"
                )
                rec["_gap"] = "缺少 item_id"
            item_id_s = str(item_id or "")
            problems.extend(inject_original_ish(rec, item_id_s, registry))
            if not rec.get("text") or not rec.get("type"):
                problems.append(f"{item_id_s}|ent: 缺 text/type（实体注解必填字段）")
            try:
                problems.extend(check_enum_fields("ent", rec, item_id_s, strict=strict))
            except ValueError:
                problems.append(f"{item_id_s}|ent: strict 枚举阻断")
                raise
            if rec.get("normalized") in (None, ""):
                rec["normalized"] = rec["text"]  # 未写主名则原文就是主名
            collect_enum_usage("ent", rec, usage)
            rec["volume"] = vol
            rec["layer"] = "ent"
            anns.append(rec)
        vol_ann[vol] = anns

    # 2) 组级归并（跨卷）
    old = _read_old_keys()
    old_entities: List[Dict[str, Any]] = old.get("entities") or []
    old_by_key: Dict[str, Dict[str, Any]] = {e["key"]: e for e in old_entities}
    old_pending: List[Dict[str, Any]] = old.get("pending") or []

    groups: Dict[str, Dict[str, Any]] = {}  # key = "normalized|type" -> 组
    ent_records: Dict[str, List[Dict[str, Any]]] = {}
    pending_now: List[Dict[str, Any]] = []

    # 2a) 先放入旧表中「不属于本次重算卷」的组，保证非请求卷信息不回退
    for key, e in old_by_key.items():
        src_vol = str(e.get("first_source", "")).split("-", 1)[0]
        if src_vol not in vols:
            groups[key] = copy.deepcopy(e)

    # 2b) 逐卷注解分组：命中旧组复用 ID，否则现场分配
    for vol in vols:
        anns = vol_ann.get(vol, [])
        ents_vol: List[Dict[str, Any]] = []
        for idx, rec in enumerate(anns, start=1):
            key = f"{rec['normalized']}|{rec['type']}"
            g = groups.get(key)
            if g is None:
                g = {
                    "ent_id": alloc_id("ENT-", int(vol), slot_of(rec, idx)),
                    "key": key,
                    "normalized": rec["normalized"],
                    "type": rec["type"],
                    "count": 0,
                    "first_source": rec["item_id"],
                    "surfaces": [],
                }
                groups[key] = g
            rec["ent_id"] = g["ent_id"]
            g["count"] += 1
            if str(g["first_source"]) > str(rec["item_id"]):
                g["first_source"] = rec["item_id"]
            if rec["text"] not in g["surfaces"]:
                g["surfaces"].append(rec["text"])
            ents_vol.append(rec)
        ent_records[vol] = ents_vol

    # 2c) 同名异型待核：同 normalized 不同 type 有两种可能（同名异人 / 一人多职），
    #     按「宁建勿并」保留双组，但写入 pending 供 V2 人工校验
    seen_normalized: Dict[str, List[str]] = {}
    for key, g in groups.items():
        norm, _t = key.split("|", 1)
        seen_normalized.setdefault(norm, []).append(key)
    for norm, keys in seen_normalized.items():
        if len(keys) > 1:
            pending_now.append(
                {
                    "reason": "同主名多类型（同名异人候选）",
                    "surface": norm,
                    "keys": sorted(keys),
                    "ent_ids": [groups[k]["ent_id"] for k in sorted(keys)],
                }
            )

    # 3) 落盘：主键表 + 卷产物 + 全局聚合
    entities = [groups[k] for k in sorted(groups)]
    alias_index: Dict[str, str] = {}
    for g in entities:
        for s in g["surfaces"]:
            alias_index.setdefault(s, g["ent_id"])
    normalized_inventory = [
        {"normalized": g["normalized"], "type": g["type"], "ent_id": g["ent_id"]}
        for g in entities
    ]
    meta = {
        "registry_version": enums.REGISTER_VERSION,
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "entity_total": len(entities),
        "layers_schema": "05-xianjinyifeng-knowledge/references/schemas.md",
    }
    keys_payload = {
        "meta": meta,
        "entities": entities,
        "alias_index": alias_index,
        "normalized_inventory": normalized_inventory,
        "pending": pending_now,
    }
    atomic_write_json(ENT_KEYS_FILE, keys_payload)

    for vol in vols:
        vol_path = os.path.join(cfg.LAYERS_DIR, f"ent_{vol}.json")
        atomic_write_json(
            vol_path,
            {
                "layer": "ent",
                "volume": vol,
                "records": ent_records.get(vol, []),
                "total": len(ent_records.get(vol, [])),
            },
        )
    # 全局聚合与其余五层结构一致（volumes 分卷 + merge_layer_all 合并语义）
    agg_path = os.path.join(cfg.LAYERS_DIR, "ent_all.json")
    agg = merge_layer_all(agg_path, "ent", ent_records, requested)
    atomic_write_json(agg_path, agg)

    # 4) 问题清单落盘（写文件输出，不依赖 stdout）
    err, gap = summary_problems(problems, "ent")
    report_path = os.path.join(cfg.VALIDATE_DIR, "ent_打包问题.txt")
    with open(report_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# ent 层打包问题（ERR={err} GAP={gap}）\n")
        for p in problems:
            f.write(p + "\n")
        f.write(f"\n实体组: {len(entities)}（含跨卷归并）\n")
        f.write(f"别名映射: {len(alias_index)} 词形\n")
        f.write(f"待核: {len(pending_now)} 条\n")
        for p in pending_now:
            f.write(f"  {p['reason']}: {p['surface']} -> {p['ent_ids']}\n")
        f.write("\n枚举使用分布:\n")
        for enum_key, dist in sorted(usage.items()):
            f.write(f"  {enum_key}: {len(dist)} 种值 {dict(sorted(dist.items()))}\n")

    print_progress(
        f"[ent] ERR={err} GAP={gap} 实体组={len(entities)} 注解合计={sum(len(a) for a in ent_records.values())}"
    )
    for v in sorted(ent_records.keys()):
        print_progress(f"  [ent] 卷{v}: {len(ent_records[v])} 条注解")
    print_progress(f"  主键表: {ENT_KEYS_FILE}")
    print_progress(f"  问题清单: {report_path}")
    return 1 if err > 0 else 0


def inject_original_ish(
    rec: Dict[str, Any], item_id: str, registry: Dict[str, Any]
) -> List[str]:
    """实体注解注入 original/norm（引用侧主名规范化，口径见 naming-normalization 记忆）。"""
    from _kg_pack_base import inject_original

    return inject_original(rec, item_id, registry)


def main() -> int:
    cfg.ensure_dirs()
    ap = argparse.ArgumentParser(
        description="《先进遗风》L1 实体层打包器（build_ent_keys）"
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
    return build_ent_keys(requested, strict=args.strict)


if __name__ == "__main__":
    main_guard()
    raise SystemExit(main())
