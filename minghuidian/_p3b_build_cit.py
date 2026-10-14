# -*- coding: utf-8 -*-
"""P3-B1: 扩 L6.CIT 引用层（Q9 出处溯源）。

旧版仅 10 部书、每条目只取首个命中。新版：
  · 典籍词典扩至 30+ 部（律令/礼制/政书/地志/历法/经书 六类）；
  · 逐条目抽取**全部**命中典籍，并截取所在分句为 context；
  · 依「见/载/据/照/准/依」标记区分「援引」与「直引」。
"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
PUA = {0xE5AB: "隶", 0xEA1F: "弘", 0xF5F6: "封", 0xEB08: "卷"}


def nz(t):
    return "".join(PUA.get(ord(c), c) for c in t)


BOOKS = {
    "律令": ["大明律", "大明令", "御制大诰", "大诰", "问刑条例", "宪纲", "教民榜文",
             "至正条格", "皇明制书", "祖训录", "皇明祖训", "孝慈录", "风宪忠告"],
    "礼制": ["明集礼", "大明集礼", "洪武礼制", "礼仪定式", "稽古定制", "皇明典礼",
             "周礼", "礼记"],
    "政书": ["诸司职掌", "大明官制", "经世大典", "唐六典", "文献通考", "通典", "大明会典"],
    "地志": ["大明一统志", "寰宇通志", "洪武京城图志"],
    "历法": ["大明清类天文分野之书", "回回历法", "洪武正韵"],
    "经书": ["诗经", "易经", "论语", "孟子", "尔雅"],
}
# 长名优先，避免「大诰」抢先匹配「御制大诰」
ALL_BOOKS = sorted({b for v in BOOKS.values() for b in v}, key=len, reverse=True)
BOOK2CAT = {b: cat for cat, v in BOOKS.items() for b in v}

# 词内误切防护：书名后/前若为下列字符，则非该典籍（如「仪礼司」「大明律令」）
GUARD_NXT = {"仪礼": "司", "礼记": "记", "诗经": "云", "周礼": "司"}
GUARD_PRE = {"仪礼": "行", "礼记": "大"}

SPL = re.compile(r"[。；　]")
records = []
seen = set()
for k, v in sorted(reg.items()):
    t = nz(v.get("original") or "")
    for book in ALL_BOOKS:
        start = 0
        while True:
            i = t.find(book, start)
            if i < 0:
                break
            start = i + len(book)
            # 若被更长书名包含，跳过（如 大诰 ⊂ 御制大诰）
            longer = any(o != book and len(o) > len(book) and
                         t[max(0, i - len(o) + 1):i + len(book)] == o for o in ALL_BOOKS)
            if longer:
                continue
            nxt = t[i + len(book):i + len(book) + 1]
            prv = t[i - 1:i] if i > 0 else ""
            if nxt and nxt in GUARD_NXT.get(book, ""):
                continue
            if prv and prv in GUARD_PRE.get(book, ""):
                continue
            key = (k, book, i)
            if key in seen:
                continue
            seen.add(key)
            # 取所在分句作 context
            s = max((m.end() for m in SPL.finditer(t, 0, i)), default=0)
            e = SPL.search(t, i + len(book))
            e = e.start() if e else min(len(t), i + 40)
            ctx = t[s:e]
            pre = t[max(0, i - 2):i]
            ctype = "援引" if re.search(r"(见|载|据|照|准|依)$", pre) else "直引"
            records.append({
                "cit_id": "", "item_id": k, "volume": v.get("volume"),
                "cited_work": book, "work_category": BOOK2CAT[book],
                "citation_type": ctype, "context": ctx[:120],
            })

records.sort(key=lambda x: x["item_id"])
for i, r in enumerate(records, 1):
    r["cit_id"] = f"CIT-{i:04d}"

json.dump(records, open(os.path.join(ROOT, "_layers/cits.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

books = sorted({r["cited_work"] for r in records})
print(f"CIT 层：{len(records)} 条，覆盖 {len(books)} 部书")
print("分类:", dict(Counter(r["work_category"] for r in records)))
print("典籍:", dict(Counter(r["cited_work"] for r in records).most_common()))
print("类型:", dict(Counter(r["citation_type"] for r in records)))
print("--- 抽样 ---")
for r in records[:10]:
    print(f"  [{r['item_id']}] {r['cited_work']}({r['work_category']}/{r['citation_type']}) «{r['context'][:40]}»")
