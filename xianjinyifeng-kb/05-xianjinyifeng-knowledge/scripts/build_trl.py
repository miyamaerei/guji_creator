# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - TRL 古今翻译层打包器

源数据：data/_src/_trl_ai_<vol>.py（顶层键 trls；全覆盖要求：翻译数 = 条目数）
风格基准：直译为主、意译达意、专名保留+括注、四字格点缀
用法：python build_trl.py [--volumes 01,02] [--strict]
schema 见 05-xianjinyifeng-knowledge/references/schemas.md §8
"""

from __future__ import annotations

import _kg_layer_builder as builder

if __name__ == "__main__":
    raise SystemExit(builder.main_for("trl"))
