# -*- coding: utf-8 -*-
"""spine_build.py —— 按 C9《书籍著录与结构契约》生成联邦库 spine 表（Tier1）。

背景（两处权威豁免，本脚本正是它的兑现）
------------------------------------------------------------
1. `docs/书籍著录与结构契约.md` §6b（`:24-25`、`:371-373`）：
   盘上 17 本已有 `书籍json/<书>_校对版.json`，book→卷→条 树与条级全文就地在那儿，
   **这批书不另建 `spine.json`**，改为就地补机采字段。
2. `tools/book_json_augment.py` 只回填了 meta 级 8 字段与 item 级 `level`，
   `sections` 标「预留位，本轮不建」——节标题因此从未进库。

而联邦库 `items.title` 的语义**不是**节标题：
`load.py:129` `norm = a.get("norm") or a.get("original") or ""`、
`load.py:135` `"title": norm[:50]` —— 存的是「正文前 50 字短摘要」，
这是 `docs/跨书合并-数据库设计.md` 偏差台账 A6 明确承认的设计
（守「原文只在指纹库」铁律的折中）。adapter 的 `fingerprints()` 虽返回
title，但取值口径各书不一（卷名 / iid / 恒「原文」），也被 load.py 忽略。

真源节标题只在 `书籍json/volumes[].items[].title`（与 `items.item_id` 同构）。
本脚本把它按 C9 §3.6 的 DDL 落进 `spine` 表，供阅读器展示。

生成什么（对齐 C9 §3.2 六级 ladder：book/juan/pian/zhang/duan/ju）
------------------------------------------------------------
只生成 `kind ∈ {book, juan, duan}` 三级：

  book  1 条/书   sid=<bid>          title=书名
  juan  N 条/书   sid=<bid>:j<NN>    title=卷名（volumes[].name，缺则「卷NN」）
  duan  M 条/书   sid=<bid>:d<NNNN>  title=条标题（volumes[].items[].title）

不生成 pian/zhang/ju：
  - C9 §3.2b 第 5 条：「凡候选层与条数相等，先怀疑它是条」——本批书的「节」即条，
    不重复登记，故无 zhang 级。
  - `duan` 依 C9 定义应为容器态（title 恒 null + start/end 指入 original）。
    但本批书正是 §6b 的豁免对象，`original` 全文留在 `书籍json`，
    DB 侧无副本可指。故此处把 duan 作为**聚合态**使用：title 承载条标题，
    start_offset/end_offset 留 NULL，并在 `evidence` 中如实注明该偏离。
    这是一次**有意且受限**的偏离，仅服务阅读器展示；将来若补 `spine.json`
    或把原文纳入 Tier1，应改为容器态并回填偏移。

C9 §3.3 S 族校验的自查（脚本内 assert）
  S1 root 唯一            → 每书恰好一个 kind=book 且 parent_sid IS NULL
  S2 parent 存在          → 所有非根节点 parent_sid 落在同书节点集合内
  S3 no 连续              → juan 的 no 覆盖 00..N-1；duan 的 no 覆盖 1..M
  S7 卷前缀 = juan 祖先   → duan.item_id 的前缀 == 其 juan 祖先的 no
  S9 kind=juan ⊇ items.volume → 并集包含（不含该断言则打印覆盖缺口）
  S12 spine_single_tree   → 单连通：节点数 = 边数 + 1
  S15 spine_isomorphism   → 同构只登记一次（book 只 1 条）

用法
------
  python spine_build.py --books            # 只看各书能生成什么（不落库）
  python spine_build.py --build            # 落库（先建表，再逐书 INSERT OR REPLACE）
  python spine_build.py --build --book sdr # 只重建某书
  python spine_build.py --verify           # 跑 S 族校验并打印结果
  python spine_build.py --drop             # 删掉 spine 表（回滚用）

约束（刻意的）
--------------
* **不跑 `federation.py transform`**：`docs/联邦库原表增量与稀疏诊断.md` §5 硬警告，
  现库身份层与 transform.py 不是同一套算法，重跑会把 canonical 1580→643、
  members 6772→2979、`canon-xxxxx` 编号集体错位。
* **不跑 `load-all`**：会重建全部 items/records。
* 本脚本只碰 `spine` / `spine_meta` 两张表，其余 29 张表一个字都不动。
"""

