# -*- coding: utf-8 -*-
"""
《水东日记》知识工程 —— L1 实体主键生成器（build_ent_keys）
=============================================================
读 sources/_ent_ai_NN.py（AI 逐条判定标注，只写条号+解读）
→ 校验 → 计算 start/end（在 original 中定位）→ 归一汇总
→ 全局主键表 ENT-xxx + alias_index（先查后建，随卷累积，幂等重跑）

产物：
  data/ent/ent_NN.json            每卷标注（含注入 original）
  data/ent/ent_keys.json          主键表 + alias_index + 归一汇总
  data/ent/ent_surfaces.csv       词形索引（text → ent_id）
"""
import argparse
import csv
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from _kg_enums import ENTITY_TYPES, ENTITY_TYPES_VERSION, ID_PREFIXES, check_enum

ENT_PREFIX = ID_PREFIXES["ent"]


def next_ent_id(keys):
    """从现有主键表取下一个 ENT 序号。"""
    n = 0
    for ent_id in keys.get("entities", []):
        m = re.match(rf"^{re.escape(ENT_PREFIX)}(\d+)$", ent_id["ent_id"])
        if m:
            n = max(n, int(m.group(1)))
    return n + 1


def locate(original, text):
    """在 original 中定位 text 的 (start, end)；找不到返回 (None, None)。"""
    idx = original.find(text)
    if idx < 0:
        return None, None
    return idx, idx + len(text)


def build(volumes=None, verbose=True):
    os.makedirs(os.path.join(common.DATA_DIR, "ent"), exist_ok=True)
    keys_path = os.path.join(common.DATA_DIR, "ent", "ent_keys.json")
    keys = common.load_json(keys_path) if os.path.exists(keys_path) else {
        "normalized_inventory": [], "entities": [], "alias_index": {},
        "surfaces": {}, "register_version": ENTITY_TYPES_VERSION,
    }
    reg = common.load_registry()
    issues = []

    vols = common.iter_volumes()
    if volumes:
        vols = [v for v in vols if v[0] in volumes]

    for vol_no, vol_file in vols:
        data = common.load_source("ent", vol_no)
        if data is None:
            msg = f"卷 {vol_no}：缺 ent 源数据 sources/_ent_ai_{vol_no}.py"
            issues.append(msg)
            if verbose:
                print("[缺漏]", msg)
            continue
        annotations = data if isinstance(data, list) else data.get("annotations", [])
        vol_out = {"volume": vol_no, "annotations": []}
        for ann in annotations:
            item_id = ann.get("item_id")
            if not re.match(r"^\d{2}-\d{3}$", str(item_id or "")):
                issues.append(f"卷 {vol_no}：非法 item_id {item_id!r}")
                continue
            item = reg.get(item_id)
            if item is None:
                issues.append(f"卷 {vol_no}：item_id {item_id} 不在指纹库")
                continue
            text = ann.get("text", "")
            if not text:
                issues.append(f"卷 {vol_no} {item_id}：缺少 text 字段")
                continue
            etype = ann.get("type", "unknown")
            try:
                check_enum(etype, ENTITY_TYPES, "实体类型", ENTITY_TYPES_VERSION)
            except ValueError as e:
                issues.append(f"卷 {vol_no} {item_id}：{e}")
                continue
            normalized = ann.get("normalized") or text
            start, end = locate(item["original"], text)
            rec = {
                "id": None,  # 打包器分配
                "item_id": item_id,
                "text": text,
                "type": etype,
                "start": start,
                "end": end,
                "normalized": normalized,
                "confidence": ann.get("confidence", 0.5),
                "source": ann.get("source", "原文片段"),
                "original": item["original"],
                "norm": item["norm"],
            }
            vol_out["annotations"].append(rec)

        # 合并进主键表（先查后建）
        alias_index = keys["alias_index"]
        surfaces = keys["surfaces"]
        entities = keys["entities"]
        inventory = keys["normalized_inventory"]
        for rec in vol_out["annotations"]:
            key = rec["normalized"]
            if key in alias_index:
                rec["id"] = alias_index[key]
            else:
                nid = f"{ENT_PREFIX}{next_ent_id(keys):03d}"
                alias_index[key] = nid
                entities.append({
                    "ent_id": nid, "normalized": key, "type": rec["type"],
                    "count": 0, "first_source": rec["item_id"], "surfaces": [],
                })
                inventory.append({
                    "normalized": key, "type": rec["type"], "count": 0,
                    "first_source": rec["item_id"], "surfaces": [],
                })
                rec["id"] = nid
            ent = next(e for e in entities if e["ent_id"] == rec["id"])
            ent["count"] += 1
            if rec["item_id"] not in ent["surfaces"]:
                ent["surfaces"].append(rec["item_id"])
            inv = next(i for i in inventory if i["normalized"] == key)
            inv["count"] += 1
            if rec["item_id"] not in inv["surfaces"]:
                inv["surfaces"].append(rec["item_id"])
            # 词形索引（surface text → ent_id，复合词形可手工映射补充）
            if rec["text"] not in surfaces:
                surfaces[rec["text"]] = rec["id"]

        common.write_json(os.path.join(common.DATA_DIR, "ent", f"ent_{vol_no}.json"), vol_out)
        if verbose:
            print(f"卷 {vol_no}: {len(vol_out['annotations'])} 条标注，累计实体 {len(entities)}")

    common.write_json(keys_path, keys)
    # 词形索引 CSV
    with io.open(os.path.join(common.DATA_DIR, "ent", "ent_surfaces.csv"), "w",
                 encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["surface", "ent_id"])
        for s, eid in sorted(keys["surfaces"].items(), key=lambda x: x[1]):
            w.writerow([s, eid])

    if issues:
        print(f"\n[校验问题 {len(issues)} 条]")
        for i in issues[:30]:
            print("  -", i)
    else:
        print("\n实体层校验通过（问题数 = 0）")
    print(f"实体主键 {len(keys['entities'])} 个，alias_index {len(keys['alias_index'])} 项")
    return issues


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="L1 实体主键生成器")
    ap.add_argument("--volumes", nargs="*", help="仅处理指定卷，如 --volumes 01 02")
    args = ap.parse_args()
    build(volumes=args.volumes)
