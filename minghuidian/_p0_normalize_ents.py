# -*- coding: utf-8 -*-
"""P0-4 实体类型归一

问题：ents / _kg_join 的实体 type 用 institution / official / person_title 等
非规范值，与 schemas.md 的 ENT_TYPE 枚举（org/off/geo/doc/obj/era）不一致，
导致跨层无法按统一口径检索。

处理：
  - 把 `type` 归一为 schema 枚举值；
  - 原值保留到 `type_raw`（可溯源）；
  - 未识别值归入 `type_pending`，并登记到 _pending_enums.csv（走 V3 校准）。
"""
import json, os, csv

ROOT = os.path.dirname(os.path.abspath(__file__))
LAY = os.path.join(ROOT, "_layers")

TYPE_MAP = {
    # 衙门
    "institution": "org", "org": "org", "yamen": "org", "office_org": "org",
    # 官职
    "official": "off", "off": "off", "person_title": "off", "title": "off",
    "position": "off", "rank_title": "off",
    # 地名
    "geo": "geo", "place": "geo", "location": "geo",
    # 典籍
    "doc": "doc", "book": "doc", "classic": "doc",
    # 器物
    "obj": "obj", "object": "obj", "item": "obj",
    # 年号
    "era": "era", "reign": "era", "year": "era",
}
VALID = {"org", "off", "geo", "doc", "obj", "era", "type_pending"}

pending = {}


def norm_type(t):
    if t is None or t == "":
        return "type_pending"
    if t in VALID:
        return t
    if t in TYPE_MAP:
        return TYPE_MAP[t]
    pending[t] = pending.get(t, 0) + 1
    return "type_pending"


def norm_ents_list(lst):
    n = 0
    for ent in lst:
        if not isinstance(ent, dict):
            continue
        old = ent.get("type")
        new = norm_type(old)
        if old != new:
            ent["type_raw"] = old
            ent["type"] = new
            n += 1
    return n


def main():
    stats = {}
    # 1) ents.json
    p = os.path.join(LAY, "ents.json")
    d = json.load(open(p, encoding="utf-8"))
    stats["ents"] = norm_ents_list(d)
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # 2) _kg_join.json
    p = os.path.join(ROOT, "_kg_join.json")
    d = json.load(open(p, encoding="utf-8"))
    tot = 0
    for rec in d:
        tot += norm_ents_list(rec.get("ents", []))
    stats["_kg_join"] = tot
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print("归一化实体数:", stats)

    # 3) 登记未识别枚举
    if pending:
        with open(os.path.join(ROOT, "_pending_enums.csv"), "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f)
            w.writerow(["层名", "枚举字段", "未匹配值", "出现次数", "建议归类"])
            for k, v in sorted(pending.items(), key=lambda x: -x[1]):
                w.writerow(["L1实体", "type", k, v, "待人工决议"])
        print("未识别枚举 -> _pending_enums.csv:", pending)
    else:
        print("无未识别枚举。")

    # 复核
    import collections
    e = json.load(open(os.path.join(LAY, "ents.json"), encoding="utf-8"))
    print("ents type 分布:", collections.Counter(x.get("type") for x in e).most_common())


if __name__ == "__main__":
    main()
