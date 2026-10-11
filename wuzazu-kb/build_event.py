"""《五杂俎》知识工程 | 事件层（EVT）打包器

源数据：_src/_event_ai_<NN>.py
    RECORDS = [{
        item_id, type, who, action, what, when, where, who_ent_ids?
    }]
    who 可写字符串（自动转 {text, who_ent_ids}），也可直接写字典；
    when / where 未考处必须显式写 "未明"；type 走 event_type 枚举（22 值 + 其他）。

产物：_layers/event_<NN>.json（顶层 records）、_build/event__summary.json、_build/_event_logs.json

重跑：python build_event.py [--volumes 01] [--check] [--rebuild-index]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_layer_runner import layer_cli  # noqa: E402
from _kg_pack_base import main_guard  # noqa: E402

TITLE = "事件层（EVT）"

if __name__ == "__main__":
    main_guard(lambda: layer_cli("event", TITLE))
