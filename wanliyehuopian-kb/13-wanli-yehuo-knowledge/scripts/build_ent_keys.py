# -*- coding: utf-8 -*-
"""全局实体主键表（跨卷归一，非破坏式）。

现状：34 卷 ents 已带卷内分配好的 ENT ID（卷×100 段位），跨卷同实体各有独立 ID。
本脚本不改写既有 ID，而是建立归一层：
  _global/ent_keys.json   normalized -> {primary, occurrences, type, text_variants}
                          primary = 最早卷次的 ENT ID（item_id 卷序最小者）
  _global/alias_index.json text(原文词形) -> normalized

下游（build_kg_join / views）以 primary 作为跨卷聚合主键。
幂等：重跑结果一致。用法：python scripts/build_ent_keys.py
"""
import io
import json
import os
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTS_DIR = os.path.join(BASE, "_layers", "ents")
GLOBAL_DIR = os.path.join(BASE, "_global")


def load_layer_array(path):
    """兼容两种落盘格式：顶层数组 与 {"records": [...]}"""
    with io.open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d["records"] if isinstance(d, dict) else d


def main():
    os.makedirs(GLOBAL_DIR, exist_ok=True)
    groups = defaultdict(list)  # normalized -> [ (item_id, ent_id, text, type) ]
    alias = {}
    total = 0
    for fn in sorted(os.listdir(ENTS_DIR)):
        if not fn.endswith(".json"):
            continue
        for r in load_layer_array(os.path.join(ENTS_DIR, fn)):
            total += 1
            norm = (r.get("normalized") or r.get("text") or "").strip()
            if not norm or not r.get("ent_id"):
                continue
            groups[norm].append((r["item_id"], r["ent_id"], r.get("text", norm), r.get("type", "unknown")))
            alias.setdefault(r.get("text", norm), norm)

    ent_keys = {}
    dup_clusters = 0
    for norm, occ in groups.items():
        occ_sorted = sorted(occ)  # 按 (item_id, ent_id) —— 最早卷次的记录成为主键
        primary = occ_sorted[0][1]
        if len(occ_sorted) > 1:
            dup_clusters += 1
        ent_keys[norm] = {
            "primary": primary,
            "type": occ_sorted[0][3],
            "occurrences": [{"item_id": a, "ent_id": b} for a, b, _, _ in occ_sorted],
            "text_variants": sorted(set(t for _, _, t, _ in occ)),
        }

    with io.open(os.path.join(GLOBAL_DIR, "ent_keys.json"), "w", encoding="utf-8") as f:
        json.dump({"entities": ent_keys, "total": len(ent_keys)}, f, ensure_ascii=False, indent=2)
    with io.open(os.path.join(GLOBAL_DIR, "alias_index.json"), "w", encoding="utf-8") as f:
        json.dump(alias, f, ensure_ascii=False, indent=2)

    print("ents 记录总数: %d" % total)
    print("归一实体数: %d（跨卷复用主键的簇: %d）" % (len(ent_keys), dup_clusters))
    print("_global/ent_keys.json + alias_index.json 已写出")


if __name__ == "__main__":
    main()
