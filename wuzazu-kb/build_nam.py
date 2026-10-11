"""《五杂俎》知识工程 | 名录谱牒层（NAM）打包器

源数据：_src/_nam_ai_<NN>.py
    RECORDS = [{
        item_id, name, category, scope,
        entries: [{seq?, person, courtesy_name, hometown, office}, ...],
        ent_ids?
    }]
    entries 缺 seq 时按出现顺序自动补 1..n；
    category 走 nam_category 枚举；ent_ids 缺省时按 entries.person 词形回填。

产物：_layers/nam_<NN>.json、_build/nam__summary.json、_build/_nam_logs.json

重跑：python build_nam.py [--volumes 05] [--check] [--rebuild-index]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_layer_runner import layer_cli  # noqa: E402
from _kg_pack_base import main_guard  # noqa: E402

TITLE = "名录谱牒层（NAM）"

if __name__ == "__main__":
    main_guard(lambda: layer_cli("nam", TITLE))
