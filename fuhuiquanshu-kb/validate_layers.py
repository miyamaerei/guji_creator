# -*- coding: utf-8 -*-
"""校验器（验收闸门）：C5 枚举 / C6 字段完整 / C3 original 注入 / 引用槽位 / item_id 全回填。
层：ent/rule/struct/reg/opn/proc/doc/rel（8 层）。
用法：python validate_layers.py [--skip-baseline]
退出码：0=通过；1=有 ERR 或 GAP。输出 _validate/验证缺漏清单.txt"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (ROOT, LAYER_DIR, LAYER_ENUM_GROUP, load_enums,
                           load_registry, read_json)

ENUMS = load_enums()
ERR, GAP = [], []

PRESENT_OK = {
    "ent": {"original"},
    "rule": {"modals", "subject_ent_ids", "purpose", "punishment", "original"},
    "struct": {"target_ent_ids", "original"},
    "reg": {"evolution", "target", "original"},
    "opn": {"evidence_refs", "original"},
    "proc": {"state_machine", "events", "original"},
    "doc": {"related_item", "original"},
    "rel": {"person_a_ent_ids", "person_b_ent_ids", "evidence", "original"},
}
NOT_EMPTY = {
    "ent": {"ent_id", "item_id", "text", "type", "start", "end", "normalized", "confidence", "source"},
    "rule": {"rule_id", "item_id", "type", "condition", "subject", "action", "object", "confidence"},
    "struct": {"struct_id", "item_id", "dim", "content", "confidence"},
    "reg": {"reg_id", "item_id", "name", "type", "content", "confidence"},
    "opn": {"opn_id", "item_id", "topic", "stance", "argument", "confidence"},
    "proc": {"process_id", "item_id", "name", "steps", "confidence"},
    "doc": {"doc_id", "item_id", "name", "category", "confidence"},
    "rel": {"rel_id", "item_id", "person_a", "person_b", "relation_type", "direction", "confidence"},
}
# struct 维度类型字段（按 dim 必填且命中枚举）
STRUCT_TYPE_FIELD = {"ACT": "act_type", "FRD": "frd_type", "LGR": "lgr_type", "TME": "tme_type"}
STRUCT_TYPE_GROUP = {"ACT": "ACT", "FRD": "FRD", "LGR": "LGR", "TME": "TME"}
ENUM_FIELD = {
    "ent": "type", "rule": "type", "reg": "type", "opn": "stance",
    "doc": "category", "rel": "relation_type",
}
ID_KEY = {
    "ent": "ent_id", "rule": "rule_id", "struct": "struct_id", "reg": "reg_id",
    "opn": "opn_id", "proc": "process_id", "doc": "doc_id", "rel": "rel_id",
    "structs": "struct_id", "rules": "rule_id", "regs": "reg_id", "opns": "opn_id",
    "procs": "process_id", "docs": "doc_id", "rels": "rel_id",
}


def check_fields(layer, rec):
    for f in NOT_EMPTY[layer]:
        if f not in rec or rec[f] in ("", [], None):
            ERR.append("[%s] 缺必填字段 %s (record=%s)" % (layer, f, rec.get("item_id")))
    for f in PRESENT_OK[layer]:
        if f not in rec:
            ERR.append("[%s] 缺字段 %s (record=%s)" % (layer, f, rec.get("item_id")))


def layer_files(layer, prefix):
    d = os.path.join(LAYER_DIR, layer)
    if not os.path.isdir(d):
        return []
    out = []
    for f in sorted(os.listdir(d)):
        if f.startswith(prefix) and f.endswith(".json"):
            vol = f[len(prefix):-5]
            if vol.isdigit() and len(vol) == 2:
                out.append(f)
    return out


def main():
    registry = load_registry()
    skip_baseline = "--skip-baseline" in sys.argv

    for layer, group in LAYER_ENUM_GROUP.items():
        enums = set(ENUMS.get(group + "_TYPES", []))
        for f in layer_files(layer, layer + "_"):
            vol = f[len(layer) + 1:-5]
            data = read_json(os.path.join(LAYER_DIR, layer, f), {"records": []})
            for r in data["records"]:
                check_fields(layer, r)
                ev = ENUM_FIELD.get(layer)
                if ev and r.get(ev) not in enums:
                    ERR.append("[%s] 未注册枚举值 %r (%s)" % (layer, r.get(ev), r[ID_KEY[layer]]))
                if r["item_id"] not in registry:
                    GAP.append("[%s] item_id 不在指纹库: %s" % (layer, r[ID_KEY[layer]]))
                if r.get("original") != registry.get(r["item_id"], {}).get("original"):
                    ERR.append("[%s] original 与指纹库不一致: %s" % (layer, r[ID_KEY[layer]]))
            print("%s 卷%s：%d 条" % (layer, vol, len(data["records"])))

    # struct 四维特殊校验
    for f in layer_files("structs", "structs_"):
        data = read_json(os.path.join(LAYER_DIR, "structs", f), {"records": []})
        for r in data["records"]:
            dim = r.get("dim")
            if dim not in STRUCT_TYPE_FIELD:
                ERR.append("[structs] 未注册 dim %r (%s)" % (r.get("dim"), r.get("struct_id")))
                continue
            tf = STRUCT_TYPE_FIELD[dim]
            tv = r.get(tf)
            if tv not in set(ENUMS[STRUCT_TYPE_GROUP[dim] + "_TYPES"]):
                ERR.append("[structs] %s 未注册 %s=%r (%s)" % (dim, tf, tv, r.get("struct_id")))

    # 悬空引用（reg.target / opn.evidence_refs / proc.events / doc.related_item / rel ent 槽）
    ent_keys = read_json(os.path.join(ROOT, "_global", "ent_keys.json"), {})
    known = set(ent_keys.values())
    for layer in ("reg", "opn", "proc", "doc", "rel", "structs"):
        for f in layer_files(layer, layer + "_"):
            for r in read_json(os.path.join(LAYER_DIR, layer, f), {"records": []})["records"]:
                known.add(r.get(ID_KEY[layer], ""))
    for f in layer_files("reg", "regs_"):
        for r in read_json(os.path.join(LAYER_DIR, "regs", f), {"records": []})["records"]:
            t = r.get("target", "")
            if t and t not in known:
                GAP.append("[regs] 悬空 target %s (item=%s)" % (t, r["item_id"]))
    for f in layer_files("opn", "opns_"):
        for r in read_json(os.path.join(LAYER_DIR, "opns", f), {"records": []})["records"]:
            for t in r.get("evidence_refs", []):
                if t and t not in known:
                    GAP.append("[opns] 悬空 evidence_ref %s (item=%s)" % (t, r["item_id"]))
    for f in layer_files("procs", "procs_"):
        for r in read_json(os.path.join(LAYER_DIR, "procs", f), {"records": []})["records"]:
            for t in r.get("events", []) or []:
                if t and t not in known:
                    GAP.append("[procs] 悬空 events 引用 %s (item=%s)" % (t, r["item_id"]))
    for f in layer_files("docs", "docs_"):
        for r in read_json(os.path.join(LAYER_DIR, "docs", f), {"records": []})["records"]:
            t = r.get("related_item", "")
            if t and t not in registry:
                GAP.append("[docs] 悬空 related_item %s (doc=%s)" % (t, r["doc_id"]))
    for f in layer_files("rels", "rels_"):
        for r in read_json(os.path.join(LAYER_DIR, "rels", f), {"records": []})["records"]:
            for slot in ("person_a_ent_ids", "person_b_ent_ids"):
                for t in r.get(slot, []):
                    if t and t not in known:
                        GAP.append("[rels] 悬空 %s %s (item=%s)" % (slot, t, r["item_id"]))

    if not skip_baseline:
        join = read_json(os.path.join(ROOT, "_kg_join.json"), {"records": []})
        joined = {r["item_id"] for r in join["records"]}
        missing = sorted(set(registry) - joined)
        if missing:
            GAP.append("item_id 未回填到 _kg_join: %s（%d 个）" % (",".join(missing), len(missing)))

    lines = ["验证缺漏清单（ERR=%d / GAP=%d）" % (len(ERR), len(GAP))]
    lines += ["ERR: " + e for e in ERR]
    lines += ["GAP: " + g for g in GAP]
    if not ERR and not GAP:
        lines.append("全部通过 ✓")
    os.makedirs(os.path.join(ROOT, "_validate"), exist_ok=True)
    with io.open(os.path.join(ROOT, "_validate", "验证缺漏清单.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))
    sys.exit(0 if (not ERR and not GAP) else 1)


if __name__ == "__main__":
    main()
