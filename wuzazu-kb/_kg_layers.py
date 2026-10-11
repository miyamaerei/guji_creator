"""《五杂俎》知识工程 | 各层打包引擎（配置驱动）

本模块把"每层打包器"的公共逻辑收敛到一处：
    读源数据 -> 原文注入 -> 枚举校验 -> 引用解析 -> 稳定排序 -> 分配 ID -> 落盘

每层的差异只用 ENGINE 里的一份配置描述（源字段 -> 目标字段 -> 形状），
新增层 = ENGINE 加一项，不需要复制打包代码。

形状（shape）约定：
    scalar      标量
    dict        嵌套对象，如 who = {text, who_ent_ids}
    dictlist    对象数组，如 nam.entries / appt.inst 等
    list        数组
    enum        标量 + 枚举校验（未知值入 pending，不中断）
    undecided   未考处，必须显式写 "未明"（skill 口径：不许留空）

约定：源数据（_src/_<layer>_ai_<NN>.py）只写条号与解读字段，
original / norm 一律由 _item_registry.json 注入，业务 ID 由本引擎分配。
"""

from __future__ import annotations

from typing import Any, Callable

import _kg_enums as E
from _kg_pack_base import (
    ALL_VOLUMES,
    BUILD_DIR,
    BUILD_VERSION,
    COMMON_KEYS,
    LAYERS,
    UNKNOWN,
    VOLUME_NAME,
    IdAllocator,
    ensure_dirs,
    collect_layer_records,
    inject_original,
    layer_json_path,
    layer_sort_key,
    load_registry,
    load_sources,
    normalize_text,
    now_stamp,
    read_json,
    write_json,
    write_volume_products,
)

# 叶子字段命名不统一时的别名归一（源数据允许写简写）
FIELD_ALIASES: dict[str, str] = {
    "ent_id": "id",
    "who_ids": "who_ent_ids",
    "ent_ids": "ent_ids",
    "person_ids": "person_ent_ids",
    "official_ids": "official_ent_ids",
    "inst_ids": "inst_ent_ids",
    "region_ids": "region_ent_ids",
    "work_ids": "work_ent_ids",
    "a_ids": "a_ent_ids",
    "b_ids": "b_ent_ids",
}

# 未考处枚举字段：允许写 "未明"，其余值按枚举校验
UNDECIDED = "未明"

# 翻译层风格基准标注（references/translation-style.md：余光中风格七条）
TRL_NOTE = "余光中风格基准"

# 各层源字段 -> 目标字段（值 = (形状, 枚举名 or None)）
SHAPE_DICT = "dict"
SHAPE_DICT_LIST = "dictlist"
SHAPE_LIST = "list"

# 该字段为空时是否必须显式 "未明"（skill：未考处必须显式声明）
REQUIRE_UNDECIDED = {
    "event": ("who", "when", "where"),
    "ming": ("when", "where"),
    "appt": ("when",),
}


# --------------------------------------------------------------------------
# 层配置
# --------------------------------------------------------------------------
# 每项：
#   shape       字段形状
#   enum        枚举名（_kg_enums.BASE_ENUMS 的键）
#   refs        该层引用字段 -> 被引用的 ent type（用于回填 *_ent_ids）
#   sub         嵌套对象内部叶子结构（自解释、供 schema 文档与校验使用）
#   note        口径备注

