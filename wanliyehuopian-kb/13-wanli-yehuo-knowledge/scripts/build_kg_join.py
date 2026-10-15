# -*- coding: utf-8 -*-
"""跨层整合打包器：以条目（item_id）为主键 join 全部 10 层。

产物：
  _kg_join.json       顶层 {"records":[...]}：每条目一条，含各层记录 ID 清单、
                      本卷 ENT 引用解析后的全局主键实体（canonical_ents）
  _kg_join_flat.csv   扁平表：item_id, layer, record_id, summary, reign, canonical_ent
幂等：纯读 _layers/ + _global/ + _item_registry.json，重跑结果一致。
用法：python scripts/build_kg_join.py
"""
import csv
import io
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYERS_DIR = os.path.join(BASE, "_layers")
GLOBAL_DIR = os.path.join(BASE, "_global")
REGISTRY = os.path.join(BASE, "_item_registry.json")

LAYERS = ["ents", "rules", "events", "appts", "rels", "cits", "opns", "mings", "tmes", "regs"]
ID_KEY = {"ents": "ent_id", "rules": "rule_id", "events": "event_id", "appts": "appt_id",
          "rels": "rel_id", "cits": "cit_id", "opns": "opn_id", "mings": "ming_id",
          "tmes": "tme_id", "regs": "reg_id"}
ENT_RE = re.compile(r"^ENT-\d{4}$")


def load_layer_array(path):
    with io.open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d["records"] if isinstance(d, dict) else d


def iter_ent_refs(value):
    """递归找出记录里所有 ENT-xxxx 引用（兼容字段名跨卷异构）"""
    if isinstance(value, str):
        if ENT_RE.match(value):
            yield value
    elif isinstance(value, list):
        for v in value:
            if isinstance(v, str) and ENT_RE.match(v):
                yield v
            elif isinstance(v, dict):
                for x in v.values():
                    for y in iter_ent_refs(x):
                        yield y
            else:
                for y in iter_ent_refs(v):
                    yield y
    elif isinstance(value, dict):
        for v in value.values():
            for y in iter_ent_refs(v):
                yield y


def summary_of(layer, r):
    if layer == "ents":
        return r.get("text", "")
    if layer == "rules":
        return r.get("title", "")
    if layer == "events":
        return r.get("title", "")
    if layer == "appts":
        return "%s→%s" % (r.get("person_text", ""), r.get("position", r.get("office", "")))
    if layer == "rels":
        return "%s-%s->%s" % (r.get("source_text", ""), r.get("relation", ""), r.get("target_text", ""))
    if layer == "cits":
        return "%s（引：%s）" % (r.get("cited_work", ""), r.get("author", ""))
    if layer == "opns":
        return "%s论%s" % (r.get("author_text", ""), r.get("target", ""))
    if layer == "mings":
        return "%s：%s" % (r.get("person_text", r.get("first_person", "")), r.get("event", ""))
    if layer == "tmes":
        return r.get("event", r.get("target", ""))
    if layer == "regs":
        return r.get("name", "")
    return ""


def main():
    with io.open(REGISTRY, encoding="utf-8") as f:
        registry = {r["item_id"]: r for r in json.load(f)["records"]}

    # ent_id -> 全局主键（canonical primary）
    with io.open(os.path.join(GLOBAL_DIR, "ent_keys.json"), encoding="utf-8") as f:
        ents = json.load(f)["entities"]
    ent_to_primary = {}
    for norm, e in ents.items():
        for occ in e["occurrences"]:
            ent_to_primary[occ["ent_id"]] = e["primary"]

    join_records, flat_rows = [], []
    vol_files = {}
    for layer in LAYERS:
        d = os.path.join(LAYERS_DIR, layer)
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".json"):
                vol_files.setdefault(layer, []).append(os.path.join(d, fn))

    # 每层每卷记录挂到 item_id
    by_item = {}  # item_id -> {layer: [rec]}
    ent_refs = {}  # item_id -> set(ent_id)（含跨层引用）
    for layer in LAYERS:
        for path in vol_files.get(layer, []):
            for r in load_layer_array(path):
                iid = r.get("item_id")
                if not iid:
                    continue
                by_item.setdefault(iid, {}).setdefault(layer, []).append(r)
                for ref in iter_ent_refs(r):
                    ent_refs.setdefault(iid, set()).add(ref)

    missing = 0
    for iid in sorted(set(list(by_item.keys()) + list(registry.keys()))):
        meta = registry.get(iid)
        if meta is None:
            missing += 1
            continue
        layers_present = by_item.get(iid, {})
        canon = sorted({ent_to_primary.get(e, e) for e in ent_refs.get(iid, set())})
        join_records.append({
            "item_id": iid,
            "volume": meta["volume"],
            "volume_name": meta["volume_name"],
            "volume_type": meta.get("volume_type", ""),
            "subcategory": meta.get("subcategory", ""),
            "entry_title": meta["entry_title"],
            "layers": {lay: [r.get(ID_KEY[lay]) for r in recs] for lay, recs in sorted(layers_present.items())},
            "layer_count": len(layers_present),
            "canonical_ents": canon,
            "ent_count": len(canon),
        })
        for lay in LAYERS:
            for r in layers_present.get(lay, []):
                rec_canon = sorted({ent_to_primary.get(e, e) for e in iter_ent_refs(r)})
                flat_rows.append({
                    "item_id": iid,
                    "entry_title": meta["entry_title"],
                    "layer": lay,
                    "record_id": r.get(ID_KEY[lay], ""),
                    "summary": summary_of(lay, r),
                    "reign": r.get("reign", r.get("effective_date", "")),
                    "canonical_ents": "|".join(rec_canon),
                })

    with io.open(os.path.join(BASE, "_kg_join.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": {"total_items": len(join_records),
                            "total_records": len(flat_rows),
                            "generated_by": "build_kg_join.py"},
                   "records": join_records}, f, ensure_ascii=False, indent=2)
    with io.open(os.path.join(BASE, "_kg_join_flat.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item_id", "entry_title", "layer", "record_id",
                                          "summary", "reign", "canonical_ents"])
        w.writeheader()
        w.writerows(flat_rows)

    print("_kg_join 条目数: %d（registry 1451 中无记录的条目: %d）" % (len(join_records), len(registry) - len(join_records) + missing))
    print("_kg_join_flat 行数: %d" % len(flat_rows))
    no_record = [i for i in registry if i not in by_item]
    print("零挂载条目: %d %s" % (len(no_record), no_record[:10]))


if __name__ == "__main__":
    main()
