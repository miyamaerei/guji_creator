# -*- coding: utf-8 -*-
"""校验器（验收闸门）：C5 枚举 / C6 字段完整 / C3 original 注入 / 引用槽位 / item_id 全回填 / TRL 翻译覆盖。
用法：python validate_layers.py [--skip-baseline]（部分装填阶段用 --skip-baseline 跳过全量回填检查）
退出码：0=通过；1=有 ERR 或 GAP。输出 _validate/验证缺漏清单.txt"""
import io
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
    "reg": {"content", "evolution", "target", "original"},
    "opn": {"argument", "evidence_refs", "original"},
    "trl": {"original", "norm", "note"},
}
NOT_EMPTY = {
    "ent": {"ent_id", "item_id", "text", "type", "start", "end", "normalized", "confidence", "source"},
    "rule": {"rule_id", "item_id", "type", "subject", "action", "confidence"},
    "struct": {"struct_id", "item_id", "dim", "confidence"},
    "reg": {"reg_id", "item_id", "name", "type", "confidence"},
    "opn": {"opn_id", "item_id", "topic", "stance", "confidence"},
    "trl": {"trl_id", "item_id", "translation", "style", "confidence"},
}
ENUM_FIELD = {
    "ent": ("ENTITY_TYPES", "type"),
    "rule": ("RULE_TYPES", "type"),
    "reg": ("REG_TYPES", "type"),
    "opn": ("OPN_STANCES", "stance"),
    "trl": ("TRL_STYLES", "style"),
}


def check_fields(layer, rec):
    for f in NOT_EMPTY[layer]:
        if f not in rec or rec[f] in ("", [], None):
            ERR.append("[%s] 缺必填字段 %s (record=%s)" % (layer, f, rec.get("id", rec.get("item_id"))))
    for f in PRESENT_OK[layer]:
        if f not in rec:
            ERR.append("[%s] 缺字段 %s (record=%s)" % (layer, f, rec.get("id", rec.get("item_id"))))
    if layer in ENUM_FIELD:
        ekey, field = ENUM_FIELD[layer]
        if rec.get(field) not in ENUMS[ekey]:
            ERR.append("[%s] 未注册枚举值 %r (%s)" % (layer, rec.get(field),
                                                     rec.get(layer + "_id", rec.get("item_id"))))


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


def check_original(layer, r):
    if r["item_id"] not in registry:
        GAP.append("[%s] item_id 不在指纹库: %s" % (layer, r.get(layer + "_id", r["item_id"])))
    elif r.get("original") != registry[r["item_id"]]["original"]:
        ERR.append("[%s] original 与指纹库不一致: %s" % (layer, r.get(layer + "_id", r["item_id"])))


def main():
    global registry
    registry = load_registry()
    skip_baseline = "--skip-baseline" in sys.argv

    seen_trl, trl_covered = set(), set()
    for layer in ["ent", "rule", "struct", "reg", "opn", "trl"]:
        for f in layer_files(layer, layer + "_"):
            vol = f[len(layer) + 1:-5]
            data = read_json(os.path.join(LAYER_DIR, layer, f), {"records": []})
            for r in data["records"]:
                check_fields(layer, r)
                check_original(layer, r)
                # struct 额外：维度类型 + target 引用格式
                if layer == "struct":
                    dim = r.get("dim")
                    tf = DIM_TYPE_FIELD.get(dim)
                    if dim not in ENUMS["STRUCT_DIMS"]:
                        ERR.append("[struct] 未注册维度 %r (%s)" % (dim, r["struct_id"]))
                    elif r.get(tf) not in ENUMS.get(dim + "_TYPES", []):
                        ERR.append("[struct] 未注册 %s 类型 %r (%s)" % (tf, r.get(tf), r["struct_id"]))
                    t = r.get("target", "")
                    if t and not (t.startswith(tuple(DIM_PREFIX.values())) or t.startswith("ENT-")):
                        ERR.append("[struct] target 引用格式非法: %s -> %s" % (r["struct_id"], t))
                # trl 额外：trl_id 规则/全局唯一 + norm 注入 + 覆盖收集
                if layer == "trl":
                    tid, iid = r.get("trl_id"), r.get("item_id")
                    if tid and iid and tid != "TRL-" + iid.replace("-", ""):
                        ERR.append("[trl] trl_id 与 item_id 不符: %s (item=%s)" % (tid, iid))
                    if tid in seen_trl:
                        ERR.append("[trl] trl_id 重复: %s" % tid)
                    if tid:
                        seen_trl.add(tid)
                    if iid in registry and r.get("norm") != registry[iid]["norm"]:
                        ERR.append("[trl] norm 与指纹库不一致: %s" % tid)
                    if iid:
                        trl_covered.add(iid)
            print("%s 卷%s：%d 条" % (layer, vol, len(data["records"])))

    # TRL 翻译覆盖（C5 硬规则：条目数=翻译数；不受 --skip-baseline 豁免）
    if not layer_files("trl", "trl_"):
        GAP.append("[trl] TRL 层未打包：_layers/trl/ 无 trl_NN.json（先运行 python build_trl.py）")
    else:
        missing_trl = sorted(set(registry) - trl_covered)
        if missing_trl:
            GAP.append("[trl] 翻译未覆盖指纹库 %d 条: %s%s"
                       % (len(missing_trl), ",".join(missing_trl[:20]),
                          "…" if len(missing_trl) > 20 else ""))

    # struct 悬空引用（target 必须存在于已打包记录或实体主键）
    ent_keys = read_json(os.path.join(ROOT, "_global", "ent_keys.json"), {})
    known = set(ent_keys.values())
    for f in layer_files("struct", "struct_"):
        for r in read_json(os.path.join(LAYER_DIR, "struct", f), {"records": []})["records"]:
            known.add(r["struct_id"])
            t = r.get("target", "")
            if t and t not in known:
                GAP.append("[struct] 悬空 target %s (item=%s)" % (t, r["item_id"]))

    # item_id 全回填（缺省全量检查；--skip-baseline 时只查已打包卷）
    if not skip_baseline:
        join = read_json(os.path.join(ROOT, "_kg_join.json"), {"records": []})
        joined = {r["item_id"] for r in join["records"]}
        missing = sorted(set(registry) - joined)
        if missing:
            GAP.append("item_id 未回填到 _kg_join: %s（%d 个）" % (",".join(missing), len(missing)))

    # 报告
    lines = ["验证缺漏清单（ERR=%d / GAP=%d）" % (len(ERR), len(GAP))]
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
