# -*- coding: utf-8 -*-
"""校验器（验收闸门）：C5 枚举 / C6 字段完整 / C3 original 注入 / 引用槽位 / item_id 全回填。
层：ent/appt/evt/lit/reg/nam/opn/cus/geo（9 层）。
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

# 各层"存在即可"字段（语义允许空值，只查存在性）；其余必填字段查非空
PRESENT_OK = {
    "ent": {"original"},
    "appt": {"person_ent_ids", "official_ent_ids", "institution_ent_ids", "when", "evidence", "original"},
    "evt": {"who_ent_ids", "when", "where", "original"},
    "lit": {"author_ent_ids", "content_location", "original"},
    "reg": {"evolution", "target", "original"},
    "nam": {"ent_ids", "original"},
    "opn": {"evidence_refs", "original"},
    "cus": {"region", "original"},
    "geo": {"attributes", "lore", "ent_ids", "original"},
}
NOT_EMPTY = {
    "ent": {"ent_id", "item_id", "text", "type", "start", "end", "normalized", "confidence", "source"},
    "appt": {"appointment_id", "item_id", "person", "office", "institution", "status", "confidence"},
    "evt": {"event_id", "item_id", "type", "who", "action", "what", "confidence"},
    "lit": {"lit_id", "item_id", "title", "type", "confidence"},
    "reg": {"reg_id", "item_id", "name", "type", "content", "confidence"},
    "nam": {"nam_id", "item_id", "name", "category", "scope", "entries", "confidence"},
    "opn": {"opn_id", "item_id", "topic", "stance", "argument", "confidence"},
    "cus": {"cus_id", "item_id", "type", "term", "description", "confidence"},
    "geo": {"geo_id", "item_id", "name", "category", "confidence"},
}
# 枚举字段 → 枚举组
ENUM_FIELD = {
    "ent": "type", "appt": "status", "evt": "type", "lit": "type",
    "reg": "type", "nam": "category", "opn": "stance", "cus": "type", "geo": "category",
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
            if vol.isdigit() and len(vol) == 2:
                out.append(f)
    return out


def main():
    registry = load_registry()
    skip_baseline = "--skip-baseline" in sys.argv

    for layer, group in LAYER_ENUM_GROUP.items():
        enums = set(ENUMS.get(group + "_TYPES", []))
        id_key = {"ent": "ent_id", "appt": "appointment_id", "evt": "event_id",
                  "lit": "lit_id", "reg": "reg_id", "nam": "nam_id",
                  "opn": "opn_id", "cus": "cus_id", "geo": "geo_id"}[layer]
        for f in layer_files(layer, layer + "_"):
            vol = f[len(layer) + 1:-5]
            data = read_json(os.path.join(LAYER_DIR, layer, f), {"records": []})
            for r in data["records"]:
                check_fields(layer, r)
                ev = ENUM_FIELD[layer]
                if r.get(ev) not in enums:
                    ERR.append("[%s] 未注册枚举值 %r (%s)" % (layer, r.get(ev), r[id_key]))
                if r["item_id"] not in registry:
                    GAP.append("[%s] item_id 不在指纹库: %s" % (layer, r[id_key]))
                if r.get("original") != registry.get(r["item_id"], {}).get("original"):
                    ERR.append("[%s] original 与指纹库不一致: %s" % (layer, r[id_key]))
            print("%s 卷%s：%d 条" % (layer, vol, len(data["records"])))

    # 悬空引用（reg.target / opn.evidence_refs 引用实体或同层 ID）
    ent_keys = read_json(os.path.join(ROOT, "_global", "ent_keys.json"), {})
    known = set(ent_keys.values())
    for layer in ("reg", "opn"):
        for f in layer_files(layer, layer + "_"):
            for r in read_json(os.path.join(LAYER_DIR, layer, f), {"records": []})["records"]:
                known.add(r["%s_id" % layer])
    for f in layer_files("reg", "reg_"):
        for r in read_json(os.path.join(LAYER_DIR, "reg", f), {"records": []})["records"]:
            t = r.get("target", "")
            if t and t not in known:
                GAP.append("[reg] 悬空 target %s (item=%s)" % (t, r["item_id"]))
    for f in layer_files("opn", "opn_"):
        for r in read_json(os.path.join(LAYER_DIR, "opn", f), {"records": []})["records"]:
            for t in r.get("evidence_refs", []):
                if t and t not in known:
                    GAP.append("[opn] 悬空 evidence_ref %s (item=%s)" % (t, r["item_id"]))

    # item_id 全回填（缺省全量检查；--skip-baseline 时只查已打包卷）
    if not skip_baseline:
        join = read_json(os.path.join(ROOT, "_kg_join.json"), {"records": []})
        joined = {r["item_id"] for r in join["records"]}
        missing = sorted(set(registry) - joined)
        if missing:
            GAP.append("item_id 未回填到 _kg_join: %s（%d 个）" % (",".join(missing), len(missing)))

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
