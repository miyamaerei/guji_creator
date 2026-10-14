# -*- coding: utf-8 -*-
"""P3-B2: 建 L6.REPORT 文册·勘合层（Q9 文移凭证溯源）。

明会典大量记载「造册/勘合/印信/引票/命诰/报表」等文书凭证制度。
本层把全库出现的文书名词抽成条目，并截取所在分句为 context。
"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
PUA = {0xE5AB: "隶", 0xEA1F: "弘", 0xF5F6: "封", 0xEB08: "卷"}


def nz(t):
    return "".join(PUA.get(ord(c), c) for c in t)


DOCS = {
    "册籍": ["鱼鳞图册", "须知文册", "实征文册", "勘合文册", "黄册", "文册", "簿籍", "底簿",
             "文簿", "清册", "总册", "图册", "册籍", "簿册", "军黄册", "匠册", "户口册"],
    "勘合凭证": ["勘合", "通关", "文凭", "批文", "执照", "号纸", "由帖", "帖文", "户帖",
                 "印票", "信票", "火票"],
    "印信": ["印信", "符验", "牌面", "关防", "条记", "印记"],
    "引票": ["盐引", "茶引", "引票", "盐钞", "仓钞"],
    "命诰": ["诰命", "敕命", "敕书", "告身", "敕谕"],
    "报表": ["岁报", "季报", "月报", "岁办", "岁解", "岁派"],
}
ALL_DOCS = sorted({d for v in DOCS.values() for d in v}, key=len, reverse=True)
DOC2CAT = {d: cat for cat, v in DOCS.items() for d in v}
SPL = re.compile(r"[。；　]")

records = []
seen = set()
for k, v in sorted(reg.items()):
    t = nz(v.get("original") or "")
    for d in ALL_DOCS:
        start = 0
        while True:
            i = t.find(d, start)
            if i < 0:
                break
            start = i + len(d)
            key = (k, d, i)
            if key in seen:
                continue
            seen.add(key)
            s = max((m.end() for m in SPL.finditer(t, 0, i)), default=0)
            e = SPL.search(t, i + len(d))
            e = e.start() if e else min(len(t), i + 40)
            records.append({
                "rep_id": "", "item_id": k, "volume": v.get("volume"),
                "doc_name": d, "doc_category": DOC2CAT[d],
                "context": t[s:e][:120],
            })

records.sort(key=lambda x: x["item_id"])
for i, r in enumerate(records, 1):
    r["rep_id"] = f"REP-{i:05d}"

json.dump(records, open(os.path.join(ROOT, "_layers/reports.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print(f"REPORT 层：{len(records)} 条")
print("类别:", dict(Counter(r["doc_category"] for r in records)))
print("文书:", dict(Counter(r["doc_name"] for r in records).most_common(12)))
print("卷 Top8:", dict(Counter(r["volume"] for r in records).most_common(8)))
print("--- 抽样 ---")
for r in records[:12]:
    print(f"  [{r['item_id']}|{r['doc_category']}] {r['doc_name']} «{r['context'][:42]}»")