ENGINE: dict[str, dict[str, dict[str, Any]]] = {
    "event": {
        "who": {"shape": SHAPE_DICT, "sub": {"text": "scalar", "who_ent_ids": "list"},
                "refs": "person", "note": "事件主体，可为群体（如「群臣」）"},
        "type": {"shape": "enum", "enum": "event_type"},
        "action": {"shape": "scalar"},
        "what": {"shape": "scalar"},
        "when": {"shape": "undecided", "note": "未考处必须显式 未明"},
        "where": {"shape": "undecided", "note": "未考处必须显式 未明"},
    },
    "rel": {
        "person_a": {"shape": SHAPE_DICT, "sub": {"text": "scalar", "ent_ids": "list"},
                     "refs": "person"},
        "person_b": {"shape": SHAPE_DICT, "sub": {"text": "scalar", "ent_ids": "list"},
                     "refs": "person"},
        "relation_type": {"shape": "enum", "enum": "relation_type"},
        "direction": {"shape": "enum", "enum": "relation_direction"},
        "evidence": {"shape": "scalar"},
    },
    "nam": {
        "name": {"shape": "scalar", "note": "名录/谱牒名称，如「嘉靖八才子」"},
        "category": {"shape": "enum", "enum": "nam_category"},
        "scope": {"shape": "scalar"},
        "entries": {"shape": SHAPE_DICT_LIST,
                    "item_sub": {"seq": "scalar", "person": "scalar",
                                 "courtesy_name": "scalar",
                                 "hometown": "scalar", "office": "scalar"}},
        "ent_ids": {"shape": "list", "refs": "person",
                    "note": "名录成员实体（回填）"},
    },
    "cit": {
        "cited_work": {"shape": SHAPE_DICT, "sub": {"text": "scalar", "ent_ids": "list"},
                       "refs": "work", "note": "被引书名/篇名"},
        "citation_type": {"shape": "enum", "enum": "citation_type"},
        "context": {"shape": "enum", "enum": "citation_context"},
    },
    "obj": {
        "name": {"shape": SHAPE_DICT, "sub": {"text": "scalar", "ent_ids": "list"},
                 "refs": "object"},
        "category": {"shape": "enum", "enum": "obj_category"},
        "attributes": {"shape": SHAPE_DICT, "note": "随名物类别而异，自由键"},
        "lore": {"shape": "scalar", "note": "掌故/考据补充"},
    },
    "cus": {
        "type": {"shape": "enum", "enum": "cus_type"},
        "region": {"shape": SHAPE_DICT, "sub": {"text": "scalar", "ent_ids": "list"},
                   "refs": "place"},
        "term": {"shape": "scalar"},
        "description": {"shape": "scalar"},
    },
    "opn": {
        "topic": {"shape": "scalar"},
        "stance": {"shape": "enum", "enum": "opn_stance"},
        "argument": {"shape": "scalar"},
        "evidence_refs": {"shape": "list", "note": "条号或本层 ID 引用，如 01-012 / WZZ-E-004"},
    },
    "ming": {
        "era": {"shape": "scalar"},
        "who": {"shape": SHAPE_DICT, "sub": {"text": "scalar", "ent_ids": "list"},
                "refs": "person"},
        "what": {"shape": "scalar"},
        "when": {"shape": "undecided"},
        "where": {"shape": "undecided"},
        "category": {"shape": "enum", "enum": "ming_category"},
        "first_person": {"shape": "scalar", "note": "true/false：是否作者亲历"},
        "ref_events": {"shape": "list", "note": "引用的事件层 ID"},
    },
    "appt": {
        "person": {"shape": SHAPE_DICT, "sub": {"text": "scalar", "person_ent_ids": "list"},
                   "refs": "person"},
        "office": {"shape": SHAPE_DICT, "sub": {"text": "scalar", "official_ent_ids": "list"},
                   "refs": "official"},
        "institution": {"shape": SHAPE_DICT, "sub": {"text": "scalar", "ent_ids": "list"}},
        "when": {"shape": "undecided"},
        "status": {"shape": "enum", "enum": "appt_status"},
        "evidence": {"shape": "scalar"},
    },
    "trl": {
        "translation": {"shape": "scalar", "note": "古今对译正文，风格七条余光中基准"},
        "style": {"shape": "enum", "enum": "trl_style"},
        "note": {"shape": "scalar", "note": "默认「余光中风格基准」"},
        "confidence": {"shape": "scalar"},
    },
}

