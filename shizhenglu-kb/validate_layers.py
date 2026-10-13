# -*- coding: utf-8 -*-
"""校验器（验收闸门）：C5 枚举 / C6 字段完整 / C3 original 注入 / 引用槽位 / item_id 全回填。
用法：python validate_layers.py [--skip-baseline]（部分装填阶段用 --skip-baseline 跳过全量回填检查）
退出码：0=通过；1=有 ERR 或 GAP。输出 _validate/验证缺漏清单.txt"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _kg_pack_base import (DIM_PREFIX, DIM_TYPE_FIELD, ROOT, LAYER_DIR, load_enums,
                           load_registry, read_json)

ENUMS = load_enums()
ERR, GAP = [], []


# 各层"存在即可"字段（语义允许空值，只查存在性）；其余必填字段查非空
PRESENT_OK = {
    "ent": {"original"},
    "rule": {"modals", "condition", "subject_ent_ids", "object", "purpose", "punishment", "original"},
    "struct": {"target", "evidence", "original"},
}
NOT_EMPTY = {
    "ent": {"ent_id", "item_id", "text", "type", "start", "end", "normalized", "confidence", "source"},
    "rule": {"rule_id", "item_id", "type", "subject", "action", "confidence"},
    "struct": {"struct_id", "item_id", "dim", "confidence"},
}


def check_fields(layer, rec):
    for f in NOT_EMPTY[layer]:
        if f not in rec or rec[f] in ("", [], None):
            ERR.append("[%s] 缺必填字段 %s (record=%s)" % (layer, f, rec.get("id", rec.get("item_id"))))
    for f in PRESENT_OK[layer]:
        if f not in rec:
            ERR.append("[%s] 缺字段 %s (record=%s)" % (layer, f, rec.get("id", rec.get("item_id"))))


def layer_files(layer, prefix):
    d = os.path.join(LAYER_DIR, layer)
    if not os.path.isdir(d):
        return []
    out = []
    for f in sorted(os.listdir(d)):
        if f.startswith(prefix) and f.endswith(".json"):
            vol = f[len(prefix):-5]
            if vol.isdigit() and len(vol) == 2:  # 只认 NN 两位卷名
                out.append(f)
    return out


def main():
    registry = load_registry()
    skip_baseline = "--skip-baseline" in sys.argv

    # ent
    for f in layer_files("ent", "ent_"):
        vol = f[4:-5]
        data = read_json(os.path.join(LAYER_DIR, "ent", f), {"records": []})
        for r in data["records"]:
            check_fields("ent", r)
            if r["type"] not in ENUMS["ENTITY_TYPES"]:
                ERR.append("[ent] 未注册实体类型 %r (%s)" % (r["type"], r["ent_id"]))
            if r["item_id"] not in registry:
                GAP.append("[ent] item_id 不在指纹库: %s" % r["ent_id"])
            if r["original"] != registry.get(r["item_id"], {}).get("original"):
                ERR.append("[ent] original 与指纹库不一致: %s" % r["ent_id"])
        print("ent 卷%s：%d 条" % (vol, len(data["records"])))

    # rule
    for f in layer_files("rule", "rule_"):
        vol = f[5:-5]
        data = read_json(os.path.join(LAYER_DIR, "rule", f), {"records": []})
        for r in data["records"]:
            check_fields("rule", r)
            if r["type"] not in ENUMS["RULE_TYPES"]:
                ERR.append("[rule] 未注册规则类型 %r (%s)" % (r["type"], r["rule_id"]))
            if r["item_id"] not in registry:
                GAP.append("[rule] item_id 不在指纹库: %s" % r["rule_id"])
            if r["original"] != registry.get(r["item_id"], {}).get("original"):
                ERR.append("[rule] original 与指纹库不一致: %s" % r["rule_id"])
        print("rule 卷%s：%d 条" % (vol, len(data["records"])))

    # struct（含维度类型 + target 引用检查）
    all_ids = set()
    for f in layer_files("struct", "struct_"):
        vol = f[7:-5]
        data = read_json(os.path.join(LAYER_DIR, "struct", f), {"records": []})
        for r in data["records"]:
            check_fields("struct", r)
            dim = r["dim"]
            tf = DIM_TYPE_FIELD.get(dim)
            if dim not in ENUMS["STRUCT_DIMS"]:
                ERR.append("[struct] 未注册维度 %r (%s)" % (dim, r["struct_id"]))
            elif r.get(tf) not in ENUMS.get(dim + "_TYPES", []):
                ERR.append("[struct] 未注册 %s 类型 %r (%s)" % (tf, r.get(tf), r["struct_id"]))
            if r["item_id"] not in registry:
                GAP.append("[struct] item_id 不在指纹库: %s" % r["struct_id"])
            if r["original"] != registry.get(r["item_id"], {}).get("original"):
                ERR.append("[struct] original 与指纹库不一致: %s" % r["struct_id"])
            t = r.get("target", "")
            if t and not (t.startswith(tuple(DIM_PREFIX.values())) or t.startswith("ENT-")):
                ERR.append("[struct] target 引用格式非法: %s -> %s" % (r["struct_id"], t))
            if t:
                all_ids.add((r["item_id"], t))
        print("struct 卷%s：%d 条" % (vol, len(data["records"])))

    # 悬空引用（target 必须存在于已打包记录或实体主键）
    if all_ids:
        ent_keys = read_json(os.path.join(ROOT, "_global", "ent_keys.json"), {})
        known = set(ent_keys.values())
        for f in layer_files("struct", "struct_"):
            for r in read_json(os.path.join(LAYER_DIR, "struct", f), {"records": []})["records"]:
                known.add(r["struct_id"])
        for item_id, t in all_ids:
            if t not in known:
                GAP.append("[struct] 悬空 target %s (item=%s)" % (t, item_id))

    # item_id 全回填（缺省全量检查；--skip-baseline 时只查已打包卷）
    if not skip_baseline:
        join = read_json(os.path.join(ROOT, "_kg_join.json"), {"records": []})
        joined = {r["item_id"] for r in join["records"]}
        missing = sorted(set(registry) - joined)
        if missing:
            GAP.append("item_id 未回填到 _kg_join: %s（%d 个）" % (",".join(missing), len(missing)))

    # 报告
    lines = []
    lines.append("验证缺漏清单（ERR=%d / GAP=%d）" % (len(ERR), len(GAP)))
    for e in ERR:
        lines.append("ERR: " + e)
    for g in GAP:
        lines.append("GAP: " + g)
    if not ERR and not GAP:
        lines.append("全部通过 ✓")
    os.makedirs(os.path.join(ROOT, "_validate"), exist_ok=True)
    with io.open(os.path.join(ROOT, "_validate", "验证缺漏清单.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))
    sys.exit(0 if (not ERR and not GAP) else 1)


if __name__ == "__main__":
    main()
