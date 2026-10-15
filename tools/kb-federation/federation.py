"""federation.py —— 联邦库 ELT CLI 入口

子命令：
  create     建库（schema + meta）
  collision  F0-a 撞号体检（固化撞号数字，作为装载前置断言）
  extract    仅抽取中间表（不入库，调试用）
  load       装载单书
  load-all   六书全量装载（F2）
  transform  T0–T3 去歧义（F3）+ 引用物化 + 裁决重放（F4）：nodes/edges/
             record_refs/canonical/members，名字归一配置驱动
  search     跨书搜索一个名字，返回全部成员 + 方法 + 置信度
  resolve    逐书解析一个名字（T1），看每个书里落到哪个 ent
  refs       重建 record_refs（物化 payload 内 *_ent_ids 引用边）
  assoc      关联查询（十三个：identity_bridge/person_network/career_chain/
             citation_network/work_author/place_culture/object_lineage/
             event_opinion/parallel_reading/dangling_refs/
             joint_timeline/salary_bridge/org_career_chain）
  conflicts  待人工复核的 conflict 成员
  lock       人工裁决（--action lock 确认同人 / reject 解除误并）
  unlock     撤销人工裁决
  enum-import 稀疏表填充：枚举库→enum_registry/enum_values + 漂移检测
  volumes    稀疏表填充：从 records 派生 volumes 目录表

用法：
  python federation.py create
  python federation.py collision
  python federation.py extract --book kzz
  python federation.py load --book kzz
  python federation.py load-all
  python federation.py transform
  python federation.py search 王忠毅公
  python federation.py resolve 王忠毅公
  python federation.py refs
  python federation.py assoc identity_bridge --name 苏轼
  python federation.py conflicts --limit 5
  python federation.py lock kzz:01:ENT-0136 --action lock --reason 确为同一人
  python federation.py unlock kzz:01:ENT-0136

零第三方依赖。所有路径相对仓库根解析，搬到任意机器都能跑。
"""

import os
import sys
import json
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))  # guji/
DEFAULT_DB = os.path.join(HERE, "kb.sqlite")

from kbdb import connect, ensure_schema  # noqa: E402
from collision import check_collision, format_report  # noqa: E402
from adapters import BOOK_ROOTS, BOOK_REGISTRY, BOOK_NAMES  # noqa: E402
from load import load_book  # noqa: E402
from extract import extract_book  # noqa: E402
from transform import run_transform  # noqa: E402
from query import FederationQuery  # noqa: E402
from name_resolver import load_rules  # noqa: E402
from assoc import AssocQuery  # noqa: E402
from curate import decide, list_conflicts, review_stats, undecide  # noqa: E402
from refs import materialize_refs  # noqa: E402

# F2 装载顺序：先装最规整的 xyf 探路，再铺其余五本。
# 注意：load-all 不再依赖此表——它遍历 BOOK_REGISTRY，新书登记后自动纳入。
# 此表仅用于给出「推荐装载次序」（探路书排前，便于早发现 adapter 问题）。
LOAD_ORDER = ["xyf", "kzz", "wzz", "sdr", "qb", "xgf"]


def load_order():
    """全量装载次序：LOAD_ORDER 里登记的排前面，其余按 BOOK_REGISTRY 登记顺序补齐。

    新增书只需在 adapters/__init__.py 登记 BOOK_REGISTRY，即自动纳入 load-all。
    """
    seen = [b for b in LOAD_ORDER if b in BOOK_REGISTRY]
    rest = [b for b in BOOK_REGISTRY if b not in seen]
    return seen + rest


def cmd_create(args):
    con = connect(args.db)
    ensure_schema(con)
    con.close()
    print(f"已建库：{args.db}（18 表就绪，FTS5 可用则建 fts_nodes）")


def cmd_collision(args):
    roots = {b: os.path.join(REPO_ROOT, r) for b, r in BOOK_ROOTS.items()}
    rep = check_collision(roots)
    print(format_report(rep))
    if rep["collisions"] == 0:
        print("\n⚠️ 未检测到撞号——复合主键隔离无可验证对象，请检查扫描路径。")
    return rep


def cmd_extract(args):
    slices = extract_book(args.book)
    print(f"{args.book} 发现层：")
    for k, s in slices.items():
        print(
            f"  {k:<6} kind={s.kind:<10} container={s.container_kind:<6} "
            f"前缀={s.id_prefix or '(item_id)'} 记录={len(s.records)}"
        )


