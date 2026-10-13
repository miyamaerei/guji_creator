# -*- coding: utf-8 -*-
"""《先进遗风》知识工程基准管线 - APPT 职官任职层打包器

源数据：data/_src/_appt_ai_<vol>.py（顶层键 appointments；每条 = 一次任职）
用法：python build_appt.py [--volumes 01,02] [--strict]
schema 见 05-xianjinyifeng-knowledge/references/schemas.md §4
"""

from __future__ import annotations

import _kg_layer_builder as builder

if __name__ == "__main__":
    raise SystemExit(builder.main_for("appt"))
