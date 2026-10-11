"""《五杂俎》知识工程 | 实体层（L1）打包器

源数据：_src/_ent_ai_<NN>.py，RECORDS = [{item_id, text, type, start?, end?, confidence?}]
产物：_layers/ent_<NN>.json + ent_keys.json（主键表/别名索引）+ ent_normalized_inventory.json
      + _build/ent_table.json + _build/ent_ambiguous.csv（同名异人待核）+ 每层引用所需的
      _layers/ent_index.json（词形 -> ENT 主键）。

重跑：python build_ent.py [--volumes 01 02] [--check]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_entity import run_ent_layer  # noqa: E402
from _kg_pack_base import (  # noqa: E402
    banner,
    build_context,
    ensure_dirs,
    have_source,
    load_registry,
    main_guard,
    report_stats,
)


def main() -> None:
    args, vols = build_context("实体层（L1）打包器")
    banner("实体层（L1）ent")
    if args.volumes is None:
        run_vols = list(vols)
    else:
        run_vols = [v for v in vols if have_source("ent", v)]
        skipped = [v for v in vols if v not in run_vols]
        if skipped:
            print(f"[提示] 以下卷无源数据 _src/_ent_ai_NN.py，已跳过：{skipped}")
    ensure_dirs()
    if not args.check:
        load_registry()
    stats = run_ent_layer(args, run_vols)
    report_stats("实体层统计", stats)
    if not args.check:
        print("\n[产物] _layers/ent_<NN>.json | ent_keys.json | ent_normalized_inventory.json | "
              "ent_index.json | _build/ent_table.json | _build/ent_ambiguous.csv")


if __name__ == "__main__":
    main_guard(main)
