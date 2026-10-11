# -*- coding: utf-8 -*-
"""
《新官轨范》实体主键表生成器 + 标注 ent_id 回填（kg-join P0-1 标准产出，可重跑）
- 从 新官轨范_实体归一_汇总.json 的 normalized_inventory 生成 ENT-001..N
- 回填各卷标注 JSON：按 (normalized, type) 匹配 inventory → ent_id
- 生成 alias_index：surface(text) → [ent_ids]（回填时统计）
- 用法：python build_ent_keys.py
"""
import os, re, json, glob

BASE = r"C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat"
ANN_DIR = os.path.join(BASE, "新官轨范_标注")
MERGE = os.path.join(BASE, "新官轨范_实体归一_汇总.json")
OUT = os.path.join(BASE, "新官轨范_实体_主键表.json")


def main():
    m = json.load(open(MERGE, encoding="utf-8"))
    inv = m["normalized_inventory"]
    # (normalized,type) -> ent_id
    key2ent = {}
    for i, it in enumerate(inv, 1):
        key2ent[(it["normalized"], it["type"])] = f"ENT-{i:03d}"
    for i, it in enumerate(inv, 1):
        it["ent_id"] = f"ENT-{i:03d}"

    alias_index = {}
    total_back = 0
    for f in sorted(glob.glob(os.path.join(ANN_DIR, "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        n = 0
        for e in d["entities"]:
            eid = key2ent.get((e["normalized"], e["type"]))
            if eid:
                e["ent_id"] = eid
                n += 1
                alias_index.setdefault(e["text"], set()).add(eid)
            else:
                e["ent_id"] = None
        total_back += n
        with open(f, "w", encoding="utf-8") as fo:
            json.dump(d, fo, ensure_ascii=False, indent=1)
        print(f"{os.path.basename(f)}: 回填 {n}/{len(d['entities'])}")

    alias_index = {k: sorted(v) for k, v in alias_index.items()}
    table = {
        "schema_version": "kg-entity-key-v1",
        "total": len(inv),
        "unique_entities": m.get("unique_entities"),
        "total_annotations": m.get("total_entities"),
        "alias_index_count": len(alias_index),
        "entity_types": m.get("by_type"),
        "entities": inv,
        "alias_index": alias_index,
    }
    with open(OUT, "w", encoding="utf-8") as fo:
        json.dump(table, fo, ensure_ascii=False, indent=1)
    print(f"\n主键表: {OUT}  total={len(inv)}  alias={len(alias_index)}  回填总条数={total_back}")


if __name__ == "__main__":
    main()
