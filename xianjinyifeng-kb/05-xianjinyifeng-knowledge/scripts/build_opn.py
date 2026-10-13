# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - OPN 作者论说层打包器

源数据：data/_src/_opn_ai_<vol>.py（顶层键 opns；argument 只写要点概要不抄原文）
触发词：论曰/愚按/耿子曰/余按/予谓/余以为/余闻/盖尝论
用法：python build_opn.py [--volumes 01,02] [--strict]
schema 见 05-xianjinyifeng-knowledge/references/schemas.md §7
"""

from __future__ import annotations

import _kg_layer_builder as builder

if __name__ == "__main__":
    raise SystemExit(builder.main_for("opn"))
