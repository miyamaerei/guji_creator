"""《五杂俎》知识工程 | 跨层整合验证器

校验 _kg_join 产物的自洽性（只读）：
  1. 条覆盖：_item_registry.json 的每一条是否都在 join 里出现，无重复行
  2. 层计数：每行 layer_count 是否等于非空层数组个数
  3. 引用完整：行内各层 ID 是否真的存在于对应层产物（防悬挂）
  4. 翻译覆盖：trl 覆盖率（翻译层口径：条目数 = 翻译数）
  5. 分布：一条命中 N 层的分布 + 分卷覆盖率

产物：_validate/kg_join_validation.json + _validate/kg_join_validation_summary.md
退出码：0 = 通过；1 = 存在 error
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_pack_base import (  # noqa: E402
    ALL_VOLUMES,
    BUILD_DIR,
    JOIN_LAYER_KEYS,
    LAYERS,
    LAYER_JSON_DIR,
    REGISTRY_PATH,
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

JOIN_JSON = LAYER_JSON_DIR / "_kg_join.json"


def collect_layer_ids(vols: list[str]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    for layer, cfg in LAYERS.items():
        ids: set[str] = set()
        for vol in vols:
            obj = read_json(LAYER_JSON_DIR / f"{layer}_{vol}.json", default=None)
            if not obj:
                continue
            for rec in obj.get("records", []) if isinstance(obj, dict) else obj:
                rid = str(rec.get(cfg["id_field"], ""))
                if rid:
                    ids.add(rid)
        out[layer] = ids
    return out


def run_validation(vols: list[str]) -> dict:
    registry = read_json(REGISTRY_PATH, default=None) or {}
    join = read_json(JOIN_JSON, default=None) or {}
    rows = join.get("rows", []) if isinstance(join, dict) else list(join)

    layer_ids = collect_layer_ids(vols)
    issues: list[dict] = []

    def add(level: str, code: str, item_id: str, message: str, value: str = "") -> None:
        issues.append({"level": level, "code": code, "item_id": item_id,
                       "message": message, "value": str(value)[:120]})

    expected_items = [i for i in registry if i.split("-")[0] in vols]
    seen: set[str] = set()
    for row in rows:
        item_id = str(row.get("item_id", ""))
        if item_id in seen:
            add("error", "join_duplicate", item_id, "同一条目在 join 中出现多次")
        seen.add(item_id)
        if item_id not in registry:
            add("error", "join_unknown_item", item_id, "join 条目不在指纹库内")
        expect = 0
        for layer, key in JOIN_LAYER_KEYS.items():
            ids = row.get(key) or []
            if ids:
                expect += 1
            for rid in ids:
                if rid not in layer_ids.get(layer, set()):
                    add("error", "join_dangling", item_id,
                        f"{key} 中的 ID 不在 {layer} 层产物里", rid)
        if "ents" in row:
            if row.get("ents"):
                expect += 1
            for ent_id in row.get("ents") or []:
                if ent_id not in layer_ids.get("ent", set()):
                    add("error", "join_dangling_ent", item_id, "ents 中的 ID 不在实体表里", ent_id)
        if int(row.get("layer_count", -1)) != expect:
            add("error", "layer_count_mismatch", item_id,
                f"layer_count={row.get('layer_count')}，实际非空层数={expect}")

    missing = [i for i in expected_items if i not in seen]
    for item_id in missing[:200]:
        add("warn", "join_missing_item", item_id, "指纹库有条目但 join 无行")

    layer_hits = {key: 0 for key in JOIN_LAYER_KEYS}
    layer_hits["ents"] = 0
    for row in rows:
        for key in layer_hits:
            layer_hits[key] += len(row.get(key) or [])
    trl_items = sum(1 for row in rows if row.get("trls"))
    coverage = (len(seen & set(expected_items)) / len(expected_items)) if expected_items else 0.0

    stats = {
        "generated_at": now_stamp(),
        "volumes": vols,
        "expected_items": len(expected_items),
        "join_rows": len(rows),
        "join_missing": len(missing),
        "coverage_ratio": round(coverage, 4),
        "layer_hits": layer_hits,
        "trl_coverage": round(trl_items / len(rows), 4) if rows else 0.0,
        "errors": sum(1 for i in issues if i["level"] == "error"),
        "warnings": sum(1 for i in issues if i["level"] == "warn"),
        "issues": issues[:500],
        "issues_total": len(issues),
    }
    return stats


def main() -> None:
    args, vols = build_context("跨层整合验证器 validate_kg_join")
    banner("跨层整合验证 validate_kg_join")
    ensure_dirs()
    stats = run_validation(vols)
    if not args.check:
        write_json(VALIDATE_DIR / "kg_join_validation.json", stats)
        write_text(VALIDATE_DIR / "kg_join_validation_summary.md", _markdown(stats))
    report_stats("贯通验证结果", {
        "应有条目": stats["expected_items"],
        "join 行数": stats["join_rows"],
        "缺失条目": stats["join_missing"],
        "条覆盖": f"{stats['coverage_ratio'] * 100:.2f}%",
        "翻译覆盖": f"{stats['trl_coverage'] * 100:.2f}%",
        "错误": stats["errors"],
        "警告": stats["warnings"],
    })
    if stats["errors"]:
        raise SystemExit(1)


def _markdown(stats: dict) -> str:
    lines = [
        "# 《五杂俎》知识工程 跨层整合验证报告",
        "",
        f"- 生成时间：{stats['generated_at']}",
        f"- 覆盖卷：{', '.join(stats['volumes'])}",
        f"- 应有条目：{stats['expected_items']}　join 行数：{stats['join_rows']}",
        f"- 缺失条目：{stats['join_missing']}　条覆盖：{stats['coverage_ratio'] * 100:.2f}%",
        f"- 翻译覆盖：{stats['trl_coverage'] * 100:.2f}%",
        f"- 错误：{stats['errors']}　警告：{stats['warnings']}",
        "",
        "## 各层命中数",
        "",
        "| 层键 | 命中记录 |",
        "| --- | ---: |",
    ]
    for key, hits in stats["layer_hits"].items():
        lines.append(f"| {key} | {hits} |")
    if stats["issues"]:
        lines += ["", "## 问题明细（前 500 条）", "",
                  "| level | code | item_id | message | value |",
                  "| --- | --- | --- | --- | --- |"]
        for issue in stats["issues"]:
            lines.append(f"| {issue['level']} | {issue['code']} | {issue['item_id']} | "
                         f"{issue['message']} | {issue['value']} |")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    main_guard(main)
