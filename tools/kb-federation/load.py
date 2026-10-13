"""load.py —— L 阶段：中间表 → Tier1（items / records）+ 写 catalog

忠实装载、先删后插幂等：
- items：只存条目指针（fingerprint_ref = item_id），不抄正文大段（守「原文只在指纹库」）
- records：每 Slice.records 逐条 INSERT（payload = 整条记录 JSON 原文）
- layer_catalog / layer_fields：目录登记（T0 再细化字段 role）
- load_runs：装载审计
"""

import json
import os
import subprocess

from kbdb import upsert, wipe_book, md5, now, REPO_ROOT
from adapters import make_adapter, LAYER_DECL, BOOK_REGISTRY, BOOK_NAMES, book_source_root


def source_rev(book_id):
    """源工程目录的快照 id —— 增量水印（见 docs/联邦库原表增量与稀疏诊断.md §1）。

    优先取「最近一次触及该目录的 git 提交」(git log -1 --format=%H -- <dir>)：
    仅当该书源被提交改动时 rev 才变，符合 git 工作流。
    若 git 不可用 / 目录不存在 / 尚未提交，退回「目录内容指纹」(文件名+大小+mtime 的 md5)，
    连未提交的改动也能感知。
    """
    root = book_source_root(book_id)
    try:
        out = subprocess.run(
            ["git", "-C", REPO_ROOT, "log", "-1", "--format=%H", "--", root],
            capture_output=True, text=True, timeout=15,
        )
        h = (out.stdout or "").strip()
        if h:
            return h
    except Exception:
        pass
    # 退回目录内容指纹
    try:
        h = hashlib_md5()
        if not os.path.isdir(root):
            return None
        for dirpath, _, fnames in os.walk(root):
            for f in sorted(fnames):
                fp = os.path.join(dirpath, f)
                try:
                    st = os.stat(fp)
                    h.update(f.encode("utf-8"))
                    h.update(str(st.st_size).encode())
                    h.update(str(int(st.st_mtime)).encode())
                except OSError:
                    continue
        return "dir:" + h.hexdigest()
    except Exception:
        return None


def hashlib_md5():
    import hashlib
    return hashlib.md5()


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
                "source_rev": source_rev(book_id),
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
    # 防御性检查：插入的去重主键数若小于记录数，说明同 (book,layer,local_id)
    # 出现重复 —— 通常是某书 ID 按卷重排却没加卷前缀导致的折叠。
    distinct = con.execute(
        "SELECT COUNT(*) FROM (SELECT 1 FROM records WHERE book_id=? "
        "GROUP BY book_id,layer_key,local_id)",
        (book_id,),
    ).fetchone()[0]
    return len(item_rows), len(rec_rows), distinct


def load_book(con, book_id, *, wipe_first=True, commit=True):
    adapter = make_adapter(book_id)
    if wipe_first:
        wipe_book(con, book_id)
    slices = adapter.discover()
    n_cat, n_field = register_catalog(con, book_id, slices)
    n_items, n_rec, distinct = load_records(con, book_id, slices, adapter)
    counts = {k: len(s.records) for k, s in slices.items()}
    # 主键折叠告警（F2 关键断言：六书 ID 撞号必须由复合主键消解，不能静默丢记录）
    collision_lost = n_rec - distinct
    if collision_lost > 0:
        print(
            f"  ⚠️ 警告：{book_id} 有 {collision_lost} 条记录因 "
            f"(book,layer,local_id) 重复被 OR REPLACE 折叠 —— 请检查 ID 命名空间！"
        )
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
        "distinct": distinct,
        "collision_lost": collision_lost,
        "catalog": n_cat,
        "fields": n_field,
    }