import argparse
import glob
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))  # guji/
DEFAULT_DB = os.path.join(HERE, "kb.sqlite")

AXIS = "primary"
GENERATOR = "tools/kb-federation/spine_build.py"
CONTRACT = "书籍著录与结构契约.md §3.6"

# ---------------------------------------------------------------- 表 DDL
# 列名/列序逐字对齐《书籍著录与结构契约.md》§3.6 的落库映射
DDL_SPINE = """
CREATE TABLE IF NOT EXISTS spine (
  book_id      TEXT NOT NULL,
  axis         TEXT NOT NULL,          -- 轴：primary | geo | date ...（本批全 primary）
  sid          TEXT NOT NULL,          -- 节点稳定标识 <book_id>[:<seg>...]
  parent_sid   TEXT,                   -- 父节点 sid；根为 NULL
  kind         TEXT NOT NULL,          -- book|juan|pian|zhang|duan|ju（本批用前三者）
  no           TEXT,                   -- 同级序号，两位/四位零填充
  title        TEXT,                   -- 显示标题（duan 级承载条标题，见模块 docstring）
  origin       TEXT NOT NULL,          -- source | derived
  evidence     TEXT,                   -- 判定依据（人可读）
  rule         TEXT,                   -- derived 时的切分规则
  item_id      TEXT,                   -- duan/ju 指向条目
  start_offset INTEGER,                -- duan/ju 半开区间 [start,end) 指入 original
  end_offset   INTEGER,
  first_item   TEXT,                   -- 聚合态：子树首条 item_id
  last_item    TEXT,                   -- 聚合态：子树末条 item_id
  PRIMARY KEY (book_id, axis, sid),
  FOREIGN KEY (book_id) REFERENCES books(book_id)
);
CREATE INDEX IF NOT EXISTS idx_spine_parent ON spine(book_id, axis, parent_sid);
CREATE INDEX IF NOT EXISTS idx_spine_item   ON spine(book_id, item_id);
CREATE INDEX IF NOT EXISTS idx_spine_kind   ON spine(book_id, kind);
"""

DDL_SPINE_META = """
CREATE TABLE IF NOT EXISTS spine_meta (
  book_id       TEXT NOT NULL,
  axis          TEXT NOT NULL,
  declared_depth TEXT,                 -- book|juan|pian|zhang|duan|ju
  registry_hash TEXT,                  -- 规则集指纹（S5 重算校验用）
  offset_unit   TEXT,                  -- char | byte
  generator     TEXT,
  generated_at  TEXT,
  contract      TEXT,
  note          TEXT,
  PRIMARY KEY (book_id, axis)
);
"""

# ---------------------------------------------------------------- 书目录
# 与 adapters/__init__.py 的 BOOK_ROOTS 同源；这里只列书籍json 真源路径
BOOK_DIRS = {
    "kzz": "kezuozhuiyu-kb",
    "wzz": "wuzazu-kb",
    "sdr": "shuidongriji-kb",
    "xgf": "xinguanguifan-kb",
    "qb": "qubian_kb",
    "xyf": "xianjinyifeng-kb",
    "lgs": "shizhenglu-kb",
    "xzl": "xuezhenglu-kb",
    "ysz": "yuanshuzaji-kb",
    "fqh": "fuhuiquanshu-kb",
    "ppy": "pingpingyan-kb",
    "shz": "mingshi/mingshi-shihuozhi",
    "zgz": "mingshi/mingshi-zhiguanzhi",
}

