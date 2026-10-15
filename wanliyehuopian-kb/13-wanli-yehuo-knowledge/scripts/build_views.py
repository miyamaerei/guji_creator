# -*- coding: utf-8 -*-
"""派生视图生成器（SKILL.md §10 六视图）。

输入：_layers/ 十层 + _global/ent_keys.json + _item_registry.json
输出到 views/：
  timeline/<人物>.json                人物全任职+事件+议论时间线（≥3 条记录的人物）
  faction_network.json                党派关系网络（节点=主键实体，边=rels）
  institution_evolution/<制度>.json   制度沿革链（regs+tmes，按 REIGN_ORDER 排序）
  subcategory_index.json              ○ 分类索引
  supplements_to_ming_history.csv     补正史之阙条目汇总
  author_stance_index.json            沈德符立场索引（按 target 分组）
幂等：全量重建。用法：python scripts/build_views.py
"""
import csv
import io
import json
import os
import re
import shutil
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYERS_DIR = os.path.join(BASE, "_layers")
VIEWS = os.path.join(BASE, "views")
GLOBAL_DIR = os.path.join(BASE, "_global")

LAYERS = ["ents", "rules", "events", "appts", "rels", "cits", "opns", "mings", "tmes", "regs"]
ID_KEY = {"ents": "ent_id", "rules": "rule_id", "events": "event_id", "appts": "appt_id",
          "rels": "rel_id", "cits": "cit_id", "opns": "opn_id", "mings": "ming_id",
          "tmes": "tme_id", "regs": "reg_id"}
ENT_RE = re.compile(r"^ENT-\d{4}$")
SUPPLEMENT_VALUES = {"补正史之阙", "正史不载", "异于正史"}

import sys
sys.path.insert(0, os.path.join(BASE, "scripts"))
from _kg_enums import REIGN_ORDER  # noqa: E402


def load_layer_array(path):
    with io.open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d["records"] if isinstance(d, dict) else d


def load_all():
    data = {}
    for layer in LAYERS:
        recs = []
        d = os.path.join(LAYERS_DIR, layer)
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".json"):
                recs.extend(load_layer_array(os.path.join(d, fn)))
        data[layer] = recs
    return data


def ent_refs(value):
    if isinstance(value, str):
        if ENT_RE.match(value):
            yield value
    elif isinstance(value, list):
        for v in value:
            if isinstance(v, str) and ENT_RE.match(v):
                yield v
            else:
                for x in ent_refs(v):
                    yield x
    elif isinstance(value, dict):
        for v in value.values():
            for x in ent_refs(v):
                yield x


def reign_rank(r):
    return REIGN_ORDER.get((r or "").split("（")[0].strip(), 99)


