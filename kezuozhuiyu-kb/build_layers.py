# -*- coding: utf-8 -*-
"""《客座赘语》知识工程 | 统一打包器 build_layers

读 13 个 _src/_<layer>_ai_<NN>.py 的 RECORDS，逐层：
  1. 源数据字段完整性检查（must_fields 报告到 _validate/<layer>_<NN>_缺失清单.txt）；
  2. 按层全局顺序分配业务 ID（IdAllocator，宽 4 位：ENT-0001），排序键稳定（同卷同序→同 ID）；
  3. 从 _item_registry.json 注入 original/norm（不手抄原文）；
  4. ENT 层：在 original 中 find text 回填 start/end（找不到 -1/-1），normalized=text；
  5. NAM 层：names 列表 → entries dictlist（seq 从 1，courtesy_name/hometown/office 未明）；
  6. 引用回填：MING.ref_events 空 → 回填同条 EVT id；OPN.evidence_refs 空 → 回填同条 CIT id；
     各 *_ent_ids 空槽按文本匹配本卷 ENT alias 回填，未命中留空 []；
  7. 写 _layers/<layer>_<NN>.json（13 个）+ _kg_join.json / _deliver/_kg_join_flat.csv / _build/kg_join_report.json。

重跑：python build_layers.py [--volumes 01 02] [--check]
"""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_pack_base import (  # noqa: E402
    BUILD_DIR,
    BUILD_VERSION,
    DELIVER_DIR,
    JOIN_LAYER_KEYS,
    LAYERS,
    LAYER_JSON_DIR,
    REGISTRY_PATH,
    VALIDATE_DIR,
    VOLUME_NAME,
    IdAllocator,
    build_context,
    ensure_dirs,
    layer_json_path,
    layer_sort_key,
    load_registry,
    load_source,
    make_id,
    now_stamp,
    read_json,
    write_csv,
    write_json,
    write_text,
)

# 打包器负责注入、源数据可省的字段（不参与"源数据缺失"报告）
INJECTED_FIELDS = {"start", "end", "original", "norm", "volume"}
# 顶层 *_ent_ids / ent_ids 用文本匹配回填的兜底（保持 [] 即可不报错）
ID_LIST_FIELD_SUFFIX = "_ent_ids"


def src_missing(layer: str, record: dict) -> list[str]:
    cfg = LAYERS[layer]
    return [
        f for f in cfg["must_fields"] if f not in INJECTED_FIELDS and f not in record
    ]


def iter_ent_id_slots(record: dict):
    """遍历记录中所有 {text, *_ent_ids} 形态的字典字段及其 ent_ids 键。"""
    for k, v in record.items():
        if isinstance(v, dict):
            for sub_k, sub_v in v.items():
                if (
                    sub_k.endswith(ID_LIST_FIELD_SUFFIX)
                    and isinstance(sub_v, list)
                    and not sub_v
                ):
                    yield v, sub_k
        elif k.endswith(ID_LIST_FIELD_SUFFIX) and isinstance(v, list) and not v:
            # NAM 顶层 ent_ids：由 entries 的 person 文本回填
            yield record, k


def build_ent_alias(records: list[dict]) -> dict[str, str]:
    """本卷 ENT alias：text -> ent_id（同 text 取第一条；type 不参与面向库表的 alias）。"""
    alias: dict[str, str] = {}
    for r in records:
        text = str(r.get("text") or "").strip()
        eid = r.get("ent_id", "")
        if text and eid and text not in alias:
            alias[text] = eid
    return alias


_PAREN_RE = re.compile(r"[（(][^（()）]*[）)]")
_PLACEHOLDER = {"未明", "不明", "无", ""}


