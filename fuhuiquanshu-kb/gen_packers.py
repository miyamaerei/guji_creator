# -*- coding: utf-8 -*-
"""生成福惠 7 个层打包器（rule/struct/reg/opn/proc/doc/rel）。结构统一：枚举硬校验 → 段位 ID → original 注入。"""
import io
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

COMMON_HEAD = '''# -*- coding: utf-8 -*-
"""{layer} 打包：ID 分配 → 枚举硬校验（C5）→ original 注入 → _layers/{layer}/{layer}_NN.json。
用法：python build_{layer}.py --volumes 01,02   （幂等：段位固定）"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (ROOT, LAYER_DIR, alloc_id, load_enums, load_registry,
                           load_src, parse_volumes, write_json)

ENUMS = load_enums()
ID_KEY = "{id_key}"
SCHEMA_FIELDS = {schema}
LIST_DEFAULTS = {lists}
'''

BODY_ENUM = '''
GROUP, EV_FIELD = "{group}", "{ev_field}"
TYPES = set(ENUMS[GROUP + "_TYPES"])
def main():
    vols = parse_volumes(); registry = load_registry(); errors, gaps = [], []
    for vol in vols:
        recs = load_src(vol, "{layer}") or []; out = []
        for seq, r in enumerate(recs, 1):
            item_id = r.get("item_id"); ev = r.get(EV_FIELD)
            if item_id not in registry:
                gaps.append("[%s] item_id 不在指纹库: %s" % (vol, item_id)); continue
            if ev not in TYPES:
                errors.append("[%s] 未注册枚举值 %r (item=%s)" % (vol, ev, item_id)); continue
            rec = {{ID_KEY: alloc_id("{prefix}", vol, seq)}}
            for k in SCHEMA_FIELDS:
                if k in r: rec[k] = r[k]
            for _lk in LIST_DEFAULTS:
                if _lk not in rec and _lk in SCHEMA_FIELDS: rec[_lk] = []
            rec["original"] = registry[item_id]["original"]
            out.append(rec)
        write_json(os.path.join(LAYER_DIR, "{layer}", "{layer}_%s.json" % vol), {{"records": out}})
        print("卷%s {layer}打包完成：%d 条" % (vol, len(out)))
    with io.open(os.path.join(ROOT, "_build", "{layer}_errors.txt"), "w", encoding="utf-8") as f:
        f.write("\\n".join(["ERR: " + e for e in errors] + ["GAP: " + g for g in gaps]) or "OK")
    print("{layer}层 ERR=%d GAP=%d" % (len(errors), len(gaps)))
'''

BODY_NOENUM = '''
def main():
    vols = parse_volumes(); registry = load_registry(); errors, gaps = [], []
    for vol in vols:
        recs = load_src(vol, "{layer}") or []; out = []
        for seq, r in enumerate(recs, 1):
            item_id = r.get("item_id")
            if item_id not in registry:
                gaps.append("[%s] item_id 不在指纹库: %s" % (vol, item_id)); continue
            rec = {{ID_KEY: alloc_id("{prefix}", vol, seq)}}
            for k in SCHEMA_FIELDS:
                if k in r: rec[k] = r[k]
            for _lk in LIST_DEFAULTS:
                if _lk not in rec and _lk in SCHEMA_FIELDS: rec[_lk] = []
            rec["original"] = registry[item_id]["original"]
            out.append(rec)
        write_json(os.path.join(LAYER_DIR, "{layer}", "{layer}_%s.json" % vol), {{"records": out}})
        print("卷%s {layer}打包完成：%d 条" % (vol, len(out)))
    with io.open(os.path.join(ROOT, "_build", "{layer}_errors.txt"), "w", encoding="utf-8") as f:
        f.write("\\n".join(["ERR: " + e for e in errors] + ["GAP: " + g for g in gaps]) or "OK")
    print("{layer}层 ERR=%d GAP=%d" % (len(errors), len(gaps)))
'''

