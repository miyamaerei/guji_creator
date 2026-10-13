# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - L5 事件层打包器

源数据：data/_src/_event_ai_<vol>.py（顶层键 events；五元组，未明显式写「未明」）
用法：python build_event.py [--volumes 01,02] [--strict]
schema 见 05-xianjinyifeng-knowledge/references/schemas.md §6
"""

from __future__ import annotations

import _kg_layer_builder as builder

if __name__ == "__main__":
    raise SystemExit(builder.main_for("event"))
