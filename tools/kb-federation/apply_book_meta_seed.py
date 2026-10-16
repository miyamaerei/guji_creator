# -*- coding: utf-8 -*-
"""把 server/book-meta.seed.sql 灌进 kb.sqlite（sqlite3 CLI 不可用时的替代）。

用法：
    python apply_book_meta_seed.py [--db <kb.sqlite>] [--seed <seed.sql>] [--dry]
"""
import argparse
import os
import re
import sqlite3
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.join(HERE, "kb.sqlite")
# guji/tools/kb-federation -> guji/tools -> guji -> ToolBox -> reader-vue/server
DEFAULT_SEED = os.path.normpath(
    os.path.join(HERE, "..", "..", "..", "reader-vue", "server", "book-meta.seed.sql")
)


def split_statements(sql):
    """按分号切语句，跳过纯注释/空白。注释里含中文分号不影响。"""
    # 去掉行注释（-- 到行尾），保留字符串内的原样
    out = []
    for line in sql.splitlines():
        idx = line.find("--")
        if idx >= 0:
            # 粗略判断：若 -- 在引号内则不切（种子文件无此情况）
            if line[:idx].count("'") % 2 == 0:
                line = line[:idx]
        out.append(line)
    text = "\n".join(out)
    stmts = []
    buf = []
    in_str = False
    for ch in text:
        if ch == "'":
            in_str = not in_str
        if ch == ";" and not in_str:
            s = "".join(buf).strip()
            if s:
                stmts.append(s)
            buf = []
        else:
            buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        stmts.append(tail)
    return stmts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--seed", default=DEFAULT_SEED)
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    seed = os.path.abspath(args.seed)
    print("seed =", seed)
    if not os.path.exists(seed):
        print("!! seed 不存在")
        return 1
    with open(seed, encoding="utf-8") as f:
        sql = f.read()
    stmts = split_statements(sql)
    print("语句数 =", len(stmts))
    for i, s in enumerate(stmts):
        print("  [%d] %s..." % (i, re.sub(r"\s+", " ", s)[:90]))
    if args.dry:
        print("(dry-run，不落库)")
        return 0

    con = sqlite3.connect(args.db)
    con.execute("PRAGMA foreign_keys=OFF")
    before = con.execute("select count(*) from book_meta").fetchone()[0]
    for s in stmts:
        con.execute(s)
    con.commit()
    after = con.execute("select count(*) from book_meta").fetchone()[0]
    rows = con.execute(
        "select book_id, name, dynasty, author, genre, subject from book_meta order by book_id"
    ).fetchall()
    con.close()

    print()
    print("book_meta 行数 %d -> %d" % (before, after))
    for r in rows:
        print("  %-5s %-12s %-3s %-8s %-8s %s" % r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
