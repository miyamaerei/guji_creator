# -*- coding: utf-8 -*-
"""对比"原有记录"与"本次新增记录"的溯源违约率（严格 vs 宽松）。
严格=按源文逐字（去空白）；宽松=再忽略标点。
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
PROV = ("original", "evidence", "quoted_text")


def strip_punct(s):
    return "".join(c for c in s if c not in PUNCT)


def norm2(s):
    return strip_punct(re.sub(r"[\s\u3000]", "", s or ""))


segs = {v: A.build_segments(v) for v in ["%02d" % i for i in range(1, 35)]}


def scan(recs, vol):
    tot = 0
    ds = []
    dl = []
    for r in recs:
        s = segs[vol].get(r["item_id"])
        if not s:
            continue
        ss = norm2(s)
        for k in PROV:
            val = r.get(k)
            if not isinstance(val, str) or len(val) < 8:
                continue
            parts = [p for p in re.split(r"……|；", val) if p.strip()]
            if k == "original" and "……" in val:
                ok_s = all(re.sub(r"[\s\u3000]", "", p) in s for p in parts)
                ok_l = all(norm2(p) in ss for p in parts)
            else:
                ok_s = re.sub(r"[\s\u3000]", "", val) in s
                ok_l = norm2(val) in ss
            tot += 1
            rid = "?"
            for kk in ("ent_id", "rule_id", "event_id", "appt_id", "rel_id", "cit_id", "opn_id", "ming_id", "tme_id", "reg_id"):
                if kk in r:
                    rid = r[kk]
                    break
            if not ok_s:
                ds.append((rid, k))
            if not ok_l:
                dl.append((rid, k, val[:28]))
    return tot, ds, dl


BACKUPS = {"06": "_backup_gap0610", "07": "_backup_gap0610", "08": "_backup_gap0610",
           "09": "_backup_gap0610", "10": "_backup_gap0610",
           "11": "_backup_gap1120", "12": "_backup_gap1120", "13": "_backup_gap1120",
           "14": "_backup_gap1120", "15": "_backup_gap1120",
           "16": "_backup_gap1120", "17": "_backup_gap1120", "18": "_backup_gap1120",
           "19": "_backup_gap1120", "20": "_backup_gap1120",
           "01": None, "02": None, "03": None, "04": None, "05": None,
           }

vols = sys.argv[1].split(",") if len(sys.argv) > 1 and sys.argv[1] != "01" else ["%02d" % i for i in range(6, 21)]

for v in vols:
    cur = []
    for L in A.LAYERS:
        d = json.load(open(BASE / "_layers" / L / f"{L}_{v}.json", encoding="utf-8"))
        cur += d["records"] if isinstance(d, dict) else d
    t2, ds2, dl2 = scan(cur, v)
    line = f"vol{v} 现有: 校验{t2} 严失{len(ds2)} 宽失{len(dl2)}"
    bk = BACKUPS.get(v)
    if bk:
        old = []
        for L in A.LAYERS:
            d2 = json.load(open(BASE / bk / f"{L}_{v}.json", encoding="utf-8"))
            old += d2["records"] if isinstance(d2, dict) else d2
        t1, ds1, dl1 = scan(old, v)
        line += f"  ||  原有: 校验{t1} 严失{len(ds1)} 宽失{len(dl1)}"
    print(line)
    if len(sys.argv) > 2 and sys.argv[2] == "detail":
        for x in dl2[:12]:
            print("     宽失:", x)
