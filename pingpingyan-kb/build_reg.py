# -*- coding: utf-8 -*-
"""制度层打包（REG）：ID 分配（REG- 段位）→ 枚举硬校验（C5）→ original 注入 → _layers/reg/reg_NN.json。
用法：python build_reg.py --volumes 01,02   （幂等：段位固定）"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (ROOT, LAYER_DIR, alloc_id, load_enums, load_registry,
                           load_src, parse_volumes, write_json)

ENUMS = load_enums()
REG_TYPES = set(ENUMS["REG_TYPES"])


def main():
    vols = parse_volumes()
    registry = load_registry()
    errors, gaps = [], []

    for vol in vols:
        recs = load_src(vol, "regs") or []   # _src/_regs_ai_NN.py（源键名复数，与家族惯例一致）
        out = []
        for seq, r in enumerate(recs, 1):
            item_id = r.get("item_id")
            rtype = r.get("type")
            if item_id not in registry:
                gaps.append("[%s] item_id 不在指纹库: %s" % (vol, item_id))
                continue
            if rtype not in REG_TYPES:
                errors.append("[%s] 未注册制度类型 %r (item=%s)" % (vol, rtype, item_id))
                continue
            out.append({
                "reg_id": alloc_id("REG-", vol, seq),
                "item_id": item_id,
                "name": r.get("name", ""),
                "type": rtype,
                "content": r.get("content", ""),
                "evolution": r.get("evolution", ""),
                "target": r.get("target", ""),
                "original": registry[item_id]["original"],
                "confidence": r.get("confidence", "high"),
            })
        write_json(os.path.join(LAYER_DIR, "reg", "reg_%s.json" % vol),
                   {"records": out})
        print("卷%s 制度打包完成：%d 条" % (vol, len(out)))

    with io.open(os.path.join(ROOT, "_build", "reg_errors.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(["ERR: " + e for e in errors] + ["GAP: " + g for g in gaps]) or "OK")
    print("制度层 ERR=%d GAP=%d" % (len(errors), len(gaps)))


if __name__ == "__main__":
    main()
