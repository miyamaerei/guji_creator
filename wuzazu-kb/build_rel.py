"""《五杂俎》知识工程 | 关系层（REL）打包器

源数据：_src/_rel_ai_<NN>.py
    RECORDS = [{
        item_id, person_a, person_b, relation_type, direction, evidence
    }]
    person_a / person_b 可写字符串（自动转 {text, ent_ids}）；
    relation_type 走 relation_type 枚举（12 值，别名 主从 -> 上下级）；
    direction ∈ {单向, 双向, 未明}。

产物：_layers/rel_<NN>.json、_build/rel__summary.json、_build/_rel_logs.json

重跑：python build_rel.py [--volumes 05] [--check] [--rebuild-index]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_layer_runner import layer_cli  # noqa: E402
from _kg_pack_base import main_guard  # noqa: E402

TITLE = "关系层（REL）"

if __name__ == "__main__":
    main_guard(lambda: layer_cli("rel", TITLE))
