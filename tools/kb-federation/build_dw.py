"""build_dw.py —— 联邦库 → 数据仓库维度模型 ETL

从 kb.sqlite（联邦库）抽取，重建 kb_dw.sqlite（维度模型）。
架构：星座模型（Fact Constellation），详见 docs/数据仓库设计.md 与 kb_dw_schema.sql。

设计要点：
  - 本库是联邦库的纯派生，可重建、不入 git、绝不回写联邦库。
  - 维度/桥表/事实按依赖顺序装载；度量从 payload JSON 在 ETL 阶段解析成数值列，
    不让分析查询现解 JSON。
  - 时间维 best-effort（枚举/年份稀疏），见 _collect_years。
  - **增量装载**（默认，非 --full）：比对 kb.sqlite 的 load_runs.finished_at 与
    dw_watermark.last_loaded_at，只重抽「源库装载时刻更新过」的书；跨书解析层
    （bridge / dim_entity_resolved / f_resolution / 关系与引用的 resolved 列）因体量小
    （edges 仅 ~1500 行）每轮全局刷新，保证跨书一致。详见 docs/联邦库原表增量与稀疏诊断.md §1。

用法：
  python build_dw.py                # 增量装载（首次/无 dw 时退化为全量）
  python build_dw.py --full         # 强制全量重建
  python build_dw.py --src X.db --dw Y.db

零第三方依赖（仅标准库 sqlite3 / json / re / argparse）。
"""

import os
import re
import json
import sqlite3
import argparse
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SRC = os.path.join(HERE, "kb.sqlite")
DEFAULT_DW = os.path.join(HERE, "kb_dw.sqlite")
SCHEMA = os.path.join(HERE, "kb_dw_schema.sql")

# 年份提取窗口：元(末) / 明 / 清初
YEAR_RE = re.compile(r"(?<!\d)(1[12]\d{2}|1[3-6]\d{2}|1700)(?!\d)")


def connect(path):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=OFF")
    return con


def load_schema(dw):
    with open(SCHEMA, "r", encoding="utf-8") as f:
        sql = f.read()
    dw.executescript(sql)
    dw.commit()


def safe_cols(con, table, wanted):
    """只选源表真实存在的列，避免 schema 漂移导致 INSERT 失败。"""
    cur = con.execute(f"PRAGMA table_info({table})")
    exist = {r[1] for r in cur.fetchall()}
    return [c for c in wanted if c in exist]


# ----------------------------------------------------------------------------
# 增量判定
# ----------------------------------------------------------------------------

def get_freshness(src):
    """源库每本书最近一次装载完成时刻 {book_id: finished_at}。"""
    out = {}
    for b, m in src.execute(
        "SELECT book_id, MAX(finished_at) FROM load_runs GROUP BY book_id"):
        out[b] = m
    return out


def get_watermarks(dw):
    try:
        return {b: m for b, m in dw.execute(
            "SELECT book_id, last_loaded_at FROM dw_watermark")}
    except Exception:
        return {}


def changed_books(freshness, watermarks):
    """源库装载时刻晚于水印（或尚无水印）的书 = 需要重建。"""
    out = []
    for b, fin in freshness.items():
        if fin is None:
            continue
        wm = watermarks.get(b)
        if wm is None or fin > wm:
            out.append(b)
    return sorted(out)


def is_newer(freshness, watermarks):
    """是否存在任何需要重建的书。"""
    return bool(changed_books(freshness, watermarks))


# ----------------------------------------------------------------------------
# 维度装载（支持按书过滤）
# ----------------------------------------------------------------------------

def _in_clause(books):
    return "(" + ",".join("?" for _ in books) + ")"