BODY_STRUCT = '''
DIMS = {{"ACT": "ACT_TYPES", "FRD": "FRD_TYPES", "LGR": "LGR_TYPES", "TME": "TME_TYPES"}}
TYPE_FIELD = {{"ACT": "act_type", "FRD": "frd_type", "LGR": "lgr_type", "TME": "tme_type"}}
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
            rec = {{ID_KEY: alloc_id(dim + "-", vol, seq), "dim": dim}}
            for k in SCHEMA_FIELDS:
                if k in r: rec[k] = r[k]
            for _lk in LIST_DEFAULTS:
                if _lk not in rec and _lk in SCHEMA_FIELDS: rec[_lk] = []
            rec["original"] = registry[item_id]["original"]
            out.append(rec)
        write_json(os.path.join(LAYER_DIR, "structs", "structs_%s.json" % vol), {{"records": out}})
        print("卷%s structs打包完成：%d 条" % (vol, len(out)))
    with io.open(os.path.join(ROOT, "_build", "structs_errors.txt"), "w", encoding="utf-8") as f:
        f.write("\\n".join(["ERR: " + e for e in errors] + ["GAP: " + g for g in gaps]) or "OK")
    print("structs层 ERR=%d GAP=%d" % (len(errors), len(gaps)))
'''

CONF = {
    "rules":  dict(id_key="rule_id", prefix="RULE-", layer="rules", group="RULE", ev_field="type",
                   schema="['rule_id','item_id','type','modals','condition','subject','subject_ent_ids','action','object','purpose','punishment','original','confidence']",
                   lists="['modals','subject_ent_ids']", enum=True),
    "structs":dict(id_key="struct_id", prefix="STRUCT-", layer="structs",
                   schema="['struct_id','item_id','dim','act_type','frd_type','lgr_type','tme_type','target','target_ent_ids','content','original','confidence']",
                   lists="['target_ent_ids']", enum=False, struct=True),
    "regs":   dict(id_key="reg_id", prefix="REG-", layer="regs", group="REG", ev_field="type",
                   schema="['reg_id','item_id','name','type','content','evolution','target','original','confidence']",
                   lists="[]", enum=True),
    "opns":   dict(id_key="opn_id", prefix="OPN-", layer="opns", group="OPN", ev_field="stance",
                   schema="['opn_id','item_id','topic','stance','argument','evidence_refs','original','confidence']",
                   lists="['evidence_refs']", enum=True),
    "procs":  dict(id_key="process_id", prefix="PROC-", layer="procs",
                   schema="['process_id','item_id','name','steps','state_machine','events','original','confidence']",
                   lists="[]", enum=False),
    "docs":   dict(id_key="doc_id", prefix="DOC-", layer="docs", group="DOC", ev_field="category",
                   schema="['doc_id','item_id','name','category','format','purpose','flow','related_item','original','confidence']",
                   lists="[]", enum=True),
    "rels":   dict(id_key="rel_id", prefix="REL-", layer="rels", group="REL", ev_field="relation_type",
                   schema="['rel_id','item_id','person_a','person_a_ent_ids','person_b','person_b_ent_ids','relation_type','direction','evidence','original','confidence']",
                   lists="['person_a_ent_ids','person_b_ent_ids']", enum=True),
}

TAIL = '''
if __name__ == "__main__":
    main()
'''

for layer, c in CONF.items():
    head = COMMON_HEAD.format(layer=c["layer"], id_key=c["id_key"], schema=c["schema"], lists=c["lists"])
    if c.get("struct"):
        body = BODY_STRUCT.format()
    elif c["enum"]:
        body = BODY_ENUM.format(layer=c["layer"], group=c["group"], ev_field=c["ev_field"], prefix=c["prefix"])
    else:
        body = BODY_NOENUM.format(layer=c["layer"], prefix=c["prefix"])
    with io.open(os.path.join(ROOT, "build_%s.py" % layer), "w", encoding="utf-8") as f:
        f.write(head + body + TAIL)
    print("生成 build_%s.py" % layer)
