# -*- coding: utf-8 -*-
"""《客座赘语》知识工程 | 源数据 schema 自检 check_src_schema

在写源数据后、build 之前，对 _src/_<layer>_ai_<NN>.py 的 RECORDS 做静态断言：
  1. 每条记录必须是 dict，且含 item_id；
  2. item_id 格式 NN-NNN、卷号与文件卷号一致、且已登记在 _item_registry.json；
  3. 该层 must_fields（排除打包器注入字段 start/end/original/norm/volume）必须存在且非空；
  4. 源数据不得自带注入字段（start/end/original/norm/volume 由打包器回填）；
  5. 出现未知语义键（不在 must_fields / 兼容键范围内）时告警提示。

用法：python check_src_schema.py [--volumes 05]
退出码：0 = 全通过；1 = 存在缺失/格式错误（可带 --warn-as-error 把告警也计入失败）。
输出：终端汇总 + _validate/check_src_report_<NN>.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_pack_base import (  # noqa: E402
    LAYERS,
    REGISTRY_PATH,
    SRC_DIR,
    VALIDATE_DIR,
    load_registry,
    load_source,
    now_stamp,
    read_json,
    write_json,
)

# 打包器负责注入、源数据必须省写的字段（与 build_layers.INJECTED_FIELDS 对齐）
INJECTED_FIELDS = {"start", "end", "original", "norm", "volume"}
# 各层源数据允许出现的非 must 键（evidence 全书通用；nam 的 names/entries 由打包器展开；
# opn/rel/appt 等语义键在各层 must 之外的部分在此登记为兼容键，避免误报未知键）
COMPAT_KEYS = {
    "evidence",
    "source",
    "confidence",
    "note",
    "names",  # nam：pack 展开为 entries
    "entries",  # nam：已展开形态
    "region",  # cus：地域
    "description",  # nam：别名说明
    "where",  # ming：名物出处
    "who",  # ming/opn：指涉人物
    "location",  # geo：地名坐标
    "history",  # geo：沿革
    # opn 层扩展键
    "detail",  # opn：观点表述
    "first_person",  # opn：言说主体
    "stance",  # opn：态度（如必须字段未含则此处豁免）
    "topic",  # opn：议题
    # appt 层扩展键
    "status",  # appt：任职状态
    "institution",  # appt：任职机构
    "when",  # appt：时间
    # obj 层扩展键
    "attributes",  # obj
    "lore",  # obj
    # cit 层扩展键
    "purpose",  # cit
    # ent 层：normalized 为规范主名双字段口径的正式字段（非打包器注入）
    "normalized",
    "alias",
    "surfaces",
}
ITEM_ID_RE = re.compile(r"^(\d{2})-(\d{3})$")

# 各层"合理出现"的键全集 = must_fields + COMPAT_KEYS（item_id 为必须键）
# 其中 volume/original/norm/start/end 由打包器注入，源数据禁止携带
FORBIDDEN_IN_SRC = INJECTED_FIELDS - {"item_id"}


def _collect_issues(volume: str | None) -> tuple[list[dict], dict[str, dict]]:
    issues: list[dict] = []
    stats: dict[str, dict] = {}
    registry = load_registry()

    files = sorted(SRC_DIR.glob("_*_ai_*.py"))
    if volume:
        files = [p for p in files if p.name.endswith(f"_{volume}.py")]
    if not files:
        issues.append(
            {
                "file": "*",
                "item_id": "",
                "field": "file",
                "note": f"未找到卷 {volume} 源数据文件",
            }
        )

    for path in files:
        m = re.match(r"^_(\w+)_ai_(\d{2})\.py$", path.name)
        if not m:
            issues.append(
                {
                    "file": path.name,
                    "item_id": "",
                    "field": "file",
                    "note": "文件名不符合 _<layer>_ai_<NN>.py",
                }
            )
            continue
        layer, vol = m.group(1), m.group(2)
        if layer not in LAYERS:
            issues.append(
                {
                    "file": path.name,
                    "item_id": "",
                    "field": "file",
                    "note": f"未知层名 {layer}",
                }
            )
            continue
        cfg = LAYERS[layer]
        must = [f for f in cfg["must_fields"] if f not in INJECTED_FIELDS]
        allowed = set(must) | COMPAT_KEYS

        try:
            records = load_source(layer, vol)
        except Exception as exc:  # noqa: BLE001
            issues.append(
                {
                    "file": path.name,
                    "item_id": "",
                    "field": "file",
                    "note": f"源数据加载失败：{exc}",
                }
            )
            continue

        n = len(records)
        stats.setdefault(layer, {"volume": vol, "records": 0, "issues": 0})
        stats[layer]["records"] += n
        for i, rec in enumerate(records, 1):
            seq_no = f"#{i}"
            if not isinstance(rec, dict):
                issues.append(
                    {
                        "file": path.name,
                        "item_id": seq_no,
                        "field": "",
                        "note": "记录非 dict",
                    }
                )
                stats[layer]["issues"] += 1
                continue
            item_id = str(rec.get("item_id", ""))
            # 1) item_id 格式 + 卷号一致
            mm = ITEM_ID_RE.match(item_id)
            if not mm:
                issues.append(
                    {
                        "file": path.name,
                        "item_id": item_id or seq_no,
                        "field": "item_id",
                        "note": "格式应为 NN-NNN",
                    }
                )
                stats[layer]["issues"] += 1
                continue
            if mm.group(1) != vol:
                issues.append(
                    {
                        "file": path.name,
                        "item_id": item_id,
                        "field": "item_id",
                        "note": f"卷号 {mm.group(1)} 与文件名 {vol} 不一致",
                    }
                )
                stats[layer]["issues"] += 1
            if item_id not in registry:
                issues.append(
                    {
                        "file": path.name,
                        "item_id": item_id,
                        "field": "item_id",
                        "note": "registry 无此条目",
                    }
                )
                stats[layer]["issues"] += 1
            # 2) 禁止自带注入字段
            for f in sorted(FORBIDDEN_IN_SRC - {"item_id"}):
                if f in rec:
                    issues.append(
                        {
                            "file": path.name,
                            "item_id": item_id,
                            "field": f,
                            "note": "注入字段不应出现在源数据",
                        }
                    )
                    stats[layer]["issues"] += 1
            # 3) must_fields 必须存在且非空
            for f in must:
                v = rec.get(f)
                if v is None or v == "" or v == [] or v == {}:
                    issues.append(
                        {
                            "file": path.name,
                            "item_id": item_id,
                            "field": f,
                            "note": "必须字段缺失或为空",
                        }
                    )
                    stats[layer]["issues"] += 1
            # 4) 未知键告警（仅提示，不计入缺失）
            for key in rec:
                if key not in allowed and key not in INJECTED_FIELDS:
                    issues.append(
                        {
                            "file": path.name,
                            "item_id": item_id,
                            "field": key,
                            "note": "未知语义键（如确需请加入 COMPAT_KEYS）",
                            "level": "warn",
                        }
                    )

    return issues, stats


def main() -> None:
    ap = __import__("argparse").ArgumentParser(
        description="源数据 schema 自检（写数据后、build 前）"
    )
    ap.add_argument(
        "--volumes", default=None, help="只检查指定卷，如 05（缺省=全部已存在源文件）"
    )
    ap.add_argument(
        "--warn-as-error", action="store_true", help="把 warn 级问题计入退出码"
    )
    args = ap.parse_args()
    volume = args.volumes

    issues, stats = _collect_issues(volume)
    errors = [x for x in issues if x.get("level") != "warn"]
    warns = [x for x in issues if x.get("level") == "warn"]
    fail = bool(errors) or (args.warn_as_error and bool(warns))

    print("=" * 68)
    print(f"《客座赘语》知识工程 | 源数据 schema 自检（卷 {volume or '全部'}）")
    print("=" * 68)
    for layer, s in stats.items():
        print(f"  {layer:<5} {s['records']:>4} 条 | 问题 {s['issues']}")
    print(f"  缺失/格式错误 {len(errors)} 处 | 未知键告警 {len(warns)} 处")
    if warns:
        seen = set()
        for w in warns:
            key = (w["file"], w["field"])
            if key not in seen:
                seen.add(key)
                print(f"  [告警] {w['file']} 字段 {w['field']}: {w['note']}")
    print(
        f"[结论] {'PASS' if not fail else 'FAIL'} | 错误 {len(errors)} | 告警 {len(warns)}"
    )

    report = {
        "volumes": volume,
        "checked_at": now_stamp(),
        "stats": stats,
        "issues": issues,
        "conclusion": "PASS" if not fail else "FAIL",
        "error_count": len(errors),
        "warn_count": len(warns),
    }
    if volume:
        out = VALIDATE_DIR / f"check_src_report_{volume}.json"
    else:
        out = VALIDATE_DIR / "check_src_report_all.json"
    write_json(out, report)
    print(f"[产物] {out}")
    raise SystemExit(1 if fail else 0)


if __name__ == "__main__":
    main()