def load_dimensions(src, dw, books=None):
    # ---- dim_book ----
    cols = safe_cols(src, "books",
                     ["book_id", "code", "name", "source_root", "status",
                      "schema_version", "loaded_at"])
    if books is None:
        rows = src.execute(f"SELECT {','.join(cols)} FROM books").fetchall()
    else:
        rows = src.execute(
            f"SELECT {','.join(cols)} FROM books WHERE book_id IN {_in_clause(books)}",
            books).fetchall()
    if books is not None:
        dw.execute(f"DELETE FROM dim_book WHERE book_id IN {_in_clause(books)}", books)
    dw.executemany(
        "INSERT OR REPLACE INTO dim_book "
        "(book_id,code,name,source_root,status,schema_version,loaded_at) "
        "VALUES (?,?,?,?,?,?,?)",
        [tuple(r[col] for col in cols) for r in rows])

    # ---- dim_layer ----
    cols = safe_cols(src, "layer_catalog",
                     ["book_id", "layer_key", "layer_code", "layer_name",
                      "container_kind", "kind", "id_prefix", "status", "record_count"])
    if books is None:
        rows = src.execute(f"SELECT {','.join(cols)} FROM layer_catalog").fetchall()
    else:
        rows = src.execute(
            f"SELECT {','.join(cols)} FROM layer_catalog "
            f"WHERE book_id IN {_in_clause(books)}", books).fetchall()
    if books is not None:
        dw.execute(f"DELETE FROM dim_layer WHERE book_id IN {_in_clause(books)}", books)
    dw.executemany(
        "INSERT OR REPLACE INTO dim_layer "
        "(book_id,layer_key,layer_code,layer_name,container_kind,kind,"
        "id_prefix,status,record_count) VALUES (?,?,?,?,?,?,?,?,?)",
        [tuple(r[col] for col in cols) for r in rows])

    # ---- dim_volume（从 items / records 的 volume 字段派生）----
    if books is not None:
        dw.execute(f"DELETE FROM dim_volume WHERE book_id IN {_in_clause(books)}", books)
    vols = set()
    if books is None:
        q = "SELECT book_id, volume FROM items WHERE volume IS NOT NULL"
        q2 = "SELECT book_id, volume FROM records WHERE volume IS NOT NULL"
        params = ()
    else:
        q = f"SELECT book_id, volume FROM items WHERE volume IS NOT NULL " \
            f"AND book_id IN {_in_clause(books)}"
        q2 = f"SELECT book_id, volume FROM records WHERE volume IS NOT NULL " \
             f"AND book_id IN {_in_clause(books)}"
        params = books * 2
    for b, v in src.execute(q, params[0:len(books)] if books else ()):
        vols.add((b, v))
    for b, v in src.execute(q2, params[len(books):] if books else ()):
        vols.add((b, v))
    rm = {}
    try:
        for b, v, m in src.execute("SELECT book_id, volume, reading_mode FROM volumes"):
            if books is None or b in books:
                rm[(b, v)] = m
    except Exception:
        pass
    dw.executemany(
        "INSERT OR REPLACE INTO dim_volume (book_id, volume, reading_mode) VALUES (?,?,?)",
        [(b, v, rm.get((b, v))) for (b, v) in sorted(vols)])

    # ---- dim_entity_raw（nodes）----
    cols = safe_cols(src, "nodes",
                     ["uid", "book_id", "layer_key", "local_id", "label", "type"])
    if books is None:
        rows = src.execute(f"SELECT {','.join(cols)} FROM nodes").fetchall()
    else:
        rows = src.execute(
            f"SELECT {','.join(cols)} FROM nodes "
            f"WHERE book_id IN {_in_clause(books)}", books).fetchall()
    if books is not None:
        dw.execute(f"DELETE FROM dim_entity_raw WHERE book_id IN {_in_clause(books)}",
                   books)
    dw.executemany(
        "INSERT OR REPLACE INTO dim_entity_raw "
        "(uid,book_id,layer_key,local_id,label,type) VALUES (?,?,?,?,?,?)",
        [tuple(r[col] for col in cols) for r in rows])


def load_enum_dims(src, dw):
    """枚举维度（全局，与书无关）—— 每次刷新，保证与联邦库 enum_* 同步。"""
    dw.execute("DELETE FROM dim_enum_group")
    dw.execute("DELETE FROM dim_enum_value")
    eg_cols = safe_cols(src, "enum_registry",
                        ["enum_group", "name", "version", "section"])
    if eg_cols:
        rows = src.execute(f"SELECT {','.join(eg_cols)} FROM enum_registry").fetchall()
        dw.executemany(
            "INSERT OR REPLACE INTO dim_enum_group "
            "(enum_group,name,version,section) VALUES (?,?,?,?)",
            [tuple(r[c] for c in eg_cols) for r in rows])
    ev_cols = safe_cols(src, "enum_values",
                        ["enum_group", "value", "is_top", "parent", "alias"])
    if ev_cols:
        rows = src.execute(f"SELECT {','.join(ev_cols)} FROM enum_values").fetchall()
        dw.executemany(
            "INSERT OR REPLACE INTO dim_enum_value "
            "(enum_group,value,is_top,parent,alias) VALUES (?,?,?,?,?)",
            [tuple(r[c] for c in ev_cols) for r in rows])