# xyf 无 书籍json（探针7 实证）：其条标题不在任何真源里，只有正文。
# 见 _probe_spine2.py 输出：xianjinyifeng-kb 下唯一的 json 是
# 05-xianjinyifeng-knowledge/data/_item_registry.json（无 volumes）；
# join 的 fingerprints 只有 item_id/norm/original/volume，**无 title**。
NO_TITLE_SOURCE = {"xyf"}


def now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- 读真源
def find_booksjson(book_dir):
    """定位 <book_dir>/书籍json/<书>_校对版.json（优先带「校对版」）。"""
    cands = []
    for pat in ("书籍json/*.json", "*.json"):
        cands += glob.glob(os.path.join(REPO_ROOT, book_dir, pat))
    cands = sorted(
        c for c in cands
        if not os.path.basename(c).startswith("_")
        and "分卷json" not in c
        and os.path.basename(c) not in ("book.meta.json", "spine.json")
    )
    pref = [c for c in cands if "_校对版" in c]
    for p in (pref or cands):
        try:
            doc = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        if "volumes" in doc:
            return p, doc
    return None, None


def read_book_json(book_id):
    """返回 (path, doc) 或 (None, None)。"""
    d = BOOK_DIRS.get(book_id)
    if not d:
        return None, None
    return find_booksjson(d)


def book_title(doc, book_id):
    meta = doc.get("meta") or {}
    t = (meta.get("书名") or "").strip()
    return t or book_id


def vol_title(v, idx):
    """卷名：volumes[].name 优先，回落「卷NN」。"""
    name = (v.get("name") or "").strip()
    if name:
        return name
    no = (v.get("no") or "").strip()
    return "卷%s" % (no or "%02d" % idx) if not name else name


# ---------------------------------------------------------------- 生成节点
def build_nodes(book_id, doc):
    """按 C9 生成 book/juan/duan 三级节点 + meta。

    返回 (nodes, meta_rows, stats)。
    """
    vols = doc.get("volumes") or []
    nodes = []

    # ---- book 级（聚合态）
    all_items = [
        it for v in vols for it in (v.get("items") or []) if it.get("id")
    ]
    nodes.append({
        "book_id": book_id, "axis": AXIS,
        "sid": book_id, "parent_sid": None, "kind": "book",
        "no": None,
        "title": book_title(doc, book_id),
        "origin": "source",
        "evidence": "书籍json meta.书名（C9 §6b 豁免书：不另建 spine.json）",
        "rule": None, "item_id": None,
        "start_offset": None, "end_offset": None,
        "first_item": all_items[0]["id"] if all_items else None,
        "last_item": all_items[-1]["id"] if all_items else None,
    })

    n_juan = n_duan = 0
    n_title_ok = 0
    juan_nos = []

    for vi, v in enumerate(vols):
        vno = (v.get("no") or "").strip()
        if not vno:
            continue
        juan_nos.append(vno)
        items = [it for it in (v.get("items") or []) if it.get("id")]
        sid_j = "%s:j%s" % (book_id, vno)
        nodes.append({
            "book_id": book_id, "axis": AXIS,
            "sid": sid_j, "parent_sid": book_id, "kind": "juan",
            "no": vno,
            "title": vol_title(v, vi),
            "origin": "source" if (v.get("name") or "").strip() else "derived",
            "evidence": (
                "书籍json volumes[].name"
                if (v.get("name") or "").strip()
                else "书籍json volumes[].no 无 name，回落「卷%s」"%vno
            ),
            "rule": None,
            "item_id": None, "start_offset": None, "end_offset": None,
            "first_item": items[0]["id"] if items else None,
            "last_item": items[-1]["id"] if items else None,
        })
        n_juan += 1

        # ---- duan 级（聚合态用法，见模块 docstring 的偏离说明）
        for di, it in enumerate(items):
            iid = it["id"]
            t = (it.get("title") or "").strip()
            if t:
                n_title_ok += 1
            nodes.append({
                "book_id": book_id, "axis": AXIS,
                "sid": "%s:d%s" % (book_id, iid.replace("-", "")),
                "parent_sid": sid_j, "kind": "duan",
                "no": "%04d" % (di + 1),
                "title": t or None,
                "origin": "source",
                "evidence": "书籍json volumes[].items[].title（条标题真源）",
                "rule": None,
                "item_id": iid,
                "start_offset": None, "end_offset": None,
                "first_item": None, "last_item": None,
            })
            n_duan += 1

    stats = {
        "vols": n_juan, "duan": n_duan, "title_ok": n_title_ok,
        "juan_nos": sorted(juan_nos),
        "src": None,
    }
    meta_rows = [{
        "book_id": book_id, "axis": AXIS,
        "declared_depth": "duan",
        "registry_hash": None,
        "offset_unit": "char",
        "generator": GENERATOR,
        "generated_at": now(),
        "contract": CONTRACT,
        "note": (
            "C9 §6b 豁免书：不建 spine.json，节标题就地取自 "
            "书籍json volumes[].items[].title；duan 以聚合态承载 title，"
            "start/end 留 NULL（DB 侧无 original 副本可指）"
        ),
    }]
    return nodes, meta_rows, stats


