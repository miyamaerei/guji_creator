# -*- coding: utf-8 -*-
"""《客座赘语》知识工程 | T3 自检（字段完整性 / 主键与关联一致性 / 词形一致性 / 回查清单 / 抽样原文回查）

用法：python validate_layers.py [--volumes 01]
输出：_validate/t3_report_<NN>.json + 终端摘要

词形一致性（warning 级，不阻断 PASS）：引用侧文本字段若命中 ent 层
normalized≠text 的旧词形则记 warning，提示回查改为主名；original/文本类
长注中保留原文词形的正常引述不视为错误。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_pack_base import (
    JOIN_LAYER_KEYS,
    LAYERS,
    VOLUME_NAME,
    layer_json_path,
    read_layer_volume,
)

# 必须非空字段：直接取打包基线 LAYERS 配置中的 must_fields（排除 item_id，主键另查）
MUST_LAYER_NOT_NULL: dict[str, list[str]] = {
    layer: [f for f in cfg["must_fields"] if f != "item_id"]
    for layer, cfg in LAYERS.items()
}

# 引用字段（值应为 ID 列表）→ 校验指向存在的 ID
ID_REF_FIELDS = [
    "person_ent_ids",
    "office_ent_ids",
    "institution_ent_ids",
    "who_ent_ids",
    "cited_ent_ids",
    "name_ent_ids",
    "location_ent_ids",
    "author_ent_ids",
    "evidence_refs",
    "ref_events",
    "ref_appts",
    "subject_ent_ids",
    "agent_ent_ids",
    "person_a_ent_ids",
    "person_b_ent_ids",
    "source_ent_ids",
    "ent_ids",
]


def _read_all(layer: str, volumes: list[str]) -> list[dict]:
    out: list[dict] = []
    for vol in volumes:
        out.extend(read_layer_volume(layer, vol))
    return out


def _read_join(volumes: list[str]) -> list[dict]:
    """读 _layers/_kg_join.json（唯一跨层 join 产物，rows 键 + 每行 volume 字段）。"""
    p = Path(__file__).resolve().parent / "_layers" / "_kg_join.json"
    if not p.exists():
        return []
    obj = json.loads(p.read_text(encoding="utf-8"))
    rows = obj.get("rows", []) if isinstance(obj, dict) else obj
    return [r for r in rows if str(r.get("volume", "")) in volumes]


# 引用侧 ID 字段（已校验指向），词形检查跳过这些键，只扫文本字段
ID_REF_KEYS = set(ID_REF_FIELDS) | {
    "item_id",
    "volume",
    "volume_name",
    "original",
    "norm",
    "start",
    "end",
    "_layer",
    "source",
    "evidence",
    "translation",
    "ent_id",
}


def _iter_texts(value) -> list[str]:
    """递归收集 value 中所有字符串叶子（list/dict 均摊开），用于词形匹配。"""
    out: list[str] = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, list):
        for x in value:
            out.extend(_iter_texts(x))
    elif isinstance(value, dict):
        for x in value.values():
            out.extend(_iter_texts(x))
    return out


def _form_and_review(
    volumes: list[str], report: dict, join_rows: list[dict]
) -> tuple[list[dict], dict]:
    """词形一致性（引用侧须用主名，否则 warning）+ 建议回查清单。

    返回 (form_warnings, review_hints)：
      - compound_top:   按条内记录数最多的复合条 top 5（跨层合计）
      - variant_items:  词形差异涉及的条目（引用侧命中旧词形的 item_id 去重）
      - dense_rel_opn:  rels>=2 或 opns>=2 的关系/观点密集条
    """
    # 1) ent 层 normalized != text 的旧词形映射（打包后记录）
    ent_old_to_new: dict[str, str] = {}
    for rec in _read_all("ent", volumes):
        text = rec.get("text") or ""
        norm = rec.get("normalized") or ""
        if norm and norm != text:
            ent_old_to_new.setdefault(text, norm)

    # 2) 引用侧非 ent 层记录扫描
    warnings: list[dict] = []
    for layer in LAYERS:
        if layer == "ent":
            continue
        cfg = LAYERS[layer]
        id_field = cfg["id_field"]
        for rec in _read_all(layer, volumes):
            if not isinstance(rec, dict):
                continue
            rid = str(rec.get(id_field, ""))
            item_id = str(rec.get("item_id", ""))
            for field, value in rec.items():
                if field in ID_REF_KEYS:
                    continue
                for txt in _iter_texts(value):
                    if not txt:
                        continue
                    for old, new in sorted(
                        ent_old_to_new.items(), key=len, reverse=True
                    ):
                        # 原文语料中主名 might 含旧词形子串，只匹配整词/2+ 字差异
                        if len(old) >= 2 and old in txt:
                            warnings.append(
                                {
                                    "layer": layer,
                                    "id": rid,
                                    "item_id": item_id,
                                    "field": field,
                                    "found": old,
                                    "should": new,
                                }
                            )

    # 3) 复合条 top（按条内记录数，跨层合计）
    per_item: dict[str, dict] = {}
    for layer in LAYERS:
        cfg = LAYERS[layer]
        id_field = cfg["id_field"]
        for rec in _read_all(layer, volumes):
            if not isinstance(rec, dict):
                continue
            item_id = str(rec.get("item_id", ""))
            if not item_id:
                continue
            agg = per_item.setdefault(item_id, {"records": 0, "layers": set()})
            agg["records"] += 1
            agg["layers"].add(layer)
    compound_top = [
        {"item_id": iid, "records": agg["records"], "layers": sorted(agg["layers"])}
        for iid, agg in sorted(
            per_item.items(), key=lambda kv: (-kv[1]["records"], kv[0])
        )[:5]
    ]

    # 4) rel/opn 密集条（自 join 行计数字段）
    dense: list[dict] = []
    for row in join_rows:
        rels = row.get("rels") or []
        opns = row.get("opns") or []
        rn = len(rels) if isinstance(rels, list) else (1 if rels else 0)
        on = len(opns) if isinstance(opns, list) else (1 if opns else 0)
        if rn >= 2 or on >= 2:
            dense.append({"item_id": row.get("item_id"), "rels": rn, "opns": on})
    dense.sort(key=lambda d: -(d["rels"] + d["opns"]))

    variant_items = sorted({w["item_id"] for w in warnings})
    review_hints = {
        "compound_top": compound_top,
        "variant_items": variant_items,
        "dense_rel_opn": dense,
    }
    report["form_check"] = {
        "old_forms": len(ent_old_to_new),
        "checked_volumes": volumes,
        "warnings": warnings,
    }
    report["review_hints"] = review_hints
    return warnings, review_hints


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--volumes", default="01")
    args = ap.parse_args()
    volumes = [v.strip() for v in args.volumes.split(",") if v.strip()]

    report: dict = {"volumes": volumes, "layers": {}, "join": {}, "sampled": []}
    all_ids: dict[str, set[str]] = {}  # id_prefix -> set of ids
    item_id_set: dict[
        str, dict[str, list[str]]
    ] = {}  # layer -> item_id -> [record ids]

    # 1) 逐层字段完整 + 主键收集
    for layer in LAYERS:
        cfg = LAYERS[layer]
        id_field = cfg["id_field"]
        prefix = cfg["id_prefix"] + "-"
        lid = {"missing": [], "dup_ids": [], "bad_refs": [], "count": 0}
        id_set: set[str] = set()
        records = _read_all(layer, volumes)
        lid["count"] = len(records)
        per_item: dict[str, list[str]] = {}
        for rec in records:
            rid = str(rec.get(id_field, ""))
            if not rid:
                lid["missing"].append({"id": rid, "why": "无主键"})
                continue
            if rid in id_set:
                lid["dup_ids"].append(rid)
            id_set.add(rid)
            item_id = str(rec.get("item_id", ""))
            per_item.setdefault(item_id, []).append(rid)
            # 必须非空字段
            for f in MUST_LAYER_NOT_NULL.get(layer, []):
                v = rec.get(f)
                if v is None or v == "" or v == [] or v == {}:
                    lid["missing"].append({"id": rid, "why": f"字段 {f} 为空"})
        all_ids[prefix] = id_set
        item_id_set[layer] = per_item
        report["layers"][layer] = lid

    # 2) 关联一致性：引用字段必须指向存在的层 ID；item_id 需存在于 registry 可注入卷
    registry_path = Path(__file__).resolve().parent / "_item_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    # 建 id -> layer 反查表（用于判断引用是否跨层指向正确前缀）
    id_to_layer: dict[str, str] = {}
    for layer, ids in all_ids.items():
        for rid in ids:
            id_to_layer[rid] = layer

    for layer in LAYERS:
        cfg = LAYERS[layer]
        id_field = cfg["id_field"]
        records = _read_all(layer, volumes)
        for rec in records:
            rid = str(rec.get(id_field, ""))
            item_id = str(rec.get("item_id", ""))
            if item_id and item_id not in registry:
                report["layers"][layer].setdefault("bad_refs", []).append(
                    {"id": rid, "why": f"item_id {item_id} 不在 registry"}
                )
            for f in ID_REF_FIELDS:
                v = rec.get(f)
                if not v:
                    continue
                refs = v if isinstance(v, list) else [v]
                for ref in refs:
                    ref = str(ref)
                    if ref not in id_to_layer:
                        report["layers"][layer]["bad_refs"].append(
                            {"id": rid, "why": f"{f} 引用 {ref} 不存在"}
                        )

    # 3) join 贯通性
    join_records: list[dict] = _read_join(volumes)
    join_layer_keys = (
        [k[2:] for k in JOIN_LAYER_KEYS.values()]
        if isinstance(JOIN_LAYER_KEYS, dict)
        else []
    )
    empty = 0
    hit_any = 0
    for row in join_records:
        has = any(
            row.get(f)
            for f in ("item_id",)
            + tuple(
                k
                for k in row
                if k.endswith("_ids") or k in ("translation", "layer_count")
            )
        )
        if not has:
            empty += 1
        if row.get("layer_count", 0) > 0:
            hit_any += 1
    report["join"] = {
        "count": len(join_records),
        "zero_layer": empty,
        "with_any_layer": hit_any,
    }

    # 3.5) 词形一致性（warning 级）+ 建议回查清单
    norm_check, review_hints = _form_and_review(volumes, report, join_records)

    # 4) 汇总
    total_missing = sum(len(v["missing"]) for v in report["layers"].values())
    total_dup = sum(len(v["dup_ids"]) for v in report["layers"].values())
    total_bad_refs = sum(len(v["bad_refs"]) for v in report["layers"].values())
    total_form_warn = len(report["form_check"]["warnings"])
    ok = (
        total_missing == 0
        and total_dup == 0
        and total_bad_refs == 0
        and report["join"]["zero_layer"] == 0
    )

    print("=" * 68)
    print(f"《客座赘语》知识工程 | T3 自检（卷 {','.join(volumes)}）")
    print("=" * 68)
    for layer in LAYERS:
        v = report["layers"][layer]
        print(
            f"  {layer:<5} {v['count']:>3} 条 | 缺字段 {len(v['missing'])} | "
            f"重复ID {len(v['dup_ids'])} | 坏引用 {len(v['bad_refs'])}"
        )
    print(
        f"  跨层 _kg_join {report['join']['count']} 条 | 零层 {report['join']['zero_layer']} | "
        f"至少一层 {report['join']['with_any_layer']}"
    )
    print(
        f"  词形一致性 | 旧词形登记 {report['form_check']['old_forms']} | "
        f"引用侧命中 {total_form_warn} 处（warning，须回查主名）"
    )
    hints = report["review_hints"]
    if hints["compound_top"]:
        top_txt = " ".join(
            f"{h['item_id']}({h['records']})" for h in hints["compound_top"]
        )
        print(f"  复合条 top5 | {top_txt}")
    if hints["variant_items"]:
        print(
            f"  词形差异条 {len(hints['variant_items'])} 条 | "
            f"{' '.join(hints['variant_items'][:12])}"
        )
    if hints["dense_rel_opn"]:
        dense_txt = " ".join(
            f"{d['item_id']}(rel{d['rels']}/opn{d['opns']})"
            for d in hints["dense_rel_opn"][:10]
        )
        print(f"  rel/opn 密集条 {len(hints['dense_rel_opn'])} 条 | {dense_txt}")
    print(
        f"[结论] {'PASS' if ok else 'FAIL'} | 缺字段 {total_missing} | 重复ID {total_dup} | 坏引用 {total_bad_refs}"
    )

    out = Path(__file__).resolve().parent / "_validate" / f"t3_report_{volumes[0]}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[产物] {out}")


if __name__ == "__main__":
    main()
