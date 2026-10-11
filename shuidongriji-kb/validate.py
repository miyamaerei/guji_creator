# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— 全量验证器（validate）
==============================================
验证维度（skill §10 管线与验证）：
  A. 底座完整性：39 卷文件、条目文件、指纹库键数
  B. 源数据覆盖：每卷 8 层 sources/_<layer>_ai_NN.py 是否齐备
  C. 打包器产物：每卷每层 data/<layer>/<layer>_NN.json（源数据存在则必须有产物）
  D. 格式校验：ID 唯一性、item_id 合法且存在于指纹库、必填字段、枚举合法
  E. 引用校验：各层 ent_ids 引用必须存在于 ent_keys 主键表
  F. TRL 覆盖：每卷条目数 = 翻译数
  G. 枚举口径：快照输出（registerVersion 比对基准）

结果写文件：reports/验证缺漏清单.txt（不依赖 stdout 截断）。
问题数 = 0 为通过标准。
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from _kg_enums import (APPT_STATUS, ENTITY_TYPES, EVENT_TYPES, ID_PREFIXES,
                       LIT_TYPES, NAM_ENTRY_FIELDS, NAM_TYPES, REG_TYPES,
                       REL_DIRECTIONS, REL_TYPES, TRL_STYLES, VOL_MODES,
                       check_enum, check_in_list, enum_snapshot)

LAYERS = ["ent", "appt", "event", "reg", "lit", "rel", "nam", "trl"]
EXPECTED_VOLUMES = [f"{i:02d}" for i in range(0, 39)]  # 00 + 01..38
EXPECTED_ITEMS = 1197  # 底座实测条目数（build_base 输出，2026-10-10）


def check_entity_types(rec, issues, item_id, ctx):
    try:
        check_enum(rec.get("type"), ENTITY_TYPES, ctx, 1)
    except ValueError as e:
        issues.append(str(e))


def check_appt(rec, issues, item_id):
    try:
        check_enum(rec.get("status"), APPT_STATUS, "任职状态", 1)
    except ValueError as e:
        issues.append(str(e))


def check_event(rec, issues, item_id):
    try:
        check_enum(rec.get("type"), EVENT_TYPES, "事件类型", 1)
    except ValueError as e:
        issues.append(str(e))


def check_reg(rec, issues, item_id):
    try:
        check_enum(rec.get("type"), REG_TYPES, "制度类型", 1)
    except ValueError as e:
        issues.append(str(e))


def check_lit(rec, issues, item_id):
    try:
        check_enum(rec.get("type"), LIT_TYPES, "文献类型", 1)
    except ValueError as e:
        issues.append(str(e))


def check_rel(rec, issues, item_id):
    try:
        check_enum(rec.get("relation_type"), REL_TYPES, "关系类型", 1)
        check_in_list(rec.get("direction"), REL_DIRECTIONS, "关系方向", 1)
    except ValueError as e:
        issues.append(str(e))


def check_nam(rec, issues, item_id):
    try:
        check_enum(rec.get("category"), NAM_TYPES, "名录类型", 1)
    except ValueError as e:
        issues.append(str(e))
    entries = rec.get("entries")
    if isinstance(entries, list):
        for e in entries:
            for k in NAM_ENTRY_FIELDS:
                if k not in e:
                    issues.append(f"{item_id}：NAM entries 缺字段 {k}")
                    break


def check_trl(rec, issues, item_id):
    try:
        check_enum(rec.get("style"), TRL_STYLES, "翻译风格", 1)
    except ValueError as e:
        issues.append(str(e))


