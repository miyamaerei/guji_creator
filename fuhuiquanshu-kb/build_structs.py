# -*- coding: utf-8 -*-
"""structs 打包：ID 分配 → 枚举硬校验（C5）→ original 注入 → _layers/structs/structs_NN.json。
用法：python build_structs.py --volumes 01,02   （幂等：段位固定）"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (ROOT, LAYER_DIR, alloc_id, load_enums, load_registry,
                           load_src, parse_volumes, write_json)

ENUMS = load_enums()
ID_KEY = "struct_id"
SCHEMA_FIELDS = ['struct_id','item_id','dim','act_type','frd_type','lgr_type','tme_type','target','target_ent_ids','content','original','confidence']
LIST_DEFAULTS = ['target_ent_ids']

DIMS = {"ACT": "ACT_TYPES", "FRD": "FRD_TYPES", "LGR": "LGR_TYPES", "TME": "TME_TYPES"}
TYPE_FIELD = {"ACT": "act_type", "FRD": "frd_type", "LGR": "lgr_type", "TME": "tme_type"}
def main():
    vols = parse_volumes(); registry = load_registry(); errors, gaps = [], []
    for vol in vols:
        recs = load_src(vol, "structs") or []; out = []
        for seq, r in enumerate(recs, 1):
            item_id = r.get("item_id"); dim = r.get("dim")
            if item_id not in registry:
                gaps.append("[%s] item_id 不在指纹库: %s" % (vol, item_id)); continue
            if dim not in DIMS:
                errors.append("[%s] 未注册 dim %r (item=%s)" % (vol, dim, item_id)); continue
            tf = TYPE_FIELD[dim]; tv = r.get(tf)
            if tv not in set(ENUMS[DIMS[dim]]):
                errors.append("[%s] %s 未注册 %s=%r (item=%s)" % (vol, dim, tf, tv, item_id)); continue
            rec = {ID_KEY: alloc_id(dim + "-", vol, seq), "dim": dim}
            for k in SCHEMA_FIELDS:
                if k in r: rec[k] = r[k]
            for _lk in LIST_DEFAULTS:
                if _lk not in rec and _lk in SCHEMA_FIELDS: rec[_lk] = []
            rec["original"] = registry[item_id]["original"]
            out.append(rec)
        write_json(os.path.join(LAYER_DIR, "structs", "structs_%s.json" % vol), {"records": out})
        print("卷%s structs打包完成：%d 条" % (vol, len(out)))
    with io.open(os.path.join(ROOT, "_build", "structs_errors.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(["ERR: " + e for e in errors] + ["GAP: " + g for g in gaps]) or "OK")
    print("structs层 ERR=%d GAP=%d" % (len(errors), len(gaps)))

if __name__ == "__main__":
    main()
