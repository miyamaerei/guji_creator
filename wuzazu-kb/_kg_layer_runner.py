"""《五杂俎》知识工程 | 各层打包器公共入口

每个 build_<layer>.py 都是这个函数的三行壳子：

    from _kg_layers import layer_cli, ENGINE
    from _kg_pack_base import main_guard
    if __name__ == "__main__":
        main_guard(lambda: layer_cli("event", "事件层（EVT）"))

约定：
- 缺省全量重跑；`--volumes 01 02` 只重算指定卷并增量并回共享汇总；
- `--check` 只统计不落盘；
- `--rebuild-index` 先按 _src/_ent_ai_NN.py 重建实体表，再打包本层；
- 无源数据的卷在 --volumes 模式下跳过，全量模式下写出空卷占位。
"""

from __future__ import annotations

from _kg_layers import describe, run_layer
from _kg_pack_base import (
    ALL_VOLUMES,
    VOLUME_NAME,
    banner,
    build_context,
    ensure_dirs,
    have_source,
    load_registry,
    load_sources,
    report_stats,
)


def layer_cli(layer: str, title: str) -> dict:
    args, vols = build_context(f"{title} 打包器")
    banner(f"{title} {layer}")

    if args.volumes is None:
        run_vols = list(vols)
    else:
        run_vols = [v for v in vols if have_source(layer, v)]
        skipped = [v for v in vols if v not in run_vols]
        if skipped:
            print(f"[提示] 以下卷无源数据 _src/_{layer}_ai_NN.py，已跳过：{skipped}")

    ensure_dirs()
    check = getattr(args, "check", False)
    if not check:
        load_registry()  # 缺指纹库立即报错，不留半成品

    sources = load_sources(layer, run_vols)
    stats = run_layer(layer, args, run_vols, sources=sources)
    stats["volumes_detail"] = ", ".join(f"{v}:{len(sources.get(v, []))}" for v in run_vols) or "-"
    report_stats(f"{title} 统计", stats)
    if not check:
        print(f"\n[产物] 每卷 JSON：_layers/{layer}_<NN>.json"
              f" | 汇总：_build/{layer}__summary.json"
              f" | 日志：_build/_{layer}_logs.json")
    return stats


def layer_fields(layer: str) -> dict:
    """打印某层字段契约（调试用：python -c "import _kg_layer_runner as r; ..."）。"""
    return describe(layer)


__all__ = ["ALL_VOLUMES", "VOLUME_NAME", "describe", "layer_cli", "layer_fields"]