# 各层汇总产物文件名
SUMMARY_NAME = "_summary.json"


# --------------------------------------------------------------------------
# 形状工具
# --------------------------------------------------------------------------


def default_for(field: str, spec: dict) -> Any:
    shape = spec.get("shape", "scalar")
    if shape == SHAPE_DICT:
        sub = spec.get("sub", {})
        out = {}
        for k, ks in sub.items():
            out[k] = [] if ks == SHAPE_LIST else ""
        return out
    if shape == SHAPE_DICT_LIST:
        return []
    if shape == SHAPE_LIST:
        return []
    if shape == "undecided":
        return UNKNOWN
    return ""


def blank_record(layer: str) -> dict:
    """按 ENGINE 生成空记录骨架（供 --check / 表单提示使用）。"""
    rec: dict = {"item_id": ""}
    for field, spec in ENGINE.get(layer, {}).items():
        rec[field] = default_for(field, spec)
    return rec


def _inline_spec(layer: str, field: str, kind: str) -> dict[str, Any]:
    """把 ENGINE 中 sub/item_sub 的形状转成 spec，供递归归一。"""
    spec: dict[str, Any] = {"shape": kind}
    parent = ENGINE.get(layer, {}).get(field, {})
    sub = parent.get("sub") if kind == SHAPE_DICT else parent.get("item_sub")
    if sub:
        spec["sub"] = sub
    return spec


# --------------------------------------------------------------------------
# 引用回填：实体层 -> 本层 *_ent_ids
# --------------------------------------------------------------------------


def resolve_entity_ids(texts: list[str], ent_type: str | None,
                       index: dict[str, Any] | None) -> tuple[list[str], list[str]]:
    """按词形（norm）在实体表里查实体 ID。返回 (命中 ID, 未命中词形)。"""
    if not index:
        return [], [t for t in texts if str(t).strip()]
    ids: list[str] = []
    miss: list[str] = []
    for raw in texts:
        key = normalize_text(str(raw))
        if not key:
            continue
        hit = index.get(key)
        if hit is None and "\u3000" in str(raw):
            hit = index.get(str(raw))
        if hit is None:
            miss.append(key)
            continue
        if isinstance(hit, str):
            hit = {"id": hit, "type": ""}
        if ent_type and hit.get("type") and hit["type"] != ent_type:
            # 类型不符：仍记入 ID，同时登记为待核
            miss.append(f"{key}@{hit.get('type')}")
        ids.append(hit["id"])
    # 去重保序
    seen: set[str] = set()
    uniq = [i for i in ids if not (i in seen or seen.add(i))]
    return uniq, miss


def fill_refs(layer: str, record: dict, field: str, spec: dict,
              index: dict[str, Any] | None, miss_log: list[dict]) -> None:
    """回填单个嵌套引用节点（内部工具，供 resolve_refs 复用）。"""
    shape = spec.get("shape")
    if shape != SHAPE_DICT or not isinstance(record.get(field), dict):
        return
    node = record[field]
    id_key = _leaf_id_key(spec)
    if node.get(id_key):
        return
    ids, miss = resolve_entity_ids([node.get("text", "")], spec.get("refs"), index)
    node[id_key] = ids
    if miss and node.get("text"):
        miss_log.append({"layer": layer, "item_id": record.get("item_id", ""),
                         "field": f"{field}.{id_key}", "text": node.get("text", ""),
                         "miss": miss})


# --------------------------------------------------------------------------
# 枚举校验（收集 - 报告 - 暂存）
# --------------------------------------------------------------------------


def check_enum(layer: str, field: str, value: Any, enum_name: str | None,
               item_id: str, unknown_log: list[dict]) -> Any:
    if enum_name is None:
        return value
    raw = "" if value is None else str(value)
    if raw == UNDECIDED:
        return raw
    fixed, bad = E.validate(enum_name, raw, where=f"{layer}.{field}@{item_id}")
    if bad is not None:
        unknown_log.append({"layer": layer, "item_id": item_id, "field": field,
                            "enum": enum_name, "value": raw})
    return fixed


