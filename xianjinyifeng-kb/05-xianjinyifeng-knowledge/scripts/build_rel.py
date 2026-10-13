# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - REL 人物关系层打包器

源数据：data/_src/_rel_ai_<vol>.py（顶层键 relations；只建原文有直接证据的关系）
用法：python build_rel.py [--volumes 01,02] [--strict]
schema 见 05-xianjinyifeng-knowledge/references/schemas.md §5
"""

from __future__ import annotations

import _kg_layer_builder as builder

if __name__ == "__main__":
    raise SystemExit(builder.main_for("rel"))
