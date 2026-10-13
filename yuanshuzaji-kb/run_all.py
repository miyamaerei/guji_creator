# -*- coding: utf-8 -*-
"""宛署 9 层管线：底座切分 → 装填（人工）→ 打包 → 整合 → 校验。
用法：
  python run_all.py '--volumes=NN'       # 打包指定卷（源数据已装填）
  python run_all.py --all                # 全量打包已装填卷 + 整合 + 校验
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

BUILDERS = ["build_ent_keys.py", "build_appts.py", "build_events.py", "build_lits.py",
            "build_regs.py", "build_nams.py", "build_opns.py", "build_cuss.py",
            "build_geos.py"]


def run(cmd):
    print(">>> " + " ".join(cmd))
    r = subprocess.run([sys.executable] + cmd, cwd=ROOT)
    if r.returncode != 0:
        sys.exit(r.returncode)
    return r


def main():
    args = sys.argv[1:]
    if "--all" in args:
        for b in BUILDERS:
            run([b])
        run(["build_kg_join.py"])
        run(["validate_layers.py"])
        return
    # 单卷/多卷：--volumes=NN 或 '--volumes=NN'
    vol_arg = None
    for a in args:
        if a.startswith("--volumes"):
            vol_arg = a
            break
    if vol_arg is None:
        print("用法：python run_all.py '--volumes=NN' 或 python run_all.py --all")
        sys.exit(1)
    for b in BUILDERS:
        run([b, vol_arg])


if __name__ == "__main__":
    main()
