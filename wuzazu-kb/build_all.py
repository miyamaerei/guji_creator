"""《五杂俎》知识工程 | 一键全量重跑 / 端到端自检

顺序（与 skill 执行流程一致）：
    底座 build_base -> 卷阅读模式标注 -> 实体层 ent -> event -> rel -> nam -> cit
    -> obj -> cus -> opn -> ming -> appt -> trl -> 跨层整合 _kg_join
    -> 分层验证 -> 贯通验证

用法：
    python build_all.py                 # 全量重跑 + 自检
    python build_all.py --volumes 01    # 只重算 01 卷的解读层（底座仍全量）
    python build_all.py --skip-validate # 只打包不验证
    python build_all.py --stage ent,event        # 只跑指定阶段
    python build_all.py --list          # 打印阶段清单

任何阶段抛错即中止并报告（非零退出码），日志同时写入 _build/run_all.log。
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# Windows 控制台可能是 GBK：强制 UTF-8 并允许替换，避免中文报告触发 UnicodeEncodeError
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
os.environ.setdefault("PYTHONIOENCODING", "utf-8:replace")

from _kg_pack_base import BUILD_DIR, banner, report_stats, write_text  # noqa: E402

# (阶段名, 脚本, 是否支持 --volumes)
STAGES: list[tuple[str, str, bool]] = [
    ("base", "build_base.py", False),
    ("profile", "build_volume_profile.py", True),
    ("spread", "_vol_schema.py", True),   # 统一卷源 → 11 个分层文件（按卷扇出的摊平）
    ("ent", "build_ent.py", True),
    ("event", "build_event.py", True),
    ("rel", "build_rel.py", True),
    ("nam", "build_nam.py", True),
    ("cit", "build_cit.py", True),
    ("obj", "build_obj.py", True),
    ("cus", "build_cus.py", True),
    ("opn", "build_opn.py", True),
    ("ming", "build_ming.py", True),
    ("appt", "build_appt.py", True),
    ("trl", "build_trl.py", True),
    ("join", "build_kg_join.py", True),
    ("validate", "validate_layers.py", True),
    ("validate_join", "validate_kg_join.py", True),
]


def run_stage(name: str, script: str, supports_volumes: bool, vols: list[str] | None,
              log: list[str]) -> tuple[int, float]:
    cmd = [sys.executable, str(ROOT / script)]
    # _vol_schema.py 是多命令工具，摊平阶段显式给子命令
    if script == "_vol_schema.py":
        cmd.append("split")
    if vols and supports_volumes:
        cmd += ["--volumes", *vols]
    started = time.time()
    print(f"\n>>> [{name}] {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    elapsed = time.time() - started
    log.append(f"\n{'=' * 70}\n[{name}] {script}  exit={proc.returncode}  {elapsed:.2f}s\n"
               f"{'-' * 70}\n{proc.stdout}\n{proc.stderr}")
    tail = (proc.stdout or "").strip().splitlines()[-6:]
    for line in tail:
        print(f"    {line}")
    if proc.returncode != 0:
        print(f"    [stderr] {(proc.stderr or '').strip()[:400]}")
    return proc.returncode, elapsed


def main() -> None:
    argv = sys.argv[1:]
    skip_validate = "--skip-validate" in argv
    only: list[str] | None = None
    for i, token in enumerate(argv):
        if token == "--stage" and i + 1 < len(argv):
            only = [s.strip() for s in argv[i + 1].replace(",", " ").split()]
        elif token.startswith("--stage="):
            only = [s.strip() for s in token.split("=", 1)[1].replace(",", " ").split()]
    vols: list[str] | None = None
    for i, token in enumerate(argv):
        if token == "--volumes":
            vols = []
            for nxt in argv[i + 1:]:
                if nxt.startswith("-"):
                    break
                vols.append(nxt.zfill(2))
        elif token.startswith("--volumes="):
            vols = [v.zfill(2) for v in token.split("=", 1)[1].replace(",", " ").split() if v]

    if "--list" in argv:
        banner("阶段清单")
        for name, script, sup in STAGES:
            print(f"  {name:<14} {script:<22} --volumes: {'是' if sup else '否'}")
        return

    banner("一键重跑 build_all")
    stages = STAGES
    if only:
        stages = [s for s in STAGES if s[0] in only]
        unknown = [s for s in only if s not in {x[0] for x in STAGES}]
        if unknown:
            raise SystemExit(f"未知阶段：{unknown}")
    if skip_validate:
        stages = [s for s in stages if not s[0].startswith("validate")]

    log: list[str] = [f"build_all 启动：{time.strftime('%Y-%m-%d %H:%M:%S')}  volumes={vols or '全部'}"]
    results: list[dict] = []
    failed = False
    for name, script, sup in stages:
        code, elapsed = run_stage(name, script, sup, vols, log)
        results.append({"stage": name, "script": script, "exit": code,
                        "seconds": round(elapsed, 2)})
        if code != 0:
            failed = True
            print(f"\n[中止] 阶段 {name} 失败（exit={code}），后续阶段未执行。")
            break

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    write_text(BUILD_DIR / "run_all.log", "\n".join(log) + "\n")
    report_stats("阶段结果", {r["stage"]: f"exit={r['exit']}  {r['seconds']}s" for r in results})
    print(f"\n[日志] {BUILD_DIR / 'run_all.log'}")
    if failed:
        raise SystemExit(1)
    print("\n[完成] 底座 + 11 层 + 跨层整合 + 双层验证 全部通过。")


if __name__ == "__main__":
    main()