def collect_years(src, books=None):
    """best-effort：扫描 payload JSON，收集 1200–1700 区间的 4 位年份。"""
    years = set()
    tbls = ("records", "edges", "nodes")
    for tbl in tbls:
        try:
            if books is None:
                cur = src.execute(f"SELECT payload FROM {tbl}")
            else:
                cur = src.execute(
                    f"SELECT payload FROM {tbl} "
                    f"WHERE book_id IN {_in_clause(books)}", books)
        except Exception:
            continue
        for (p,) in cur:
            if not p:
                continue
            for m in YEAR_RE.findall(p):
                y = int(m)
                if 1200 <= y <= 1700:
                    years.add(y)
    return sorted(years)


def dynasty_of(y):
    if y <= 1367:
        return "元"
    if 1368 <= y <= 1644:
        return "明"
    return "清(初)"


def load_time_dim(src, dw, books=None):
    """时间维：保留已有年份，增量补入变更书的年份（年份只增不减）。"""
    if books is not None:
        years = collect_years(src, books)
        existing = {r[0] for r in dw.execute("SELECT year FROM dim_time_year")}
        years = [y for y in years if y not in existing]
    else:
        dw.execute("DELETE FROM dim_time_year")
        years = collect_years(src)
    for y in years:
        dw.execute(
            "INSERT OR REPLACE INTO dim_time_year (year,dynasty,century,is_ming) "
            "VALUES (?,?,?,?)",
            (y, dynasty_of(y), y // 100 + 1, 1 if 1368 <= y <= 1644 else 0))


def build_member_maps(src):
    """uid → canonical_id（偏好 locked > auto）；canonical 成员统计。"""
    order = {"locked": 2, "auto": 1, "conflict": 0, "pending": 0}
    uid_best = {}
    canon_members = {}
    for canon, uid, status in src.execute(
            "SELECT canonical_id, uid, status FROM members"):
        canon_members.setdefault(canon, []).append((uid, status))
        rank = order.get(status, 0)
        best = uid_best.get(uid)
        if best is None or rank > best[1]:
            uid_best[uid] = (canon, rank)
    uid_to_canon = {u: c for u, (c, _) in uid_best.items()}
    return uid_to_canon, canon_members


def load_entity_resolved_and_bridge(src, dw):
    """跨书解析维度 + 桥表 + F3（全局，每次刷新）。返回 uid→canonical 映射。"""
    dw.execute("DELETE FROM dim_entity_resolved")
    dw.execute("DELETE FROM bridge_entity_member")
    dw.execute("DELETE FROM f_resolution")
    uid_to_canon, canon_members = build_member_maps(src)

    rows = src.execute(
        "SELECT canonical_id, repr_type, repr_label, status FROM canonical").fetchall()
    for canon, rtype, rlabel, status in rows:
        members = canon_members.get(canon, [])
        member_count = len(members)
        book_ids = {u.split(":", 1)[0] for u, _ in members if ":" in u}
        dw.execute(
            "INSERT OR REPLACE INTO dim_entity_resolved "
            "(canonical_id,repr_type,repr_label,status,member_count,book_span) "
            "VALUES (?,?,?,?,?,?)",
            (canon, rtype, rlabel, status, member_count, len(book_ids)))

    for canon, uid, method, conf, status, ev in src.execute(
            "SELECT canonical_id, uid, method, confidence, status, evidence_count "
            "FROM members"):
        is_confirmed = 1 if status in ("auto", "locked") else 0
        book_id = uid.split(":", 1)[0] if ":" in uid else None
        dw.execute(
            "INSERT OR REPLACE INTO bridge_entity_member "
            "(canonical_id,uid,book_id,method,confidence,status,evidence_count,"
            "is_confirmed) VALUES (?,?,?,?,?,?,?,?)",
            (canon, uid, book_id, method, conf, status, ev, is_confirmed))
        dw.execute(
            "INSERT OR REPLACE INTO f_resolution "
            "(canonical_id,uid,book_id,method,confidence,status,evidence_count) "
            "VALUES (?,?,?,?,?,?,?)",
            (canon, uid, book_id, method, conf, status, ev))

    return uid_to_canon


def json_of(s):
    if not s:
        return {}
    try:
        v = json.loads(s)
        return v if isinstance(v, dict) else {}
    except Exception:
        return {}


def count_ref_entities(payload):
    n = 0
    for k, v in payload.items():
        if k.endswith("_ent_ids") and isinstance(v, list):
            n += len(v)
    return n


def _first_year_in(payload):
    if not payload:
        return None
    m = YEAR_RE.search(payload)
    return int(m.group(1)) if m else None


def load_facts(src, dw, uid_to_canon, books=None):
    """事实表装载（支持按书过滤）。返回载入的 (book,layer) 漂移对供调用方用。"""
    # ---- F1 f_annotation（records）----
    if books is not None:
        dw.execute(f"DELETE FROM f_annotation WHERE book_id IN {_in_clause(books)}",
                   books)
    drift_pairs = set()
    for book, layer in src.execute(
            "SELECT DISTINCT book_id, layer_key FROM enum_drift"):
        drift_pairs.add((book, layer))
    if books is None:
        recs = src.execute(
            "SELECT book_id, layer_key, local_id, volume, item_id, payload FROM records")
    else:
        recs = src.execute(
            f"SELECT book_id, layer_key, local_id, volume, item_id, payload "
            f"FROM records WHERE book_id IN {_in_clause(books)}", books)
    for book, layer, lid, vol, item, payload in recs:
        p = json_of(payload)
        entity_raw_uid = f"{book}:{lid}" if layer == "ent" else None
        ref_n = count_ref_entities(p)
        has_drift = 1 if (book, layer) in drift_pairs else 0
        dw.execute(
            "INSERT OR REPLACE INTO f_annotation "
            "(book_id,layer_key,local_id,volume,entity_raw_uid,item_id,"
            "payload_bytes,ref_entity_count,has_enum_drift) VALUES (?,?,?,?,?,?,?,?,?)",
            (book, layer, lid, vol, entity_raw_uid, item,
             len(payload) if payload else 0, ref_n, has_drift))

    # ---- F2 f_relationship（edges）----
    if books is not None:
        dw.execute(f"DELETE FROM f_relationship WHERE book_id IN {_in_clause(books)}",
                   books)
    if books is None:
        eds = src.execute(
            "SELECT book_id,layer_key,local_id,predicate,subject_uid,object_uid,payload "
            "FROM edges")
    else:
        eds = src.execute(
            f"SELECT book_id,layer_key,local_id,predicate,subject_uid,object_uid,payload "
            f"FROM edges WHERE book_id IN {_in_clause(books)}", books)
    for book, layer, lid, pred, subj, obj, payload in eds:
        p = json_of(payload)
        vol = p.get("volume")
        year = _first_year_in(payload)
        subj_res = uid_to_canon.get(subj) if subj else None
        obj_res = uid_to_canon.get(obj) if obj else None
        is_resolved = 1 if (subj and obj) else 0
        dw.execute(
            "INSERT OR REPLACE INTO f_relationship "
            "(book_id,layer_key,local_id,volume,predicate,subject_raw_uid,"
            "object_raw_uid,subject_resolved,object_resolved,event_year,is_resolved) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (book, layer, lid, vol, (pred or None), subj, obj,
             subj_res, obj_res, year, is_resolved))

    # ---- F4 f_citation（record_refs）----
    if books is not None:
        dw.execute(f"DELETE FROM f_citation WHERE book_id IN {_in_clause(books)}", books)
    if books is None:
        cites = src.execute(
            "SELECT ref_id,book_id,layer_key,local_id,field,volume,role,"
            "target_uid,target_ambiguous,item_id FROM record_refs")
    else:
        cites = src.execute(
            f"SELECT ref_id,book_id,layer_key,local_id,field,volume,role,"
            f"target_uid,target_ambiguous,item_id FROM record_refs "
            f"WHERE book_id IN {_in_clause(books)}", books)
    for (ref_id, book, layer, lid, field, vol, role,
         target_uid, ambiguous, item) in cites:
        m = re.search(r"#(\d+)$", ref_id or "")
        ref_index = int(m.group(1)) if m else 0
        tgt_res = uid_to_canon.get(target_uid) if target_uid else None
        dw.execute(
            "INSERT OR REPLACE INTO f_citation "
            "(ref_id,book_id,layer_key,local_id,field,ref_index,volume,role,"
            "target_raw_uid,target_resolved,target_ambiguous,item_id) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (ref_id, book, layer, lid, field, ref_index, vol, role,
             target_uid, tgt_res, ambiguous, item))

    # ---- F5 f_drift（enum_drift，全局刷新）----
    dw.execute("DELETE FROM f_drift")
    for book, layer, field, eg, val, in_lib, cnt in src.execute(
            "SELECT book_id,layer_key,field,enum_group,value,in_library,count "
            "FROM enum_drift"):
        dw.execute(
            "INSERT OR REPLACE INTO f_drift "
            "(book_id,layer_key,field,enum_group,value,drift_count,in_library) "
            "VALUES (?,?,?,?,?,?,?)",
            (book, layer, field, eg, val, cnt, in_lib))

    return drift_pairs