# ---------------------------------------------------------------- S 族校验
def check_s(nodes, stats):
    """C9 §3.3 S 族自查。返回 problems 列表。"""
    bad = []
    # S1 root 唯一
    roots = [n for n in nodes if n["kind"] == "book"]
    if len(roots) != 1:
        bad.append("S1 root 数 = %d（应 1）" % len(roots))
    # S3 no 连续：**按 parent 分组**逐个检查。
    # 注意 duan 的 no 在每个卷内从 0001 重新起算（同级内连续），
    # 展平后整体不单调 —— 早先按全局展平比序会误报。
    parent_of = {n["sid"]: n["parent_sid"] for n in nodes}
    by_sid = {n["sid"]: n for n in nodes}
    groups = {}
    for n in nodes:
        if n["kind"] in ("juan", "duan"):
            groups.setdefault((n["kind"], n["parent_sid"]), []).append(n["no"])
    for (kind, p), nos in groups.items():
        if nos != sorted(nos):
            bad.append("S3 %s(parent=%s) no 未按序" % (kind, p))
        if len(set(nos)) != len(nos):
            bad.append("S3 %s(parent=%s) no 有重复" % (kind, p))
    # juan 的 no 须零填充且卷内序号连续。
    # 注意：本批书卷号**不都从 00 起**（kzz/sdr/wzz/xgf/qb 有卷 00 前置内容，
    # lgs/xzl/ysz/fqh/ppy/shz/zgz 从 01 起），故只要求「连续」不要求「从 00 起」。
    jnos = [n["no"] for n in nodes if n["kind"] == "juan"]
    if jnos:
        want = ["%02d" % (int(jnos[0]) + i) for i in range(len(jnos))]
        if jnos != want:
            bad.append("S3 juan no 不连续：%s" % jnos)
    # S7 duan.item_id 前缀 == juan 祖先 no

    for n in nodes:
        if n["kind"] != "duan" or not n["item_id"]:
            continue
        pj = parent_of.get(n["sid"])
        jn = by_sid.get(pj)
        if not jn:
            bad.append("S7 %s 的 juan 祖先缺失" % n["sid"])
            continue
        pref = n["item_id"].split("-")[0]
        if pref != (jn["no"] or ""):
            bad.append("S7 %s item_id 前缀 %s != juan no %s"
                       % (n["sid"], pref, jn["no"]))
    # S12 单连通：边数 = 节点数 - 1
    edges = sum(1 for n in nodes if n["parent_sid"])
    if len(nodes) - edges != 1:
        bad.append("S12 非单连通树：节点 %d，边 %d（应差 1）"
                   % (len(nodes), edges))
    # S2 parent 存在
    sids = set(by_sid)
    for n in nodes:
        if n["parent_sid"] and n["parent_sid"] not in sids:
            bad.append("S2 %s 的 parent %s 不存在" % (n["sid"], n["parent_sid"]))
    return bad


