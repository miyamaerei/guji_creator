# -*- coding: utf-8 -*-
"""产出《使用报告》《项目总结报告》所需的全部实测数字。"""
import io, sys, os, json, glob
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

R = {}

# ---------- 底座 ----------
reg = json.load(open("_item_registry.json", encoding="utf-8"))
R["registry"] = len(reg)
ids = sorted(reg.keys())
R["id_first"], R["id_last"] = ids[0], ids[-1]
vols = Counter(k.split("-")[0] for k in ids)
R["volumes"] = len(vols)
R["vol_min"], R["vol_max"] = min(vols), max(vols)

# ---------- 全层规模 ----------
LAYERS = {
    "ents": "实体归一", "nams": "人名索引", "rules": "规则/事例", "geo": "地理",
    "orgs": "衙门", "offices": "官职", "objs": "器物", "reports": "报告/奏议",
    "num": "数字文册", "process": "流程", "cits": "引书", "laws": "律例",
    "rituals": "礼仪", "dress": "冠服", "inspect": "考核", "eng": "工程",
    "foreign": "朝贡", "materials": "物料", "xref": "互见", "njc": "两京对照",
    "rank": "品级章服", "tim": "制度时间线", "mentions": "实体提及索引",
}
files = {}
for f in glob.glob("_layers/*.json"):
    files[os.path.basename(f)[:-5]] = f
R["layer_files"] = sorted(files.keys())

scale = {}
for k, f in files.items():
    try:
        d = json.load(open(f, encoding="utf-8"))
        scale[k] = len(d) if isinstance(d, (list, dict)) else 0
    except Exception as e:
        scale[k] = f"ERR {e}"
R["scale"] = scale

# ---------- join ----------
J = json.load(open("_kg_join.json", encoding="utf-8"))
R["join_rows"] = len(J)
rows = list(J.values()) if isinstance(J, dict) else J
BUCKETS = ["rules", "ents", "nams", "cits", "laws", "inspect", "rituals", "dress",
           "foreign", "materials", "eng", "offices", "process", "orgs", "rank",
           "njc", "xref", "geo", "num", "reports", "objs", "mentions", "rank_seq"]
R["bucket_fill"] = {b: sum(1 for r in rows if r.get(b)) for b in BUCKETS}
R["lc"] = dict(sorted(Counter(r.get("layer_count", 0) for r in rows).items()))
R["multi"] = sum(1 for r in rows if r.get("layer_count", 0) >= 2)
R["orphan"] = sum(1 for r in rows if r.get("layer_count", 0) == 0)
R["orphan_kind"] = dict(Counter(r.get("node_kind") for r in rows
                                if r.get("layer_count", 0) == 0))
flat = "_kg_join_flat.csv"
R["flat_kb"] = round(os.path.getsize(flat) / 1024) if os.path.exists(flat) else 0

# ---------- 三棵树 ----------
for f in ("org_tree", "office_tree"):
    t = json.load(open(f"_layers/{f}.json", encoding="utf-8"))
    R[f] = {k: v for k, v in t.items() if not isinstance(v, list)}
    R[f]["n_roots_list"] = len(t.get("roots") or [])

# ---------- 孤立条审计 ----------
if os.path.exists("_p4_orphans.json"):
    orp = json.load(open("_p4_orphans.json", encoding="utf-8"))
    R["orphan_audit"] = len(orp)

# ---------- 文件清单 ----------
R["root_scripts"] = sorted(os.path.basename(p) for p in glob.glob("*.py"))
R["root_reports"] = sorted(os.path.basename(p) for p in glob.glob("*.md"))
R["deliver"] = sorted(os.path.basename(p) for p in glob.glob("_deliver/*"))
R["n_extract"] = len(glob.glob("_extract/*.txt"))
R["n_layers"] = len(files)

for k, v in R.items():
    print(f"### {k}")
    print(json.dumps(v, ensure_ascii=False, indent=1)[:2600])
