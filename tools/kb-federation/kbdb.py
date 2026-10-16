"""kbdb.py —— 联邦库低层 DB 工具（零第三方依赖）

仅依赖 sqlite3 / os / json / hashlib / datetime。
守住联邦线铁律：复合主键 (book_id, ...) 隔离撞号；原文只存指针；
Tier1/2 全部可重建、入 git 时忽略。
"""

import sqlite3
import os
import json
import hashlib
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(HERE, "schema.sql")
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))  # guji/


def now():
    """UTC ISO8601 时间戳。"""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def connect(path):
    con = sqlite3.connect(path)
    con.execute("PRAGMA foreign_keys=OFF")  # schema 已设；目录驱动，loader 自管写入顺序
    return con


def ensure_schema(con):
    """执行 schema.sql（FTS5 段为注释，无害）；若 FTS5 可用则建 fts_nodes。

    幂等 ALTER：schema.sql 用 CREATE TABLE IF NOT EXISTS，对已存在的旧表不会加新列，
    故这里对新增列做防御性 ALTER（列已存在则静默跳过）。
    """
    sql = open(SCHEMA_PATH, encoding="utf-8").read()
    con.executescript(sql)
    try:
        con.execute("ALTER TABLE books ADD COLUMN source_rev TEXT")
    except sqlite3.OperationalError:
        pass  # 列已存在（新版 schema 已含）
    try:
        con.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS fts_nodes "
            "USING fts5(uid UNINDEXED, label, normalized, raw_name)"
        )
    except sqlite3.OperationalError:
        pass  # 编译不含 FTS5：跳过，不影响其余表
    con.execute(
        "INSERT OR REPLACE INTO federation_meta(key,value) VALUES('schema_version','1')"
    )
    con.execute(
        "INSERT OR REPLACE INTO federation_meta(key,value) VALUES('created_at',?)",
        (now(),),
    )
    con.commit()


def make_uid(book_id, local_id):
    return f"{book_id}:{local_id}"


def upsert(con, table, rows, pk_cols):
    """批量 INSERT OR REPLACE；rows 为 dict 列表。返回写入行数。"""
    if not rows:
        return 0
    cols = list(rows[0].keys())
    colsql = ",".join(cols)
    placeholders = ",".join("?" * len(cols))
    sql = f"INSERT OR REPLACE INTO {table} ({colsql}) VALUES ({placeholders})"
    con.executemany(sql, [[r[c] for c in cols] for r in rows])
    return len(rows)


def md5(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


# Tier1 + Tier2 中按 book_id 隔离的表（wipe_book 清理范围）
# 注意：**不含 spine / spine_meta**。spine 由 tools/kb-federation/spine_build.py
# 独立维护（C9 §6b 豁免书的就地派生产物），load/load-all 不应连带清掉它。
_BOOK_ID_TABLES = [
    "records",
    "items",
    "nodes",
    "edges",
    "pending_refs",
    "layer_fields",
    "layer_catalog",
]


def wipe_book(con, book_id):
    """清掉某书在联邦库的全部痕迹（先删后插，保证重跑幂等）。

    注意各表列不同：
      - _BOOK_ID_TABLES 含 book_id 列，直接按 book_id 删；
      - members / canonical 只有 uid（book_id:local_id），按 uid 前缀删；
      - candidate_links 的 a_uid/b_uid 也是该书 uid，按前缀删。
    """
    for t in _BOOK_ID_TABLES:
        con.execute(f"DELETE FROM {t} WHERE book_id=?", (book_id,))
    con.execute("DELETE FROM members WHERE uid LIKE ?", (book_id + ":%",))
    con.execute(
        "DELETE FROM candidate_links WHERE a_uid LIKE ? OR b_uid LIKE ?",
        (book_id + ":%", book_id + ":%"),
    )
    con.execute("DELETE FROM load_runs WHERE book_id=?", (book_id,))
    con.execute("DELETE FROM books WHERE book_id=?", (book_id,))
    con.commit()
