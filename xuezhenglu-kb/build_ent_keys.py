# -*- coding: utf-8 -*-
"""实体层打包（L1）：归一 → 主键表（先查后建）→ ID 分配 → original 注入 → _layers/ent/ent_NN.json。
用法：python build_ent_keys.py --volumes 01,02   （幂等：同名实体复用主键）"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (ROOT, GLOBAL_DIR, LAYER_DIR, alloc_id, find_span,
                           load_enums, load_registry, load_src, parse_volumes,
                           read_json, write_json)

ENUMS = load_enums()
ENTITY_TYPES = set(ENUMS["ENTITY_TYPES"])
ALIASES = ENUMS.get("ENTITY_ALIASES", {})
KEYS_PATH = os.path.join(GLOBAL_DIR, "ent_keys.json")
ALIAS_PATH = os.path.join(GLOBAL_DIR, "alias_index.json")


def main():
    vols = parse_volumes()
    registry = load_registry()
    ent_keys = read_json(KEYS_PATH, {})       # normalized -> ent_id
    alias_index = read_json(ALIAS_PATH, {})   # text(原文词形) -> normalized
    errors, gaps = [], []
    next_seq = len(ent_keys) + 1

    for vol in vols:
        recs = load_src(vol, "ents") or []
        out = []
        for r in recs:
            item_id = r.get("item_id")
            text = r.get("text", "").strip()
            raw_type = r.get("type", "unknown")
            if item_id not in registry:
                gaps.append("[%s] item_id 不在指纹库: %s" % (vol, item_id))
                continue
            if raw_type not in ENTITY_TYPES:
                errors.append("[%s] 未注册实体类型 %r (item=%s text=%s)" % (vol, raw_type, item_id, text))
                continue
            original = registry[item_id]["original"]
            span = find_span(original, text)
            if span is None:
                gaps.append("[%s] text 未在原文命中: item=%s text=%s" % (vol, item_id, text))
                span = {"start": -1, "end": -1}
            normalized = (alias_index.get(text) or r.get("normalized") or text)
            if normalized not in ent_keys:
                ent_keys[normalized] = "ENT-%04d" % next_seq
                alias_index[text] = normalized
                next_seq += 1
            out.append({
                "ent_id": ent_keys[normalized],
                "item_id": item_id,
                "text": text,
                "type": raw_type,
                "start": span["start"], "end": span["end"],
                "normalized": normalized,
                "confidence": r.get("confidence", "high"),
                "source": item_id,
                "original": original,
            })
        write_json(os.path.join(LAYER_DIR, "ent", "ent_%s.json" % vol),
                   {"records": out})
        print("卷%s 实体打包完成：%d 条（ENT 全局已 %d）" % (vol, len(out), len(ent_keys)))

    write_json(KEYS_PATH, ent_keys)
    write_json(ALIAS_PATH, alias_index)
    with io.open(os.path.join(ROOT, "_build", "ent_errors.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(["ERR: " + e for e in errors] + ["GAP: " + g for g in gaps]) or "OK")
    print("实体层 ERR=%d GAP=%d" % (len(errors), len(gaps)))


if __name__ == "__main__":
    main()