def validate(volumes=None, verbose=True):
    os.makedirs(common.REPORTS_DIR, exist_ok=True)
    report = []
    problems = 0
    gaps = 0

    def add(sev, msg):
        nonlocal problems, gaps
        if sev == "ERR":
            problems += 1
        elif sev == "GAP":
            gaps += 1
        report.append(f"[{sev}] {msg}")

    # ---- A. 底座完整性 ----
    add("OK", "== A. 底座完整性 ==")
    vol_files = common.iter_volumes()
    vols_found = [v for v, _ in vol_files]
    for v in EXPECTED_VOLUMES:
        if v not in vols_found:
            add("ERR", f"缺失卷文件 {v}")
    reg = common.load_registry()
    if len(reg) != EXPECTED_ITEMS:
        add("ERR", f"指纹库键数 {len(reg)}，期望 {EXPECTED_ITEMS}")
    else:
        add("OK", f"指纹库 {len(reg)} 条")
    missing_items = [f"{v}-001" for v in EXPECTED_VOLUMES if f"{v}-001" not in reg]
    if missing_items:
        add("ERR", f"指纹库缺卷首条目: {missing_items[:5]}...")

    # ---- B. 源数据覆盖 ----
    add("OK", "== B. 源数据覆盖（AI 判定逐卷填写；缺失=执行缺口 GAP，非结构错误）==")
    for v in EXPECTED_VOLUMES[1:]:  # 卷 00 提要不要求 8 层
        for layer in LAYERS:
            if os.path.exists(os.path.join(common.SOURCES_DIR, f"_{layer}_ai_{v}.py")):
                add("OK", f"{v} {layer} 源数据齐备")
            else:
                add("GAP", f"{v} {layer} 源数据缺失（待执行该卷时用 scaffold_volume.py 生成）")

    # ---- C. 打包器产物 ----
    add("OK", "== C. 打包器产物完整性 ==")
    for v in EXPECTED_VOLUMES[1:]:
        for layer in LAYERS:
            src = os.path.join(common.SOURCES_DIR, f"_{layer}_ai_{v}.py")
            out = os.path.join(common.DATA_DIR, layer, f"{layer}_{v}.json")
            if os.path.exists(src) and not os.path.exists(out):
                add("ERR", f"{v} {layer}：源数据存在但产物缺失")

    # ---- D/E/F. 各层格式、引用、TRL 覆盖 ----
    add("OK", "== D. 格式 / E. 引用 / F. TRL 覆盖 ==")
    ent_keys = common.load_json(os.path.join(common.DATA_DIR, "ent", "ent_keys.json")) or {}
    ent_ids = {e["ent_id"] for e in ent_keys.get("entities", [])}
    layer_checkers = {
        "appt": check_appt, "event": check_event, "reg": check_reg,
        "lit": check_lit, "rel": check_rel, "nam": check_nam, "trl": check_trl,
    }
    seen_ids = {layer: set() for layer in LAYERS}
    trl_items_by_vol = {}
    for v in EXPECTED_VOLUMES[1:]:
        for layer in LAYERS:
            data = common.load_json(os.path.join(common.DATA_DIR, layer, f"{layer}_{v}.json"))
            if not data:
                continue
            for rec in data.get("records", []):
                item_id = rec.get("item_id")
                if not re.match(r"^\d{2}-\d{3}$", str(item_id or "")):
                    add("ERR", f"{v} {layer}：非法 item_id {item_id!r}")
                    continue
                if item_id not in reg:
                    add("ERR", f"{v} {layer} {item_id}：不在指纹库")
                rid = rec.get("id") or rec.get({
                    "appt": "appointment_id", "event": "event_id", "reg": "reg_id",
                    "lit": "lit_id", "rel": "rel_id", "nam": "nam_id", "trl": "trl_id",
                }.get(layer, "id"))
                if not rid:
                    add("ERR", f"{v} {layer} {item_id}：缺主键 ID")
                elif rid in seen_ids[layer]:
                    add("ERR", f"{v} {layer}：ID 重复 {rid}")
                else:
                    seen_ids[layer].add(rid)
                # 枚举校验
                checker = layer_checkers.get(layer)
                if checker:
                    checker(rec, add, item_id)
                # E. 引用校验：各层 *_ent_ids 必须指向存在实体
                for field in ["person_ent_ids", "official_ent_ids", "ent_ids",
                              "who_ent_ids", "author_ent_ids", "person_a_ent_ids",
                              "person_b_ent_ids"]:
                    for eid in rec.get(field) or []:
                        if eid and eid not in ent_ids:
                            add("ERR", f"{v} {layer} {item_id}：引用未注册实体 {eid}")
                if layer == "trl":
                    trl_items_by_vol.setdefault(v, set()).add(item_id)
    # F. TRL 覆盖：条目数 = 翻译数（未翻译=执行缺口 GAP）
    for v in EXPECTED_VOLUMES[1:]:
        vol_items = {i for i in reg if i.startswith(v + "-")}
        translated = trl_items_by_vol.get(v, set())
        if vol_items and translated != vol_items:
            missing = sorted(vol_items - translated)[:5]
            add("GAP", f"{v} TRL 覆盖不齐：缺 {len(vol_items - translated)} 条，如 {missing}（待 AI 逐条翻译）")

    # ---- G. 枚举口径快照 ----
    add("OK", "== G. 枚举口径快照（registerVersion 基准）==")
    snap = enum_snapshot()
    for k, v in sorted(snap.items()):
        add("OK", f"{k}: {len(v)} 项 {list(v)[:6]}{'...' if len(v) > 6 else ''}")
    add("OK", f"ID 前缀: {ID_PREFIXES}")

    # ---- 汇总 ----
    summary = (f"\n===== 验证汇总 ====="
               f"\n结构性问题(ERR) = {problems}"
               f"\n执行缺口(GAP) = {gaps}（待逐卷填充 AI 源数据/翻译，属预期）"
               f"\n通过项(OK) = {sum(1 for l in report if l.startswith('[OK]'))}"
               f"\n{'通过：结构性问题 = 0' if problems == 0 else '未通过：请修复结构性错误后重跑 run_all.py'}")
    report.append(summary)
    report_text = "\n".join(report)
    common.write_text(os.path.join(common.REPORTS_DIR, "验证缺漏清单.txt"), report_text)
    if verbose:
        print(report_text)
    return problems


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="全量验证器")
    ap.add_argument("--volumes", nargs="*", help="仅验证指定卷")
    args = ap.parse_args()
    sys.exit(1 if validate(volumes=args.volumes) else 0)
