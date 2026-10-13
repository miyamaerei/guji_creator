# -*- coding: utf-8 -*-
"""事件层打包：ID 分配（EVT-段位）→ 枚举硬校验（C5）→ original 注入 → _layers/evt/evt_NN.json。
用法：python build_events.py --volumes 01,02   （幂等：段位固定）"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (ROOT, LAYER_DIR, alloc_id, load_enums, load_registry,
                           load_src, parse_volumes, write_json)

ENUMS = load_enums()
GROUP = "EVENT"
TYPES = set(ENUMS[GROUP + "_TYPES"])
ID_KEY = "event_id"
SCHEMA_FIELDS = ['event_id', 'item_id', 'type', 'who', 'who_ent_ids', 'action', 'what', 'when', 'where', 'original', 'confidence']
LIST_DEFAULTS = ["person_ent_ids", "official_ent_ids", "institution_ent_ids",
                 "who_ent_ids", "author_ent_ids", "ent_ids", "evidence_refs"]


def main():
    vols = parse_volumes()
    registry = load_registry()
    errors, gaps = [], []

    for vol in vols:
        recs = load_src(vol, "evt") or []
        out = []
        for seq, r in enumerate(recs, 1):
            item_id = r.get("item_id")
            enum_val = r.get("type")
            if item_id not in registry:
                gaps.append("[%s] item_id 不在指纹库: %s" % (vol, item_id))
                continue
            if enum_val not in TYPES:
                errors.append("[%s] 未注册枚举值 %r (item=%s)" % (vol, enum_val, item_id))
                continue
            rec = dict()
            rec[ID_KEY] = alloc_id("EVT-", vol, seq)
            for k in SCHEMA_FIELDS:
                if k in r:
                    rec[k] = r[k]
            for _lk in LIST_DEFAULTS:
                if _lk not in rec and _lk in SCHEMA_FIELDS:
                    rec[_lk] = []
            rec["original"] = registry[item_id]["original"]
            out.append(rec)
        write_json(os.path.join(LAYER_DIR, "evt", "evt_%s.json" % vol),
                   {"records": out})
        print("卷%s evt打包完成：%d 条" % (vol, len(out)))

    with io.open(os.path.join(ROOT, "_build", "evt_errors.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(["ERR: " + e for e in errors] + ["GAP: " + g for g in gaps]) or "OK")
    print("evt层 ERR=%d GAP=%d" % (len(errors), len(gaps)))


if __name__ == "__main__":
    main()