def cmd_load(args):
    if args.book not in BOOK_REGISTRY:
        print(f"✗ 未注册 adapter：{args.book}（已注册：{', '.join(BOOK_REGISTRY)}）")
        return
    con = connect(args.db)
    ensure_schema(con)
    rep = load_book(con, args.book, wipe_first=not args.no_wipe)
    con.close()
    print(f"已装载 {BOOK_NAMES.get(args.book, args.book)}（{args.book}）")
    print(
        f"  items：{rep['items']}  records：{rep['records']}  "
        f"（去重主键 {rep['distinct']}，折叠 {rep['collision_lost']}）"
    )
    print(f"  catalog：{rep['catalog']}  fields：{rep['fields']}")
    print(f"  各层条数：{json.dumps(rep['layers'], ensure_ascii=False)}")


def cmd_load_all(args):
    con = connect(args.db)
    ensure_schema(con)
    total_rec = 0
    total_items = 0
    total_lost = 0
    for b in load_order():
        if b not in BOOK_REGISTRY:
            continue
        rep = load_book(con, b, wipe_first=True, commit=False)
        total_rec += rep["records"]
        total_items += rep["items"]
        total_lost += rep["collision_lost"]
        flag = " ⚠️折叠!" if rep["collision_lost"] else ""
        print(
            f"  {b} {BOOK_NAMES.get(b, b):<5} items={rep['items']:<5} "
            f"records={rep['records']:<6} layers={len(rep['layers'])}{flag}"
        )
    con.commit()
    con.close()
    print("-" * 50)
    print(
        f"全量装载完成（{len(load_order())} 本）：items={total_items}  records={total_rec}  "
        f"折叠丢失={total_lost}"
    )
    if total_lost:
        print("⚠️ 存在主键折叠，联邦库未完整回本，请先修复 adapter 的 ID 命名空间！")
    else:
        print("✓ 撞号全部由复合主键 (book_id,layer_key,local_id) 消解，零折叠。")


def cmd_transform(args):
    con = connect(args.db)
    ensure_schema(con)
    out = run_transform(con)
    con.close()
    print("F3 T0–T3 完成：")
    print(f"  nodes      ：{out['nodes']}")
    print(f"  edges      ：{out['edges']}（悬空 pending_refs {out['pending']}）")
    print(f"  candidates ：{out['candidates']}")
    t3 = out["t3"]
    print(
        f"  canonicals ：{t3['canonicals']}  members：{t3['members']}  "
        f"关系提升 {t3['relation_boosted']}（{t3['rounds']} 轮）"
    )


def cmd_search(args):
    con = connect(args.db)
    ensure_schema(con)
    q = FederationQuery(con)
    results = q.cross_search(args.name, type=args.type)
    if not results:
        print(f"未命中：{args.name}")
        con.close()
        return
    for r in results[: args.limit]:
        head = f"[{r['canonical_id'] or '独立'}] {r['repr_label']}"
        if r["repr_type"]:
            head += f" ({r['repr_type']})"
        print(f"{head}  best_conf={r['best_confidence']}")
        for m in r["members"]:
            print(
                f"    {m['book']}:{m['uid'].split(':', 1)[1]:<18} "
                f"label={m['label']}  {m['method']}={m['confidence']} "
                f"({m['status']})"
            )
        print()
    con.close()


def cmd_resolve(args):
    con = connect(args.db)
    ensure_schema(con)
    q = FederationQuery(con)
    out = q.resolve_across_books(args.name)
    if not out:
        print(f"未解析：{args.name}")
    for book, lst in out.items():
        for uid, method, conf in lst:
            print(f"  {book}:{uid.split(':', 1)[1]:<18} {method}={conf}")
    con.close()


def cmd_assoc(args):
    """执行关联查询（F4 的十三个查询之一）。"""
    con = connect(args.db)
    ensure_schema(con)
    aq = AssocQuery(con)
    kw = {"limit": args.limit}
    for k in ("name", "work", "author", "place", "keyword", "book_id", "reign"):
        v = getattr(args, k, None)
        if v:
            kw[k] = v
    if getattr(args, "predicates", None):
        kw["predicates"] = [p.strip() for p in args.predicates.split(",") if p.strip()]
    try:
        out = getattr(aq, args.query)(**kw)
    except AttributeError:
        print(f"✗ 未知查询：{args.query}")
        print("  可用：" + " / ".join(aq and [c["name"] for c in aq.catalog()]))
        con.close()
        return
    print(json.dumps(out, ensure_ascii=False, indent=2))
    con.close()


