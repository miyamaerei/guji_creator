# -*- coding: utf-8 -*-
"""P0-5 把底座重建产生的 ID 变动（_id_map.json）同步到全部下游层。

底座 v2 重建后，有 329 个旧 item_id 被重新指派（卷33/122/129/130 的边界修正）。
本脚本把这些旧 ID 在所有下游层中的引用改写到新 ID，避免悬空引用。
"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
LAY = os.path.join(ROOT, "_layers")
id_map = json.load(open(os.path.join(ROOT, "_id_map.json"), encoding="utf-8"))
print("ID 映射条目:", len(id_map))

total = 0


def remap_item(rec):
    global total
    n = 0
    if isinstance(rec, dict):
        v = rec.get("item_id")
        if isinstance(v, str) and v in id_map:
            rec["item_id"] = id_map[v]
            rec["item_id_prev"] = v
            n += 1
        si = rec.get("source_items")
        if isinstance(si, list):
            new = [id_map.get(x, x) for x in si]
            if new != si:
                rec["source_items"] = new
                n += len([1 for a, b in zip(si, new) if a != b])
    total += n
    return n


# 1) 各层
for f in sorted(os.listdir(LAY)):
    if not f.endswith(".json"):
        continue
    p = os.path.join(LAY, f)
    d = json.load(open(p, encoding="utf-8"))
    if not isinstance(d, list):
        continue
    c = sum(remap_item(r) for r in d)
    if c:
        json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("  %-22s 改写 %d 处" % (f, c))

# 2) _kg_join
p = os.path.join(ROOT, "_kg_join.json")
d = json.load(open(p, encoding="utf-8"))
c = sum(remap_item(r) for r in d)
if c:
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("  %-22s 改写 %d 处" % ("_kg_join.json", c))

print("合计改写:", total)

# 3) 校验：下游 item_id 是否都能在底座中找到
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))
keys = set(reg)
bad = {}
for f in sorted(os.listdir(LAY)):
    if not f.endswith(".json"):
        continue
    d = json.load(open(os.path.join(LAY, f), encoding="utf-8"))
    if not isinstance(d, list):
        continue
    miss = sum(1 for r in d if isinstance(r, dict) and r.get("item_id") and r["item_id"] not in keys)
    if miss:
        bad[f] = miss
print("悬空 item_id 层:", bad if bad else "无")