def refresh_resolved_columns(dw, uid_to_canon):
    """增量模式下，全局刷新关系/引用事实的 resolved 列，保证跨书一致。"""
    rows = dw.execute(
        "SELECT book_id,layer_key,local_id,subject_raw_uid,object_raw_uid "
        "FROM f_relationship").fetchall()
    for book, layer, lid, subj, obj in rows:
        subj_res = uid_to_canon.get(subj) if subj else None
        obj_res = uid_to_canon.get(obj) if obj else None
        is_resolved = 1 if (subj and obj) else 0
        dw.execute(
            "UPDATE f_relationship SET subject_resolved=?,object_resolved=?,"
            "is_resolved=? WHERE book_id=? AND layer_key=? AND local_id=?",
            (subj_res, obj_res, is_resolved, book, layer, lid))
    rows = dw.execute(
        "SELECT ref_id,target_raw_uid FROM f_citation").fetchall()
    for ref_id, tgt in rows:
        tgt_res = uid_to_canon.get(tgt) if tgt else None
        dw.execute("UPDATE f_citation SET target_resolved=? WHERE ref_id=?",
                   (tgt_res, ref_id))


def refresh_annotation_drift_flag(dw):
    """全局刷新 f_annotation.has_enum_drift（枚举漂移表变更后保持同步）。"""
    dw.execute(
        "UPDATE f_annotation SET has_enum_drift=0 WHERE has_enum_drift<>0")
    dw.execute(
        "UPDATE f_annotation SET has_enum_drift=1 "
        "WHERE (book_id,layer_key) IN "
        "(SELECT DISTINCT book_id,layer_key FROM f_drift)")