def cmd_conflicts(args):
    """待人工复核的 conflict 成员。"""
    con = connect(args.db)
    ensure_schema(con)
    print(json.dumps(review_stats(con), ensure_ascii=False))
    for c in list_conflicts(con, limit=args.limit, book_id=args.book):
        print(
            f"\n  {c['canonical_id']}  代表={c['canonical_repr']!r}({c['canonical_type']})"
        )
        print(
            f"    待判 {c['book']}:{c['uid'].split(':', 1)[1]}  {c['label']!r}  "
            f"{c['method']}={c['confidence']}"
        )
        for s in c["siblings"]:
            print(
                f"      兄弟 {s['book']}:{s['uid'].split(':', 1)[1]}  {s['label']!r}  "
                f"{s['confidence']} [{s['status']}]"
            )
        print(f"    建议：{c['suggestion']}")
    con.close()


def cmd_lock(args):
    """人工裁决：--action lock（确认同人）/ reject（解除误并）。"""
    con = connect(args.db)
    ensure_schema(con)
    try:
        out = decide(
            con,
            args.uid,
            args.action,
            canonical_id=args.canonical_id,
            reason=args.reason,
            decided_by="cli",
        )
    except ValueError as e:
        print("✗ %s" % e)
        con.close()
        return
    print(json.dumps(out, ensure_ascii=False))
    print("（裁决已记录；重跑 transform 会由 replay_overrides 自动重放）")
    con.close()


def cmd_unlock(args):
    """撤销人工裁决。"""
    con = connect(args.db)
    ensure_schema(con)
    try:
        print(json.dumps(undecide(con, args.uid), ensure_ascii=False))
    except ValueError as e:
        print("✗ %s" % e)
    con.close()


def cmd_refs(args):
    """重建 record_refs（物化 payload 内的 *_ent_ids 引用边）。"""
    con = connect(args.db)
    ensure_schema(con)
    stats = materialize_refs(con, book_id=args.book)
    print(json.dumps(stats, ensure_ascii=False))
    con.close()


def cmd_enum_import(args):
    """稀疏表填充（一）：枚举基准库 → enum_registry / enum_values + 漂移检测。"""
    from enum_import import import_enums, compute_drift  # 局部导入避免环

    con = connect(args.db)
    ensure_schema(con)
    imp = import_enums(con)
    print(
        "枚举导入：groups=%d values=%d (顶层 %d)"
        % (imp["groups"], imp["values"], imp["tops"])
    )
    if not args.no_drift:
        dr = compute_drift(con)
        print(
            "漂移检测：distinct=%d rows=%d" % (dr["distinct_values"], dr["drift_rows"])
        )
    con.close()


def cmd_volumes(args):
    """稀疏表填充（二）：从 records 派生填充 volumes 目录表。"""
    from volumes import populate_volumes  # 局部导入避免环

    con = connect(args.db)
    ensure_schema(con)
    out = populate_volumes(con)
    print("volumes 填充：%d 行" % out["volumes"])
    con.close()


def cmd_source_rev(args):
    """回填 books.source_rev（源工程目录的 git rev / 目录指纹）—— 增量水印。

    已注册但 source_rev 为 NULL 的书会被补全；已非空的书默认跳过（--force 重算）。
    下次 load / load-all 也会由 register_catalog 自动写入。
    """
    from load import source_rev  # 局部导入避免环

    con = connect(args.db)
    ensure_schema(con)
    n = 0
    for b in sorted(BOOK_REGISTRY):
        cur = con.execute(
            "SELECT source_rev FROM books WHERE book_id=?", (b,)
        ).fetchone()
        if cur and cur[0] and not args.force:
            continue
        rev = source_rev(b)
        if rev is None:
            print(f"  {b}: 无 source_root / 计算失败，跳过")
            continue
        con.execute(
            "INSERT INTO books(book_id,code,name,source_root,status,source_rev) "
            "VALUES(?,?,?,?,?,?) "
            "ON CONFLICT(book_id) DO UPDATE SET source_rev=excluded.source_rev",
            (b, b, BOOK_NAMES.get(b, b), BOOK_REGISTRY[b].get("root"), "active", rev),
        )
        n += 1
        print(
            f"  {b}: {rev[:12]}…"
            if rev.startswith(("dir:",)) or len(rev) > 12
            else f"  {b}: {rev}"
        )
    con.commit()
    con.close()
    print("source_rev 回填：%d 本" % n)


