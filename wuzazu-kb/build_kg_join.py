"""《五杂俎》知识工程 | 跨层整合（_kg_join）

以条（item_id）为主键，把 11 层产物贯通成一行：
    item_id | volume | source | events | rels | nams | cits | objs | cuss |
    opns | mings | appts | trls | ents | layer_count

产物：
    _layers/_kg_join.json          全量贯通（含各层 ID 列表）
    _layers/_kg_join_index.json    精简索引（只留 ID 数组，供检索/建图）
    _deliver/_kg_join_flat.csv     一行一条的扁平表（含原文与译文）
    _build/kg_join_report.json     覆盖统计（一条命中几层 / 各层命中条数）

重跑：python build_kg_join.py [--volumes 01 02] [--minus-ents] [--check]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_pack_base import (  # noqa: E402
    BUILD_DIR,
    BUILD_VERSION,
    DELIVER_DIR,
    JOIN_LAYER_KEYS,
    LAYERS,
    LAYER_JSON_DIR,
    REGISTRY_PATH,
    VOLUME_NAME,
    banner,
    ensure_dirs,
    main_guard,
    now_stamp,
    read_json,
    report_stats,
    write_csv,
    write_json,
)

JOIN_JSON = LAYER_JSON_DIR / "_kg_join.json"
JOIN_INDEX = LAYER_JSON_DIR / "_kg_join_index.json"
JOIN_CSV = DELIVER_DIR / "_kg_join_flat.csv"
JOIN_REPORT = BUILD_DIR / "kg_join_report.json"

# 扁平 CSV 的列序（人可读交付面）
CSV_FIELDS = [
    "item_id", "volume", "volume_name", "layer_count",
    "ents", "events", "rels", "nams", "cits", "objs", "cuss", "opns", "mings", "appts", "trls",
    "event_actions", "rel_pairs", "nam_names", "cit_works", "obj_names",
    "cus_terms", "opn_topics", "ming_whats", "appt_offices", "translation",
    "source", "original", "norm",
]


def load_layer_slices(layer: str, vols: list[str]) -> dict[str, list[dict]]:
    """按卷读取某层记录（缺卷返回空列表）。"""
    out: dict[str, list[dict]] = {}
    for vol in vols:
        obj = read_json(LAYER_JSON_DIR / f"{layer}_{vol}.json", default=None)
        rows = []
        if obj:
            rows = obj.get("records", []) if isinstance(obj, dict) else list(obj)
        out[vol] = rows
    return out


def _ids(records: list[dict], id_field: str) -> list[str]:
    return [str(r.get(id_field, "")) for r in records if r.get(id_field)]


def _texts(records: list[dict], key: str) -> list[str]:
    """取某层用于人读的短标签（动作/人名/书名/名物名/术名/论题/职名）。"""
    out: list[str] = []
    for r in records:
        value = r.get(key)
        if isinstance(value, dict):
            value = value.get("text", "")
        value = str(value or "").strip()
        if value and value not in out:
            out.append(value)
    return out


def _pairs(records: list[dict]) -> list[str]:
    out: list[str] = []
    for r in records:
        a = r.get("person_a")
        b = r.get("person_b")
        a = a.get("text", "") if isinstance(a, dict) else a
        b = b.get("text", "") if isinstance(b, dict) else b
        pair = f"{a or '未明'}—{b or '未明'}"
        if pair not in out:
            out.append(pair)
    return out


def build_join(vols: list[str], include_ents: bool = True) -> tuple[list[dict], dict]:
    registry = read_json(REGISTRY_PATH, default=None) or {}
    layer_records: dict[str, dict[str, list[dict]]] = {}
    for layer in LAYERS:
        if layer == "ent" and not include_ents:
            continue
        layer_records[layer] = load_layer_slices(layer, vols)

    rows: list[dict] = []
    layer_hits: dict[str, int] = {k: 0 for k in JOIN_LAYER_KEYS}
    if include_ents:
        layer_hits["ents"] = 0
    items_by_vol: dict[str, list[str]] = {}
    for item_id in registry:
        vol_id, _, _seq = item_id.partition("-")
        if vol_id in vols:
            items_by_vol.setdefault(vol_id, []).append(item_id)
    for vol in items_by_vol:
        items_by_vol[vol].sort()

    by_layer_item: dict[str, dict[str, list[dict]]] = {}
    for layer, per_vol in layer_records.items():
        index: dict[str, list[dict]] = {}
        for rows_v in per_vol.values():
            for r in rows_v:
                index.setdefault(str(r.get("item_id", "")), []).append(r)
        by_layer_item[layer] = index

    for vol in sorted(items_by_vol):
        for item_id in items_by_vol[vol]:
            row: dict = {
                "item_id": item_id,
                "volume": vol,
                "volume_name": VOLUME_NAME.get(vol, ""),
                "source": f"_extract/{vol}_{VOLUME_NAME.get(vol, '')}.txt",
            }
            count = 0
            for layer, key in JOIN_LAYER_KEYS.items():
                records = by_layer_item.get(layer, {}).get(item_id, [])
                id_field = LAYERS[layer]["id_field"]
                row[key] = _ids(records, id_field)
                if records:
                    count += 1
                    layer_hits[key] = layer_hits.get(key, 0) + len(records)
            if include_ents:
                ents = by_layer_item.get("ent", {}).get(item_id, [])
                row["ents"] = _ids(ents, "ent_id")
                if ents:
                    count += 1
                    layer_hits["ents"] = layer_hits.get("ents", 0) + len(ents)
            row["layer_count"] = count
            # 人读标签（扁平表用）
            ev = by_layer_item.get("event", {}).get(item_id, [])
            rl = by_layer_item.get("rel", {}).get(item_id, [])
            nm = by_layer_item.get("nam", {}).get(item_id, [])
            ct = by_layer_item.get("cit", {}).get(item_id, [])
            ob = by_layer_item.get("obj", {}).get(item_id, [])
            cs = by_layer_item.get("cus", {}).get(item_id, [])
            op = by_layer_item.get("opn", {}).get(item_id, [])
            mi = by_layer_item.get("ming", {}).get(item_id, [])
            ap = by_layer_item.get("appt", {}).get(item_id, [])
            tr = by_layer_item.get("trl", {}).get(item_id, [])
            row["event_actions"] = _texts(ev, "action")
            row["rel_pairs"] = _pairs(rl)
            row["nam_names"] = _texts(nm, "name")
            row["cit_works"] = [str((c.get("cited_work") or {}).get("text", "")) for c in ct]
            row["obj_names"] = [str((c.get("name") or {}).get("text", "")) for c in ob]
            row["cus_terms"] = _texts(cs, "term")
            row["opn_topics"] = _texts(op, "topic")
            row["ming_whats"] = _texts(mi, "what")
            row["appt_offices"] = [str((a.get("office") or {}).get("text", "")) for a in ap]
            row["translation"] = str((tr[0] if tr else {}).get("translation", ""))
            entry = registry.get(item_id, {})
            row["original"] = entry.get("original", "")
            row["norm"] = entry.get("norm", "")
            rows.append(row)

    total = len(rows)
    report = {
        "generated_at": now_stamp(),
        "builder": BUILD_VERSION,
        "volumes": vols,
        "items": total,
        "layer_hits": layer_hits,
        "coverage": _coverage(rows, total),
        "empty_items": sum(1 for r in rows if r["layer_count"] == 0),
    }
    return rows, report


def _coverage(rows: list[dict], total: int) -> dict:
    dist: dict[int, int] = {}
    for r in rows:
        dist[r["layer_count"]] = dist.get(r["layer_count"], 0) + 1
    per_volume: dict[str, dict] = {}
    for r in rows:
        slot = per_volume.setdefault(r["volume"], {"items": 0, "hit_items": 0, "layers_sum": 0})
        slot["items"] += 1
        slot["layers_sum"] += r["layer_count"]
        if r["layer_count"]:
            slot["hit_items"] += 1
    for vol, slot in per_volume.items():
        slot["avg_layers"] = round(slot["layers_sum"] / slot["items"], 3) if slot["items"] else 0.0
    return {
        "layer_count_distribution": {str(k): v for k, v in sorted(dist.items())},
        "items_with_any_layer": sum(v for k, v in dist.items() if k > 0),
        "coverage_ratio": round(sum(v for k, v in dist.items() if k > 0) / total, 4) if total else 0.0,
        "per_volume": per_volume,
    }


def main() -> None:
    import argparse

    from _kg_pack_base import build_context

    # build_context 之外再补本模块私有开关
    argv = sys.argv[1:]
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--minus-ents", action="store_true",
                    help="贯通时跳过实体层（只做 10 个解读层的条-层索引）")
    known, rest = ap.parse_known_args(argv)
    sys.argv = [sys.argv[0]] + rest
    args, vols = build_context("跨层整合 _kg_join")
    banner("跨层整合 build_kg_join")
    include_ents = not known.minus_ents
    rows, report = build_join(vols, include_ents=include_ents)

    if not args.check:
        ensure_dirs()
        # 精简索引：只留各层 ID 数组，便于检索/建图
        index_rows = [{"item_id": r["item_id"], "volume": r["volume"],
                       "layer_count": r["layer_count"],
                       **{k: r.get(k, []) for k in JOIN_LAYER_KEYS},
                       **({"ents": r.get("ents", [])} if include_ents else {})}
                      for r in rows]
        write_json(JOIN_INDEX, {"generated_at": now_stamp(), "count": len(index_rows),
                                "rows": index_rows})
        write_json(JOIN_JSON, {"generated_at": now_stamp(), "builder": BUILD_VERSION,
                               "count": len(rows), "rows": rows})
        write_csv(JOIN_CSV, rows, CSV_FIELDS)
        write_json(JOIN_REPORT, report)

    report_stats("贯通统计", {
        "覆盖卷": len(vols),
        "条目数": report["items"],
        "零层条目": report["empty_items"],
        "命中至少一层": report["coverage"]["items_with_any_layer"],
        "覆盖率": f"{report['coverage']['coverage_ratio'] * 100:.2f}%",
        **{f"层 {k}": v for k, v in report["layer_hits"].items()},
    })
    if not args.check:
        print(f"\n[产物] {JOIN_JSON.name} | {JOIN_INDEX.name} | _deliver/_kg_join_flat.csv | "
              f"_build/kg_join_report.json")


if __name__ == "__main__":
    main_guard(main)
