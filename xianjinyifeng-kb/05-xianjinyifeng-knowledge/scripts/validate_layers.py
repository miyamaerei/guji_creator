# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - 构建校验器（validate_layers.py）

在六层打包 + kg_join 之后运行，输出「验证结论」：
    data/_validate/验证缺漏清单.txt   逐层缺漏清单（ERR 阻断项 / GAP 宽容项），
                                     本文件问题数 = 0 才算达标（T5 验收标尺）
    data/_validate/V2待核清单.csv     同名异人候选 + 低置信(<CONFIDENCE_WARN) 记录
    data/_validate/枚举分布.txt       六层枚举实际使用值与预注册封闭集的偏离

校验项：
    E1 指纹库完整性：条数、编号连续
    E2 层-卷覆盖：每层每卷产物存在且 total 一致
    E3 TRL 全覆盖：翻译条数 = 条目数（--expect-trl 覆盖冒烟场景）
    E4 枚举口径：实际值 ⊆ 封闭集（未注册值记 ERR）；漂移比值 > 1.5 告警
    E5 ID 命名空间：跨层无前缀冲突、单层内 ID 无重复（段位撞号）
    E6 join 完整性：kg_join 层 total 与各 *_all.json 一致
    E7 CSV 逻辑行一致：kg_join_flat.csv 逻辑行数 = 各层 total 之和

用法：
    python validate_layers.py                 # 全量标准校验（条数=100，TRL 全覆盖）
    python validate_layers.py --skip-baseline # 冒烟：跳过条数/TRL 全覆盖基线比对
    python validate_layers.py --expect-trl 4  # 指定 TRL 期望条数（部分装填阶段）
