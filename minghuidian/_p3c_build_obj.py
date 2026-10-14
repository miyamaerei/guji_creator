# -*- coding: utf-8 -*-
"""P3-C: 建 L5.OBJ 器物层（仪仗卤簿/车舆/军器/祭器/乐器/玺印/器用）。

以多字器物名为主（避免「旗/印/车」等单字词内误切），并设词内防护
（华盖殿、牺牲所、轿夫 等非器物用法）。服饰另见 dress.json，不重复。
"""
import json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
PUA = {0xE5AB: "隶", 0xEA1F: "弘", 0xF5F6: "封", 0xEB08: "卷"}


def nz(t):
    return "".join(PUA.get(ord(c), c) for c in t)


OBJ = {
    "仪仗卤簿": ["黄旗", "白旗", "青旗", "红旗", "黑旗", "龙旗", "日月旗", "门旗", "金节",
                 "仪锽", "豹尾", "龙扇", "黄盖", "华盖", "伞盖", "信幡", "绛引旛", "幢节",
                 "吾仗", "立瓜", "卧瓜", "骨朶", "镫杖", "班剑", "仪刀", "戟氅", "旄节"],
    "车舆": ["玉辂", "大辂", "金辂", "象辂", "革辂", "木辂", "步辇", "大马辇", "小马辇",
             "板轿", "鞍辔", "宝匣", "凉步辇"],
    "军器": ["铠甲", "盔甲", "弓矢", "弓弩", "神臂弓", "火铳", "铜铳", "铁炮", "佛郎机",
             "狼牙棒", "长枪", "腰刀", "鱼鳞甲", "明光甲", "蒺藜", "矛盾", "撒袋", "箭袋"],
    "祭器": ["玉圭", "苍璧", "笾豆", "簠簋", "牺牲", "登铏", "篚俎", "圭璧", "镇圭",
             "信圭", "躬圭", "谷璧", "蒲璧"],
    "乐器": ["编钟", "编磬", "琴瑟", "笙箫", "大鼓", "应鼓", "柷敔", "埙篪", "钟磬"],
    "玺印": ["宝玺", "玉玺", "御宝", "印信", "关防", "符验", "牌面"],
    "器用": ["铜器", "铁器", "漆器", "磁器", "瓷器", "木器", "器皿", "供器"],
}
ALL_OBJ = sorted({o for v in OBJ.values() for o in v}, key=len, reverse=True)
OBJ2CAT = {o: cat for cat, v in OBJ.items() for o in v}
# 词内防护
GUARD_NXT = {"华盖": "殿", "牺牲": "所", "轿": "夫", "铁器": "达", "大鼓": "吹"}
SPL = re.compile(r"[。；　]")

records = []
seen = set()
for k, v in sorted(reg.items()):
    t = nz(v.get("original") or "")
    for o in ALL_OBJ:
        start = 0
        while True:
            i = t.find(o, start)
            if i < 0:
                break
            start = i + len(o)
            nxt = t[i + len(o):i + len(o) + 1]
            if nxt and nxt in GUARD_NXT.get(o, ""):
                continue
            key = (k, o, i)
            if key in seen:
                continue
            seen.add(key)
            s = max((m.end() for m in SPL.finditer(t, 0, i)), default=0)
            e = SPL.search(t, i + len(o))
            e = e.start() if e else min(len(t), i + 40)
            records.append({
                "obj_id": "", "item_id": k, "volume": v.get("volume"),
                "obj_name": o, "obj_category": OBJ2CAT[o],
                "context": t[s:e][:120],
            })

records.sort(key=lambda x: x["item_id"])
for i, r in enumerate(records, 1):
    r["obj_id"] = f"OBJ-{i:04d}"

json.dump(records, open(os.path.join(ROOT, "_layers/objs.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print(f"OBJ 层：{len(records)} 条，{len({r['obj_name'] for r in records})} 种器物")
print("类别:", dict(Counter(r["obj_category"] for r in records)))
print("器物 Top12:", dict(Counter(r["obj_name"] for r in records).most_common(12)))
print("卷 Top8:", dict(Counter(r["volume"] for r in records).most_common(8)))
print("--- 抽样 ---")
for r in records[:12]:
    print(f"  [{r['item_id']}|{r['obj_category']}] {r['obj_name']} «{r['context'][:40]}»")
