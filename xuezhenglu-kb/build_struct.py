# -*- coding: utf-8 -*-
"""结构化层打包（L4 四维）：dim → 维度前缀 ID（ACT-/FRD-/LGR-/TME- 段位）→ 枚举硬校验（C5）→ original 注入。
用法：python build_struct.py --volumes 01,02   （幂等：段位固定）"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (DIM_PREFIX, DIM_TYPE_FIELD, ROOT, LAYER_DIR, alloc_id,
                           load_enums, load_registry, load_src, parse_volumes, write_json)

ENUMS = load_enums()
DIMS = set(ENUMS["STRUCT_DIMS"])
TYPE_FIELDS = {dim: ENUMS[dim + "_TYPES"] for dim in ["ACT", "FRD", "LGR", "TME"]}


def main():
    vols = parse_volumes()
    registry = load_registry()
    errors, gaps = [], []

    for vol in vols:
        recs = load_src(vol, "struct") or []   # _src/_struct_ai_NN.py（与 schemas.md §7.1 一致）
        out = []
        for seq, r in enumerate(recs, 1):
            item_id = r.get("item_id")
            dim = r.get("dim")
            if item_id not in registry:
                gaps.append("[%s] item_id 不在指纹库: %s" % (vol, item_id))
                continue
            if dim not in DIMS:
                errors.append("[%s] 未注册维度 %r (item=%s)" % (vol, dim, item_id))
                continue
            type_field = DIM_TYPE_FIELD[dim]
            tval = r.get(type_field)
            if tval not in TYPE_FIELDS[dim]:
                errors.append("[%s] 未注册 %s 类型 %r (item=%s)" % (vol, type_field, tval, item_id))
                continue
            rec = {
                "struct_id": alloc_id(DIM_PREFIX[dim], vol, seq),
                "item_id": item_id,
                "dim": dim,
                type_field: tval,
                "target": r.get("target", ""),
                "evidence": r.get("evidence", ""),
                "original": registry[item_id]["original"],
                "confidence": r.get("confidence", "high"),
            }
            # 维度专属字段透传（act/frd/lgr/tme 的 detail 字段）
            for k, v in r.items():
                if k not in rec and k not in ("slot", "item_id", "dim", type_field,
                                              "target", "evidence", "confidence"):
                    rec[k] = v
            out.append(rec)
        write_json(os.path.join(LAYER_DIR, "struct", "struct_%s.json" % vol),
                   {"records": out})
        print("卷%s 结构化打包完成：%d 条" % (vol, len(out)))

    with io.open(os.path.join(ROOT, "_build", "struct_errors.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(["ERR: " + e for e in errors] + ["GAP: " + g for g in gaps]) or "OK")
    print("结构化层 ERR=%d GAP=%d" % (len(errors), len(gaps)))


if __name__ == "__main__":
    main()
