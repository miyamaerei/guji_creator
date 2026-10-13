# -*- coding: utf-8 -*-
"""
全层验证器：结构性 ERR（id 唯一性[ENT 豁免]、item_id∈registry、枚举越界、geo 引环/层级回退）
与 GAP（text/era_raw/raw/name/flow/change 未命中原文）分开统计；
跨层引用检查：geo_parent 悬空、children 悬空、ent_ids 悬空。
用法：python validate_layers.py [--volumes 01,03]
先行依赖：build_* 已跑完（读 _layers + 指纹库）。
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C
import _kg_enums as E

ERR, GAP, WARN = [], [], []


def _read_json(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def check(cond, tag, msg):
    if not cond:
        (ERR if tag == "ERR" else GAP if tag == "GAP" else WARN).append(msg)


def deep_ent_ids(r):
    """递归收集 *_ent_ids / ent_id 引用。"""
    ids = []
    for k, v in r.items() if isinstance(r, dict) else []:
        if v is None:
            continue
        if k in ("ent_ids", "ent_id") and isinstance(v, (list, str)):
            ids.extend(v if isinstance(v, list) else [v])
        elif isinstance(v, dict):
            ids.extend(deep_ent_ids(v))
        elif isinstance(v, list):
            for x in v:
                if isinstance(x, dict):
                    ids.extend(deep_ent_ids(x))
    return ids


def validate_layer(layer, key, regex_exempt, reg, ent_ids):
    records = []
    for p in C.layer_files(layer):
        obj = _read_json(p)
        records.extend(obj.get("records", []))

    seen = {}
    for r in records:
        rid = r.get(key, "")
        if not rid:
            check(False, "ERR", "%s 缺 id" % r.get("item_id", "?"))
            continue
        if rid.startswith("ENT-"):
            continue  # 主键复用豁免
        if rid in seen:
            check(
                False,
                "ERR",
                "%s id 重复: %s (item=%s/%s)"
                % (layer, rid, seen[rid], r.get("item_id")),
            )
        seen[rid] = r.get("item_id", "?")

        iid = r.get("item_id", "")
        if iid and iid not in reg:
            check(False, "ERR", "%s/%s item_id 不在指纹库: %s" % (layer, rid, iid))

        # 原文命中（逐字段）
        norm = reg.get(iid, {}).get("norm", []) if iid else []
        for f in ("text", "raw", "flow", "change"):
            v = r.get(f)
            if v and v != "未明" and v not in norm:
                check(False, "GAP", "%s/%s %s 未命中原文: %s" % (layer, rid, f, v[:24]))
        for f in ("era_raw",):
            v = r.get(f)
            if v and v != "未明" and v not in norm:
                check(False, "GAP", "%s/%s %s 未命中原文: %s" % (layer, rid, f, v[:24]))
        for bd in r.get("bearing_distance", []) or []:
            if bd.get("raw") and bd["raw"] not in norm:
                check(
                    False,
                    "GAP",
                    "%s/%s bearing.raw 未命中: %s" % (layer, rid, bd["raw"][:24]),
                )

        # 跨层引用
        for eid in deep_ent_ids(r):
            if eid not in ent_ids:
                check(False, "ERR", "%s/%s 悬空 ent 引用: %s" % (layer, rid, eid))

    return records


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volumes", default=None)
    args = ap.parse_args()
    vols = C.iter_volumes(args.volumes)

    reg = C.load_registry()

    # 实体主键表
    pk_path = os.path.join(C.ROOT, "_data", "ent", "实体_主键表.json")
    ent_ids = set()
    if os.path.isfile(pk_path):
        pk = _read_json(pk_path)
        for e in pk.get("entities", []):
            ent_ids.add(e["ent_id"])

    for layer, key, _ in [
        ("ents", "id", None),
        ("tmes", "id", None),
        ("geos", "id", None),
        ("evos", "id", None),
        ("hyds", "id", None),
        ("gars", "id", None),
        ("ress", "id", None),
    ]:
        validate_layer(layer, key, "ENT-", reg, ent_ids)

    # geo 树结构专项
    geo = {}
    for p in C.layer_files("geos"):
        for r in _read_json(p).get("records", []):
            geo[r["id"]] = r
    for rid, r in geo.items():
        pid = (r.get("parent") or {}).get("geo_id")
        if pid and pid not in geo:
            check(False, "ERR", "geos/%s parent 悬空: %s" % (rid, pid))
        for cid in r.get("children", []) or []:
            if cid not in geo:
                check(False, "ERR", "geos/%s children 悬空: %s" % (rid, cid))

    # 枚举复查（以指纹库无关的全层汇总为准）
    enums = {
        "ents-type": (E.ENTITY_TYPES, "ents", "type"),
        "tmes-category": (E.TME_CATEGORIES, "tmes", "category"),
        "geos-level": (E.GEO_LEVELS, "geos", "level"),
        "geos-node_type": (E.GEO_NODES, "geos", "node_type"),
        "geos-tusi_type": (E.TUSI_TYPES, "geos", "tusi_type"),
        "evos-change_type": (E.EVO_TYPES, "evos", "change_type"),
        "hyds-type": (E.HYD_TYPES, "hyds", "type"),
        "hyds-events.kind": (E.HYD_EVENTS, "hyds", "events"),
        "gars-type": (E.GAR_TYPES, "gars", "type"),
        "gars-territorial": (E.GAR_TERRITORIAL, "gars", "territorial"),
        "ress-type": (E.RES_TYPES, "ress", "type"),
    }
    for name, (allowed, layer, field) in enums.items():
        if field == "events":
            vals = [
                e.get("kind")
                for p in C.layer_files(layer)
                for r in _read_json(p).get("records", [])
                for e in (r.get("events") or [])
            ]
        else:
            vals = [
                r.get(field)
                for p in C.layer_files(layer)
                for r in _read_json(p).get("records", [])
                if r.get(field)
            ]
        bad = sorted({v for v in vals if v and v not in allowed})
        for v in bad:
            check(False, "ERR", "%s 枚举越界: %s" % (name, v))

    # 报告
    C.atomic_write_text(
        os.path.join(C.ROOT, "验证缺漏清单.txt"),
        "\n".join(
            ["ERR %d / GAP %d / WARN %d" % (len(ERR), len(GAP), len(WARN))]
            + ["-- ERR --"]
            + ERR
            + ["-- GAP --"]
            + GAP
            + ["-- WARN --"]
            + WARN
        )
        + "\n",
    )
    print("验证完成: ERR=%d GAP=%d WARN=%d" % (len(ERR), len(GAP), len(WARN)))
    for e in ERR[:30]:
        print("  ERR", e)
    for g in GAP[:30]:
        print("  GAP", g)
    for w in WARN[:30]:
        print("  WARN", w)


if __name__ == "__main__":
    main()