def set_watermarks(dw, freshness, books=None):
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if books is None:
        books = list(freshness.keys())
    for b in books:
        fin = freshness.get(b)
        if not fin:
            continue
        dw.execute(
            "INSERT INTO dw_watermark(book_id,last_loaded_at,built_at) "
            "VALUES(?,?,?) ON CONFLICT(book_id) "
            "DO UPDATE SET last_loaded_at=excluded.last_loaded_at, "
            "built_at=excluded.built_at",
            (b, fin, now_iso))


def verify(dw):
    print("\n=== 数仓验证（行数）===")
    tabs = ["dim_book", "dim_layer", "dim_volume", "dim_entity_raw",
            "dim_entity_resolved", "dim_enum_group", "dim_enum_value",
            "dim_time_year", "bridge_entity_member",
            "f_annotation", "f_relationship", "f_resolution",
            "f_citation", "f_drift"]
    res = {}
    for t in tabs:
        try:
            n = dw.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        except Exception as e:
            n = f"ERR {e}"
        res[t] = n
        print(f"  {t:<22} {n}")
    try:
        confirmed = dw.execute(
            "SELECT COUNT(*) FROM bridge_entity_member WHERE is_confirmed=1").fetchone()[0]
        locked = dw.execute(
            "SELECT COUNT(*) FROM f_resolution WHERE status='locked'").fetchone()[0]
        resolved_edges = dw.execute(
            "SELECT COUNT(*) FROM f_relationship "
            "WHERE subject_resolved IS NOT NULL OR object_resolved IS NOT NULL").fetchone()[0]
        drift = dw.execute("SELECT COUNT(*) FROM f_drift").fetchone()[0]
        print(f"\n  桥表确认成员(is_confirmed=1)：{confirmed}")
        print(f"  锁定成员(人工裁决)：{locked}")
        print(f"  关系事实已对齐到跨书实体：{resolved_edges}")
        print(f"  枚举漂移事实(f_drift)：{drift}")
    except Exception as e:
        print("  一致性抽查 ERR:", e)
    return res


