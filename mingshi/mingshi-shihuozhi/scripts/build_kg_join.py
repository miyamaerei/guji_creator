#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Cross-Layer Join —— 条 → 各层记录的反向索引（SKILL §13）。

产出（项目根，与 _data/ 底座并列）：
  _kg_join.json      list[{item_id, volume, layers:{8层ID列表}, layer_count}]
  _kg_join_flat.csv  item_id, volume, layer, id 扁平行

纪律：目录名/文件名前缀/索引槽位名三处同源（坑 #28/#29，全部复数）；
     交付须报空条目率（SKILL §13.2）。
"""

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    BASE_DIR,
    KG_JOIN_FILE,
    KG_JOIN_FLAT_FILE,
    LAYER_SPECS,
    REGISTRY_FILE,
    load_json,
    layer_dir,
)


def _records_of(key: str) -> list:
    """读某层全部记录（registry 型按子类展开；list 型按记录展开）。"""
    spec = LAYER_SPECS[key]
    d = layer_dir(key)
    out: list[dict] = []
    if not d.exists():
        return out
    for f in sorted(d.glob("*.json")):
        data = load_json(f, [])
        if spec["kind"] == "registry":
            for _sub, items in (data or {}).items():
                for r in items or []:
                    out.append(r)
        else:
            if isinstance(data, dict):
                data = data.get("records", data.get("items", []))
            for r in data or []:
                out.append(r)
    return out


def main() -> None:
    print("=== Build Cross-Layer Join ===")
    reg = load_json(REGISTRY_FILE, {})
    joined: dict[str, dict] = {
        iid: {
            "item_id": iid,
            "volume": reg[iid]["volume"],
            "layers": {k: [] for k in LAYER_SPECS},
            "layer_count": 0,
        }
        for iid in reg
    }
    layer_totals: dict[str, int] = {}
    for key in LAYER_SPECS:
        recs = _records_of(key)
        layer_totals[key] = len(recs)
        for r in recs:
            iid = r.get("item_id")
            if isinstance(iid, list):
                for one in iid:
                    if one in joined:
                        joined[one]["layers"][key].append(r.get("id", ""))
            elif iid in joined:
                joined[iid]["layers"][key].append(r.get("id", ""))
        print(f"  {key:<8} 索引 {layer_totals[key]} 条")

    rows = []
    for j in joined.values():
        j["layer_count"] = sum(1 for ids in j["layers"].values() if ids)
        rows.append(j)

    empty = sum(1 for j in rows if j["layer_count"] == 0)
    total = len(rows)
    empty_rate = f"{empty}/{total} ({empty / total * 100:.1f}%)" if total else "0/0"
    print(f"\n  空条目率: {empty_rate}")

    with open(KG_JOIN_FILE, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"  [写] {KG_JOIN_FILE.relative_to(BASE_DIR)}  ({total} 条)")

    flat = []
    for j in rows:
        for key, ids in j["layers"].items():
            for rid in ids:
                flat.append(
                    {
                        "item_id": j["item_id"],
                        "volume": j["volume"],
                        "layer": key,
                        "id": rid,
                    }
                )
    with open(KG_JOIN_FLAT_FILE, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["item_id", "volume", "layer", "id"])
        w.writeheader()
        for r in flat:
            w.writerow(r)
    print(f"  [写] {KG_JOIN_FLAT_FILE.relative_to(BASE_DIR)}  ({len(flat)} 行)")
    print("=== Build Cross-Layer Join Complete ===")


if __name__ == "__main__":
    main()
