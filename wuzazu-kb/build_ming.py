"""《五杂俎》知识工程 | 明代纪事层（MING）打包器

源数据：_src/_ming_ai_<NN>.py
    RECORDS = [{
        item_id, era, who, what, when, where, category, first_person, ref_events?
    }]
    who 可写字符串（自动转 {text, ent_ids}）或字典；
    era 写年号（如 万历 / 嘉靖），when / where 未考处显式写 "未明"；
    first_person 写 true/false（作者是否亲历）；
    ref_events 引用事件层 ID（WZZ-E-004）。

产物：_layers/ming_<NN>.json、_build/ming__summary.json、_build/_ming_logs.json

重跑：python build_ming.py [--volumes 13] [--check] [--rebuild-index]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_layer_runner import layer_cli  # noqa: E402
from _kg_pack_base import main_guard  # noqa: E402

TITLE = "明代纪事层（MING）"

if __name__ == "__main__":
    main_guard(lambda: layer_cli("ming", TITLE))
