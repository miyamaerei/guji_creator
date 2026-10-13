# -*- coding: utf-8 -*-
"""事件层打包（L5）：ID 分配（EVT- 段位）→ 枚举硬校验（C5）→ original 注入 → _layers/evt/evt_NN.json。
用法：python build_events.py --volumes 01,02   （幂等：段位固定）"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (ROOT, LAYER_DIR, alloc_id, load_enums, load_registry,
                           load_src, parse_volumes, write_json)

ENUMS = load_enums()
EVENT_TYPES = set(ENUMS["EVENT_TYPES"])


def main():
    vols = parse_volumes()
    registry = load_registry()
    errors, gaps = [], []

    for vol in vols:
        recs = load_src(vol, "evt") or []
        out = []
        for seq, r in enumerate(recs, 1):
            item_id = r.get("item_id")
            rtype = r.get("type")
            if item_id not in registry:
                gaps.append("[%s] item_id 不在指纹库: %s" % (vol, item_id))
                continue
            if rtype not in EVENT_TYPES:
                errors.append("[%s] 未注册事件类型 %r (item=%s)" % (vol, rtype, item_id))
                continue
            out.append({
                "event_id": alloc_id("EVT-", vol, seq),
                "item_id": item_id,
                "type": rtype,
                "who": r.get("who", ""),
                "who_ent_ids": r.get("who_ent_ids", []),
                "action": r.get("action", ""),
                "what": r.get("what", ""),
                "when": r.get("when", ""),
                "where": r.get("where", ""),
                "original": registry[item_id]["original"],
                "confidence": r.get("confidence", "high"),
            })
        write_json(os.path.join(LAYER_DIR, "evt", "evt_%s.json" % vol),
                   {"records": out})
        print("卷%s 事件打包完成：%d 条" % (vol, len(out)))

    with io.open(os.path.join(ROOT, "_build", "evt_errors.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(["ERR: " + e for e in errors] + ["GAP: " + g for g in gaps]) or "OK")
    print("事件层 ERR=%d GAP=%d" % (len(errors), len(gaps)))


if __name__ == "__main__":
    main()
