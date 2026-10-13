# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - 一键全量重跑（run_all.py）

收敛者入口：按 SKILL.md §10 的构建顺序依次执行
    1. annotate       底座提取（全本 -> 分卷条目 + 指纹库）
    2. build_ent_keys L1 实体（组级 ID + alias_index）
    3. build_appt / build_rel / build_event / build_opn / build_trl
    4. build_kg_join 跨层整合索引
    5. validate_layers 构建校验（验收标尺：验证缺漏清单.txt 问题数 = 0）

用法：
    python run_all.py                     # 全量重跑（含 annotate 全量底座）
    python run_all.py --skip-annotate     # 底座已存在：跳过 annotate，只重跑打包与校验
    python run_all.py --volumes 01        # 只重算卷 01（增量合并，其余卷保留）
    python run_all.py --smoke             # 冒烟：把 scripts/samples/ 拷入 _src 后跑打包——
                                          #   验证代码管线可运行（配合 validate --skip-baseline）
退出码：任一步骤失败（非 0）即中断并返回该退出码。
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from typing import List, Optional

import _kg_config as cfg
from _kg_pack_base import main_guard, print_progress

_SCRIPTS = os.path.dirname(os.path.abspath(__file__))


def _run(step: str, args: List[str]) -> int:
    print_progress(f"\n===== [{step}] python {' '.join(args)} =====")
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        [sys.executable] + args, cwd=_SCRIPTS, env=env, text=True, encoding="utf-8"
    )
    if proc.returncode != 0:
        print_progress(
            f"[run_all] 步骤 {step} 失败（退出码 {proc.returncode}），终止。"
        )
    return proc.returncode


def run_all(
    skip_annotate: bool = False,
    volumes: Optional[str] = None,
    smoke: bool = False,
) -> int:
    cfg.ensure_dirs()
    vol_args = ["--volumes", volumes] if volumes else []
    smoke_args = ["--skip-baseline"] if smoke else []

    # 冒烟模式：把 samples/ 拷入 _src（可重跑基准的样例数据，真实装填前可随时清空）
    if smoke:
        for f in sorted(os.listdir(cfg.SAMPLES_DIR)):
            src = os.path.join(cfg.SAMPLES_DIR, f)
            dst = os.path.join(cfg.SRC_DIR, f)
            shutil.copy2(src, dst)
            print_progress(
                f"[smoke] 样例 {f} -> {os.path.relpath(dst, cfg.INSTANCE_DIR)}"
            )

    steps: List[str] = []
    if not skip_annotate:
        steps.append("annotate")
    steps += [
        "build_ent_keys",
        "build_appt",
        "build_rel",
        "build_event",
        "build_opn",
        "build_trl",
    ]
    steps.append("build_kg_join")
    steps.append("validate_layers")

    for step in steps:
        if step == "annotate":
            code = _run(
                step, ["annotate.py", "--expect", cfg.DEFAULT_EXPECT_ITEMS, *vol_args]
            )
        elif step == "validate_layers":
            code = _run(step, ["validate_layers.py", *smoke_args])
        else:
            code = _run(step, [f"{step}.py", *vol_args])
        if code != 0:
            return code
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="《先进遗风》一键全量重跑（run_all）")
    ap.add_argument(
        "--skip-annotate", action="store_true", help="跳过底座提取（底座已存在时）"
    )
    ap.add_argument("--volumes", default=None, help="只重算的卷号（01,02）")
    ap.add_argument(
        "--smoke", action="store_true", help="冒烟模式（拷入样例 + 跳过基线比对）"
    )
    args = ap.parse_args()
    return run_all(
        skip_annotate=args.skip_annotate, volumes=args.volumes, smoke=args.smoke
    )


if __name__ == "__main__":
    main_guard()
    raise SystemExit(main())
