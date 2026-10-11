"""《五杂俎》知识工程 | 职官任职层（APPT）打包器

源数据：_src/_appt_ai_<NN>.py
    RECORDS = [{
        item_id, person, office, institution, when, status, evidence,
        person_ent_ids?, official_ent_ids?, inst_ent_ids?
    }]
    person / office / institution 可写字符串（自动转嵌套字典）或字典；
    office 走实体表 type=official（职官）回填，institution 走 type=place/official；
    status 走 appt_status 枚举（12 值，含 未明）；when 未考处显式写 "未明"。

产物：_layers/appt_<NN>.json、_build/appt__summary.json、_build/_appt_logs.json

重跑：python build_appt.py [--volumes 05 06] [--check] [--rebuild-index]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_layer_runner import layer_cli  # noqa: E402
from _kg_pack_base import main_guard  # noqa: E402

TITLE = "职官任职层（APPT）"

if __name__ == "__main__":
    main_guard(lambda: layer_cli("appt", TITLE))