# ---------------------------------------------------------------- 落库
def ensure_tables(con):
    con.executescript(DDL_SPINE)
    con.executescript(DDL_SPINE_META)
    con.commit()


def wipe_book_spine(con, book_id):
    con.execute("DELETE FROM spine WHERE book_id=?", (book_id,))
    con.execute("DELETE FROM spine_meta WHERE book_id=?", (book_id,))


def insert_nodes(con, nodes):
    if not nodes:
        return 0
    cols = ["book_id", "axis", "sid", "parent_sid", "kind", "no", "title",
            "origin", "evidence", "rule", "item_id",
            "start_offset", "end_offset", "first_item", "last_item"]
    sql = ("INSERT OR REPLACE INTO spine (%s) VALUES (%s)"
           % (",".join(cols), ",".join("?" * len(cols))))
    con.executemany(sql, [[n.get(c) for c in cols] for n in nodes])
    return len(nodes)


def insert_meta(con, meta_rows):
    cols = ["book_id", "axis", "declared_depth", "registry_hash", "offset_unit",
            "generator", "generated_at", "contract", "note"]
    sql = ("INSERT OR REPLACE INTO spine_meta (%s) VALUES (%s)"
           % (",".join(cols), ",".join("?" * len(cols))))
    con.executemany(sql, [[m.get(c) for c in cols] for m in meta_rows])


# ---------------------------------------------------------------- 命令
def cmd_books(con):
    print("=" * 104)
    print("spine_build --books：各书可生成的 spine 节点")
    print("=" * 104)
    print("%-5s %-6s %-6s %-8s %-9s %-8s  %s"
          % ("bid", "卷", "条", "title有值", "juan缺no", "S族问题", "真源"))
    for bid in BOOK_DIRS:
        p, doc = read_book_json(bid)
        if not doc:
            print("%-5s  —— 无 书籍json，跳过（%s）"
                  % (bid, "见 NO_TITLE_SOURCE" if bid in NO_TITLE_SOURCE else "?"))
            continue
        nodes, metas, st = build_nodes(bid, doc)
        bad = check_s(nodes, st)
        # juan no 连续性
        nos = st["juan_nos"]
        want = ["%02d" % i for i in range(len(nos))]
        gapno = "" if nos == want else "有"
        # S9：juan no 集合 vs 库内 items.volume
        dbvols = {r[0] for r in con.execute(
            "select distinct volume from items where book_id=?", (bid,))
            if r[0] is not None}
        miss = sorted(dbvols - set(nos))
        if miss:
            # shz 是已知例外：它的 items.volume 存中文卷名（食货一…食货六），
            # 而 item_id 前缀是两位数字（01-001…），两者不同构。
            # juan 节点按 item_id 前缀建（与 C9 §4.3「item_id 前缀 = 卷节点 no」一致），
            # 故 S9 在此**有意偏离**，卷名以 juan.title 承载。
            s9 = "S9偏离(卷名非数字，宽容):%s" % ",".join(miss)
        else:
            s9 = "S9 ok"
        print("%-5s %-6d %-6d %-8d %-9s %-8s  %s  %s"
              % (bid, st["vols"], st["duan"], st["title_ok"], gapno,
                 "无" if not bad else len(bad), s9,
                 os.path.relpath(p, REPO_ROOT)))


