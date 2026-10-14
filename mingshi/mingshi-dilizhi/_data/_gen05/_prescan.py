# -*- coding: utf-8 -*-
"""预扫 gen_part*.py 中所有 N(iid, text) 调用的 norm 命中情况（一次性全检，免逐条试错）。"""
import io, json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
reg = json.load(io.open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

PAT = re.compile(r'N\("(\d\d-\d\d\d)",\s*"([^"]*)"\)')

total_miss = 0
for fn in sys.argv[1:]:
    src = io.open(fn, encoding="utf-8").read()
    calls = PAT.findall(src)
    miss = [(iid, t) for iid, t in calls if t not in reg[iid]["norm"]]
    print("%s: N()=%d 未命中=%d" % (os.path.basename(fn), len(calls), len(miss)))
    for iid, t in miss:
        print("   %s %r" % (iid, t))
    total_miss += len(miss)
print("TOTAL MISS =", total_miss)
