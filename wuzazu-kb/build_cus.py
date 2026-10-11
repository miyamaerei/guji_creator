"""《五杂俎》知识工程 | 方言风俗层（CUS）打包器

源数据：_src/_cus_ai_<NN>.py
    RECORDS = [{
        item_id, type, region, term, description, region_ent_ids?
    }]
    region 可写字符串（自动转 {text, ent_ids}）或字典；
    type 走 cus_type 枚举；未考处（如不知何地）显式写 "未明"。

产物：_layers/cus_<NN>.json、_build/cus__summary.json、_build/_cus_logs.json

重跑：python build_cus.py [--volumes 03] [--check] [--rebuild-index]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _kg_layer_runner import layer_cli  # noqa: E402
from _kg_pack_base import main_guard  # noqa: E402

TITLE = "方言风俗层（CUS）"

if __name__ == "__main__":
    main_guard(lambda: layer_cli("cus", TITLE))
