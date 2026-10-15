# -*- coding: utf-8 -*-
"""溯源强校验器：校验每条记录的原文引用是否落在【其所属条目】的原文段内。
按整卷校验无法发现跨条目串引，本脚本按条目级校验。
用法: python _audit_origins.py 06,07,08,09,10   （或 11,12,... / 16,17,...）
只读，不写文件。
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
LAYERS = ["ents", "rules", "events", "appts", "rels", "opns", "cits", "mings", "tmes", "regs"]
IDKEY = {"ents": "ent_id", "rules": "rule_id", "events": "event_id", "appts": "appt_id",
         "rels": "rel_id", "cits": "cit_id", "opns": "opn_id", "mings": "ming_id",
         "tmes": "tme_id", "regs": "reg_id"}
PROV = ("original", "evidence", "quoted_text", "source_text", "text", "content", "description")

vols = sys.argv[1].split(",")

txt = open(BASE / "assets" / "sources" / "万历野获编.txt", encoding="utf-8").read()
flat = re.sub(r"[\s\u3000]", "", txt)
anchors = [(m.group(1), m.start()) for m in re.finditer(r"【([^】]{1,40})】", txt)]

regs = json.load(open(BASE / "_item_registry.json", encoding="utf-8"))["records"]


def build_segments(vol):
    """按顺序把 registry 条目与源文 【title】 锚点对齐，返回 {item_id: 该条目源文(去空白)}"""
    items = [r for r in regs if r["item_id"].startswith(vol + "-")]
    # flat 坐标下的锚点
    fpos = []
    for m in re.finditer(r"【([^】]{1,40})】", flat):
        fpos.append((m.group(1), m.start()))
    fp = dict()
    cur = 0
    out = {}
    # 顺序匹配：从 cur 起找下一个该 title
    idx = 0
    ordered = []
    for r in items:
        title = r["entry_title"]
        j = None
        for k in range(idx, len(fpos)):
            if fpos[k][0] == title:
                j = k
                break
        if j is None:
            ordered.append((r["item_id"], None))
            continue
        ordered.append((r["item_id"], j))
        idx = j + 1
    for i, (iid, j) in enumerate(ordered):
        if j is None:
            out[iid] = None
            continue
        start = fpos[j][1]
        end = len(flat)
        for (iid2, j2) in ordered[i + 1:]:
            if j2 is not None:
                end = fpos[j2][1]
                break
        out[iid] = flat[start:end]
    return out


def norm(s):
    return re.sub(r"[\s\u3000]", "", s or "")


total_bad = 0
for vol in vols:
    seg = build_segments(vol)
    miss_seg = [k for k, v in seg.items() if v is None]
    if miss_seg:
        print("vol%s 段未对齐条目: %s" % (vol, miss_seg))
    bad = []
    for L in LAYERS:
        d = json.load(open(BASE / "_layers" / L / f"{L}_{vol}.json", encoding="utf-8"))
        recs = d["records"] if isinstance(d, dict) else d
        for r in recs:
            iid = r["item_id"]
            s = seg.get(iid)
            if not s:
                continue
            for k in PROV:
                val = r.get(k)
                if not isinstance(val, str) or not val or len(val) < 8:
                    continue
                if k in ("text", "content", "description") and "……" not in val:
                    # 文本型字段允许概括，仅在含书名号/引号时校验
                    if "《" not in val and "“" not in val:
                        continue
                if k == "original" and val.count("……"):
                    parts = [p for p in re.split(r"……|；", val) if p.strip()]
                    ok = all(norm(p) in s for p in parts)
                else:
                    ok = norm(val) in s
                if not ok:
                    bad.append((L, r[IDKEY[L]], iid, k, val[:40]))
    print("vol%s 溯源越界 %d 条" % (vol, len(bad)))
    seen = set()
    for L, rid, iid, k, v in bad:
        if rid in seen:
            continue
        seen.add(rid)
        print("   %-6s %-14s item=%s %-12s %r" % (L, rid, iid, k, v))
    total_bad += len(bad)

print("TOTAL 溯源问题:", total_bad)
