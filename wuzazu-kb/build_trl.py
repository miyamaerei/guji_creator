"""《五杂俎》知识工程 | 古今翻译层（TRL）打包器

源数据：_src/_trl_ai_<NN>.py
    RECORDS = [{
        item_id, translation, style, note, confidence
    }]
    translation 为逐条今译正文，风格按 references/translation-style.md 的
    余光中风格七条基准（note 缺省自动写「余光中风格基准」）；
    style 走 trl_style 枚举；覆盖口径：条目数 = 翻译数（一条目一条译文）。

产物：_layers/trl_<NN>.json、_build/trl__summary.json、_build/_trl_logs.json

重跑：python build_trl.py [--volumes 01] [--check] [--rebuild-index]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_layer_runner import layer_cli  # noqa: E402
from _kg_pack_base import main_guard  # noqa: E402

TITLE = "古今翻译层（TRL）"

if __name__ == "__main__":
    main_guard(lambda: layer_cli("trl", TITLE))
