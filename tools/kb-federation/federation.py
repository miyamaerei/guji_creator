"""federation.py —— 联邦库 ELT CLI 入口

子命令：
  create     建库（schema + meta）
  collision  F0-a 撞号体检（固化撞号数字，作为装载前置断言）
  extract    仅抽取中间表（不入库，调试用）
  load       装载单书
  load-all   六书全量装载（F2）

用法：
  python federation.py create
  python federation.py collision
  python federation.py extract --book kzz
  python federation.py load --book kzz
  python federation.py load-all

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

# F2 装载顺序：先装最规整的 xyf 探路，再铺其余五本
LOAD_ORDER = ["xyf", "kzz", "wzz", "sdr", "qb", "xgf"]


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
    for b in LOAD_ORDER:
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
    print(f"六书全量装载完成：items={total_items}  records={total_rec}  "
          f"折叠丢失={total_lost}")
    if total_lost:
        print("⚠️ 存在主键折叠，联邦库未完整回本，请先修复 adapter 的 ID 命名空间！")
    else:
        print("✓ 撞号全部由复合主键 (book_id,layer_key,local_id) 消解，零折叠。")


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
    else:
        build_parser().print_help()


if __name__ == "__main__":
    main()