def _resolve_ent(text: str, alias: dict[str, str]) -> str | None:
    """引用文本 -> ENT id。匹配顺序：精确 → 剥离全/半角括注 → 双向子串。

    - 精确：text 原样命中 alias；
    - 剥括注：如"皇太子（朱高炽）"→"皇太子"；"朱元璋（高皇帝）"→"高皇帝"
      （优先剥后整体命中；整体仍不中时再匹配括注内文字）；
    - 子串：源 text 与 ENT text 互为子串（如"郑宣化"∈"郑宣化太守"、
      "杨溥"∈"洗马杨溥"），取长度最短者（最短词形最接近裸名）。
    """
    if not text:
        return None
    hit = alias.get(text)
    if hit:
        return hit
    core = _PAREN_RE.sub("", text).strip()
    if core and core != text:
        hit = alias.get(core)
        if hit:
            return hit
        hit = alias.get(
            text.replace("（", "").replace("）", "").replace("(", "").replace(")", "")
        )
        if hit:
            return hit
    # 括注内文字单独试（如"朱元璋（高皇帝）"→核心"朱元璋"不中，括注"高皇帝"中）
    for part in re.findall(r"[（(][^（()）]*[）)]", text):
        inner = part[1:-1].strip()
        if inner:
            hit = alias.get(inner)
            if hit:
                return hit
    # 双向子串兜底：源 text 与某个 ENT text 互为子串时取最短
    if len(text) >= 2 and text not in _PLACEHOLDER:
        cands = [k for k in alias if len(k) >= 2 and (k in text or text in k)]
        if cands:
            cands.sort(key=len)
            return alias[cands[0]]
    return None


def fill_ent_refs(record: dict, alias: dict[str, str], miss_log: list[dict]) -> None:
    """回填 {text, *_ent_ids} 空槽。命中写入；未命中记 miss（note=引用未解析）。"""
    # NAM 顶层 ent_ids：entries[].person 文本匹配
    if record.get("nam_id"):
        entries = record.get("entries") or []
        ids: list[str] = []
        for e in entries:
            t = str(e.get("person") or "").strip()
            eid = _resolve_ent(t, alias)
            if eid:
                ids.append(eid)
        if ids:
            record["ent_ids"] = ids
    # 通用 {text, *_ent_ids} 空槽
    for holder, key in list(iter_ent_id_slots(record)):
        text = ""
        if isinstance(holder, dict):
            text = str(holder.get("text") or holder.get("name") or "").strip()
        if not text:
            continue
        if text in _PLACEHOLDER:
            continue
        eid = _resolve_ent(text, alias)
        if eid:
            holder[key] = [eid]
        else:
            miss_log.append(
                {
                    "layer": record.get("_layer", ""),
                    "item_id": record.get("item_id"),
                    "field": key,
                    "text": text,
                    "note": "引用未解析",
                }
            )


def finalize_record(
    layer: str, volume: str, src: dict, alloc: IdAllocator, registry: dict
) -> dict:
    cfg = LAYERS[layer]
    rec: dict = dict(src)
    rec["volume"] = volume
    rec[cfg["id_field"]] = alloc.next()
    rec["_layer"] = layer
    from _kg_pack_base import inject_original

    inject_original(rec, registry)

    if layer == "ent":
        text = str(rec.get("text") or "")
        start = rec.get("start")
        end = rec.get("end")
        if start is None or end is None:
            pos = rec.get("original", "").find(text)
            rec["start"] = pos if pos >= 0 else -1
            rec["end"] = (pos + len(text)) if pos >= 0 else -1
        rec.setdefault("normalized", text)
        rec.setdefault("confidence", 0.95)
        rec.setdefault("source", "")
    elif layer == "nam":
        names = rec.get("names")
        if isinstance(names, list) and "entries" not in rec:
            tv = rec.get("name")
            rec["entries"] = [
                {
                    "seq": i,
                    "person": str(n),
                    "courtesy_name": "未明",
                    "hometown": "未明",
                    "office": "未明",
                }
                for i, n in enumerate(names, 1)
            ]
        rec.setdefault("ent_ids", [])
    # 层内留空字段显式"未明"兜底（ENUM 为"未明"或文档要求时）
    for f in ("when", "where", "era"):
        if f in cfg.get("must_fields", ()) or f in rec:
            if (
                f not in rec
                or rec[f] is None
                or (isinstance(rec[f], str) and not rec[f].strip())
            ):
                if f in ("when", "where"):
                    rec[f] = "未明"
    return rec


def refill_same_item(records: list[dict], layer: str, src_field: str) -> None:
    """MING.ref_events / OPN.evidence_refs 空 → 回填同条 EVT / CIT id。"""
    ids_by_item: dict[str, list[str]] = {}
    for r in records:
        if r.get("_layer") == layer:
            id_field = LAYERS[layer]["id_field"]
            ids_by_item.setdefault(str(r.get("item_id")), []).append(
                str(r.get(id_field) or "")
            )
    for r in records:
        if r.get("_layer") != layer or r.get("_skip"):
            continue
        cur = r.get(src_field) or []
        if not cur:
            r[src_field] = list(ids_by_item.get(str(r.get("item_id")), []))