# ----------------------------------------------------------------------------
# 入口
# ----------------------------------------------------------------------------

def run_full(src, freshness, args):
    """全量重建：删除旧 DW → 建表 → 全量抽取 → 写水印。"""
    if os.path.exists(args.dw):
        os.remove(args.dw)
    dw = connect(args.dw)
    load_schema(dw)
    print(">> [全量] 装载一致性维度 ...")
    load_dimensions(src, dw)
    print(">> [全量] 装载时间维（best-effort）...")
    load_time_dim(src, dw)
    print(">> [全量] 装载枚举维度（全局）...")
    load_enum_dims(src, dw)
    print(">> [全量] 装载实体解析维度 + 桥表 + F3 ...")
    uid_to_canon = load_entity_resolved_and_bridge(src, dw)
    print(">> [全量] 装载事实表 F1/F2/F4/F5 ...")
    load_facts(src, dw, uid_to_canon)
    dw.commit()
    set_watermarks(dw, freshness)
    dw.commit()
    verify(dw)
    print(f"\n✓ 数仓已全量重建：{args.dw}")


def run_incremental(src, dw, freshness, watermarks, to_rebuild, args):
    print(f">> [增量] 需重建 {len(to_rebuild)} 本：{', '.join(to_rebuild)}")
    print(">> [增量] 装载变更书的一致性维度 ...")
    load_dimensions(src, dw, books=to_rebuild)
    print(">> [增量] 补入变更书的时间维年份 ...")
    load_time_dim(src, dw, books=to_rebuild)
    print(">> [增量] 刷新枚举维度（全局）...")
    load_enum_dims(src, dw)
    print(">> [增量] 刷新跨书解析维度 + 桥表 + F3（全局）...")
    uid_to_canon = load_entity_resolved_and_bridge(src, dw)
    print(">> [增量] 装载变更书事实表 F1/F2/F4 ...")
    load_facts(src, dw, uid_to_canon, books=to_rebuild)
    print(">> [增量] 全局刷新关系/引用 resolved 列 ...")
    refresh_resolved_columns(dw, uid_to_canon)
    print(">> [增量] 全局刷新 f_annotation 枚举漂移标记 ...")
    refresh_annotation_drift_flag(dw)
    dw.commit()
    set_watermarks(dw, freshness, books=to_rebuild)
    dw.commit()
    verify(dw)
    print(f"\n✓ 数仓已增量更新：{args.dw}（{len(to_rebuild)} 本重建）")


def main():
    ap = argparse.ArgumentParser(description="联邦库 → 数据仓库 ETL")
    ap.add_argument("--src", default=DEFAULT_SRC)
    ap.add_argument("--dw", default=DEFAULT_DW)
    ap.add_argument("--full", action="store_true", help="强制全量重建（忽略水印）")
    args = ap.parse_args()

    if not os.path.exists(args.src):
        raise SystemExit(f"✗ 源库不存在：{args.src}")

    src = connect(args.src)
    freshness = get_freshness(src)

    dw_exists = os.path.exists(args.dw)
    if args.full or not dw_exists:
        run_full(src, freshness, args)
        src.close()
        return

    dw = connect(args.dw)
    watermarks = get_watermarks(dw)
    to_rebuild = changed_books(freshness, watermarks)
    if not to_rebuild:
        print("✓ 数仓已是最新（所有书源库装载时刻均晚于水印），无需重建。")
        dw.close(); src.close()
        return
    run_incremental(src, dw, freshness, watermarks, to_rebuild, args)
    dw.close(); src.close()


if __name__ == "__main__":
    main()