# --------------------------------------------------------------------------
# 记录归一
# --------------------------------------------------------------------------


def _norm_value(layer: str, field: str, value: Any, spec: dict, item_id: str,
                unknown_log: list[dict]) -> Any:
    shape = spec.get("shape", "scalar")
    if shape == SHAPE_DICT:
        sub = spec.get("sub", {})
        if not isinstance(value, dict):
            value = {"text": value} if value not in (None, "") else default_for(field, spec)
        out: dict[str, Any] = {}
        for k, ks in sub.items():
            v = value.get(k)
            if ks == SHAPE_LIST:
                if v is None:
                    v = []
                elif not isinstance(v, list):
                    v = [v]
                out[k] = [_scalar_or_unknown(ks, x, spec.get("required_undecided")) for x in v]
            else:
                out[k] = _scalar_or_unknown(ks, v, spec.get("required_undecided"))
        # 保留源数据额外键（如 attributes 自由键 / 名录成员扩展）
        for k, v in value.items():
            out.setdefault(k, v)
        return out
    if shape == SHAPE_DICT_LIST:
        item_sub = spec.get("item_sub", {})
        if value is None:
            return []
        if isinstance(value, dict):
            value = [value]
        rows: list[dict] = []
        for idx, row in enumerate(value if isinstance(value, list) else []):
            if not isinstance(row, dict):
                row = {"person": row}
            item: dict[str, Any] = {}
            for k, ks in item_sub.items():
                if k == "seq" and row.get("seq") in (None, ""):
                    item[k] = idx + 1
                else:
                    item[k] = _scalar_or_unknown(ks, row.get(k))
            for k, v in row.items():
                item.setdefault(k, v)
            rows.append(item)
        return rows
    if shape == SHAPE_LIST:
        if value is None:
            return []
        if not isinstance(value, list):
            return [value]
        return list(value)
    if shape == "enum":
        return check_enum(layer, field, _scalar_or_unknown(shape, value), spec.get("enum"),
                          item_id, unknown_log)
    if shape == "undecided":
        if value in (None, ""):
            return UNKNOWN
        return _scalar_or_unknown(shape, value)
    return _scalar_or_unknown(shape, value)


def _scalar_or_unknown(shape: str, value: Any, required: bool = False) -> Any:
    if isinstance(value, bool):
        return value
    if value is None:
        return UNKNOWN if shape == "undecided" else ""
    if isinstance(value, str):
        text = normalize_text(value)
        if not text and shape == "undecided":
            return UNKNOWN
        return text
    return value


def normalize_record(layer: str, src: dict, item_id: str,
                     unknown_log: list[dict], missing_log: list[dict]) -> dict:
    """把源记录整形成目标 schema（含枚举校验与未考处补 未明）。"""
    out: dict[str, Any] = {"item_id": item_id}
    for field, spec in ENGINE.get(layer, {}).items():
        raw = src.get(field)
        if raw is None:
            # 源数据用了别名？
            for alias, target in FIELD_ALIASES.items():
                if target == field and alias in src:
                    raw = src[alias]
                    break
        if raw is None:
            raw = default_for(field, spec)
            if field in REQUIRE_UNDECIDED.get(layer, ()) or spec.get("shape") == "undecided":
                raw = UNKNOWN
            else:
                missing_log.append({"layer": layer, "item_id": item_id, "field": field})
        out[field] = _norm_value(layer, field, raw, spec, item_id, unknown_log)
    _apply_fallbacks(layer, out)
    # 保留源数据里的额外字段（不丢信息，但不参与 ID 计算）
    for k, v in src.items():
        if k not in out and k not in FIELD_ALIASES and not k.startswith("_"):
            out[k] = v
    return out