def build_layer(
    layer: str, volume: str, alloc: IdAllocator, registry: dict
) -> tuple[list[dict], list[dict]]:
    cfg = LAYERS[layer]
    src_records = load_source(layer, volume)
    records: list[dict] = []
    missing_log: list[dict] = []
    for src in src_records:
        item_id = str(src.get("item_id") or "").strip()
        if not item_id or item_id not in registry:
            missing_log.append(
                {
                    "layer": layer,
                    "item_id": item_id,
                    "field": "item_id",
                    "note": "registry 无此条目",
                }
            )
            continue
        miss = src_missing(layer, src)
        if miss:
            missing_log.append(
                {
                    "layer": layer,
                    "item_id": item_id,
                    "field": ",".join(miss),
                    "note": "源数据缺字段",
                }
            )
        records.append(finalize_record(layer, volume, src, alloc, registry))
    records.sort(key=lambda r: layer_sort_key(r, cfg))
    # 排序后 ID 已按序分配；由于 alloc 已连续，直接用源序重分配以保持 item 内顺序稳定
    for i, r in enumerate(records, 1):
        r[cfg["id_field"]] = make_id(cfg["id_prefix"], i, width=4)
    if layer == "ent":
        pass  # start/end 已回填
    return records, missing_log


def build_all(volumes: list[str]) -> None:
    registry = load_registry()
    per_layer: dict[str, list[dict]] = {}
    all_ids: dict[str, str] = {}  # 层 -> id_field
    global_missing: list[dict] = []
    ent_alias: dict[str, str] = {}

    # 第一阶段：逐层构建（ENT 先跑，供 alias）
    layer_order = ["ent"] + [k for k in LAYERS if k != "ent"]
    for layer in layer_order:
        if layer not in LAYERS:
            continue
        cfg = LAYERS[layer]
        alloc = IdAllocator(cfg["id_prefix"])
        records, missing = [], []
        for vol in volumes:
            recs, mis = build_layer(layer, vol, alloc, registry)
            records.extend(recs)
            missing.extend(mis)
        per_layer[layer] = records
        all_ids[layer] = cfg["id_field"]
        global_missing.extend(missing)
        if layer == "ent":
            ent_alias = build_ent_alias(records)

    # 第二阶段：引用回填
    # 1) 通用 *_ent_ids 槽
    for layer, records in per_layer.items():
        if layer == "ent":
            continue
        for r in records:
            fill_ent_refs(r, ent_alias, global_missing)
    # 2) MING.ref_events -> 同条 EVT；OPN.evidence_refs -> 同条 CIT
    if "event" in per_layer:
        for r in list(per_layer.get("ming", [])):
            if not (r.get("ref_events") or []):
                same = [
                    x
                    for x in per_layer["event"]
                    if str(x.get("item_id")) == str(r.get("item_id"))
                ]
                r["ref_events"] = [x["event_id"] for x in same]
    if "cit" in per_layer:
        for r in list(per_layer.get("opn", [])):
            if not (r.get("evidence_refs") or []):
                same = [
                    x
                    for x in per_layer["cit"]
                    if str(x.get("item_id")) == str(r.get("item_id"))
                ]
                r["evidence_refs"] = [x["cit_id"] for x in same]

    # 第三阶段：写每卷 JSON + 缺失清单
    from collections import defaultdict

    by_layer_vol: dict = defaultdict(lambda: defaultdict(list))
    for layer, records in per_layer.items():
        for r in records:
            by_layer_vol[layer][str(r.get("volume"))].append(r)
    for layer, vol_map in by_layer_vol.items():
        for vol, recs in vol_map.items():
            cfg = LAYERS[layer]
            payload = {
                "layer": layer,
                "volume": vol,
                "name": VOLUME_NAME.get(vol, ""),
                "id_prefix": cfg["id_prefix"],
                "id_field": cfg["id_field"],
                "count": len(recs),
                "generated_at": now_stamp(),
                "builder": BUILD_VERSION,
                "records": recs,
            }
            write_json(layer_json_path(layer, vol), payload)
    # 缺失/待核清单（写文件，问题数供 T3 用）
    ensure_dirs()
    for layer in LAYERS:
        layer_miss = [m for m in global_missing if m.get("layer") == layer]
        if layer_miss:
            lines = [
                f"{m['item_id']} | {m.get('field', '')} | {m.get('text', '')} | {m.get('note', '')}"
                for m in layer_miss
            ]
            write_text(
                VALIDATE_DIR / f"{layer}_{volumes[0]}_缺失清单.txt",
                "\n".join(lines) + "\n",
            )

    # 第四阶段：跨层 join
    build_join(volumes, per_layer, registry, global_missing)


