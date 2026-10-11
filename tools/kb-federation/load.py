"""load.py —— L 阶段：中间表 → Tier1（items / records）+ 写 catalog

忠实装载、先删后插幂等：
- items：只存条目指针（fingerprint_ref = item_id），不抄正文大段（守「原文只在指纹库」）
- records：每 Slice.records 逐条 INSERT（payload = 整条记录 JSON 原文）
- layer_catalog / layer_fields：目录登记（T0 再细化字段 role）
- load_runs：装载审计
"""

import json

from kbdb import upsert, wipe_book, md5, now
from adapters import make_adapter, LAYER_DECL, BOOK_REGISTRY, BOOK_NAMES


def register_catalog(con, book_id, slices):
    reg = BOOK_REGISTRY[book_id]
    name = BOOK_NAMES.get(book_id, book_id)
    upsert(
        con,
        "books",
        [
            {
                "book_id": book_id,
                "code": book_id,
                "name": name,
                "source_root": reg["root"],
                "schema_version": 1,
                "loaded_at": now(),
            }
        ],
        ["book_id"],
    )

    cat_rows = []
    field_rows = []
    for key, sl in slices.items():
        decl = LAYER_DECL.get(book_id, {}).get(key, ("annotation", "layers", ""))
        cat_rows.append(
            {
                "book_id": book_id,
                "layer_key": key,
                "layer_code": None,
                "layer_name": key,
                "container_kind": decl[1],
                "kind": decl[0],
                "id_prefix": decl[2] or None,
                "record_count": len(sl.records),
                "loaded_at": now(),
            }
        )
        fields = set()
        for r in sl.records:
            fields.update(r["payload"].keys())
        for f in sorted(fields):
            field_rows.append(
                {
                    "book_id": book_id,
                    "layer_key": key,
                    "field_name": f,
                    "field_type": "text",
                    "role": "attr",
                }
            )

    upsert(con, "layer_catalog", cat_rows, ["book_id", "layer_key"])
    # layer_fields 用 INSERT OR IGNORE：跨层同名字段主键不冲突
    for fr in field_rows:
        con.execute(
            "INSERT OR IGNORE INTO layer_fields"
            "(book_id,layer_key,field_name,field_type,role) VALUES(?,?,?,?,?)",
            (fr["book_id"], fr["layer_key"], fr["field_name"], fr["field_type"], fr["role"]),
        )
    return len(cat_rows), len(field_rows)


def load_records(con, book_id, slices, adapter):
    # items：从 fingerprints（本书条目指纹库）抽指针；不抄正文
    anchors = adapter.fingerprints()
    item_rows = []
    for a in anchors:
        norm = a.get("norm") or a.get("original") or ""
        item_rows.append(
            {
                "book_id": book_id,
                "item_id": a["item_id"],
                "volume": a.get("volume"),
                "title": norm[:50],  # 仅存前 50 字短摘要，非正文大段
                "fingerprint_ref": a["item_id"],  # 回查原文用（指向 kg_join.fingerprints）
                "layer_count": 0,
            }
        )
    upsert(con, "items", item_rows, ["book_id", "item_id"])

    # records：所有层统一落点（payload = 整条记录 JSON）
    rec_rows = []
    for key, sl in slices.items():
        for r in sl.records:
            payload = json.dumps(r["payload"], ensure_ascii=False)
            rec_rows.append(
                {
                    "book_id": book_id,
                    "layer_key": key,
                    "local_id": r["local_id"],
                    "item_id": r.get("item_id"),
                    "volume": r.get("volume"),
                    "payload": payload,
                    "checksum": md5(payload),
                    "loaded_at": now(),
                }
            )
    upsert(con, "records", rec_rows, ["book_id", "layer_key", "local_id"])
    return len(item_rows), len(rec_rows)


def load_book(con, book_id, *, wipe_first=True, commit=True):
    adapter = make_adapter(book_id)
    if wipe_first:
        wipe_book(con, book_id)
    slices = adapter.discover()
    n_cat, n_field = register_catalog(con, book_id, slices)
    n_items, n_rec = load_records(con, book_id, slices, adapter)
    counts = {k: len(s.records) for k, s in slices.items()}
    con.execute(
        "INSERT INTO load_runs(book_id,started_at,finished_at,status,record_counts) "
        "VALUES(?,?,?,?,?)",
        (book_id, now(), now(), "done", json.dumps(counts, ensure_ascii=False)),
    )
    if commit:
        con.commit()
    return {
        "book_id": book_id,
        "layers": counts,
        "items": n_items,
        "records": n_rec,
        "catalog": n_cat,
        "fields": n_field,
    }