def cmd_build(con, only=None):
    ensure_tables(con)
    print("=" * 104)
    print("spine_build --build：落库")
    print("=" * 104)
    total = 0
    for bid in BOOK_DIRS:
        if only and bid != only:
            continue
        p, doc = read_book_json(bid)
        if not doc:
            print("[%s] 跳过：无 书籍json" % bid)
            continue
        nodes, metas, st = build_nodes(bid, doc)
        bad = check_s(nodes, st)
        wipe_book_spine(con, bid)
        n = insert_nodes(con, nodes)
        insert_meta(con, metas)
        con.commit()
        total += n
        print("[%s] %s  book=1 juan=%d duan=%d  写入=%d  S族=%s"
              % (bid, os.path.basename(p), st["vols"], st["duan"], n,
                 "无问题" if not bad else bad))
    print("-" * 104)
    print("合计写入 %d 行（spine）" % total)


def cmd_verify(con):
    tables = {r[0] for r in con.execute(
        "select name from sqlite_master where type='table'")}
    if "spine" not in tables:
        print("spine 表不存在，先跑 --build")
        return 1
    print("=" * 104)
    print("spine_build --verify：库内 spine 校验")
    print("=" * 104)
    rows = list(con.execute(
        "select book_id, kind, count(*) from spine group by book_id, kind "
        "order by book_id, kind"))
    per = {}
    for bid, kind, c in rows:
        per.setdefault(bid, {})[kind] = c
    print("%-5s %-6s %-6s %-6s  %s" % ("bid", "book", "juan", "duan", "库内 items"))
    for bid in sorted(per):
        d = per[bid]
        nitems = con.execute(
            "select count(*) from items where book_id=?", (bid,)).fetchone()[0]
        print("%-5s %-6d %-6d %-6d  %d" % (bid, d.get("book", 0), d.get("juan", 0),
                                           d.get("duan", 0), nitems))
    # 逐书跑 S7 / S12
    print("-" * 104)
    prob = 0
    for bid in sorted(per):
        nodes = [dict(zip(
            ["sid", "parent_sid", "kind", "no", "item_id"], r))
            for r in con.execute(
                "select sid,parent_sid,kind,no,item_id from spine where book_id=?",
                (bid,))]
        st = {"vols": per[bid].get("juan", 0), "duan": per[bid].get("duan", 0),
              "title_ok": 0, "juan_nos": []}
        bad = check_s(nodes, st)
        # duan 覆盖 = items 覆盖
        dun = {n["item_id"] for n in nodes if n["kind"] == "duan" and n["item_id"]}
        dbn = {r[0] for r in con.execute(
            "select item_id from items where book_id=?", (bid,))}
        cover = "duan覆盖 items %d/%d" % (len(dun & dbn), len(dbn))
        if bad:
            prob += len(bad)
            print("[%s] %s  %s" % (bid, cover, bad))
        else:
            print("[%s] %s  S族 ok" % (bid, cover))
    print("-" * 104)
    print("合计问题 %d 条" % prob)
    return 0 if prob == 0 else 1


def cmd_drop(con):
    con.execute("DROP TABLE IF EXISTS spine")
    con.execute("DROP TABLE IF EXISTS spine_meta")
    con.commit()
    print("已删除 spine / spine_meta 表")


def main():
    ap = argparse.ArgumentParser(
        description="按 C9 §3.6 生成联邦库 spine 表（Tier1）")
    ap.add_argument("--db", default=DEFAULT_DB)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--books", action="store_true", help="只勘察，不落库")
    g.add_argument("--build", action="store_true", help="落库")
    g.add_argument("--verify", action="store_true", help="校验库内 spine")
    g.add_argument("--drop", action="store_true", help="删除 spine 表")
    ap.add_argument("--book", default=None, help="只处理某书（配合 --build）")
    args = ap.parse_args()

    if not os.path.isfile(args.db):
        print("DB 不存在：%s" % args.db)
        return 1
    con = sqlite3.connect(args.db)

    if args.books:
        cmd_books(con)
    elif args.build:
        cmd_build(con, args.book)
    elif args.verify:
        return cmd_verify(con)
    elif args.drop:
        cmd_drop(con)
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