def build_join(
    volumes: list[str],
    per_layer: dict[str, list[dict]],
    registry: dict,
    missing_log: list[dict],
) -> None:
    by_layer_item: dict[str, dict[str, list[dict]]] = {}
    for layer, records in per_layer.items():
        idx: dict[str, list[dict]] = {}
        for r in records:
            idx.setdefault(str(r.get("item_id")), []).append(r)
        by_layer_item[layer] = idx

    rows: list[dict] = []
    layer_hits: dict[str, int] = {k: 0 for k in JOIN_LAYER_KEYS}
    for item_id in sorted(
        registry, key=lambda k: (k.split("-")[0], int(k.split("-")[1]))
    ):
        vol = item_id.split("-")[0]
        if vol not in volumes:
            continue
        row: dict = {
            "item_id": item_id,
            "volume": vol,
            "volume_name": VOLUME_NAME.get(vol, ""),
            "source": f"_extract/{vol}_{VOLUME_NAME.get(vol, '')}.txt",
        }
        count = 0
        for layer, key in JOIN_LAYER_KEYS.items():
            recs = by_layer_item.get(layer, {}).get(item_id, [])
            id_field = LAYERS[layer]["id_field"]
            row[key] = [r.get(id_field) for r in recs if r.get(id_field)]
            if recs:
                count += 1
                layer_hits[key] = layer_hits.get(key, 0) + len(recs)
        row["layer_count"] = count

        # 人读标签
        def labels(layer: str, field: str) -> list[str]:
            out: list[str] = []
            for r in by_layer_item.get(layer, {}).get(item_id, []):
                v = r.get(field)
                if isinstance(v, dict):
                    v = v.get("text", "")
                s = str(v or "").strip()
                if s and s not in out:
                    out.append(s)
            return out

        def dict_labels(layer: str, field: str) -> list[str]:
            out: list[str] = []
            for r in by_layer_item.get(layer, {}).get(item_id, []):
                v = r.get(field)
                if isinstance(v, dict):
                    v = v.get("text", "")
                s = str(v or "").strip()
                if s and s not in out:
                    out.append(s)
            return out

        row["event_actions"] = labels("event", "action")
        rel_pairs: list[str] = []
        for r in by_layer_item.get("rel", {}).get(item_id, []):
            a = dict_labels("rel", "person_a") or dict_labels("rel", "person_a")
            pa = r.get("person_a")
            pb = r.get("person_b")
            pa = pa.get("text", "") if isinstance(pa, dict) else pa
            pb = pb.get("text", "") if isinstance(pb, dict) else pb
            pair = f"{pa or '未明'}—{pb or '未明'}"
            if pair not in rel_pairs:
                rel_pairs.append(pair)
        row["rel_pairs"] = rel_pairs
        row["nam_names"] = labels("nam", "name")
        row["cit_works"] = dict_labels("cit", "cited_work")
        row["obj_names"] = dict_labels("obj", "name")
        row["cus_terms"] = labels("cus", "term")
        row["opn_topics"] = labels("opn", "topic")
        row["ming_whats"] = labels("ming", "what")
        row["appt_offices"] = dict_labels("appt", "office")
        row["geo_names"] = dict_labels("geo", "name")
        row["lit_titles"] = labels("lit", "title")
        tr = by_layer_item.get("trl", {}).get(item_id, [])
        row["translation"] = str(tr[0].get("translation", "")) if tr else ""
        entry = registry.get(item_id, {})
        row["original"] = entry.get("original", "")
        row["norm"] = entry.get("norm", "")
        rows.append(row)

    total = len(rows)
    dist: dict[int, int] = {}
    for r in rows:
        dist[r["layer_count"]] = dist.get(r["layer_count"], 0) + 1
    report = {
        "generated_at": now_stamp(),
        "builder": BUILD_VERSION,
        "volumes": volumes,
        "items": total,
        "layer_hits": layer_hits,
        "layer_count_distribution": {str(k): v for k, v in sorted(dist.items())},
        "items_with_any_layer": sum(v for k, v in dist.items() if k > 0),
        "empty_items": sum(1 for r in rows if r["layer_count"] == 0),
    }
    write_json(
        LAYER_JSON_DIR / "_kg_join.json",
        {
            "generated_at": now_stamp(),
            "builder": BUILD_VERSION,
            "count": len(rows),
            "rows": rows,
        },
    )
    csv_fields = list(JOIN_LAYER_KEYS.values())
    flat_fields = (
        ["item_id", "volume", "volume_name", "layer_count"]
        + csv_fields
        + [
            "event_actions",
            "rel_pairs",
            "nam_names",
            "cit_works",
            "obj_names",
            "cus_terms",
            "opn_topics",
            "ming_whats",
            "appt_offices",
            "geo_names",
            "lit_titles",
            "translation",
            "source",
            "original",
            "norm",
        ]
    )
    write_csv(DELIVER_DIR / "_kg_join_flat.csv", rows, flat_fields)
    write_json(BUILD_DIR / "kg_join_report.json", report)

    print("=" * 68)
    print(f"《客座赘语》知识工程 | 统一打包 build_layers（卷 {','.join(volumes)}）")
    print("=" * 68)
    for layer in LAYERS:
        recs = per_layer.get(layer, [])
        miss = [m for m in missing_log if m.get("layer") == layer]
        print(f"  {layer:<5} {len(recs):>3} 条 | 缺字段 {len(miss)}")
    print(
        f"  跨层  _kg_join {total} 条 | 零层条目 {report['empty_items']} | "
        f"命中至少一层 {report['items_with_any_layer']}"
    )
    print(
        f"[产物] _layers/*.json ×{len(LAYERS)} + _kg_join.json | "
        f"_deliver/_kg_join_flat.csv | _build/kg_join_report.json"
    )


