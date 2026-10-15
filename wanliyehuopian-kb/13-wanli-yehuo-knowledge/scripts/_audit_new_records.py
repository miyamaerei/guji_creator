# -*- coding: utf-8 -*-
"""新增记录溯源终检：对比补漏前的备份，只校验本次新增记录，
按【条目级】+ 宽松（忽略标点）口径判定原文引用是否越界。
用法: python _audit_new_records.py 06-10 / 11-15 / 16-20 / all
只读，不写文件。
"""
import json
import re
import sys
from pathlib import Path

sys.argv = ["x", "01"]
BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "scripts"))
import _audit_origins as A  # noqa

PUNCT = set("，。；：、！？“”‘’（）《》〈〉…—·,.!?:;()\"'　 \n\r\t")
PROV = ("original", "evidence", "quoted_text", "source_text")
BACKUP = {v: ("_backup_gap0610" if v in ("06", "07", "08", "09", "10") else "_backup_gap1120")
          for v in ["%02d" % i for i in range(6, 21)]}


def n2(s):
    return "".join(c for c in s if c not in PUNCT)


def rid(r):
    for k in ("ent_id", "rule_id", "event_id", "appt_id", "rel_id", "cit_id",
              "opn_id", "ming_id", "tme_id", "reg_id"):
        if k in r:
            return r[k]
    return None


segs = {v: A.build_segments(v) for v in ["%02d" % i for i in range(1, 35)]}

rng = sys.argv[1] if len(sys.argv) > 1 else "all"
if rng in ("all", "01"):
    vols = ["%02d" % i for i in range(6, 21)]
elif "-" in rng:
    a, b = rng.split("-")
    vols = ["%02d" % i for i in range(int(a), int(b) + 1)]
else:
    vols = rng.split(",")

tot_new = bad_new = tot_old = bad_old = 0
for v in vols:
    if v not in BACKUP:
        continue
    s_all = segs[v]
    for L in A.LAYERS:
        cur = json.load(open(BASE / "_layers" / L / f"{L}_{v}.json", encoding="utf-8"))
        cur = cur["records"] if isinstance(cur, dict) else cur
        old = json.load(open(BASE / BACKUP[v] / f"{L}_{v}.json", encoding="utf-8"))
        old = old["records"] if isinstance(old, dict) else old
        oids = {rid(r) for r in old}
        for tag, recs in (("old", old), ("new", [r for r in cur if rid(r) not in oids])):
            for r in recs:
                sg = s_all.get(r["item_id"])
                if not sg:
                    continue
                ss = n2(sg)
                for k in PROV:
                    val = r.get(k)
                    if not isinstance(val, str) or len(val) < 8:
                        continue
                    parts = [p for p in re.split(r"……|；", val) if p.strip()]
                    ok = all(n2(p) in ss for p in parts)
                    if tag == "new":
                        tot_new += 1
                        if not ok:
                            bad_new += 1
                            print("NEW-BAD", L, r["item_id"], k, repr(val[:40]))
                    else:
                        tot_old += 1
                        if not ok:
                            bad_old += 1

print("本次新增记录 溯源校验 %d，越界 %d" % (tot_new, bad_new))
print("既有记录   溯源校验 %d，越界 %d（历史遗留，另行治理）" % (tot_old, bad_old))
print("NEW-RESULT:", "PASS" if bad_new == 0 else "HAS-FAILS")
