# -*- coding: utf-8 -*-
"""跨层整合：实体归一 + struct.target 引用解析。
1. 按 ent.normalized 归并全局实体 → _ent_global.json
2. ent 记录加 global_ent_id 字段
3. struct.target 命中 normalized 的，加 target_ent_id
4. 重新打包到 _deliver/
"""
import json, os, csv
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
LAYERS = os.path.join(ROOT,"_layers")
DELIVER = os.path.join(ROOT,"_deliver")

ent = json.load(open(os.path.join(LAYERS,"ent","all.json"),encoding="utf-8"))["records"]
struct = json.load(open(os.path.join(LAYERS,"struct","all.json"),encoding="utf-8"))["records"]

# ---- 1. 按 normalized 归并全局实体 ----
groups = defaultdict(list)
for r in ent:
    groups[r["normalized"]].append(r)

global_ents = []
norm2gid = {}
for i, (norm, mentions) in enumerate(sorted(groups.items()), 1):
    gid = f"GENT-{i:04d}"
    norm2gid[norm] = gid
    types = set(m["type"] for m in mentions)
    # 取最常见 text 作为 display_text
    from collections import Counter
    texts = Counter(m["text"] for m in mentions)
    global_ents.append({
        "global_ent_id": gid,
        "normalized": norm,
        "display_text": texts.most_common(1)[0][0],
        "type": sorted(types)[0],  # 多类型取字典序第一，可后续人工调
        "mention_count": len(mentions),
        "mentioned_in_items": sorted(set(m["item_id"] for m in mentions)),
        "ent_ids": [m["ent_id"] for m in mentions],
    })

json.dump(global_ents, open(os.path.join(ROOT,"_ent_global.json"),"w",encoding="utf-8"),
          ensure_ascii=False, indent=2)

# ---- 2. ent 加 global_ent_id ----
norm2ent = {m["normalized"]: m for m in ent}
for r in ent:
    r["global_ent_id"] = norm2gid[r["normalized"]]

# ---- 3. struct.target → target_ent_id ----
hit = 0
for r in struct:
    t = r.get("target","")
    if t in norm2gid:
        r["target_ent_id"] = norm2gid[t]
        hit += 1
    else:
        r["target_ent_id"] = None

# ---- 4. 重写 _layers 和 _deliver ----
for layer, recs in [("ent",ent),("struct",struct)]:
    out = os.path.join(LAYERS,layer,"all.json")
    json.dump({"records":recs,"count":len(recs)}, open(out,"w",encoding="utf-8"),
              ensure_ascii=False, indent=2)
    out2 = os.path.join(DELIVER,f"{layer}.json")
    json.dump({"records":recs,"count":len(recs)}, open(out2,"w",encoding="utf-8"),
              ensure_ascii=False, indent=2)

# 全局实体表也进 deliver
json.dump(global_ents, open(os.path.join(DELIVER,"ent_global.json"),"w",encoding="utf-8"),
          ensure_ascii=False, indent=2)

# ---- 报告 ----
print("=== 实体归一 ===")
print(f"  ent: {len(ent)} 条 mention → {len(global_ents)} 个全局实体")
print(f"  跨条目重复实体: {sum(1 for g in global_ents if g['mention_count']>1)}")
print(f"  高频实体 top5:")
for g in sorted(global_ents, key=lambda x:-x['mention_count'])[:5]:
    print(f"    {g['global_ent_id']} {g['normalized']} ({g['type']}) ×{g['mention_count']}")

print(f"\n=== struct.target 引用解析 ===")
print(f"  命中 ent.normalized: {hit}/{len(struct)} ({hit*100//len(struct)}%)")
print(f"  未命中（target 是行为/动作，非实体）: {len(struct)-hit}")

print(f"\n=== _deliver/ 更新 ===")
print(f"  ent.json (加 global_ent_id)")
print(f"  struct.json (加 target_ent_id)")
print(f"  ent_global.json (新)")
