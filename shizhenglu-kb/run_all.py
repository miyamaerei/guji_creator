# -*- coding: utf-8 -*-
"""一键重跑：四段式（②③④）。用法：python run_all.py [--volumes 01,02]
--volumes 指定时只重算该卷（幂等，不动其它卷）；缺省重跑全部已装填卷。"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]
vol_flag = []
for a in args:
    if a.startswith("--volumes"):
        val = a.split("=", 1)[1] if "=" in a else args[args.index(a) + 1]
        vol_flag = ["--volumes", val]
        break

cmds = [
    [sys.executable, os.path.join(ROOT, "build_ent_keys.py")] + vol_flag,
    [sys.executable, os.path.join(ROOT, "build_rules.py")] + vol_flag,
    [sys.executable, os.path.join(ROOT, "build_struct.py")] + vol_flag,
    [sys.executable, os.path.join(ROOT, "build_kg_join.py")] + vol_flag,
]
if "--skip-baseline" in args:
    cmds.append([sys.executable, os.path.join(ROOT, "validate_layers.py"), "--skip-baseline"])
else:
    cmds.append([sys.executable, os.path.join(ROOT, "validate_layers.py")])

for c in cmds:
    print(">>>", " ".join(c))
    r = subprocess.call(c)
    if r != 0:
        sys.exit("管线中止：%s 退出码 %d" % (os.path.basename(c[1]), r))
print("管线全部通过 ✓")
