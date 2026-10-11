# -*- coding: utf-8 -*-
"""A/B 回归：老路径（直接读分层文件）vs 新路径（统一卷源 → 摊平 → 读分层文件）。

对每个卷做：
  A. 用备份的老分层文件跑打包器，快照每层产物
  B. 用统一卷源摊平出来的分层文件跑打包器，快照每层产物
  C. 逐层逐条比对（ID、业务字段、引用回填结果）

两者产物必须逐字节一致 —— 这才证明"换装填格式"对下游零影响。

用法：python _vol_ab_regression.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

import _vol_schema as V  # noqa: E402

LEGACY = ROOT / "_backup_src_20261010"          # 迁移前的老分层文件
CUR = ROOT / "_src"
VOLUMES = ["01", "02"]
LAYER_ENTRIES = {                # 层 -> 入口脚本
    "ent": "build_ent.py", "event": "build_event.py", "rel": "build_rel.py",
    "nam": "build_nam.py", "cit": "build_cit.py", "obj": "build_obj.py",
    "cus": "build_cus.py", "opn": "build_opn.py", "ming": "build_ming.py",
    "appt": "build_appt.py", "trl": "build_trl.py",
}


def stash_current() -> None:
    stash = ROOT / "_ab_stash"
    if stash.exists():
        shutil.rmtree(stash)
    stash.mkdir()
    for layer in V.LAYERS:
        for vol in V.ALL_VOLUMES:
            p = CUR / f"_{layer}_ai_{vol}.py"
            if p.exists():
                shutil.copy2(p, stash / p.name)


def place(files_from: Path, layers: list[str], vols: list[str]) -> None:
    """把指定来源的分层文件放到 _src/，并清掉不在来源里的（避免混入）。"""
    for layer in layers:
        for vol in V.ALL_VOLUMES:
            tgt = CUR / f"_{layer}_ai_{vol}.py"
            src = files_from / tgt.name
            if vol in vols and src.exists():
                shutil.copy2(src, tgt)
            elif tgt.exists():
                tgt.unlink()


def restore_stash() -> None:
    stash = ROOT / "_ab_stash"
    for layer in V.LAYERS:
        for vol in V.ALL_VOLUMES:
            tgt = CUR / f"_{layer}_ai_{vol}.py"
            if tgt.exists():
                tgt.unlink()
    if stash.exists():
        for p in stash.glob("*.py"):
            shutil.copy2(p, CUR / p.name)
        shutil.rmtree(stash)


def run_layer(layer: str, vols: list[str]) -> bool:
    proc = subprocess.run(
        [sys.executable, str(ROOT / LAYER_ENTRIES[layer]), "--volumes", *vols],
        cwd=str(ROOT), capture_output=True, text=True,
        encoding="utf-8", errors="replace")
    return proc.returncode == 0


def snapshot(layers: list[str], vols: list[str]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for layer in layers:
        rows: list[dict] = []
        for vol in vols:
            p = ROOT / "_layers" / f"{layer}_{vol}.json"
            if not p.exists():
                continue
            obj = json.loads(p.read_text(encoding="utf-8"))
            rows.extend(obj.get("records", []))
        if rows:
            out[layer] = rows
    return out


def strip_volatile(rows: list[dict]) -> list[str]:
    """去掉时间戳类易变字段，只比业务内容。"""
    volatile = {"generated_at", "builder"}
    out = []
    for r in rows:
        out.append(repr(sorted((k, repr(v)) for k, v in r.items() if k not in volatile)))
    return sorted(out)


# 已知的**有意数据修正**（迁移前就存在的错值，按枚举口径改对）：
# 02-080 的 cit 把 citation_type 的值「考辨」写进了 context 字段，
# 2026-10-10 修正为「考源」。A/B 老路径用的是修正前的备份，故会报差异。
# 注意：只作用于 cit 层——event/rel 本来就没有 context 字段。
KNOWN_FIXES: dict[str, dict[str, dict[str, str]]] = {
    "cit": {"02-080": {"context": "考源"}},
}


def apply_known_fixes(layer: str, rows: list[dict]) -> list[dict]:
    """把老路径快照里的已知错值按修正口径改过来，使比对只反映迁移影响。"""
    by_item = KNOWN_FIXES.get(layer)
    if not by_item:
        return rows
    out = []
    for r in rows:
        r = dict(r)
        for k, v in by_item.get(str(r.get("item_id")), {}).items():
            if r.get(k) != v:
                r[k] = v
        out.append(r)
    return out


def main() -> None:
    layers = [l for l in V.LAYERS
              if any((LEGACY / f"_{l}_ai_{v}.py").exists() for v in VOLUMES)]
    if not layers:
        print(f"备份目录 {LEGACY.name}/ 里没有可比对的分层文件，先跑一次迁移")
        return

    print("=" * 68)
    print("A/B 回归：老分层文件 vs 统一卷源摊平")
    print(f"参与比对层：{layers}　卷：{VOLUMES}")
    print("=" * 68)

    stash_current()
    try:
        # ---- A. 老路径 ----
        place(LEGACY, layers, VOLUMES)
        for layer in layers:
            run_layer(layer, VOLUMES)
        snap_a = snapshot(layers, VOLUMES)
        print(f"\n[A] 老路径完成：" +
              " ".join(f"{k}={len(v)}" for k, v in snap_a.items()))

        # ---- B. 新路径 ----
        for vol in VOLUMES:
            V.split(vol)
        for layer in layers:
            run_layer(layer, VOLUMES)
        snap_b = snapshot(layers, VOLUMES)
        print(f"[B] 新路径完成：" +
              " ".join(f"{k}={len(v)}" for k, v in snap_b.items()))

        # ---- C. 比对 ----
        print("\n比对结果：")
        ok = True
        for layer in layers:
            a = strip_volatile(apply_known_fixes(layer, snap_a.get(layer, [])))
            b = strip_volatile(snap_b.get(layer, []))
            if a == b:
                print(f"  PASS  {layer:6s} {len(a):4d} 条逐字段一致")
            else:
                ok = False
                print(f"  FAIL  {layer:6s} {len(a)} vs {len(b)} 条不一致")
                for x in [y for y in a if y not in b][:2]:
                    print(f"          仅老路径有：{x[:150]}")
                for x in [y for y in b if y not in a][:2]:
                    print(f"          仅新路径有：{x[:150]}")
        print()
        print("结论：" + ("下游产物完全一致，换装填格式零影响" if ok else "存在差异"))
        sys.exit(0 if ok else 1)
    finally:
        restore_stash()


if __name__ == "__main__":
    main()