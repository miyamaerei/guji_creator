# -*- coding: utf-8 -*-
"""批量补层：纯规则卷加ents，纯名录卷加geo/offices"""
import json, os, re
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
reg = json.load(open(os.path.join(ROOT, "_item_registry.json"), encoding="utf-8"))

# 加载现有层
layers = {}
for layer in ["rules", "nams", "ents", "cits", "laws", "rituals", "geo", "org_events", "offices", "materials", "inspect", "dress", "foreign"]:
    p = os.path.join(ROOT, "_layers", layer + ".json")
    if os.path.exists(p):
        layers[layer] = json.load(open(p, encoding="utf-8"))
    else:
        layers[layer] = []

layers["ents"] = [e for e in layers["ents"] if not e.get("item_id", "").startswith("VIRT")]

def build_index(data):
    d = defaultdict(list)
    for r in data:
        d[r["item_id"]].append(r)
    return d

idx = {layer: build_index(data) for layer, data in layers.items()}

# ===== 1. 找出低密度卷（<1.2） =====
vol_stats = defaultdict(lambda: {"items": 0, "records": 0, "layers": Counter()})
for iid in reg:
    vol = int(iid.split("-")[0])
    vol_stats[vol]["items"] += 1
    for layer in layers:
        cnt = len(idx[layer][iid])
        vol_stats[vol]["records"] += cnt
        if cnt > 0:
            vol_stats[vol]["layers"][layer] += 1

low_vols = []
for vol, s in vol_stats.items():
    d = s["records"] / s["items"] if s["items"] else 0
    if d < 1.2:
        # 判断是纯规则卷还是纯名录卷
        main_layer = s["layers"].most_common(1)[0][0] if s["layers"] else "unknown"
        low_vols.append((vol, d, main_layer, s["items"]))

low_vols.sort()
print(f"低密度卷（<1.2）共{len(low_vols)}卷:")
print(f"  {'卷':>4s} {'密度':>6s} {'主层':>8s} {'条目':>5s}")
print("  " + "-" * 30)
for vol, d, main, items in low_vols:
    print(f"  卷{vol:3d}: {d:6.2f}  {main:8s} {items:5d}")

# ===== 2. 批量提取实体（给纯规则卷） =====
# 实体类型关键词
ENT_PATTERNS = {
    "institution": ["部", "院", "寺", "监", "司", "府", "州", "县", "卫", "所", "局", "厂", "库", "仓"],
    "person_title": ["尚书", "侍郎", "都御史", "御史", "郎中", "员外郎", "主事", "知府", "知州", "知县"],
    "regulation": ["例", "制", "令", "诏", "敕"],
}

def extract_ents(title, original):
    """从文本中提取实体"""
    ents = []
    text = title + " " + original

    # 衙门名
    for m in re.finditer(r"([一-龥]{2,10}(部|院|寺|监|司|府|卫|所))", text):
        name = m.group(1)
        if len(name) <= 8:
            ents.append({"text": name, "type": "institution"})

    # 官职名
    for m in re.finditer(r"([一-龥]{2,6}(尚书|侍郎|御史|郎中|员外郎|主事|知府|知州|知县))", text):
        name = m.group(1)
        if len(name) <= 8:
            ents.append({"text": name, "type": "person_title"})

    return ents

# ===== 3. 批量提取geo/offices（给纯名录卷） =====
GEO_SUFFIXES = ["府", "州", "县", "卫", "千户所"]
OFFICE_SUFFIXES = ["大夫", "郎", "少卿", "寺丞", "主事", "郎中", "员外郎", "御史", "都督"]

def extract_geo_offices(title, original):
    """从名录条目中提取geo和offices"""
    geos = []
    offices = []

    # 短行标题（名录类）
    if len(title) < 30:
        parts = re.split(r"[\s　]+", title)
        for p in parts:
            p = p.strip()
            if not p or len(p) < 2:
                continue

            # 判断是否是地名
            for suffix in GEO_SUFFIXES:
                if p.endswith(suffix):
                    geos.append(p)
                    break

            # 判断是否是官职
            for suffix in OFFICE_SUFFIXES:
                if p.endswith(suffix) and len(p) <= 8:
                    offices.append(p)
                    break

    return geos, offices

# ===== 执行批量补层 =====
new_ents = []
new_geos = []
new_offices = []

ent_seq = len(layers["ents"])
geo_seq = len(layers["geo"])
off_seq = len(layers["offices"])

for vol, density, main_layer, items in low_vols:
    vol_items = [(iid, item) for iid, item in reg.items() if int(iid.split("-")[0]) == vol]

    for iid, item in vol_items:
        title = item["title"]
        original = item["original"]

        # 纯规则卷 → 加ents
        if main_layer == "rules":
            ents = extract_ents(title, original)
            for e in ents:
                ent_seq += 1
                new_ents.append({
                    "ent_id": f"ENT-{ent_seq:05d}",
                    "item_id": iid,
                    "text": e["text"],
                    "type": e["type"],
                })

        # 纯名录卷 → 加geo/offices
        elif main_layer == "nams":
            geos, offices = extract_geo_offices(title, original)
            for g in geos:
                geo_seq += 1
                new_geos.append({
                    "geo_id": f"GEO-{geo_seq:04d}",
                    "item_id": iid,
                    "name": g,
                    "level": "unknown",
                })
            for o in offices:
                off_seq += 1
                new_offices.append({
                    "off_id": f"OFF-{off_seq:04d}",
                    "item_id": iid,
                    "office_name": o,
                })

print(f"\n{'='*60}")
print(f"批量补层结果")
print(f"{'='*60}")
print(f"新增 ents 实体: {len(new_ents)} 条")
print(f"新增 geo 地理: {len(new_geos)} 条")
print(f"新增 offices 官职: {len(new_offices)} 条")

# 合并到现有层
all_ents = layers["ents"] + new_ents
all_geos = layers["geo"] + new_geos
all_offices = layers["offices"] + new_offices

# 保存
for name, data in [("ents", all_ents), ("geo", all_geos), ("offices", all_offices)]:
    outpath = os.path.join(ROOT, "_layers", f"{name}.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"已保存: {outpath} ({len(data)}条)")
