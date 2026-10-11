"""《五杂俎》知识工程 | 分层验证器

对 11 层产物做体检（只读，不改数据）：
  1. 结构：必填字段齐、形状对（dict/list/dictlist）、顶层 records 键规范
  2. 主键：ID 唯一、前缀正确、条号 item_id 在指纹库内
  3. 口径：枚举值合法（未知值收集入 _build/_enums_pending.json）、未考处必须显式 "未明"
  4. 溯源：original/norm 与 _item_registry.json 完全一致（不允许手抄漂移）
  5. 引用：*_ent_ids 指向的 ENT 主键必须存在于实体表

产物：_validate/layer_validation.json + _validate/layer_validation_summary.md
退出码：0 = 通过（含仅警告）；1 = 存在 error
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _kg_enums as E  # noqa: E402
from _kg_entity import INDEX_PATH, load_entity_index  # noqa: E402
from _kg_layers import ENGINE, SHAPE_DICT, SHAPE_DICT_LIST, SHAPE_LIST  # noqa: E402
from _kg_pack_base import (  # noqa: E402
    ALL_VOLUMES,
    BUILD_DIR,
    LAYERS,
    LAYER_JSON_DIR,
    REGISTRY_PATH,
    UNKNOWN,
    VALIDATE_DIR,
    VOLUME_NAME,
    banner,
    build_context,
    ensure_dirs,
    main_guard,
    now_stamp,
    read_json,
    report_stats,
    write_json,
    write_text,
)

# 未考处必须显式写的层字段
UNDECIDED_FIELDS = {
    "event": ("when", "where"),
    "ming": ("when", "where"),
    "appt": ("when",),
}
# 嵌套节点里必须显式 未明 的叶子
UNDECIDED_LEAVES = {
    "event.who.text",
    "rel.person_a.text",
    "rel.person_b.text",
    "cit.cited_work.text",
    "obj.name.text",
    "cus.region.text",
    "ming.who.text",
    "appt.person.text",
    "appt.office.text",
    "appt.institution.text",
}


def check_record(layer: str, cfg: dict, rec: dict, entities: set[str],
                 registry: dict) -> list[dict]:
    issues: list[dict] = []
    item_id = str(rec.get("item_id", ""))

    def add(level: str, code: str, field: str, message: str, value=None) -> None:
        issues.append({"level": level, "layer": layer, "item_id": item_id,
                       "field": field, "code": code, "message": message,
                       "value": "" if value is None else str(value)[:120]})

    # 1) 主键
    rid = str(rec.get(cfg["id_field"], ""))
    if not rid:
        add("error", "id_missing", cfg["id_field"], "缺少业务主键")
    elif not rid.startswith(cfg["id_prefix"]):
        add("error", "id_prefix", cfg["id_field"], f"主键前缀应为 {cfg['id_prefix']}", rid)
    if not item_id or item_id not in registry:
        add("error", "item_unknown", "item_id", "item_id 不在 _item_registry.json 内", item_id)
    if str(rec.get("volume", "")) and rec["volume"] not in VOLUME_NAME:
        add("error", "volume_unknown", "volume", "卷号非法", rec["volume"])

    # 2) 必填 / 未考处
    for field in cfg.get("must_fields", ()):
        value = rec.get(field)
        empty = value is None or (isinstance(value, str) and not value.strip()) or \
            (isinstance(value, (list, dict)) and len(value) == 0)
        if empty:
            add("error", "must_missing", field, "必填字段为空")
    for field in UNDECIDED_FIELDS.get(layer, ()):
        value = rec.get(field)
        text = str(value if value is not None else "").strip()
        # 口径：未考处必须**显式**写「未明」，而不是留空。
        # 填了实际考订值（"京师"/"宋仁宗嘉祐年间"）是正确的，不该报警；
        # 只有「空串/ 空 list / 缺失 / None」才是"没显式声明"。
        if text in ("", "None", "[]", "{}"):
            add("warn", "undecided_undeclared", field,
                f"未考处应显式写 {UNKNOWN}（当前为空）", value)
        elif isinstance(value, list) and UNKNOWN in [str(x) for x in value]:
            add("warn", "undecided_partial", field,
                f"部分未考，应逐项显式写 {UNKNOWN}", value)

    # 3) 形状
    for field, spec in ENGINE.get(layer, {}).items():
        value = rec.get(field)
        shape = spec.get("shape")
        if shape == SHAPE_DICT and not isinstance(value, dict):
            add("error", "shape_dict", field, "应为嵌套对象 {text, *_ent_ids}", type(value).__name__)
        elif shape == SHAPE_DICT_LIST and not isinstance(value, list):
            add("error", "shape_dictlist", field, "应为对象数组", type(value).__name__)
        elif shape == SHAPE_LIST and not isinstance(value, list):
            add("error", "shape_list", field, "应为数组", type(value).__name__)

    # 4) 枚举
    for field, enum_name in _enum_map(layer).items():
        raw = str(rec.get(field, "") or "")
        if raw in ("", UNKNOWN):
            continue
        fixed, bad = E.validate(enum_name, raw, where=f"{layer}.{field}@{item_id}")
        if bad is not None:
            add("error", "enum_unknown", field, f"枚举 {enum_name} 无此值", bad)
        elif fixed != raw:
            add("warn", "enum_alias", field, f"别名已归一为 {fixed}", raw)

    # 5) 溯源（original/norm 必须来自指纹库）
    if "original" in rec and item_id in registry:
        if rec.get("original") != registry[item_id]["original"]:
            add("error", "original_drift", "original", "原文与指纹库不一致（禁止手抄漂移）")
        if rec.get("norm") != registry[item_id]["norm"]:
            add("error", "norm_drift", "norm", "norm 与指纹库不一致")

    # 6) 引用
    for field, spec in ENGINE.get(layer, {}).items():
        if not spec.get("refs"):
            continue
        for path, ids in _iter_ref_ids(rec, field, spec):
            for ent_id in ids:
                if ent_id not in entities:
                    add("error", "ref_dangling", path, "引用实体不存在于实体表", ent_id)
    for field in ("evidence_refs", "ref_events"):
        for ref in rec.get(field) or []:
            _check_ref_shape(add, field, str(ref), registry)

    # 7) 嵌套叶子的未考处
    for path in UNDECIDED_LEAVES:
        top, _, leaf = path.partition(".")
        if top != layer:
            continue
        node = rec.get(leaf.split(".")[0]) if "." in leaf else rec.get(leaf)
        if isinstance(node, dict):
            text = str(node.get("text", ""))
            if text == "":
                add("warn", "undecided_empty", leaf, f"未考处应显式写 {UNKNOWN}，不允许留空")
    return issues


def _enum_map(layer: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for field, spec in ENGINE.get(layer, {}).items():
        if spec.get("enum"):
            out[field] = spec["enum"]
    if layer == "trl":
        out.setdefault("style", "trl_style")
    return out


def _iter_ref_ids(rec: dict, field: str, spec: dict):
    value = rec.get(field)
    if spec.get("shape") == SHAPE_DICT and isinstance(value, dict):
        for k, v in value.items():
            if k.endswith("_ent_ids") or k == "ent_ids":
                yield f"{field}.{k}", [str(x) for x in (v or [])]
    elif spec.get("shape") == SHAPE_LIST and isinstance(value, list):
        yield field, [str(x) for x in value]


def _check_ref_shape(add, field: str, ref: str, registry: dict) -> None:
    if not ref:
        return
    if ref.startswith(("WZZ-E-", "ENT-", "REL-", "NAM-", "CIT-", "OBJ-", "CUS-",
                       "OPN-", "MING-", "APPT-", "TRL-")):
        return
    if ref not in registry:
        add("warn", "ref_softmiss", field, "引用条号不存在于指纹库", ref)


def run_validation(vols: list[str]) -> dict:
    registry = read_json(REGISTRY_PATH, default=None) or {}
    ent_index = load_entity_index()
    entities = set()
    ent_obj = read_json(INDEX_PATH, default=None)
    if ent_obj:
        entities = {meta.get("id", "") for meta in ent_obj.get("index", {}).values()
                    if isinstance(meta, dict)}
        entities.discard("")

    per_layer: dict[str, dict] = {}
    all_issues: list[dict] = []
    for layer, cfg in LAYERS.items():
        issues: list[dict] = []
        seen_ids: dict[str, str] = {}
        total = 0
        id_fields = cfg["id_field"]
        for vol in vols:
            obj = read_json(LAYER_JSON_DIR / f"{layer}_{vol}.json", default=None)
            if not obj:
                continue
            records = obj.get("records", []) if isinstance(obj, dict) else list(obj)
            if isinstance(obj, dict) and "records" not in obj:
                issues.append({"level": "error", "layer": layer, "item_id": "",
                               "field": "records", "code": "records_key",
                               "message": "单卷 JSON 顶层缺少 records 键", "value": vol})
            for rec in records:
                total += 1
                rid = str(rec.get(id_fields, ""))
                if rid in seen_ids:
                    issues.append({"level": "error", "layer": layer,
                                   "item_id": str(rec.get("item_id", "")),
                                   "field": id_fields, "code": "id_duplicate",
                                   "message": f"主键重复（另见 {seen_ids[rid]}）", "value": rid})
                seen_ids[rid] = f"{layer}_{vol}"
                issues.extend(check_record(layer, cfg, rec, entities, registry))
        counts: dict[str, int] = {}
        for issue in issues:
            counts[issue["level"]] = counts.get(issue["level"], 0) + 1
        per_layer[layer] = {
            "layer": layer, "id_prefix": cfg["id_prefix"], "records": total,
            "unique_ids": len(seen_ids),
            "errors": counts.get("error", 0), "warnings": counts.get("warn", 0),
            "issues": issues[:200], "issues_total": len(issues),
        }
        all_issues.extend(issues)

    stats = {
        "generated_at": now_stamp(),
        "volumes": vols,
        "layers": per_layer,
        "totals": {
            "records": sum(v["records"] for v in per_layer.values()),
            "errors": sum(v["errors"] for v in per_layer.values()),
            "warnings": sum(v["warnings"] for v in per_layer.values()),
        },
    }
    return stats


def main() -> None:
    args, vols = build_context("分层验证器 validate_layers")
    banner("分层验证 validate_layers")
    ensure_dirs()
    stats = run_validation(vols)

    if not args.check:
        write_json(VALIDATE_DIR / "layer_validation.json", stats)
        write_text(VALIDATE_DIR / "layer_validation_summary.md", _markdown(stats))
        E.flush_pending()

    report_stats("分层验证结果", {
        "记录总数": stats["totals"]["records"],
        "错误": stats["totals"]["errors"],
        "警告": stats["totals"]["warnings"],
        **{f"{k}": f"{v['records']} 条 / error {v['errors']} / warn {v['warnings']}"
           for k, v in stats["layers"].items()},
    })
    if stats["totals"]["errors"]:
        raise SystemExit(1)


def _markdown(stats: dict) -> str:
    lines = [
        "# 《五杂俎》知识工程 分层验证报告",
        "",
        f"- 生成时间：{stats['generated_at']}",
        f"- 覆盖卷：{', '.join(stats['volumes'])}",
        f"- 记录总数：{stats['totals']['records']}",
        f"- 错误：{stats['totals']['errors']}　警告：{stats['totals']['warnings']}",
        "",
        "## 分层概览",
        "",
        "| 层 | ID 前缀 | 记录 | 唯一主键 | error | warn |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for layer, row in stats["layers"].items():
        lines.append(f"| {layer} | {row['id_prefix']} | {row['records']} | "
                     f"{row['unique_ids']} | {row['errors']} | {row['warnings']} |")
    lines.append("")
    lines.append("## 问题明细（每层最多 200 条）")
    for layer, row in stats["layers"].items():
        if not row["issues"]:
            lines.append(f"\n### {layer}：无问题")
            continue
        lines.append(f"\n### {layer}（共 {row['issues_total']} 条，下列前 {len(row['issues'])}）")
        lines.append("")
        lines.append("| level | code | item_id | field | message | value |")
        lines.append("| --- | --- | --- | --- | --- | --- |")
        for issue in row["issues"]:
            lines.append(f"| {issue['level']} | {issue['code']} | {issue['item_id']} | "
                         f"{issue['field']} | {issue['message']} | {issue['value']} |")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main_guard(main)