def _apply_fallbacks(layer: str, record: dict) -> None:
    """层内口径兜底（schema 要求但源数据可省）。"""
    if layer == "trl" and not str(record.get("note") or "").strip():
        record["note"] = TRL_NOTE


# --------------------------------------------------------------------------
# 主流程
# --------------------------------------------------------------------------


def entity_index_from_file(path) -> dict[str, Any]:
    obj = read_json(path, default=None)
    if not obj:
        return {}
    index = obj.get("index") if isinstance(obj, dict) and "index" in obj else obj
    return index if isinstance(index, dict) else {}


def load_entity_index() -> dict[str, Any]:
    from _kg_pack_base import LAYER_JSON_DIR
    for name in ("ent_index.json", "ent_alias_index.json"):
        data = entity_index_from_file(LAYER_JSON_DIR / name)
        if data:
            return data
    return {}


def resolve_refs(layer: str, record: dict, ent_index: dict[str, Any],
                 miss_log: list[dict]) -> None:
    """按 ENGINE 的 refs 声明回填所有 *_ent_ids 叶子字段。"""
    for field, spec in ENGINE.get(layer, {}).items():
        if not spec.get("refs"):
            continue
        if spec.get("shape") == SHAPE_DICT:
            fill_refs(layer, record, field, spec, ent_index, miss_log)
        elif spec.get("shape") == SHAPE_LIST:
            if record.get(field):
                continue
            texts = _member_texts(layer, field, record)
            if texts:
                ids, miss = resolve_entity_ids(texts, spec["refs"], ent_index)
                record[field] = ids
                if miss:
                    miss_log.append({"layer": layer, "item_id": record["item_id"],
                                     "field": field, "text": " / ".join(texts),
                                     "miss": miss})


def _leaf_id_key(spec: dict) -> str:
    for k in spec.get("sub", {}):
        if k.endswith("_ent_ids") or k == "ent_ids":
            return k
    return "ent_ids"


def _member_texts(layer: str, field: str, record: dict) -> list[str]:
    if layer == "nam" and field == "ent_ids":
        return [str(e.get("person", "")) for e in record.get("entries", []) if e.get("person")]
    return []


def pack_volume(layer: str, volume: str, src_records: list[dict], registry: dict,
                ent_index: dict[str, Any], alloc: IdAllocator,
                logs: dict[str, list]) -> list[dict]:
    cfg = LAYERS[layer]
    prepared: list[dict] = []
    for src in src_records:
        item_id = str(src.get("item_id") or "").strip()
        if not item_id:
            # 允许只写条号 seq，由卷号拼装
            seq = src.get("seq") or src.get("条") or src.get("no")
            if seq:
                item_id = f"{volume}-{int(seq):03d}"
        if not item_id or item_id not in registry:
            logs["bad_item"].append({"layer": layer, "volume": volume, "item_id": item_id,
                                     "src_index": len(prepared)})
            continue
        rec = normalize_record(layer, src, item_id, logs["unknown_enum"], logs["missing"])
        rec["volume"] = volume
        prepared.append(rec)
    prepared.sort(key=lambda r: layer_sort_key(r, cfg))
    for rec in prepared:
        inject_original(rec, registry)
        resolve_refs(layer, rec, ent_index, logs["unresolved_ref"])
        rec[cfg["id_field"]] = alloc.next()
    return prepared