ZIP_STANDARD_ITEMS = 17  # 13 层 json + 4 个跨层/报告产物


def make_zip(volumes: list[str]) -> Path:
    """统一标准打包：13 层 json + _kg_join.json + _kg_join_flat.csv
    + kg_join_report.json + t3_report_<NN>.json，共 17 项（arcname 取 basename）。

    zip 命名：kezuozhuiyu_vol{NN}_layers.zip（多卷时 _ 连接），落 _deliver/。
    t3 报告由 validate_layers 生成，缺失时降级打包 16 项并打印提示。
    """
    ensure_dirs()
    zip_name = "kezuozhuiyu_vol{}_layers.zip".format("_".join(volumes))
    zip_path = DELIVER_DIR / zip_name

    manifest: list[tuple[str, Path]] = []
    for vol in volumes:
        for layer in LAYERS:
            manifest.append((f"{layer}_{vol}.json", layer_json_path(layer, vol)))
    manifest.append(("_kg_join.json", LAYER_JSON_DIR / "_kg_join.json"))
    manifest.append(("_kg_join_flat.csv", DELIVER_DIR / "_kg_join_flat.csv"))
    manifest.append(("kg_join_report.json", BUILD_DIR / "kg_join_report.json"))
    for vol in volumes:
        manifest.append(
            (f"t3_report_{vol}.json", VALIDATE_DIR / f"t3_report_{vol}.json")
        )

    missing = [(name, p) for name, p in manifest if not p.exists()]
    if missing:
        for name, p in missing:
            if name.startswith("t3_report_"):
                print(
                    f"[提示] 缺 {name}（先跑 validate_layers.py --volumes {volumes[0]}"
                    f" 再重跑 --zip 可补全 17 项）"
                )
            else:
                print(f"[错误] 缺 {p}，无法打包", file=sys.stderr)
        if any(not n.startswith("t3_report_") for n, _ in missing):
            raise SystemExit(1)
        manifest = [(n, p) for n, p in manifest if p.exists()]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, p in manifest:
            zf.write(p, arcname=name)
    print(
        f"[打包] {zip_path} | {len(manifest)} 项"
        f"{'' if len(manifest) == ZIP_STANDARD_ITEMS else f'（标准{ZIP_STANDARD_ITEMS}项，t3 后补）'}"
    )
    return zip_path


def main() -> None:
    args, volumes = build_context("统一打包 build_layers")
    ensure_dirs()
    try:
        build_all(volumes)
        if args.zip:
            make_zip(volumes)
    except FileNotFoundError as exc:
        print(f"[错误] {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
