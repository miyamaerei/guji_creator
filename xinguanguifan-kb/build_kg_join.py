# -*- coding: utf-8 -*-
"""
《新官轨范》跨层索引生成器（kg-join v1，P1 产物）
一行看全：item_id → rule_id / proc_ids / event_ids / struct(五维度) / ent_ids。
数据源：各层归一汇总 + 实体主键表 + 实体层卷标注（按 source 条号映射）。
用法：python build_kg_join.py
"""
import os, re, json, glob

BASE = r"C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat"
OUT = os.path.join(BASE, "_kg_join.json")

REG = json.load(open(os.path.join(BASE, "_item_registry.json"), encoding="utf-8"))
RULE_MERGE = json.load(open(os.path.join(BASE, "新官轨范_规则_ai", "归一_汇总.json"), encoding="utf-8"))
PROC_MERGE = json.load(open(os.path.join(BASE, "新官轨范_流程_ai", "归一_汇总.json"), encoding="utf-8"))
EV_MERGE = json.load(open(os.path.join(BASE, "新官轨范_事件_ai", "归一_汇总.json"), encoding="utf-8"))
STRUCT_MERGE = json.load(open(os.path.join(BASE, "新官轨范_结构_ai", "归一_汇总.json"), encoding="utf-8"))
KEY_TABLE = json.load(open(os.path.join(BASE, "新官轨范_实体_主键表.json"), encoding="utf-8"))

# item -> rule 与 source
item2rule = {r["item_id"]: r["rule_id"] for r in RULE_MERGE["rules"]}
item2source = {r["item_id"]: r["source"] for r in RULE_MERGE["rules"]}
# item -> proc ids
item2proc = {}
for p in PROC_MERGE["processes"]:
    for it in p.get("derived_from", []):
        item2proc.setdefault(it, []).append(p["process_id"])
# item -> event ids
item2ev = {}
for e in EV_MERGE["events"]:
    for it in e.get("derived_from", []):
        item2ev.setdefault(it, []).append(e["event_id"])
# item -> struct ids（按 item_id 字段，P0-3 已回填）
SEC_KEYS = {"ledgers": "ledger_id", "times": "time_id", "docs": "doc_id",
            "actors": "actor_id", "frauds": "fraud_id"}
item2struct = {}
for sec, idk in SEC_KEYS.items():
    for it in STRUCT_MERGE.get(sec, []):
        iid = it.get("item_id")
        if iid:
            item2struct.setdefault(iid, {}).setdefault(sec, []).append(it[idk])
# item -> ent ids（实体层标注按 source 条号）
SRC_RE = re.compile(r"(\d{2})_卷.*?\.xhtml#条(\d+)")
item2ent = {}
for f in glob.glob(os.path.join(BASE, "新官轨范_标注", "*.json")):
    d = json.load(open(f, encoding="utf-8"))
    for e in d.get("entities", []):
        m = SRC_RE.search(e.get("source", ""))
        if not m or not e.get("ent_id"):
            continue
        iid = "%s-%03d" % (m.group(1), int(m.group(2)))
        item2ent.setdefault(iid, []).append(e["ent_id"])

entries = []
for iid in sorted(REG.keys()):
    src = item2source.get(iid, "")
    entries.append({
        "item_id": iid,
        "source": src,
        "rule_id": item2rule.get(iid, ""),
        "proc_ids": sorted(set(item2proc.get(iid, []))),
        "event_ids": sorted(set(item2ev.get(iid, []))),
        "struct": {k: sorted(set(v)) for k, v in item2struct.get(iid, {}).items()},
        "ent_ids": sorted(set(item2ent.get(iid, []))),
    })

stats = {
    "total_items": len(entries),
    "with_rule": sum(1 for e in entries if e["rule_id"]),
    "with_proc": sum(1 for e in entries if e["proc_ids"]),
    "with_event": sum(1 for e in entries if e["event_ids"]),
    "with_struct": sum(1 for e in entries if e["struct"]),
    "with_ent": sum(1 for e in entries if e["ent_ids"]),
    "all_five": sum(1 for e in entries if e["rule_id"] and e["proc_ids"] and e["event_ids"] and e["struct"] and e["ent_ids"]),
}
join = {
    "schema_version": "kg-join-v1",
    "generated_from": {
        "registry": "_item_registry.json", "rules": "新官轨范_规则_ai/归一_汇总.json",
        "procs": "新官轨范_流程_ai/归一_汇总.json", "events": "新官轨范_事件_ai/归一_汇总.json",
        "struct": "新官轨范_结构_ai/归一_汇总.json", "entities": "新官轨范_实体_主键表.json + 新官轨范_标注/*.json",
    },
    "stats": stats,
    "entries": entries,
}
json.dump(join, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 扁平 CSV（UTF-8 BOM，Excel 直开）：一行一条 item，各层 ID 平铺
import csv
CSV_OUT = os.path.join(BASE, "_kg_join_flat.csv")
struct_order = ["ledgers", "times", "docs", "actors", "frauds"]
with open(CSV_OUT, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["item_id", "chapter", "source", "rule_id", "proc_ids", "event_ids",
                "struct_ids", "ent_ids", "layer_count"])
    for e in entries:
        sid = e["source"]
        if sid and ".xhtml" in sid:
            ch = "_".join(sid.split(".xhtml")[0].split("_")[:2])
        else:
            ch = e["item_id"][:2] + "_卷"
        st = ";".join(k + ":" + ",".join(v) for k in struct_order for v in [e["struct"].get(k, [])] if v)
        cnt = sum([bool(e["rule_id"]), bool(e["proc_ids"]), bool(e["event_ids"]),
                   bool(e["struct"]), bool(e["ent_ids"])])
        w.writerow([e["item_id"], ch, sid, e["rule_id"],
                    " ".join(e["proc_ids"]), " ".join(e["event_ids"]),
                    st, " ".join(e["ent_ids"]), cnt])

print(json.dumps(stats, ensure_ascii=False))
print("已写:", OUT)
print("已写:", CSV_OUT)
# 抽查
for probe in ["01-001", "04-002", "07-021"]:
    e = next(x for x in entries if x["item_id"] == probe)
    print(probe, "rule=%s proc=%s event=%s struct_keys=%s ents=%d" % (
        e["rule_id"], e["proc_ids"], e["event_ids"], list(e["struct"].keys()), len(e["ent_ids"])))