"""

from __future__ import annotations

import argparse
import csv
import os
from typing import Any, Dict, List, Optional

import _kg_config as cfg
import _kg_enums as enums
from _kg_pack_base import (
    all_records_of,
    load_json,
    load_registry,
    main_guard,
    print_progress,
)

VALIDATE_TXT = os.path.join(cfg.VALIDATE_DIR, "验证缺漏清单.txt")
PENDING_CSV = os.path.join(cfg.VALIDATE_DIR, "V2待核清单.csv")
ENUM_TXT = os.path.join(cfg.VALIDATE_DIR, "枚举分布.txt")

DEFAULT_EXPECT_TOTAL = (
    100  # 指纹库预期条数：卷上 58 + 卷下 42（见 annotate.py --expect）
)


def _load_layer_records(layer: str) -> List[Dict[str, Any]]:
    """汇总某层全部逻辑记录（用 *_all.json，兼容 volumes/records 两种结构）。"""
    d = load_json(os.path.join(cfg.LAYERS_DIR, f"{layer}_all.json"))
    if not d:
        return []
    if d.get("volumes"):
        return all_records_of(d)
    return list(d.get("records", []))


def _loaded_src_volumes(all_vols: List[str]) -> List[str]:
    """已装填源数据的卷：_src 中存在任一 _<layer>_ai_<vol>.py|.json。"""
    loaded = []
    for vol in all_vols:
        if any(
            os.path.exists(os.path.join(cfg.SRC_DIR, f"_{layer}_ai_{vol}.py"))
            or os.path.exists(os.path.join(cfg.SRC_DIR, f"_{layer}_ai_{vol}.json"))
            for layer in cfg.LAYER_ORDER
        ):
            loaded.append(vol)
    return loaded


def validate_layers(
    skip_baseline: bool = False, expect_total: Optional[int] = None
) -> int:
    cfg.ensure_dirs()
    problems: List[str] = []
    all_vols = sorted(cfg.VOLUME_MAP.values())
    registry = load_registry()
    exp_total = expect_total if expect_total is not None else len(registry)

    # E1 指纹库完整性
    reg_ids = sorted(registry.keys())
    problems.append(f"[E1] 指纹库条数: {len(reg_ids)}")
    if not skip_baseline and len(reg_ids) != DEFAULT_EXPECT_TOTAL:
        problems.append(
            f"[E1-ERR] 指纹库条数 {len(reg_ids)} != 预期 {DEFAULT_EXPECT_TOTAL}"
        )
    for vol in all_vols:
        prefix = f"{vol}-"
        ids = [i for i in reg_ids if i.startswith(prefix)]
        expected = [f"{prefix}{n:03d}" for n in range(1, len(ids) + 1)]
        if ids != expected:
            missing = [e for e in expected if e not in ids]
            extra = [i for i in ids if i not in expected]
            problems.append(f"[E1-ERR] 卷{vol} 编号缺口: 缺 {missing} 多 {extra}")
        else:
            problems.append(f"[E1] 卷{vol} 编号连续 {len(ids)} 条 OK")

    # E2/E3 层-卷覆盖与 TRL 全覆盖（#12：未装填卷跳过低校验，只列 GAP）
    loaded_vols = _loaded_src_volumes(all_vols)
    for vol in all_vols:
        if vol not in loaded_vols:
            problems.append(
                f"[E2-GAP] 卷 {vol} 未装填源数据（_src/*_ai_{vol}.*），跳过层覆盖校验"
            )
    unbuilt = [v for v in all_vols if v not in loaded_vols]
    layer_total: Dict[str, int] = {}
    for layer in cfg.LAYER_ORDER:
        recs = _load_layer_records(layer)
        layer_total[layer] = len(recs)
        missing_vols = [v for v in all_vols if v not in unbuilt]
        miss = [
            v
            for v in missing_vols
            if not os.path.exists(os.path.join(cfg.LAYERS_DIR, f"{layer}_{v}.json"))
        ]
        if miss:
            problems.append(
                f"[E2-ERR] 层 {layer} 缺已装填卷产物: {miss}（请先跑 build_{layer}）"
            )
        problems.append(f"[E2] 层 {layer}: {len(recs)} 逻辑记录")
    if not skip_baseline and layer_total.get("trl", 0) != exp_total:
        problems.append(
            f"[E3-ERR] TRL 未全覆盖: {layer_total.get('trl', 0)} != {exp_total}"
        )

    # E4 枚举口径（按 ENUM_FIELD_MAP 的 (layer, field) 精确路由收集，避免同名字段串层）
    enum_txt_lines: List[str] = []
    for enum_key, entry in enums.ENUM_REGISTRY.items():
        allowed = entry["values"]
        used_values: Dict[str, int] = {}
        routes = [
            (layer, field)
            for layer, pairs in enums.ENUM_FIELD_MAP.items()
            for field, ek in pairs
            if ek == enum_key
        ]
        if not routes:
            continue
        for layer, field in routes:
            for r in _load_layer_records(layer):
                v = r.get(field)
                if v is not None and v != "":
                    used_values[str(v)] = used_values.get(str(v), 0) + 1
        field_name = ", ".join(f"{l}.{f}" for l, f in routes)
        unknown = [v for v in used_values if v not in allowed]
        if unknown and not skip_baseline:
            problems.append(
                f"[E4-ERR] 字段 {field_name} 使用未注册值: {unknown}（请走枚举修正流程）"
            )
        ratio = len(used_values) / len(allowed) if allowed else 0.0
        if ratio > 1.5:
            problems.append(
                f"[E4-WARN] 口径漂移: {field_name} 实际 {len(used_values)}/{len(allowed)} 定义值（>1.5）"
            )
        enum_txt_lines.append(
            f"{field_name} -> {enum_key}: 实际 {len(used_values)}/{len(allowed)} 定义值 比值 {ratio:.2f}\n"
            f"    实际值: {sorted(used_values)}\n"
        )
    with open(ENUM_TXT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# 枚举口径分布（#27 封闭集 + 漂移告警）\n")
        f.writelines(enum_txt_lines)

    # E5 ID 命名空间唯一性（跨层/段位撞号）
    seen: Dict[str, str] = {}
    dup = False
    for layer in cfg.LAYER_ORDER:
        for r in _load_layer_records(layer):
            i = r.get("id") or r.get("ent_id")
            if not i:
                continue
            i = str(i)
            prev = seen.get(i)
            if prev is not None and prev != layer:
                problems.append(f"[E5-ERR] ID {i} 跨层冲突: {prev} vs {layer}")
            elif prev == layer:
                dup = True
            seen[i] = layer
    if dup:
        problems.append(
            "[E5-ERR] 存在单层内重复 ID（段位撞号），请检查 SEGMENT_CAPACITY"
        )

    # E6 join 完整性
    join = load_json(os.path.join(cfg.LAYERS_DIR, "kg_join.json"))
    if join is None:
        problems.append("[E6-ERR] kg_join.json 不存在（请先跑 build_kg_join）")
    else:
        jt = join.get("meta", {}).get("layers_total", {})
        for layer in cfg.LAYER_ORDER:
            if jt.get(layer) != layer_total[layer]:
                problems.append(
                    f"[E6-ERR] kg_join 层 {layer} total {jt.get(layer)} != 实产 {layer_total[layer]}"
                )
        if not skip_baseline:
            fp = join.get("meta", {}).get("total_fingerprints")
            if fp != DEFAULT_EXPECT_TOTAL:
                problems.append(
                    f"[E6-ERR] kg_join 指纹库 {fp} != {DEFAULT_EXPECT_TOTAL}"
                )

    # E7 CSV 逻辑行一致
    csv_path = os.path.join(cfg.LAYERS_DIR, "kg_join_flat.csv")
    logical_rows = 0
    if os.path.exists(csv_path):
        with open(csv_path, "r", encoding="utf-8") as f:
            for _row in csv.reader(f):
                logical_rows += 1
        logical_rows = max(logical_rows - 1, 0)  # 减表头
    expect_rows = sum(layer_total.values())
    if logical_rows != expect_rows:
        problems.append(
            f"[E7-ERR] kg_join_flat.csv 逻辑行 {logical_rows} != 各层合计 {expect_rows}"
        )

    # V2 待核清单（同名异人候选 + 低置信）
    pend_rows: List[List[str]] = [["layer", "id", "item_id", "reason", "detail"]]
    keys_p = load_json(os.path.join(cfg.LAYERS_DIR, "ent_keys.json"))
    if keys_p:
        for p in keys_p.get("pending", []):
            pend_rows.append(
                [
                    "ent",
                    ",".join(p.get("ent_ids", [])),
                    "",
                    p.get("reason", ""),
                    p.get("surface", ""),
                ]
            )
    for layer in cfg.LAYER_ORDER:
        for r in _load_layer_records(layer):
            conf = r.get("confidence")
            if conf is None:
                continue
            try:
                if float(conf) < cfg.CONFIDENCE_WARN:
                    pend_rows.append(
                        [
                            layer,
                            str(r.get("id") or r.get("ent_id", "")),
                            str(r.get("item_id", "")),
                            "低置信",
                            f"confidence={conf}",
                        ]
                    )
            except (TypeError, ValueError):
                pass
    with open(PENDING_CSV, "w", encoding="utf-8-sig", newline="\n") as f:
        csv.writer(f).writerows(pend_rows)

    # 汇总判定（ERR 计入问题数）
    errs = [p for p in problems if "-ERR" in p]
    with open(VALIDATE_TXT, "w", encoding="utf-8", newline="\n") as f:
        f.write("# 《先进遗风》验证缺漏清单（T5 验收标尺：问题数 = 0）\n")
        for p in problems:
            f.write(p + "\n")
        f.write(f"\n# 结论: ERR问题数 = {len(errs)}\n")

    print_progress(f"[validate] 验证缺漏清单.txt ERR问题数 = {len(errs)}")
    print_progress(f"  -> {VALIDATE_TXT}")
    print_progress(f"  -> {PENDING_CSV}（{len(pend_rows) - 1} 条待核）")
    print_progress(f"  -> {ENUM_TXT}")
    return 1 if errs else 0


def main() -> int:
    cfg.ensure_dirs()
    ap = argparse.ArgumentParser(
        description="《先进遗风》构建校验器（validate_layers）"
    )
    ap.add_argument(
        "--skip-baseline",
        action="store_true",
        help="冒烟模式：跳过指纹库条数/TRL 全覆盖基线比对",
    )
    ap.add_argument(
        "--expect-trl",
        type=int,
        default=None,
        help="TRL 期望条数（部分装填阶段用；缺省=指纹库条数）",
    )
    args = ap.parse_args()
    return validate_layers(
        skip_baseline=args.skip_baseline, expect_total=args.expect_trl
    )


if __name__ == "__main__":
    main_guard()
    raise SystemExit(main())
