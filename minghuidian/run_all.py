# -*- coding: utf-8 -*-
"""一键运行：底座 → 打包 → 校验"""
import os, sys, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable

for step in ["build_base.py", "build_layers.py", "validate_layers.py"]:
    print("\n========== %s ==========" % step)
    r = subprocess.run([PY, os.path.join(ROOT, step)], cwd=ROOT)
    if r.returncode != 0:
        print("✗ %s 失败 (exit %d)" % (step, r.returncode))
        sys.exit(r.returncode)
print("\n✓ 全流程完成")