def build_parser():
    p = argparse.ArgumentParser(prog="federation", description="古籍联邦库 ELT")
    sub = p.add_subparsers(dest="cmd")

    pc = sub.add_parser("create", help="建库（schema + meta）")
    pc.add_argument("--db", default=DEFAULT_DB)

    pcol = sub.add_parser("collision", help="撞号体检（F0-a）")
    pcol.add_argument("--db", default=DEFAULT_DB)

    pe = sub.add_parser("extract", help="仅抽取中间表（不入库）")
    pe.add_argument("--book", required=True)

    pl = sub.add_parser("load", help="装载单书")
    pl.add_argument("--book", required=True)
    pl.add_argument("--db", default=DEFAULT_DB)
    pl.add_argument("--no-wipe", action="store_true", help="不清空重装")

    pa = sub.add_parser("load-all", help="六书全量装载（F2）")
    pa.add_argument("--db", default=DEFAULT_DB)

    pt = sub.add_parser("transform", help="T0–T3 去歧义 + 引用物化 + 裁决重放（F3/F4）")
    pt.add_argument("--db", default=DEFAULT_DB)

    ps = sub.add_parser("search", help="跨书搜索（带置信度）")
    ps.add_argument("name")
    ps.add_argument("--db", default=DEFAULT_DB)
    ps.add_argument("--type", default=None, help="限定类型 person/place/...")
    ps.add_argument("--limit", type=int, default=3)

    pr = sub.add_parser("resolve", help="逐书解析一个名字（T1）")
    pr.add_argument("name")
    pr.add_argument("--db", default=DEFAULT_DB)

    pref = sub.add_parser("refs", help="重建 record_refs（物化引用边）")
    pref.add_argument("--db", default=DEFAULT_DB)
    pref.add_argument("--book", default=None, help="只重建某书（缺省全库）")

    pas = sub.add_parser("assoc", help="关联查询（F4 十三个查询之一）")
    pas.add_argument("query")
    pas.add_argument("--db", default=DEFAULT_DB)
    pas.add_argument("--limit", type=int, default=20)
    for k, h in (
        ("name", "人名/名物名"),
        ("work", "被引书名"),
        ("author", "作者名"),
        ("place", "地名"),
        ("keyword", "关键词"),
        ("predicates", "关系类型过滤（逗号分隔）"),
        ("reign", "年号过滤（joint_timeline，如 嘉靖）"),
    ):
        pas.add_argument("--" + k, default=None, help=h)

    pcf = sub.add_parser("conflicts", help="待人工复核的 conflict 成员")
    pcf.add_argument("--db", default=DEFAULT_DB)
    pcf.add_argument("--limit", type=int, default=10)
    pcf.add_argument("--book", default=None)

    plk = sub.add_parser("lock", help="人工裁决（lock 确认同人 / reject 解除误并）")
    plk.add_argument("uid")
    plk.add_argument("--action", default="lock", choices=["lock", "reject"])
    plk.add_argument("--canonical-id", default=None)
    plk.add_argument("--reason", default=None)
    plk.add_argument("--db", default=DEFAULT_DB)

    pul = sub.add_parser("unlock", help="撤销人工裁决")
    pul.add_argument("uid")
    pul.add_argument("--db", default=DEFAULT_DB)

    pen = sub.add_parser(
        "enum-import", help="稀疏表填充：枚举库→enum_registry/enum_values + 漂移检测"
    )
    pen.add_argument("--db", default=DEFAULT_DB)
    pen.add_argument("--no-drift", action="store_true", help="跳过漂移检测")

    pvol = sub.add_parser("volumes", help="稀疏表填充：从 records 派生 volumes 目录表")
    pvol.add_argument("--db", default=DEFAULT_DB)

    psr = sub.add_parser("source-rev", help="回填 books.source_rev（增量水印）")
    psr.add_argument("--db", default=DEFAULT_DB)
    psr.add_argument("--force", action="store_true", help="重算已非空的书")

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.cmd == "create":
        cmd_create(args)
    elif args.cmd == "collision":
        cmd_collision(args)
    elif args.cmd == "extract":
        cmd_extract(args)
    elif args.cmd == "load":
        cmd_load(args)
    elif args.cmd == "load-all":
        cmd_load_all(args)
    elif args.cmd == "transform":
        cmd_transform(args)
    elif args.cmd == "search":
        cmd_search(args)
    elif args.cmd == "resolve":
        cmd_resolve(args)
    elif args.cmd == "refs":
        cmd_refs(args)
    elif args.cmd == "assoc":
        cmd_assoc(args)
    elif args.cmd == "conflicts":
        cmd_conflicts(args)
    elif args.cmd == "lock":
        cmd_lock(args)
    elif args.cmd == "unlock":
        cmd_unlock(args)
    elif args.cmd == "enum-import":
        cmd_enum_import(args)
    elif args.cmd == "volumes":
        cmd_volumes(args)
    elif args.cmd == "source-rev":
        cmd_source_rev(args)
    else:
        build_parser().print_help()


if __name__ == "__main__":
    main()
