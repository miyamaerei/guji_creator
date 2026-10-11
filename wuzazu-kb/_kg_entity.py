"""《五杂俎》知识工程 | 实体层（L1）实现与实体表索引

两件事：
1. 实体层（ent）的归一、去重、主键表构建；
2. `_layers/ent_index.json` —— 供事件 / 关系 / 名录 / 引书 / 名物 /
   方俗 / 纪事 / 职官各层回填 *_ent_ids 的查询表（词形 → ENT 主键）。

索引回填口径（skill）：词形归一后查表；同名异人（同词形、不同类型）
不强行合并，写入 `_build/ent_ambiguous.csv` 待核清单，索引取首个类型
为缺省，其余保留在 `candidates` 里。绝不静默丢弃。
"""

from __future__ import annotations

from typing import Any

from _kg_pack_base import (
    ALL_VOLUMES,
    BUILD_DIR,
    BUILD_VERSION,
    LAYER_JSON_DIR,
    SRC_DIR,
    VOLUME_NAME,
    IdAllocator,
    ensure_dirs,
    inject_original,
    load_registry,
    load_sources,
    normalize_text,
    now_stamp,
    read_json,
    write_csv,
    write_json,
    write_text,
)

# --------------------------------------------------------------------------
# 常量
# --------------------------------------------------------------------------

ENUM_NAME = "entity_type"

# 词形归一：类型别名 -> 规范类型（skill 口径：office→official、book→work）
TYPE_ALIAS: dict[str, str] = {
    "office": "official",
    "book": "work",
    "person_name": "person",
    "place_name": "place",
    "book_name": "work",
    "dynasty": "era",
    "title": "official",
}

# 规范类型集合（与 _kg_enums.entity_type 叶子对齐，缺项时以枚举为准）
CANONICAL_TYPES: tuple[str, ...] = (
    "person", "place", "work", "official", "era",
    "object", "animal", "plant", "food", "unknown",
)

INDEX_PATH = LAYER_JSON_DIR / "ent_index.json"
ALIAS_INDEX_PATH = LAYER_JSON_DIR / "ent_alias_index.json"
INVENTORY_PATH = LAYER_JSON_DIR / "ent_normalized_inventory.json"
KEYS_PATH = LAYER_JSON_DIR / "ent_keys.json"
ENT_TABLE_PATH = BUILD_DIR / "ent_table.json"
AMBIGUOUS_PATH = BUILD_DIR / "ent_ambiguous.csv"
COVERAGE_PATH = BUILD_DIR / "ent_coverage.csv"

ENT_ID_FIELD = "ent_id"
RECORD_ID_FIELD = "id"
ID_PREFIX = "ENT-"


# --------------------------------------------------------------------------
# 类型与词形归一
# --------------------------------------------------------------------------


def canon_type(value: Any) -> str:
    raw = normalize_text(str(value or ""))
    if not raw:
        return "unknown"
    raw = TYPE_ALIAS.get(raw, raw)
    if raw not in CANONICAL_TYPES:
        return "unknown"
    return raw


def canon_surface(value: Any) -> str:
    """词形归一键：去空白与常见虚字尾，作为索引主键。"""
    text = normalize_text(str(value or ""))
    return text.strip("　 ")


def ent_sort_key(row: dict) -> tuple:
    return (str(row.get("item_id", "")), int(row.get("start") or 0),
            canon_surface(row.get("text", "")))


# --------------------------------------------------------------------------
# 索引
# --------------------------------------------------------------------------


def _scan_volumes() -> list[str]:
    return [v for v in ALL_VOLUMES if (SRC_DIR / f"_ent_ai_{v}.py").exists()]


def _make_index(entries: list[dict]) -> dict[str, Any]:
    """按词形建索引；同名多类型进 candidates，缺省取首个。"""
    index: dict[str, Any] = {}
    amb: list[dict] = []
    for row in entries:
        key = canon_surface(row.get("normalized") or row.get("text", ""))
        if not key:
            continue
        slot = index.get(key)
        cand = {"id": row[ENT_ID_FIELD], "type": row.get("type", "unknown"),
                "item_id": row.get("item_id", "")}
        if slot is None:
            index[key] = cand
            continue
        cands = slot.setdefault("candidates", [])
        if not any(c["id"] == cand["id"] for c in cands):
            cands.append(cand)
        if slot.get("type") != cand.get("type"):
            amb.append({"normalized": key, "type_a": slot.get("type"),
                        "ent_a": slot.get("id"), "type_b": cand.get("type"),
                        "ent_b": cand.get("id"), "item_id": row.get("item_id", "")})
    return {"index": index, "ambiguous": amb}


def index_from_artifacts() -> dict[str, Any]:
    """从已落盘的每卷实体 JSON 重建索引（不读源数据）。"""
    entries: list[dict] = []
    for vol in ALL_VOLUMES:
        obj = read_json(LAYER_JSON_DIR / f"ent_{vol}.json", default=None)
        if not obj:
            continue
        entries.extend(obj.get("records", []) if isinstance(obj, dict) else obj)
    return _make_index(entries)


