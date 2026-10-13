# -*- coding: utf-8 -*-
"""福惠全书总调度：指定卷全层打包 → 跨层整合 → 校验。
用法：python run_all.py --volumes 01   （幂等；不加参数=全部已装填卷）"""
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PACKERS = ["build_ent_keys", "build_rules", "build_structs", "build_regs",
           "build_opns", "build_procs", "build_docs", "build_rels",
           "build_kg_join"]


def run(cmd):
    print(">>", cmd)
    r = subprocess.run(cmd, cwd=ROOT, capture_output=False)
    if r.returncode != 0:
        print("!! 退出码 %d：%s" % (r.returncode, cmd))
        sys.exit(r.returncode)


def main():
    args = sys.argv[1:]
    for p in PACKERS:
        run([sys.executable, os.path.join(ROOT, p + ".py")] + args)
    run([sys.executable, os.path.join(ROOT, "validate_layers.py"), "--skip-baseline"])
    print("== 全层打包+整合+校验完成 ==")


if __name__ == "__main__":
    main()