def run_layer(layer: str, args, volumes: list[str], *, ent_index: dict[str, Any] | None = None,
              rebuild_index: Callable[[], dict[str, Any]] | None = None,
              sources: dict[str, list[dict]] | None = None) -> dict:
    """跑一层：写每卷 JSON + 维护该层汇总。返回 stats。"""
    ensure_dirs()
    cfg = LAYERS[layer]
    registry = load_registry()
    if ent_index is None:
        if rebuild_index is not None:
            ent_index = rebuild_index()
        else:
            from _kg_pack_base import resolve_entity_index
            ent_index = resolve_entity_index(args)
    if ent_index is None:
        ent_index = load_entity_index()

    if sources is None:
        sources = load_sources(layer, volumes)
    logs: dict[str, list] = {"unknown_enum": [], "missing": [], "bad_item": [],
                             "unresolved_ref": []}
    alloc = IdAllocator(cfg["id_prefix"])
    per_volume: dict[str, list[dict]] = {}
    for vol in volumes:
        per_volume[vol] = pack_volume(layer, vol, sources.get(vol, []), registry,
                                      ent_index, alloc, logs)
    if not args.check:
        write_volume_products(layer, cfg, volumes, per_volume)
        _write_layer_summary(layer, cfg, volumes, per_volume)
        _write_layer_logs(layer, volumes, logs)
    total = sum(len(v) for v in per_volume.values())
    return {
        "layer": layer,
        "id_prefix": cfg["id_prefix"],
        "volumes": len(volumes),
        "records": total,
        "sources_found": sum(1 for v in volumes if sources.get(v)),
        "id_range": _id_range(alloc, cfg["id_prefix"], total),
        "unknown_enum": len(logs["unknown_enum"]),
        "missing_fields": len(logs["missing"]),
        "bad_item": len(logs["bad_item"]),
        "unresolved_ref": len(logs["unresolved_ref"]),
        "checked_only": bool(args.check),
    }


def _id_range(alloc: IdAllocator, prefix: str, total: int) -> str:
    if total <= 0:
        return "-"
    return f"{prefix}001~{prefix}{total:03d}"


def _write_layer_summary(layer: str, cfg: dict, volumes: list[str],
                         per_volume: dict[str, list[dict]]) -> None:
    """共享汇总文件：只替换本次请求卷的切片（增量合并）。"""
    path = BUILD_DIR / f"{layer}_{SUMMARY_NAME}"
    existing = read_json(path, default=None) or {}
    merged = dict(existing)
    merged.update({
        "layer": layer,
        "id_prefix": cfg["id_prefix"],
        "builder": BUILD_VERSION,
        "generated_at": now_stamp(),
    })
    tree = dict(existing.get("volumes") or {})
    for vol in volumes:
        records = per_volume.get(vol, [])
        tree[vol] = {"volume": vol, "name": VOLUME_NAME.get(vol, ""),
                     "count": len(records),
                     "ids": [r.get(cfg["id_field"]) for r in records]}
    merged["volumes"] = tree
    merged["total"] = sum(int(v.get("count", 0)) for v in tree.values())
    write_json(path, merged)


def _write_layer_logs(layer: str, volumes: list[str], logs: dict[str, list]) -> None:
    path = BUILD_DIR / f"_{layer}_logs.json"
    existing = read_json(path, default=None) or {}
    merged = {"layer": layer, "generated_at": now_stamp(), "volumes": volumes}
    for key, rows in logs.items():
        merged[key] = rows
        merged[f"{key}_total"] = len(rows)
    merged["previous"] = {k: existing.get(f"{k}_total", 0) for k in logs}
    write_json(path, merged)


def load_layer_records(layer: str, volumes: list[str] | None = None) -> list[dict]:
    cfg = LAYERS[layer]
    return collect_layer_records(layer, cfg, volumes or ALL_VOLUMES)


def describe(layer: str) -> dict:
    """输出该层的字段契约（供 README / 校验报告复用）。"""
    out = {}
    for field, spec in ENGINE.get(layer, {}).items():
        item = {"shape": spec.get("shape")}
        if spec.get("enum"):
            item["enum"] = spec["enum"]
        if spec.get("refs"):
            item["refs"] = spec["refs"]
        if spec.get("sub"):
            item["sub"] = spec["sub"]
        if spec.get("item_sub"):
            item["item_sub"] = spec["item_sub"]
        if spec.get("note"):
            item["note"] = spec["note"]
        out[field] = item
    return out
