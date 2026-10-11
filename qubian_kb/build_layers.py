# -*- coding: utf-8 -*-
"""《蘧编》全卷打包器 build_layers.py
读取 _ai_NN.py 源数据 → 注入 original/norm（_item_registry.json）→ 按段位分配业务 ID
→ 计算 ent start/end → 输出每卷 JSON + 各层全局归一 + 跨层索引 _kg_join。
ID 段位：卷 NN 基础 = NN*500；每卷每层独立从 1 编起 → 前缀+(NN*500+序号)，全局唯一。
"""
import json, os, re, sys

KB = r"C:\Users\Administrator\DoubaoWork\chats\2026-10-10\new-chat-7\qubian_kb"
VOLUMES = [f"{i:02d}" for i in range(1, 21)]
LAYERS = ["ents", "appts", "evts", "rels", "lits", "mems", "chrs", "trls"]
PREFIX = {"ents": "ENT-", "appts": "APPT-", "evts": "EVT-", "rels": "REL-",
          "lits": "LIT-", "mems": "MEM-", "chrs": "CHR-", "trls": "TRL-"}
SRC_KEY = {"ents": "ents", "appts": "appts", "evts": "evts", "rels": "rels",
           "lits": "lits", "mems": "mems", "chrs": "chr", "trls": "trl"}

with open(os.path.join(KB, "_item_registry.json"), encoding="utf-8") as f:
    REG = json.load(f)

def load_src(vol):
    ns = {}
    with open(os.path.join(KB, f"_ai_{vol}.py"), encoding="utf-8") as f:
        code = f.read()
    exec(code, ns)
    return ns["SRC"]

def find_span(text, original):
    i = original.find(text)
    if i >= 0:
        return i, i + len(text)
    return None, None

def build():
    all_layers = {k: [] for k in LAYERS}
    volume_json = {}
    counter = {k: {} for k in LAYERS}  # layer -> volume -> seq

    for vol in VOLUMES:
        src = load_src(vol)
        vj = {"volume": vol, "records": {k: [] for k in LAYERS}}
        for item_id, data in src.items():
            if item_id not in REG:
                print(f"[ERR] item_id 不在指纹库: {item_id}")
                continue
            original = REG[item_id]["original"]
            norm = REG[item_id]["norm"]

            for layer in LAYERS:
                prefix = PREFIX[layer]
                seq = counter[layer].get(vol, 0)
                raw_list = data.get(SRC_KEY[layer], [])
                if layer == "chrs" and isinstance(raw_list, dict):
                    raw_list = [raw_list]
                elif layer == "trls" and isinstance(raw_list, str):
                    raw_list = [raw_list]
                for raw in raw_list:
                    seq += 1
                    if layer == "ents" and not isinstance(raw, dict):
                        raw = {"text": raw[0], "type": raw[1], "normalized": raw[2] if len(raw) > 2 else raw[0]}
                    elif layer == "rels" and not isinstance(raw, dict):
                        raw = {"person_a": raw[0], "person_b": raw[1], "type": raw[2],
                               "direction": raw[3] if len(raw) > 3 else "未明"}
                    elif layer == "trls" and isinstance(raw, str):
                        raw = {"translation": raw, "style": "注释性翻译"}
                    rec = dict(raw)
                    rec["id"] = f"{prefix}{int(vol) * 500 + seq}"
                    rec["volume"] = vol
                    rec["item_id"] = item_id
                    rec["original"] = original
                    if layer == "ents":
                        start, end = find_span(rec["text"], original)
                        rec["start"] = start
                        rec["end"] = end
                    vj["records"][layer].append(rec)
                    all_layers[layer].append(rec)
                counter[layer][vol] = seq

        # TRL 特殊：id 分配后仍按条（每卷每条约一条 trl 记录）
        volume_json[vol] = vj

    # 写出每卷 JSON
    for vol in VOLUMES:
        p = os.path.join(KB, f"_kg_{vol}.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(volume_json[vol], f, ensure_ascii=False, indent=1)
        print(f"[输出] _kg_{vol}.json")

    # 全局归一：实体按 normalized 合并（alias_index），其他层直接汇总
    ent_map = {}
    alias_index = {}
    for rec in all_layers["ents"]:
        key = rec.get("normalized") or rec["text"]
        if key not in ent_map:
            ent_map[key] = rec["id"]
            alias_index[key] = [rec["id"]]
        else:
            alias_index[key].append(rec["id"])
    for rec in all_layers["ents"]:
        rec["ent_id"] = ent_map.get(rec.get("normalized") or rec["text"])

    for layer in LAYERS:
        p = os.path.join(KB, f"归一_{layer}.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump({"layer": layer, "count": len(all_layers[layer]), "records": all_layers[layer]},
                      f, ensure_ascii=False, indent=1)
        print(f"[输出] 归一_{layer}.json（{len(all_layers[layer])} 条）")

    with open(os.path.join(KB, "alias_index.json"), "w", encoding="utf-8") as f:
        json.dump(alias_index, f, ensure_ascii=False, indent=1)
    print(f"[输出] alias_index.json（{len(alias_index)} 个归一实体）")

    # 跨层索引：按 item_id 聚合（全卷入层条目）
    join = {}
    for item_id in REG:
        if not REG[item_id].get("in_layer"):
            continue
        entry = {"item_id": item_id, "volume": item_id[:2], "title": REG[item_id].get("title", ""),
                 "layers": {k: [] for k in LAYERS}, "layer_count": 0}
        for layer in LAYERS:
            ids = [r["id"] for r in all_layers[layer] if r["item_id"] == item_id]
            entry["layers"][layer] = ids
            if ids:
                entry["layer_count"] += 1
        join[item_id] = entry
    with open(os.path.join(KB, "_kg_join.json"), "w", encoding="utf-8") as f:
        json.dump({"scope": "卷01-20", "items": len(join), "records": join}, f, ensure_ascii=False, indent=1)
    print(f"[输出] _kg_join.json（{len(join)} 条）")

    # 统计
    print("--- 各层总量 ---")
    for layer in LAYERS:
        print(f"  {layer}: {len(all_layers[layer])}")

if __name__ == "__main__":
    build()
