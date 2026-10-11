"""《五杂俎》知识工程 | 端到端自检（run_selftest）

不依赖任何真实层数据：在 _src/ 下临时写入一份三条的迷你样本，跑完
   底座 -> 实体层 -> 事件层 -> 关系层 -> 名物层 -> 跨层整合 -> 双层验证
断言以下设施真的工作，然后**逐字节还原 _src/ 与 _layers/ 的原始状态**：

  1. 底座：条目指纹库条目数、norm 注入、原文零漂移
  2. 实体层：ID 前缀 ENT-、词形索引 ent_index.json 可查
  3. 事件层：who 字符串自动升格为 {text, who_ent_ids} 且回填成功
  4. 关系层：枚举别名「主从」自动归一为「上下级」
  5. 各层：ID 前缀正确、层汇总与日志落盘
  6. 跨层：_kg_join 一行贯通，layer_count 与各层数组一致
  7. 验证器：分层验证与贯通验证均 0 error

用法：python run_selftest.py [--keep]      # --keep 保留样本产物供人工检查
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
os.environ.setdefault("PYTHONIOENCODING", "utf-8:replace")

from _kg_pack_base import (  # noqa: E402
    BUILD_DIR,
    LAYERS,
    LAYER_JSON_DIR,
    REGISTRY_PATH,
    SRC_DIR,
    banner,
    ensure_dirs,
    read_json,
    report_stats,
    write_text,
)

# 迷你样本：用卷一前三条，覆盖"实体 - 事件 - 关系 - 名物"四层与跨层引用
DEMO_VOLUME = "01"
SAMPLE_FILES: dict[str, str] = {
    "_ent_ai_01.py": '''"""自检样本：实体层（L1）"""

RECORDS = [
    {"item_id": "01-001", "text": "老子", "type": "person"},
    {"item_id": "01-003", "text": "释氏", "type": "person"},
    {"item_id": "01-004", "text": "朱晦翁", "type": "person"},
    {"item_id": "01-004", "text": "天", "type": "object"},
    {"item_id": "01-005", "text": "天变不足畏", "type": "work"},
    {"item_id": "01-006", "text": "璇玑玉衡", "type": "object"},
    {"item_id": "01-006", "text": "洛下闳", "type": "person"},
    {"item_id": "01-006", "text": "僧一行", "type": "person"},
    {"item_id": "01-007", "text": "汉明帝", "type": "person"},
    {"item_id": "01-007", "text": "张重", "type": "person"},
    {"item_id": "01-007", "text": "日南郡", "type": "place"},
    {"item_id": "01-006", "text": "舜", "type": "person"},
]
''',
    "_event_ai_01.py": '''"""自检样本：事件层（EVT）"""

RECORDS = [
    {"item_id": "01-006", "type": "文事", "who": "舜", "action": "作璇玑玉衡以齐七政",
     "what": "舜践帝位后制作浑仪类仪器以齐七政", "when": "未明", "where": "未明"},
    {"item_id": "01-007", "type": "轶事", "who": "汉明帝", "action": "嘲张重",
     "what": "汉明帝以日南郡人应北向看日相嘲", "when": "未明", "where": "未明"},
]
''',
    "_rel_ai_01.py": '''"""自检样本：关系层（REL）——含枚举别名「主从」测归一"""

RECORDS = [
    {"item_id": "01-006", "person_a": "舜", "person_b": "洛下闳",
     "relation_type": "主从", "direction": "单向",
     "evidence": "舜作璇玑玉衡，后世洛下闳等冥思精数，亦能范围天地"},
]
''',
    "_obj_ai_01.py": '''"""自检样本：名物层（OBJ）"""

RECORDS = [
    {"item_id": "01-006", "name": "璇玑玉衡", "category": "器物",
     "attributes": {"形制": "浑仪倚盖", "用途": "齐七政"},
     "lore": "舜以耕稼陶渔之夫一旦践帝位即作此器"},
]
''',
}

# 额外校验：底座必须切出这些条目
REQUIRED_ITEMS = ["00-001", "00-002", "01-001", "01-125", "16-143"]


def run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def _stage_error_total(script: str) -> int | None:
    """验证类阶段的真实结论看产物（其入口壳子恒返 0）。"""
    if script == "validate_layers.py":
        data = read_json(ROOT / "_validate" / "layer_validation.json", default={}) or {}
        totals = data.get("totals") or {}
        if "errors" in totals:
            return int(totals["errors"])
    if script == "validate_kg_join.py":
        data = read_json(ROOT / "_validate" / "kg_join_validation.json", default={}) or {}
        if "errors" in data:
            return int(data["errors"])
    return None


def _stage_ok(script: str, code: int) -> bool:
    total = _stage_error_total(script)
    return code == 0 and (total is None or total == 0)


def snapshot(paths: list[Path]) -> dict[str, bytes]:
    return {str(p): p.read_bytes() for p in paths if p.exists()}


def restore(snap: dict[str, bytes], paths: list[Path]) -> None:
    for p in paths:
        key = str(p)
        if key in snap:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(snap[key])
        elif p.exists():
            p.unlink()


def all_layer_source_paths() -> list[Path]:
    """_src 下所有分层源数据文件（统一卷源也一并算上）。

    自检必须把它们**全部**临时挪走：只清自己 stub 的那几个会让真实数据
    残留进验证器——那些记录的实体/事件 ID 指向已被样本覆盖的层，
    于是报出一堆"悬空引用"，看起来像自检失败，其实是被测数据污染。
    """
    paths = [p for p in SRC_DIR.glob("_vol_*.py")]
    paths += [p for p in SRC_DIR.glob("_*_ai_*.py")]
    return sorted(paths)


def all_layer_json_paths() -> list[Path]:
    """_layers 下所有每层 JSON（含非样本卷），验证器会一并扫。"""
    return sorted(p for p in LAYER_JSON_DIR.glob("*.json"))


def main() -> None:
    keep = "--keep" in sys.argv
    banner("端到端自检 run_selftest")
    ensure_dirs()

    sample_paths = [SRC_DIR / name for name in SAMPLE_FILES]
    # 隔离面 = 全部源数据 + 全部层产物，跑完逐字节还原
    source_paths = all_layer_source_paths()
    layer_paths = all_layer_json_paths()
    snap = snapshot(source_paths + layer_paths)
    stash_dir = ROOT / "_build" / "_selftest_stash"
    if stash_dir.exists():
        shutil.rmtree(stash_dir)
    stash_dir.mkdir(parents=True, exist_ok=True)

    checks: list[dict] = []
    steps: list[dict] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": name, "ok": bool(ok), "detail": detail})
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" —— {detail}" if detail else ""))

    try:
        # 把真实源数据挪进暂存区（--keep 时也挪，否则样本与真实数据混跑）
        moved = 0
        for p in source_paths:
            shutil.move(str(p), stash_dir / p.name)
            moved += 1
        for p in layer_paths:
            if p.name.startswith("_kg_join"):
                continue
            p.unlink()
        print(f"[隔离] 暂存 {moved} 份源数据、清理 {len(layer_paths)} 份层产物")

        for name, body in SAMPLE_FILES.items():
            (SRC_DIR / name).write_text(body, encoding="utf-8")
        print(f"[样本] 写入 {len(SAMPLE_FILES)} 份 _src/_*_ai_{DEMO_VOLUME}.py")

        stages = [
            ("底座", ["build_base.py"]),
            ("实体层", ["build_ent.py"]),
            ("事件层", ["build_event.py"]),
            ("关系层", ["build_rel.py"]),
            ("名物层", ["build_obj.py"]),
            ("跨层整合", ["build_kg_join.py"]),
            ("分层验证", ["validate_layers.py"]),
            ("贯通验证", ["validate_kg_join.py"]),
        ]
        for label, cmd in stages:
            code, out = run([sys.executable, *cmd])
            ok = _stage_ok(cmd[0], code)
            steps.append({"stage": label, "exit": code, "ok": ok, "tail": out[-2000:]})
            check(f"阶段 {label}（{cmd[0]}）通过", ok,
                  "" if ok else f"exit={code} errors={_stage_error_total(cmd[0])}")
            if not ok:
                print(out[-3000:])
                raise RuntimeError(f"{label} 失败，自检中止")

        # 1) 底座
        registry = read_json(REGISTRY_PATH, default={}) or {}
        missing = [i for i in REQUIRED_ITEMS if i not in registry]
        check("底座指纹库含关键条目", not missing, f"缺失 {missing}" if missing else
              f"{len(registry)} 条")
        sample = registry.get("01-001", {})
        check("指纹库 original/norm 齐备",
              bool(sample.get("original")) and bool(sample.get("norm")))
        check("norm 去掉段首缩进（不再以全角空格开头）",
              not sample.get("norm", " ").startswith("\u3000"))

        # 2) 实体层
        ent = read_json(LAYER_JSON_DIR / f"ent_{DEMO_VOLUME}.json", default={}) or {}
        ent_records = ent.get("records", [])
        check("实体层单卷 JSON 顶层 records 非空", bool(ent_records),
              f"{len(ent_records)} 条")
        check("实体主键前缀 ENT-", all(str(r.get("ent_id", "")).startswith("ENT-")
                                      for r in ent_records))
        check("实体记录注入 original/norm（与指纹库一致）",
              all(r.get("original") == registry.get(r["item_id"], {}).get("original")
                  for r in ent_records))
        index = read_json(LAYER_JSON_DIR / "ent_index.json", default={}) or {}
        check("实体索引 ent_index.json 可查「洛下闳」",
              "洛下闳" in (index.get("index") or {}))

        # 3) 事件层
        event = read_json(LAYER_JSON_DIR / f"event_{DEMO_VOLUME}.json", default={}) or {}
        ev_records = event.get("records", [])
        check("事件主键前缀 WZZ-E-",
              all(str(r.get("event_id", "")).startswith("WZZ-E-") for r in ev_records))
        who_ok = all(isinstance(r.get("who"), dict) and "who_ent_ids" in r["who"]
                     for r in ev_records)
        check("who 字符串自动升格为 {text, who_ent_ids}", who_ok)
        check("when/where 未考处显式写「未明」",
              all(r.get("when") == "未明" and r.get("where") == "未明" for r in ev_records))
        resolved = [r for r in ev_records if r["who"].get("who_ent_ids") == []]
        check("who 词形命中实体表（汉明帝 已回填 ENT-）",
              any(r["who"].get("text") == "汉明帝" and r["who"].get("who_ent_ids")
                  for r in ev_records), f"未回填 {len(resolved)} 条")

        # 4) 关系层：枚举别名归一
        rel = read_json(LAYER_JSON_DIR / f"rel_{DEMO_VOLUME}.json", default={}) or {}
        rel_records = rel.get("records", [])
        check("关系层「主从」归一为「上下级」",
              all(r.get("relation_type") == "上下级" for r in rel_records),
              f"{[r.get('relation_type') for r in rel_records]}")
        check("关系层 person_a.ent_ids 回填",
              all((r.get("person_a") or {}).get("ent_ids") for r in rel_records))

        # 5) 名物层
        obj = read_json(LAYER_JSON_DIR / f"obj_{DEMO_VOLUME}.json", default={}) or {}
        check("名物层 attributes 保留自由键",
              all(isinstance(r.get("attributes"), dict) for r in obj.get("records", [])))

        # 6) 层汇总与日志
        summary = read_json(BUILD_DIR / "event__summary.json", default={}) or {}
        check("层汇总 event__summary.json 含本次卷切片",
              DEMO_VOLUME in (summary.get("volumes") or {}))
        logs = read_json(BUILD_DIR / "_event_logs.json", default={}) or {}
        check("层日志 _event_logs.json 落盘", "unknown_enum_total" in logs)

        # 7) 枚举待核（收集-报告-暂存：未知值入 pending 而不中断打包）
        pending_path = BUILD_DIR / "_enums_pending.json"
        pending = read_json(pending_path, default=None)
        check("枚举待核文件 _enums_pending.json 可读且为容器", isinstance(pending, (list, dict)),
              f"类型 {type(pending).__name__}")

        # 8) 跨层贯通
        join = read_json(LAYER_JSON_DIR / "_kg_join.json", default={}) or {}
        rows = join.get("rows", [])
        by_id = {r["item_id"]: r for r in rows}
        check("_kg_join 行数 = 指纹库条目数", len(rows) == len(registry),
              f"{len(rows)} vs {len(registry)}")
        row = by_id.get("01-006", {})
        check("贯通行含 events/rels/objs 三键",
              all(row.get(k) for k in ("events", "rels", "objs")))
        check("layer_count 与非空层数一致",
              all(int(r["layer_count"]) == sum(
                  1 for k in ("events", "rels", "nams", "cits", "objs", "cuss",
                              "opns", "mings", "appts", "trls", "ents") if r.get(k))
                  for r in rows))

        # 9) 验证器
        layer_val = read_json(ROOT / "_validate" / "layer_validation.json", default={}) or {}
        check("分层验证 0 error", layer_val.get("totals", {}).get("errors") == 0,
              str(layer_val.get("totals")))
        join_val = read_json(ROOT / "_validate" / "kg_join_validation.json", default={}) or {}
        check("贯通验证 0 error", join_val.get("errors") == 0,
              f"errors={join_val.get('errors')} warnings={join_val.get('warnings')}")
        check("贯通覆盖率 100%", join_val.get("coverage_ratio") == 1.0,
              str(join_val.get("coverage_ratio")))
    finally:
        # 先把样本与本轮产物删掉，再原样搬回真实数据，最后按快照兜底
        for p in sample_paths:
            if p.exists():
                p.unlink()
        for p in layer_paths:
            if p.exists() and str(p) in snap:
                continue
            if p.exists():
                p.unlink()
        if stash_dir.exists():
            for p in sorted(stash_dir.glob("*")):
                # 源数据（含统一卷源）回 _src/，层产物回 _layers/
                if p.name.endswith(".py") and ("_ai_" in p.name
                                               or p.name.startswith("_vol_")):
                    dest_dir = SRC_DIR
                else:
                    dest_dir = LAYER_JSON_DIR
                target = dest_dir / p.name
                if target.exists():
                    target.unlink()
                shutil.move(str(p), str(target))
            shutil.rmtree(stash_dir)
        restore(snap, source_paths + layer_paths)
        if keep:
            print("\n[保留] 样本产物保留在 _src/_layers，便于人工检查"
                  "（真实数据已还原，重跑前请先清掉样本文件）。")
        else:
            for extra in ("_validate/layer_validation.json",
                          "_validate/kg_join_validation.json"):
                p = ROOT / extra
                if p.exists():
                    p.unlink()
            print("\n[还原] _src 与 _layers 已逐字节还原。")

    failed = [c for c in checks if not c["ok"]]
    report_stats("自检结果", {
        "检查项": len(checks),
        "通过": len(checks) - len(failed),
        "失败": len(failed),
        "失败项": [c["check"] for c in failed] or "无",
    })
    write_text(ROOT / "_selftest_last.txt", json.dumps(
        {"checks": checks, "steps": steps}, ensure_ascii=False, indent=2) + "\n")
    if failed:
        raise SystemExit(1)
    print("\n[完成] 端到端自检全部通过。")


if __name__ == "__main__":
    main()
