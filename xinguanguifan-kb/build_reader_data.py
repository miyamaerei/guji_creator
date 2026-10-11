# -*- coding: utf-8 -*-
"""《新官轨范》知识阅读器数据打包器（kg-reader v1）
- 读：章节 XHTML + 实体标注(11卷) + 主键表 + 规则/流程/结构/事件归一 + _kg_join
- 出：新官轨范_阅读器/data.js（window.KG 内嵌全部数据，离线 file:// 可用）
- 并：复制各层原始 JSON 到 raw/（保真副本）
- 用法：python build_reader_data.py
"""
import os, re, json, glob, shutil, html as htmllib

BASE = r"C:\Users\Administrator\DoubaoWork\chats\2026-10-09\new-chat"
RD = os.path.join(BASE, "新官轨范_阅读器")
CH_DIR = os.path.join(BASE, "新官轨范_章节")
ANN_DIR = os.path.join(BASE, "新官轨范_标注")
RAW = os.path.join(RD, "raw")
os.makedirs(RAW, exist_ok=True)

TYPE_CN = {"official": "职官", "person": "人物", "org": "机构", "place": "地点",
           "document": "文书", "institution": "制度", "behavior": "行为",
           "object": "器物", "punishment": "刑罚", "time": "时间",
           "quantity": "数量", "undetermined": "类型待定"}

# ---------- 1. 章节 + 条目文本 ----------
chapters = []
for fp in sorted(glob.glob(os.path.join(CH_DIR, "*.xhtml"))):
    base = os.path.basename(fp)
    no = base[:2]
    if no == "00":
        continue
    content = open(fp, encoding="utf-8").read()
    items = re.findall(r'<p class="item">(.*?)</p>', content, re.S)
    items = [htmllib.unescape(m).strip() for m in items]
    if not items:
        items = re.findall(r'<p[^>]*>(.*?)</p>', content, re.S)
        items = [htmllib.unescape(m).strip() for m in items]
    chapters.append({
        "no": no, "file": base, "name": os.path.splitext(base)[0][3:],
        "vol": "卷上" if no == "01" else "卷下",
        "items": [{"iid": f"{no}-{i:03d}", "text": t.lstrip("√").strip()}
                  for i, t in enumerate(items, 1)],
    })

# ---------- 2. 实体标注（按条挂载，含 ent_id） ----------
ann_map = {}
for f in sorted(glob.glob(os.path.join(ANN_DIR, "*.json"))):
    d = json.load(open(f, encoding="utf-8"))
    for e in d["entities"]:
        iid = f"{d['chapter_no']}-{int(e['source'].split('#条')[-1]):03d}"
        ann_map.setdefault(iid, []).append({
            "t": TYPE_CN.get(e["type"], e["type"]), "ty": e["type"],
            "s": e["start"], "e": e["end"], "n": e["normalized"],
            "eid": e.get("ent_id"), "c": e.get("confidence"),
        })
for ch in chapters:
    for it in ch["items"]:
        it["entities"] = ann_map.get(it["iid"], [])

# ---------- 3. 各层归一 -> ID map ----------
def load(rel):
    return json.load(open(os.path.join(BASE, rel), encoding="utf-8"))

def id_map(items, key):
    return {x[key]: x for x in items}

rules_m = load(r"新官轨范_规则_ai\归一_汇总.json")
procs_m = load(r"新官轨范_流程_ai\归一_汇总.json")
struct_m = load(r"新官轨范_结构_ai\归一_汇总.json")
ev_m = load(r"新官轨范_事件_ai\归一_汇总.json")
join_m = load(r"_kg_join.json")
key_m = load(r"新官轨范_实体_主键表.json")

rules = id_map(rules_m["rules"], "rule_id")
procs = id_map(procs_m["processes"], "process_id")
events = id_map(ev_m["events"], "event_id")
SEC = [("ledgers", "ledger_id", "文簿台账"), ("times", "time_id", "县政时间"),
       ("docs", "doc_id", "公文生命周期"), ("actors", "actor_id", "角色职责"),
       ("frauds", "fraud_id", "防弊机制")]
structs = {}
for sec, idk, cn in SEC:
    for x in struct_m.get(sec, []):
        x = dict(x)
        x["section"] = sec
        x["section_cn"] = cn
        structs[x[idk]] = x
entities = {x["ent_id"]: x for x in key_m["entities"]}
for eid, e in entities.items():
    e["alias"] = [k for k, v in key_m["alias_index"].items() if eid in v]
join = {e["item_id"]: e for e in join_m["entries"]}

# ---------- 4. raw 副本 ----------
copy_pairs = [
    (glob.glob(os.path.join(CH_DIR, "*.xhtml")), "章节"),
    (glob.glob(os.path.join(ANN_DIR, "*.json")), "标注"),
    (glob.glob(os.path.join(BASE, "新官轨范_规则_ai", "*.json")), "规则"),
    (glob.glob(os.path.join(BASE, "新官轨范_流程_ai", "*.json")), "流程"),
    (glob.glob(os.path.join(BASE, "新官轨范_结构_ai", "*.json")), "结构"),
    (glob.glob(os.path.join(BASE, "新官轨范_事件_ai", "*.json")), "事件"),
    ([os.path.join(BASE, "新官轨范_实体_主键表.json"),
      os.path.join(BASE, "_item_registry.json"),
      os.path.join(BASE, "_kg_join.json")], "索引"),
]
for files, sub in copy_pairs:
    d = os.path.join(RAW, sub)
    os.makedirs(d, exist_ok=True)
    for f in files:
        shutil.copy2(f, os.path.join(d, os.path.basename(f)))

# ---------- 5. 输出 data.js ----------
kg = {
    "meta": {
        "title": "新官轨范",
        "subtitle": "明·佚名 官箴书 知识阅读器",
        "chapters": len(chapters),
        "items": sum(len(c["items"]) for c in chapters),
        "rules": len(rules), "procs": len(procs), "events": len(events),
        "structs": len(structs), "entities": len(entities),
        "join_all_five": join_m["stats"]["all_five"],
    },
    "chapters": chapters,
    "entities": entities,
    "rules": rules,
    "procs": procs,
    "events": events,
    "structs": structs,
    "join": join,
    "alias": key_m["alias_index"],
}
js = "window.KG = " + json.dumps(kg, ensure_ascii=False, separators=(",", ":")) + ";"
with open(os.path.join(RD, "data.js"), "w", encoding="utf-8") as f:
    f.write(js)
print("data.js 字节:", os.path.getsize(os.path.join(RD, "data.js")))
print("chapters=%d items=%d rules=%d procs=%d events=%d structs=%d entities=%d alias=%d" % (
    len(chapters), sum(len(c["items"]) for c in chapters), len(rules), len(procs),
    len(events), len(structs), len(entities), len(key_m["alias_index"])))
print("raw 复制完成:", RAW)