def load_entity_index(force: bool = False) -> dict[str, Any]:
    """装载实体索引（优先用已落盘的 ent_index.json）。"""
    if not force:
        obj = read_json(INDEX_PATH, default=None)
        if obj and obj.get("index"):
            return obj["index"]
    return index_from_artifacts().get("index", {})


def rebuild_entity_index(write: bool = True) -> dict[str, Any]:
    """按源数据重建实体层产物与索引（不依赖 CLI 上下文）。

    返回索引本身；数据源为空时退回已落盘产物，绝不因缺源而抛错。
    """
    vols = _scan_volumes()
    if vols:
        registry = load_registry()
        alloc = IdAllocator(ID_PREFIX)
        per_volume: dict[str, list[dict]] = {}
        for vol in vols:
            rows, _ = build_volume_records(vol, registry, alloc)
            per_volume[vol] = rows
        all_records = [r for v in sorted(per_volume) for r in per_volume[v]]
        all_records.sort(key=lambda r: r[ENT_ID_FIELD])
        entities, alias_index, ambiguous = build_keys(all_records)
        inventory = build_inventory(all_records)
        index = _make_index(all_records)["index"]
        if write:
            for vol, rows in per_volume.items():
                write_json(LAYER_JSON_DIR / f"ent_{vol}.json", {
                    "layer": "ent", "volume": vol, "name": VOLUME_NAME.get(vol, ""),
                    "count": len(rows), "generated_at": now_stamp(),
                    "builder": BUILD_VERSION, "records": rows,
                })
            write_json(INVENTORY_PATH, {"generated_at": now_stamp(),
                                        "count": len(inventory),
                                        "normalized_inventory": inventory})
            write_json(KEYS_PATH, {"generated_at": now_stamp(), "count": len(entities),
                                   "entities": entities, "alias_index": alias_index})
            write_json(INDEX_PATH, {"generated_at": now_stamp(), "count": len(index),
                                    "index": index})
            write_json(ALIAS_INDEX_PATH, {"generated_at": now_stamp(),
                                          "count": len(alias_index),
                                          "index": {k: {"id": v, "type": ""}
                                                    for k, v in alias_index.items()}})
            write_csv(AMBIGUOUS_PATH, ambiguous,
                      ["surface", "ent_a", "ent_b", "type", "item_id"])
        return index
    return index_from_artifacts().get("index", {})


# --------------------------------------------------------------------------
# 实体层打包
# --------------------------------------------------------------------------


def iter_ent_sources(volume: str) -> list[dict]:
    return load_sources("ent", [volume]).get(volume, [])


def build_volume_records(volume: str, registry: dict, alloc: IdAllocator) -> tuple[list[dict], list[dict]]:
    """打包单卷实体记录：返回 (records, 待核同名异人)。"""
    srcs = iter_ent_sources(volume)
    rows: list[dict] = []
    for src in srcs:
        item_id = str(src.get("item_id") or "").strip()
        if not item_id:
            seq = src.get("seq") or src.get("条")
            if seq:
                item_id = f"{volume}-{int(seq):03d}"
        if item_id not in registry:
            continue
        text = normalize_text(str(src.get("text") or src.get("词形") or ""))
        if not text:
            continue
        start = src.get("start")
        end = src.get("end")
        if start in (None, ""):
            start = registry[item_id]["original"].find(text) + 1 if text else 0
        if end in (None, ""):
            end = (int(start or 0) + len(text) - 1) if start else 0
        rows.append({
            "volume": volume,
            "item_id": item_id,
            "text": text,
            "type": canon_type(src.get("type") or src.get("类型")),
            "start": int(start or 0),
            "end": int(end or 0),
            "normalized": canon_surface(src.get("normalized") or text),
            "confidence": src.get("confidence", "high"),
            "source": src.get("source", "ai"),
        })
    rows.sort(key=ent_sort_key)
    for row in rows:
        inject_original(row, registry)
        row[ENT_ID_FIELD] = alloc.next()
    return rows, []


def build_inventory(records: list[dict]) -> list[dict]:
    """归一汇总：normalized + type 归并，记录次数与来源。"""
    table: dict[tuple[str, str], dict] = {}
    for row in records:
        key = (canon_surface(row.get("normalized")), row.get("type", "unknown"))
        slot = table.get(key)
        if slot is None:
            slot = {"normalized": key[0], "type": key[1], "count": 0,
                    "first_source": row.get("item_id", ""), "surfaces": []}
            table[key] = slot
        slot["count"] += 1
        surface = row.get("text", "")
        if surface and surface not in slot["surfaces"]:
            slot["surfaces"].append(surface)
    return sorted(table.values(), key=lambda r: (-r["count"], r["normalized"]))


