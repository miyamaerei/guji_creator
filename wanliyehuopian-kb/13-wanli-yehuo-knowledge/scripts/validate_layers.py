# -*- coding: utf-8 -*-
"""
Layer 文件校验器
检查 _layers/ 下所有 JSON 文件的结构完整性和数据一致性
"""
import json
import os
import re
import sys
from pathlib import Path
from collections import Counter

BASE = Path(__file__).resolve().parent.parent
LAYERS = BASE / "_layers"
REGISTRY = BASE / "_item_registry.json"

LAYER_TYPES = ["ents", "rules", "events", "appts", "rels", "opns", "cits", "mings", "tmes", "regs"]
ID_PREFIXES = {
    "ents": "ENT-",
    "rules": "RULE-",
    "events": "EVT-",
    "appts": "APPT-",
    "rels": "REL-",
    "opns": "OPN-",
    "cits": "CIT-",
    "mings": "MING-",
    "tmes": "YHB-TME-",
    "regs": "REG-",
}
ID_KEYS = {
    "ents": "ent_id",
    "rules": "rule_id",
    "events": "event_id",
    "appts": "appt_id",
    "rels": "rel_id",
    "opns": "opn_id",
    "cits": "cit_id",
    "mings": "ming_id",
    "tmes": "tme_id",
    "regs": "reg_id",
}

errors = []
warnings = []
stats = {}

def load_registry():
    if not REGISTRY.exists():
        warnings.append(f"_item_registry.json not found")
        return set()
    with open(REGISTRY, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {r["item_id"] for r in data.get("records", [])}

def check_json_parse(layer, vol, fpath):
    try:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        errors.append(f"[JSON] {layer}_{vol}: {e}")
        return None

def check_empty(data, layer, vol):
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        records = data.get("records", data)
        if isinstance(records, list):
            return len(records)
    errors.append(f"[STRUCT] {layer}_{vol}: unexpected top-level type")
    return 0

def check_ids(data, layer, vol):
    id_key = ID_KEYS[layer]
    prefix = ID_PREFIXES[layer]
    records = data if isinstance(data, list) else data.get("records", [])
    ids = []
    for r in records:
        if id_key not in r:
            errors.append(f"[ID] {layer}_{vol}: missing {id_key} in record")
            continue
        rid = r[id_key]
        ids.append(rid)
        if not rid.startswith(prefix):
            errors.append(f"[ID] {layer}_{vol}: {rid} doesn't start with {prefix}")
    dupes = {k: v for k, v in Counter(ids).items() if v > 1}
    for k, v in dupes.items():
        errors.append(f"[DUP] {layer}_{vol}: {k} appears {v} times")
    return ids

def check_item_refs(data, layer, vol, registry_ids):
    records = data if isinstance(data, list) else data.get("records", [])
    missing = []
    for r in records:
        item_id = r.get("item_id", r.get("source", ""))
        if item_id and registry_ids and item_id not in registry_ids:
            missing.append(item_id)
    if missing:
        unique_missing = set(missing)
        warnings.append(f"[REF] {layer}_{vol}: {len(unique_missing)} item_ids not in registry: {sorted(unique_missing)[:3]}...")
    return {r.get("item_id", r.get("source", "")) for r in records if r.get("item_id", r.get("source", ""))}

def main():
    print("=" * 60)
    print("《万历野获编》Layer 文件校验")
    print("=" * 60)

    registry = load_registry()
    registry_ids = registry
    print(f"Registry: {len(registry_ids)} items loaded\n")

    total_records = 0
    vol_stats = {}
    covered = set()

    for layer in LAYER_TYPES:
        layer_dir = LAYERS / layer
        if not layer_dir.exists():
            errors.append(f"[DIR] {layer_dir} missing")
            continue

        files = sorted(layer_dir.glob(f"{layer}_*.json"))
        for fpath in files:
            m = re.search(r'(\d+)', fpath.stem)
            vol = m.group(1) if m else "?"

            data = check_json_parse(layer, vol, fpath)
            if data is None:
                continue

            count = check_empty(data, layer, vol)
            ids = check_ids(data, layer, vol) if count > 0 else []
            covered |= check_item_refs(data, layer, vol, registry_ids)

            total_records += count
            vol_stats.setdefault(vol, {})
            vol_stats[vol][layer] = count

            status = "OK" if count > 0 else "EMPTY"
            if count > 0:
                print(f"  {layer}_{vol}: {count:4d} records  [{status}]")

    print(f"\n{'=' * 60}")
    print(f"Total records: {total_records}")
    print(f"{'=' * 60}")

    print(f"\n--- Per-volume summary ---")
    for vol in sorted(vol_stats.keys()):
        layers = vol_stats[vol]
        total = sum(layers.values())
        filled = sum(1 for v in layers.values() if v > 0)
        empty_layers = [k for k, v in layers.items() if v == 0]
        status = "FULL" if filled == 10 else f"PARTIAL({filled}/10)"
        empty_str = f" empty: {empty_layers}" if empty_layers else ""
        print(f"  Vol {vol}: {total:5d} records, {filled}/10 layers  [{status}]{empty_str}")

    print(f"\n--- Per-item coverage gate (GAP=0 required) ---")
    gaps = sorted(registry_ids - covered)
    by_vol = {}
    for iid in gaps:
        by_vol.setdefault(iid[:2], []).append(iid)
    cov_rate = (len(registry_ids) - len(gaps)) / max(len(registry_ids), 1) * 100
    print(f"  items covered: {len(registry_ids) - len(gaps)}/{len(registry_ids)} ({cov_rate:.1f}%)")
    if gaps:
        for v in sorted(by_vol):
            print(f"    GAP vol {v}: {len(by_vol[v])} 条未覆盖 (如 {by_vol[v][:3]})")
        errors.append(f"[GAP] {len(gaps)} registry items not referenced by any layer record")
    else:
        print("  GAP=0: 全部条目均被层记录引用")

    if errors:
        print(f"\n!!! ERRORS ({len(errors)}) !!!")
        for e in errors[:30]:
            print(f"  {e}")
        if len(errors) > 30:
            print(f"  ... and {len(errors) - 30} more")

    if warnings:
        print(f"\n--- WARNINGS ({len(warnings)}) ---")
        for w in warnings[:20]:
            print(f"  {w}")
        if len(warnings) > 20:
            print(f"  ... and {len(warnings) - 20} more")

    if not errors and not warnings:
        print("\nAll checks passed!")

    missing_vols = []
    for vol_num in range(1, 35):
        vol_str = f"{vol_num:02d}"
        if vol_str not in vol_stats:
            missing_vols.append(vol_str)
    if missing_vols:
        print(f"\n--- MISSING VOLUMES ---")
        print(f"  No layer files found for: {missing_vols}")

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