def main():
    data = load_all()
    with io.open(os.path.join(GLOBAL_DIR, "ent_keys.json"), encoding="utf-8") as f:
        ek = json.load(f)["entities"]
    ent_to_primary = {}
    primary_meta = {}
    for norm, e in ek.items():
        primary_meta[e["primary"]] = norm
        for occ in e["occurrences"]:
            ent_to_primary[occ["ent_id"]] = e["primary"]

    with io.open(os.path.join(BASE, "_item_registry.json"), encoding="utf-8") as f:
        registry = {r["item_id"]: r for r in json.load(f)["records"]}

    if os.path.isdir(VIEWS):
        shutil.rmtree(VIEWS)
    os.makedirs(os.path.join(VIEWS, "timeline"), exist_ok=True)
    os.makedirs(os.path.join(VIEWS, "institution_evolution"), exist_ok=True)

    def canon(rec):
        return sorted({ent_to_primary.get(e, e) for e in ent_refs(rec)})

    # ---- 1. timeline/<人物>.json ----
    person_bag = defaultdict(lambda: defaultdict(list))
    for layer in ["appts", "events", "opns", "mings", "rels"]:
        for r in data[layer]:
            for p in canon(r):
                if primary_meta.get(p) and ek[primary_meta[p]]["type"] == "person":
                    person_bag[p][layer].append({ID_KEY[layer]: r[ID_KEY[layer]],
                                                  "item_id": r.get("item_id"),
                                                  "reign": r.get("reign", "")})
    tl_count = 0
    for primary, bag in person_bag.items():
        total = sum(len(v) for v in bag.values())
        if total < 3:
            continue
        name = primary_meta[primary]
        timeline = {"person": name, "ent_id": primary,
                    "volumes": sorted({registry[i]["volume"] for lay in bag.values()
                                       for i in (x["item_id"] for x in lay) if i in registry}),
                    "by_reign": sorted({x["reign"] for lay in bag.values() for x in lay if x["reign"]}),
                    "layers": {k: sorted(v, key=lambda x: (reign_rank(x["reign"]), x["item_id"]))
                               for k, v in sorted(bag.items())},
                    "total_records": total}
        with io.open(os.path.join(VIEWS, "timeline", "%s.json" % name), "w", encoding="utf-8") as f:
            json.dump(timeline, f, ensure_ascii=False, indent=2)
        tl_count += 1

    # ---- 2. faction_network.json ----
    nodes, edges = {}, []
    for r in data["rels"]:
        c = canon(r)
        for e in c:
            nodes.setdefault(e, {"ent_id": e, "name": primary_meta.get(e, e),
                                 "faction": None, "degree": 0})
        if len(c) >= 2:
            edges.append({"source": c[0], "target": c[1],
                          "relation": r.get("relation", ""), "item_id": r.get("item_id"),
                          "detail": r.get("detail", "")})
            for e in c:
                nodes[e]["degree"] += 1
    for r in data["opns"]:
        f = r.get("faction")
        if f and f != "无":
            for e in canon(r):
                if e in nodes:
                    nodes[e]["faction"] = f
    with io.open(os.path.join(VIEWS, "faction_network.json"), "w", encoding="utf-8") as f:
        json.dump({"nodes": sorted(nodes.values(), key=lambda x: -x["degree"]),
                   "edges": edges}, f, ensure_ascii=False, indent=2)

    # ---- 3. institution_evolution/<制度>.json ----
    inst_bag = defaultdict(list)
    for r in data["tmes"]:
        key = (r.get("target") or r.get("institution_target") or "").strip()
        if key:
            inst_bag[key].append({"kind": "tme", "tme_id": r["tme_id"], "item_id": r.get("item_id"),
                                  "reign": r.get("reign", ""), "date": r.get("date", ""),
                                  "event": r.get("event", "")})
    for r in data["regs"]:
        key = (r.get("name") or "").strip()
        if key:
            inst_bag[key].append({"kind": "reg", "reg_id": r["reg_id"], "item_id": r.get("item_id"),
                                  "reign": r.get("reign", ""), "type": r.get("type", ""),
                                  "description": r.get("description", "")[:120]})
    inst_count = 0
    for key, rows in inst_bag.items():
        if len(rows) < 2:
            continue
        rows.sort(key=lambda x: (reign_rank(x.get("reign")), x.get("item_id", "")))
        safe = re.sub(r'[\\/:*?"<>|]', "·", key)
        with io.open(os.path.join(VIEWS, "institution_evolution", "%s.json" % safe), "w", encoding="utf-8") as f:
            json.dump({"institution": key, "chain": rows, "span_reigns":
                       sorted({x.get("reign") for x in rows if x.get("reign")}, key=reign_rank)},
                      f, ensure_ascii=False, indent=2)
        inst_count += 1

    # ---- 4. subcategory_index.json ----
    sub_idx = defaultdict(list)
    for iid, meta in registry.items():
        if meta.get("subcategory"):
            sub_idx[meta["subcategory"]].append({"item_id": iid, "title": meta["entry_title"],
                                                 "volume": meta["volume_name"]})
    with io.open(os.path.join(VIEWS, "subcategory_index.json"), "w", encoding="utf-8") as f:
        json.dump({k: sorted(v, key=lambda x: x["item_id"]) for k, v in sorted(sub_idx.items())},
                  f, ensure_ascii=False, indent=2)

    # ---- 5. supplements_to_ming_history.csv ----
    rows = []
    for layer in ["mings", "events", "regs"]:
        for r in data[layer]:
            v = r.get("vs_official_history", "")
            extra = (r.get("supplements_what") or "") if layer == "mings" else ""
            if v in SUPPLEMENT_VALUES or extra:
                meta = registry.get(r.get("item_id"), {})
                rows.append({"item_id": r.get("item_id", ""), "entry_title": meta.get("entry_title", ""),
                             "volume": meta.get("volume_name", ""), "layer": layer,
                             "record_id": r.get(ID_KEY[layer], ""),
                             "vs_official_history": v, "supplements_what": extra,
                             "summary": (r.get("event") or r.get("title") or r.get("name") or "")[:100]})
    with io.open(os.path.join(VIEWS, "supplements_to_ming_history.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item_id", "entry_title", "volume", "layer",
                                         "record_id", "vs_official_history", "supplements_what", "summary"])
        w.writeheader()
        w.writerows(sorted(rows, key=lambda x: x["item_id"]))

    # ---- 6. author_stance_index.json ----
    stance = defaultdict(list)
    for r in data["opns"]:
        key = (r.get("target") or "未标注").strip()
        stance[key].append({"opn_id": r["opn_id"], "item_id": r.get("item_id"),
                            "reign": r.get("reign", ""), "opinion_type": r.get("opinion_type", ""),
                            "tone": r.get("tone", ""), "content": r.get("content", "")[:150]})
    with io.open(os.path.join(VIEWS, "author_stance_index.json"), "w", encoding="utf-8") as f:
        json.dump({"total_targets": len(stance),
                   "index": {k: sorted(v, key=lambda x: x["item_id"]) for k, v in sorted(stance.items())}},
                  f, ensure_ascii=False, indent=2)

    print("timeline 人物数: %d" % tl_count)
    print("faction_network 节点/边: %d/%d" % (len(nodes), len(edges)))
    print("institution_evolution 制度数: %d" % inst_count)
    print("subcategory 类数: %d" % len(sub_idx))
    print("supplements_to_ming_history 行数: %d" % len(rows))
    print("author_stance 目标数: %d" % len(stance))


if __name__ == "__main__":
    main()