def build_keys(records: list[dict]) -> tuple[list[dict], dict[str, str], list[dict]]:
    """实体主键表 + 别名索引 + 同名异人待核清单。"""
    table: dict[tuple[str, str], dict] = {}
    alias_index: dict[str, str] = {}
    ambiguous: list[dict] = []
    for row in records:
        key = (canon_surface(row.get("normalized")), row.get("type", "unknown"))
        slot = table.get(key)
        if slot is None:
            slot = {"ent_id": row[ENT_ID_FIELD], "normalized": key[0], "type": key[1],
                    "count": 0, "first_source": row.get("item_id", ""), "surfaces": []}
            table[key] = slot
        slot["count"] += 1
        surface = row.get("text", "")
        if surface and surface not in slot["surfaces"]:
            slot["surfaces"].append(surface)
        prev = alias_index.get(surface)
        if prev is None:
            alias_index[surface] = slot["ent_id"]
        elif prev != slot["ent_id"]:
            ambiguous.append({"surface": surface, "ent_a": prev, "ent_b": slot["ent_id"],
                              "type": key[1], "item_id": row.get("item_id", "")})
        alias_index.setdefault(canon_surface(surface), slot["ent_id"])
    entities = sorted(table.values(), key=lambda r: (-r["count"], r["normalized"]))
    return entities, alias_index, ambiguous


def run_ent_layer(args, volumes: list[str]) -> dict:
    """实体层主流程：写 _layers/ent_NN.json + 主键表 + 索引。"""
    ensure_dirs()
    registry = load_registry()
    alloc = IdAllocator(ID_PREFIX)
    per_volume: dict[str, list[dict]] = {}
    for vol in volumes:
        rows, _ = build_volume_records(vol, registry, alloc)
        per_volume[vol] = rows

    all_records: list[dict] = []
    for vol in ALL_VOLUMES:
        if vol in per_volume:
            all_records.extend(per_volume[vol])
        else:
            obj = read_json(LAYER_JSON_DIR / f"ent_{vol}.json", default=None)
            if obj:
                all_records.extend(obj.get("records", []) if isinstance(obj, dict) else obj)
    all_records.sort(key=lambda r: (r["ent_id"]))

    inventory = build_inventory(all_records)
    entities, alias_index, ambiguous = build_keys(all_records)
    built = _make_index(all_records)
    index = built["index"]
    ambiguous.extend(built["ambiguous"])

    total = sum(len(v) for v in per_volume.values())
    stats = {
        "layer": "ent",
        "id_prefix": ID_PREFIX,
        "volumes": len(volumes),
        "records": total,
        "id_range": f"{ID_PREFIX}001~{ID_PREFIX}{total:03d}" if total else "-",
        "entities_dedup": len(entities),
        "inventory": len(inventory),
        "alias_keys": len(alias_index),
        "ambiguous_same_name": len(ambiguous),
        "sources_found": sum(1 for v in volumes if iter_ent_sources(v)),
        "checked_only": bool(args.check),
    }
    if args.check:
        return stats

    for vol in volumes:
        payload = {"layer": "ent", "volume": vol, "name": VOLUME_NAME.get(vol, ""),
                   "count": len(per_volume[vol]), "generated_at": now_stamp(),
                   "builder": BUILD_VERSION, "records": per_volume[vol]}
        write_json(LAYER_JSON_DIR / f"ent_{vol}.json", payload)

    write_json(INVENTORY_PATH, {"generated_at": now_stamp(), "count": len(inventory),
                                "normalized_inventory": inventory})
    write_json(KEYS_PATH, {"generated_at": now_stamp(), "count": len(entities),
                           "entities": entities, "alias_index": alias_index})
    write_json(INDEX_PATH, {"generated_at": now_stamp(), "count": len(index),
                            "index": index})
    write_json(ALIAS_INDEX_PATH, {"generated_at": now_stamp(), "count": len(alias_index),
                                  "index": {k: {"id": v, "type": ""} for k, v in alias_index.items()}})
    write_json(ENT_TABLE_PATH, {"generated_at": now_stamp(), "entities": entities})
    write_csv(AMBIGUOUS_PATH, ambiguous,
              ["surface", "ent_a", "ent_b", "type", "item_id"])
    write_csv(COVERAGE_PATH, [
        {"volume": v, "name": VOLUME_NAME.get(v, ""), "count": len(per_volume.get(v, []))}
        for v in ALL_VOLUMES
    ], ["volume", "name", "count"])

    # 层汇总（增量合并）
    from _kg_layers import _write_layer_summary
    from _kg_pack_base import LAYERS
    _write_layer_summary("ent", LAYERS["ent"], volumes, per_volume)
    _write_text_report(stats, entities, inventory)
    return stats


def _write_text_report(stats: dict, entities: list[dict], inventory: list[dict]) -> None:
    lines = [
        "《五杂俎》实体层（L1）摘要",
        "=" * 40,
        f"生成时间：{now_stamp()}",
        f"实体出现记录数：{stats['records']}",
        f"去重后实体数：{stats['entities_dedup']}",
        f"归一汇总条目：{stats['inventory']}",
        f"索引键数：{stats['alias_keys']}",
        f"同名异人待核：{stats['ambiguous_same_name']}",
        "",
        "出现频次 Top 20：",
    ]
    for row in entities[:20]:
        lines.append(f"  {row['ent_id']}  {row['normalized']}（{row['type']}）×{row['count']}"
                     f"  首次 {row['first_source']}")
    write_text(BUILD_DIR / "ent_report.txt", "\n".join(lines) + "\n")
